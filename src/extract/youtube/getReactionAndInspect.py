import googleapiclient.discovery
import googleapiclient.errors

from src.common.config.user_config import Config


api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=Config.youtube_api.key)


def get_video_inspect(video_id_list, enum):
    is_filelist = False
    inspect_list = []
    title_list = []
    thumbnail_list = []
    viewcount_list = []
    likecount_list = []
    tag_list = []
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

        title_list.append({"id": video_id, "title": title})
        thumbnail_list.append({"id": video_id, "thumbnail": thumbnail})
        viewcount_list.append({"id": video_id, "viewcount": viewcount})
        likecount_list.append({"id": video_id, "likecount": likecount})
        tag_list.append({"id": video_id, "tag": tag})

    inspect_list.append(title_list)
    inspect_list.append(thumbnail_list)
    inspect_list.append(viewcount_list)
    inspect_list.append(likecount_list)
    inspect_list.append(tag_list)

    return is_filelist, enum, ["title", "thumbnail", "viewcount", "likecount", "tag"], inspect_list


if __name__ == '__main__':
    video_ids = ['nZODAXlTv4E', 'jANE8lpoj2c', 'TzcfrbYGPY8']
    print(get_video_inspect(video_ids, api_service_name))
