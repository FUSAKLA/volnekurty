from datetime import date, time
import re


MONTH_NAMES = ["leden", "únor", "březen", "duben", "květen", "červen",
               "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]


def month_name_to_date(month_name):
    return date(
        year=date.today().year,
        month=MONTH_NAMES.index(month_name) + 1,
        day=1
    )


def time_from_text(time_text):
    hours = 0
    minutes = 0
    patt = re.compile(r"([0-9]{1,2})([\s:\.\-]{1,3}[0-9]{1,2})?")
    min_patt = re.compile(r"^.*([0-9]{1,2})$")

    res = patt.search(time_text)
    if res:
        hours = int(res.group(1))
        if res.group(2):
            minutes = int(min_patt.search(res.group(2)).group(1))
    return time(hour=hours, minute=minutes)