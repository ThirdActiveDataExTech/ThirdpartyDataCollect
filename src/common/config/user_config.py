class _MinioServer:
    access_key = ""
    secret_key = ""
    url = "0.0.0.0:9004"


class _PostgresServer:
    host = "0.0.0.0"
    user = ""
    password = ""
    port = 5432
    database = ""


class _DataPortal:
    base_url = ""
    endpoint = ""
    service_key = ""


class _SeoulPortal:
    base_url = "openapi.seoul.go.kr:8088/"
    endpoint = ""
    service_key = ""


class _NaverAPIIdentify:
    client_id = ""
    client_secret = ""


class _YoutubeAPIIdentifyCode:
    key = ""


class _OpenaiIdentifyCode:
    key = ""


class Config:
    minio_server = _MinioServer()
    postgres_server = _PostgresServer()
    data_portal = _DataPortal()
    seoul_portal = _SeoulPortal()
    naver_api = _NaverAPIIdentify()
    youtube_api = _YoutubeAPIIdentifyCode()
    openai_api = _OpenaiIdentifyCode()