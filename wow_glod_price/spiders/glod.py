# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from wow_glod_price.items import WowGlodPriceItem
from bs4 import BeautifulSoup as BS4
from wow_glod_price.settings import MAX_PAGE
import js2xml
import re
import time
import random

class GlodSpider(scrapy.Spider):
    name = 'glod'
    allowed_domains = ['5173.com']
    base_url = 'http://s.5173.com/wow-0-0-0-0-ou5epo-0-0-0-a-a-a-a-a-0-0-0-'
    start_urls = [base_url + '1.shtml']
    js_text = None

    def parse(self, response):
        html = Selector(response=response).css('script').extract()
        for i in html:
            if re.search('totalAmount', i):
                i = i.strip('<script type="text/javascript">').strip('</script>')
                self.js_text = js2xml.parse(i, debug=False)
                break
        if len(self.js_text):
            totalAmount = int(self.js_text.xpath('//property[@name="totalAmount"]/number/@value')[0])
            currentPage = int(self.js_text.xpath('//property[@name="currentPage"]/number/@value')[0])
            if totalAmount > MAX_PAGE:
                totalAmount = MAX_PAGE
            while currentPage < totalAmount:
                currentPage +=1
                url = self.base_url+'%s.shtml' % currentPage
                yield Request(
                    url=url,
                    callback=self.order
                )
            # url = self.base_url + '%s.shtml' % 1
            # yield Request(
            #     url=url,
            #     callback=self.order
            # )

    def order(self, response):
        order_href = Selector(response=response).xpath('//li[@class="tt"]/h2/a/@href').extract()
        for href in order_href:
            yield Request(url=href, callback=self.details)

    def details(self, response):
        details_html = Selector(response=response).extract()
        detail = BS4(details_html, 'lxml')
        details_data = self.make_details_data(detail)
        price = details_data.get('price')
        glod = details_data.get('glod')
        if price != 0:
            unit_price = glod/price
        else:
            unit_price = 0
        print(glod,price,response.url)
        item_obj = WowGlodPriceItem(price=price,
                                    glod=glod,
                                    unit_price=unit_price,
                                    area=details_data.get('area'),
                                    server=details_data.get('server'),
                                    camp=details_data.get('camp'),
                                    push_timestrap=details_data.get('push_timestrap'),
                                    order_id=details_data.get('order_id'),
                                    url = response.url
                                    )
        yield item_obj

    def make_details_data(self, detail):
        try:
            price = detail.find(id='spanPrice').text  # 价格
        except AttributeError as e:
            price = detail.find(id='lblPrice').text  # 价格
        glod = detail.find(text=re.compile('^\d+金')).strip('金')  # 金币
        try:
            ddGameAreaServerName = detail.find(id='ddGameAreaServerName').text.split('/')
            area = ddGameAreaServerName[-3].strip()  # 大区
            server = ddGameAreaServerName[-2].strip()  # 服务器
            camp = ddGameAreaServerName[-1].strip()  # 阵营
        except AttributeError as e:
            area = detail.find(id='lbGArea').text
            server = detail.find(id='lbGServer').text
            camp = detail.find(id='lbGameRace').text
        try:
            push_time = detail.find(id='GoodsDescription1_spanEPublishTime').text
            order_id = detail.find(id='GoodsDescription1_spanEBizofferId').text  # 订单号
        except AttributeError as e:
            push_time = detail.find(id='bizOfferInfo_cnt').find_all('label')[0].text.strip().strip('发布时间：')
            order_id = detail.find(id='bizOfferInfo_cnt').find_all('label')[1].text.strip().strip('商品编号：')
        timeArray = time.strptime(push_time, "%Y-%m-%d %H:%M:%S")
        push_timestrap = time.mktime(timeArray)  # 提交时间
        return {
            'price': float(price),
            'glod': float(glod),
            'area': area,
            'server': server,
            'camp': camp,
            'push_timestrap': push_timestrap,
            'order_id': order_id
        }

# def get_proxy():
#     try:
#         with open('proxy.conf') as f:
#             proxys = f.readlines()
#         proxy = random.choice(proxys).strip('\n')
#         return {"http":"http://"+proxy}
#     except (FileNotFoundError,IndexError) as e:
#         return {}