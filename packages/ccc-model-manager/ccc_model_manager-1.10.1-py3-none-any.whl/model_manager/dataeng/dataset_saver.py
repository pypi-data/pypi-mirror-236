#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

import logging
import os
import time
import pandas as pd

from model_manager.dataeng.dataset import Dataset
from model_manager.stores.blob_store import BlobStore
from model_manager.stores.dataset_store import DatasetStore, DatasetRef, DatasetMetadata



class DatasetSaver(object):
    """ Load Dataset referenced by DataRef from DatasetStore and BlobStore"""
    # TODO: naming convention
    BLOB_STORE_NAME_FORMAT = "{name}-{key}"

    def __init__(self, dataset_store: DatasetStore, blob_store: BlobStore,
                 temp_dir: str):
        self._data_store = dataset_store  # where meta data of dataset is stored
        self._blob_store = blob_store  # where the binary is stored
        self._temp_dir = temp_dir  # temp loaded location
        self._all_format_savers = {cls.DATA_FORMAT: cls for cls in FormatSaver.__subclasses__()}
        self.logger = logging.getLogger(__name__)

    def load(self, data_ref: DatasetRef):
        data_meta = self._data_store.get_metadata(dataset_ref=data_ref)
        format_saver = self._all_format_savers[data_meta.data_format]()
        states_filename = os.path.join(self._temp_dir, format_saver.STATES_FILENAME_FORMAT.format(name=data_ref.name, version=data_ref.version))
        # get file from blob
        self._blob_store.get_file(data_meta.states_data_address, states_filename)
        self.logger.debug("Data downloaded to local storage")
        # load dataset from file

        states = self._all_format_savers[data_meta.data_format]().load_dataset(states_filename)
        return Dataset(org_id=data_meta.org_id,
                       dataset_ref=data_ref,
                       states=states)

    def save(self, dataset: Dataset, data_format: str, name: str, task_id: str, tags=None):
        format_saver = self._all_format_savers[data_format]()
        temp_state_file = format_saver.save_dataset(dataset, self._temp_dir)
        self.logger.debug("Data saved to temp directory")
        state_address = self._blob_store.store_file(temp_state_file, self.BLOB_STORE_NAME_FORMAT.format(name=name, key="state"))
        self.logger.debug("Data saved to blob store")
        data_meta = DatasetMetadata(
            org_id=dataset.org_id if dataset.org_id else None,
            name=name,
            states_data_address=state_address,
            task_id=task_id,
            data_format=format_saver.DATA_FORMAT,
            tags=tags
        )
        dataset_ref = self._data_store.store_metadata(data_meta)
        dataset.dataset_ref = dataset_ref
        return dataset_ref

    def purge_data_by_org_id(self, org_id: str, dry_run: bool = False) -> int:
        """
        :param org_id customer org_id to purge
        :param dry_run don't delete data if set to True, just return count of impacted datasets
        """
        assert org_id
        dataset_refs = self._data_store.query(None, False, None, org_id)
        if dry_run:
            return len(dataset_refs)
        # first delete associated blobs
        for data_ref in dataset_refs:
            data_meta = self._data_store.get_metadata(data_ref)
            self._blob_store.delete_data(data_meta.states_data_address)
        # now delete metadata
        self._data_store.purge_datasets(dataset_refs)
        # and return indication of number of matching datasets which were deleted
        return len(dataset_refs)


class FormatSaver(object):
    DATA_FORMAT = 'NULL'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_dataset(self, states_filename):
        raise NotImplementedError

    def save_dataset(self, dataset, local_dir: str):
        raise NotImplementedError


class CsvFormatSaver(FormatSaver):
    """ DatasetSaver that saves dataset actions and states in separate .npz file"""
    DATA_FORMAT = 'CSV'
    STATES_FILENAME_FORMAT = "states_data_{name}-{version}.csv"
    TEMP_FILENAME_FORMAT = "{key}-{time}.csv"

    def load_dataset(self, states_filename):
        states_data = pd.read_csv(states_filename)
        return states_data

    def save_dataset(self, dataset, local_dir: str):
        t = int(time.time())
        temp_state_file = os.path.join(local_dir, self.TEMP_FILENAME_FORMAT.format(key="state", time=t))
        states = dataset.states
        states.to_csv(temp_state_file)
        self.logger.debug("States saved in: {}".format(temp_state_file))

        return temp_state_file

