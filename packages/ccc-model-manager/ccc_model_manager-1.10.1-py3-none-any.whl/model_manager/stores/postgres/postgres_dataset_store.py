#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

import time
import typing
import uuid
from datetime import datetime
from typing import Set

from model_manager import stores
from model_manager.stores.dataset_store import DatasetRef, DatasetMetadata, DatasetStore
from model_manager.stores.postgres.tables.postgres_documents_table import PostgresDocumentsTable
from model_manager.stores.postgres.postgres_utils import PostgresQueryHelper


class PostgresDatasetStore(DatasetStore):

    def __init__(self, connection_info: dict):
        self._store = PostgresDocumentsTable(connection_info=connection_info, cls=DatasetMetadata)

    def get_metadata(self, dataset_ref: DatasetRef) -> DatasetMetadata:
        m: DatasetMetadata = self._store.get_object(name=dataset_ref.name, version=dataset_ref.version)
        return m

    def get_versions(self, name: str) -> typing.List[DatasetRef]:
        versions = self._store.get_versions(name)
        return [DatasetRef(name=name, version=v) for v in versions]

    def store_metadata(self, metadata: DatasetMetadata) -> DatasetRef:
        if metadata.version:
            raise ValueError("metadata.version must not be set as it is assigned by the store")

        version = str(uuid.uuid4())
        metadata.version = version
        ts = time.time()
        dataset_ref = DatasetRef(name=metadata.name, version=version)
        self._store.add_object(name=metadata.name, version=version, ts=ts, instance=metadata)
        return dataset_ref

    def update_metadata(self, metadata: DatasetMetadata):
        # If the version was not set, raise a value error
        if not metadata.version:
            raise ValueError("metadata.version must be set for update")
        ts = time.time()
        self._store.update_object(metadata.serialize(), name=metadata.name, ts=ts, version=metadata.version)

    def query_latest_versions(self, model_name: str):
        return self._store.query_latest_versions(doc_name=model_name)

    def query(self, name: str = None, latest: bool = True, tags: dict = None, org_id: str = None, min_time: float=None, max_time: float=None) -> typing.List[DatasetRef]:
        if name is not None:
            versions = self._store.query_versions(name, latest, tags, org_id, min_time, max_time)
            return [DatasetRef(name=name, version=v) for v in versions]
        else:
            assert not latest, "if name is not specified latest should be False"
            refs = self._store.query_refs(tags, org_id, min_time, max_time)
            return [DatasetRef(name, version) for name, version in refs]

    def purge_datasets(self, datasets: Set[DatasetRef]):
        return self._store.purge(datasets)

    def purge_non_accessed_data(self, purge_before_timestamp: datetime, dry_run: bool = False):
        log_columns = ['doc_name', 'doc_version']
        where_clause = {'doc_type': self._store._cls_name}

        count, rows = self._store.purge_non_accessed_data(purge_before_timestamp, dry_run=dry_run,
                                                          where_params=where_clause, log_columns=log_columns)
        return count, PostgresQueryHelper.parse_postgres_results(log_columns, rows)
