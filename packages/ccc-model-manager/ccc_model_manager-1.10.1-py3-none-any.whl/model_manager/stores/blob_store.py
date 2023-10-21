# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
import os
from typing import List, Optional


class BlobStore:
    PATH_SEPARATOR = "/"

    def store_data(self, namespace: str, data: bytes) -> str:
        """
        Stores the data and returns the address
        :param metadata:
        :param namespace:
        :param data:
        :return:
        """
        raise NotImplementedError()

    def store_file(self, file_location: str, namespace: str) -> str:
        raise NotImplementedError()

    def get_data(self, address: str) -> bytes:
        """
        Reads the data from the address
        :param object_id:
        :param directory:
        :return:
        """
        raise NotImplementedError()

    def get_file(self, address: str, file_location: str):
        raise NotImplementedError()

    def get_data_addresses(self, namespace: str) -> List[str]:
        raise NotImplementedError()

    def delete_data(self, address: str):
        """
        Purge the data at the given address
        @param address:
        @return:
        """
        raise NotImplementedError()

    def get_existing_blob_file(self, file_location: str, namespace: str = None) -> Optional[str]:
        """
        Check the input namespace for existing blob files, and return the
        latest if not empty. Else returns None
        :param file_location: path pointing to file to be stored.
        :param namespace: namespace to check.
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def _get_default_namespace(file_location: str) -> str:
        """
        Returns default namespace as the file_name parsed from file_location.
        :param file_location:
        :return:
        """
        _, file_name = os.path.split(file_location)
        return file_name
