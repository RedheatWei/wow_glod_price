# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WowGlodPriceItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    glod = scrapy.Field()
    unit_price = scrapy.Field()
    area = scrapy.Field()
    server = scrapy.Field()
    camp = scrapy.Field()
    push_timestrap = scrapy.Field()
    order_id = scrapy.Field()
    url = scrapy.Field()
