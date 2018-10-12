#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@auther = 'Redheat'
@create = '2018/10/11 14:45'
@email = 'qjyyn@qq.com'
'''
from peewee import MySQLDatabase, Model,FloatField,CharField

db = MySQLDatabase('spyders', host='127.0.0.1', user='root', passwd='vv231', charset='utf8', port=3306)
db.connect()

class WowGlodPrice(Model):
    price = FloatField(verbose_name='价格')
    glod = FloatField(verbose_name='金币')
    unit_price = FloatField(verbose_name='单价')
    area = CharField(verbose_name='大区')
    server = CharField(verbose_name='服务器')
    camp = CharField(verbose_name='阵营')
    push_timestrap = CharField(verbose_name='订单时间')
    order_id = CharField(verbose_name='订单号')
    url = CharField(verbose_name='url')

    class Meta:
        database = db
        table_name = 'wow_glod_price'  # 这里可以自定义表名
