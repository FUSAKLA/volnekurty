# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 20:33:06 2016

@author: FUSAKLA
"""

import urllib2
import urllib

from reservation_scraper import spiders


for spider in spiders.__all__:
    if spider != '__init__':
        url = 'http://localhost:6800/schedule.json'
        values = {
            'project': 'reservation_scraper',
            'spider': spider
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        resp = urllib2.urlopen(req)
        print(resp.read())


