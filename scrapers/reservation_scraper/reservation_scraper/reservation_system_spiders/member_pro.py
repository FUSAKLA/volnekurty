from datetime import datetime, timedelta
import re
import urllib

import scrapy
from reservation_scraper.items import ReservationScraperItem
from reservation_scraper.db_driver.mongo import MongoDriver
from reservation_scraper.utils import date_utils
from config import config


class MemberProSpider(scrapy.Spider):
    name = "member_pro"

    day_count_to_scrape = int(config["TimeInterval"]["DayCountToScrape"])

    base_url_pattern = "http://www.{host}/{sname}/"
    ajax_url_pattern = "{base_url}/default.aspx"
    host_pattern = "{host}/{url_name}"
    hours_shift = 5
    reservation_length = 30
    court_number_shift = 6
    minutes_id_mapping = {
        '01': 0,
        '03': 30
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': "",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
    }

    def __init__(self, reservation_system_host, system_url_name, additional_payload):
        system_domain = ".".join(reservation_system_host.split(".")[-2:])
        self.allowed_domains = [system_domain]
        self.base_url = self.base_url_pattern.format(host=reservation_system_host, sname=system_url_name)
        self.ajax_url = self.ajax_url_pattern.format(base_url=self.base_url)
        self.headers["Host"] = reservation_system_host
        self.host = self.host_pattern.format(host=reservation_system_host, url_name=system_url_name)
        self.additional_payload = additional_payload

    def start_requests(self):
        MongoDriver.delete_all_future_facility_reservations(self.host)
        for i, d in enumerate(date_utils.get_days_set(self.day_count_to_scrape)):
            url = self.base_url + '?d=' + d.strftime('%d.%m.%Y')
            yield scrapy.Request(url, callback=self.get_day, meta={'cookiejar': i}, headers=self.headers)

    def get_day(self, response):
        viewstate = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
        eventvalidation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first()
        viewstategenerator = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        hidden_field = urllib.parse.unquote(response.xpath('//script[contains(@src,"Toolkit")]/@src').extract_first().split('=')[-1])
        act_date = response.url.split('=')[-1]
        payload = {
            "Datepicker1": act_date,
            "HF_ID_KL_G": "0",
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
        payload.update(self.additional_payload)

        print("?????????????????????????????????????")
        print(self.headers)
        print("?????????????????????????????????????")
        self.headers['Referer'] = response.url
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        yield scrapy.Request(
            self.ajax_url,
            callback=self.parse_day,
            method="POST",
            body=urllib.parse.urlencode(payload),
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.headers
        )

    def parse_day(self, response):
        with open("response.html", "w") as f:
            f.write(response.text)
        d = response.xpath('//input[@id="Datepicker1"]/@value').extract_first()
        act_day = datetime.strptime(d, '%d.%m.%Y').date()
        opening_hour_text = response.xpath('//td[contains(@id, "TAB_ROZPIS_TabPanel_l_1_TH")]/text()')[0].extract()
        opening_time = date_utils.time_from_text(opening_hour_text)
        act_datetime = datetime.combine(act_day, opening_time)
        rezervation_inputs = response.xpath('//input[@class="btnrezclose"]/@name')
        for rezervation in rezervation_inputs:
            # dont touch this, once you tried after some time and those BTN ids are black magick
            # seriously dude... back off
            rez_id = rezervation.extract().split('$BTN')[-1]
            btn_id = self.parse_btn_id(rez_id)
            court_num = int(btn_id["line_id"]) - self.court_number_shift
            hour = int(btn_id["hour_shift"])-1
            minutes = self.minutes_id_mapping[btn_id["hour_part"]]
            start_time = act_datetime + timedelta(hours=hour, minutes=minutes)
            end_time = start_time + timedelta(minutes=self.reservation_length)
            item = ReservationScraperItem()
            item['start_time'] = start_time
            item['end_time'] = end_time
            item['court_id'] = court_num
            item['facility_id'] = self.host
            item['html_id'] = rez_id
            yield item

    @staticmethod
    def parse_btn_id(id_text):
        id_pattern = re.compile(r"[0-9](?P<line_id>[0-9]{2})(?P<hour_shift>[0-9]{2})(?P<hour_part>[0-9]{2})")
        return id_pattern.search(id_text).groupdict()







