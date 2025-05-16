import json
import time
import pika

import requests
from bs4 import BeautifulSoup
from common import util

import re

'''
언론사 'dailian' 의 뉴스 기사 크롤러 모듈 입니다.
'''


def get_links(url):
    dailian_base_url = 'https://www.dailian.co.kr'
    embedded_links = set()

    page = util.read_web(url)

    if page is not None:
        links = page.select("a")
        for l in links:
            url_candidate = l.get("href")
            if isinstance(url_candidate, str) and re.search("/news/view/\d+/", url_candidate):
                embedded_url = dailian_base_url + url_candidate
                embedded_links.add(embedded_url)

    return embedded_links

    # page = util.read_web('https://www.dailian.co.kr/news/view/1359210/')
    #


if __name__ == '__main__':
    start_url = 'https://www.dailian.co.kr/home'
    get_links(start_url)
