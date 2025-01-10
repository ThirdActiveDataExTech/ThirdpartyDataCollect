import os

import googleapiclient.discovery
import googleapiclient.errors
import yt_dlp

import config.conf as config

from youtube_transcript_api import YouTubeTranscriptApi


def get_video_script(video_id):
    # fh = io.FileIO("YOUR_FILE", "wb")

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['ko'])

    # 번역 기능
    # translated_transcript = transcript.translate('ko')
    script = transcript.fetch()
    print(script)

    sentences = []
    for sentence in script:
        text = sentence['text'].replace('\n', ' ')
        sentences.append(text)

    # fh.write(transcript)
    # download = MediaIoBaseDownload(fh, request)
    # complete = False
    # while not complete:
    #     status, complete = download.next_chunk()
    return sentences


def get_video_url(video_id):
    url = "https://www.youtube.com/watch?v="+video_id
    return url


def get_video_mp3(video_id):
    url = get_video_url(video_id)
    output_dir = os.path.join('./tmp/', 'mp3test', '%(title)s.%(ext)s')
    try:
        ydl_opts = {  # youtube_dl 라이브러리 설정
            'outtmpl': output_dir,
            'format': 'bestaudio/best',  # 최고 품질로 추출
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # 영상을 오디오 파일로 추출
                'preferredcodec': 'mp3',  # 오디오 파일 포맷을 mp3 파일로 설정
                'preferredquality': '192', #오디오 품질 설정 192k
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error occurred: {e}")


class YouTubeApi:
    def __init__(self, search_term):
        self.search_term = search_term
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=config.UserIdentifyCode.api_key)

    def get_video_list(self):
        request = self.youtube.search().list(
            part="snippet",
            maxResults=5,
            order="viewCount",
            q=self.search_term,
            regionCode="KR",
            relevanceLanguage="ko",
            type="video"
        )
        response = request.execute()

        return response

    def get_video_ids(self):
        video_list = self.get_video_list()
        video_ids = [item["id"]["videoId"] for item in video_list["items"]]
        return video_ids

    def get_reply(self):
        request = self.youtube.commentThreads().list(
            part="snippet,replies",
            maxResults=5,
            videoId='QbLhA5v4GfU'
        )
        response = request.execute()
        return response

    def get_video_inspect(self, video_id):
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        return response

    def get_video_thumbnail(self, video_id):
        video_inspect = self.get_video_inspect(video_id)
        thumbnail = [item["snippet"]["thumbnails"] for item in video_inspect["items"]]
        return thumbnail

    def get_video_viewcount(self, video_id):
        video_inspect = self.get_video_inspect(video_id)
        viewcount = [item["statistics"]["viewCount"] for item in video_inspect["items"]]
        return viewcount

    def get_video_like_count(self, video_id):
        video_inspect = self.get_video_inspect(video_id)
        like_count = [item["statistics"]["likeCount"] for item in video_inspect["items"]]
        return like_count

    def get_video_tag(self, video_id):
        video_inspect = self.get_video_inspect(video_id)
        tag = [item["snippet"]["tags"] for item in video_inspect["items"]]
        return tag


if __name__ == "__main__":
    youtube_api = YouTubeApi("sbs 드라마")
    test_video_id = "JQ2aoqwHmgE"
    # print(youtube_api.get_video_list())
    # print(youtube_api.get_video_ids())
    #
    # print(get_video_script(test_video_id))
    # print(youtube_api.get_reply(test_video_id))
    #
    # print(youtube_api.get_video_inspect(test_video_id))
    #
    # print(youtube_api.get_video_thumbnail(test_video_id))
    # print(youtube_api.get_video_viewcount(test_video_id))
    # print(youtube_api.get_video_like_count(test_video_id))
    # print(youtube_api.get_video_url(test_video_id))
    # print(youtube_api.get_video_tag(test_video_id))
    # print(get_video_url(test_video_id))
    get_video_mp3(test_video_id)
