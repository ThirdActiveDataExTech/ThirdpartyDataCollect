import os
import tempfile
from typing import Any, Dict, List, Tuple

import imageio_ffmpeg
import yt_dlp

from load.load_data import minio_load


# 비디오 mp3를 추출해서 리턴하는 함수
def get_video_mp3(videos: Tuple[str, List[Dict[str, Any]]],
                  minio_url: str,
                  minio_access_key: str,
                  minio_secret_key: str) -> Tuple[str, List[Dict[str, Any]]]:
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    # 컨텍스트 매니저 방식
    mp3_path_list = []
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"임시 디렉토리 생성됨: {temp_dir}")
        # 디렉토리 내 작업 가능
        for video in videos[1]:
            video_id = video["id"]
            output_dir = os.path.join(temp_dir, video_id)
            try:
                with yt_dlp.YoutubeDL({  # youtube_dl 라이브러리 설정
                    'outtmpl': output_dir,
                    'format': 'bestaudio/best',  # 최고 품질로 추출
                    'ffmpeg_location': ffmpeg_path,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',  # 영상을 오디오 파일로 추출
                        'preferredcodec': 'mp3',  # 오디오 파일 포맷을 mp3 파일로 설정
                        'preferredquality': '192',  # 오디오 품질 설정 192k
                    }],
                }) as ydl:
                    ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
                print(f"✅ {video} - mp3 다운로드 완료")
                mp3_path = minio_load(minio_url,
                                      minio_access_key,
                                      minio_secret_key,
                                      "youtube",
                                      f"{output_dir}.mp3")
                mp3_path_list.append({
                    "id": video_id,
                    "mp3_path": mp3_path,
                })
            except Exception as e:
                print(f"⚠️ {video} - mp3 다운로드 실패: {e}")
                continue

    return "youtube", mp3_path_list


if __name__ == '__main__':
    video_ids = ['nZODAXlTv4E', 'jANE8lpoj2c', 'TzcfrbYGPY8']
    get_video_mp3(video_ids, 'youtube')
