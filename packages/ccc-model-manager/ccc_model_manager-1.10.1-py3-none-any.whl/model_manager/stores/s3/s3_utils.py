# Copyright (c) 2022 VMware, Inc. All Rights Reserved.

import logging
import os
import boto3

from minio import Minio
from minio.error import MinioException

_logger = logging.getLogger(__name__)
MAX_RETRIES = 5


class S3Utils(object):
    """
    Util class to handle common s3 tasks across s3_blob_store.py and s3_uploader
    """
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str, region: str = None,
                 secure: bool = True):
        _logger.debug(
            "S3 blob store endpoint: %s bucket: %s region: %s secure: %s" % (endpoint, bucket, region, secure))
        self._endpoint = endpoint
        self._secure = secure
        self._bucket = bucket
        self._region = region
        self._access_key = access_key
        self._secret_key = secret_key
        self._client = self._init_client()

    def get_client(self):
        """ returns a singleton client to connect to s3"""
        try:
            if not self._client:
                self._client = self._init_client()
            self._client.bucket_exists(self._bucket)  # check if valid connection
        except MinioException:
            self._client = self._init_client()
        return self._client

    def _init_client(self, retry_counter=0):
        client = None
        aws_arn_role = os.getenv("AWS_ROLE_ARN", "")
        aws_web_identity_token_file = os.getenv("AWS_WEB_IDENTITY_TOKEN_FILE", "")
        aws_web_identity_token = ""
        if aws_web_identity_token_file:
            aws_web_identity_token = open(aws_web_identity_token_file).read()

        try:
            _logger.info(f"Trying to connect to s3. Attempt {retry_counter} of {MAX_RETRIES}")

            if aws_arn_role and aws_web_identity_token:
                session = boto3.Session(region_name=self._region)
                sts_client = session.client('sts')
                response = sts_client.assume_role_with_web_identity(
                    RoleArn=aws_arn_role,
                    WebIdentityToken=aws_web_identity_token,
                    RoleSessionName="ccc-ml-pipeline"
                )

                credentials = response["Credentials"]

                client = Minio(
                    endpoint=self._endpoint,
                    region=self._region,
                    access_key=credentials['AccessKeyId'],
                    secret_key=credentials['SecretAccessKey'],
                    session_token=credentials['SessionToken'],
                    secure=self._secure
                )

            else:
                client = Minio(self._endpoint, access_key=self._access_key,
                               secret_key=self._secret_key,
                               secure=self._secure,
                               region=self._region)
            _logger.info(f"Connected to s3 at endpoint: {self._endpoint}")

        except MinioException as e:
            if retry_counter < MAX_RETRIES:
                self._init_client(retry_counter + 1)
            else:
                raise e
        # create bucket with given name
        if client.bucket_exists(self._bucket):
            return client
        # if bucket doesn't exist (e.g. new local minio setup) try and create
        # will already exist in prod deployment where we don't have permission to create anyway
        try:
            client.make_bucket(self._bucket, self._region)
        except BucketAlreadyOwnedByYou:
            pass
        except BucketAlreadyExists:
            pass
        except ResponseError:
            raise
        return client
