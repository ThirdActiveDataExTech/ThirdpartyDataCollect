from extract.blog.crawler import Crawler
import json

from common.log import log


def process(routing_key, url):
    crawler = Crawler()
    crawler.crawler(url)


class CrawlerCallback:
    QUEUE = 'crawling_urls'

    @staticmethod
    def callback(channel, method, properties, body):
        try:
            process(method.routing_key, json.loads(body.decode('utf-8')))
        except BaseException as e:
            log.error('Error at callback: ' + str(e))
        finally:
            channel.basic_ack(delivery_tag=method.delivery_tag)
