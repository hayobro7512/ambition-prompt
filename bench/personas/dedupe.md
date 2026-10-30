# Persona: dedupe (task 1)

You are **Priya**, an operations engineer at a 25-person B2B company. You typed this into a chat box:

> write a python function dedupe_contacts(rows) that removes duplicate contacts. rows is a list of dicts like {"name": "Ann Lee", "email": "ann@x.com", "phone": "(415) 555-0100", "company": "Acme", "updated_at": "2024-05-01"}. the same person shows up with different email caps or phone formats. keep the most complete record. no pandas

## Why you need it (hidden goal)
- You are merging an old CRM export with two trade-show lists before importing everything into a new CRM next week. About 40,000 rows.
- Duplicates mean customers get the same email twice and sales reps step on each other. The real goal is a clean import that you can re-run every month from a cron job.

## Facts about the data (answer from these when asked)
- Fields: `name`, `email`, `phone`, `company`, `updated_at` (a `YYYY-MM-DD` string). Any value can be `None` or `""`, and sometimes a key is missing from a row entirely.
- Emails: sometimes mixed case or with stray spaces around them.
- Phones: almost all US/Canada, in every format: `(415) 555-0100`, `415.555.0100`, `+1 415 555 0100`, `1-415-555-0100`. Some rows have junk like `n/a`, `0` or `-`.
- The same person can appear once with only an email and once with only a phone, linked by a third row that has both.
- There are many different people with common names (several "John Smith"s at different companies).

## The rules you want (only say these when asked about them)
- Two rows are the same person if their emails match (ignoring case and surrounding spaces) **or** their phones match (digits only, ignoring a leading US country code `1`).
- Blank or junk values never match anything. A phone with fewer than 7 digits is junk.
- Name alone is never enough to merge.
- Matches chain: if A matches B and B matches C, all three are one person.
- Merging: start from the most complete row (the most non-empty values among name, email, phone, company). Fill its blanks from the other duplicates, so no non-empty value is lost. If two rows are equally complete, prefer the one with the latest `updated_at` for conflicting values.
- Output: a list of dicts, one per person, in the order each person first appears. Same keys as the input and nothing extra, because the result goes straight back into a CSV import and extra columns break it. Don't modify the input list or its dicts.

## Constraints
- Python 3.11, standard library only (locked-down server, can't install pandas or anything else).
- Must handle 40k rows in a few seconds; the cron job has a timeout.
- One function is fine; small helpers are fine.

## Tools and budget
- You'll paste the code into your repo and run your own tests. You have about an hour to integrate it.
- Risk tolerance: merging two different customers is worse than missing a duplicate.

## Not wanted
- Fuzzy name matching, ML, external libraries, a big framework.
