#  Copyright (c) 2018-2020 VMware, Inc. All rights reserved

from model_manager.common.serializable import Serializable


class BaseModelParams(Serializable):
    def __init__(self, model_address: str):
        self.model_address = model_address
