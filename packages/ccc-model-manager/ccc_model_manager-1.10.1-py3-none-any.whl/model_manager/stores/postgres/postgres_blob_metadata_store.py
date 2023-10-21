# Copyright (c) 2022 VMware, Inc. All Rights Reserved.


import datetime

from model_manager.stores.blob_metadata_store import BlobMetadataStore
from model_manager.stores.postgres.postgres_utils import PostgresQueryHelper
from model_manager.stores.postgres.tables import postgres_blob_metadata_table as metadata_table


class PostgresBlobMetadataStore(BlobMetadataStore):
    """A Companion/Metadata store to Blob Store. This is used only with s3 blob store since there's no way
    to handle access metadata for s3"""

    def __init__(self, connection_info: dict):
        self._store = metadata_table.PostgresS3BlobMetadataTable(connection_info=connection_info)

    def store_data(self, address: str, **kwargs) -> str:
        self._store.add_object(address)
        return address

    def get_data(self, address: str):
        return self._store.get_object(address)

    def delete_data(self, address: str):
        self._store.delete_object(address)

    def list_all_objects(self):
        return [item[0] for item in self._store.run_query(['address'], {})]

    def delete_all_tables_and_indexes(self):
        self._store._delete_all_tables_and_indexes()

    def bulk_insert_from_file(self, file_name: str, columns: tuple):
        self._store.bulk_insert_from_file(file_name, columns)

    def purge_non_accessed_data(self, purge_before_timestamp: datetime, dry_run: bool = False):
        columns = ['address']
        count, rows = self._store.purge_non_accessed_data(purge_before_timestamp, dry_run=dry_run, log_columns=columns)
        return count, PostgresQueryHelper.parse_postgres_results(columns, rows)
