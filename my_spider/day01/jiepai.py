import json
import re
from urllib import request


def deal_html(html):
    print(html)
    patterns = re.compile(r'gallery: JSON.parse\((.*?)\)',re.S)
    pat = patterns.findall(html)

    pat =re.findall(r'"(http:.*?)\"',pat[0][1:-1].replace('\\\\\\u002F','/').replace('\\',''))

    print(set(pat))



def main(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    req = request.Request(url, headers=headers)
    res = request.urlopen(req)
    # print(res.read().decode())
    return res.read().decode()


if __name__ == '__main__':
    url = 'https://www.toutiao.com/a6727436738928574980/#p=1'
    html = main(url)
    deal_html(html)
