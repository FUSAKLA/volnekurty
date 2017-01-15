import scrapy


class FacilityInformationScraperItem(scrapy.Item):
    name = scrapy.Field()
    hostname = scrapy.Field()
    address = scrapy.Field()
    email = scrapy.Field()
    opening_hours = scrapy.Field()
    position = scrapy.Field()
    telephone = scrapy.Field()
    prices = scrapy.Field()

