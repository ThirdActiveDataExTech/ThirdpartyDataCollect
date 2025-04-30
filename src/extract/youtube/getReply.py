import googleapiclient.discovery
import googleapiclient.errors
from src.common.config.user_config import Config

YOUTUBE = googleapiclient.discovery.build("youtube", "v3", developerKey=Config.youtube_api.key)


# 영상 댓글을 리스트로 반환하는 함수
def get_reply(video_id_list, enum, table, number):
    is_filelist = False
    reply_list = []
    for video_id in video_id_list:
        request = YOUTUBE.commentThreads().list(
            part="snippet,replies",
            maxResults=number,
            videoId=video_id
        )
        response = request.execute()

        reply = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response["items"]]
        reply_list.append({"id": video_id, "reply": reply})
    return is_filelist, enum, table, reply_list


if __name__ == '__main__':
    print(get_reply("nZODAXlTv4E", "youtube", 4, 5))
