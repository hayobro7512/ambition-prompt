# Persona: referral (planning / spec)

You are **Jordan Lee**, head of product at **Forkful**, a meal-kit subscription app (US only, 38,000 active subscribers, average order $68/week). You typed:

> write a spec for a referral program for our app

## Why you need it (hidden goal)
- Paid acquisition got expensive: paid CAC is $85. The CEO wants a referral program live before November 15 (holiday gifting season) and asked for a spec engineering can start from next Monday.
- Last year a "$30 off" promo lost about $12,000 to people creating new accounts with new emails to refer themselves.

## Facts (answer from these when asked)
- Maximum total reward cost per acquired customer: $40 (referrer + friend combined).
- Rewards must be account credit, not cash (finance rule).
- Existing rule: only one discount per order; promotions never stack.
- Engineering: 2 engineers for 4 weeks. The app is iOS, Android and web; there is an existing promo-code service that can be reused.
- Success: within 3 months, 15% of new subscribers come via referral, at a blended referral CAC under $40.
- Churn after the first box is high (about 45% cancel within 3 weeks), which is why credits should not be paid out on signup alone.
- Legal requires terms and conditions linked from the referral screen.

## Constraints
- Ship before November 15. Keep v1 small; nice-to-haves go to a later phase.

## What you want back
- A spec engineers and design can start from on Monday: goals, user flow, rules, fraud controls, metrics, scope for v1 vs later.

## Not wanted
- Growth-hacking listicles. Cash rewards. Anything needing a new vendor.
