import scrapy


class ReservationScraperItem(scrapy.Item):
    # define the fields for your item here like:
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    court_id = scrapy.Field()
    facility_id = scrapy.Field()
