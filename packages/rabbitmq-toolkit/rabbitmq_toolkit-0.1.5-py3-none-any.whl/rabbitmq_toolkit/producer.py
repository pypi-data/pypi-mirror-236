import json
import logging
import pika

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
            # Ensure there's a live connection before sending
            self._queue_manager.ensure_connection()

            serialized_message = Producer.serialize_message(message)

            logging.info("Attempting to send message to %s: %s", queue_name, serialized_message)

            # delivery_mode = 2 makes the message persistent.
            # the message is stored both in memory and on disk. If the RabbitMQ server restarts,
            # the message will still be there afterward.
            properties = pika.BasicProperties(delivery_mode=2)

            self._queue_manager.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=serialized_message,
                properties=properties
            )
            logging.info("Sent message to %s: %s", queue_name, serialized_message)
        except Exception as e:
            logging.error("Error sending message: %s", e)
