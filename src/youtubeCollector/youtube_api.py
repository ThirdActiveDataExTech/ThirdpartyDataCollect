import os
import io

import googleapiclient.discovery
import googleapiclient.errors
import config.conf as config

from youtube_transcript_api import YouTubeTranscriptApi

import mkFilePath

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def get_search_res(search_term):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=config.UserIdentifyCode.api_key)

    request = youtube.search().list(
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


def get_video_ids(search_term):
    video_ids = [item["id"]["videoId"] for item in get_search_res(search_term)["items"]]
    return video_ids


def get_video_script():
    video_ids = get_video_ids("sbs 드라마")

    for video_id in video_ids:
        fh = io.FileIO("YOUR_FILE", "wb")

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


if __name__ == "__main__":
    get_video_ids("sbs 드라마")
    # get_video_script()
