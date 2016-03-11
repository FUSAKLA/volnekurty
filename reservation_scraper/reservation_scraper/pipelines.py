# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 19:05:38 2016

@author: FUSAKLA
"""

from reservation_scraper.items import ReservationScraperItem
from reservation_scraper.db_worker import db_worker


class ReservationScraperPipeline(object):
    def process_item(self, item, spider):
        db_worker.insert_reservation_item(item)
        return item

    def __del__(self):
        self.conn.close()
