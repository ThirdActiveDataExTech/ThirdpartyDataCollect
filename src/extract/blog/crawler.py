import os
import os.path
import os.path
import re
import sqlite3
import gzip

from . import search
from common import config
from common import util, error
from common.log import log

'''
 bs4 page 인자에서 통 html, 텍스트 파일을 추출해서 저장하는 기능
'''


class Crawler:
    # 기본 path
    # db_path = config.DB_PATH
    base_path = config.BASE_PATH

    platform, blogId, postId = '', '', ''
    is_html_save, is_text_save = False, False

    def data_save(self, content, content_type):
        file_save_path = os.path.join('data', self.platform, content_type, self.blogId) # /data/naver/html/user-1/123.html
        save_dir = os.path.join(self.base_path, file_save_path)

        try:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            filepath = os.path.join(save_dir, f'{self.postId}.{content_type}')
            with gzip.open(filepath + '.gz', 'wt', encoding='utf-8') as file:
                file.write(content)

            if content_type == 'html':
                self.is_html_save = True
            elif content_type == 'txt':
                self.is_text_save = True

        except IOError as e:
            log.error("Error saving text to file:", e)

    def record_result(self):

        conn = sqlite3.connect(config.META_DB_PATH)
        cur = conn.cursor()
        cur.execute('''
        insert into metadb values(?,?,?,?,?)
        ''', (self.platform, self.blogId, self.postId, self.is_html_save, self.is_text_save,))
        conn.commit()

    def url_parsing(self, url):

        # blog
        tistory_pattern = r"https://([^\.]+)\.tistory\.com/(?:m/)?(\d+)"
        naver_pattern = r"https://m\.blog\.naver\.com/([^/]+)/(\d+)"

        # news
        dailian_pattern = r"https?://(?:www\.)?dailian\.co\.kr/news/view/(\d+)/"

        match_tistory = re.match(tistory_pattern, url)
        match_naver = re.match(naver_pattern, url)
        match_dailian = re.match(dailian_pattern, url)

        if match_tistory:
            self.platform = 'tistory'
            self.blogId = match_tistory.group(1)
            self.postId = match_tistory.group(2)
        elif match_naver:
            self.platform = 'naver'
            self.blogId = match_naver.group(1)
            self.postId = match_naver.group(2)
        elif match_dailian:
            self.platform = 'news'
            self.blogId = 'dailian'
            self.postId = match_dailian.group(1)
        else:
            log.info("URL 형식이 맞지 않습니다.")
            self.platform = 'test-platform'
            self.blogId = 'test-blogId'
            self.postId = 'test-postId'
            return False

        return True

    def crawler(self, url):
        log.info(f'Start to crawl URL: {url}')

        # URL 유효성 체크
        try:
            util.status_check(url)
        except error.WebRequestsError:
            raise

        if self.url_parsing(url):
            page = util.read_web(url)

            # 1. html 데이터 수집
            html_data = str(page)

            # 2. text 데이터 수집
            text_data = page.get_text()

            self.data_save(html_data, 'html')
            self.data_save(text_data, 'txt')
            self.record_result()

            # 해당 web 에 있는 모든 url 을 [수집 대기 URL queue] 에 전송
            # current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            search.publish_embedded_links(url, self.platform)
            log.info('publish_embedded_links done')



if __name__ == "__main__":
    # test_url = 'https://covenant.tistory.com/247'
    test_url = 'https://www.dailian.co.kr/news/view/1359210/'
    crawler = Crawler()
    crawler.crawler(test_url)