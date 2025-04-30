import json
import os
import uuid
from urllib.parse import urlencode
from src.common.config.user_config import Config

import requests


def make_file_path(url):
    file_name = str(uuid.uuid4()) + ".txt"
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_dir = os.path.join(root_dir, 'tmp_files/')
    file_path = file_dir + file_name
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    return file_path, file_name


def get_data_portal(endpoint, data_portal_params=None):
    """
    공공 데이터 포털 API에서 데이터를 가져옵니다.

    :param data_portal_params: 추가적인 파라미터 (딕셔너리 형태)
    :return: JSON 응답 데이터
    """
    param = urlencode(data_portal_params)

    url = (f"https://{Config.data_portal.base_url}{endpoint}?serviceKey="
           f"{Config.data_portal.service_key}&{param}")

    try:
        response = requests.get(url)
        file_path, file_id = make_file_path(url)
        bucket_name = "dataportal"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
        except EOFError as e:
            print(f"파일 저장 실패: {e}")

        return file_id, file_path, bucket_name
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


def get_data_seoul(endpoint, data_seoul_params=None):
    """
    서울열린데이터포털 API에서 데이터를 가져옵니다.

    :return: JSON 응답 데이터
    """

    url = f"http://{Config.seoul_portal.base_url}{Config.seoul_portal.service_key}{endpoint}"

    try:
        response = requests.get(url)
        file_path, file_id = make_file_path(url)
        bucket_name = "seoulportal"
        if response.status_code == 200:
            content = response.text
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except EOFError as e:
                print(f"파일 저장 실패: {e}")
            return file_id, file_path, bucket_name
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


if __name__ == "__main__":
    data_portal_base_url = Config.data_portal.base_url  # 데이터 포털의 기본 URL
    data_portal_endpoint = "/15113444/v1/uddi:1ae26320-fa56-4206-8d06-9ee5db5a8dcf"  # API 엔드포인트
    data_portal_service_key = Config.data_portal.service_key

    data_seoul_base_url = Config.seoul_portal.base_url
    data_seoul_endpoint = "/xml/publicHygieneBizCleaningProducts/1/5/"
    data_seoul_service_key = Config.seoul_portal.service_key

    data_portal_api = get_data_portal(data_portal_endpoint)
    data_seoul_api = get_data_seoul(data_seoul_endpoint)

    params = {"pageNo": "1", "numOfRows": "1", "_type": "json", "nm": "강북"}

    data_portal = data_portal_api.get_data_portal(params)
    data_seoul = data_seoul_api.get_data_seoul()
    if data_portal:
        print(data_portal)
        print("\n")
    else:
        print("get_data_portal failed\n")

    if data_seoul:
        print(data_seoul)
        print("\n")
    else:
        print("get_data_seoul failed\n")
