#  Copyright (c) 2022 VMware, Inc. All rights reserved

import json
import logging
import os

from model_manager.model_publish_params import ModelPublishParams, PUBLISH_URL, AUTH_TOKEN, ORG_ID
from model_manager.stores.model_store import ModelStore
from model_manager.stores.dataset_store import DatasetStore
from model_manager.stores.postgres.postgres import HOST, DATABASE, PORT, USER, PASSWORD
from model_manager.stores.postgres.postgres_model_store import PostgresModelStore
from model_manager.stores.postgres.postgres_dataset_store import PostgresDatasetStore
from model_manager.stores.s3.s3_blob_store import S3BlobStore

SECRETS_DIR = os.getenv("MAGNA_SECRETS_DIR", os.path.join(os.path.dirname(__file__), "_secrets"))

logging.info("MAGNA_SECRETS_DIR: %s", SECRETS_DIR)

PIPELINE_SECRETS_FILE = os.path.join(SECRETS_DIR, "pipeline.json")

# try to load any local s3/postgres configuration secrets
try:
    with open(PIPELINE_SECRETS_FILE, 'r') as json_data:
        magna_secrets = json.load(json_data)
except IOError:
    logging.debug("No pipeline secrets file found")
    magna_secrets = {}


PIPELINE_S3_PORT = os.getenv("PIPELINE_S3_PORT", magna_secrets.get("PIPELINE_S3_PORT"))
PIPELINE_S3_HOST = os.getenv("PIPELINE_S3_HOST", magna_secrets.get("PIPELINE_S3_HOST"))
PIPELINE_S3_BUCKET = os.getenv("PIPELINE_S3_BUCKET", magna_secrets.get("PIPELINE_S3_BUCKET"))
PIPELINE_S3_REGION = os.getenv("PIPELINE_S3_REGION", magna_secrets.get("PIPELINE_S3_REGION"))
PIPELINE_S3_SECURE = ("True" == os.getenv("PIPELINE_S3_SECURE", magna_secrets.get("PIPELINE_S3_SECURE")))

PIPELINE_AWS_ACCESS_KEY = os.getenv("PIPELINE_AWS_ACCESS_KEY", magna_secrets.get("PIPELINE_AWS_ACCESS_KEY"))
PIPELINE_AWS_SECRET_KEY = os.getenv("PIPELINE_AWS_SECRET_KEY", magna_secrets.get("PIPELINE_AWS_SECRET_KEY"))

PIPELINE_S3_ARTIFACTS_SUBDIR = "magna/artifacts"
PIPELINE_S3_PUBLISHED_SUBDIR = "magna/published"

PIPELINE_S3_ENDPOINT = "{}:{}".format(PIPELINE_S3_HOST, PIPELINE_S3_PORT)

PIPELINE_POSTGRES_HOST = os.getenv("PIPELINE_POSTGRES_HOST", magna_secrets.get("PIPELINE_POSTGRES_HOST"))
PIPELINE_POSTGRES_PORT = os.getenv("PIPELINE_POSTGRES_PORT", magna_secrets.get("PIPELINE_POSTGRES_PORT"))
PIPELINE_POSTGRES_DATABASE = os.getenv("PIPELINE_POSTGRES_DATABASE", magna_secrets.get("PIPELINE_POSTGRES_DATABASE"))
PIPELINE_POSTGRES_USERNAME = os.getenv("PIPELINE_POSTGRES_USERNAME", magna_secrets.get("PIPELINE_POSTGRES_USERNAME"))
PIPELINE_POSTGRES_PASSWORD = os.getenv("PIPELINE_POSTGRES_PASSWORD", magna_secrets.get("PIPELINE_POSTGRES_PASSWORD"))

PIPELINE_MODEL_PUBLISH_URL = os.getenv("PIPELINE_MODEL_PUBLISH_URL", magna_secrets.get("PIPELINE_MODEL_PUBLISH_URL"))
PIPELINE_MODEL_PUBLISH_AUTH_TOKEN = os.getenv("PIPELINE_MODEL_PUBLISH_AUTH_TOKEN",
                                              magna_secrets.get("PIPELINE_MODEL_PUBLISH_AUTH_TOKEN"))
PIPELINE_MODEL_PUBLISH_ORG_ID = os.getenv("PIPELINE_MODEL_PUBLISH_ORG_ID",
                                          magna_secrets.get("PIPELINE_MODEL_PUBLISH_ORG_ID"))
PIPELINE_MODEL_NOTIF_KAFKA_TOPIC = os.getenv("PIPELINE_MODEL_NOTIF_KAFKA_TOPIC", magna_secrets.get("PIPELINE_MODEL_NOTIF_KAFKA_TOPIC"))


class EnvironmentContext(object):

    def __init__(self):
        self._model_store = None
        self._dataset_store = None
        self.s3_blob_store = None
        self.postgres_config = {
            # Use following structure to fill in connection values
            HOST: PIPELINE_POSTGRES_HOST,
            PORT: PIPELINE_POSTGRES_PORT,
            DATABASE: PIPELINE_POSTGRES_DATABASE,
            USER: PIPELINE_POSTGRES_USERNAME,
            PASSWORD: PIPELINE_POSTGRES_PASSWORD,
            "connect_timeout": 10
        }
        self._model_publish_params = {
            PUBLISH_URL: PIPELINE_MODEL_PUBLISH_URL,
            AUTH_TOKEN: PIPELINE_MODEL_PUBLISH_AUTH_TOKEN,
            ORG_ID : PIPELINE_MODEL_PUBLISH_ORG_ID
        }
        self.model_notif_kafka_topic = PIPELINE_MODEL_NOTIF_KAFKA_TOPIC

    @property
    def blob_store(self) -> S3BlobStore:

        if self.s3_blob_store is None:
            self.s3_blob_store = S3BlobStore(self.postgres_config, PIPELINE_S3_ENDPOINT, PIPELINE_AWS_ACCESS_KEY,
                                             PIPELINE_AWS_SECRET_KEY, PIPELINE_S3_BUCKET, PIPELINE_S3_REGION,
                                             PIPELINE_S3_SECURE)

        return self.s3_blob_store

    @property
    def model_store(self) -> ModelStore:
        if self._model_store is None:
            self._model_store = self._build_model_store()
        return self._model_store

    def _build_model_store(self):
        if self.postgres_config:
            return PostgresModelStore(self.postgres_config)

    @property
    def dataset_store(self) -> DatasetStore:
        if self._dataset_store is None:
            self._dataset_store = self._build_dataset_store()
        return self._dataset_store

    def _build_dataset_store(self):
        if self.postgres_config:
            return PostgresDatasetStore(self.postgres_config)

    @property
    def model_publish_params(self) -> ModelPublishParams:
        if self._model_publish_params:
            return ModelPublishParams(self._model_publish_params)
