from typing import List, Dict, Tuple, Any

import googleapiclient.discovery
import googleapiclient.errors


# 검색결과 리스트를 반환하는 함수
# max_result : 반환 결과값 개수 지정
def get_video_id_list(search_term: str,
                      count: int,
                      youtube_api_key: str) -> Tuple[str, List[Dict[str, Any]]]:
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=youtube_api_key)
    request = youtube.search().list(
        part="id",
        maxResults=count,
        order="viewCount",
        q=search_term,
        regionCode="KR",
        relevanceLanguage="ko",
        type="video"
    )
    response = request.execute()

    id_list = []
    for item in response['items']:
        video_id = item['id']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"
        id_list.append({
            "id": video_id,
            "url": url,
        })

    return "youtube", id_list


if __name__ == "__main__":
    id_list, origin = get_video_id_list("SBS 드라마", 5)
    print(id_list)
    # print(get_reply(id_list, origin))
    # print(get_video_mp3(id_list, origin))
    # print(get_video_script(id_list, origin))
    # print(get_video_url(id_list, origin))
