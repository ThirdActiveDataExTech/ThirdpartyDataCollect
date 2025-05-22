from typing import Any, Dict, Tuple, List

from openai import OpenAI


# ai가 요약한 영상 내용을 리턴하는 함수
def get_video_summary(scripts: Tuple[str, List[Dict[str, Any]]],
                      openai_api_key: str) -> Tuple[str, List[Dict[str, Any]]]:
    summary_list = []
    client = OpenAI(
        api_key=openai_api_key
    )
    for script in scripts[1]:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", "content": f"{script.get('script')}"}
            ]
        )

        summary_list.append({"id": script.get('id'), "summary": completion.choices[0].message.content})

    return "youtube", summary_list


if __name__ == "__main__":
    print(get_video_summary(["cSq6GzcVs9A", "XePxJJ3ssOQ", "RpA2RO-NmXc", "ObIGMBLNDg8"], 'youtube'))
    # print(get_video_summary(, 'youtube'))
    # print(get_video_summary( 'youtube'))
    # print(get_video_summary( 'youtube'))
    # print(get_video_summary("sNNxaAxnQfc", 'youtube'))
