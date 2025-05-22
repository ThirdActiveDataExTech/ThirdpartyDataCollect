from typing import List, Tuple, Dict, Any

import googleapiclient.discovery
import googleapiclient.errors


# 영상 댓글을 리스트로 반환하는 함수
def get_reply(videos: Tuple[str, List[Dict[str, Any]]],
              count: int,
              youtube_api_key: str) -> Tuple[str, List[Dict[str, Any]]]:
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=youtube_api_key)
    reply_list = []
    for video in videos[1]:
        video_id = video["id"]
        try:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                maxResults=count,
                videoId=video_id
            )
            response = request.execute()

            reply = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response["items"]]
            reply_list.append({
                "id": video_id,
                "reply": reply,
            })
        except googleapiclient.errors.HttpError as error:
            print(error)
            reply_list.append({"id": video_id, "reply": []})
    return "youtube", reply_list


if __name__ == '__main__':
    print(get_reply("nZODAXlTv4E", "youtube", 4, 5))
