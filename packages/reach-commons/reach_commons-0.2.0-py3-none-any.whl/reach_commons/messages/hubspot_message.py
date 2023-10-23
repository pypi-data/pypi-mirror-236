import os
from reach_commons.reach_aws.sqs.client import SQSClient


class HubspotMessage:
    SERVICE_NAME = "hubspot"
    TOPIC_NAME = "reach-data-bridge-messages-queue"
    DEFAULT_LOG_LEVEL = "info"
    DEFAULT_REGION = "us-east-1"
    DEFAULT_TOPIC_PREFIX = os.environ.get("ENV", "Staging")

    def __init__(
        self,
        log_level=DEFAULT_LOG_LEVEL,
        region_name=DEFAULT_REGION,
        topic_prefix=DEFAULT_TOPIC_PREFIX,
    ):
        self.log_level = log_level
        self.region_name = region_name
        self.topic_prefix = topic_prefix

    @property
    def client(self):
        return SQSClient(
            topic_name=f"{self.topic_prefix}-{self.TOPIC_NAME}",
            log_level=self.log_level,
            region_name=self.region_name,
        )

    def send_business_message(self, business_id, additional_info=None):
        return self.client.publish(
            message_data={
                "object_name": "business",
                "object_id": business_id,
                "additional_info": additional_info,
            },
            message_attributes={"service_name": self.SERVICE_NAME},
        )


hubspot_msg = HubspotMessage()
hubspot_msg.send_business_message(business_id=10293)
