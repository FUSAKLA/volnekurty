import datetime
import re
import urllib
import json

import scrapy
from scrapy.selector import HtmlXPathSelector
from reservation_scraper.items import ReservationScraperItem
from reservation_scraper.utils import date_utils
from reservation_scraper.db_driver.mongo import MongoDriver
from config import config


class BizzySpider(scrapy.Spider):
    name = "bizzy"

    day_count_to_scrape = int(config["TimeInterval"]["DayCountToScrape"])

    calendar_input_day_pattern = re.compile(r"calendarInputDate=([0-9\.]+)[&\']")
    base_url_pattern = "http://{host}/Branch/pages/Schedule.faces"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': "",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    def __init__(self, reservation_system_host, additional_ajax_payload):
        system_domain = ".".join(reservation_system_host.split(".")[-2:])
        self.allowed_domains = [system_domain]
        self.start_urls = [self.base_url_pattern.format(host=reservation_system_host)]
        self.headers['Host'] = reservation_system_host
        self.additional_ajax_payload = additional_ajax_payload
        self.host = reservation_system_host

    def parse(self, response):
        MongoDriver.delete_all_future_facility_reservations(self.host)
        for i, start_date in enumerate(date_utils.get_weeks_set(self.day_count_to_scrape)):
            url = self.start_urls[0] + "?d={}".format(start_date.strftime('%d.%m.%Y'))
            req = scrapy.Request(
                url,
                callback=self.request_view_state,
                meta={'cookiejar': i},
                headers=self.headers
            )
            yield req

    def request_view_state(self, response):
        original_request_url = response.request.meta['redirect_urls'][0]
        url = self.start_urls[0] + '?d=' + original_request_url.split('=')[-1]
        req = scrapy.Request(
            url,
            callback=self.request_weeks,
            headers=self.headers,
            dont_filter=True,
            meta={'cookiejar': response.meta['cookiejar']}
        )
        yield req

    def request_weeks(self, response):
        view_state = str(response.xpath('//input[@id="javax.faces.ViewState"]/@value').extract_first())

        payload = {
            "AJAXREQUEST": 'scheduleNavigForm:schedule-navig-region',
            "scheduleNavigForm:j_id212": "scheduleNavigForm:j_id212",
            "scheduleNavigForm:view_filter_menu": 'horizontal_service_dayand6days',
            "scheduleNavigForm_SUBMIT": '1',
            "javax.faces.ViewState": view_state,
            "scheduleNavigForm:schedule_calendarInputCurrentDate": '{dt.month}/{dt.year}'.format(dt=datetime.datetime.now()),
            "scheduleNavigForm:schedule_calendarInputDate": response.request.url.split('=')[-1]
        }

        payload.update(self.additional_ajax_payload)

        self.headers['Referer'] = self.start_urls[0]

        req = scrapy.Request(
            self.start_urls[0],
            self.parse_week,
            method="POST",
            body=urllib.parse.urlencode(payload),
            headers=self.headers,
            dont_filter=True,
            meta={
                'cookiejar': response.meta['cookiejar'],
                'dont_redirect': False
            },
        )
        jsession = str(response.request.headers['Cookie']).split('=')[-1]

        req.cookies['__utma'] = '245080538.4863447.1457455890.1457455890.1457455890.1'
        req.cookies['__utmb'] = '245080538.1.10.1457455890'
        req.cookies['__utmc'] = '245080538'
        req.cookies['__utmz'] = '245080538.1457455890.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
        req.cookies['__utmt'] = '1'
        req.cookies['JSESSIONID'] = jsession
        yield req

    def parse_week(self, response):
        xml_resp = HtmlXPathSelector(response)
        schedule_data = xml_resp.xpath('//script[contains(text(),"scheduleData")]//text()').extract_first()[19:-4]
        data = json.loads(schedule_data)
        str_base_date = self.calendar_input_day_pattern.search(urllib.parse.unquote(str(response.request.body))).group(1)
        # str_base_date = urllib.parse.unquote(str(response.request.body)).split('calendarInputDate=')[1].split("'", 1)[0]
        base_date = datetime.datetime.strptime(str_base_date, '%d.%m.%Y')
        for e in data['events']:
            ev_date = base_date + datetime.timedelta(days=e['gridId'])
            rows = e['end'][1] - e['start'][1]
            for court_num in range(1, rows + 1):
                start_time = ev_date + datetime.timedelta(hours=e['start'][0])
                end_time = ev_date + datetime.timedelta(hours=e['end'][0])
                item = ReservationScraperItem()
                item['start_time'] = start_time
                item['end_time'] = end_time
                item['court_id'] = court_num
                item['facility_id'] = self.host
                yield item
