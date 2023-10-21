# Copyright (c) 2023 VMware, Inc. All Rights Reserved.

import logging

from model_manager.models.model_saver import ModelSaver
from model_manager.models.model_utils import ModelType
from model_manager.stores.env_context import EnvironmentContext

_logger = logging.getLogger(__name__)


def get_model_loader(ctx: EnvironmentContext, model_type: ModelType, target_model_dir: str) -> ModelSaver:
    if ModelType.BERT == model_type:
        # Having import here helps to load this model only when required
        from model_manager.models.bert_model_saver import BERTModelSaver
        return BERTModelSaver(ctx, target_model_dir)
    elif ModelType.BART == model_type:
        from model_manager.models.bart_model_saver import BARTModelSaver
        return BARTModelSaver(ctx, target_model_dir)
    elif ModelType.APRIORI == model_type:
        from model_manager.models.apriori_model_saver import AprioriModelSaver
        return AprioriModelSaver(ctx, target_model_dir)
    else:
        _logger.error(f"Model type {model_type} is not supported")
        raise ValueError(f"Model type {model_type} is not supported")