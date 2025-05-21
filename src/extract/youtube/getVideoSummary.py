from openai import OpenAI

from getVideoScript import get_video_script


# ai가 요약한 영상 내용을 리턴하는 함수
def get_video_summary(video_id_list, enum, openai_api_key):
    is_filelist = False
    summary_list = []
    for video_id in video_id_list:
        script, enum = get_video_script([video_id], enum)
        client = OpenAI(
            api_key=openai_api_key
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": f"{script}"}
            ]
        )

        summary_list.append({"id": video_id, "summary": completion.choices[0].message})

    return is_filelist, enum, summary_list


if __name__ == "__main__":
    print(get_video_summary(["cSq6GzcVs9A", "XePxJJ3ssOQ", "RpA2RO-NmXc", "ObIGMBLNDg8"], 'youtube'))
    # print(get_video_summary(, 'youtube'))
    # print(get_video_summary( 'youtube'))
    # print(get_video_summary( 'youtube'))
    # print(get_video_summary("sNNxaAxnQfc", 'youtube'))
