import json
import os
import urllib.parse
import urllib.request
import uuid

import requests

import search
import util
from config.config import Config

from extract.keyword.extract_keyword import extract_keyword


def blog_api_temp(search_term):
    client_id = Config.naver_api.client_id
    client_secret = Config.naver_api.client_secret
    enc_text = urllib.parse.quote(search_term)
    url = "https://openapi.naver.com/v1/search/blog?query=" + enc_text  # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()

        return response_body.decode('utf-8')
    else:
        print("Error Code:" + rescode)


def get_data_list(search_response):
    for item in search_response:
        title = item.get("title")
        blog_url = item.get("bloggerlink")
        post_date = item.get("postdate")
        file = get_crawling_file(item.get("link"))

        data_list = [title, blog_url, post_date, file]
        load_data(data_list)


def get_crawling_file(link):
    # URL 유효성 체크
    url = link[0:8] + 'm.' + link[8:]
    try:
        util.status_check(url)
    except requests.exceptions.HTTPError:
        raise
    try:
        page = util.read_web(url)
    except requests.exceptions.HTTPError:
        raise
    text_data = page.get_text()

    file_name = str(uuid.uuid4())
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_dir = os.path.join(root_dir, 'tmp_files/blog/')
    file_path = file_dir + file_name
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(text_data, f, ensure_ascii=False, indent=4)
        except EOFError as e:
            print(f"파일 저장 실패: {e}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return file_name


class ExtractBlogUrl:
    def __init__(self, search_word):
        self.search_word = search_word

    def blog_crawler(self):
        # 해당 web 에 있는 모든 url 을 수집해 리턴
        blog_url_list = search.search_link(self.search_word)

        path_list = []

        for blog_url in blog_url_list:
            # URL 유효성 체크
            url = blog_url[0:8] + 'm.' + blog_url[8:]
            try:
                util.status_check(url)
            except requests.exceptions.HTTPError:
                raise
            try:
                page = util.read_web(url)
            except requests.exceptions.HTTPError:
                continue
            text_data = page.get_text()

            file_name = str(uuid.uuid4())
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_dir = os.path.join(root_dir, 'tmp_files/blog/')
            file_path = file_dir + file_name
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            try:
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(text_data, f, ensure_ascii=False, indent=4)
                except EOFError as e:
                    print(f"파일 저장 실패: {e}")
            except Exception as err:
                print(f"An error occurred: {err}")

            path_list.append(file_path)

        extract_keyword(path_list)
        return path_list


if __name__ == "__main__":
    start_word = '고양이'
    # extractor = ExtractBlogUrl(start_word)
    # crawler = extractor.blog_crawler()
    api_request = blog_api_temp(start_word)