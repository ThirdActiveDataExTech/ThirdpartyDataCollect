from youtube_transcript_api import YouTubeTranscriptApi


# 비디오 자막을 리턴하는 함수
def get_video_script(video_id_list):
    # fh = io.FileIO("YOUR_FILE", "wb")
    transcripts = []
    for video_id in video_id_list:
        try:
            transcript_list = YouTubeTranscriptApi().list(video_id)
            transcript = transcript_list.find_transcript(['ko'])

            # 번역 기능
            # translated_transcript = transcript.translate('ko')
            script = transcript.fetch()
            # print(script)

            sentences = []
            for sentence in script:
                text = sentence.text.replace('\n', ' ')
                sentences.append(text)

            transcripts.append({"id": video_id, "script": sentences})
            # fh.write(transcript)
            # download = MediaIoBaseDownload(fh, request)
            # complete = False
            # while not complete:
            #     status, complete = download.next_chunk()
        except Exception as e:
            print(e)
            transcripts.append({"id": video_id, "script": []})
    return transcripts


if __name__ == '__main__':
    print(get_video_script(['QbLhA5v4GfU']))
    print(get_video_script(['oAkNZ1leVys']))
    print(get_video_script(['xvLBfFIYIeI']))
    print(get_video_script(['b-poivwvqw4']))
    print(get_video_script(['cSq6GzcVs9A']))
