from collections import namedtuple

import googleapiclient.discovery
import googleapiclient.errors

from src.common.config.user_config import Config


youtube = googleapiclient.discovery.build(
    "youtube", "v3", developerKey=Config.youtube_api.key)


def get_video_inspect(video_id_list, enum):
    inspect_list = []
    inspect_data = namedtuple('youtube', ['title', 'thumbnail', 'viewcount', 'likecount', 'tag', 'data_id'])

    for video_id in video_id_list:
        request = youtube.videos().list(
            part="snippet, statistics",
            id=video_id
        )
        response = request.execute()
        item = response["items"][0]
        snippet = item["snippet"]
        statistics = item["statistics"]

        title = snippet["title"]
        thumbnail = snippet["thumbnails"]["default"]["url"]
        viewcount = statistics["viewCount"]
        likecount = statistics["likeCount"]
        tag = snippet.get('tags', [])

        data = inspect_data(title=title, thumbnail=thumbnail, viewcount=viewcount, likecount=likecount, tag=tag,
                            data_id=video_id)
        inspect_list.append(data)

    return inspect_list


if __name__ == '__main__':
    video_ids = ['nZODAXlTv4E', 'jANE8lpoj2c', 'TzcfrbYGPY8']
    print(get_video_inspect(video_ids, "youtube"))
