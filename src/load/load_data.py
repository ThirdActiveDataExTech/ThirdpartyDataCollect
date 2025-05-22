import json
import os
from collections import defaultdict
from typing import Any, Dict, List, Tuple

import psycopg2
import urllib3
from minio import Minio
from minio import S3Error
from psycopg2 import sql

from common import log


def get_postgres_connect(host, port, user, password, database):
    return psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
    )


def minio_load(minio_url, minio_access_key, minio_secret_key, origin, path):
    minio = Minio(
        minio_url,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
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
    file_name = os.path.basename(path).split("=")[0]
    try:
        minio.fput_object(origin, str(file_name), path)
    except S3Error as e:
        print(f"{file_name} txt 파일 업로드 중 에러가 발생했습니다: {e}")
    print(f"{file_name} - minio 저장 완료")
    return f"{minio_url}/browser/{origin}/{file_name}"


def load_common(postgres_host, postgres_port, postgres_user, postgres_password, postgres_database, origin, data):
    if origin in ('blog', 'news'):
        load_multiple_list(postgres_host, postgres_port, postgres_user, postgres_password, postgres_database, data)
    elif origin == 'portal':
        print('load_single')
        # load_single(data)
    elif origin == 'youtube':
        load_list(postgres_host, postgres_port, postgres_user, postgres_password, postgres_database, data)
    else:
        log.error("지원하지 않는 수집 type입니다.")


# dict 형태로 data 전달
def load_single(postgres_host, postgres_port, postgres_user, postgres_password, postgres_database, data_dict):
    if not data_dict:
        return

    data_id = data_dict.get("data_id")
    origin = data_dict.get("origin")

    data = {k: v for k, v in data_dict.items() if k not in ("data_id", "origin")}

    postgres_conn = get_postgres_connect(postgres_host, postgres_port, postgres_user, postgres_password,
                                         postgres_database)
    postgres_cur = postgres_conn.cursor()
    for key, value in data.items():
        query = sql.SQL("INSERT INTO {} (data_id, {}) VALUES (%s, %s)").format(
            sql.Identifier(f"{origin}_{key}"),
            sql.Identifier(key)
        )
        values = [data_id, value]
        postgres_cur.execute(query, values)
    postgres_conn.commit()


# namedtuple list 형태로 data 전달(1개 항목)
def load_list(postgres_host, postgres_port, postgres_user, postgres_password, postgres_database, data_list):
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
    postgres_conn = get_postgres_connect(postgres_host, postgres_port, postgres_user, postgres_password,
                                         postgres_database)
    postgres_cur = postgres_conn.cursor()
    postgres_cur.executemany(sql, values)
    postgres_conn.commit()


# namedtuple list 형태로 data 전달(n개 항목)
def load_multiple_list(postgres_host, postgres_port, postgres_user, postgres_password, postgres_database, data_list):
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

    postgres_conn = get_postgres_connect(postgres_host, postgres_port, postgres_user, postgres_password,
                                         postgres_database)
    postgres_cur = postgres_conn.cursor()
    for field, values in field_data.items():
        sql = f"INSERT INTO {origin}_{field} (data_id, {field}) VALUES (%s, %s)"
        postgres_cur.executemany(sql, values)

    postgres_conn.commit()


def load(*data: Tuple[str, List[Dict[str, Any]]],
         postgres_host: str,
         postgres_port: int,
         postgres_user: str,
         postgres_password: str,
         postgres_database: str) -> Dict[str, int]:
    if not data:
        return {}
    postgres_conn = get_postgres_connect(postgres_host, postgres_port, postgres_user, postgres_password,
                                         postgres_database)
    postgres_cur = postgres_conn.cursor()
    result = {}
    for d in data:
        origin_, data_list = d
        id_key = "id"
        # 필드별로 insert 대상 그룹화
        batched = defaultdict(list)
        for row in data_list:
            data_id = row[id_key]
            for field, value in row.items():
                if field == id_key:
                    continue
                if isinstance(value, list) or isinstance(value, dict):
                    batched[field].append((data_id, json.dumps(value)))
                else:
                    batched[field].append((data_id, value))

        for field, values in batched.items():
            table_name = f"{origin_}_{field}"
            sql = (f"INSERT INTO {table_name} (data_id, {field}) VALUES (%s, %s)"
                   f"ON CONFLICT (data_id) DO NOTHING")
            try:
                postgres_cur.executemany(sql, values)
            except psycopg2.Error as e:
                print(e)
                continue
            result[table_name] = postgres_cur.rowcount

    postgres_conn.commit()
    return result


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
