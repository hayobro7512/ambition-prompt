import re
from datetime import date, datetime


def _day(x):
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    if isinstance(x, str):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", x):
            raise ValueError(f"not YYYY-MM-DD: {x!r}")
        return date.fromisoformat(x)
    raise TypeError(f"not a date: {x!r}")


def _weekdays_upto(d):  # weekdays in ordinals 1..n; ordinal 1 is a Monday
    w, r = divmod(d.toordinal(), 7)
    return 5 * w + min(r, 5)


def business_days(start, end, holidays=()):
    s, e = _day(start), _day(end)
    if e < s:
        return -business_days(e, s, holidays)
    hol = {_day(h) for h in holidays}
    return _weekdays_upto(e) - _weekdays_upto(s) - sum(1 for h in hol if s < h <= e and h.weekday() < 5)
