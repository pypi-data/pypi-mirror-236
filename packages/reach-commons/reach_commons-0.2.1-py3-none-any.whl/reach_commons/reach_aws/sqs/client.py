import json
import logging
from decimal import Decimal
from functools import cached_property

import boto3
from botocore.exceptions import ClientError

from reach_commons.reach_aws.sqs.exceptions import (SQSClientPublishError,
                                                    SQSClientTopicNotFound)

logger = logging.getLogger(__name__)

MESSAGE_ATTRIBUTES_TYPE = {
    str: "String",
    int: "Number",
    Decimal: "Number",
    float: "Number",
    bytes: "Binary",
    list: "String.Array",
    tuple: "String.Array",
}

FALLBACK_MESSAGE_ATTRIBUTES_TYPE = "String"


# noinspection PyMethodMayBeStatic
class BaseSQSClient:
    def __init__(self, topic_name=None, log_level="debug", region_name="us-east-1"):
        self.topic_name = topic_name
        self.log_level = log_level
        self.region_name = region_name

    @property
    def log(self):
        return getattr(logger, self.log_level)

    @staticmethod
    def _prepare_message_attributes(attributes):
        message_attributes = {}
        for key, value in attributes.items():
            attr_type = MESSAGE_ATTRIBUTES_TYPE.get(
                type(value), FALLBACK_MESSAGE_ATTRIBUTES_TYPE
            )
            value_key = "BinaryValue" if attr_type == "Binary" else "StringValue"
            if attr_type in ("String.Array", "Number"):
                value = json.dumps(value)
            elif attr_type == "String":
                value = str(value)
            message_attributes[key] = {
                "DataType": attr_type,
                value_key: value,
            }
        return message_attributes

    def handle_exception(self, exc, message_data, message_attributes):
        error_msg = (
            "error_publishing_message, "
            "topic_name={}, "
            "message_data={!r}, "
            "message_attributes={!r}, "
            "error={!r}".format(self.topic_name, message_data, message_attributes, exc)
        )
        logger.error(error_msg)
        if exc.response["Error"]["Code"] == "NotFound":
            raise SQSClientTopicNotFound(error_msg)
        raise SQSClientPublishError(error_msg)


class SQSClient(BaseSQSClient):
    @cached_property
    def client(self):
        return boto3.client("sqs")

    def publish(self, message_data, message_attributes=None):
        message_attributes = message_attributes or {}
        message_attributes = self._prepare_message_attributes(message_attributes)

        logger.info(
            "topic_name={}, "
            "message_data={!r}, "
            "message_attributes={!r}".format(
                self.topic_name, message_data, message_attributes
            )
        )

        message = json.dumps(message_data)

        try:
            self.client.send_message(
                QueueUrl=self.topic_name,
                MessageBody=message,
                DelaySeconds=1,
                MessageAttributes=message_attributes,
            )
        except ClientError as exc:
            self.handle_exception(exc, message_data, message_attributes)

        self.log(
            "published_message, "
            "topic_name={}, "
            "message={!r}, "
            "message_attributes={!r}".format(
                self.topic_name, message, message_attributes
            )
        )

        return True
