import json
from urllib.parse import urlencode
from datetime import datetime

from load.load_data import minio_load
from src.common.config.user_config import Config
from src.common.common_def import make_file_path

import requests

origin = "portal"


def get_data_seoul(endpoint, data_seoul_params=None):
    """
    서울열린데이터포털 API에서 데이터를 가져옵니다.

    :param endpoint: 수집할 url endpoint
    :param data_seoul_params: 추가적인 파라미터 (딕셔너리 형태)
    :return: JSON 응답 데이터
    """

    params = urlencode(data_seoul_params)
    url = f"http://{Config.seoul_portal.base_url}{Config.seoul_portal.service_key}{endpoint}"
    data = {}

    try:
        response = requests.get(url, params=params)
        if endpoint[0] == "/":
            data_id = endpoint.replace("/", "_")[1:]
        else:
            data_id = endpoint.replace("/", "_")
        file_path = make_file_path("seoulportal", data_id)
        data["url"] = f"{url}?{params}"
        data["data_id"] = data_id
        data["origin"] = origin
        data["date"] = datetime.now().date()

        if response.status_code == 200:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    # f.write(response.text)
                    json.dump(response.json(), f, ensure_ascii=False, indent=4)
            except EOFError as e:
                print(f"파일 저장 실패: {e}")
            data["file_path"] = minio_load("seoulportal", file_path)
            return data
        else:
            raise Exception(f"해당 url을 불러오는 데에 실패하였습니다.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


if __name__ == "__main__":
    data_seoul_endpoint = "/json/SeoulAdminMesure/1/5/"

    portal_params = {'KEY': Config.data_portal.service_key, 'TYPE': 'json', 'SERVICE': 'SeoulAdminMesure', 'START_INDEX': '0', 'END_INDEX': '10'}

    data_seoul = get_data_seoul(data_seoul_endpoint, portal_params)

    if data_seoul:
        print(data_seoul)
        print("\n")
    else:
        print("get_data_seoul failed\n")
