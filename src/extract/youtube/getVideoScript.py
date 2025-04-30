from youtube_transcript_api import YouTubeTranscriptApi


# 비디오 자막을 리턴하는 함수
def get_video_script(video_id_list, enum):
    is_filelist = False
    # fh = io.FileIO("YOUR_FILE", "wb")
    transcript_list = []
    for video_id in video_id_list:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except Exception as e:
            print(e)
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

        transcript_list.append({"id": video_id, "script": sentences})
        # fh.write(transcript)
        # download = MediaIoBaseDownload(fh, request)
        # complete = False
        # while not complete:
        #     status, complete = download.next_chunk()
    return is_filelist, enum, transcript_list


if __name__ == '__main__':
    print(get_video_script(['QbLhA5v4GfU'], 'youtube'))
    print(get_video_script(['oAkNZ1leVys'], 'youtube'))
    print(get_video_script(['xvLBfFIYIeI'], 'youtube'))
    print(get_video_script(['b-poivwvqw4'], 'youtube'))
    print(get_video_script(['cSq6GzcVs9A'], 'youtube'))
