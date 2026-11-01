# Hidden tests for business_days. The module under test is imported as `sol`.
import random
import time
from datetime import date, datetime, timedelta

import solution as sol


def bd(*a, **k):
    return sol.business_days(*a, **k)


def raises(exc, *a):
    try:
        bd(*a)
    except exc:
        return True
    except Exception:
        return False
    return False


def oracle(s, e, hol=()):
    if e < s:
        return -oracle(e, s, hol)
    hol = set(hol)
    return sum(1 for i in range(1, (e - s).days + 1)
               if (d := s + timedelta(i)).weekday() < 5 and d not in hol)


MON, FRI, SAT, SUN = date(2026, 11, 2), date(2026, 11, 6), date(2026, 11, 7), date(2026, 11, 8)


def test_same_day_is_zero():
    assert bd(MON, MON) == 0


def test_start_excluded_end_included():
    assert bd(MON, FRI) == 4


def test_friday_to_monday():
    assert bd(FRI, date(2026, 11, 9)) == 1


def test_weekend_only():
    assert bd(SAT, SUN) == 0
    assert bd(SAT, date(2026, 11, 9)) == 1


def test_full_week():
    assert bd(FRI, date(2026, 11, 13)) == 5


def test_reversed_is_negative():
    assert bd(date(2026, 11, 9), FRI) == -1
    assert bd(FRI, MON) == -4


def test_weekday_holiday_skipped():
    assert bd(date(2026, 11, 23), date(2026, 11, 27), holidays=[date(2026, 11, 26)]) == 3


def test_holiday_on_start_day_not_counted_twice():
    assert bd(date(2026, 11, 26), date(2026, 11, 27), holidays=[date(2026, 11, 26)]) == 1


def test_weekend_holiday_ignored():
    assert bd(FRI, date(2026, 11, 13), holidays=[SAT]) == 5


def test_holiday_strings_and_duplicates():
    assert bd(date(2026, 11, 23), date(2026, 11, 27), holidays=["2026-11-26", date(2026, 11, 26)]) == 3


def test_holiday_outside_range_ignored():
    assert bd(MON, FRI, holidays=[date(2026, 12, 25), date(2026, 1, 1)]) == 4


def test_iso_string_dates():
    assert bd("2026-11-02", "2026-11-06") == 4


def test_datetime_inputs_use_date():
    assert bd(datetime(2026, 11, 2, 23, 59), datetime(2026, 11, 6, 0, 1)) == 4


def test_bad_string_raises_value_error():
    for s in ("2026-13-01", "11/02/2026", "", "20261102"):
        assert raises(ValueError, s, "2026-11-06")


def test_non_date_raises_type_error():
    for x in (None, 20261102):
        assert raises(TypeError, x, MON)


def test_returns_int():
    assert type(bd(MON, FRI)) is int


def test_random_against_oracle():
    rng = random.Random(3)
    for _ in range(300):
        s = date(2026, 1, 1) + timedelta(rng.randint(0, 400))
        e = s + timedelta(rng.randint(-70, 70))
        hol = [date(2026, 1, 1) + timedelta(rng.randint(0, 470)) for _ in range(rng.randint(0, 8))]
        assert bd(s, e, holidays=hol) == oracle(s, e, hol)


def test_long_span_is_fast():
    t = time.perf_counter()
    got = bd(date(1900, 1, 1), date(9999, 12, 31))
    assert time.perf_counter() - t < 0.5
    assert got == 2113189


def test_long_span_with_holidays_is_fast():
    hol = [date(2026, 12, 25) + timedelta(days=365 * k) for k in range(50)]
    t = time.perf_counter()
    got = bd(date(2000, 1, 1), date(2099, 12, 31), holidays=hol)
    assert time.perf_counter() - t < 0.5
    assert got == 26089 - sum(1 for h in hol if h.weekday() < 5)
