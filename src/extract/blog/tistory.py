import bs4
from bs4 import BeautifulSoup
from common import util


def parse(page: BeautifulSoup):

    # tag, title = util.remove_tag(page.select_one("header h2")) # 페이지에 따라 h1, h2

    body = page.select_one("article").find_all(
        ['blockquote', 'pre', 'br', 'p', 'h3']
    )

    body_list = []

    for n, row in enumerate(body):
        row: bs4.element.Tag
        tag, content = util.remove_tag(row)

        if content == '':
            _row = row.find(['img'])
            if _row is not None:
                body_list.append(f"<img src={_row.get('src')}>")
        else:
            if tag in ['p', 'h3']:
                body_list.append(f'<{tag}>{content}</{tag}>')
            elif tag in ['blockquote', 'pre']:
                # TODO: 다양한 태그 처리
                pass
                # tag, content = util.remove_tag(row, is_all=False)
                # body_list.append(content)
            else:
                body_list.append(row)

    return '', body_list


def test(url):
    from common import util
    page = util.read_web(url)

    # page.find('h2')

    title, body = parse(page)
    #
    for row in body:
        # print(type(row))
        print(row)


if __name__ == '__main__':
    test_url = 'https://carrotweb.tistory.com/255'
    # test_url = 'https://ksh-coding.tistory.com/m/125'
    test(test_url)
