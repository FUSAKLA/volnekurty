# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:46:46 2016

@author: FUSAKLA
"""

import scrapy

#from reservation_scraper.items import ReservationScraperItem

import datetime
import urllib

from reservation_scraper.items import ReservationScraperItem
from reservation_scraper.db_worker import db_worker


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'www.onlinememberpro.cz',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
}

court_number_shift = 6

HOURS_SHIFT = 5

MINUTES_ID_MAPPING = {
    '01': 0,
    '03': 30
}

RESERVATION_LENGTH = 30

BASE_URL = "http://www.onlinememberpro.cz/sprint/"

DAY_COUNT = 7


class SprintSpider(scrapy.Spider):
    name = "sprint"
    allowed_domains = ['www.onlinememberpro.cz']

    def start_requests(self):
        self.sport_center_guid = db_worker.get_center_guid(headers['Host'])
        db_worker.remove_center_reservations(self.sport_center_guid)
        db_worker.update_center_last_edited(self.sport_center_guid)
        dates = self.get_month_days()
        for i, d in enumerate(dates):
            url = BASE_URL + '?d=' + d.strftime('%d.%m.%Y')
            yield scrapy.Request(url, callback=self.get_day, meta={'cookiejar': i}, headers=headers)

    def get_day(self, response):
        viewstate = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
        eventvalidation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first()
        viewstategenerator = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        hidden_field = urllib.unquote(response.xpath('//script[contains(@src,"Toolkit")]/@src').extract_first().split('=')[-1])
        act_date = response.url.split('=')[-1]
        payload = {
            "Datepicker1": act_date,
            "HF_ID_KL_G": "0",
            "BTN3": "Badminton+hala",
            "ToolkitScriptManager2_HiddenField": hidden_field,
            "TAB_ROZPIS_ClientState": '{"ActiveTabIndex":0,"TabState":[true]}',
            "__VIEWSTATE": viewstate,
            "__EVENTVALIDATION": eventvalidation,
            "__VIEWSTATEGENERATOR": viewstategenerator,
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__SCROLLPOSITIONX": "0",
            "__SCROLLPOSITIONY": "0",
            "__VIEWSTATEENCRYPTED": "",
            "TB_UserName": "",
            "TB_UserName_TextBoxWatermarkExtender_ClientState": "",
            "TB_password": "",
            "TB_password_TextBoxWatermarkExtender_ClientStatev": ""
        }
        headers['Referer'] = 'http://www.onlinememberpro.cz/sprint/default.aspx'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        yield scrapy.Request(
            'http://www.onlinememberpro.cz/sprint/default.aspx',
            callback=self.parse_day,
            method="POST",
            body=urllib.urlencode(payload),
            meta={'cookiejar': response.meta['cookiejar']},
            headers=headers
        )

    def parse_day(self, response):
        d = response.xpath('//input[@id="Datepicker1"]/@value').extract_first()
        act_day = datetime.datetime.strptime(d, '%d.%m.%Y')
        rezervation_inputs = response.xpath('//input[@class="btnrezclose"]/@name')
        for rezervation in rezervation_inputs:
            rez_id = rezervation.extract().split('$BTN1')[-1]
            court_num = int(rez_id[:2]) - court_number_shift
            hour = int(rez_id[2:4]) + HOURS_SHIFT
            minutes = MINUTES_ID_MAPPING[rez_id[4:]]
            start_time = act_day + datetime.timedelta(hours=hour, minutes=minutes)
            end_time = start_time + datetime.timedelta(minutes=RESERVATION_LENGTH)
            item = ReservationScraperItem()
            item['start_time'] = str(start_time)
            item['end_time'] = str(end_time)
            item['court_number'] = court_num
            item['fk_sport_center'] = self.sport_center_guid
            yield item

    @staticmethod
    def get_month_days():
        return [datetime.date.today() + datetime.timedelta(days=x) for x in range(DAY_COUNT)]
    


        

                    
        
            