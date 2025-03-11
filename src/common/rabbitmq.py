import pika
from . import config


def get_connection_parameters():
    # props = {'connection_name': os.getenv('HOSTNAME', 'mq-collector')}
    return pika.ConnectionParameters(
        config.QUEUE_HOST,
        config.QUEUE_PORT,
        credentials=pika.PlainCredentials(
            username=config.QUEUE_USER,
            password=config.QUEUE_PASS
        ),
        # client_properties=props,
        # heartbeat=60,
        # tcp_options={'TCP_KEEPALIVE':30}
    )
