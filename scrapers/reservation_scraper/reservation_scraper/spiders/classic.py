import datetime

import scrapy
from reservation_scraper.items import ReservationScraperItem
from reservation_scraper.db_driver.mongo import MongoDriver
from reservation_scraper.utils import date_utils
from config import config


class ClassicSpider(scrapy.Spider):
    name = "classic"
    host = 'clubclassic.cz'

    allowed_domains = [host]

    day_count_to_scrape = int(config["TimeInterval"]["DayCountToScrape"])

    start_urls = [
        "http://rezervace.clubclassic.cz/index.php?page=day_overview&id=29"
    ]
    headers = {
        'Host': 'www.clubclassic.cz'
    }

    def parse(self, response):
        MongoDriver.delete_all_future_facility_reservations(self.host)
        for d in date_utils.get_days_set(self.day_count_to_scrape):
            url = response.urljoin('?page=day_overview&id=29&date=' + str(d.date()))
            yield scrapy.Request(url, callback=self.parse_day)

    def parse_day(self, response):
        act_date = datetime.datetime.strptime(response.url.split('=')[-1], '%Y-%m-%d')
        rows = response.xpath('//table[@class="btable denni-prehled"]//tr[@class="rows"]')
        for r in rows:
            time_cell = r.xpath('th/text()')
            start_datetime, end_datetime = self.get_border_times(act_date, time_cell.extract_first())
            cells = r.xpath('td')
            for c_num, c in enumerate(cells):
                if c.xpath('@class').extract_first() == 'obsazeno':
                    item = ReservationScraperItem()
                    item['start_time'] = start_datetime
                    item['end_time'] = end_datetime
                    item['court_id'] = c_num + 1
                    item['facility_id'] = self.host
                    item['html_id'] = ''
                    yield item

    @staticmethod
    def get_border_times(act_date, time_string):
        start, end = [x.strip() for x in time_string.split('-')]
        start_hour, start_minute = [int(x) for x in start.split(':')]
        end_hour, end_minute = [int(x) for x in end.split(':')]
        start_datetime = act_date.replace(hour=start_hour, minute=start_minute)
        end_datetime = act_date.replace(hour=end_hour, minute=end_minute)
        return start_datetime, end_datetime

