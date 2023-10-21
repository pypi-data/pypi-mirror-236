#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved
from datetime import datetime
from typing import List

import numpy as np

from model_manager.stores.purgeable_store import PurgeableStore
from model_manager.stores.base import VersionedRef, BaseMetadata
from model_manager.common.serializable import Serializable


class ModelRef(VersionedRef):
    """
    Reference to a model based on name and version
    """
    def __init__(self, name: str, version: str, type: str = None):
        self._name = name
        self._version = version
        self._type = type

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def type(self):
        return self._type

    @version.setter
    def version(self, value):
        self._version = value


class TensorDef(Serializable):
    def __init__(self, name: str, dtype: str, shape: tuple):
        self.name = name
        self.dtype = dtype
        self.shape = shape

    @staticmethod
    def from_tensor(tensor, name: str=None):
        """
        Create definition for the provided tensor
        :param tensor:
        :param name: If provided this name will be used instead of the tensor's name
        :return:
        """
        return TensorDef(name=name if name else tensor.name, shape=tuple(tensor.shape.as_list()), dtype=tensor.dtype.name)

    @staticmethod
    def get_shape(record_shape: tuple, batched: bool, batch_size: int=None, sequence_length: int=1):
        shape = record_shape
        if sequence_length and sequence_length > 1:
            shape = (sequence_length,) + shape
        if batched:
            shape = (batch_size,) + shape
        return shape

    @staticmethod
    def as_np_dtype(dtype: str):
        return np.typeDict[dtype]

    @staticmethod
    # def as_tf_dtype(dtype: str):
    #     return tf.as_dtype(dtype)

    def __str__(self):
        return "{dtype} {name}[{dims}]".format(
            dtype=self.dtype,
            name=self.name,
            dims=", ".join([str(i) for i in self.shape])
        )

    def __repr__(self):
        return "{class_name}({fields})".format(
            class_name=self.__class__.__name__,
            fields=", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        )


class ModelMetadata(BaseMetadata):
    """
    Represents the metadata for a model
    """

    def __init__(self, name: str, inputs: List[TensorDef], outputs: List[TensorDef], model_type: str, model_params: dict,
                 org_id: str = None, version: str = None, tags: dict = None, creation_time: str = None):
        """
        :param name: identifier of this model
        :param inputs: definitions of the input tensors
        :param outputs: definitions of the output tensors
        :param tags: key-value pairs describing the model - how it was generated, description, accuracy at particular
            task, etc.
        :param model_type: The type of the model - e.g. bert, keras, ...
        :param model_params: Model type - specific parameters (i.e. the Links for ensemble, regressor type, etc.
        :param version: The version is assigned when the model is stored
        """
        super().__init__(name, org_id, version, tags, creation_time)
        self.inputs = [] if inputs is None else inputs
        self.outputs = [] if outputs is None else outputs
        self.model_type = model_type
        self.model_params = {} if model_params is None else model_params

    @staticmethod
    def timestamp_to_timestr(timestamp):
        if not timestamp:
            return None
        dt = datetime.utcfromtimestamp(timestamp)
        return "{0:%Y-%m-%d %H:%M:%S}".format(dt)


class ModelStore(PurgeableStore):
    def get_metadata(self, model_ref: ModelRef) -> ModelMetadata:
        """
        Gets the metadata identified by the ModelRef

        :param model_ref: Reference to the model
        :return: The model metadata for the model identified by the provided dataset_ref
        """
        raise NotImplementedError()

    def get_model_versions(self, name: str) -> List[ModelRef]:
        """
        Gets the list of model references for all versions associated with the provided name

        :param name: The name of the model for which to get the references
        :return: The model references for all available versions of the model metadata
        """
        raise NotImplementedError()

    def store_metadata(self, metadata: ModelMetadata) -> ModelRef:
        """
        Stores the metadata and returns the reference

        :param metadata: The model metadata to store
        :return: A model reference containing the new version
        """
        raise NotImplementedError()

    def update_metadata(self, metadata: ModelMetadata):
        """
        Updates the metadata, keep the reference

        :param metadata: The model metadata to store
        """
        raise NotImplementedError()

    def query(self, name=None, latest=True, tags=None, org_id: str=None, min_time: float=None, max_time: float=None) -> List[ModelRef]:
        """
        Query the store for models with the specified name.

        :param name:
        :param latest: Return only the latest model matching the criteria
        :param tags: Tag values to match
        :param org_id: Org ID to match
        :param min_time: min ts to consider
        :param max_time: max ts to consider
        :return: List of tuples(version, metadata) ordered by time added, descending (latest first)
        """
        raise NotImplementedError()

    def query_latest_versions(self, model_name: str):
        raise NotImplementedError()

    def purge_models(self, models: List[ModelRef]):
        """
        Purge the given models permanently
        :param set of models refs to delete permanently
        """
        raise NotImplementedError()

    def delete_all_tables_and_indexes(self):
        """
        Delete all tables and indexes of the tables.
        """
        raise NotImplementedError()
