import json
import logging

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
            logging.info("Sent message to %s: %s", queue_name, serialized_message)
        except Exception as e:
            logging.error("Error sending message: %s", e)
