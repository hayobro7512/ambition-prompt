"""Generates activation.csv (seed 11). Story: activation rises every spring; the March 2026 email
sequence adds only ~0.5 points; the August 2026 row is incomplete (export ran before the 7-day window closed)."""
import csv
import random
from math import sqrt

rng = random.Random(11)
SEASON = {1: .300, 2: .310, 3: .350, 4: .360, 5: .360, 6: .350, 7: .330, 8: .330, 9: .330, 10: .320, 11: .300, 12: .290}
rows = []
for i in range(26):  # 2024-07 .. 2026-08
    y, m = 2024 + (6 + i) // 12, (6 + i) % 12 + 1
    p = SEASON[m] + 0.008 * (i / 12) + (0.005 if (y, m) >= (2026, 3) else 0)
    n = rng.randint(3800, 4400)
    act = sum(rng.random() < p for _ in range(n))
    if (y, m) == (2026, 8):
        act = round(act * 24 / 31)  # signups from Aug 25-31 have not had 7 days yet
    rows.append((f"{y}-{m:02d}", n, act))
with open("activation.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["month", "signups", "activated_within_7d"])
    w.writerows(rows)


def rate(months):
    s = [r for r in rows if r[0] in months]
    return sum(r[2] for r in s) / sum(r[1] for r in s), sum(r[1] for r in s)


pre26, n1 = rate({"2025-11", "2025-12", "2026-01", "2026-02"})
post26, n2 = rate({"2026-03", "2026-04", "2026-05", "2026-06"})
pre25, n3 = rate({"2024-11", "2024-12", "2025-01", "2025-02"})
post25, n4 = rate({"2025-03", "2025-04", "2025-05", "2025-06"})
did = (post26 - pre26) - (post25 - pre25)
se = sqrt(sum(p * (1 - p) / n for p, n in [(pre26, n1), (post26, n2), (pre25, n3), (post25, n4)]))
print(f"Nov-Feb 25/26 {pre26:.2%} -> Mar-Jun 26 {post26:.2%}: {100 * (post26 - pre26):+.2f} pts")
print(f"Nov-Feb 24/25 {pre25:.2%} -> Mar-Jun 25 {post25:.2%}: {100 * (post25 - pre25):+.2f} pts")
print(f"YoY Mar-Jun: {100 * (post26 - post25):+.2f} pts; diff-in-diff {100 * did:+.2f} pts, SE {100 * se:.2f}")
aug = [r for r in rows if r[0] == "2026-08"][0]
jul = [r for r in rows if r[0] == "2026-07"][0]
print(f"Jul 2026 {jul[2] / jul[1]:.2%}; Aug 2026 as exported {aug[2] / aug[1]:.2%}")
