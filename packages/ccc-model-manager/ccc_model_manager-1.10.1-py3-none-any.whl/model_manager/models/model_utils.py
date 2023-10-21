# Copyright (c) 2023 VMware, Inc. All Rights Reserved.

from strenum import StrEnum


MODEL_NAME = 'model_name'
MODEL_VERSION = 'model_version'
MODEL_TYPE = 'model_type'
MODEL_ORG = 'org_id'
MODEL = 'model'
TOKENIZER = 'tokenizer'


class ModelType(StrEnum):
    BERT = 'bert'
    BART = 'bart'
    APRIORI = 'apriori'

