import re

import scrapy
from facility_information_scraper.items import FacilityInformationScraperItem
from facility_information_scraper.utils import date_utils
from facility_information_scraper.utils import xpath_utils

headers = {
    'Host': 'www.clubclassic.cz'
}


class Fit4AllInformationSpider(scrapy.Spider):
    name = "fit4all"
    hostname = "clubclassic.cz"
    allowed_domains = ['clubclassic.cz']
    start_urls = [
        "http://www.clubclassic.cz/kontakt/"
    ]

    def parse(self, response):
        url = self.start_urls[0]
        yield scrapy.Request(url, callback=self.process_contact_page)

    def process_contact_page(self, response):
        rows = response.xpath('//div[@id="content"]/table//p')
        map_url = response.xpath('///iframe/@src').extract()[0]

        item = FacilityInformationScraperItem()
        item["address"] = self.extract_address(rows[1])
        item["telephone"] = self.extract_telephone_numbers(rows[2])
        item["email"] = self.extract_email(rows[3])
        opening_hours = [
            self.extract_opening_hours(rows[7]),
            self.extract_opening_hours(rows[8])
        ]
        item["opening_hours"] = opening_hours
        item["position"] = self.parse_position(map_url)

        price_req = scrapy.Request("http://www.clubclassic.cz/o-klubu/cenik/", callback=self.process_prices)
        price_req.meta['item'] = item
        yield price_req

    def process_prices(self, response):
        item = response.meta["item"]
        price_lines = response.xpath('//div[@id="content"]/p')
        prices = [
            self.extract_price(price_lines[0]),
            self.extract_price(price_lines[1])
        ]
        item["prices"] = prices
        yield item

    @classmethod
    def extract_price(cls, price_path):
        price_patt = "{text} {link}"
        price_link_patt = '<a href="http://{host}/{href}"> zde </a>'
        price_href = price_path.xpath("a/@href").extract()[0].strip()
        price_text = xpath_utils.extract_string_from_path(price_path).strip()
        return price_patt.format(
            text=price_text,
            link=price_link_patt.format(host=cls.hostname, href=price_href)
        )

    @classmethod
    def extract_email(cls, email_path):
        email_text = xpath_utils.extract_string_from_path(email_path.select("a"))
        return email_text

    @classmethod
    def extract_address(cls, address_path):
        address_text = xpath_utils.extract_string_from_path(address_path)
        return cls.parse_address(address_text)

    @staticmethod
    def parse_address(address_text):
        return address_text.replace("/n", ", ")

    @classmethod
    def extract_opening_hours(cls, opening_hours_path):
        opening_hours_text = xpath_utils.extract_string_from_path(opening_hours_path)
        return cls.parse_opening_hours(opening_hours_text)

    @staticmethod
    def parse_opening_hours(opening_hour_text):
        patt = re.compile(r"^.*\(([^\s\-]+) - ([^\s\-]+)\).*([0-9]{1,2}) - ([0-9]{1,2})")
        res = patt.search(opening_hour_text)
        opening_hours = {
            "season_from": None,
            "season_to": None,
            "open_from": None,
            "open_to": None,
        }
        if res:
            opening_hours["season_from"] = date_utils.month_name_to_date(res.group(1))
            opening_hours["season_to"] = date_utils.month_name_to_date(res.group(2))
            opening_hours["open_from"] = date_utils.time_from_text(res.group(3))
            opening_hours["open_to"] = date_utils.time_from_text(res.group(4))
        return opening_hours

    @classmethod
    def extract_telephone_numbers(cls, telephone_numbers_path):
        telephone_numbers_text = xpath_utils.extract_string_from_path(telephone_numbers_path)
        return cls.parse_telephone_numbers(telephone_numbers_text)

    @staticmethod
    def parse_telephone_numbers(telephone_numbers_text):
        patt = re.compile(r"([0-9\s\+]{11,16})")
        tel_numbers = patt.findall(telephone_numbers_text)
        return [n.strip() for n in tel_numbers]

    @staticmethod
    def parse_position(map_link):
        position = {
            "lat": 0,
            "lon": 0
        }
        patt = re.compile(r"ll=([0-9\.]+),([0-9\.]+)&")
        res = patt.search(map_link)
        if res:
            position["lat"] = float(res.group(1))
            position["lon"] = float(res.group(2))
        return position


