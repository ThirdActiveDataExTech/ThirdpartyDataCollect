import os
import tempfile
import urllib.parse
import urllib.request
from typing import Tuple, List, Dict, Any

from common import common_def
from load.load_data import minio_load

origin = 'blog'


# naver의 검색 api를 이용한 크롤링 함수
# 입력: 검색어/ 출력: 검색결과 url list
def search_blog_api(search_term: str,
                    count: int,
                    client_id: str,
                    client_secret: str
                    ) -> List[Dict[str, Any]]:
    enc_text = urllib.parse.quote(search_term)
    url = f"https://openapi.naver.com/v1/search/blog?query={enc_text}&display={count}"  # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    data = common_def.search_api(client_id, client_secret, url)
    return data


# 검색 api의 결과에서 data('title', 'blog_url', 'post_date', 'file_path', 'data_id')를 추출하는 함수
# 입력: 검색결과 url list/ 출력: load 할 data
def get_blog_list(search_response: List[Dict[str, Any]],
                  minio_url: str,
                  minio_access_key: str,
                  minio_secret_key: str
                  ) -> Tuple[str, List[Dict[str, Any]]]:
    blog_list = []
    for item in search_response:
        post_url = item.get("link")
        data_id = common_def.get_data_id(origin, post_url)
        title = str(item.get("title"))
        blog_url = item.get("bloggerlink")
        post_date = item.get("postdate")

        page = common_def.get_crawling_file(origin, post_url)
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_file_path = os.path.join(tmpdir, f"{data_id}.txt")
            common_def.write_file_of_web(temp_file_path, page)
            file_path = minio_load(minio_url,
                                   minio_access_key,
                                   minio_secret_key,
                                   origin,
                                   temp_file_path)

        blog_list.append({
            "post_url": post_url,
            "title": title,
            "blog_url": blog_url,
            "post_date": post_date,
            "file_path": file_path,
            "id": data_id
        })

    return "blog", blog_list


if __name__ == "__main__":
    start_word = '책'
    enum = "blog"
    # api_extract = search_api
    # extractor = ExtractBlogUrl(start_word)
    # crawler = extractor.blog_crawler()
    api_response = search_blog_api(start_word, 10)
    a = get_blog_list(api_response)
    print(a[2].title)
    # get_data_id()
