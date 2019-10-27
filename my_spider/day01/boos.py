# 1. 爬取的地址整理

# 2.页面分析,页面中没有加载就是(只要页面源码,就可以提取内容)
import re
import urllib.request


def get_html(new_url):
    # 接受需要爬取的地址,返回该地址的源码信息
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/77.0.3865.120 Safari/537.36 ',
        "Cookie": '__zp_stoken__=f84bJ0Vbbe0jMRvLQZfrBr%2Bgfe61qoPG%2FHL21UCfLS7wtSLJ84IMLPqKg3doN6mTDhldHTpGokQp%2B9'
                  '%2BkA%2FM3f8qWLw%3D%3D',
    }
    req = urllib.request.Request(new_url, headers=headers)
    res = urllib.request.urlopen(req)

    return res.read().decode()


def get_result(html):
    # 解析信息
    # patterns = re.compile('<ul>.*?<li>.*?</li>.*?</ul>', re.S)
    patterns = re.compile('<div class="job-primary">.*?<div class="job-title">(.*?)</div>.*?<span class="red">(.*?)</span>.*?<p>(.*?)<em class="vline"></em>(.*?)<em class="vline"></em>(.*?)</p>.*?target="_blank">(.*?)</a></h3>.*?<p>(.*?)<em class="vline"></em>(.*?)<em class="vline"></em>(.*?)</p>.*?</li>', re.S)

    result = patterns.findall(html)
    return result


def main():
    url = 'https://www.zhipin.com/c101280600/?query=python&page={}&ka=page-{}'
    for i in range(1, 2):
        # 组装需要爬取的地址
        new_url = url.format(i, i)
        # 数据的获取
        html = get_html(new_url)
        print(html)
        result = get_result(html)
        print(result)
        for i in result:
            print(i)


if __name__ == '__main__':
    main()
