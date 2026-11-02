# Writes handle.csv and prints the numbers behind truth.md. Fixed rows, no randomness.
import csv

ROWS = [  # agent, type, tickets, total minutes, reopened
    ("Maya", "password", 60, 361, 2), ("Maya", "billing", 90, 1442, 5), ("Maya", "integration", 250, 11498, 20),
    ("Jonas", "password", 300, 2403, 15), ("Jonas", "billing", 120, 2277, 8), ("Jonas", "integration", 30, 1742, 4),
    ("Priti", "password", 260, 1948, 10), ("Priti", "billing", 140, 3362, 31), ("Priti", "integration", 50, 2598, 5),
    ("Theo", "password", 18, 127, 1), ("Theo", "billing", 6, 121, 1),
]
with open("handle.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["agent", "ticket_type", "tickets", "total_handle_minutes", "reopened"])
    w.writerows(ROWS)

agents = sorted({r[0] for r in ROWS})
types = ["password", "billing", "integration"]
mix = {t: sum(r[2] for r in ROWS if r[1] == t) for t in types}
print("mix", mix, sum(mix.values()))
for a in agents:
    rows = [r for r in ROWS if r[0] == a]
    n, m, ro = (sum(r[i] for r in rows) for i in (2, 3, 4))
    by = {r[1]: r for r in rows}
    per = {t: round(by[t][3] / by[t][2], 1) for t in by}
    reopen = {t: round(100 * by[t][4] / by[t][2], 1) for t in by}
    std = sum(mix[t] * by[t][3] / by[t][2] for t in types) / sum(mix.values()) if len(by) == 3 else None
    print(a, "n", n, "overall", round(m / n, 2), "per", per, "reopen%", reopen, "standardized", std and round(std, 2))
