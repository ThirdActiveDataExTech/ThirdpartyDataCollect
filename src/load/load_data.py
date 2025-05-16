import os
from collections import namedtuple, defaultdict

import psycopg2
from psycopg2 import sql
import urllib3
from minio import Minio

from src.common.config.user_config import Config
from common import log
from minio import S3Error

config = Config()
minio_url = Config.minio_server.url
minio = Minio(
    minio_url,
    access_key=Config.minio_server.access_key,
    secret_key=Config.minio_server.secret_key,
    secure=False,
    http_client=urllib3.PoolManager(
        timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
        retries=urllib3.Retry(
            total=1,
            backoff_factor=0.2,
            status_forcelist=()
        )
    )
)

postgres_conn = psycopg2.connect(
    host=Config.postgres_server.host,
    database=Config.postgres_server.database,
    user=Config.postgres_server.user,
    password=Config.postgres_server.password,
    port=Config.postgres_server.port
)

postgres_cur = postgres_conn.cursor()


def minio_load(origin, path):
    file_name = os.path.basename(path).split("=")[0]
    try:
        minio.fput_object(origin, str(file_name), path)
    except S3Error as e:
        print(f"{file_name} txt 파일 업로드 중 에러가 발생했습니다: {e}")
    print(f"{file_name} - minio 저장 완료")
    return f"{Config.minio_server.url}/browser/{origin}/{file_name}"


def load_common(origin, data):
    if origin in ('blog', 'news'):
        load_multiple_list(data)
    elif origin == 'portal':
        print('load_single')
        # load_single(data)
    elif origin == 'youtube':
        load_list(data)
    else:
        log.error("지원하지 않는 수집 type입니다.")


# dict 형태로 data 전달
def load_single(data_dict):
    if not data_dict:
        return

    data_id = data_dict.get("data_id")
    origin = data_dict.get("origin")

    data = {k: v for k, v in data_dict.items() if k not in ("data_id", "origin")}

    for key, value in data.items():
        query = sql.SQL("INSERT INTO {} (data_id, {}) VALUES (%s, %s)").format(
            sql.Identifier(f"{origin}_{key}"),
            sql.Identifier(key)
        )
        values = [data_id, value]
        postgres_cur.execute(query, values)
    postgres_conn.commit()


# namedtuple list 형태로 data 전달(1개 항목)
def load_list(data_list):
    if not data_list:
        return

    # 필드 이름 추출
    fields = data_list[0]._fields

    placeholders = ', '.join([f'%s'] * len(fields))
    columns = ', '.join(fields)
    table_name = f"{data_list[0].__class__.__name__}"

    # SQL 생성
    sql = (
        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) "
        f"ON CONFLICT (data_id) DO NOTHING"
    )

    # 값 리스트 준비
    values = [tuple(row) for row in data_list]

    # 실행
    postgres_cur.executemany(sql, values)
    postgres_conn.commit()


# namedtuple list 형태로 data 전달(n개 항목)
def load_multiple_list(data_list):
    if not data_list:
        return

    field_data = defaultdict(list)

    value_fields = [field for field in data_list[0]._fields if field != 'data_id']
    origin = data_list[0].__class__.__name__

    for item in data_list:
        for field in value_fields:
            value = getattr(item, field)
            data_id = getattr(item, 'data_id')
            field_data[field].append((data_id, value))  # 튜플 형태로 저장

    for field, values in field_data.items():
        sql = f"INSERT INTO {origin}_{field} (data_id, {field}) VALUES (%s, %s)"
        postgres_cur.executemany(sql, values)

    postgres_conn.commit()


if __name__ == '__main__':
    # dataportal test
    # from src.extract.dataportal.extract_dataportal import get_data_portal
    # data_portal_endpoint = "/1320000/PlanCrossRoadInfoService/getPlanCRHDInfo"  # API 엔드포인트
    # potral_params = {'serviceKey': Config.data_portal.service_key, 'pageNo': '1', 'numOfRows': '10', 'type': 'json', 'srchCTId': 'L01', 'srchCRNm': '시청'}
    # data_list = get_data_portal(data_portal_endpoint, potral_params)
    # load_single(data_list)

    # seoulportal test
    # from src.extract.dataportal.extract_seoulportal import get_data_seoul
    # data_seoul_endpoint = "/json/SeoulAdminMesure/1/5/"
    # portal_params = {'KEY': Config.data_portal.service_key, 'TYPE': 'json', 'SERVICE': 'SeoulAdminMesure', 'START_INDEX': '0', 'END_INDEX': '10'}
    # data_list = get_data_seoul(data_seoul_endpoint, portal_params)
    # load_single(data_list)

    # youtube test
    from extract.youtube.getVideoIdList import get_video_id_list
    # from extract.youtube.getVideoReply import get_reply
    from extract.youtube.getVideoMp3 import get_video_mp3
    # load_list(get_reply(get_video_id_list("SBS 드라마", 5), "youtube", 4, 5))
    load_list(get_video_mp3(get_video_id_list("SBS 드라마", 5)))

    # blog test
    # from src.extract.blog.naver import extract_blog
    # load_multiple_list(extract_blog.get_blog_list(extract_blog.search_blog_api("책", 10)))

    # news test
    # from extract.news import extract_news
    # load_multiple_list(extract_news.get_news_list(extract_news.search_news_api("위암", 3)))
