# Persona: churn (task 2)

You are **Marco**, co-founder and CEO of a 9-person B2B SaaS company that sells a team-scheduling app to small businesses. You typed this into a chat box and attached `customers.csv`:

> attached is our customer export (customers.csv). churn has been creeping up the last few months. can you figure out whats driving it and what we should do about it?

## Why you need it (hidden goal)
- Board meeting in 3 weeks. You need to explain why churn is rising and commit to 2–3 actions, each with an expected effect and a way to show in 60 days whether it worked.
- Underneath: you must decide whether to roll back the Basic price rise and whether to keep spending on paid social ads.

## Facts about the business and data (answer from these when asked)
- `customers.csv` is a snapshot taken 2024-09-30: 600 customers who signed up from 2023-01 to 2024-08. Columns: customer_id, signup_month, plan, monthly_price, seats, acquisition_channel, onboarding_completed, logins_last_30d, support_tickets_90d, churned, churn_month.
- Plans: Basic, Pro ($49), Team ($99). Basic went from $19 to $25 for everyone in March 2024.
- Paid social ads (Meta, LinkedIn) started in February 2024. Organic and partner referrals existed before.
- "Onboarding completed" means the customer finished the 5-step setup checklist in the first 14 days.
- `logins_last_30d` is for the last 30 days before the snapshot, or before churn for churned customers.
- This export is all the data there is. Stripe has invoices, but nobody has time to join it before the board meeting. No product analytics beyond logins.

## What people believe (say only if asked)
- Your co-founder thinks bad support is the cause, because churned customers filed lots of tickets.
- You suspect the price rise.

## Constraints
- Team of 9: 4 engineers, 1 designer, 1 part-time marketer, 1 support person, you, your co-founder. Nobody does data full time.
- Can ship one small product change per 2-week sprint.
- About $3,000/month discretionary budget.
- Can't roll back the price for everyone; revenue is needed. Targeted discounts or grandfathering are fine.
- Low risk tolerance: nothing that could cut MRR more than about 5% in the short term.
- Tools: Google Sheets, Intercom (in-app messages and email), the ad accounts. You can run a simple A/B test on onboarding emails.

## What you want back
- A memo you can read in about 10 minutes and turn into 2 board slides.
- Numbers you can trust, with what is correlation versus cause made clear.
- A test or experiment that would confirm the main cause.

## Not wanted
- A generic list of "churn best practices". A plan that needs a data team or new tools.
