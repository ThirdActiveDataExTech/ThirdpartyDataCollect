import json
import time
import pika

import requests
from bs4 import BeautifulSoup
from common import util

import re


def get_links(page: BeautifulSoup):

    dailian_base_url = 'https://www.dailian.co.kr'

    links = page.select("a")
    for l in links:
        url_candidate = l.get("href")
        # print(type(url_candidate), url_candidate)
        if isinstance(url_candidate, str) and re.search("/news/view/\d+/", url_candidate):
            embedded_url = dailian_base_url + url_candidate
            print(embedded_url)


    # page = util.read_web('https://www.dailian.co.kr/news/view/1359210/')
    #
    # # 1. html 데이터 수집
    # html_data = str(page)
    #
    # # 2. text 데이터 수집
    # text_data = page.get_text()
    #
    # # print(html_data)
    # print(text_data)



def run(url):
    # response = requests.get(url)
    page = util.read_web(url)
    if page is not None:
        get_links(page)


if __name__ == '__main__':
    start_url = 'https://www.dailian.co.kr/home'
    run(start_url)
