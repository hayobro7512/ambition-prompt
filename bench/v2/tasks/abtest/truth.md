# Answer key (judge only; computed by make_data.py, 56 data rows)

Totals (visitors, orders, conversion, AOV, revenue/visitor):
- All: A 36,685 / 1,400 / 3.82% / $62.20 / $2.374; B 39,072 / 1,621 / 4.15% / $57.42 / $2.382.
- Desktop: A 15,622 / 809 / 5.18% / $68.31 / $3.538; B 18,040 / 938 / 5.20% / $62.98 / $3.275.
- Mobile: A 21,063 / 591 / 2.81% / $53.83 / $1.510; B 21,032 / 683 / 3.25% / $49.78 / $1.617.
- Mobile days 1-7: A 2.79% vs B 3.47% (rev/visitor 1.501 vs 1.723). Mobile days 8-14: A 2.82% vs B 3.02% (1.520 vs 1.511).
- Desktop days 8-14 visitors: A 7,773 vs B 10,334.

Key findings a strong answer reaches:
1. Sample ratio mismatch: B got 51.6% of visitors overall, and on desktop days 8-14 B got 57%. Assignment is broken from about day 8, so the pooled result is not a clean test.
2. The headline conversion lift (3.82% -> 4.15%) is inflated by B's extra desktop traffic, which converts higher (a mix effect).
3. B's average order value is about 7-8% lower on both devices, so revenue per visitor is flat overall ($2.37 vs $2.38) and down about 7% on desktop.
4. On mobile B converts better, but the lift decays from about +24% in week 1 to about +7% in week 2, with revenue per visitor flat in week 2: likely a novelty effect.
5. Recommendation: do not ship on the pooled number. Fix assignment and rerun (or analyze only clean traffic), make revenue per visitor the primary metric, and consider a mobile-only follow-up with an AOV guardrail.

Wrong or weak: declaring B the winner from pooled conversion; ignoring AOV/revenue; missing the traffic imbalance; inventing p-values not derivable from the data.
