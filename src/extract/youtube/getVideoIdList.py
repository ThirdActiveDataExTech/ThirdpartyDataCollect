import googleapiclient.discovery
import googleapiclient.errors
from src.common.config.user_config import Config

ENUM = 'youtube'
YOUTUBE = googleapiclient.discovery.build("youtube", "v3", developerKey=Config.youtube_api.key)


# 검색결과 리스트를 반환하는 함수
# max_result : 반환 결과값 개수 지정
def get_video_id_list(search_term, count):
    id_list = []
    request = YOUTUBE.search().list(
        part="id",
        maxResults=count,
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
    id_list, enum = get_video_id_list("SBS 드라마", 5)
    print(id_list)
    # print(get_reply(id_list, enum))
    # print(get_video_mp3(id_list, enum))
    # print(get_video_script(id_list, enum))
    # print(get_video_url(id_list, enum))

