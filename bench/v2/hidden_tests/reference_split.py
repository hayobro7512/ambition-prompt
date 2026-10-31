from fractions import Fraction


def split_bill(items, tax, tip_percent):
    if not items:
        return {}
    everyone = sorted({p for it in items for p in (it.get("shared_by") or [])})
    sub = {p: Fraction(0) for p in everyone}
    for it in items:
        people = list(it.get("shared_by") or []) or everyone
        if not people:
            continue
        cost = Fraction(str(it["price"])) * int(it.get("qty", 1))
        for p in people:
            sub[p] = sub.get(p, Fraction(0)) + cost / len(people)
    subtotal = sum(sub.values())
    total = subtotal + Fraction(str(tax)) + subtotal * Fraction(str(tip_percent)) / 100
    total_cents = int((total * 100 + Fraction(1, 2)) // 1)
    if subtotal == 0:
        exact = {p: Fraction(total_cents, len(sub)) for p in sub}
    else:
        exact = {p: s / subtotal * total_cents for p, s in sub.items()}
    floor = {p: int(v // 1) for p, v in exact.items()}
    left = total_cents - sum(floor.values())
    for p in sorted(exact, key=lambda p: (-(exact[p] - floor[p]), p))[:left]:
        floor[p] += 1
    return {p: c / 100 for p, c in floor.items()}
