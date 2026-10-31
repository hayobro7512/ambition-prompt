# Hidden tests for split_bill. The module under test is imported as `sol`.
import copy, time
from fractions import Fraction
import solution as sol

f = sol.split_bill


def cents(d):
    return {k: round(v * 100) for k, v in d.items()}


def test_empty():
    assert f([], 0, 0) == {}


def test_single_person():
    assert cents(f([{"name": "a", "price": 10, "shared_by": ["ana"]}], 1, 20)) == {"ana": 1300}


def test_even_split_no_tax():
    assert cents(f([{"name": "p", "price": 20, "shared_by": ["ana", "ben"]}], 0, 0)) == {"ana": 1000, "ben": 1000}


def test_sums_exactly_to_total():
    items = [{"name": "x", "price": 10, "shared_by": ["a", "b", "c"]}, {"name": "y", "price": 7.33, "shared_by": ["b"]}]
    out = cents(f(items, 1.57, 18))
    sub = Fraction("10") + Fraction("7.33")
    total = sub + Fraction("1.57") + sub * Fraction(18, 100)
    assert sum(out.values()) == int((total * 100 + Fraction(1, 2)) // 1)


def test_tax_is_amount_proportional():
    items = [{"name": "x", "price": 30, "shared_by": ["a"]}, {"name": "y", "price": 10, "shared_by": ["b"]}]
    assert cents(f(items, 4, 0)) == {"a": 3300, "b": 1100}


def test_tip_on_pretax_subtotal():
    items = [{"name": "x", "price": 50, "shared_by": ["a"]}, {"name": "y", "price": 50, "shared_by": ["b"]}]
    assert cents(f(items, 10, 20)) == {"a": 6500, "b": 6500}


def test_leftover_cent_largest_remainder_then_alpha():
    assert cents(f([{"name": "x", "price": 10, "shared_by": ["cy", "al", "bo"]}], 0, 0)) == {"al": 334, "bo": 333, "cy": 333}


def test_empty_shared_by_means_everyone():
    items = [{"name": "x", "price": 10, "shared_by": ["a"]}, {"name": "y", "price": 10, "shared_by": ["b"]},
             {"name": "water", "price": 6, "shared_by": []}]
    assert cents(f(items, 0, 0)) == {"a": 1300, "b": 1300}


def test_missing_shared_by_means_everyone():
    items = [{"name": "x", "price": 4, "shared_by": ["a", "b"]}, {"name": "bread", "price": 2}]
    assert cents(f(items, 0, 0)) == {"a": 300, "b": 300}


def test_string_prices():
    assert cents(f([{"name": "x", "price": "18.50", "shared_by": ["a", "b"]}], "0", 0)) == {"a": 925, "b": 925}


def test_qty():
    assert cents(f([{"name": "beer", "price": 6, "qty": 3, "shared_by": ["a"]}], 0, 0)) == {"a": 1800}


def test_discount_shared():
    items = [{"name": "x", "price": 20, "shared_by": ["a", "b"]}, {"name": "promo", "price": -4, "shared_by": ["a", "b"]}]
    assert cents(f(items, 0, 0)) == {"a": 800, "b": 800}


def test_no_float_drift():
    items = [{"name": str(i), "price": 0.1, "shared_by": ["a"]} for i in range(30)]
    assert cents(f(items, 0, 0)) == {"a": 300}


def test_zero_price_person_present():
    items = [{"name": "x", "price": 10, "shared_by": ["a"]}, {"name": "tap water", "price": 0, "shared_by": ["z"]}]
    out = cents(f(items, 0, 0))
    assert out == {"a": 1000, "z": 0}


def test_total_rounds_half_up():
    out = cents(f([{"name": "x", "price": "0.05", "shared_by": ["a"]}], 0, 10))  # 0.055 -> 0.06
    assert out == {"a": 6}


def test_input_not_mutated():
    items = [{"name": "x", "price": "5", "shared_by": ["b", "a"]}, {"name": "y", "price": 3}]
    before = copy.deepcopy(items)
    f(items, 1, 15)
    assert items == before


def test_returns_rounded_floats():
    out = f([{"name": "x", "price": 10, "shared_by": ["a", "b", "c"]}], 0.99, 17)
    assert all(isinstance(v, float) and abs(v * 100 - round(v * 100)) < 1e-6 for v in out.values())


def test_matches_reference_random():
    import random
    import reference_split as ref
    rng = random.Random(3)
    names = ["ana", "ben", "cy", "di", "ed"]
    for _ in range(40):
        items = [{"name": f"i{k}", "price": round(rng.uniform(-3, 40), 2), "qty": rng.randint(1, 3),
                  "shared_by": rng.sample(names, rng.randint(1, 4))} for k in range(rng.randint(1, 8))]
        if sum(i["price"] * i["qty"] for i in items) <= 0:
            continue
        tax, tip = round(rng.uniform(0, 9), 2), rng.choice([0, 15, 18, 20, 22.5])
        assert cents(f(items, tax, tip)) == cents(ref.split_bill(items, tax, tip))


def test_performance():
    items = [{"name": str(i), "price": 9.99, "shared_by": [f"p{j}" for j in range(i % 7 + 1)]} for i in range(5000)]
    t = time.time()
    f(items, 250, 18)
    assert time.time() - t < 2
