import json
import logging


class Consumer:
    def __init__(self, queue_manager):
        self._queue_manager = queue_manager

    @staticmethod
    def deserialize_message(message_str):
        """Deserialize a JSON string into a Python object."""
        return json.loads(message_str)

    def start_consuming(self, queue_name, callback, requeue_on_error=False):
        """Starts consuming messages from the specified queue."""

        def internal_callback(ch, method, properties, body):
            try:
                # Deserialize the message body
                deserialized_body = Consumer.deserialize_message(body)

                # Log the received message
                logging.info("Received message from %s: %s", queue_name, deserialized_body)

                # Pass the deserialized body to the callback
                callback(deserialized_body)

                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logging.error("Error processing message from %s: %s", queue_name, e)

                # Determine if the message should be requeued
                should_requeue = requeue_on_error

                # Send a negative acknowledgment
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=should_requeue)

        # Ensure a valid connection before consuming
        self._queue_manager.ensure_connection()

        self._queue_manager.channel.basic_consume(queue=queue_name, on_message_callback=internal_callback)
        try:
            logging.info("Starting to consume messages from %s", queue_name)
            self._queue_manager.channel.start_consuming()
        except Exception as e:
            logging.error("Error starting consuming from %s: %s", queue_name, e)
