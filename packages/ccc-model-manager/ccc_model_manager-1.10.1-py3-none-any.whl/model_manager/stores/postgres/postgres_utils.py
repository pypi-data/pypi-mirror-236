# Copyright (c) 2022 VMware, Inc. All Rights Reserved.

import logging
import time
import typing
from typing import Tuple, List

import psycopg2
from model_manager.stores.postgres.postgres import PORT, HOST

_logger = logging.getLogger(__name__)
MAX_RETRIES = 5


class PostgresConnectionHandler(object):

    def __init__(self, connection_info):
        self._conn_info = connection_info
        self._conn = None
        self._connect()

    def _connect(self, retry_counter=0):

        # defaults
        conn_info = {
            # Use following structure to fill in connection values
            # HOST: 'localhost',
            # PORT: 5432,
            # DATABASE: 'postgres',
            # USER: 'postgres',
            # PASSWORD: <PASSWORD>,
            # "connect_timeout": 10
        }

        # override with user settings
        conn_info.update(self._conn_info)

        # connect
        try:
            _logger.info(f"Connecting to database: {conn_info.get(HOST)}:{conn_info.get(PORT)}. "
                         f"Attempt {retry_counter} of {MAX_RETRIES}")
            self._conn = psycopg2.connect(**conn_info)
        except (Exception, psycopg2.Error) as error:
            if retry_counter >= MAX_RETRIES:
                raise error from None  # pep 409 supressing exception context
            else:
                time.sleep(5)
                self._connect(retry_counter + 1)

    def get_conn(self):
        try:
            cur = self._conn.cursor()
            # this puts an extra query load on the DB but we do
            # not have that high DB reads to make it a problem.
            # Stable connections more important to have reliable checkpoints over longer training
            cur.execute("SELECT 1")  # sample query to check connection
            cur.close()
        except psycopg2.Error as error:
            self._connect()
        return self._conn


class PostgresQueryHelper(object):
    def __init__(self, connection_handler: PostgresConnectionHandler):
        self._connection_handler = connection_handler

    def execute(self, commands):
        # VJAN-3386: Workaround to enable db tracing,
        # connection & cursor created inside with-resources block are not being traced
        conn = self._connection_handler.get_conn()
        with conn:
            cur = conn.cursor()
            with cur:
                # execute commands
                for command in commands:
                    if isinstance(command, tuple):
                        query, params = command
                        cur.execute(query, params)
                    else:
                        cur.execute(command)
            conn.commit()

    def get_one(self, query_clause, query_params=None) -> typing.Optional[typing.Tuple]:
        # returns a single sequence
        # VJAN-3386: Workaround to enable db tracing,
        # connection & cursor created inside with-resources block are not being traced
        conn = self._connection_handler.get_conn()
        with conn:
            cur = conn.cursor()
            with cur:
                cur.execute(query_clause, query_params)
                row = cur.fetchone()
        return row

    def get_all(self, query_clause, query_params=None) -> typing.List[typing.Tuple]:
        # returns all matching sequences
        # VJAN-3386: Workaround to enable db tracing,
        # connection & cursor created inside with-resources block are not being traced
        conn = self._connection_handler.get_conn()
        with conn:
            cur = conn.cursor()
            with cur:
                cur.execute(query_clause, query_params)
                # TODO this all assumes all must fit in memory
                rows = cur.fetchall()
        return rows

    def delete_all(self, delete_clause):
        self.execute(delete_clause)
        self._connection_handler.get_conn().close()

    @staticmethod
    def parse_where_clause(where_dict: dict, query_params=None) -> Tuple[str, List[str]]:
        """
        Takes a dict where the key is the column name for where clause and the valus is the value to filter on.
        Example:

         parse_where_clause({})
         ('', [])

         parse_where_clause({'doc_type': 'metadata', 'doc_version': '1234'})
         ('where doc_type=%s and doc_version=%s', ['metadata', '1234'])

        Note: Cannot handle complicated expressions like "in" yet. We haven't had the need for it.

        :param where_dict: dict for where clause
        :param query_params: if query_params from previous queries
        :return: tuple of where clause and query params
        """

        query_params = query_params if query_params else []

        if not where_dict:
            where_str = ''
            # emtpy dict == no where clause
            return where_str, query_params

        if not all(where_dict.keys()) or not all(where_dict.values()):
            raise ValueError(f"Bad input to parse where clause: {where_dict}")

        where_str = "where " + "=%s and ".join(where_dict.keys())
        where_str = where_str + '=%s'
        query_params.extend(list(where_dict.values()))

        return where_str, query_params

    @staticmethod
    def parse_select_clause(select_list: list) -> str:
        """
        Takes a list of params to select as input and returns a SQL legible select string

        Examples
        --------
        >> parse_select_clause([])
        ValueError: Cannot parse NoneType or empty for select string

        >> parse_select_clause([''])
        ValueError: One or more params in select_list: [''] are falsy. Malformed select str

        >> parse_select_clause(['doc_type', 'doc_name'])
        'select doc_type, doc_name'

        :param select_list: list
        :return: SQL select string
        """
        if not select_list:
            # emtpy dict == no select clause, not allowed
            raise ValueError("Cannot parse NoneType or empty for select string")

        if not all(select_list):
            raise ValueError(f"One or more params in select_list: {select_list} are falsy. Malformed select str")

        select_str = ', '.join(select_list)
        return 'select ' + select_str

    @staticmethod
    def parse_postgres_results(log_columns: list, rows: list):
        result = []
        for row in rows:
            per_row_dict = {col: row[idx] for idx, col in enumerate(log_columns)}
            result.append(per_row_dict)
        return result
