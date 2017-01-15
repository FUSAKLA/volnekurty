from datetime import datetime, timedelta
from math import ceil


def get_days_set(day_count=1):
    return [get_today_date() + timedelta(days=x) for x in range(day_count)]


def get_weeks_set(day_count=1):
    return [get_today_date() + timedelta(days=x) for x in range(0, ceil(day_count/7), 7)]


def get_today_date():
    return datetime.today().replace(hour=0, minute=0)