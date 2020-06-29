# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewFangItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区
    name = scrapy.Field()
    # 居室
    room = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 是否在售
    on_sale = scrapy.Field()
    # 详情页面
    dateil_url = scrapy.Field()



class EsfFangItem(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区
    name = scrapy.Field()
    # 居室
    room = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 几层
    floor = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 总价
    price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 详情页面
    dateil_url = scrapy.Field()

