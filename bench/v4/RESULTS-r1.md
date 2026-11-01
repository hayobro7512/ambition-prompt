# Results — run `v4-r1`

Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here (NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.

Models: optimizer `claude-sonnet-5-5`, simulated user `claude-sonnet-5-5`, executor `claude-sonnet-5-5`, judge 1 (primary) `nvidia/nemotron-3-ultra-550b-a55b`, judge 2 `nvidia/nemotron-3.5-lightning-30b-a3b`. Seed 7. n=2 executor samples per arm per task. OpenAI calls used: 0/0.

Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.

## Task: bizdays

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Hidden tests pass rate | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.58 ± 0.35 | 0.92 ± 0.35 | +0.60 ± 0.01 / +0.54 ± 0.07 | 68% ± 7% | 1710 ± 307 | 1.5 / 0.62 | 123 | 0 |
| B prompt-master | 0.33 ± 0.24 | 0.58 ± 0.12 | -1.08 ± 0.21 / -0.92 ± 0.10 | 26% ± 0% | 3454 ± 44 | 1.0 / 1.38 | 2033 | 0 |
| R rival | 0.33 ± 0.24 | 0.58 ± 0.12 | -0.54 ± 0.29 / -0.50 ± 0.16 | 53% ± 0% | 2645 ± 71 | 0.62 / 1.38 | 2380 | 0 |
| D ambition-prompt | 3.00 ± 0.00 | 2.83 ± 0.24 | +1.02 ± 0.04 / +0.89 ± 0.27 | 100% ± 0% | 4564 ± 97 | 2.88 / 2.0 | 4848 | 1 |

Hidden-test failures (count of samples failing, per arm):

| Test | A | B | R | D |
|---|---|---|---|---|
| test_bad_string_raises_value_error | 2 | 2 | 2 | 0 |
| test_datetime_inputs_use_date | 0 | 2 | 2 | 0 |
| test_friday_to_monday | 0 | 2 | 0 | 0 |
| test_full_week | 0 | 2 | 0 | 0 |
| test_holiday_on_start_day_not_counted_twice | 2 | 0 | 2 | 0 |
| test_holiday_outside_range_ignored | 0 | 2 | 0 | 0 |
| test_holiday_strings_and_duplicates | 1 | 2 | 2 | 0 |
| test_iso_string_dates | 1 | 2 | 2 | 0 |
| test_long_span_is_fast | 0 | 2 | 0 | 0 |
| test_long_span_with_holidays_is_fast | 2 | 0 | 2 | 0 |
| test_random_against_oracle | 2 | 2 | 2 | 0 |
| test_reversed_is_negative | 0 | 2 | 2 | 0 |
| test_same_day_is_zero | 0 | 2 | 0 | 0 |
| test_start_excluded_end_included | 0 | 2 | 0 | 0 |
| test_weekday_holiday_skipped | 0 | 2 | 0 | 0 |
| test_weekend_holiday_ignored | 0 | 2 | 0 | 0 |
| test_weekend_only | 2 | 0 | 2 | 0 |

## Task: activation

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.25 ± 0.12 | 2.42 ± 0.12 | -0.01 ± 0.11 / -0.24 ± 0.11 | 2345 ± 71 | 0.62 / 0.75 | 226 | 0 |
| B prompt-master | 1.83 ± 1.18 | 2.83 ± 0.24 | -0.55 ± 1.18 / -0.06 ± 0.25 | 4982 ± 182 | 1.62 / 2.5 | 3776 | 0 |
| R rival | 2.17 ± 0.47 | 2.75 ± 0.12 | -0.06 ± 0.48 / +0.17 ± 0.09 | 1825 ± 137 | 2.5 / 2.5 | 3343 | 1 |
| D ambition-prompt | 3.00 ± 0.00 | 3.00 ± 0.00 | +0.62 ± 0.00 / +0.12 ± 0.01 | 4740 ± 135 | 2.88 / 2.5 | 5821 | 1 |

## Task: outage

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 0.17 ± 0.00 | 0.25 ± 0.12 | -0.09 ± 0.03 / -0.03 ± 0.15 | 2367 ± 18 | 0.62 / 0.75 | 56 | 0 |
| B prompt-master | 1.92 ± 0.82 | 2.58 ± 0.12 | -0.68 ± 0.83 / -0.16 ± 0.11 | 1338 ± 2 | 2.5 / 2.0 | 3499 | 2 |
| R rival | 2.75 ± 0.12 | 2.58 ± 0.12 | +0.30 ± 0.06 / -0.00 ± 0.18 | 1388 ± 21 | 2.75 / 1.88 | 2675 | 1 |
| D ambition-prompt | 2.75 ± 0.12 | 2.58 ± 0.12 | +0.48 ± 0.25 / +0.19 ± 0.03 | 1449 ± 48 | 2.75 / 2.0 | 4086 | 1 |

## Task: flags

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.92 ± 0.12 | 2.92 ± 0.12 | -0.02 ± 0.13 / +0.15 ± 0.12 | 2810 ± 153 | 0.25 / 0.75 | 85 | 0 |
| B prompt-master | 3.00 ± 0.00 | 2.75 ± 0.35 | +0.13 ± 0.03 / -0.00 ± 0.36 | 3471 ± 368 | 2.5 / 2.25 | 2733 | 0 |
| R rival | 2.67 ± 0.24 | 2.67 ± 0.00 | -0.03 ± 0.22 / -0.04 ± 0.00 | 6038 ± 214 | 2.5 / 2.12 | 2914 | 0 |
| D ambition-prompt | 2.83 ± 0.24 | 2.67 ± 0.47 | -0.09 ± 0.22 / -0.10 ± 0.48 | 2909 ± 164 | 2.38 / 2.0 | 4297 | 1 |

## Task: actions

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.42 ± 0.12 | 1.67 ± 0.94 | +0.26 ± 0.21 / +0.21 ± 0.98 | 554 ± 8 | 1.62 / 1.62 | 365 | 0 |
| B prompt-master | 1.25 ± 0.12 | 1.00 ± 0.00 | -0.13 ± 0.03 / -0.09 ± 0.04 | 635 ± 10 | 2.0 / 1.5 | 2103 | 0 |
| R rival | 1.25 ± 0.12 | 1.00 ± 0.00 | -0.15 ± 0.47 / -0.10 ± 0.28 | 634 ± 66 | 2.12 / 1.62 | 1848 | 0 |
| D ambition-prompt | 1.25 ± 0.12 | 1.00 ± 0.00 | +0.02 ± 0.25 / -0.02 ± 0.18 | 653 ± 42 | 2.0 / 1.5 | 2323 | 1 |

## Prompt rubric by criterion (mean over tasks and both judges, 0–3)

| Arm | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Infeasible-demand flags (judge-listed / keyword hits) |
|---|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.50 | 0.20 | 0.10 | 0.50 | 0.40 | 0.70 | 2.10 | 2.80 | 4 / 0 |
| B prompt-master | 1.70 | 1.90 | 1.10 | 2.00 | 2.00 | 2.70 | 2.20 | 1.80 | 8 / 0 |
| R rival | 1.90 | 1.90 | 0.90 | 2.00 | 2.10 | 2.80 | 2.40 | 2.00 | 6 / 2 |
| D ambition-prompt | 2.60 | 2.10 | 1.10 | 2.30 | 2.60 | 2.90 | 2.70 | 2.00 | 2 / 3 |

P1 altitude, P2 depth, P3 range, P4 done criteria + outside judge, P5 limits/stop rules, P6 output spec, P7 consistency, P8 concision.

## Pairwise (D vs competitor, both orderings, per executor sample)

D win rate = (D wins + 0.5 × ties) / comparisons. Position-consistent = same winner in both orderings.

| Task | Pair | Judge | D wins | Ties | D losses | D win rate | Position-consistent |
|---|---|---|---|---|---|---|---|
| bizdays | D vs B | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| bizdays | D vs B | Judge 2 | 4 | 0 | 0 | 1.00 | 2/2 |
| bizdays | D vs R | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| bizdays | D vs R | Judge 2 | 4 | 0 | 0 | 1.00 | 2/2 |
| activation | D vs B | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| activation | D vs B | Judge 2 | 3 | 0 | 0 | 1.00 | 1/2 |
| activation | D vs R | Judge 1 | 3 | 0 | 1 | 0.75 | 1/2 |
| activation | D vs R | Judge 2 | 1 | 0 | 3 | 0.25 | 1/2 |
| outage | D vs B | Judge 1 | 0 | 0 | 4 | 0.00 | 2/2 |
| outage | D vs B | Judge 2 | 3 | 0 | 1 | 0.75 | 1/2 |
| outage | D vs R | Judge 1 | 2 | 0 | 2 | 0.50 | 2/2 |
| outage | D vs R | Judge 2 | 1 | 0 | 3 | 0.25 | 1/2 |
| flags | D vs B | Judge 1 | 2 | 0 | 2 | 0.50 | 0/2 |
| flags | D vs B | Judge 2 | 1 | 0 | 2 | 0.33 | 0/2 |
| flags | D vs R | Judge 1 | 1 | 0 | 3 | 0.25 | 1/2 |
| flags | D vs R | Judge 2 | 1 | 0 | 0 | 1.00 | 0/1 |
| actions | D vs B | Judge 1 | 1 | 3 | 0 | 0.62 | 1/2 |
| actions | D vs B | Judge 2 | 0 | 1 | 3 | 0.12 | 1/2 |
| actions | D vs R | Judge 1 | 0 | 0 | 4 | 0.00 | 2/2 |
| actions | D vs R | Judge 2 | 0 | 0 | 4 | 0.00 | 2/2 |
| all | D vs B | Judge 1 | 11 | 3 | 6 | 0.62 | 7/10 |
| all | D vs B | Judge 2 | 11 | 1 | 6 | 0.64 | 5/10 |
| all | D vs R | Judge 1 | 10 | 0 | 10 | 0.50 | 8/10 |
| all | D vs R | Judge 2 | 7 | 0 | 10 | 0.41 | 6/9 |

## Judge agreement (Judge 1 vs Judge 2)

- Output scores: Pearson r = 0.88 (n=40); mean absolute difference = 0.31
- Prompt scores: Pearson r = 0.79 (n=20)
- Pairwise winners: 24/35 comparisons agree

## Length vs score

- Pearson r between output chars and output score: Judge 1 0.28 (n=40), Judge 2 0.43 (n=40)

## Verdict on headline metrics (D vs B and R; n=2, no significance test)

- bizdays, D vs B: tests 100% vs 26%; output (Judge 1) 3.00 vs 0.33; output (Judge 2) 2.83 vs 0.58
- bizdays, D vs R: tests 100% vs 53%; output (Judge 1) 3.00 vs 0.33; output (Judge 2) 2.83 vs 0.58
- activation, D vs B: output (Judge 1) 3.00 vs 1.83; output (Judge 2) 3.00 vs 2.83
- activation, D vs R: output (Judge 1) 3.00 vs 2.17; output (Judge 2) 3.00 vs 2.75
- outage, D vs B: output (Judge 1) 2.75 vs 1.92; output (Judge 2) 2.58 vs 2.58
- outage, D vs R: output (Judge 1) 2.75 vs 2.75; output (Judge 2) 2.58 vs 2.58
- flags, D vs B: output (Judge 1) 2.83 vs 3.00; output (Judge 2) 2.67 vs 2.75
- flags, D vs R: output (Judge 1) 2.83 vs 2.67; output (Judge 2) 2.67 vs 2.67
- actions, D vs B: output (Judge 1) 1.25 vs 1.25; output (Judge 2) 1.00 vs 1.00
- actions, D vs R: output (Judge 1) 1.25 vs 1.25; output (Judge 2) 1.00 vs 1.00

## Raw prompts (hand-written, verbatim)

**bizdays:**

```
write a python function business_days(start, end, holidays=()) that counts the business days between two dates. stdlib only
```

**activation:**

```
attached is our monthly signup and activation export (activation.csv). we launched a new onboarding email sequence in march and activation went up about 6 points. can you confirm the impact so I can put it in the board update?
```

**outage:**

```
write an email to our customers about yesterday's outage
```

**flags:**

```
should we build our own feature flag system or buy one? my notes are below (notes.md)
```

**actions:**

```
turn the meeting transcript below (transcript.md) into a list of action items. a markdown table with columns Owner, Action, Due. only include items someone actually agreed to do, not ideas or maybes. due dates as YYYY-MM-DD; write "none" if no date was set. order by due date, "none" last. after the table, one line listing open questions nobody took. nothing else.
```
