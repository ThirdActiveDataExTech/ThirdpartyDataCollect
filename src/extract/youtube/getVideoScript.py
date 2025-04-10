from youtube_transcript_api import YouTubeTranscriptApi


# 비디오 자막을 리턴하는 함수
def get_video_script(video_id, enum):
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
    return sentences, enum
