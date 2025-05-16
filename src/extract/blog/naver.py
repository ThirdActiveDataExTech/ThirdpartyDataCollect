from bs4 import BeautifulSoup
from common import util
import re

from common.log import log


def parse(page: BeautifulSoup):
    title = util.remove_tag(page.select(".se-module.se-module-text.se-title-text")[0])
    body = page.select_one(".se-main-container").find_all('p')

    body_list = []
    for n, row in enumerate(body):
        row = util.remove_tag(row)
        if row == '':
            continue
        body_list.append(f'<p data-reader-unique-id={n}>{row}</p>')

    return title, body_list


def get_links(page: BeautifulSoup):
    link_list = []

    links = page.select("a")
    # print(links)
    for l in links:
        url_candidate = l.get("href")
        print(type(url_candidate), url_candidate)
        # if isinstance(url_candidate, str) and re.search("https?://\w+", url_candidate):
        #     print(url_candidate)


def test():
    from common import util
    # d = util.read_web('https://m.blog.naver.com/qufslagkdl/223391689387')
    page = util.read_web('https://m.blog.naver.com/cltube/223391894408')
    # title, body = parse(page)
    # for row in body:
    #     print(row)

    get_links(page)


def validate_url_check(url):
    naver_pattern = r"https://blog\.naver\.com/([^/]+)/(\d+)"
    naver = re.match(naver_pattern, url)
    if naver:
        url = url.replace("https://blog", "https://m.blog")

    naver_common_pattern = r"https://m\.blog\.naver\.com/([^/]+)\.naver"
    common_match = re.match(naver_common_pattern, url)
    if common_match:
        # log.info(f'common url : {url}')
        return None

    return url


if __name__ == '__main__':
    test()
