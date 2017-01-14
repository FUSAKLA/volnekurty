# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 19:05:38 2016

@author: FUSAKLA
"""

#from reservation_scraper.db_worker import db_worker
from reservation_scraper.db_driver.file_worker import FileWorker


class ReservationScraperPipeline(object):
    @staticmethod
    def process_item(item, spider):
        #db_worker.insert_reservation_item(item)
        FileWorker.insert_reservation_item(item)
        return item

