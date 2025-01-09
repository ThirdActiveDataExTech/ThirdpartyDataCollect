import os
import io

import googleapiclient.discovery
import googleapiclient.errors
import config.conf as config

from youtube_transcript_api import YouTubeTranscriptApi

import mkFilePath

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


class YouTubeApi:
    def __init__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=config.UserIdentifyCode.api_key)

    def get_search_res(self, search_term):
        request = self.youtube.search().list(
            part="snippet",
            maxResults=1,
            order="viewCount",
            q=search_term,
            regionCode="KR",
            relevanceLanguage="ko",
            type="video"
        )
        response = request.execute()

        return response

    def get_video_ids(self, search_term):
        video_list = self.get_search_res(search_term)
        video_ids = [item["id"]["videoId"] for item in video_list["items"]]
        return video_ids

    def get_video_script(self):
        video_ids = self.get_video_ids("sbs 드라마")

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

    def get_reply(self, search_term):
        for video_id in self.get_video_ids(search_term):
            request = self.youtube.commentThreads().list(
                part="snippet,replies",
                maxResults=5,
                videoId=video_id
            )
            response = request.execute()

            print(response)


if __name__ == "__main__":
    youtube_api = YouTubeApi()
    print(youtube_api.get_video_ids("sbs 드라마"))
    # youtube_api.get_video_script()
    # youtube_api.get_reply()
