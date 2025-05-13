from urllib.parse import urlencode
from common.config.user_config import Config
from load.load_data import minio_load
from src.common.common_def import make_file_path

import requests
import json

origin = 'dataportal'


def get_data_portal(endpoint, data_portal_params=None):
    """
    공공 데이터 포털 API에서 데이터를 가져옵니다.

    :param endpoint: 수집할 url endpoint
    :param data_portal_params: 추가적인 파라미터 (딕셔너리 형태)
    :return: JSON 응답 데이터

    주의! json만 가능 -> 추후 xml 추가 예정
    secretkey는 parameter 에 넣어주어야 함
    """
    params = urlencode(data_portal_params)
    url = f"https://{Config.data_portal.base_url}{endpoint}"
    data = {}

    try:
        response = requests.get(url, params=params)
        if endpoint[0] == "/":
            file_id = endpoint.replace("/", "_")[1:]
        else:
            file_id = endpoint.replace("/", "_")
        file_path = make_file_path(origin, file_id)
        data["file_id"] = file_id
        data["bucket"] = "dataportal"

        if response.status_code == 200:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=4)
            except EOFError as e:
                print(f"파일 저장 실패: {e}")

            data["file_path"] = minio_load(origin, file_path)
            return data
        else:
            raise Exception(f"해당 url을 불러오는 데에 실패하였습니다.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


if __name__ == "__main__":
    data_portal_base_url = Config.data_portal.base_url  # 데이터 포털의 기본 URL
    # http://apis.data.go.kr 을 제외한 나머지
    data_portal_endpoint = "/1320000/PlanCrossRoadInfoService/getPlanCRHDInfo"  # API 엔드포인트
    data_portal_service_key = Config.data_portal.service_key

    potral_params = {'serviceKey': Config.data_portal.service_key, 'pageNo': '1', 'numOfRows': '10', 'type': 'json', 'srchCTId': 'L01', 'srchCRNm': '시청'}

    data_portal_api = get_data_portal(data_portal_endpoint, potral_params)
    if data_portal_api:
        print(data_portal_api)
        print("\n")
    else:
        print("get_data_portal failed\n")
