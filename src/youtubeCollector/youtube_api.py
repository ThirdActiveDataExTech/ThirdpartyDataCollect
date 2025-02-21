import os

import googleapiclient.discovery
import googleapiclient.errors
import yt_dlp

import config.conf as config

from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI


# Youtube API를 이용해 특정 검색어에 대한 결과 리스트와 각 영상에 대한 데이터를 크롤링하는 모듈 #


# 비디오 자막을 리턴하는 함수
def get_video_script(video_id):
    # fh = io.FileIO("YOUR_FILE", "wb")
    transcript_list = []

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except:
        return None
    transcript = transcript_list.find_transcript(['ko'])

    # 번역 기능
    # translated_transcript = transcript.translate('ko')
    script = transcript.fetch()
    # print(script)

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


# ai가 요약한 영상 내용을 리턴하는 함수
def get_video_summary(video_id):
    script = get_video_script(video_id)
    client = OpenAI(
        api_key=config.UserIdentifyCode.openai_key
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": f"{script}"}
        ]
    )

    return completion.choices[0].message


# 비디오 url을 리턴하는 함수
def get_video_url(video_id):
    url = "https://www.youtube.com/watch?v=" + video_id
    return url


# 비디오 mp3를 추출해서 리턴하는 함수
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
                'preferredquality': '192',  # 오디오 품질 설정 192k
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

    # 검색결과 리스트를 반환하는 함수
    def get_video_id_list(self):
        video_id_list = []
        request = self.youtube.search().list(
            part="id",
            maxResults=1,
            order="viewCount",
            q=self.search_term,
            regionCode="KR",
            relevanceLanguage="ko",
            type="video"
        )
        response = request.execute()

        for item in response['items']:
            video_id_list.append(item['id']['videoId'])

        return video_id_list

    # 검색 결과 리스트의 각 영상에 대한 상세정보를 반환하는 함수
    def get_video_detail(self):
        video_detail = {}
        video_id_list = self.get_video_id_list()
        for video_id in video_id_list:

            request = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()

            extracted_data = {
                "title": response["items"][0]["snippet"]["title"],
                "thumbnail_url": response["items"][0]["snippet"]["thumbnails"]["default"]["url"],
                "channel_title": response["items"][0]["snippet"]["channelTitle"],
                "tags": response["items"][0]["snippet"]["tags"],
                "view_count": response["items"][0]["statistics"]["viewCount"],
                "like_count": response["items"][0]["statistics"]["likeCount"],
                "video_url": get_video_url(video_id),
                "video_script": get_video_script(video_id),
                "video_summary": get_video_summary(video_id),
                "video_mp3": get_video_mp3(video_id),
                "reply": self.get_reply(video_id)
            }

            video_detail[video_id] = extracted_data
        return video_detail

    # 영상 댓글을 리스트로 반환하는 함수
    def get_reply(self, video_id):
        request = self.youtube.commentThreads().list(
            part="snippet,replies",
            maxResults=5,
            videoId=video_id
        )
        response = request.execute()

        reply_list = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response["items"]]

        return reply_list


if __name__ == "__main__":
    youtube_api = YouTubeApi("뉴스")
    test_video_id = "-PG6rqUTWkg"
    # print(youtube_api.get_video_id_list("sbs 드라마"))
    # print(youtube_api.get_video_detail(youtube_api.get_video_id_list("sbs 드라마")))

    # print(youtube_api.get_reply(test_video_id))

    # print(get_video_url(test_video_id))
    # get_video_mp3(test_video_id)
    # get_video_summary(test_video_id)
    # print(youtube_api.get_reply(test_video_id))

    print(youtube_api.get_video_detail())
