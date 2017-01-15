import datetime

import scrapy
from reservation_scraper.items import ReservationScraperItem
from reservation_scraper.db_driver.mongo import MongoDriver
from reservation_scraper.utils import date_utils
from config import config


class Fit4AllSpider(scrapy.Spider):
    name = "fit4all"
    host = "fit4all.cz"

    allowed_domains = [host]

    day_count_to_scrape = int(config["TimeInterval"]["DayCountToScrape"])

    reservation_length = 30
    start_urls = [
        'http://www.fit4all.cz/cs/online-rezervace?id_sportoviste=6&id_instruktora=-1&id_typ_lekce=-1&datum='
    ]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'cs,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.fit4all.cz',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
    }

    def start_requests(self):
        MongoDriver.delete_all_future_facility_reservations(self.host)
        for d in date_utils.get_days_set(self.day_count_to_scrape):
            url = self.start_urls[0] + d.strftime('%d.%m.%Y')
            yield scrapy.Request(url, callback=self.parse_day, headers=self.headers)

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
                        end_time = start_time + datetime.timedelta(minutes=self.reservation_length)
                        item = ReservationScraperItem()
                        item['start_time'] = start_time
                        item['end_time'] = end_time
                        item['court_id'] = c_num + 1
                        item['facility_id'] = self.host
                        item['html_id'] = ""
                        yield item

