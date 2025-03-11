import pika
from common.log import log

from common.callback.manager import ManageCallback
from common import rabbitmq


def on_channel_open(channel):
    # for callback in [ManageCallback]:
    channel.basic_qos(prefetch_count=50)
    channel.basic_consume(ManageCallback.QUEUE, ManageCallback.callback, auto_ack=False, )


def on_open(_connection):
    _connection.channel(on_open_callback=on_channel_open)


def on_close(_connection, exception):
    _connection.ioloop.stop()


def server():
    connection = pika.SelectConnection(
        parameters=rabbitmq.get_connection_parameters(),
        on_open_callback=on_open,
        on_close_callback=on_close
    )

    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()


def server_start():
    server()


if __name__ == '__main__':
    log.info('Manager Server Start')
    server_start()
