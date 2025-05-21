import os
import tempfile
from collections import namedtuple

import yt_dlp

from load.load_data import minio_load


# 비디오 mp3를 추출해서 리턴하는 함수
def get_video_mp3(video_id_list, minio_url, minio_access_key, minio_secret_key):
    origin = f"youtube_mp3_path"
    mp3_data = namedtuple(origin, ['data_id', 'mp3_path'])
    file_path_list = []

    # 컨텍스트 매니저 방식
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"임시 디렉토리 생성됨: {temp_dir}")
        # 디렉토리 내 작업 가능
        for video_id in video_id_list:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            output_dir = os.path.join(temp_dir, str(video_id))
            ydl_opts = {  # youtube_dl 라이브러리 설정
                'outtmpl': output_dir,
                'format': 'bestaudio/best',  # 최고 품질로 추출
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # 영상을 오디오 파일로 추출
                    'preferredcodec': 'mp3',  # 오디오 파일 포맷을 mp3 파일로 설정
                    'preferredquality': '192',  # 오디오 품질 설정 192k
                }],
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                print(f"{video_id} - mp3 다운로드 완료")
            except Exception as e:
                print(f"{video_id} - mp3 download error: {e}")
                return None

            url = minio_load(minio_url, minio_access_key, minio_secret_key, "youtube", f"{output_dir}.mp3")
            file_path_list.append(mp3_data(data_id=video_id, mp3_path=url))

    return file_path_list


if __name__ == '__main__':
    video_ids = ['nZODAXlTv4E', 'jANE8lpoj2c', 'TzcfrbYGPY8']
    get_video_mp3(video_ids, 'youtube')
