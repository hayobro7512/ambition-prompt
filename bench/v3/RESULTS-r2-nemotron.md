# Results — run `v3-r2-nem`

Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here (NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.

Models: optimizer `claude-sonnet-5-5`, simulated user `claude-sonnet-5-5`, executor `claude-sonnet-5-5`, judge 1 (primary) `nvidia/nemotron-3-ultra-550b-a55b`, judge 2 `openai/gpt-oss-20b`. Seed 7. n=2 executor samples per arm per task. OpenAI calls used: 1/140.

Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.

## Task: duration

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Hidden tests pass rate | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.50 ± 0.00 | 0.33 ± 0.47 | -0.10 ± 0.04 / -0.16 ± 0.47 | 71% ± 4% | 1397 ± 116 | None / 0.75 | 111 | 0 |
| B prompt-master | 0.92 ± 0.59 | 0.33 ± 0.47 | -0.07 ± 0.58 / -0.14 ± 0.47 | 79% ± 0% | 2930 ± 56 | None / 2.25 | 2011 | 0 |
| R rival | 1.00 ± 0.47 | 0.33 ± 0.47 | -0.12 ± 0.44 / -0.13 ± 0.47 | 68% ± 0% | 3822 ± 252 | None / 2.0 | 1999 | 0 |
| D ambition-prompt | 1.17 ± 0.24 | 0.92 ± 0.35 | +0.29 ± 0.23 / +0.44 ± 0.35 | 89% ± 0% | 2390 ± 45 | None / 2.38 | 3307 | 2 |

Hidden-test failures (count of samples failing, per arm):

| Test | A | B | R | D |
|---|---|---|---|---|
| test_bare_number_is_seconds | 2 | 2 | 2 | 0 |
| test_clock_hms | 2 | 2 | 2 | 2 |
| test_clock_ms | 2 | 2 | 2 | 2 |
| test_non_string | 1 | 0 | 0 | 0 |
| test_repeated_unit | 2 | 0 | 0 | 0 |
| test_returns_int | 0 | 0 | 2 | 0 |
| test_rounding_half_up | 2 | 2 | 2 | 0 |
| test_weeks | 0 | 0 | 2 | 0 |

## Task: csat

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.75 ± 0.12 | 2.75 ± 0.12 | -0.07 ± 0.15 / -0.07 ± 0.15 | 2796 ± 392 | 0.62 / 0.0 | 118 | 0 |
| B prompt-master | 3.00 ± 0.00 | 3.00 ± 0.00 | +0.09 ± 0.01 / +0.07 ± 0.01 | 4346 ± 206 | 2.38 / 2.0 | 2897 | 0 |
| R rival | 3.00 ± 0.00 | 3.00 ± 0.00 | +0.06 ± 0.01 / +0.04 ± 0.01 | 4980 ± 192 | 2.5 / 2.0 | 3550 | 0 |
| D ambition-prompt | 2.92 ± 0.12 | 3.00 ± 0.00 | -0.08 ± 0.07 / -0.04 ± 0.06 | 7084 ± 1877 | 3.0 / 2.5 | 6697 | 1 |

## Task: jobpost

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 0.17 ± 0.00 | 0.00 ± 0.00 | +0.40 ± 0.07 / +0.35 ± 0.06 | 4297 ± 68 | 0.62 / 0.62 | 46 | 0 |
| B prompt-master | 0.17 ± 0.00 | 0.00 ± 0.00 | -1.03 ± 0.09 / -0.90 ± 0.08 | 3156 ± 60 | 1.62 / 2.88 | 2668 | 0 |
| R rival | 2.92 ± 0.12 | 2.42 ± 0.12 | +0.71 ± 0.23 / +0.62 ± 0.02 | 2532 ± 63 | 2.0 / 2.88 | 4274 | 1 |
| D ambition-prompt | 2.92 ± 0.12 | 2.42 ± 0.12 | -0.07 ± 0.16 / -0.07 ± 0.08 | 2140 ± 18 | 2.0 / 2.88 | 4799 | 1 |

## Task: trial

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.92 ± 0.12 | 2.75 ± 0.12 | +0.13 ± 0.11 / -0.05 ± 0.15 | 3162 ± 200 | 0.62 / 0.5 | 101 | 0 |
| B prompt-master | 2.67 ± 0.00 | 2.92 ± 0.12 | -0.12 ± 0.00 / +0.05 ± 0.11 | 3566 ± 43 | 2.0 / 2.25 | 2619 | 0 |
| R rival | 2.67 ± 0.00 | 2.92 ± 0.12 | -0.13 ± 0.00 / -0.01 ± 0.14 | 4032 ± 139 | 1.75 / 2.25 | 2109 | 0 |
| D ambition-prompt | 2.92 ± 0.12 | 3.00 ± 0.00 | +0.12 ± 0.12 / +0.01 ± 0.00 | 4580 ± 25 | 2.88 / 2.75 | 6384 | 1 |

## Task: relnotes

| Arm | Output score (Judge 1) | Output score (Judge 2) | Length-controlled (Judge 1 / Judge 2) | Output chars | Prompt score (Judge 1 / Judge 2) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.33 ± 0.24 | 2.75 ± 0.35 | +0.25 ± 0.27 / +0.25 ± 0.32 | 1227 ± 16 | 1.0 / 1.75 | 305 | 0 |
| B prompt-master | 2.33 ± 0.24 | 2.75 ± 0.35 | +0.13 ± 0.47 / +0.11 ± 0.10 | 1170 ± 107 | 2.12 / 1.75 | 1925 | 0 |
| R rival | 2.33 ± 0.24 | 2.75 ± 0.35 | -0.20 ± 0.19 / -0.25 ± 0.40 | 1026 ± 18 | 2.0 / 1.75 | 1851 | 0 |
| D ambition-prompt | 1.17 ± 0.00 | 1.58 ± 1.30 | -0.18 ± 0.01 / -0.11 ± 1.29 | 1645 ± 6 | 2.88 / 1.75 | 3557 | 1 |

## Prompt rubric by criterion (mean over tasks and both judges, 0–3)

| Arm | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Infeasible-demand flags (judge-listed / keyword hits) |
|---|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.44 | 0.00 | 0.00 | 0.33 | 0.22 | 0.33 | 1.78 | 2.67 | 3 / 0 |
| B prompt-master | 1.89 | 2.11 | 1.11 | 2.22 | 2.11 | 2.78 | 2.67 | 2.22 | 3 / 0 |
| R rival | 2.22 | 1.89 | 1.11 | 2.22 | 1.89 | 2.78 | 2.67 | 2.22 | 2 / 1 |
| D ambition-prompt | 2.56 | 2.56 | 1.78 | 2.67 | 2.67 | 3.00 | 2.89 | 2.33 | 1 / 3 |

P1 altitude, P2 depth, P3 range, P4 done criteria + outside judge, P5 limits/stop rules, P6 output spec, P7 consistency, P8 concision.

## Pairwise (D vs competitor, both orderings, per executor sample)

D win rate = (D wins + 0.5 × ties) / comparisons. Position-consistent = same winner in both orderings.

| Task | Pair | Judge | D wins | Ties | D losses | D win rate | Position-consistent |
|---|---|---|---|---|---|---|---|
| duration | D vs B | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| duration | D vs B | Judge 2 | 4 | 0 | 0 | 1.00 | 2/2 |
| duration | D vs R | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| duration | D vs R | Judge 2 | 4 | 0 | 0 | 1.00 | 2/2 |
| csat | D vs B | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| csat | D vs B | Judge 2 | 1 | 0 | 3 | 0.25 | 1/2 |
| csat | D vs R | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| csat | D vs R | Judge 2 | 0 | 0 | 4 | 0.00 | 2/2 |
| jobpost | D vs B | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| jobpost | D vs B | Judge 2 | 4 | 0 | 0 | 1.00 | 2/2 |
| jobpost | D vs R | Judge 1 | 2 | 1 | 1 | 0.62 | 1/2 |
| jobpost | D vs R | Judge 2 | 4 | 0 | 0 | 1.00 | 2/2 |
| trial | D vs B | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| trial | D vs B | Judge 2 | 3 | 0 | 1 | 0.75 | 1/2 |
| trial | D vs R | Judge 1 | 4 | 0 | 0 | 1.00 | 2/2 |
| trial | D vs R | Judge 2 | 4 | 0 | 0 | 1.00 | 2/2 |
| relnotes | D vs B | Judge 1 | 0 | 0 | 4 | 0.00 | 2/2 |
| relnotes | D vs B | Judge 2 | 0 | 0 | 4 | 0.00 | 2/2 |
| relnotes | D vs R | Judge 1 | 0 | 0 | 4 | 0.00 | 2/2 |
| relnotes | D vs R | Judge 2 | 0 | 0 | 4 | 0.00 | 2/2 |
| all | D vs B | Judge 1 | 16 | 0 | 4 | 0.80 | 10/10 |
| all | D vs B | Judge 2 | 12 | 0 | 8 | 0.60 | 8/10 |
| all | D vs R | Judge 1 | 14 | 1 | 5 | 0.72 | 9/10 |
| all | D vs R | Judge 2 | 12 | 0 | 8 | 0.60 | 10/10 |

## Judge agreement (Judge 1 vs Judge 2)

- Output scores: Pearson r = 0.93 (n=40); mean absolute difference = 0.31
- Prompt scores: Pearson r = 0.69 (n=16)
- Pairwise winners: 30/40 comparisons agree

## Length vs score

- Pearson r between output chars and output score: Judge 1 0.23 (n=40), Judge 2 0.15 (n=40)

## Verdict on headline metrics (D vs B and R; n=2, no significance test)

- duration, D vs B: tests 89% vs 79%; output (Judge 1) 1.17 vs 0.92; output (Judge 2) 0.92 vs 0.33
- duration, D vs R: tests 89% vs 68%; output (Judge 1) 1.17 vs 1.00; output (Judge 2) 0.92 vs 0.33
- csat, D vs B: output (Judge 1) 2.92 vs 3.00; output (Judge 2) 3.00 vs 3.00
- csat, D vs R: output (Judge 1) 2.92 vs 3.00; output (Judge 2) 3.00 vs 3.00
- jobpost, D vs B: output (Judge 1) 2.92 vs 0.17; output (Judge 2) 2.42 vs 0.00
- jobpost, D vs R: output (Judge 1) 2.92 vs 2.92; output (Judge 2) 2.42 vs 2.42
- trial, D vs B: output (Judge 1) 2.92 vs 2.67; output (Judge 2) 3.00 vs 2.92
- trial, D vs R: output (Judge 1) 2.92 vs 2.67; output (Judge 2) 3.00 vs 2.92
- relnotes, D vs B: output (Judge 1) 1.17 vs 2.33; output (Judge 2) 1.58 vs 2.75
- relnotes, D vs R: output (Judge 1) 1.17 vs 2.33; output (Judge 2) 1.58 vs 2.75

## Raw prompts (hand-written, verbatim)

**duration:**

```
write a python function parse_duration(s) that turns strings like "1h30m" into a number of seconds. stdlib only
```

**csat:**

```
attached is our support CSAT export (csat.csv). CSAT dropped last month. what happened and what should we do about it?
```

**jobpost:**

```
write a job post for a senior backend engineer
```

**trial:**

```
we're thinking of moving our free trial from 14 to 30 days. my notes are below (notes.md). should we?
```

**relnotes:**

```
turn the changelog below (changelog.md) into customer-facing release notes for Ledgerly v4.2. group them under New, Improved and Fixed. leave out internal-only changes. put anything that breaks existing setups at the very top with what customers need to do. plain language, no PR numbers, under 300 words.
```
