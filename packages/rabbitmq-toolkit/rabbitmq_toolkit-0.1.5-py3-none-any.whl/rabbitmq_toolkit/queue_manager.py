import pika
import logging


class QueueManager:
    def __init__(self, host='localhost'):
        """
        Constructor for the QueueManager.

        :param host: RabbitMQ server host. Default is 'localhost'.
        """
        self._host = host
        self._connection = None
        self._channel = None
        self.connect()

    def connect(self):
        """
        Connects to the RabbitMQ server.
        """
        try:
            params = pika.ConnectionParameters(self._host, heartbeat=600)
            self._connection = pika.BlockingConnection(params)
            self._channel = self._connection.channel()
            logging.info("Connected to RabbitMQ on %s", self._host)
        except Exception as e:
            logging.error("Error connecting to RabbitMQ: %s", e)

    def ensure_connection(self):
        """
        Ensures that a connection and channel to the RabbitMQ server exist and are open.
        If not, it tries to reconnect.
        """
        if not self._connection or not self._connection.is_open:
            self.connect()

    def declare_queue(self, queue_name):
        """
        Declares a queue.

        :param queue_name: Name of the queue to be declared.
        """
        try:
            self.ensure_connection()
            # durable - queues will still exist after the server is back up after restart.
            self._channel.queue_declare(queue=queue_name, durable=True)
            logging.info("Declared queue %s", queue_name)
        except Exception as e:
            logging.error("Error declaring queue: %s", e)

    def delete_queue(self, queue_name):
        """
        Deletes a queue.

        :param queue_name: Name of the queue to be deleted.
        """
        try:
            self.ensure_connection()
            self._channel.queue_delete(queue=queue_name)
            logging.info("Deleted queue %s", queue_name)
        except Exception as e:
            logging.error("Error deleting queue: %s", e)

    @property
    def channel(self):
        """
        Returns the channel object.

        :return: Channel object.
        """
        self.ensure_connection()
        return self._channel

    def close(self):
        """
        Closes the channel and connection gracefully.
        """
        try:
            if self._channel and self._channel.is_open:
                self._channel.close()
            if self._connection and self._connection.is_open:
                self._connection.close()
            logging.info("Connection closed")
        except Exception as e:
            logging.error("Error closing connection: %s", e)
