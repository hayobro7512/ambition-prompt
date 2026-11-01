# Feature flags: notes

Context: 45 engineers. Today we turn features on and off with environment variables and a redeploy. Three teams (18 engineers) want flags now; the rest may follow next year.

## Source 1: FlagPilot pricing page (vendor)
- Team plan: $20 per seat per month. On/off flags, percentage rollouts, web UI.
- Enterprise plan: $45 per seat per month. Adds SSO, audit log of every flag change, EU data residency.
- "A seat is any user who can view or change flags." Annual billing.

## Source 2: Slack message from Tom (staff engineer)
"Honestly we could build this in two weeks, one engineer. A table in Postgres, an admin endpoint, and a client that polls every 30s. On/off flags only to start."

## Source 3: Blog post, "How we saved $100k by building our own flags" (2025)
Written by a company with about 400 engineers. They built flags in-house over a quarter with two engineers and say the vendor would have cost them over $100k a year.

## Source 4: Note from our security lead
- Our SOC 2 audit is in March. Any system that changes production behavior needs an audit log of who changed what and when.
- Our EU customer contracts require their data to be processed in the EU. Flags are evaluated with user IDs and account country, so this applies.

## Source 5: Incident review, September
A bad release broke checkout for EU customers. Rolling back by redeploy took 50 minutes; a kill switch would have taken about 2 minutes. We paid about $18,000 in SLA credits.

## Other numbers
- Loaded cost of an engineer: about $200,000 a year.
- Our past internal tools have needed about 10% of an engineer's time each year to maintain.
