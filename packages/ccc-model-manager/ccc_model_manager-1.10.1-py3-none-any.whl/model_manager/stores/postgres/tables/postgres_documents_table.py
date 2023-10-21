#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

import json
import logging
import typing

from model_manager.common.serializable import Serializable
from model_manager.stores.model_store import VersionedRef
from model_manager.stores.postgres.postgres_utils import PostgresQueryHelper
from model_manager.stores.postgres.tables.postgres_table import PostgresTable

_logger = logging.getLogger(__name__)


class PostgresDocumentsTable(PostgresTable):
    __table_name__ = 'documents'

    """
    Postgres object store - stores and retrieves Serializable instances as JSON documents,
    the instances are roughly organized in collections corresponding to their class names.
    This store is used internally by the Postgres(Task/Dataset/Model)Store.
    """

    def __init__(self, connection_info: dict, cls: typing.Type[Serializable]):
        super().__init__(connection_info)
        self._cls = cls
        self._cls_name = cls.__name__.lower()
        self._query_helper = PostgresQueryHelper(self.connection_handler)

    def _create_tables_and_indexes(self):
        commands = [
            """
            create table if not exists documents (
                doc_type    varchar (32) not null,
                doc_name    varchar (64) not null,
                doc_version varchar (64) not null,
                ts          numeric not null,
                doc         jsonb not null
            );
            """,
            f"""
            alter table {self.__table_name__} add column if not exists access_ts timestamp with time zone default (now() at time zone 'utc')
            """,
            f"""
            create index if not exists {self.__table_name__}_access_ts_idx on {self.__table_name__} (access_ts)
            """,
            """
            create index if not exists documents_id_idx on documents (doc_type, doc_name, doc_version)
            """,
            """
            create index if not exists documents_ts_idx on documents (doc_type, doc_name, ts)
            """,
            """
            create index if not exists documents_docs_gin on documents using gin(doc jsonb_path_ops)
            """
        ]
        self._query_helper.execute(commands)

    def _delete_all_tables_and_indexes(self):
        commands = [
            """
            drop table if exists documents;
            """,
            """
            drop index if exists documents_id_idx;
            """,
            """
            drop index if exists documents_ts_idx;
            """,
            f"""
            drop index if exists {self.__table_name__}_access_ts_idx
            """,
            """
            drop index if exists documents_docs_gin;
            """
        ]
        self._query_helper.execute(commands)

    def get_object(self, name: str, version: str) -> typing.Optional[Serializable]:
        query_params = (self._cls_name, name, version)
        row = self._query_helper.get_one("select doc, access_ts from documents where doc_type=%s and doc_name=%s and doc_version=%s", query_params)

        if row is None:
            return None
        if self.must_update_last_accessed_ts(row[1]):
            self._query_helper.execute([(
                f"update {self.__table_name__} set access_ts='{self.now()}' where doc_type=%s and doc_name=%s and doc_version=%s",
                query_params
            )])
        serialized = row[0]
        if serialized is None:
            return None
        # TODO psycopg can directly manipulate Python objects instead of needing to convert to string
        # see http://initd.org/psycopg/docs/extras.html
        data = serialized
        return self._cls.deserialize(data=data)

    def add_object(self, name: str, version: str, ts: float, instance: Serializable):
        data = instance.serialize()
        serialized = json.dumps(data)
        self._create_tables_and_indexes()
        self._query_helper.execute([(
            "insert into documents (doc_type, doc_name, doc_version, ts, access_ts, doc) values (%s, %s, %s, %s, %s, %s);",
            (self._cls_name, name, version, ts, self.now(), serialized)
        )])

    def purge(self, object_refs: typing.Set[VersionedRef]):
        # name_version_pairs = [(f"'{ref.name}'", f"'{ref.version}'") for ref in object_refs]
        name_version_pairs = [(ref.name, ref.version) for ref in object_refs]
        # VJAN-3386: Workaround to enable db tracing,
        # connection & cursor created inside with-resources block are not being traced
        conn = self.connection_handler.get_conn()
        with conn:
            cur = conn.cursor()
            with cur:
                cur.executemany(
                    "delete from documents where doc_name=%s and doc_version=%s", name_version_pairs)
                conn.commit()

    def update_object(self, updates: dict, name: str, ts: float, version: str):
        obj = self.get_object(name, version)
        obj_dict = obj.serialize()
        obj_dict.update(updates)

        serialized = json.dumps(obj_dict)
        self._query_helper.execute([(
            "update documents set doc = %s, ts = %s, access_ts = %s where doc_type = %s and doc_name = %s and doc_version = %s",
            (serialized, ts, self.now(), self._cls_name, name, version)
        )])

    def get_versions(self, name: str) -> typing.List[str]:
        """
        Finds the versions matching the provided name

        :param name:
        :return:
        """
        return self.query_versions(name, False, None, None)

    def query_versions(self, name: str, latest: bool = True, tags: dict = None, org_id: str = None,
                       min_time: float = None, max_time: float = None) -> typing.List[str]:

        if latest:
            assert name

        where_clause, query_params = self.create_query(name)
        where_clause, query_params = self.update_query_with_tags(tags, where_clause, query_params)
        where_clause, query_params = self.update_query_with_org_id(org_id, where_clause, query_params)
        where_clause, query_params = self.update_query_with_time_range(min_time, max_time, where_clause, query_params)

        select_clause = "doc_version"
        rows = self.run_query(latest, select_clause, where_clause, query_params)

        return [row[0] for row in rows] if rows else []

    def query_latest_versions(self, doc_name: str):
        self._create_tables_and_indexes()
        query = f"SELECT MAX(doc_version), doc->>'org_id' as org_id FROM documents" \
                f" WHERE doc_name ='{doc_name}' AND doc_type ='{self._cls_name}'" \
                f" GROUP BY doc->>'org_id';"
        rows = self._query_helper.get_all(query, None)
        return [(row[0]) for row in rows] if rows else []

    def query_refs(self, tags: dict = None, org_id: str = None, min_time: float = None, max_time: float = None) -> typing.List[str]:
        where_clause, query_params = self.create_query(name=None)
        where_clause, query_params = self.update_query_with_tags(tags, where_clause, query_params)
        where_clause, query_params = self.update_query_with_org_id(org_id, where_clause, query_params)
        where_clause, query_params = self.update_query_with_time_range(min_time, max_time, where_clause, query_params)

        select_clause = "doc_name, doc_version"
        rows = self.run_query(False, select_clause, where_clause, query_params)
        return [(row[0], row[1]) for row in rows] if rows else []

    def run_query(self, latest: bool, select_clause: str, where_clause: str, query_params: typing.List[str]):
        if latest:
            query = f"select {select_clause} from documents where " \
                f"doc_type='{self._cls_name}' and " \
                f"ts = (select max(ts) from documents where {where_clause})"
        else:
            query = f"select {select_clause} from documents where {where_clause} order by ts desc"
        # TODO do this in chunks but anyway this all assumes all must fit in memory
        rows = self._query_helper.get_all(query, query_params)
        return rows

    def create_query(self, name: typing.Optional[str]) -> typing.Tuple[str, typing.List[str]]:
        where_clause = "doc_type=%s"
        query_params = [self._cls_name]
        if name:
            where_clause = where_clause + " and doc_name = %s"
            query_params.append(name)
        return where_clause, query_params

    def update_query_with_jsonb_query(self, json_query: dict, where_clause: str, query_params: typing.List[str]) -> \
            typing.Tuple[str, typing.List[str]]:
        """
        Adds jsonb containment operator query to where_clause and query_params.
        :param json_query: jsonb dictionary to query
        :param where_clause: string
        :param query_params: query parameters
        :return: where_clause, query_params
        """
        where_clause = where_clause + f" and doc@>%s"
        query_params.append(json.dumps(json_query))
        return where_clause, query_params

    def update_query_with_tags(self, tags, where_clause, query_params) -> typing.Tuple[str, typing.List[str]]:
        if tags is not None:
            # this builds a query like:
            # select doc d from docs where
            # "docType" = 'test' and doc@>json.dumps({"tags":tags})
            where_clause, query_params = self.update_query_with_jsonb_query(
                json_query={"tags": tags}, where_clause=where_clause,
                query_params=query_params)
        return where_clause, query_params

    def update_query_with_org_id(self, org_id, where_clause, query_params):
        if org_id is not None:
            # checking both org_ids and org_id for backward compatibility
            where_clause = where_clause + "and (doc->>'org_id'=%s or doc->'org_ids'@>to_jsonb(%s::text))"
            query_params.extend([org_id] * 2)
        return where_clause, query_params

    def update_query_with_time_range(self, min_time, max_time, where_clause, query_params):
        if min_time:
            where_clause = where_clause + "and ts >= %s"
            query_params.append(min_time)
        if max_time:
            where_clause = where_clause + "and ts <= %s"
            query_params.append(max_time)
        return where_clause, query_params
