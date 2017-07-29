# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: 
                   这一部分考虑用scrapy框架代替
-------------------------------------------------
"""
import re
import requests

try:
    from importlib import reload   #py3 实际不会实用，只是为了不显示语法错误
except:
    import sys     # py2
    reload(sys)
    sys.setdefaultencoding('utf-8')

sys.path.append('../')


from Util.utilFunction import robustCrawl, getHtmlTree, getHTMLText
import logging
from Util.LogHandler import LogHandler
import time

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()

HEADER = {'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          }


class GetFreeProxy(object):
    """
    proxy getter
    """

    def __init__(self):
        self.log = LogHandler('get_freeproxy')
        pass

    @staticmethod
    @robustCrawl    #decoration print error if exception happen
    def freeProxyFirst(page=10):
        """
        抓取快代理IP http://www.kuaidaili.com/
        :param page: 翻页数
        :return:
        """
        url_list = ('http://www.kuaidaili.com/proxylist/{page}/'.format(page=page) for page in range(1, page + 1))
        # 页数不用太多， 后面的全是历史IP， 可用性不高

        for url in url_list:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//div[@id="index_free_list"]//tbody/tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    @staticmethod
    @robustCrawl
    def freeProxySecond(proxy_number=100):
        """
        抓取代理66 http://www.66ip.cn/
        :param proxy_number: 代理数量
        :return:
        """
        url = "http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            proxy_number)

        html = getHTMLText(url, headers=HEADER)
        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy

    @staticmethod
    @robustCrawl
    def freeProxyThird(days=1):
        """
        抓取有代理 http://www.youdaili.net/Daili/http/
        :param days:
        :return:
        """
        url = "http://www.youdaili.net/Daili/http/"
        tree = getHtmlTree(url)
        page_url_list = tree.xpath('.//div[@class="chunlist"]/ul/li/p/a/@href')[0:days]
        for page_url in page_url_list:
            html = requests.get(page_url, headers=HEADER).content
            # print html
            proxy_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)
            for proxy in proxy_list:
                yield proxy

    @staticmethod
    @robustCrawl
    def freeProxyFourth():
        """
        抓取西刺代理 http://api.xicidaili.com/free2016.txt
        :return:
        """
        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    ]
        for each_url in url_list:
            tree = getHtmlTree(each_url)
            proxy_list = tree.xpath('.//table[@id="ip_list"]//tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    @staticmethod
    @robustCrawl
    def freeProxyFifth():
        """
        抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
        :return:
        """
        url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
        for page in range(1, 10):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)
            proxy_list = tree.xpath('//td[@class="ip"]')
            for each_proxy in proxy_list:
                yield ''.join(each_proxy.xpath('.//text()'))

    @staticmethod
    @robustCrawl
    def freeProxyKuaiDaili():
        """
        抓取kuaidaili
        :return:
        """
        url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=937606445877172&num=30&area=%E5%9B%BD%E5%A4%96&' \
            'area_ex=%E5%8D%B0%E5%BA%A6%E5%B0%BC%E8%A5%BF%E4%BA%9A%2C%E6%B3%B0%E5%9B%BD%2C%E5%B7%B4%E8%A5%BF' \
            '%2C%E4%BF%84%E7%BD%97%E6%96%AF%2C%E5%A7%94%E5%86%85%E7%91%9E%E6%8B%89%2C%E4%BC%8A%E6%9C%97%2C%E' \
            '5%8D%B0%E5%BA%A6%2C%E8%8D%B7%E5%85%B0%2C%E6%8D%B7%E5%85%8B%2C%E5%9F%83%E5%8F%8A%2C%E4%B9%8C%E5%' \
            '85%8B%E5%85%B0%2C%E5%9C%9F%E8%80%B3%E5%85%B6%2C%E9%98%BF%E6%A0%B9%E5%BB%B7%2C%E6%B3%A2%E5%85%B0' \
            '%2C%E5%AD%9F%E5%8A%A0%E6%8B%89%E5%9B%BD%2C%E7%A7%98%E9%B2%81%2C%E8%B6%8A%E5%8D%97%2C%E6%B3%95%E' \
            '5%9B%BD%2C%E4%BB%A5%E8%89%B2%E5%88%97%2C%E5%93%A5%E4%BC%A6%E6%AF%94%E4%BA%9A%2C%E8%8B%B1%E5%9B%' \
            'BD%2C%E7%BD%97%E9%A9%AC%E5%B0%BC%E4%BA%9A%2C%E4%BC%8A%E6%8B%89%E5%85%8B%2C%E8%8F%B2%E5%BE%8B%E5' \
            '%AE%BE%2C%E9%9F%A9%E5%9B%BD%2C%E6%97%A5%E6%9C%AC%2C%E8%A5%BF%E7%8F%AD%E7%89%99%2C%E6%99%BA%E5%8' \
            '8%A9%2C%E5%8D%97%E9%9D%9E%2C%E6%9F%AC%E5%9F%94%E5%AF%A8%2C%E5%8A%A0%E6%8B%BF%E5%A4%A7%2C%E5%8E%' \
            '84%E7%93%9C%E5%A4%9A%E5%B0%94%2C%E9%A9%AC%E6%9D%A5%E8%A5%BF%E4%BA%9A%2C%E6%96%AF%E6%B4%9B%E4%BC' \
            '%90%E5%85%8B%2C%E9%98%BF%E8%81%94%E9%85%8B%2C%E6%91%A9%E5%B0%94%E5%A4%9A%E7%93%A6%2C%E7%91%9E%E' \
            '5%85%B8%2C%E5%B0%BC%E6%97%A5%E5%88%A9%E4%BA%9A%2C%E4%BF%9D%E5%8A%A0%E5%88%A9%E4%BA%9A%2C%E5%B7%' \
            'B4%E5%9F%BA%E6%96%AF%E5%9D%A6%2C%E6%A0%BC%E9%B2%81%E5%90%89%E4%BA%9A%2C%E5%B7%B4%E6%8B%89%E5%9C' \
            '%AD%2C%E5%B8%8C%E8%85%8A%2C%E7%8E%BB%E5%88%A9%E7%BB%B4%E4%BA%9A%2C%E8%8E%AB%E6%A1%91%E6%AF%94%E' \
            '5%85%8B%2C%E5%93%88%E8%90%A8%E5%85%8B%E6%96%AF%E5%9D%A6%2C%E7%99%BD%E4%BF%84%E7%BD%97%E6%96%AF%' \
            '2C%E8%91%A1%E8%90%84%E7%89%99%2C%E9%A9%AC%E8%BE%BE%E5%8A%A0%E6%96%AF%E5%8A%A0%2C%E8%82%AF%E5%B0' \
            '%BC%E4%BA%9A%2C%E6%B4%A5%E5%B7%B4%E5%B8%83%E9%9F%A6%2C%E5%A5%A5%E5%9C%B0%E5%88%A9%2C%E5%96%80%E' \
            '9%BA%A6%E9%9A%86%2C%E4%B8%B9%E9%BA%A6%2C%E6%AF%94%E5%88%A9%E6%97%B6%2C%E5%9D%A6%E6%A1%91%E5%B0%' \
            'BC%E4%BA%9A%2C%E7%91%9E%E5%A3%AB%2C%E6%AF%9B%E9%87%8C%E6%B1%82%E6%96%AF%2C%E6%96%B0%E8%A5%BF%E5' \
            '%85%B0%2C%E5%A1%9E%E6%B5%A6%E8%B7%AF%E6%96%AF%2C%E6%8C%AA%E5%A8%81%2C%E8%92%99%E5%8F%A4%2C%E7%8' \
            '8%B1%E5%B0%94%E5%85%B0%2C%E7%AB%8B%E9%99%B6%E5%AE%9B%2C%E8%80%81%E6%8C%9D%2C%E5%88%9A%E6%9E%9C%' \
            '2C%E5%8F%99%E5%88%A9%E4%BA%9A%2C%E5%AE%89%E5%93%A5%E6%8B%89%2C%E5%8C%88%E7%89%99%E5%88%A9%2C%E6' \
            '%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9A%2C%E7%AA%81%E5%B0%BC%E6%96%AF%2C%E5%AE%89%E9%81%93%E5%B0%94%2' \
            'C%E6%96%AF%E6%B4%9B%E6%96%87%E5%B0%BC%E4%BA%9A%2C%E6%8B%89%E8%84%B1%E7%BB%B4%E4%BA%9A&browser=1' \
            '&protocol=2&method=2&quality=0&sort=0&format=text&sep=1'
        
        content = getHTMLText(url)
        if content.find("ERROR") != -1:
            print 'ERROR', 'failed ! request kuaidaili url  .'
            time.sleep(10)

        ip_list = content.split('\r\n')
        for proxy in ip_list:
            yield proxy

if __name__ == '__main__':
    gg = GetFreeProxy()
    # for e in gg.freeProxyFirst():
    #     print e

    # for e in gg.freeProxySecond():
    #     print e

    # for e in gg.freeProxyThird():
    #     print e
    #
    # for e in gg.freeProxyFourth():
    #     print e

    for e in gg.freeProxyKuaiDaili():
        print(e)