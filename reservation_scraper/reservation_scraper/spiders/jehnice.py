# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:46:46 2016

@author: FUSAKLA
"""

import datetime
import urllib
import json

import scrapy
from scrapy.selector import HtmlXPathSelector

from reservation_scraper.items import ReservationScraperItem
from reservation_scraper.db_worker import db_worker


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'badminton-jehnice.e-rezervace.cz',
    'Referer': 'http://badminton-jehnice.e-rezervace.cz/Branch/pages/Schedule.faces',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
    'Content-Type': 'application/x-www-form-urlencoded',
}

opening_hour = 7
NUMBER_OF_WEEKS = 3


class JehniceSpider(scrapy.Spider):
    name = "jehnice"
    allowed_domains = ['badminton-jehnice.e-rezervace.cz']
    start_urls = [
        'http://badminton-jehnice.e-rezervace.cz/Branch/pages/Schedule.faces'
    ]


    def parse(self, response):
        self.sport_center_guid = db_worker.get_center_guid(headers['Host'])
        for i, start_date in enumerate(self.get_start_days()):
            url = 'http://badminton-jehnice.e-rezervace.cz/Branch/pages/Schedule.faces?d=' + start_date.strftime('%d.%m.%Y')
            yield scrapy.Request(url, callback=self.request_view_state, meta={'cookiejar': i}, headers=headers)

    def request_view_state(self, response):
        url = 'http://badminton-jehnice.e-rezervace.cz/Branch/pages/Schedule.faces?d=' + response.url.split('=')[-1]
        yield scrapy.Request(url, callback=self.request_weeks, headers=headers, dont_filter=True, meta={'cookiejar': response.meta['cookiejar']})


    def request_weeks(self, response):
        view_state = str(response.xpath('//input[@id="javax.faces.ViewState"]/@value').extract_first())
        payload = {
            "AJAXREQUEST": 'scheduleNavigForm:schedule-navig-region',
            "scheduleNavigForm:j_id227": "scheduleNavigForm:j_id227",
            "scheduleNavigForm:j_id232": "40001",
            "scheduleNavigForm:view_filter_menu": 'horizontal_service_dayand6days',
            "scheduleNavigForm_SUBMIT": '1',
            "javax.faces.ViewState": view_state
        }
        payload["scheduleNavigForm:schedule_calendarInputCurrentDate"] = '{dt.month}/{dt.year}'.format(dt=datetime.datetime.now())
        #for start_date in self.get_start_days():
        payload["scheduleNavigForm:schedule_calendarInputDate"] = response.url.split('=')[-1]
        yield scrapy.Request(
            'http://badminton-jehnice.e-rezervace.cz/Branch/pages/Schedule.faces',
            self.parse_week,
            method="POST",
            body=urllib.urlencode(payload),
            headers=headers,
            dont_filter=True,
            meta={'cookiejar': response.meta['cookiejar']}
        )

    def parse_week(self, response):
        xml_resp = HtmlXPathSelector(response)
        schedule_data = xml_resp.xpath('//script[contains(text(),"scheduleData")]//text()').extract_first()[19:-4]
        data = json.loads(schedule_data)
        str_base_date = urllib.unquote(response.request.body).split('calendarInputDate=')[1].split('&')[0]
        base_date = datetime.datetime.strptime(str_base_date, '%d.%m.%Y')
        for e in data['events']:
            ev_date = base_date + datetime.timedelta(days=e['gridId'])
            rows = e['end'][1] - e['start'][1]
            for court_num in range(1, rows + 1):
                start_time = ev_date + datetime.timedelta(hours=e['start'][0])
                end_time = ev_date + datetime.timedelta(hours=e['end'][0])
                item = ReservationScraperItem()
                item['start_time'] = str(start_time)
                item['end_time'] = str(end_time)
                item['court_number'] = court_num
                item['fk_sport_center'] = self.sport_center_guid
                yield item

    def get_start_days(self):
        return [datetime.date.today() + datetime.timedelta(days=x) for x in range(0, NUMBER_OF_WEEKS * 7, 7)]
    

        

        
                    
        
            