from functools import cached_property

from reach_commons.reach_aws.sqs.client import SQSClient


class HandlerHubspotMessage:
    def __init__(self, log_level="info", region_name="us-east-1"):
        self.log_level = log_level
        self.region_name = region_name
        self.service_name = "hubspot"

    @cached_property
    def client(self):
        return SQSClient(
            topic_name="Staging-reach-data-bridge-messages-queue",
            log_level=self.log_level,
            region_name=self.region_name,
        )

    def handle_business(self, business_id, additional_info=None):
        return self.client.publish(
            message_data={
                "object_name": "business",
                "object_id": business_id,
                "additional_info": additional_info,
            },
            message_attributes={"service_name": self.service_name},
        )
