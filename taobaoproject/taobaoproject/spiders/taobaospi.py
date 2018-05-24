# -*- coding: utf-8 -*-
import scrapy
import re
import json


class TaobaospiSpider(scrapy.Spider):
    name = 'taobaospi'
    allowed_domains = ['taobao.com']
    start_urls = ['http://www.taobao.com/']

    def parse(self, response):
        keys = str(open('keyword.txt').read()).rsplit('\n')
        for key in keys:
            url = 'https://s.taobao.com/search?q={}'.format(key)
            yield scrapy.Request(url,callback=self.read_url)

    def read_url(self,response):
        allsid = re.compile('isMulti":true,"sub":(.*?)isMulti":true,"sub":',re.S).findall(response.text)[0]
        sid = re.compile('{"text":"(.*?)","desc":"","isExpandShow":false,"key":"ppath","value":"(.*?)","',re.S).findall(allsid)
        for i in sid:
            url = response.url+"&ppath="+list(i)[1]
            yield scrapy.Request(url,callback=self.Category_id)

    def Category_id(self,response):
        urlid = str(response.url).rsplit('?')[1]
        pages = re.compile('"totalPage":(.*?),"currentPage"', re.S).findall(response.text)
        print("当前page数为:"+str(pages))
        url = 'https://s.taobao.com/search?data-key=s&data-value={}&ajax=true&callback=jsonp815&'

        # try:
        #     pages = re.compile('"totalPage":(.*?),"currentPage"',re.S).findall(response.text)[0]
        #     for i in range(0, int(pages)):
        #
        #         url = 'https://s.taobao.com/search?data-key=s&data-value={}&ajax=true&callback=jsonp815&'.format(
        #             i * 44) + urlid
        #         yield scrapy.Request(url, callback=self.read_data)
        # except IndexError:
        #     print('暂无翻页')



    def read_data(self,response):
        alls = str(re.compile('"nid":"(.*?)","category":".*?","pid"',re.S).findall(response.text))
        print(alls)

