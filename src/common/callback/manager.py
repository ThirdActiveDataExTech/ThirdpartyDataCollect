import json
import re
import time
from datetime import datetime

from common import db
from common import config
from common.log import log
from common.response import publish

from blog import naver


def url_filter(url):
    """
    수집할 대상이 되는 url 인지 확인
        - 이미 수집했는지, 수집 범위에 들어오는 플랫폼인지
    """

    naver_pattern = r"https?://(?:m\.)?blog\.naver\.com/([^/]+)"
    match_naver = re.match(naver_pattern, url)

    tistory_pattern = r"https?://([^\.]+)\.tistory\.com/(?:m/)?(\d+)"
    match_tistory = re.match(tistory_pattern, url)

    dailian_pattern = r"https?://(?:www\.)?dailian\.co\.kr/news/view/(\d+)/"
    match_dailian = re.match(dailian_pattern, url)

    if match_naver or match_tistory or match_dailian:
        if match_naver:
            url = naver.validate_url_check(url)
            if url is None:
                return None
        result = db.execute_select('''select * from urldb where url = ?''', config.URL_DB_PATH, (url,))
        if len(result) == 0 or result is None:
            log.info(f'ready to collect URL: {url}')
            return url
    else:
        log.info(f'{url} is not valid URL for crawling')
        return None


def process(routing_key, url):
    target_url = url_filter(url)

    if target_url is not None:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute('''insert into urldb values(?,?,?)''', config.URL_DB_PATH, (target_url, current_time, None,))
        publish(target_url, exchange='crawling_urls_exchange', routing_key='')


class ManageCallback:

    import os
    os.environ["APP_NAME"] = "crawler"
    QUEUE = 'all_urls'

    @staticmethod
    def callback(channel, method, properties, body):
        try:
            process(method.routing_key, json.loads(body.decode('utf-8')))
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except BaseException as e:
            log.error(str(e))
