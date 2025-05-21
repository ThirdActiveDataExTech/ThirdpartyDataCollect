import urllib.parse
import urllib.request
from collections import namedtuple

from common import common_def

origin = "news"


# naver의 검색 api를 이용한 크롤링 함수
def search_news_api(search_term, count, client_id, client_secret):
    enc_text = urllib.parse.quote(search_term)
    url = f"https://openapi.naver.com/v1/search/news?query={enc_text}&display={count}"  # JSON 결과
    print(url)
    return common_def.search_api(client_id, client_secret, url)


# 검색 api의 결과에서 data('title', 'url', 'post_date', 'file_path', 'data_id')를 추출하는 함수
# 입력: 검색결과 url list/ 출력: load 할 data
def get_news_list(search_response, minio_url, minio_access_key, minio_secret_key):
    from load.load_data import minio_load
    news_list = []
    news_data = namedtuple('news', ['url', 'title', 'description', 'post_date', 'file_path', 'data_id'])
    for item in search_response:
        data_id = common_def.get_data_id(origin, item.get("link"))
        title = str(item.get("title"))
        url = item.get("originallink")
        description = item.get("description")
        post_date = item.get("pubDate")
        file_path = minio_load(minio_url, minio_access_key, minio_secret_key, origin,
                               common_def.get_crawling_file(origin, url, f"{str(data_id)}.txt"))

        data = news_data(title=title, url=url, description=description, post_date=post_date, file_path=file_path,
                         data_id=data_id)
        news_list.append(data)
    return news_list


if __name__ == '__main__':
    start_word = '위암'
    api_response = search_news_api(start_word, 3, "", "")
    # print(api_response)
    a = get_news_list(api_response)
    print(a[0].title)
