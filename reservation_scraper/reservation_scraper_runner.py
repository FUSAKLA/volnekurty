# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 20:33:06 2016

@author: FUSAKLA
"""

from scrapy.utils.project import get_project_settings
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler


SPIDERS = [
    kuklenska.KuklenskaSpider,
    badmintonlisen.LisenSpider,
    classic.ClassicSpider,
    fit4all.Fit4AllSpider,
    ivanovice.IvanoviceSpider,
    jehnice.JehniceSpider,
    sprint.SprintSpider,
    zidenice.ZideniceSpider
]


class CrawlRunner:
    def __init__(self):
        self.running_crawlers = []

    def spider_closing(self, spider):
        log.msg("Spider closed: %s" % spider, level=log.INFO)
        self.running_crawlers.remove(spider)
        if not self.running_crawlers:
            reactor.stop()

    def run(self):
        settings = get_project_settings()
        for spider in SPIDERS:
            sp =
            crawler = Crawler(spider)
            crawler_obj = spider()
            self.running_crawlers.append(sp)

            crawler.signals.connect(self.spider_closing, signal=signals.spider_closed)
            crawler.configure()
            crawler.crawl()
            crawler.start()

        reactor.run()


if __name__ == '__main__':
    cr = CrawlRunner()
    cr.run()