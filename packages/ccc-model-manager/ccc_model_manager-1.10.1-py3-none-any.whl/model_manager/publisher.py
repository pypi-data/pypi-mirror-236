# Copyright (c) 2023 VMware, Inc. All Rights Reserved.

import requests

from model_manager.models.model_utils import MODEL_NAME, MODEL_VERSION, MODEL_TYPE, MODEL_ORG
from model_manager.stores.env_context import EnvironmentContext
from model_manager.stores.model_store import ModelRef


def publish_model_status(model_ref: ModelRef, org_id: str = "vmware"):
    ctx = EnvironmentContext()
    headers = {"Content-Type": "application/json; charset=utf-8",
               "Authorization": "Bearer " + ctx.model_publish_params.auth_token,
               "x-org-id": ctx.model_publish_params.org_id}
    data = {MODEL_NAME: model_ref.name, MODEL_VERSION: model_ref.version, MODEL_TYPE: model_ref.type, MODEL_ORG: org_id}
    return requests.post(
        url=ctx.model_publish_params.url,
        json=data,
        headers=headers)