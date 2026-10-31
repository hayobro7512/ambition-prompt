# Deterministic A/B export: 14 days x 2 devices x 2 variants. Story (judge-only, see truth.md):
# days 8-14 an assignment bug sends extra desktop traffic to B (sample ratio mismatch);
# mobile: B converts better but the lift decays; desktop: B ~= A; B's average order value is lower.
import csv, random
rng = random.Random(42)
rows = []
for d in range(1, 15):
    date = f"2024-09-{d:02d}"
    for device in ("desktop", "mobile"):
        for v in ("A", "B"):
            base = 1100 if device == "desktop" else 1500
            visitors = base + rng.randint(-60, 60)
            if v == "B" and device == "desktop" and d >= 8:
                visitors = int(visitors * 1.35)
            if device == "desktop":
                cr = 0.052
            else:
                cr = 0.028 if v == "A" else 0.028 * (1 + max(0.04, 0.30 - 0.025 * (d - 1)))
            orders = round(visitors * cr * (1 + rng.uniform(-0.06, 0.06)))
            aov = (68 if device == "desktop" else 54) * (0.93 if v == "B" else 1.0)
            revenue = round(orders * aov * (1 + rng.uniform(-0.03, 0.03)), 2)
            rows.append([date, device, v, visitors, orders, f"{revenue:.2f}"])
with open("ab_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "device", "variant", "visitors", "orders", "revenue"])
    w.writerows(rows)
