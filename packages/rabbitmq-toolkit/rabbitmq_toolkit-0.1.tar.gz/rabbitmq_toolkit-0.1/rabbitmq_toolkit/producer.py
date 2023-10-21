import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Producer:
    def __init__(self, queue_manager):
        self._queue_manager = queue_manager

    def send_message(self, queue_name, message):
        """Sends a message to the specified queue."""
        try:
            self._queue_manager.channel.basic_publish(exchange='', routing_key=queue_name, body=message)
            logger.info("Sent message to %s: %s", queue_name, message)
        except Exception as e:
            logger.error("Error sending message: %s", e)
