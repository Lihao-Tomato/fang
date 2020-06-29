# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class FangPipeline(object):
    def __init__(self):
        dbparams = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'root',
            'database':'fang',
            'charset':'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None
    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item["province"],item['city'],item['name'],item['room'],item['address'],item['price'],item['area'],item['on_sale'],item['dateil_url']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into fang_info(id, province, city, name, room, address, price, area, on_sale, dateil_url) values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            return self._sql
        return self._sql
