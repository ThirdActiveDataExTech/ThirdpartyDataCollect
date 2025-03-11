# ThirdpartyDataCollect

pip install --upgrade google-api-python-client
pip install --upgrade google-auth-oauthlib google-auth-httplib2
pip install youtube_transcript_api
pip3 install yt-dlp
pip install openai

# Web Crawler
블로그 데이터 수집을 위한 크롤러


## 테스트용 rabbitmq 정보

```shell
docker run -d --name rabbitmq \
    -p 5672:5672 -p 8087:15672 \
    -e RABBITMQ_DEFAULT_USER=mobigen \
    -e RABBITMQ_DEFAULT_PASS=ahqlwps12#$ \
    rabbitmq:management
```


# docker run 실행
```shell
docker run -d \
    -e QUEUE_HOST=localhost \
    -e QUEUE_PORT=5672 \
    -e QUEUE_VHOST=test \
    -e QUEUE_USER=mobigen \
    -e QUEUE_PASS=ahqlwps12#$ \
    -e BASE_PATH=/crawler \
    -e DB_PATH=/crawler/test.db \
    -v /Users/hyobins/workspace/crawler:/crawler \
    --name crawler_container \
    crawler:v0.0.0.1
```