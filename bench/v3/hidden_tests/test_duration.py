# Hidden tests for parse_duration. The module under test is imported as `sol`.
import solution as sol

f = sol.parse_duration


def raises(exc, arg):
    try:
        f(arg)
    except exc:
        return True
    except Exception:
        return False
    return False


def test_basic_combo():
    assert f("1h30m") == 5400


def test_each_unit():
    assert [f("1s"), f("1m"), f("1h"), f("1d")] == [1, 60, 3600, 86400]


def test_weeks():
    assert f("2w") == 1209600


def test_returns_int():
    assert type(f("1.5h")) is int and f("1.5h") == 5400


def test_case_insensitive():
    assert f("1H30M") == 5400


def test_spaces_between_parts():
    assert f(" 1h 30m 5s ") == 5405


def test_any_order():
    assert f("30m1h") == 5400


def test_rounding_half_up():
    assert f("2.5s") == 3 and f("1.4s") == 1


def test_bare_number_is_seconds():
    assert f("90") == 90 and f("90.5") == 91


def test_clock_hms():
    assert f("1:30:00") == 5400


def test_clock_ms():
    assert f("2:05") == 125


def test_clock_field_out_of_range():
    assert raises(ValueError, "1:75") and raises(ValueError, "1:30:75")


def test_zero():
    assert f("0s") == 0


def test_empty_and_blank():
    assert raises(ValueError, "") and raises(ValueError, "   ")


def test_negative():
    assert raises(ValueError, "-5m")


def test_unknown_unit():
    assert raises(ValueError, "5min") and raises(ValueError, "3ms")


def test_repeated_unit():
    assert raises(ValueError, "1h2h")


def test_malformed():
    assert all(raises(ValueError, x) for x in ["h", "1hh", "1.2.3h", "1h30"])


def test_non_string():
    assert raises(TypeError, 90)
