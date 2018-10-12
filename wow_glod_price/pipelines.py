# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import peewee
from scrapy.exceptions import DropItem
from wow_glod_price.handler_db import WowGlodPrice
class WowGlodPricePipeline(object):
    def process_item(self, item, spider):
        if item:
            try:
                WowGlodPrice.get(order_id = item['order_id'])
            except peewee.DoesNotExist as e:
                data = WowGlodPrice(
                    price=item['price'],
                    glod=item['glod'],
                    unit_price=item['unit_price'],
                    area=item['area'],
                    server=item['server'],
                    camp=item['camp'],
                    push_timestrap=item['push_timestrap'],
                    order_id=item['order_id'],
                    url=item['url']
                )
                data.save()
        else:
            raise DropItem
