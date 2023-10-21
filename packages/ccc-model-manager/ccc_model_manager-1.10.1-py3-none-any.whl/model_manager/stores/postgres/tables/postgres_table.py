# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
import typing
from datetime import datetime, timezone, timedelta
from typing import Tuple, List

from model_manager.common.serializable import Serializable
from model_manager.stores.postgres.postgres_utils import PostgresConnectionHandler, PostgresQueryHelper

"""
Stores can be implemented so as to use underlying Tables dervied from this class.
To be used primarily for kubernetes deployments.
"""

import logging

_logger = logging.getLogger(__name__)


class PostgresTable(object):
    __table_name__ = "<UNDEFINED>"

    """
    An abstract representation of a table in the Postgres database, with a few default implementations
    """

    LAST_ACCESSED_UPDATE_PERIOD_SECS = 7 * 24 * 60 * 60

    def __init__(self, connection_info: dict):
        self._conn_info = connection_info
        self.connection_handler = PostgresConnectionHandler(connection_info)

    def _create_tables_and_indexes(self):
        """
        Create table and add indexes if missing
        :return:
        """
        raise NotImplementedError

    def _delete_all_tables_and_indexes(self):
        """
        Drop tables and all indexes
        :return:
        """
        raise NotImplementedError

    def get_object(self, **kwargs) -> typing.Optional[Serializable]:
        """
        Fetches a single row from the table.
        :param kwargs: key-value pair to identify the row, fetches first if db returns many
        :return:
        """
        raise NotImplementedError

    def add_object(self, **kwargs):
        """
        Insert a row in the table
        :param kwargs: key-value pair containing row information
        :return:
        """
        raise NotImplementedError

    def update_object(self, updates: dict, **kwargs):
        """
        Atomically updates an object using the changes described in the updates argument.
        :param updates: a dict containing the updates to make to the row
        :param kwargs: key-value pair to identify the row, fetches first if db returns many
        :return:
        """
        raise NotImplementedError

    def run_query(self, latest: bool, select_clause: str, where_clause: str, query_params: typing.List[str]):
        """
        Run any query any query on the table
        :param latest: use max(ts) to identify most recent entry
        :param select_clause:
        :param where_clause:
        :param query_params:
        :return: uses fetchall() to return everything
        """
        raise NotImplementedError

    def create_query(self, name: typing.Optional[str]) -> typing.Tuple[str, typing.List[str]]:
        """
        Used to create where_clause and query params for arbitrary queries. Usually used in tandem with run_query()
        :param name:
        :return:
        """
        raise NotImplementedError

    def purge_non_accessed_data(self, purge_before_epoch_secs: datetime, dry_run=False, where_params: dict = None,
                                log_columns: list = None) -> Tuple[int, List]:
        """
        Purge records which have not been accessed since the given timestamp.
        For tracking and logging it's useful to know which entries were purged: log_columns allows specifying
        rows that were deleted.
        :param purge_before_epoch_secs: non accessed rows before this datetime will be purged
        :param dry_run: controls if to really purge/dry run the motion
        :param where_params: specify additional filtering when purging the table (e.g. on a doc_type). Specifically
        used by overloaded tables like documents table - which is used for storing hyperparams, models, dataset metadata
        :param log_columns: used for tracking the rows that could/would be deleted
        :return: a tuple with deleted rowcount (0 if dry run) and a list of eligible rows
        """

        # in case there's other parameters to filter purging on
        where_str, query_params = PostgresQueryHelper.parse_where_clause(where_params)
        where_str = f"{where_str} and access_ts < %s" if where_str else "where access_ts < %s"
        query_params.append(purge_before_epoch_secs)

        purged_rows = []
        deleted_count = 0
        # VJAN-3386: Workaround to enable db tracing,
        # connection & cursor created inside with-resources block are not being traced
        conn = self.connection_handler.get_conn()
        with conn:
            cur = conn.cursor()
            with cur:
                if log_columns:
                    select_str = PostgresQueryHelper.parse_select_clause(log_columns)
                    cur.execute(f"{select_str} from {self.__table_name__} {where_str}", query_params)
                    purged_rows = cur.fetchall()
                    _logger.info(f"found {len(purged_rows)} entries to delete from table: {self.__table_name__}")
                if not dry_run:
                    cur.execute(f"delete from {self.__table_name__} {where_str}", query_params)
                    deleted_count = cur.rowcount
                    _logger.info(f"deleted {deleted_count} entries from table: {self.__table_name__}")
            conn.commit()
        return deleted_count, purged_rows

    def must_update_last_accessed_ts(self, access_ts: datetime) -> bool:
        return access_ts < self.now() - timedelta(seconds=self.LAST_ACCESSED_UPDATE_PERIOD_SECS)

    @staticmethod
    def now() -> datetime:
        return datetime.now(timezone.utc)
