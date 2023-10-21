# Copyright (c) 2022 VMware, Inc. All Rights Reserved.

import logging
import time
from typing import Tuple, List

from model_manager.stores.postgres.postgres_utils import PostgresQueryHelper
from model_manager.stores.postgres.tables.postgres_table import PostgresTable

_logger = logging.getLogger(__name__)


class PostgresS3BlobMetadataTable(PostgresTable):
    __table_name__ = 's3_blobs_metadata'

    def __init__(self, connection_info: dict):
        super().__init__(connection_info)
        self.query_helper = PostgresQueryHelper(self.connection_handler)

    def _create_tables_and_indexes(self):
        """
        Create table and add indexes if missing
        :return:
        """
        create_clauses = [
            f"""
            create table if not exists {self.__table_name__} (
                address        varchar (512) not null,
                created_ts     numeric default extract(epoch from now()),
                access_ts      timestamptz default (now() at time zone 'utc'),
                PRIMARY KEY (address)
            )
            """
        ]
        self.query_helper.execute(create_clauses)

    def _delete_all_tables_and_indexes(self):
        """
        Drop tables and all indexes
        :return:
        """
        delete_clauses = [
            f"""
            drop table if exists {self.__table_name__};
            """
        ]
        self.query_helper.execute(delete_clauses)

    def create_query(self, select_clause: list, where_clause: dict, query_params: list = None) -> Tuple[str, List[str]]:
        """
        Returns a query str with query params
        :return:
        """
        query_params = query_params if query_params else []
        select_str = self.query_helper.parse_select_clause(select_clause)
        where_str, query_params = self.query_helper.parse_where_clause(where_clause, query_params)

        query = f"{select_str} from {self.__table_name__} {where_str}"

        return query, query_params

    def run_query(self, select_clause: list, where_clause: dict, query_params: List[str] = None):
        """
        Calls parse_where_clause(dict) and parse_select_clause(str) to generate SQL query string
        """
        query_str, query_params = self.create_query(select_clause, where_clause, query_params)
        rows = self.query_helper.get_all(query_str, query_params)
        return rows

    def add_object(self, address):
        query_clause = f"insert into {self.__table_name__} (address, created_ts, access_ts) values (%s, %s, %s);"
        query_params = (address, time.time(), self.now())
        self._create_tables_and_indexes()
        return self.query_helper.execute([(query_clause, query_params)])

    def get_object(self, address: str):
        query_clause = f"select access_ts from {self.__table_name__} where address = %s;"
        query_params = (address,)
        res = self.query_helper.get_one(query_clause, query_params)
        if not res:
            return res

        if self.must_update_last_accessed_ts(res[0]):
            self.query_helper.execute(
                [(f"update {self.__table_name__} set access_ts='{self.now()}' where address=%s", query_params)])
        return res[0]

    def delete_object(self, address: str):
        query_clause = f"delete from {self.__table_name__} where address=%s"
        query_params = (address,)

        return self.query_helper.execute([(query_clause, query_params)])

    def bulk_insert_from_file(self, file_name: str, columns: Tuple):
        # VJAN-3386: Workaround to enable db tracing,
        # connection & cursor created inside with-resources block are not being traced
        conn = self.connection_handler.get_conn()
        with conn:
            cur = conn.cursor()
            with cur:
                with open(file_name, mode='r') as f:
                    cur.copy_from(f, table=self.__table_name__, sep=',', columns=columns)
                conn.commit()
        _logger.info("Done inserting bulk records")
