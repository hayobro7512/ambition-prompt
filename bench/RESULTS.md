# Results — run `20261030-run3`

Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here (NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.

Models: optimizer `nvidia/nemotron-3-ultra-550b-a55b`, simulated user `nvidia/nemotron-3.5-lightning-30b-a3b`, executor `nvidia/nemotron-3-ultra-550b-a55b`, judge 1 (primary) `gpt-5.6-sol`, judge 2 `openai/gpt-oss-20b`. Seed 7. n=3 executor samples per arm per task. OpenAI calls used: 32/40.

Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.

## Task: dedupe

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Hidden tests pass rate | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|---|
| A raw prompt | 1.83 ± 0.60 | 0.94 ± 0.48 | +0.28 ± 0.60 / +0.06 ± 0.58 | 73% ± 13% | 4099 ± 610 | 1.12 / 0.75 | 334 | 0 |
| B prompt-master | 1.44 ± 0.35 | 0.94 ± 0.48 | -0.11 ± 0.35 / +0.01 ± 0.46 | 80% ± 0% | 3830 ± 188 | 1.62 / 1.38 | 1410 | 0 |
| C OpenAI-guide | 1.28 ± 0.25 | 0.94 ± 0.48 | -0.28 ± 0.25 / +0.13 ± 0.46 | 35% ± 0% | 4508 ± 624 | 1.75 / 2.25 | 2161 | 0 |
| D ambition-prompt | 1.67 ± 0.29 | 0.44 ± 0.38 | +0.11 ± 0.29 / -0.20 ± 0.40 | 70% ± 0% | 5805 ± 969 | 2.25 / 2.38 | 2961 | 3 |

Hidden-test failures (count of samples failing, per arm):

| Test | A | B | C | D |
|---|---|---|---|---|
| test_blank_emails_do_not_match | 0 | 0 | 3 | 0 |
| test_email_case_and_spaces | 0 | 0 | 3 | 0 |
| test_fill_blanks_from_duplicates | 2 | 3 | 3 | 3 |
| test_first_appearance_order | 1 | 0 | 3 | 3 |
| test_idempotent | 2 | 0 | 3 | 3 |
| test_input_not_mutated | 0 | 0 | 3 | 0 |
| test_junk_phones_do_not_match | 2 | 3 | 3 | 0 |
| test_most_complete_record_wins | 2 | 0 | 3 | 0 |
| test_no_extra_keys | 0 | 0 | 3 | 0 |
| test_performance_20k_rows | 1 | 0 | 3 | 0 |
| test_phone_formats | 1 | 0 | 3 | 3 |
| test_phone_us_country_code | 1 | 0 | 3 | 3 |
| test_same_name_different_people | 1 | 3 | 0 | 0 |
| test_tie_prefers_latest_updated_at | 1 | 0 | 0 | 0 |
| test_transitive_chain | 2 | 3 | 3 | 3 |

## Task: churn

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 0.39 ± 0.67 | 0.06 ± 0.10 | -0.39 ± 0.68 / -1.01 ± 0.10 | 11204 ± 306 | 0.38 / 0.12 | 164 | 0 |
| B prompt-master | 1.22 ± 0.25 | 0.83 ± 0.83 | +0.28 ± 0.26 / +0.18 ± 0.86 | 2211 ± 233 | 1.38 / 1.75 | 1792 | 0 |
| C OpenAI-guide | 0.61 ± 0.25 | 0.83 ± 1.01 | -0.25 ± 0.37 / -0.02 ± 0.73 | 8403 ± 8909 | 0.0 / 0.0 | 385 | 1 |
| D ambition-prompt | 1.17 ± 0.00 | 1.83 ± 1.36 | +0.36 ± 0.02 / +0.84 ± 1.34 | 8643 ± 1470 | 2.25 / 2.88 | 6262 | 1 |

## Prompt rubric by criterion (mean over tasks and both judges, 0–3)

| Arm | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Infeasible-demand flags (judge-listed / keyword hits) |
|---|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.25 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 1.50 | 2.25 | 1 / 0 |
| B prompt-master | 0.75 | 1.75 | 0.25 | 1.50 | 1.00 | 2.00 | 2.25 | 2.75 | 2 / 0 |
| C OpenAI-guide | 1.00 | 1.25 | 0.25 | 1.25 | 0.50 | 1.25 | 1.50 | 1.00 | 2 / 0 |
| D ambition-prompt | 3.00 | 2.50 | 2.25 | 3.00 | 1.75 | 3.00 | 2.25 | 1.75 | 6 / 2 |

P1 altitude, P2 depth, P3 range, P4 done criteria + outside judge, P5 limits/stop rules, P6 output spec, P7 consistency, P8 concision.

## Pairwise (D vs competitor, both orderings, per executor sample)

D win rate = (D wins + 0.5 × ties) / comparisons. Position-consistent = same winner in both orderings.

| Task | Pair | Judge | D wins | Ties | D losses | D win rate | Position-consistent |
|---|---|---|---|---|---|---|---|
| dedupe | D vs B | OpenAI | 0 | 0 | 6 | 0.00 | 3/3 |
| dedupe | D vs B | NVIDIA | 3 | 0 | 3 | 0.50 | 2/3 |
| dedupe | D vs C | OpenAI | 0 | 0 | 6 | 0.00 | 3/3 |
| dedupe | D vs C | NVIDIA | 1 | 0 | 5 | 0.17 | 2/3 |
| churn | D vs B | OpenAI | 0 | 0 | 6 | 0.00 | 3/3 |
| churn | D vs B | NVIDIA | 6 | 0 | 0 | 1.00 | 3/3 |
| churn | D vs C | OpenAI | 5 | 0 | 1 | 0.83 | 2/3 |
| churn | D vs C | NVIDIA | 5 | 0 | 1 | 0.83 | 2/3 |
| all | D vs B | OpenAI | 0 | 0 | 12 | 0.00 | 6/6 |
| all | D vs B | NVIDIA | 9 | 0 | 3 | 0.75 | 5/6 |
| all | D vs C | OpenAI | 5 | 0 | 7 | 0.42 | 5/6 |
| all | D vs C | NVIDIA | 6 | 0 | 6 | 0.50 | 4/6 |

## Judge agreement (OpenAI vs NVIDIA)

- Output scores: Pearson r = 0.06 (n=24); mean absolute difference = 0.83
- Prompt scores: Pearson r = 0.95 (n=8)
- Pairwise winners: 12/24 comparisons agree

## Length vs score

- Pearson r between output chars and output score: OpenAI -0.40 (n=24), NVIDIA 0.20 (n=24)

## Verdict on headline metrics (D vs B and C; n=3, no significance test)

- dedupe, D vs B: tests 70% vs 80%; output (OpenAI) 1.67 vs 1.44; output (NVIDIA) 0.44 vs 0.94
- dedupe, D vs C: tests 70% vs 35%; output (OpenAI) 1.67 vs 1.28; output (NVIDIA) 0.44 vs 0.94
- churn, D vs B: output (OpenAI) 1.17 vs 1.22; output (NVIDIA) 1.83 vs 0.83
- churn, D vs C: output (OpenAI) 1.17 vs 0.61; output (NVIDIA) 1.83 vs 0.83

## Raw prompts (hand-written, verbatim)

**dedupe:**

```
write a python function dedupe_contacts(rows) that removes duplicate contacts. rows is a list of dicts like {"name": "Ann Lee", "email": "ann@x.com", "phone": "(415) 555-0100", "company": "Acme", "updated_at": "2024-05-01"}. the same person shows up with different email caps or phone formats. keep the most complete record. no pandas
```

**churn:**

```
attached is our customer export (customers.csv). churn has been creeping up the last few months. can you figure out whats driving it and what we should do about it?
```
