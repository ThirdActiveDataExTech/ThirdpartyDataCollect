from src.common.config.user_config import Config
from src.common.common_def import make_file_path

import requests


def get_data_seoul(endpoint, data_seoul_params=None):
    """
    서울열린데이터포털 API에서 데이터를 가져옵니다.

    :return: JSON 응답 데이터
    """

    url = f"http://{Config.seoul_portal.base_url}{Config.seoul_portal.service_key}{endpoint}"
    # if data_seoul_params:
    #     url = f"{url}?pageNo={data_seoul_params['pageNo']}&numOfRows={data_seoul_params['numOfRows']}"

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
    data_seoul_endpoint = "/xml/publicHygieneBizCleaningProducts/1/5/"

    params = {"pageNo": "1", "numOfRows": "1", "_type": "json", "nm": "강북"}

    data_seoul = get_data_seoul(data_seoul_endpoint, params)

    if data_seoul:
        print(data_seoul)
        print("\n")
    else:
        print("get_data_seoul failed\n")
