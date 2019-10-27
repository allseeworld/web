import re
import urllib
from urllib import request


# def get_html(html):
#     patterns = re.compile('<dd>.*?>([0-9]+?)</i>.*?title="(.*?)".*?<img data-src="(.*?)".*?主演：(.*?)</p>.*?上映时间：(.*?)</p>.*?class="integer">([0-9.]+?)</i><i class="fraction">([0-9])</i></p>.*?</div>', re.S)
#     pat = patterns.findall(html)
#     print('*' * 100)
#     print(pat)
#     for i in pat:
#         print('*' * 100)
#         print(i)


def get_result():
    pass


def main(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/77.0.3865.120 Safari/537.36 '
    }
    req = request.Request(url, headers=headers)
    res = request.urlopen(req)
    # print(res.read().decode())
    html = res.read().decode()
    print(html)
    return html


if __name__ == '__main__':
    url = 'https://maoyan.com/board/6'
    # for i in [7]:
    #     html = main(url + f'{i}')
    #     get_html(html)
    # for i in range(0,10):
    html = main(url)
        # get_html(html)
