import json
import os.path
import tempfile
from datetime import datetime
from typing import Dict, Tuple, List, Any
from urllib.parse import urlencode

import requests

from load.load_data import minio_load

origin = 'portal'


def get_data_portal(minio_url: str,
                    minio_access_key: str,
                    minio_secret_key: str,
                    data_portal_base_url: str,
                    endpoint: str,
                    data_portal_params: dict = None)\
        -> Tuple[str, List[Dict[str, Any]]]:
    """
    공공 데이터 포털 API에서 데이터를 가져옵니다.

    :param data_portal_base_url:
    :param endpoint: 수집할 url endpoint
    :param data_portal_params: 추가적인 파라미터 (딕셔너리 형태)
    :return: JSON 응답 데이터

    주의! json만 가능 -> 추후 xml 추가 예정
    secretkey는 parameter 에 넣어주어야 함
    """
    params = urlencode(data_portal_params)
    url = f"{data_portal_base_url}{endpoint}"
    data = {}
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            response = requests.get(url, params=params)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        data_id = endpoint.lstrip("/").replace("/", "_")
        tmp_file_path = os.path.join(tmpdir, data_id)
        data["url"] = f"{url}?{params}"
        data["data_id"] = data_id
        data["origin"] = origin
        data["date"] = datetime.now().date()

        if response.status_code == 200:
            try:
                with open(tmp_file_path, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=4)
            except EOFError as e:
                print(f"파일 저장 실패: {e}")

            data["file_path"] = minio_load(minio_url,
                                           minio_access_key,
                                           minio_secret_key,
                                           "dataportal",
                                           tmp_file_path)
            return "portal", [data]
        else:
            print(f"해당 url을 불러오는 데에 실패하였습니다.")
    return "portal", []


if __name__ == "__main__":
    # http://apis.data.go.kr 을 제외한 나머지
    data_portal_endpoint = "/1320000/PlanCrossRoadInfoService/getPlanCRHDInfo"  # API 엔드포인트

    # potral_params = {'serviceKey': Config.data_portal.service_key, 'pageNo': '1', 'numOfRows': '10', 'type': 'json', 'srchCTId': 'L01', 'srchCRNm': '시청'}
    potral_params = {}

    data_portal_api = get_data_portal(data_portal_endpoint, potral_params)
    if data_portal_api:
        print(data_portal_api)
        print("\n")
    else:
        print("get_data_portal failed\n")
