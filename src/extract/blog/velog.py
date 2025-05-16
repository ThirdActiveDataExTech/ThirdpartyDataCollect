from bs4 import BeautifulSoup
from common import util


def parse(page: BeautifulSoup):
    title = page.find("h1").text
    print(title)

    body = page.select_one(".sc-eGRUor.gdnhbG.atom-one").find_all('p')

    body_list = []
    for n, row in enumerate(body):
        row = util.remove_tag(row)
        if row == '':
            continue
        body_list.append(f'<p data-reader-unique-id={n}>{row}</p>')

    return title, body_list


def test():
    from common import util
    # d = util.read_web('https://m.blog.naver.com/qufslagkdl/223391689387')
    page = util.read_web('https://velog.io/@jisu0807/%EC%9B%B9%ED%81%AC%EB%A1%A4%EB%A7%81-BeautifulSoup%EC%97%90%EC%84%9C-find%EC%99%80-select-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0')
    title, body = parse(page)

    for row in body:
        print(row)


if __name__ == '__main__':
    test()