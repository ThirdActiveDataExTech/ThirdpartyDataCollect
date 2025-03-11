import pika
import json
from common import rabbitmq


def publish(message, exchange, routing_key=''):
    message = json.dumps(message).encode('utf-8')
    # print(message)

    with pika.BlockingConnection(
        rabbitmq.get_connection_parameters()
    ) as connection:
        channel = connection.channel()

        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message
            # properties=pika.BasicProperties(
            #    delivery_mode=pika.DeliveryMode.Persistent
            # )
        )
