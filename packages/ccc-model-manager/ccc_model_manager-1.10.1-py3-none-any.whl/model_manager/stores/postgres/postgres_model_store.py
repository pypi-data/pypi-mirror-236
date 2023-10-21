#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

import time
import typing
from datetime import datetime

from model_manager.stores.model_store import ModelMetadata, ModelStore, ModelRef
from model_manager.stores.postgres.postgres_utils import PostgresQueryHelper
from model_manager.stores.postgres.tables.postgres_documents_table import PostgresDocumentsTable

PROD_VERSION = '1.0'  # TODO xxxjiayi, find a better way to define the product version.


class PostgresModelStore(ModelStore):
    def __init__(self, connection_info: dict):
        self._store = PostgresDocumentsTable(connection_info=connection_info, cls=ModelMetadata)

    def get_metadata(self, model_ref: ModelRef) -> ModelMetadata:
        # noinspection PyTypeChecker
        m: ModelMetadata = self._store.get_object(name=model_ref.name, version=model_ref.version)
        return m

    def get_model_versions(self, name: str) -> typing.List[ModelRef]:
        versions = self._store.get_versions(name=name)
        return [ModelRef(name=name, version=v) for v in versions]

    def store_metadata(self, metadata: ModelMetadata) -> ModelRef:
        ts = time.time()
        metadata.creation_time = ModelMetadata.timestamp_to_timestr(ts)

        if metadata.version:
            raise ValueError("metadata.version must not be set as it is assigned by the store")
        version = "{}_{}".format(PROD_VERSION, "{0:%Y-%m-%d-%H:%M:%S}".format(datetime.utcfromtimestamp(ts)))
        metadata.version = version
        model_ref = ModelRef(name=metadata.name, version=version, type=metadata.model_type)
        self._store.add_object(name=metadata.name, version=metadata.version, ts=ts, instance=metadata)
        return model_ref

    def update_metadata(self, metadata: ModelMetadata):
        # If the version was not set, raise a value error
        if not metadata.version:
            raise ValueError("metadata.version must be set for update")
        ts = time.time()
        self._store.update_object(metadata.serialize(), name=metadata.name, ts=ts, version=metadata.version)

    def query(self, name=None, latest=True, tags=None, org_id: str=None, min_time: float=None, max_time: float=None) -> typing.List[ModelRef]:
        if name is not None:
            versions = self._store.query_versions(name, latest, tags, org_id, min_time, max_time)
            return [ModelRef(name=name, version=v) for v in versions]
        else:
            assert not latest, "if name is not specified latest should be False"
            refs = self._store.query_refs(tags, org_id, min_time, max_time)
            return [ModelRef(name, version) for name, version in refs]

    def query_latest_versions(self, model_name: str):
        return self._store.query_latest_versions(doc_name=model_name)

    def purge_non_accessed_data(self, purge_before_timestamp: datetime, dry_run: bool = False):
        log_columns = ['doc_name', 'doc_version']
        where_clause = {'doc_type': self._store._cls_name}

        count, rows = self._store.purge_non_accessed_data(purge_before_timestamp, dry_run=dry_run,
                                                          where_params=where_clause, log_columns=log_columns)
        return count, PostgresQueryHelper.parse_postgres_results(log_columns, rows)

    def purge_models(self, model_refs: typing.List[ModelRef]):
        return self._store.purge(set(model_refs))

    def delete_all_tables_and_indexes(self):
        return self._store._delete_all_tables_and_indexes()
    