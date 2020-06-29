# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewFangItem, EsfFangItem


class FangSpiderSpider(scrapy.Spider):
    name = 'fang_spider'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td")
            province_td = tds[1]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r'\s','',province_text)
            if province_text:
                province = province_text
            # 海外的房价不能爬取
            if province == '其它':
                continue
            city_td = tds[2]
            citys = city_td.xpath(".//a")
            for city_temp in citys:
                city = city_temp.xpath(".//text()").get()
                city_url = city_temp.xpath(".//@href").get()
                # 构建新房的链接：https://wuhu.newhouse.fang.com /house/s/
                url_model = city_url.split("//")
                url_model = url_model[1].split(".")[0]
                new_house_url = 'https://'+url_model+'.newhouse.fang.com/house/s/'
                # 构建二手房链接：https://wuhu.esf.fang.com/
                esf_house_url = 'https://'+url_model+'.esf.fang.com/'
                # 新房
                yield scrapy.Request(url=new_house_url,
                                     callback=self.parse_new_house,
                                     meta={'info':(province,city)}
                                     )

                # 二手房
                # yield scrapy.Request(url=esf_house_url,
                #                      callback=self.parse_esf_house,
                #                      meta={'info': (province, city)}

    def parse_new_house(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class, 'nl_con')]//li")
        for li in lis:
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get()
            if name is not None:
                name = name.strip()
            room = li.xpath(".//div[contains(@class, 'house_type')]//a/text()").getall()
            room = "/".join(room)
            area = ''.join(li.xpath(".//div[contains(@class, 'house_type')]/text()").getall())
            area = re.sub(r"\s|－",'',area)
            address = li.xpath(".//div[@class='address']/a/@title").get()
            price = ''.join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s","",price)
            on_sale = li.xpath(".//div[contains(@class, 'fangyuan')]/span/text()").get()
            dateil_url = li.xpath(".//div[@class='address']/a/@href").get()
            dateil_url = response.urljoin(dateil_url)
            item = NewFangItem(province=province, city=city, name=name, room=room, area=area, address=address, price=price, on_sale=on_sale, dateil_url=dateil_url)
            yield item
        next_url = response.xpath("//div[@class='page']//a[@class='active']/following-sibling::a[1]/@href").get()
        next_url = response.urljoin(next_url)
        if next_url:
            yield scrapy.Request(url=next_url,
                                 callback=self.parse_new_house,
                                 meta={'info':(province,city)}
                                 # dont_filter=True
                                 )
            # print('*'*100)
            # print(next_url)

    def parse_esf_house(self, response):
        province, city = response.meta['info']
        dl_list = response.xpath("//div[contains(@class, 'shop_list')]//dl")
        for dl in dl_list:
            item = EsfFangItem(province=province, city=city)
            item['name'] = dl.xpath(".//span[@class='tit_shop']/text()").extract_first()
            room_list = dl.xpath(".//p[@class='tel_shop']/text()").extract()
            # 去掉rooms中的空格------>['1室1厅', '50㎡', '高层（共17层）', '东向', '2019年建', '']
            room_list = list(map(lambda x:re.sub(r"\s",'',x), room_list))
            for rooms in room_list:
                if "厅"in rooms:
                    item['room'] = rooms
                elif "㎡" in rooms:
                    item['area'] = rooms
                elif "层"in rooms or "排"in rooms or "加"in rooms or "栋" in rooms or "拼" in rooms:
                    item['floor'] = rooms
                elif "向" in rooms:
                    item['toward'] = rooms
                elif "建" in rooms:
                    item['year'] = rooms
            item['address'] = dl.xpath(".//p[@class='add_shop']//span/text()").extract_first()
            item['price'] = "".join(dl.xpath(".//dd[@class='price_right']/span[1]//text()").extract())
            item['unit_price'] = "".join(dl.xpath(".//dd[@class='price_right']/span[2]//text()").extract())
            item['dateil_url'] = response.urljoin(dl.xpath(".//dt[@class='floatl']/a/@href").extract_first())
            yield item
        next_url = response.xpath("//div[@class='page_al']//p[1]/a/@href").extract_first()
        next_url = response.urljoin(next_url)
        if next_url:
            yield scrapy.Request(url=next_url,
                                 callback=self.parse_esf_house,
                                 meta={'info':(province,city)}
                                 )

