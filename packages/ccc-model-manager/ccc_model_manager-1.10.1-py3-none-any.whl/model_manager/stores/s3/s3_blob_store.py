# Copyright (c) 2022 VMware, Inc. All Rights Reserved.

import io
import logging
import os
import re
import tempfile
import uuid
from datetime import datetime
from typing import List

from minio.deleteobjects import DeleteObject

from model_manager.stores.blob_store import BlobStore
from model_manager.stores.postgres.postgres_blob_metadata_store import PostgresBlobMetadataStore
from model_manager.stores.s3.s3_utils import S3Utils

_logger = logging.getLogger(__name__)


class S3BlobStore(BlobStore):
    """
    Implementation of blob store using S3 (or minio) storage.
    Uses a single bucket with namespaces mapped to directories inside the bucket
    """

    def __init__(self, postgres_conn_info: dict, endpoint: str, aws_access_key: str, aws_secret_key: str, bucket: str,
                 region: str = None, secure: bool = True, subdir: str = None):
        self._endpoint = endpoint
        self._secure = secure
        self._bucket = bucket
        self._region = region
        self._access_key = aws_access_key
        self._secret_key = aws_secret_key
        self.s3_utils = S3Utils(self._endpoint, self._access_key, self._secret_key,
                                self._bucket, self._region, self._secure)
        self._client = self.s3_utils.get_client()
        self._subdir = subdir
        self.blob_metadata_store = PostgresBlobMetadataStore(postgres_conn_info)

    def get_client(self):
        return self.s3_utils.get_client()

    def delete_all_buckets_and_metadata(self):
        """
        Delete this blobstore completely, including deleting its bucket
        :return:
        """
        _logger.info("Deleting s3 blobstore in bucket %s" % self._bucket)
        minio_client = self.get_client()
        names = [DeleteObject(o.object_name) for o in minio_client.list_objects(self._bucket, recursive=True)]
        for del_err in self.get_client().remove_objects(self._bucket, names):
            _logger.debug("Deletion Error: {}".format(del_err))

        self.get_client().remove_bucket(self._bucket)
        self.blob_metadata_store.delete_all_tables_and_indexes()
        self._client = None

    def _validate_id(self, id_: str) -> bool:
        """Validates the identifier against a pattern suitable for local storage"""
        VALID_ID_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9\-_.]*$"
        return re.match(VALID_ID_PATTERN, id_) is not None

    def _get_directory(self, namespace):
        """
        Uniquely and deterministically maps namespace to directory
        :param namespace:
        :return:
        """
        for path_element in namespace.split(self.PATH_SEPARATOR):
            assert self._validate_id(
                path_element), "Namespace {} contains invalid characters in {}".format(namespace, path_element)
            assert len(path_element) <= 255, "The namespace is too long"
        directory = namespace + self.PATH_SEPARATOR
        if self._subdir:
            directory = self._subdir + self.PATH_SEPARATOR + directory
        return directory

    def _build_path(self, directory: str, name: str):
        if not directory.endswith(self.PATH_SEPARATOR):
            directory = directory + self.PATH_SEPARATOR
        return "{}{}".format(directory, name)

    def _build_path_and_name(self, directory: str):
        name = "{}.blob".format(uuid.uuid4())
        return self._build_path(directory, name)

    def store_data(self, namespace: str, data: bytes) -> str:
        directory = self._get_directory(namespace=namespace)
        path = self._build_path_and_name(directory)
        stream = io.BytesIO(data)
        _ = self.blob_metadata_store.store_data(path)
        _ = self.get_client().put_object(self._bucket, path, stream, len(data))
        return path

    def store_file(self, file_location: str, namespace: str) -> str:
        assert os.path.isfile(file_location)
        directory = self._get_directory(namespace=namespace)
        path = self._build_path_and_name(directory)
        _ = self.blob_metadata_store.store_data(path)
        _ = self.get_client().fput_object(self._bucket, path, file_location)
        return path

    def get_data(self, address: str) -> bytes:
        # no metadata really needed at this point just "touch" the entry to update last_access
        _ = self.blob_metadata_store.get_data(address)
        data = self.get_client().get_object(self._bucket, address)
        return data.read()

    def get_file(self, address: str, file_location: str):
        _ = self.blob_metadata_store.get_data(address)
        self.get_client().fget_object(self._bucket, address, file_location)

    def get_data_addresses(self, namespace: str) -> List[str]:
        directory = self._get_directory(namespace=namespace)
        addresses = [self._build_path(namespace, i) for i in
                     self.get_client().list_objects(self._bucket, prefix=directory)]
        return addresses

    def delete_data(self, address: str):
        self.blob_metadata_store.delete_data(address)
        self.get_client().remove_object(self._bucket, address)

    def get_existing_blob_file(self, file_location: str, namespace: str = None):
        # TODO: VJAN-2305 created to add this and fix s3 blob store unit tests.
        raise NotImplementedError()

    def purge_non_accessed_data(self, purge_before_timestamp: datetime, dry_run: bool = True):
        # delete metadata
        _, non_accessed_addresses = self.blob_metadata_store.purge_non_accessed_data(purge_before_timestamp, dry_run)
        count = 0
        if not dry_run:
            for item in non_accessed_addresses:
                address = item['address']
                self.delete_data(address)  # delete blob
                count = count + 1
                _logger.debug(f"deleted: {address}")
        else:
            _logger.debug(f"Non accessed blob store before: {purge_before_timestamp}: {non_accessed_addresses}")

        return count, non_accessed_addresses

    def preseed_metadata(self, dry_run=False):
        """A function to add entries for all blobs in the metadata store"""
        minio_client = self.get_client()
        s3_objects = minio_client.list_objects(self._bucket, recursive=True)
        s3_objects = {obj.object_name: [obj.object_name, obj.size] for obj in s3_objects}
        _logger.info(f"Found {len(s3_objects)} records in s3")

        metadata_objects = self.blob_metadata_store.list_all_objects()
        _logger.info(f"Found metadata for {len(metadata_objects)} records")
        object_wo_metadata = list(set(s3_objects) - set(metadata_objects))

        with tempfile.NamedTemporaryFile(mode='w') as fp:
            _logger.info(f"Dumping {len(object_wo_metadata)} records to {fp.name}")
            object_wo_metadata = [f"{item}\n" for item in object_wo_metadata]
            fp.writelines(object_wo_metadata)
            fp.flush()
            if not dry_run:
                self.blob_metadata_store.bulk_insert_from_file(fp.name, columns=('address',))
