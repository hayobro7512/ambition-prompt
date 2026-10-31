# Results — run `v2-r2`

Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here (NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.

Models: optimizer `claude sonnet via Claude Code subagent (see v2/roles.md)`, simulated user `claude sonnet via Claude Code subagent (see v2/roles.md)`, executor `claude sonnet via Claude Code subagent (see v2/roles.md)`, judge 1 (primary) `gpt-5.6-sol`, judge 2 `openai/gpt-oss-20b`. Seed 7. n=2 executor samples per arm per task. OpenAI calls used: 55/150.

Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.

## Task: split

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Hidden tests pass rate | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.00 ± 0.00 | n/a / -0.31 ± 0.00 | 66% ± 4% | 2648 ± 16 | None / 0.75 | 253 | 0 |
| B prompt-master | n/a | 0.00 ± 0.00 | n/a / -0.48 ± 0.02 | 63% ± 7% | 3654 ± 107 | None / 0.88 | 2700 | 0 |
| R rival | n/a | 0.00 ± 0.00 | n/a / -0.68 ± 0.02 | 66% ± 4% | 5442 ± 165 | None / 2.38 | 1789 | 0 |
| D ambition-prompt | n/a | 2.00 ± 1.41 | n/a / +1.47 ± 1.39 | 95% ± 0% | 4028 ± 166 | None / 2.38 | 4444 | 1 |

Hidden-test failures (count of samples failing, per arm):

| Test | A | B | R | D |
|---|---|---|---|---|
| test_discount_shared | 0 | 2 | 2 | 0 |
| test_empty_shared_by_means_everyone | 2 | 2 | 2 | 0 |
| test_input_not_mutated | 2 | 2 | 2 | 0 |
| test_leftover_cent_largest_remainder_then_alpha | 2 | 0 | 0 | 0 |
| test_matches_reference_random | 2 | 2 | 2 | 2 |
| test_missing_shared_by_means_everyone | 2 | 2 | 2 | 0 |
| test_qty | 2 | 2 | 2 | 0 |
| test_returns_rounded_floats | 0 | 0 | 1 | 0 |
| test_string_prices | 0 | 1 | 0 | 0 |
| test_total_rounds_half_up | 1 | 1 | 0 | 0 |

## Task: abtest

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 2.58 ± 0.12 | n/a / -0.20 ± 0.11 | 3921 ± 99 | None / 0.0 | 126 | 0 |
| B prompt-master | n/a | 2.92 ± 0.12 | n/a / +0.07 ± 0.11 | 2764 ± 162 | None / 1.88 | 4084 | 0 |
| R rival | n/a | 2.92 ± 0.12 | n/a / +0.15 ± 0.12 | 4238 ± 49 | None / 2.0 | 3409 | 0 |
| D ambition-prompt | n/a | 2.58 ± 0.59 | n/a / -0.01 ± 0.60 | 11191 ± 902 | None / 2.25 | 4394 | 1 |

## Task: priceemail

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.00 ± 0.00 | n/a / -0.85 ± 0.06 | 1912 ± 129 | None / 0.75 | 69 | 0 |
| B prompt-master | n/a | 0.00 ± 0.00 | n/a / -1.61 ± 0.03 | 848 ± 30 | None / 2.0 | 2778 | 0 |
| R rival | n/a | 2.58 ± 0.12 | n/a / +1.18 ± 0.09 | 1060 ± 26 | None / 2.0 | 2735 | 1 |
| D ambition-prompt | n/a | 2.58 ± 0.12 | n/a / +1.28 ± 0.16 | 1178 ± 49 | None / 2.0 | 4286 | 1 |

## Task: queue

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 3.00 ± 0.00 | n/a / +0.07 ± 0.06 | 4137 ± 419 | None / 0.75 | 145 | 0 |
| B prompt-master | n/a | 3.00 ± 0.00 | n/a / -0.03 ± 0.04 | 4845 ± 366 | None / 2.88 | 3801 | 0 |
| R rival | n/a | 3.00 ± 0.00 | n/a / +0.06 ± 0.03 | 4150 ± 194 | None / 2.88 | 3071 | 0 |
| D ambition-prompt | n/a | 2.75 ± 0.35 | n/a / -0.10 ± 0.37 | 3568 ± 112 | None / 2.88 | 3713 | 1 |

## Task: referral

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.58 ± 0.82 | n/a / -0.68 ± 1.22 | 9958 ± 1073 | None / 0.0 | 47 | 0 |
| B prompt-master | n/a | 2.92 ± 0.12 | n/a / -0.45 ± 0.30 | 17746 ± 2032 | None / 2.5 | 4106 | 1 |
| R rival | n/a | 3.00 ± 0.00 | n/a / +0.75 ± 0.05 | 13032 ± 168 | None / 2.5 | 3036 | 1 |
| D ambition-prompt | n/a | 3.00 ± 0.00 | n/a / +0.39 ± 0.09 | 14386 ± 345 | None / 2.5 | 5106 | 1 |

## Prompt rubric by criterion (mean over tasks and both judges, 0–3)

| Arm | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Infeasible-demand flags (judge-listed / keyword hits) |
|---|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.80 | 1.80 | 1 / 0 |
| B prompt-master | 1.80 | 2.20 | 1.40 | 2.00 | 1.80 | 1.80 | 2.80 | 2.40 | 0 / 3 |
| R rival | 2.00 | 2.80 | 1.60 | 2.60 | 2.20 | 2.60 | 2.80 | 2.20 | 0 / 3 |
| D ambition-prompt | 2.20 | 2.80 | 1.60 | 2.60 | 2.20 | 2.80 | 2.80 | 2.20 | 0 / 4 |

P1 altitude, P2 depth, P3 range, P4 done criteria + outside judge, P5 limits/stop rules, P6 output spec, P7 consistency, P8 concision.

## Pairwise (D vs competitor, both orderings, per executor sample)

D win rate = (D wins + 0.5 × ties) / comparisons. Position-consistent = same winner in both orderings.

| Task | Pair | Judge | D wins | Ties | D losses | D win rate | Position-consistent |
|---|---|---|---|---|---|---|---|
| split | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| split | D vs B | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| split | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| split | D vs R | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| abtest | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| abtest | D vs B | NVIDIA | 2 | 0 | 2 | 0.50 | 2/2 |
| abtest | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| abtest | D vs R | NVIDIA | 3 | 0 | 1 | 0.75 | 1/2 |
| priceemail | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| priceemail | D vs B | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| priceemail | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| priceemail | D vs R | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| queue | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| queue | D vs B | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| queue | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| queue | D vs R | NVIDIA | 0 | 1 | 3 | 0.12 | 1/2 |
| referral | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| referral | D vs B | NVIDIA | 1 | 0 | 3 | 0.25 | 1/2 |
| referral | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| referral | D vs R | NVIDIA | 3 | 0 | 1 | 0.75 | 1/2 |
| all | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| all | D vs B | NVIDIA | 11 | 0 | 9 | 0.55 | 9/10 |
| all | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| all | D vs R | NVIDIA | 10 | 1 | 9 | 0.53 | 7/10 |

## Judge agreement (OpenAI vs NVIDIA)

- Output scores: n/a
- Prompt scores: Pearson r = n/a
- Pairwise winners: 0/0 comparisons agree

## Length vs score

- Pearson r between output chars and output score: OpenAI n/a, NVIDIA 0.30 (n=40)

## Verdict on headline metrics (D vs B and C; n=3, no significance test)

- split, D vs B: tests 95% vs 63%; output (OpenAI) n/a; output (NVIDIA) 2.00 vs 0.00
- split, D vs R: tests 95% vs 66%; output (OpenAI) n/a; output (NVIDIA) 2.00 vs 0.00
- abtest, D vs B: output (OpenAI) n/a; output (NVIDIA) 2.58 vs 2.92
- abtest, D vs R: output (OpenAI) n/a; output (NVIDIA) 2.58 vs 2.92
- priceemail, D vs B: output (OpenAI) n/a; output (NVIDIA) 2.58 vs 0.00
- priceemail, D vs R: output (OpenAI) n/a; output (NVIDIA) 2.58 vs 2.58
- queue, D vs B: output (OpenAI) n/a; output (NVIDIA) 2.75 vs 3.00
- queue, D vs R: output (OpenAI) n/a; output (NVIDIA) 2.75 vs 3.00
- referral, D vs B: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 2.92
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
