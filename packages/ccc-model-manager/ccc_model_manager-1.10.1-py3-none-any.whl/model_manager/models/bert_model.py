#  Copyright (c) 2022 VMware, Inc. All rights reserved

import logging

import torch
from model_manager.models import model
from model_manager.models.model_params import BaseModelParams
from model_manager.stores.model_store import TensorDef
from transformers import BertForSequenceClassification, BertTokenizer

_logger = logging.getLogger(__name__)


class BERTModel(model.PredictiveModel):
    MODEL_TYPE = "bert"

    def __init__(self, save_path: str, max_sequence_length: int=None):
        """
        :param save_path:
        """
        super().__init__([TensorDef("input_text", "List[str]",())], [TensorDef("fault", "List[int]",())])
        self.save_path = save_path
        self.max_sequence_length = 50 if max_sequence_length is None else max_sequence_length
        self.tokenizer = None
        self.model = None

    def build_model(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = BertTokenizer.from_pretrained(self.save_path)
        self.model = BertForSequenceClassification.from_pretrained(self.save_path)
        self.model.to(device)
        return self

    @classmethod
    def get_model_type(cls):
        return cls.MODEL_TYPE


class BERTModelParams(BaseModelParams):
    def __init__(self, model_address: str, max_sequence_length: int):
        super().__init__(model_address=model_address)
        self.max_sequence_length = max_sequence_length
