import json
import urllib
from urllib.parse import urlparse

import requests

from config.config import NaverAPIIdentify
import urllib.request


def grab_url_list(search_word: str):
    client_id = NaverAPIIdentify.client_id
    client_secret = NaverAPIIdentify.client_secret

    enctext = urllib.parse.quote(search_word)
    url = "https://openapi.naver.com/v1/search/blog?query=" + enctext + "&display=5&sort=date"  # JSON 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    page = response.getcode()
    if page == 200:
        response_body = response.read().decode("utf-8")
        return json.loads(response_body)
    else:
        print("Error Code:" + page)
        return None


def search_link(search_word: str):
    searched_url = set()
    try:
        page = grab_url_list(search_word)
    except requests.exceptions.HTTPError:
        raise

    items = page["items"]
    for item in items:
        url = item["link"]

        try:
            url = urlparse(url)
        except ValueError as e:
            print("Error: " + ' '.join(e.args))
            continue
        url_path = f'{url.scheme}://{url.netloc}{url.path}'
        searched_url.add(url_path)
    return searched_url


if __name__ == '__main__':
    start_word = '고양이'
    search_link(start_word)
