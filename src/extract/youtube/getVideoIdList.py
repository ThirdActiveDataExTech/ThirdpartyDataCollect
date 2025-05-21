from collections import namedtuple

import googleapiclient.discovery
import googleapiclient.errors

from load.load_data import load_list


# 검색결과 리스트를 반환하는 함수
# max_result : 반환 결과값 개수 지정
def get_video_id_list(search_term: str, count: int, youtube_api_key: str,
                      postgres_host, postgres_port, postgres_user, postgres_password, postgres_database):
    YOUTUBE = googleapiclient.discovery.build("youtube", "v3", developerKey=youtube_api_key)
    id_tuple = namedtuple('youtube_url', ['data_id', 'url'])
    load_data_list = []
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
        video_id = item['id']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"
        data = id_tuple(video_id, url)
        load_data_list.append(data)
        id_list.append(video_id)

    try:
        load_list(postgres_host, postgres_port, postgres_user, postgres_password, postgres_database, load_data_list)
    except Exception as e:
        print(f"youtube url 저장 중 에러 발생: {e}")

    return id_list


if __name__ == "__main__":
    id_list, origin = get_video_id_list("SBS 드라마", 5)
    print(id_list)
    # print(get_reply(id_list, origin))
    # print(get_video_mp3(id_list, origin))
    # print(get_video_script(id_list, origin))
    # print(get_video_url(id_list, origin))
