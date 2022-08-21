import json
import pika

class Publisher:
    EXCHANGE="netflow"
    ROUTING_KEY="flow"

    def __init__(self, config):
        self.config = config
        self._connection_params = pika.connection.ConnectionParameters(
            host=config["host"],
            credentials=pika.credentials.PlainCredentials(config["username"], config["password"])
        )
        self._connection = None
        self._channel = None

    def connect(self):
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(self._connection_params)
            self._channel = self._connection.channel()
            self._channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='fanout')

    def _publish(self, payload):
        self._channel.basic_publish(
            exchange=self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            body=json.dumps(payload)
        )

    def publish(self, payload):
        try:
            self._publish(payload)
        except pika.exceptions.ConnectionClosed:
            self.connect()
            self._publish(payload)

    def close(self):
        if self._connection and self._connection.is_open:
            self._connection.close()