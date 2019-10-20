import html
import random
import re
import ssl
import time
import urllib
# from HTMLParser import HTMLParser
import requests
from bs4 import BeautifulSoup
from lxml import etree

# from lxml.etree import HTMLParser

from CreatDB.models import TypeShop, TypeShop2, ShopList, ShopInfo


# 爬取分类
def creat(files):
    with open(files, 'rb') as f:
        index = f.read()
        index = index.decode(encoding='utf-8')

    bea = BeautifulSoup(index)
    for i in bea.find_all(class_='servicecontent'):
        # print(i)
        # print(type(i))
        bed = i.span.text
        ts = TypeShop(name=bed)
        ts.save()
        # print(ts.id)
        bed2 = i.find_all('a')
        # print('*' * 50)
        # print(bed)
        # print(bed2)
        for i in bed2:
            # print('    ', i.text)
            tss = TypeShop2(name=i.text, Fisrt_id=ts.id)
            tss.save()
            # print(tss.id)


# 商品信息
def shops(url, price,shop_list_id):
    # 构造每一页的url变化
    # print(url)
    # url = f'https://search.jd.com/Search?keyword={i2.name}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&page={2*n-1}&click=0'
    # url = f'https://search.jd.com/Search?keyword={i2.name}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page=' + str(2 * n - 1)
    head = {
        # 'authority': 'search.jd.com',
        'method': 'GET',
        # 'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=4&s=84&scrolling=y&log_id=1529828108.22071&tpl=3_M&show_items=7651927,7367120,7056868,7419252,6001239,5934182,4554969,3893501,7421462,6577495,26480543553,7345757,4483120,6176077,6932795,7336429,5963066,5283387,25722468892,7425622,4768461',
        'scheme': 'https',
        'referer': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'Cookie': 'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'
    }

    r = requests.get(url, headers=head)
    # 指定编码方式，不然会出现乱码
    # r.encoding = 'utf-8'
    html1 = etree.HTML(r.text)
    # print(html1)
    # 定位到每一个商品标签li
    datas = html1.xpath('body/div[@class="w"]/div[@class="product-intro clearfix"]')[0][0]
    introduction = datas.xpath('//*[@class="sku-name"]//text()')[0].strip()
    # print(introduction)
    name = re.findall(r'^([\u4e00-\u9fa5]+)', introduction,re.S)
    # print(type(name))
    # print(name)
    kind = []
    if name :
        for x in range(random.randint(0, 10)):

            kind_str = name[0] \
                       + f'种类{x}'
            kind.append(kind_str)
        kind = str(kind)
        inventory = random.randint(100, 10000)
        sales = random.randint(100, 10000)

        # Image = datas.xpath('div[@class="sku-name"]text()')
        image_url = datas.xpath('//*[@id="spec-img"]/@*')[2]
        # print(price, '|', introduction, sales, kind, image_url, )
        # print(type(inventory))
        ShopInfo.objects.create(name=name, price=price[0],
                                introduction=introduction,
                                sales=sales,
                                kind=kind,
                                image_url=image_url,
                                inventory=int(inventory),
                                shop_list_id=shop_list_id
                                ).save()


# 商品列表
def crow_first(i2, n):
    # 构造每一页的url变化
    print("hh",i2)
    url = f'https://search.jd.com/Search?keyword={i2.name}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&page={2 * n - 1}&click=0'
    # url = f'https://search.jd.com/Search?keyword={i2.name}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page=' + str(2 * n - 1)
    head = {'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=4&s=84&scrolling=y&log_id=1529828108.22071&tpl=3_M&show_items=7651927,7367120,7056868,7419252,6001239,5934182,4554969,3893501,7421462,6577495,26480543553,7345757,4483120,6176077,6932795,7336429,5963066,5283387,25722468892,7425622,4768461',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'
            }
    r = requests.get(url, headers=head)
    # 指定编码方式，不然会出现乱码
    r.encoding = 'utf-8'
    html1 = etree.HTML(r.text)
    # 定位到每一个商品标签li
    datas = html1.xpath('//li[contains(@class,"gl-item")]')
    # print(datas)
    for data in datas:

        p_price = data.xpath('div/div[@class="p-price"]/strong/i/text()')
        p_shop_url = data.xpath('div/div[@class="p-name p-name-type-2"]/a/@href')
        # str().split

        # print(p_shop_url)
        if not p_shop_url:
            continue
        p_shop_url = p_shop_url[0].split(':')
        # if len(p_shop_url) == 2:
            # print('sss',p_shop_url)
        p_shop_url = p_shop_url[-1]
        # print(p_shop_url)
        p_shop_url="https:"+p_shop_url
        p_image_url = data.xpath('div/div[@class="p-img"]/a/img/@*')
        # print('url', p_image_url)
        p_name = data.xpath('div/div[@class="p-name p-name-type-2"]/a/em/text()')
        # 这个if判断用来处理那些价格可以动态切换的商品，比如上文提到的小米MIX2，他们的价格位置在属性中放了一个最低价
        if len(p_price) == 0:
            p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')
            # xpath('string(.)')用来解析混夹在几个标签中的文本

        # print('shoplist', p_name, p_shop_url, p_price, p_image_url)
        shop_list_id = ShopList.objects.create(introduction=str(p_name),
                                               price=float(p_price[0]),
                                               image_url=str(p_image_url),
                                               big_id=i2.Fisrt_id,
                                               small_id=i2.id)
        shop_list_id.save()
        # print(shop_list_id.id)
        shops(p_shop_url, p_price,shop_list_id.id)


# 定义函数抓取每页后30条商品信息
def crow_last(i2, n):
    # 获取当前的Unix时间戳，并且保留小数点后5位
    a = time.time()
    b = '%.5f' % a
    url = f'https://search.jd.com/s_new.php?keyword={i2.name}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=' + str(
        2 * n) + '&s=' + str(48 * n - 20) + '&scrolling=y&log_id=' + str(b)
    head = {'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'

            }
    r = requests.get(url, headers=head)
    r.encoding = 'utf-8'
    html1 = etree.HTML(r.text)
    datas = html1.xpath('//li[contains(@class,"gl-item")]')
    # print(datas)


def files_jd():
    lei1 = TypeShop.objects.all()
    print(lei1)
    for i in lei1[6:]:
        print(i.id)
        print('   First_Page:   ' + str(i))
        lei2 = TypeShop2.objects.filter(Fisrt_id=i.id)
        print(lei2)
        for i2 in lei2:
            print(i2.id, i2.name, i2.Fisrt_id)
            for inumber in range(1,2):
                # 下面的print函数主要是为了方便查看当前抓到第几页了
                print('***************************************************')
                # try:
                crow_first(i2, inumber)
                # print('   Finish')
                # except Exception as e:
                #     print('错误first', e)
                # print('------------------')
                # try:
                #     print('   Last_Page:   ' + str(i))
                #     crow_last(i2, inumber)
                #     print('   Finish')
                # except Exception as e:
                #     print('错误list', e)
                # time.sleep(1)
