#  Copyright (c) 2023 VMware, Inc. All rights reserved

import logging

import torch
from transformers import BartForConditionalGeneration, BartTokenizer

from model_manager.models import model
from model_manager.models.model_params import BaseModelParams
from model_manager.stores.model_store import TensorDef

_logger = logging.getLogger(__name__)


class BARTModel(model.PredictiveModel):
    MODEL_TYPE = "bart"

    def __init__(self, save_path: str):
        """
        :param save_path:
        """
        super().__init__([TensorDef("input_text", "List[str]", ())], [TensorDef("output_text", "List[str]", ())])
        self.save_path = save_path
        self.tokenizer = None
        self.model = None

    def build_model(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = BartTokenizer.from_pretrained(self.save_path)
        self.model = BartForConditionalGeneration.from_pretrained(self.save_path)
        self.model.to(device)
        return self

    @classmethod
    def get_model_type(cls):
        return cls.MODEL_TYPE


class BARTModelParams(BaseModelParams):
    def __init__(self, model_address: str):
        super().__init__(model_address=model_address)
