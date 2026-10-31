# Answer key (judge only)

A strong spec (scored against the persona; an arm that never learned a fact should mark it as an open question or assumption, never invent it):
1. Reward structure within $40 total per acquired customer, paid as account credit (for example $20 + $20, or $25 + $15).
2. Rewards trigger only after a qualifying event that beats early churn (for example the friend's first box delivered, or the second paid order), not on signup.
3. Fraud controls against self-referral: matching on payment card, delivery address and/or device, not just email; limits per referrer; manual review queue.
4. No stacking: the referral credit is the one discount on the order, consistent with the existing rule.
5. v1 scope fits 2 engineers x 4 weeks by reusing the promo-code service; clear v1 vs later phases; launch before Nov 15.
6. Metrics and decision rule: share of new subscribers via referral (target 15% in 3 months), referral CAC under $40, fraud rate, and a kill/adjust rule.
7. Covers user flow (invite, share link, friend signup, reward notice), T&C link, edge cases (existing customer referred, cancelled before qualifying).
Weak: cash rewards; payout on signup; rewards above $40; ignoring fraud; scope that obviously exceeds 8 engineer-weeks.
