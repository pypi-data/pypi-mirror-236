import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self, queue_manager):
        self._queue_manager = queue_manager

    @staticmethod
    def deserialize_message(message_str):
        """Deserialize a JSON string into a Python object."""
        return json.loads(message_str)

    def start_consuming(self, queue_name, callback):
        """Starts consuming messages from the specified queue."""

        def internal_callback(ch, method, properties, body):
            try:
                # Deserialize the message body
                deserialized_body = Consumer.deserialize_message(body)

                # Pass the deserialized body to the callback
                callback(deserialized_body)

                ch.basic_ack(delivery_tag=method.delivery_tag)
                logger.info("Received message from %s: %s", queue_name, deserialized_body)
            except Exception as e:
                logger.error("Error processing message: %s", e)
                ch.basic_nack(delivery_tag=method.delivery_tag)

        self._queue_manager.channel.basic_consume(queue=queue_name, on_message_callback=internal_callback)
        try:
            self._queue_manager.channel.start_consuming()
        except Exception as e:
            logger.error("Error starting consuming: %s", e)
