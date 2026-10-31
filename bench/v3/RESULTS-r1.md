# Results — run `v3-r1`

Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here (NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.

Models: optimizer `claude-sonnet-5-5`, simulated user `claude-sonnet-5-5`, executor `claude-sonnet-5-5`, judge 1 (primary) `gpt-5.6-sol`, judge 2 `openai/gpt-oss-20b`. Seed 7. n=2 executor samples per arm per task. OpenAI calls used: 56/140.

Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.

## Task: duration

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Hidden tests pass rate | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.00 ± 0.00 | n/a / +0.00 ± 0.00 | 71% ± 4% | 1397 ± 116 | None / 0.75 | 111 | 0 |
| B prompt-master | n/a | 0.00 ± 0.00 | n/a / +0.00 ± 0.00 | 79% ± 0% | 2930 ± 56 | None / 2.0 | 2011 | 0 |
| R rival | n/a | 0.00 ± 0.00 | n/a / +0.00 ± 0.00 | 68% ± 0% | 3822 ± 252 | None / 1.88 | 1999 | 0 |
| D ambition-prompt | n/a | 0.00 ± 0.00 | n/a / +0.00 ± 0.00 | 89% ± 0% | 3434 ± 67 | None / 2.12 | 3227 | 1 |

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

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 2.25 ± 0.12 | n/a / -0.18 ± 0.27 | 2796 ± 392 | None / 0.0 | 118 | 0 |
| B prompt-master | n/a | 2.92 ± 0.12 | n/a / -0.01 ± 0.07 | 4346 ± 206 | None / 2.12 | 2897 | 0 |
| R rival | n/a | 3.00 ± 0.00 | n/a / -0.08 ± 0.04 | 4980 ± 192 | None / 2.12 | 3550 | 0 |
| D ambition-prompt | n/a | 3.00 ± 0.00 | n/a / +0.27 ± 0.09 | 3644 ± 299 | None / 2.38 | 5056 | 1 |

## Task: jobpost

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.00 ± 0.00 | n/a / -0.03 ± 0.04 | 4297 ± 68 | None / 0.75 | 46 | 0 |
| B prompt-master | n/a | 0.00 ± 0.00 | n/a / -0.79 ± 0.05 | 3156 ± 60 | None / 3.0 | 2668 | 0 |
| R rival | n/a | 2.92 ± 0.12 | n/a / +1.59 ± 0.18 | 2532 ± 63 | None / 3.0 | 4274 | 1 |
| D ambition-prompt | n/a | 1.17 ± 0.24 | n/a / -0.77 ± 0.08 | 1979 ± 127 | None / 3.0 | 4020 | 1 |

## Task: trial

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 2.50 ± 0.71 | n/a / -0.21 ± 0.72 | 3162 ± 200 | None / 0.75 | 101 | 0 |
| B prompt-master | n/a | 3.00 ± 0.00 | n/a / +0.26 ± 0.00 | 3566 ± 43 | None / 2.12 | 2619 | 0 |
| R rival | n/a | 2.50 ± 0.71 | n/a / -0.27 ± 0.71 | 4032 ± 139 | None / 2.25 | 2109 | 0 |
| D ambition-prompt | n/a | 3.00 ± 0.00 | n/a / +0.22 ± 0.00 | 4308 ± 90 | None / 2.88 | 6749 | 1 |

## Task: relnotes

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 2.33 ± 0.24 | n/a / -0.08 ± 0.24 | 1227 ± 16 | None / 1.75 | 305 | 0 |
| B prompt-master | n/a | 2.50 ± 0.00 | n/a / +0.08 ± 0.00 | 1170 ± 107 | None / 1.62 | 1925 | 0 |
| R rival | n/a | 2.50 ± 0.00 | n/a / +0.08 ± 0.00 | 1026 ± 18 | None / 1.62 | 1851 | 0 |
| D ambition-prompt | n/a | 2.33 ± 0.24 | n/a / -0.09 ± 0.24 | 960 ± 5 | None / 1.75 | 3881 | 1 |

## Prompt rubric by criterion (mean over tasks and both judges, 0–3)

| Arm | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Infeasible-demand flags (judge-listed / keyword hits) |
|---|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.40 | 0.00 | 0.00 | 0.40 | 0.20 | 0.60 | 2.40 | 2.40 | 0 / 0 |
| B prompt-master | 2.20 | 2.20 | 1.20 | 2.20 | 1.60 | 2.80 | 3.00 | 2.20 | 0 / 0 |
| R rival | 2.40 | 1.80 | 1.20 | 2.20 | 1.80 | 2.80 | 3.00 | 2.20 | 0 / 1 |
| D ambition-prompt | 3.00 | 2.40 | 1.40 | 2.40 | 2.00 | 3.00 | 3.00 | 2.20 | 0 / 3 |

P1 altitude, P2 depth, P3 range, P4 done criteria + outside judge, P5 limits/stop rules, P6 output spec, P7 consistency, P8 concision.

## Pairwise (D vs competitor, both orderings, per executor sample)

D win rate = (D wins + 0.5 × ties) / comparisons. Position-consistent = same winner in both orderings.

| Task | Pair | Judge | D wins | Ties | D losses | D win rate | Position-consistent |
|---|---|---|---|---|---|---|---|
| duration | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| duration | D vs B | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| duration | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| duration | D vs R | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| csat | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| csat | D vs B | NVIDIA | 2 | 0 | 2 | 0.50 | 2/2 |
| csat | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| csat | D vs R | NVIDIA | 2 | 0 | 2 | 0.50 | 2/2 |
| jobpost | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| jobpost | D vs B | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| jobpost | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| jobpost | D vs R | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| trial | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| trial | D vs B | NVIDIA | 1 | 0 | 3 | 0.25 | 1/2 |
| trial | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| trial | D vs R | NVIDIA | 1 | 0 | 3 | 0.25 | 1/2 |
| relnotes | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| relnotes | D vs B | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| relnotes | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| relnotes | D vs R | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| all | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| all | D vs B | NVIDIA | 11 | 0 | 9 | 0.55 | 9/10 |
| all | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| all | D vs R | NVIDIA | 7 | 0 | 13 | 0.35 | 9/10 |

## Judge agreement (OpenAI vs NVIDIA)

- Output scores: n/a
- Prompt scores: Pearson r = n/a
- Pairwise winners: 0/0 comparisons agree

## Length vs score

- Pearson r between output chars and output score: OpenAI n/a, NVIDIA 0.03 (n=40)

## Verdict on headline metrics (D vs B and C; n=3, no significance test)

- duration, D vs B: tests 89% vs 79%; output (OpenAI) n/a; output (NVIDIA) 0.00 vs 0.00
- duration, D vs R: tests 89% vs 68%; output (OpenAI) n/a; output (NVIDIA) 0.00 vs 0.00
- csat, D vs B: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 2.92
- csat, D vs R: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 3.00
- jobpost, D vs B: output (OpenAI) n/a; output (NVIDIA) 1.17 vs 0.00
- jobpost, D vs R: output (OpenAI) n/a; output (NVIDIA) 1.17 vs 2.92
- trial, D vs B: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 3.00
- trial, D vs R: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 2.50
- relnotes, D vs B: output (OpenAI) n/a; output (NVIDIA) 2.33 vs 2.50
- relnotes, D vs R: output (OpenAI) n/a; output (NVIDIA) 2.33 vs 2.50

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
