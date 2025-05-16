import json
import os
import urllib.request
import uuid

import requests
import re

from urllib.parse import urlparse
from common import log
from bs4 import BeautifulSoup
from common import error
from common.config.user_config import Config


def make_file_path(origin, file_id):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_dir = os.path.join(root_dir, 'extract/tmp_files/', origin)
    file_path = file_dir + "/" + file_id
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    return file_path


def search_api(url):
    client_id = Config.naver_api.client_id
    client_secret = Config.naver_api.client_secret
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()

        return json.loads(response_body.decode('utf-8'))['items']
    else:
        print("Error Code:" + rescode)


# url의 내용을 크롤링하는 함수
def get_crawling_file(origin, url, file_name):
    if origin == 'blog':
        # URL 유효성 체크
        url = url[0:8] + 'm.' + url[8:]

    try:
        status_check(url)
    except requests.exceptions.HTTPError:
        raise

    try:
        page = read_web(url)
    except requests.exceptions.HTTPError:
        raise

    file_path = load_to_file(origin, page, file_name)

    return file_path


def read_web(url):
    response = requests.get(url, timeout=5)
    status_check(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def status_check(url):
    response = requests.get(url)
    if response.status_code != 200:  # 정상 연결시
        raise error.WebRequestsError(url, response.status_code)


# 크롤링 결과를 file로 저장하는 함수
def load_to_file(origin, page, file_name):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_dir = f"{root_dir}/extract/tmp_files/{origin}/"
    file_path = file_dir + file_name
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(page.get_text(), f, ensure_ascii=False, indent=4)
        except EOFError as e:
            print(f"파일 저장 실패: {e}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return file_path


# blog data_id 추출 함수
def get_data_id(origin, url):
    if origin == "blog":
        # blog url은 https://blog.naver.com/ms_hs-93/223780771002" 형식
        match = re.search(r"blog.naver.com/([a-zA-Z0-9_-]+)/([0-9]+)", url)
        if match:
            return f"{match.group(1)}_{match.group(2)}"
        else:
            log.info("data_id 추출 실패 - 올바르지 않은 blog url 형식")
        return ""

    elif origin == "news":
        parsed = urlparse(url)
        # 사이트 이름 추출
        site = parsed.netloc.split('.')[1]

        # 기사 ID 추출 (no= 또는 idxno= 또는 entry_id= 등 다양한 경우 커버)
        id_match = re.search(r'([A-Za-z0-9._%+-]+)=(\d+)', parsed.query).group(2)
        if not id_match:
            # 쿼리 스트링에 없는 경우 path에서 숫자 추출 시도
            id_match = parsed.path.split("/")[-1]
            if site in id_match:
                return id_match

        return f"{site}{id_match}"

    elif origin == "youtube":
        # Youtube url은 "https://www.youtube.com/watch?v=A3DtaMoTBbA&t=2304s" 형식
        match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
        if match:
            return match.group(1)
        else:
            log.info("data_id 추출 실패 - 올바르지 않은 youtube url 형식")
    else:
        log.info("data_id 추출 실패 - 지원하지 않는 데이터 원천")
