# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:46:46 2016

@author: FUSAKLA
"""

import scrapy

#from reservation_scraper.items import ReservationScraperItem

import datetime
import urllib

from scrapy.utils.response import open_in_browser


class SprintSpider(scrapy.Spider):
    name = "sprint"
    allowed_domains = ['www.onlinememberpro.cz']
    start_urls = [
        "http://www.onlinememberpro.cz/sprint/"
    ]
    
    
    def parse(self, response):
        dates = self.get_month_days()
        for i,d in enumerate(dates):
            url = self.start_urls[0][:-1]+'?d='+d.strftime('%d.%m.%Y')
            yield scrapy.Request(url, callback=self.parse_hey, meta={'cookiejar': i})
    
    def parse_hey(self, response):
        viewstate = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
        eventvalidation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first()
        viewstategenerator = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        hidden_field = urllib.unquote(response.xpath('//script[contains(@src,"Toolkit")]/@src').extract_first().split('=')[-1])
        act_date = response.url.split('=')[-1]
        payload = {
                "Datepicker1": act_date,
                "HF_ID_KL_G":"0",                
                "Button7":"Zobrazit",
                "ToolkitScriptManager2_HiddenField":hidden_field,
                "TAB_ROZPIS_ClientState":'{"ActiveTabIndex":0,"TabState":[true]}',
                "__VIEWSTATE":viewstate,
                "__EVENTVALIDATION":eventvalidation,
                "__VIEWSTATEGENERATOR":viewstategenerator,
                "__EVENTTARGET":"",
                "__EVENTARGUMENT":"",
                "__SCROLLPOSITIONX":"0",
                "__SCROLLPOSITIONY":"0",
                "__VIEWSTATEENCRYPTED":"",
                "TB_UserName":"",
                "TB_UserName_TextBoxWatermarkExtender_ClientState":"",
                "TB_password":"",
                "TB_password_TextBoxWatermarkExtender_ClientStatev":""
                }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ,
            'Accept-Encoding': 'gzip, deflate' ,
            'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3' ,
            'Connection': 'keep-alive' ,
            'Cookie': 'ASP.NET_SessionId=v05g4iqixnmpg345rpcso055',
            'DNT': '1', 
            'Host': 'www.onlinememberpro.cz' ,
            'Referer': 'http://www.onlinememberpro.cz/sprint/default.aspx' ,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0' ,
            'Content-Type': 'application/x-www-form-urlencoded' 
            }
        yield scrapy.Request('http://www.onlinememberpro.cz/sprint/default.aspx', callback=self.parse_day, method="POST", body=urllib.urlencode(payload),meta={'cookiejar': response.meta['cookiejar']},headers=headers)
        
        
    
    def parse_day(self, response):
        d = response.xpath('//input[@id="Datepicker1"]/@value').extract_first()
        print '**********************************'
        print d
        with open('sprint.html', 'wb') as f:
            f.write(response.body)
        
        
        
    
    def get_month_days(self):
        return [datetime.date.today()+datetime.timedelta(days=x) for x in range(30)]
    
    def get_border_times(self, act_date, time_string):
        start, end = [x.strip() for x in time_string.split('-')]
        start_hour, start_minute = [int(x) for x in start.split(':')]
        end_hour, end_minute = [int(x) for x in end.split(':')]
        start_datetime = act_date.replace(hour=start_hour, minute=start_minute)
        end_datetime = act_date.replace(hour=end_hour, minute=end_minute)
        return start_datetime, end_datetime
        

        

                    
        
            