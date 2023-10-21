#  Copyright (c) 2022 VMware, Inc. All rights reserved
import logging
import os

from model_manager.common.serializable import Serializable
from model_manager.models.bert_model import BERTModel, BERTModelParams
from model_manager.models.model_saver import ModelSaver
from model_manager.stores.model_store import ModelMetadata

logger = logging.getLogger(__name__)


class BERTModelSaver(ModelSaver):
    def load(self, model_meta: ModelMetadata):
        model_dir_name = self.download_data(model_meta=model_meta)
        return self.load_local(model_meta=model_meta, base_path=model_dir_name)

    def download_data(self, model_meta: ModelMetadata) -> str:
        params = BERTModelParams.deserialize(model_meta.model_params)
        model_dir_name = self.download_tar(model_name=model_meta.name, model_version=model_meta.version,
                                           model_address=params.model_address)
        logger.debug("model %s@%s model dir: %s", model_meta.name, model_meta.version, model_dir_name)
        logger.debug("dir %s contents: %s", model_dir_name, os.listdir(model_dir_name))
        return model_dir_name

    def load_local(self, model_meta: ModelMetadata, base_path: str):
        model = BERTModel(save_path=base_path)
        return model

    def save(self, model_name: str, model: BERTModel) -> Serializable:
        model_address = self.upload_tar(model_name=model_name, path=model.save_path)
        return BERTModelParams(
            model_address=model_address,
            max_sequence_length=model.max_sequence_length
        )

    @classmethod
    def get_model_class(cls):
        return BERTModel
