import pika
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueueManager:
    def __init__(self, host='localhost'):
        """
        Initializes the QueueManager with a connection to RabbitMQ.

        Args:
        - host (str): The hostname of the RabbitMQ server. Default is 'localhost'.
        """
        try:
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(host, heartbeat=600))
            self._channel = self._connection.channel()
            logger.info("Connected to RabbitMQ on %s", host)
        except Exception as e:
            logger.error("Error connecting to RabbitMQ: %s", e)

    def declare_queue(self, queue_name):
        """Declares a queue."""
        try:
            self._channel.queue_declare(queue=queue_name)
            logger.info("Declared queue %s", queue_name)
        except Exception as e:
            logger.error("Error declaring queue: %s", e)

    def delete_queue(self, queue_name):
        """Deletes a queue."""
        try:
            self._channel.queue_delete(queue=queue_name)
            logger.info("Deleted queue %s", queue_name)
        except Exception as e:
            logger.error("Error deleting queue: %s", e)

    @property
    def channel(self):
        """Returns the channel."""
        return self._channel

    def close(self):
        """Closes the channel and connection."""
        try:
            self._channel.close()
            self._connection.close()
            logger.info("Connection closed")
        except Exception as e:
            logger.error("Error closing connection: %s", e)
