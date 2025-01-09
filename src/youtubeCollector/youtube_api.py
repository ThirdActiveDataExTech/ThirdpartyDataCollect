import os

import googleapiclient.discovery
import googleapiclient.errors
import config.conf as config
import google_auth_oauthlib.flow

from youtube_transcript_api import YouTubeTranscriptApi

import mkFilePath

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


class YouTubeApi:
    def __init__(self, search_term):
        self.search_term = search_term
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=config.UserIdentifyCode.api_key)
        self.client_secrets_file = config.UserIdentifyCode.secrets_user_identify

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

    def get_video_script(self):
        video_ids = self.get_video_ids()

        for video_id in video_ids:
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

    def get_reply(self):
        for video_id in self.get_video_ids():
            print(video_id)
            request = self.youtube.commentThreads().list(
                part="snippet,replies",
                maxResults=5,
                videoId='QbLhA5v4GfU'
            )
            response = request.execute()

            print(response)

    def get_video_inspect(self):
        for video_id in self.get_video_ids():
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, scopes)
            credentials = flow.run_local_server()
            youtube = googleapiclient.discovery.build(
                self.api_service_name, self.api_version, credentials=credentials)

            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            print(response)

    def get_video_thumbnail(self):
        video_list = self.get_video_list()
        thumbnail = [item["snippet"]["thumbnails"] for item in video_list["items"]]
        print(thumbnail)


if __name__ == "__main__":
    youtube_api = YouTubeApi("sbs 드라마")
    # print(youtube_api.get_video_ids())
    # print(youtube_api.get_video_list())
    # youtube_api.get_video_script()
    # youtube_api.get_reply()

    youtube_api.get_video_thumbnail()
    # youtube_api.get_video_inspect()
