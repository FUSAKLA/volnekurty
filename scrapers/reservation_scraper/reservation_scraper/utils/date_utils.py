from datetime import datetime, timedelta, time, date
from math import ceil
import re


def get_days_set(day_count=1):
    return [get_today_date() + timedelta(days=x) for x in range(day_count)]


def get_weeks_set(day_count=1):
    return [get_today_date() + timedelta(days=x) for x in range(0, ceil(day_count/7), 7)]


def get_today_date():
    return datetime.today().replace(hour=0, minute=0)


def time_from_text(time_text):
    hours = 0
    minutes = 0
    patt = re.compile(r"([0-9]{1,2})([\s:\.\-]{1,3}[0-9]{1,2})?")
    min_patt = re.compile(r"^[^0-9]*([0-9]+)$")

    res = patt.search(time_text)
    if res:
        hours = int(res.group(1))
        if res.group(2):
            minutes = int(min_patt.search(res.group(2)).group(1))
    return time(hour=hours, minute=minutes)


def diff_two_time_objects(start_time, end_time):
    diff = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
    return diff