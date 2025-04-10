import googleapiclient.discovery
import googleapiclient.errors
from common.config.user_config import Config

ENUM = 4
YOUTUBE = googleapiclient.discovery.build("youtube", "v3", developerKey=Config.youtube_api.key)


# 검색결과 리스트를 반환하는 함수
def get_video_id_list(search_term, max_result):
    id_list = []
    request = YOUTUBE.search().list(
        part="id",
        maxResults=max_result,
        order="viewCount",
        q=search_term,
        regionCode="KR",
        relevanceLanguage="ko",
        type="video"
    )
    response = request.execute()

    for item in response['items']:
        id_list.append(item['id']['videoId'])

    return id_list, ENUM


if __name__ == "__main__":
    print(get_video_id_list("고양이", 3))
