import urllib.request

# urllib.request.urlopen( url,data,timeout)
# url 请求地址,data请求参数,timeout过期时间

# 只传url
# url = 'http://www.baidu.com'
# res = urllib.request.urlopen(url)
# print(res.read().decode())
#
# 传入 url和data
# url = 'http://www.baidu.com/s'
# data = 'wd=python'.encode()
# # urlopen(url,data)默认请求的post请求
# res = urllib.request.urlopen(url, data=data)
# print(res.read().decode())

# url = 'http://www.baidu.com/s?'
# data = 'wd=python'
# # get请求用url拼接
# res = urllib.request.urlopen(url+data)
# print(res.read().decode())

# 传入url和timeout
# url = 'http://www.baidu.com'
# try:
#     res = urllib.request.urlopen(url, timeout=0.001)
#     print(res.read().decode())
# except urllib.error.URLError as e:
#     print(e)

# 语法2
# url = 'http://www.baidu.com'
# res = urllib.request.Request(url,data,headers)
# url = ' http://httpbin.org/get'
# headers = {
#     "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/77.0.3865.120 Safari/537.36 '
# }
# req = urllib.request.Request(url, headers=headers)
#
# # urlopen() 接受参数类型.可以是str 也可以是请求对象
# res = urllib.request.urlopen(req)
# print(res.read().decode())


# ip代理的使用
# proxies = {
#     'http': 'http://118.25.126.213:80'
# }
# url = 'http://httpbin.org/get'
# proxy_handler = urllib.request.ProxyHandler(proxies=proxies)
# opener = urllib.request.build_opener(proxy_handler)
# res = opener.open(url)
# print(res.read().decode())

url_boss = 'https://www.zhipin.com/job_detail/?query=python&city=101280600'
# url_boss = 'http://httpbin.org/get'
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.120 Safari/537.36 '
}
req = urllib.request.Request(url_boss, headers=headers)
res = urllib.request.urlopen(req)
print(res.read().decode())
