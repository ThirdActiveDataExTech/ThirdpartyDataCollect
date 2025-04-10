import os
import yt_dlp


# 비디오 mp3를 추출해서 리턴하는 함수
def get_video_mp3(video_id_list, enum):
    is_filelist = True
    file_path_list = []
    for video_id in video_id_list:
        url = "https://www.youtube.com/watch?v=" + video_id
        output_dir = os.path.join('tmp/', 'mp3test', f'{video_id}s.%(ext)s')
        file_path_list.append(output_dir)
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
                ydl.download([url])
        except:
            return None

    return is_filelist, file_path_list, enum


if __name__ == '__main__':
    video_id_list = ['nZODAXlTv4E', 'jANE8lpoj2c', 'TzcfrbYGPY8']
    get_video_mp3(video_id_list, 4)
