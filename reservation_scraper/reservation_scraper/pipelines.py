# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 19:05:38 2016

@author: FUSAKLA
"""

import psycopg2
from reservation_scraper.items   import ReservationScraperItem
 
 
class ReservationScraperPipeline(object):
    def __init__(self):
        self.conn = psycopg2.connect(host='localhost', database='volnekurty', user='postgres', password='Martin39')
        self.cur = self.conn.cursor()
     
    def process_item(self, item, spider):
        try:
            self.cur.execute(
                """INSERT INTO reservation_data.badminton_reservations(
                        fk_sport_center, 
                        court_number, 
                        start_time, 
                        end_time 
                    ) VALUES(%s, %s, %s, %s)
                """, 
                (
                    item.get('fk_sport_center'),
                    item.get('court_number'), 
                    item.get('start_time'), 
                    item.get('end_time')
                )
            )
        except psycopg2.DatabaseError, e:
          print "Error: %s" % e
        self.conn.commit()
        return item
    
    def __del__(self):
        self.conn.close()
        
