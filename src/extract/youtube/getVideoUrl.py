# 비디오 url을 리턴하는 함수
def get_video_url(video_id_list, enum):
    is_filelist = False
    url_list = []
    for video_id in video_id_list:
        url = "https://www.youtube.com/watch?v=" + video_id
        url_list.append({"id": video_id, "url": url})
    return is_filelist, enum, url_list
