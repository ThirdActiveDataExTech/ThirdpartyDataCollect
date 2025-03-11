import re


# blog data_id 추출 함수
def get_data_id(enum, url):
    if enum == 0:
        # blog url은 https://blog.naver.com/ms_hs-93/223780771002" 형식
        match = re.search(r"blog.naver.com/([a-zA-Z0-9_-]+)/([0-9]+)", url)
        if match:
            return match.group(1) + match.group(2)
        return ""
    elif enum == 1:
        # Youtube url은 "https://www.youtube.com/watch?v=A3DtaMoTBbA&t=2304s" 형식
        match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
        if match:
            return match.group(1)
        return ""
    else:
        return ""