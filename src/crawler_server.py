import pika

from common.callback.crawler import CrawlerCallback
from common import rabbitmq
from common.log import log


# def on_channel_open(channel):
#     # for callback in [CrawlerCallback]:
#     channel.basic_qos(prefetch_count=100)
#     channel.basic_consume(CrawlerCallback.QUEUE, CrawlerCallback.callback, auto_ack=False, )
#
#
# def on_open(_connection):
#     _connection.channel(on_open_callback=on_channel_open)
#
#
# def on_close(_connection, exception):
#     _connection.ioloop.stop()
#
#
# def server():
#     connection = pika.SelectConnection(
#         parameters=rabbitmq.get_connection_parameters(),
#         on_open_callback=on_open,
#         on_close_callback=on_close
#     )
#
#     try:
#         connection.ioloop.start()
#     except KeyboardInterrupt:
#         connection.close()
#         # connection.ioloop.start()


def server():
    with pika.BlockingConnection(
            rabbitmq.get_connection_parameters()
    ) as connection:
        channel = connection.channel()
        channel.basic_qos(prefetch_count=100)
        channel.basic_consume(queue=CrawlerCallback.QUEUE, on_message_callback=CrawlerCallback.callback, auto_ack=False)
        channel.start_consuming()



def server_start():
    server()


if __name__ == '__main__':
    log.info('Crawler Server Start')
    server_start()
