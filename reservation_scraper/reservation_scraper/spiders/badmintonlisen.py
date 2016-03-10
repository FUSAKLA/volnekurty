# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:46:46 2016

@author: FUSAKLA
"""

import scrapy

from reservation_scraper.items import ReservationScraperItem


import datetime
import json
from bs4 import BeautifulSoup

headers = {
            'Accept': '*/*' ,
            'Accept-Encoding': 'gzip, deflate' ,
            'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3' ,
            'Connection': 'keep-alive' ,
            'DNT': '1', 
            'Host': "www.badmintonlisen.cz" ,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'X-Requested-With': "XMLHttpRequest",
            'Referer': "http://www.badmintonlisen.cz/rezervace/"
            }



BASE_URL = 'http://www.badmintonlisen.cz/www/rezervace/?do=updateFormSnippet&d='
RESERVATION_LENGTH = 30
DAY_COUNT = 30


class LisenSpider(scrapy.Spider):
    name = "lisen"
    allowed_domains = ['badmintonlisen.cz']
    
    
    def start_requests(self):
        dates = self.get_month_days()
        for i,d in enumerate(dates):
            url = BASE_URL+d.strftime('%d.%m.%Y')
            yield scrapy.Request(
                url, 
                callback=self.parse_day, 
                headers=headers
            )
        
    
    
    def parse_day(self, response):
        act_date = datetime.datetime.strptime(response.url.split('=')[-1],'%d.%m.%Y')
        resp_data = json.loads(response.body)        
        html = resp_data['snippets']['snippet--resSnippet']
        html_resp = BeautifulSoup(html, 'html.parser')
        rows = html_resp.tbody.find_all('tr')
        for r in rows:
            cells = r.find_all('td')
            time_cell = cells[0].text.strip().split(' - ')
            start_time_cell = [int(x) for x in time_cell[0].split(':')]
            start_time = act_date + datetime.timedelta(
                                        hours=start_time_cell[0],
                                        minutes=start_time_cell[1]
                                    )
            end_time_cell = [int(x) for x in time_cell[0].split(':')]
            end_time = act_date + datetime.timedelta(
                                        hours=end_time_cell[0],
                                        minutes=end_time_cell[1]
                                    )
            for c_num, c in enumerate(cells[1:]):
                input_element = c.input
                if input_element.has_attr('checked'):
                    item = ReservationScraperItem() 
                    item['start_time'] = str(start_time)
                    item['end_time'] = str(end_time)
                    item['court_number'] = c_num+1
                    item['reservation_type'] = 'normal'
                    yield item
    
    def get_month_days(self):
        return [datetime.date.today()+datetime.timedelta(days=x) for x in range(DAY_COUNT)]

        

        
                    
        
            