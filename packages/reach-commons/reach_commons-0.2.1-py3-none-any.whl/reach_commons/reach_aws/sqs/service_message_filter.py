import json
import logging

logger = logging.getLogger(__name__)


class ServiceMessageFilter:
    """
    A utility class responsible for filtering SQS messages based on the service name.

    Methods:
        filter_messages(service_name: str, event: dict) -> list:
            Filters messages from the provided event based on the service name.
    """

    @staticmethod
    def filter_messages(event, service_name=None):
        """
        Filter messages from the provided event based on the given service name.

        If the service_name is None or matches the service specified in the message attributes,
        the message is included in the returned list.

        Args:
        - service_name (str): The name of the service to filter messages for.
                             If None, all messages are returned.
        - event (dict): The event data containing SQS records.

        Returns:
        - list: A list of messages filtered based on the service name.
        """
        logger.info(event)
        messages = []

        for record in event.get("Records", []):
            message_body = (
                record["body"]
                if isinstance(record["body"], dict)
                else json.loads(record["body"])
            )

            if (
                not service_name
                or service_name == record["messageAttributes"]["service"]["stringValue"]
            ):
                messages.append(message_body)

        return messages
