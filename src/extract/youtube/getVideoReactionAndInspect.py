from typing import List, Any, Dict, Tuple

import googleapiclient.discovery
import googleapiclient.errors


def get_video_inspect(videos: Tuple[str, List[Dict[str, Any]]],
                      youtube_api_key: str) -> Tuple[str, List[Dict[str, Any]]]:
    inspect_list = []

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=youtube_api_key)
    for video in videos[1]:
        video_id = video["id"]
        request = youtube.videos().list(
            part="snippet, statistics",
            id=video_id
        )
        response = request.execute()
        item = response["items"][0]
        snippet = item["snippet"]
        statistics = item["statistics"]

        inspect_list.append({
            "id": video_id,
            "title": snippet["title"],
            "thumbnail": snippet["thumbnails"]["default"]["url"],
            "viewcount": statistics["viewCount"],
            "likecount": statistics["likeCount"],
            "tag": snippet.get('tags', []),
        })

    return "youtube", inspect_list


if __name__ == '__main__':
    video_ids = ['nZODAXlTv4E', 'jANE8lpoj2c', 'TzcfrbYGPY8']
    print(get_video_inspect(video_ids, "youtube"))
