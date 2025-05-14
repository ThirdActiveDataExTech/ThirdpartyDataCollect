import urllib.parse
import urllib.request
from collections import namedtuple

from common import common_def
from load.load_data import minio_load

origin = 'blog'


# naver의 검색 api를 이용한 크롤링 함수
# 입력: 검색어/ 출력: 검색결과 url list
def search_blog_api(search_term, count):
    enc_text = urllib.parse.quote(search_term)
    url = f"https://openapi.naver.com/v1/search/blog?query={enc_text}&display={count}"  # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    return common_def.search_api(url)


# 검색 api의 결과에서 data('title', 'blog_url', 'post_date', 'file_path', 'data_id')를 추출하는 함수
# 입력: 검색결과 url list/ 출력: load 할 data
def get_blog_list(search_response):
    blog_list = []
    blog_data = namedtuple('blog', ['post_url', 'title', 'blog_url', 'post_date', 'file_path', 'data_id'])
    for item in search_response:
        post_url = item.get("link")
        data_id = common_def.get_data_id(origin, post_url)
        title = str(item.get("title"))
        blog_url = item.get("bloggerlink")
        post_date = item.get("postdate")
        file_path = minio_load(origin, common_def.get_crawling_file(origin, post_url, str(data_id)))

        data = blog_data(post_url=post_url, title=title, blog_url=blog_url, post_date=post_date, file_path=file_path, data_id=data_id)
        blog_list.append(data)

    return blog_list


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
