"""Deterministic CSAT export for the csat task. Story: overall CSAT falls in weeks 5-8 because chat (lower CSAT)
opened to all customers in week 5 and its share of responses jumps (mix shift). Within each channel CSAT is flat
or improving. Email, where the new hires work, is flat. Week 7 phone has a survey outage (tiny response count)."""
import csv, random
from datetime import date, timedelta

rng = random.Random(42)
rows = []
for week in range(1, 9):
    start = (date(2024, 9, 2) + timedelta(weeks=week - 1)).isoformat()
    for channel, tickets, rate in [
        ("email", rng.randint(610, 660), 0.87),
        ("phone", rng.randint(380, 420), 0.90),
        ("chat", rng.randint(35, 50) if week <= 4 else rng.randint(520, 600), 0.69 if week <= 4 else 0.72),
    ]:
        responses = round(tickets * rng.uniform(0.28, 0.33))
        if channel == "phone" and week == 7:
            responses = 9  # survey tool outage
        satisfied = round(responses * (rate + rng.uniform(-0.015, 0.015)))
        rows.append([start, week, channel, tickets, responses, satisfied])

with open("csat.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["week_start", "week", "channel", "tickets", "csat_responses", "satisfied"])
    w.writerows(rows)


def pct(sel):
    r = sum(x[4] for x in sel)
    return 100 * sum(x[5] for x in sel) / r, r


for label, weeks in [("weeks 1-4", range(1, 5)), ("weeks 5-8", range(5, 9))]:
    sel = [x for x in rows if x[1] in weeks]
    print(label, "overall %.1f%% (n=%d)" % pct(sel),
          {c: "%.1f%%" % pct([x for x in sel if x[2] == c])[0] for c in ("email", "phone", "chat")},
          "chat share of responses %.0f%%" % (100 * sum(x[4] for x in sel if x[2] == "chat") / sum(x[4] for x in sel)))
# counterfactual: weeks 5-8 channel CSAT with weeks 1-4 channel mix
a = [x for x in rows if x[1] <= 4]; b = [x for x in rows if x[1] >= 5]
mix = {c: sum(x[4] for x in a if x[2] == c) / sum(x[4] for x in a) for c in ("email", "phone", "chat")}
print("weeks 5-8 CSAT at weeks 1-4 mix: %.1f%%" % sum(mix[c] * pct([x for x in b if x[2] == c])[0] for c in mix))
print("week 7 phone:", [x for x in rows if x[1] == 7 and x[2] == "phone"])
