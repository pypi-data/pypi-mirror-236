# Copyright (c) 2022 VMware, Inc. All Rights Reserved.

class BlobMetadataStore:

    def store_data(self, address: str, **kwargs) -> str:
        """
        Stores metadata for the blob entry, current;y the metadata is just access time but that can be expanded
        :param metadata:
        :return:
        """
        raise NotImplementedError()

    def get_data(self, address: str):
        """
        Reads the metadata data for a given blob address
        :param address:
        :return:
        """
        raise NotImplementedError()

    def delete_data(self, address: str):
        """
        Purge the metadata for a given blob address
        @param address:
        @return:
        """
        raise NotImplementedError()
