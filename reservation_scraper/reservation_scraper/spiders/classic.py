# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:46:46 2016

@author: FUSAKLA
"""

import scrapy

from reservation_scraper.items import ReservationScraperItem

import datetime


class ClassicSpider(scrapy.Spider):
    name = "classic"
    allowed_domains = ['clubclassic.cz']
    start_urls = [
        "http://rezervace.clubclassic.cz/index.php?page=day_overview&id=29"
    ]
    
    
    def parse(self, response):
        dates = self.get_month_days()
        for d in dates:
            url = response.urljoin('?page=day_overview&id=29&date='+str(d))
            yield scrapy.Request(url, callback=self.parse_day)
        
    
    
    def parse_day(self, response):
        act_date = datetime.datetime.strptime(response.url.split('=')[-1],'%Y-%m-%d')
        rows = response.xpath('//table[@class="btable denni-prehled"]//tr[@class="rows"]')
        for r in rows:
            time_cell = r.xpath('th/text()')  
            start_datetime, end_datetime = self.get_border_times(act_date,time_cell.extract_first())
            cells = r.xpath('td')
            for c_num, c in enumerate(cells):
                if c.xpath('@class').extract_first() == 'obsazeno':
                    item = ReservationScraperItem() 
                    item['start_time'] = str(start_datetime)
                    item['end_time'] = str(end_datetime)
                    item['court_number'] = c_num+1
                    item['reservation_type'] = 'normal'
                    yield item
    
    def get_month_days(self):
        return [datetime.date.today()+datetime.timedelta(days=x) for x in range(30)]
    
    def get_border_times(self, act_date, time_string):
        start, end = [x.strip() for x in time_string.split('-')]
        start_hour, start_minute = [int(x) for x in start.split(':')]
        end_hour, end_minute = [int(x) for x in end.split(':')]
        start_datetime = act_date.replace(hour=start_hour, minute=start_minute)
        end_datetime = act_date.replace(hour=end_hour, minute=end_minute)
        return start_datetime, end_datetime
        

        
                    
        
            