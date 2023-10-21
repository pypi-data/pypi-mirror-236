#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved
from typing import List, Optional, Set

from model_manager.stores.purgeable_store import PurgeableStore
from .base import VersionedRef, BaseMetadata


class DatasetRef(VersionedRef):
    """
    Reference to a dataset based on name and version
    """


class DatasetMetadata(BaseMetadata):
    """
    Represents the metadata for a data set
    """

    def __init__(self,
                 name: str,
                 org_id: str,
                 task_id: str,
                 states_data_address: str,
                 data_format: str,
                 size: int = None,
                 version: str = None,
                 creation_time: str = None,
                 tags: dict = None):
        """
        :param name: A meaningful name for the dataset
        :param org_id: CSP org_id(s) identifying the ownership of the data in the dataset (not set if no owner)
        :param task_id: The reference to the task that imported the data
        :param states_data_address: Reference to the states data, e.g. blob://blob_id, file://data/samples/sample_id
        :param data_format: Data save format (numpy npz, pickle, joblib, etc)
        :param size: Size of the dataset in samples
        :param version: The version of this dataset
        :param creation_time: When the dataset was added.
        :param tags: key-value pairs providing additional description to the dataset.
        """
        super().__init__(name, org_id, version, tags, creation_time)
        self.task_id = task_id
        self.states_data_address = states_data_address
        self.data_format = data_format
        self.size = size


class DatasetStore(PurgeableStore):
    """
    Store for persisting dataset metadata.
    Subclass this interface to implement various specific store types.
    """

    def get_metadata(self, dataset_ref: DatasetRef) -> DatasetMetadata:
        """
        Gets the metadata identified by the DatasetRef

        :param dataset_ref: Reference to the dataset
        :return: The dataset metadata for the dataset identified by the provided dataset_ref
        """
        raise NotImplementedError()

    def get_versions(self, name: str) -> List[DatasetRef]:
        """
        Gets the list of dataset references for all versions associated with the provided name

        :param name: The name of the dataset for which to get the references
        :return: The dataset references for all available versions of the dataset metadata
        """
        raise NotImplementedError()

    def store_metadata(self, metadata: DatasetMetadata) -> DatasetRef:
        """
        Stores the metadata and returns the reference

        :param metadata: The dataset metadata to store
        :return: A dataset reference containing the new version
        """
        raise NotImplementedError()

    def update_metadata(self, metadata: DatasetMetadata):
        """
        Update the dataset metadata
        :param metadata: The dataset metadata to store
        """
        raise NotImplementedError

    def purge_datasets(self, datasets: Set[DatasetRef]):
        """
        Purge the given datasets permanently
        :param datasets set of datasets to delete permanently
        """
        raise NotImplementedError()

    def query(self, name: Optional[str], latest: bool = True, tags: dict = None, org_id: str = None) -> List[DatasetRef]:
        """
        Query the store for datasets with the optionally provided name, tags and org_id

        :param name: optional name
        :param latest: Return only the latest matching dataset of the given name (name is required)
        :param tags: optional Tag values to match
        :param org_id: optional org_id to match
        :return: List of tuples(version, metadata) ordered by time added, descending (latest first)
        """
        raise NotImplementedError()
