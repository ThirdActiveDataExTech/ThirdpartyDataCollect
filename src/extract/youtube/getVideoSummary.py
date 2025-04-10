from openai import OpenAI

from getVideoScript import get_video_script
from common.config.user_config import Config


# ai가 요약한 영상 내용을 리턴하는 함수
def get_video_summary(video_id, enum):
    script = get_video_script(video_id)
    client = OpenAI(
        api_key=Config.openai_api.key
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": f"{script}"}
        ]
    )

    return completion.choices[0].message, enum
