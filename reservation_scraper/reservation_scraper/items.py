# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReservationScraperItem(scrapy.Item):
    # define the fields for your item here like:
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    court_number = scrapy.Field()
    reservation_type = scrapy.Field()
