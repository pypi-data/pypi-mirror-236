# Copyright (c) 2023 VMware, Inc. All Rights Reserved.

import json
import logging
import threading
import uuid

from confluent_kafka import Consumer, KafkaException, KafkaError
from minio import S3Error
from typing import Dict
from typing import List

from model_manager.loader import get_model_loader
from model_manager.models.model import PredictiveModel
from model_manager.models.model_utils import ModelType, MODEL_NAME, MODEL_VERSION, MODEL_TYPE, MODEL_ORG
from model_manager.stores.env_context import EnvironmentContext
from model_manager.stores.model_store import ModelRef

_logger = logging.getLogger(__name__)


class ModelManager(object):
    def __init__(self, model_name_types: List[tuple], target_model_dir: str = '/tmp', kafka_configs=None):
        self.model_name_types = model_name_types
        self.model_version_cache: Dict[str, ModelRef] = {}
        self.model_cache: Dict[ModelRef, PredictiveModel] = {}
        self.kafka_configs = kafka_configs
        self.target_model_dir = target_model_dir

        ctx = EnvironmentContext()
        for name_type in self.model_name_types:
            _logger.info("Start to download the latest %s to '%s'.", name_type[0], target_model_dir)
            versions = ctx.model_store.query_latest_versions(name_type[0])
            if versions:
                for version in versions:
                    model_ref = ModelRef(name=name_type[0], version=version, type=name_type[1].value)
                    self.model_cache[model_ref], org_id = self.load_model_to_cache(ctx, model_ref=model_ref)
                    self.model_version_cache[model_ref.name + '-' + org_id] = model_ref
                    _logger.info("The Model %s for org %s has been downloaded and initialized", model_ref, org_id)
            else:
                _logger.error(f"No versions found for {name_type[0]}")
                raise ValueError(f"No versions found for {name_type[0]}")

        if self.kafka_configs:
            # start listening to models only after model_version_cache is populated
            self.listen_for_new_models(ctx)

    def consume_model_status(self, ctx: EnvironmentContext):

        topic = ctx.model_notif_kafka_topic
        config = {'bootstrap.servers': self.kafka_configs['kafka.bootstrap.servers'],
                  'group.id': 'model-consumer-' + str(uuid.uuid4()),
                  'auto.offset.reset': 'latest',
                  'enable.auto.commit': True}
        if self.kafka_configs['kafka.security.protocol'] == 'SSL':
            config['security.protocol'] = 'SSL'
            config['ssl.ca.location'] = self.kafka_configs['kafka.ssl.cafile.location']
            config['ssl.key.location'] = self.kafka_configs['kafka.ssl.keyfile.location']
            config['ssl.certificate.location'] = self.kafka_configs['kafka.ssl.certfile.location']
            config['ssl.endpoint.identification.algorithm'] = 'none'

        consumer = Consumer(config)
        _logger.info('Kafka Consumer has been initiated. Available topics to consume: ', consumer.list_topics().topics)

        consumer.subscribe([topic])
        _logger.info("Started Polling for topic: %s", topic)

        while self.kafka_configs:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    _logger.error("Topic %s not ready. Keep waiting for topic to become available...", topic)
                    continue
                elif message.error().code() == KafkaError.PARTITION_EOF:
                    _logger.error("Reached EOF for partition for Topic %s", topic)
                    continue
                else:
                    raise KafkaException(message.error())
            else:
                _logger.info("Received new model Key: %s Value: %s offset: %s",
                             message.key(), message.value(), message.offset())
                if message.value() is not None:
                    try:
                        model_json = json.loads(message.value())
                        model_ref = ModelRef(name=model_json[MODEL_NAME],
                                             version=model_json[MODEL_VERSION],
                                             type=model_json[MODEL_TYPE])
                        org_id = model_json[MODEL_ORG]
                        for name_type in self.model_name_types:
                            if model_ref.name == name_type[0]:
                                cache_version = self.get_model_version(model_name=model_ref.name, org_id=org_id)
                                if cache_version is None or model_ref.version > cache_version:
                                    self.model_cache[model_ref], org_id = self.load_model_to_cache(ctx,
                                                                                                   model_ref=model_ref)
                                    self.model_version_cache[model_ref.name + '-' + org_id] = model_ref
                                    old_model_ref = ModelRef(name=model_ref.name, version=cache_version, type=model_ref.type)
                                    del self.model_cache[old_model_ref]
                                    _logger.warning("The model version is updated to %s %s %s",
                                                    model_ref.name, model_ref.version, model_ref.type)
                            else:
                                _logger.info("Ignore model %s", model_ref)
                    except (ValueError, S3Error, Exception) as e:
                        _logger.error("Error on handling model status message: ", e)
                        continue

        consumer.close()

    def listen_for_new_models(self, ctx: EnvironmentContext):
        _logger.info("About to register listener to topic: %s", ctx.model_notif_kafka_topic)
        threading.Thread(target=self.consume_model_status, args=(ctx,), daemon=True).start()
        _logger.info("started kafka_consumer thread")

    def get_model_version(self, model_name: str, org_id: str = "vmware"):
        model_name = model_name + '-' + org_id
        if model_name in self.model_version_cache.keys():
            return self.model_version_cache[model_name].version
        else:
            raise ValueError(f"Model version for {model_name} not found")

    def load_model_to_cache(self, ctx: EnvironmentContext, model_ref: ModelRef):
        _logger.info("Start to load and build model %s", model_ref)
        model, org_id = get_model_loader(ctx, model_type=ModelType(model_ref.type),
                                         target_model_dir=self.target_model_dir) \
            .load_model(model_ref=model_ref)
        model = model.build_model()
        return model, org_id

    def does_model_exist(self, model_name: str, org_id: str = "vmware"):
        if model_name + '-' + org_id in self.model_version_cache.keys():
            return True
        return False

    def get_model(self, model_name: str, org_id: str = "vmware") -> PredictiveModel:
        model_ref = ModelRef(name=model_name,
                             version=self.get_model_version(model_name=model_name, org_id=org_id))
        if model_ref in self.model_cache.keys():
            return self.model_cache[model_ref]
        else:
            raise ValueError(f"Failed to get model {self.model_name}")
