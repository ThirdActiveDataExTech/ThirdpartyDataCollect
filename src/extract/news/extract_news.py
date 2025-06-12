import os
import tempfile
import urllib.parse
import urllib.request
from typing import Tuple, List, Dict, Any

from common import common_def

origin = "news"


# naver의 검색 api를 이용한 크롤링 함수
def search_news_api(search_term: str,
                    count: int,
                    client_id: str,
                    client_secret: str
                    ) -> List[Dict[str, Any]]:
    enc_text = urllib.parse.quote(search_term)
    url = f"https://openapi.naver.com/v1/search/news?query={enc_text}&display={count}"  # JSON 결과
    print(url)
    data = common_def.search_api(client_id, client_secret, url)
    return data


# 검색 api의 결과에서 data('title', 'url', 'post_date', 'file_path', 'data_id')를 추출하는 함수
# 입력: 검색결과 url list/ 출력: load 할 data
def get_news_list(search_response: List[Dict[str, Any]],
                  minio_url: str,
                  minio_access_key: str,
                  minio_secret_key: str
                  ) -> Tuple[str, List[Dict[str, Any]]]:
    from load.load_data import minio_load
    news_list = []
    for item in search_response:
        data_id = common_def.get_data_id(origin, item.get("link"))
        title = str(item.get("title"))
        url = item.get("originallink")
        description = item.get("description")
        post_date = item.get("pubDate")
        page = common_def.get_crawling_file(origin, url)
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_file_path = os.path.join(tmpdir, f"{data_id}.txt")
            common_def.write_file_of_web(temp_file_path, page)
        file_path = minio_load(minio_url,
                               minio_access_key,
                               minio_secret_key,
                               origin,
                               temp_file_path)

        news_list.append({
            "title": title,
            "url": url,
            "description": description,
            "post_date": post_date,
            "file_path": file_path,
            "id": data_id
        })
    return "news", news_list


if __name__ == '__main__':
    start_word = '위암'
    api_response = search_news_api(start_word, 3, "", "")
    # print(api_response)
    a = get_news_list(api_response)
    print(a[0].title)
