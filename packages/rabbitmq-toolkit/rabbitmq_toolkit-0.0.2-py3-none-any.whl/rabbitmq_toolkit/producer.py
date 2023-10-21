import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Producer:
    def __init__(self, queue_manager):
        self._queue_manager = queue_manager

    @staticmethod
    def serialize_message(data):
        """Serialize data into a JSON string."""
        return json.dumps(data)

    def send_message(self, queue_name, message):
        """Sends a message to the specified queue."""
        try:
            serialized_message = Producer.serialize_message(message)
            self._queue_manager.channel.basic_publish(exchange='', routing_key=queue_name, body=serialized_message)
            logger.info("Sent message to %s: %s", queue_name, serialized_message)
        except Exception as e:
            logger.error("Error sending message: %s", e)
