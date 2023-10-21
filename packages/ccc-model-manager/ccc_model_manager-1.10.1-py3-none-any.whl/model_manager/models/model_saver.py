#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

import logging
import os
import tarfile

from model_manager.common.serializable import Serializable
from model_manager.stores.model_store import ModelMetadata, ModelRef

logger = logging.getLogger(__name__)


class ModelSaver(object):
    def __init__(self, ctx, work_dir: str):
        self._ctx = ctx
        self._work_dir = work_dir

    def load_model(self, model_ref: ModelRef):
        """
        Fetch the given model identified by the model reference.

        We first find the model metadata using the model_ref. The metadata contains the model address, which we use to
        download the model from the blob store.
        Args:
            model_ref: model reference which is name and version.

        Returns: a PredictiveModel object

        """
        model_meta = self._ctx.model_store.get_metadata(model_ref=model_ref)
        return self.load(model_meta=model_meta), model_meta.org_id

    def save_model(self, model: 'm.PredictiveModel', model_name: str, tags:dict=None, org_id:str=None) -> ModelRef:
        """
        Save the given model to the blob store, and its metadata to the metadata store
        :param model:
        :param model_name:
        :param tags:
        :param org_id: Optional organization id this model belongs to
        :return: ModelRef with the model name and version
        """
        model_type = model.get_model_type()
        model_params = self.save(model_name=model_name, model=model)
        serialized_params = model_params.serialize()
        logger.info(
            "Serialized Saved Model Params: {}".format(serialized_params))
        model_meta = ModelMetadata(
            name=model_name,
            inputs=model.input_defs,
            outputs=model.output_defs,
            tags=tags,
            model_type=model_type,
            model_params=serialized_params,
            org_id=org_id
        )
        return self._ctx.model_store.store_metadata(metadata=model_meta)

    def download_tar(self, model_name: str, model_version: str, model_address: str) -> str:
        """
        Downloads and untars the data from the provided address.

        :param model_name:
        :param model_version:
        :param model_address:
        :return:
        """
        model_dir_name = os.path.join(self._work_dir, "{}-{}".format(model_name, model_version))
        model_file_name = model_dir_name + ".tgz"
        if os.path.exists(model_file_name) and os.path.isfile(model_file_name):
            logger.info(f"File already exists, skipping downloading, model_file_name={model_file_name}")
            return model_dir_name
        os.makedirs(model_dir_name, exist_ok=True)
        self._ctx.blob_store.get_file(address=model_address, file_location=model_file_name)
        with tarfile.open(model_file_name, "r") as f:
            f.extractall(path=model_dir_name)
        return model_dir_name

    def upload_tar(self, model_name: str, path: str) -> str:
        """
        Uploads the data from the provided directory and returns the blob address.

        :param model_name:
        :param path:
        :return:
        """
        namespace = "{}.tgz".format(model_name)
        # TODO: model name used for file operations - we need to validate
        tgz_file = os.path.join(self._work_dir, "{}.tgz".format(model_name))
        if os.path.isfile(tgz_file):
            os.remove(tgz_file)
        with tarfile.open(tgz_file, "w:gz") as f:
            f.add(path, arcname="." if os.path.isdir(path) else os.path.basename(path))
        address = self._ctx.blob_store.store_file(file_location=tgz_file, namespace=namespace)
        return address

    def load(self, model_meta: ModelMetadata):
        """
        Loads the model using the provided metadata. This usually involves deserializing the model params, downloading
        the model to the local disk, and instantiating the actual model.

        :param model_meta:
        :return: The restored model instance.
        """
        raise NotImplementedError()

    def load_local(self, model_meta: ModelMetadata, base_path: str):
        """
        Similar to load except all of the data is already local.

        :param model_meta:
        :param base_path: The path containing all of the necessary data to load the model
        :return: The restored model instance.
        """
        raise NotImplementedError()

    def save(self, model_name: str, model) -> Serializable:
        """
        Saves the model by uploading necessary data for restoring to the appropriate store and constructing the model
        parameters.

        :param model_name:
        :param model:
        :return: The model parameters that will be used when storing the model metadata.
        """
        raise NotImplementedError()
