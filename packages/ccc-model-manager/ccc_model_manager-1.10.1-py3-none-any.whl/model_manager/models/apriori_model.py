#  Copyright (c) 2023 VMware, Inc. All rights reserved


import logging
import pickle
from model_manager.models import model
from model_manager.models.model_params import BaseModelParams
from model_manager.stores.model_store import TensorDef

_logger = logging.getLogger(__name__)


class AprioriModel(model.PredictiveModel):
    MODEL_TYPE = "apriori"

    def __init__(self, save_path: str):
        """
        :param save_path:
        """
        super().__init__([TensorDef("input_text", "List[str]",())], [TensorDef("lookup", "dict",())])
        self.save_path = save_path
        self.model = None

    def build_model(self):
        with open(self.save_path, 'rb') as f:
            self.model = pickle.load(f)
        return self

    @classmethod
    def get_model_type(cls):
        return cls.MODEL_TYPE


class AprioriModelParams(BaseModelParams):
    def __init__(self, model_address: str):
        super().__init__(model_address=model_address)
