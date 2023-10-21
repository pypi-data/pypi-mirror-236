# Copyright (c) 2023 VMware, Inc. All Rights Reserved.

PUBLISH_URL = "PUBLISH_URL"
AUTH_TOKEN = "AUTH_TOKEN"
ORG_ID = "ORG_ID"


class ModelPublishParams:
    def __init__(self, config: dict):
        self.url = config.get(PUBLISH_URL)
        self.auth_token = config.get(AUTH_TOKEN)
        self.org_id = config.get(ORG_ID)