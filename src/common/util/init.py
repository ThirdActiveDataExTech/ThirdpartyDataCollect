import time

import pika
from common import rabbitmq
from common import db

from common import config


def rabbitmq_setup():
    connection = pika.BlockingConnection(
        rabbitmq.get_connection_parameters()
    )
    channel = connection.channel()
    channel.queue_declare(queue='all_urls', durable=False, auto_delete=False, exclusive=False)
    channel.queue_declare(queue='crawling_urls', durable=False, auto_delete=False, exclusive=False)

    channel.exchange_declare(exchange='all_urls_exchange', exchange_type='topic')
    channel.exchange_declare(exchange='crawling_urls_exchange', exchange_type='topic')

    channel.queue_bind(exchange='all_urls_exchange', queue='all_urls', routing_key='#')
    channel.queue_bind(exchange='crawling_urls_exchange', queue='crawling_urls', routing_key='#')

    connection.close()


def db_setup():
    db.execute('''drop table if exists metadb''', config.META_DB_PATH)
    db.execute('''drop table if exists urldb''', config.URL_DB_PATH)

    """ storage metadata 테이블 생성 """
    create_metadata = f"""
        create table if not exists metadb (
            platform text,
            blog_id text,
            post_id text,
            html_save boolean,
            txt_save boolean
        )
    """
    db.execute(create_metadata, config.META_DB_PATH)

    """ url 테이블 생성 """
    create_urldb = f"""
        create table if not exists urldb (
            url text,
            collection_time datetime,
            crawler_time datetime
        )
    """
    db.execute(create_urldb, config.URL_DB_PATH)


if __name__ == "__main__":
    rabbitmq_setup()
    db_setup()