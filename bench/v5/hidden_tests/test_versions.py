# Hidden tests for compare_versions. The module under test is imported as `sol`.
import solution as sol


def cv(a, b):
    return sol.compare_versions(a, b)


def raises(exc, *a):
    try:
        cv(*a)
    except exc:
        return True
    except Exception:
        return False
    return False


def test_basic_three_way():
    assert cv("1.2.3", "1.2.4") == -1 and cv("1.2.4", "1.2.3") == 1 and cv("1.2.3", "1.2.3") == 0


def test_numeric_not_string_order():
    assert cv("1.10.0", "1.9.0") == 1 and cv("2.0.0", "10.0.0") == -1


def test_missing_parts_are_zero():
    assert cv("1.2", "1.2.0") == 0 and cv("1", "1.0.0") == 0 and cv("1.2", "1.2.1") == -1


def test_more_than_three_parts():
    assert cv("1.2.3.4", "1.2.3") == 1 and cv("1.2.3.0", "1.2.3") == 0 and cv("1.2.3.0.0", "1.2.3.0") == 0


def test_leading_zeros():
    assert cv("1.02.0", "1.2.0") == 0 and cv("01.2", "1.2") == 0


def test_v_prefix_and_whitespace():
    assert cv("v1.2.3", "1.2.3") == 0 and cv("V1.2.3", "v1.2.3") == 0 and cv("  1.2.3\n", "1.2.3") == 0


def test_prerelease_older_than_release():
    assert cv("1.2.0-rc.1", "1.2.0") == -1 and cv("1.2.0", "1.2.0-rc.1") == 1


def test_prerelease_vs_lower_release():
    assert cv("1.2.0-rc.1", "1.1.9") == 1


def test_semver_precedence_chain():
    chain = ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-beta", "1.0.0-beta.2",
             "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0"]
    for x, y in zip(chain, chain[1:]):
        assert cv(x, y) == -1 and cv(y, x) == 1


def test_numeric_identifier_lower_than_alpha():
    assert cv("1.0.0-1", "1.0.0-a") == -1 and cv("1.0.0-999", "1.0.0-a") == -1


def test_ascii_order_in_prerelease():
    assert cv("1.0.0-RC", "1.0.0-alpha") == -1


def test_hyphen_inside_identifier():
    assert cv("1.0.0-rc-1", "1.0.0-rc-1") == 0 and cv("1.0.0-rc-1", "1.0.0") == -1 and cv("1.0.0-a-b", "1.0.0-a") == 1


def test_prerelease_on_short_release():
    assert cv("1.2-rc.1", "1.2.0-rc.1") == 0


def test_build_metadata_ignored():
    assert cv("1.0.0+a", "1.0.0+b") == 0 and cv("1.0.0+a", "1.0.0") == 0 and cv("1.0.0-rc.1+x", "1.0.0-rc.1+y") == 0


def test_hyphen_in_build_is_not_prerelease():
    assert cv("1.0.0+build-5", "1.0.0") == 0


def test_returns_exact_ints():
    for got in (cv("1", "2"), cv("2", "1"), cv("1", "1")):
        assert type(got) is int and got in (-1, 0, 1)


def test_big_numbers():
    assert cv("1.0.99999999999999999999", "1.0.99999999999999999998") == 1


def test_malformed_release_raises():
    for bad in ["", "   ", "abc", "1..2", "1.2.", ".1", "1.a", "v", "-1.2"]:
        assert raises(ValueError, bad, "1.0.0"), bad
        assert raises(ValueError, "1.0.0", bad), bad


def test_malformed_suffix_raises():
    for bad in ["1.2-", "1.2-rc..1", "1.2+", "1.2-rc.", "1.2-rc_1"]:
        assert raises(ValueError, bad, "1.0.0"), bad


def test_non_strings_raise_type_error():
    for bad in [None, 1.2, 3, ["1.2"]]:
        assert raises(TypeError, bad, "1.0.0"), bad
        assert raises(TypeError, "1.0.0", bad), bad
