# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:46:46 2016

@author: FUSAKLA
"""

import datetime

import scrapy

from reservation_scraper.items import ReservationScraperItem
from reservation_scraper.db_worker import db_worker


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'www.fit4all.cz',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
}

BASE_URL = 'http://www.fit4all.cz/cs/online-rezervace?id_sportoviste=6&id_instruktora=-1&id_typ_lekce=-1&datum='
RESERVATION_LENGTH = 30
DAY_COUNT = 30


class Fit4AllSpider(scrapy.Spider):
    name = "fit4all"
    allowed_domains = ['fit4all.cz']


    def start_requests(self):
        self.sport_center_guid = db_worker.get_center_guid(headers['Host'])
        dates = self.get_month_days()
        for i, d in enumerate(dates):
            url = BASE_URL + d.strftime('%d.%m.%Y')
            yield scrapy.Request(url, callback=self.parse_day, headers=headers)


    def parse_day(self, response):
        act_date = datetime.datetime.strptime(response.url.split('=')[-1], '%d.%m.%Y')
        rows = response.xpath('//table[@class="rozvrh-1"]//tr')[1:]
        for r in rows:
            cells = r.xpath('td[@class="bunka-rozvrhu"]')
            for c_num, c in enumerate(cells):
                divs = c.xpath('div')
                for d in divs:
                    if 'obsadene' in d.xpath('@class').extract_first():
                        hour = int(d.xpath('@data-hod').extract_first())
                        minutes = int(d.xpath('@data-min').extract_first())
                        start_time = act_date + datetime.timedelta(hours=hour, minutes=minutes)
                        end_time = start_time + datetime.timedelta(minutes=RESERVATION_LENGTH)
                        item = ReservationScraperItem()
                        item['start_time'] = str(start_time)
                        item['end_time'] = str(end_time)
                        item['court_number'] = c_num + 1
                        item['fk_sport_center'] = self.sport_center_guid
                        yield item

    @staticmethod
    def get_month_days():
        return [datetime.date.today() + datetime.timedelta(days=x) for x in range(DAY_COUNT)]

        

        
                    
        
            