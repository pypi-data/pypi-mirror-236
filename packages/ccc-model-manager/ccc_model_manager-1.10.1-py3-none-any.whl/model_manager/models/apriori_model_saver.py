#  Copyright (c) 2023 VMware, Inc. All rights reserved

import logging
import os
import time
import json
import tarfile
import pickle

from model_manager.common.serializable import Serializable
from model_manager.models.apriori_model import AprioriModel, AprioriModelParams
from model_manager.models.model_saver import ModelSaver
from model_manager.stores.model_store import ModelMetadata

logger = logging.getLogger(__name__)


class AprioriModelSaver(ModelSaver):
    def load(self, model_meta: ModelMetadata):
        model_file_name = self.download_data(model_meta=model_meta)
        return self.load_local(model_meta=model_meta, base_path=model_file_name)

    @staticmethod
    def _get_blob_file_name(base_path: str, org_id: str):
        return os.path.join(base_path, "apriori_model-{}.blob".format(org_id))

    def download_data(self, model_meta: ModelMetadata) -> str:
        """
        Returns path to dict in pickle form - as downloaded from
        the blob store.
        :param model_meta:
        :return: List of paths relative to the work directory
        """
        params = AprioriModelParams.deserialize(model_meta.model_params)
        blob_file_path = self._get_blob_file_name(self._work_dir, model_meta.org_id)
        self._ctx.blob_store.get_file(params.model_address, blob_file_path)
        return blob_file_path

    def load_local(self, model_meta: ModelMetadata, base_path: str):
        model = AprioriModel(save_path=base_path)
        return model

    def save(self, model_name: str, model: AprioriModel) -> Serializable:
        temp_file_name = os.path.join(self._work_dir, "{}-{}".format(model_name, int(time.time())))
        logger.debug("temp model address: {}".format(temp_file_name))
        with open(temp_file_name, 'wb') as f:
            pickle.dump(model.model, f)
        model_address = self._ctx.blob_store.store_file(temp_file_name, model_name)
        return AprioriModelParams(
            model_address=model_address,
        )

    @classmethod
    def get_model_class(cls):
        return AprioriModel
