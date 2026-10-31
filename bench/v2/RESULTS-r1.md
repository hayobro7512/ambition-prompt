# Results — run `v2-r1`

Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here (NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.

Models: optimizer `claude sonnet via Claude Code subagent (see v2/roles.md)`, simulated user `claude sonnet via Claude Code subagent (see v2/roles.md)`, executor `claude sonnet via Claude Code subagent (see v2/roles.md)`, judge 1 (primary) `gpt-5.6-sol`, judge 2 `openai/gpt-oss-20b`. Seed 7. n=2 executor samples per arm per task. OpenAI calls used: 150/150.

Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.

## Task: split

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Hidden tests pass rate | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|---|
| A raw prompt | 1.83 ± 0.00 | 0.00 ± 0.00 | -0.08 ± 0.00 / +0.00 ± 0.00 | 66% ± 4% | 2648 ± 16 | 1.12 / 0.0 | 253 | 0 |
| B prompt-master | 1.83 ± 0.00 | 0.00 ± 0.00 | -0.03 ± 0.00 / +0.00 ± 0.00 | 63% ± 7% | 3654 ± 107 | 2.25 / 2.12 | 2700 | 0 |
| R rival | 1.83 ± 0.00 | 0.00 ± 0.00 | +0.02 ± 0.00 / +0.00 ± 0.00 | 66% ± 4% | 5442 ± 165 | 2.5 / 2.0 | 1789 | 0 |
| D ambition-prompt | 2.00 ± 0.00 | 0.00 ± 0.00 | +0.09 ± 0.00 / +0.00 ± 0.00 | 58% ± 7% | 2618 ± 28 | 2.38 / 2.12 | 2713 | 0 |

Hidden-test failures (count of samples failing, per arm):

| Test | A | B | R | D |
|---|---|---|---|---|
| test_discount_shared | 0 | 2 | 2 | 2 |
| test_empty_shared_by_means_everyone | 2 | 2 | 2 | 2 |
| test_input_not_mutated | 2 | 2 | 2 | 2 |
| test_leftover_cent_largest_remainder_then_alpha | 2 | 0 | 0 | 2 |
| test_matches_reference_random | 2 | 2 | 2 | 2 |
| test_missing_shared_by_means_everyone | 2 | 2 | 2 | 2 |
| test_qty | 2 | 2 | 2 | 2 |
| test_returns_rounded_floats | 0 | 0 | 1 | 0 |
| test_string_prices | 0 | 1 | 0 | 1 |
| test_total_rounds_half_up | 1 | 1 | 0 | 1 |

## Task: abtest

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 2.75 ± 0.12 | n/a / +0.10 ± 0.15 | 3921 ± 99 | None / 0.0 | 126 | 0 |
| B prompt-master | n/a | 2.92 ± 0.12 | n/a / -0.15 ± 0.05 | 2764 ± 162 | None / 1.88 | 4084 | 0 |
| R rival | n/a | 2.92 ± 0.12 | n/a / +0.36 ± 0.13 | 4238 ± 49 | None / 2.25 | 3409 | 0 |
| D ambition-prompt | n/a | 2.00 ± 0.94 | n/a / -0.31 ± 0.96 | 5180 ± 60 | None / 1.5 | 4665 | 1 |

## Task: priceemail

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.00 ± 0.00 | n/a / -0.89 ± 0.05 | 1912 ± 129 | None / 0.75 | 69 | 0 |
| B prompt-master | n/a | 0.00 ± 0.00 | n/a / -1.46 ± 0.03 | 848 ± 30 | None / 1.5 | 2778 | 0 |
| R rival | n/a | 2.42 ± 0.12 | n/a / +1.12 ± 0.10 | 1060 ± 26 | None / 2.12 | 2735 | 1 |
| D ambition-prompt | n/a | 2.42 ± 0.12 | n/a / +1.23 ± 0.12 | 1246 ± 1 | None / 2.25 | 4154 | 1 |

## Task: queue

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 2.83 ± 0.24 | n/a / -0.10 ± 0.25 | 4137 ± 419 | None / 0.38 | 145 | 0 |
| B prompt-master | n/a | 3.00 ± 0.00 | n/a / +0.05 ± 0.01 | 4845 ± 366 | None / 2.25 | 3801 | 0 |
| R rival | n/a | 2.92 ± 0.12 | n/a / -0.01 ± 0.11 | 4150 ± 194 | None / 2.12 | 3071 | 0 |
| D ambition-prompt | n/a | 3.00 ± 0.00 | n/a / +0.06 ± 0.00 | 4351 ± 106 | None / 1.75 | 4382 | 1 |

## Task: referral

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.42 ± 0.59 | n/a / -0.98 ± 0.78 | 9958 ± 1073 | None / 0.75 | 47 | 0 |
| B prompt-master | n/a | 2.67 ± 0.47 | n/a / +0.23 ± 0.27 | 17746 ± 2032 | None / 2.62 | 4106 | 1 |
| R rival | n/a | 3.00 ± 0.00 | n/a / +1.12 ± 0.02 | 13032 ± 168 | None / 2.0 | 3036 | 1 |
| D ambition-prompt | n/a | 3.00 ± 0.00 | n/a / -0.37 ± 0.05 | 29867 ± 805 | None / 2.62 | 6276 | 1 |

## Prompt rubric by criterion (mean over tasks and both judges, 0–3)

| Arm | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Infeasible-demand flags (judge-listed / keyword hits) |
|---|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.00 | 0.00 | 0.00 | 0.17 | 0.17 | 0.17 | 1.50 | 2.00 | 0 / 0 |
| B prompt-master | 1.67 | 2.33 | 1.17 | 2.33 | 1.83 | 2.67 | 2.83 | 2.00 | 0 / 3 |
| R rival | 2.00 | 2.50 | 1.33 | 2.00 | 1.50 | 2.83 | 3.00 | 2.17 | 0 / 3 |
| D ambition-prompt | 2.00 | 2.00 | 1.17 | 1.83 | 1.83 | 2.50 | 3.00 | 2.50 | 0 / 6 |

P1 altitude, P2 depth, P3 range, P4 done criteria + outside judge, P5 limits/stop rules, P6 output spec, P7 consistency, P8 concision.

## Pairwise (D vs competitor, both orderings, per executor sample)

D win rate = (D wins + 0.5 × ties) / comparisons. Position-consistent = same winner in both orderings.

| Task | Pair | Judge | D wins | Ties | D losses | D win rate | Position-consistent |
|---|---|---|---|---|---|---|---|
| split | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| split | D vs B | NVIDIA | 0 | 1 | 3 | 0.12 | 1/2 |
| split | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| split | D vs R | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| abtest | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| abtest | D vs B | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| abtest | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| abtest | D vs R | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| priceemail | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| priceemail | D vs B | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| priceemail | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| priceemail | D vs R | NVIDIA | 1 | 1 | 2 | 0.38 | 0/2 |
| queue | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| queue | D vs B | NVIDIA | 2 | 0 | 2 | 0.50 | 0/2 |
| queue | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| queue | D vs R | NVIDIA | 2 | 1 | 1 | 0.62 | 1/2 |
| referral | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| referral | D vs B | NVIDIA | 2 | 0 | 2 | 0.50 | 0/2 |
| referral | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| referral | D vs R | NVIDIA | 3 | 0 | 1 | 0.75 | 1/2 |
| all | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| all | D vs B | NVIDIA | 8 | 1 | 11 | 0.42 | 5/10 |
| all | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| all | D vs R | NVIDIA | 6 | 2 | 12 | 0.35 | 6/10 |

## Judge agreement (OpenAI vs NVIDIA)

- Output scores: Pearson r = n/a; mean absolute difference = 1.88
- Prompt scores: Pearson r = 0.98 (n=4)
- Pairwise winners: 0/0 comparisons agree

## Length vs score

- Pearson r between output chars and output score: OpenAI -0.51 (n=4), NVIDIA 0.30 (n=40)

## Verdict on headline metrics (D vs B and C; n=3, no significance test)

- split, D vs B: tests 58% vs 63%; output (OpenAI) 2.00 vs 1.83; output (NVIDIA) 0.00 vs 0.00
- split, D vs R: tests 58% vs 66%; output (OpenAI) 2.00 vs 1.83; output (NVIDIA) 0.00 vs 0.00
- abtest, D vs B: output (OpenAI) n/a; output (NVIDIA) 2.00 vs 2.92
- abtest, D vs R: output (OpenAI) n/a; output (NVIDIA) 2.00 vs 2.92
- priceemail, D vs B: output (OpenAI) n/a; output (NVIDIA) 2.42 vs 0.00
- priceemail, D vs R: output (OpenAI) n/a; output (NVIDIA) 2.42 vs 2.42
- queue, D vs B: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 3.00
- queue, D vs R: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 2.92
- referral, D vs B: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 2.67
- referral, D vs R: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 3.00

## Raw prompts (hand-written, verbatim)

**split:**

```
write a python function split_bill(items, tax, tip_percent) that splits a restaurant bill between people. items is a list like [{"name": "pizza", "price": 18.50, "shared_by": ["ana", "ben"]}]. return a dict of how much each person owes. no external libs
```

**abtest:**

```
attached is the export from our checkout redesign test (ab_results.csv, B is the new checkout). did it win? should we ship it?
```

**priceemail:**

```
write an email to our customers telling them about the price increase
```

**queue:**

```
we're deciding whether to keep our postgres job queue or move to a real message broker. i pasted our notes below (sources.md). what should we do?
```

**referral:**

```
write a spec for a referral program for our app
```
