# Results — run `v3-r2`

Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here (NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.

Models: optimizer `claude-sonnet-5-5`, simulated user `claude-sonnet-5-5`, executor `claude-sonnet-5-5`, judge 1 (primary) `gpt-5.6-sol`, judge 2 `openai/gpt-oss-20b`. Seed 7. n=2 executor samples per arm per task. OpenAI calls used: 1/140.

Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.

## Task: duration

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Hidden tests pass rate | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.33 ± 0.47 | n/a / -0.16 ± 0.47 | 71% ± 4% | 1397 ± 116 | None / 0.75 | 111 | 0 |
| B prompt-master | n/a | 0.33 ± 0.47 | n/a / -0.14 ± 0.47 | 79% ± 0% | 2930 ± 56 | None / 2.25 | 2011 | 0 |
| R rival | n/a | 0.33 ± 0.47 | n/a / -0.13 ± 0.47 | 68% ± 0% | 3822 ± 252 | None / 2.0 | 1999 | 0 |
| D ambition-prompt | n/a | 0.92 ± 0.35 | n/a / +0.44 ± 0.35 | 89% ± 0% | 2390 ± 45 | None / 2.38 | 3307 | 2 |

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
| A raw prompt | n/a | 2.75 ± 0.12 | n/a / -0.07 ± 0.15 | 2796 ± 392 | None / 0.0 | 118 | 0 |
| B prompt-master | n/a | 3.00 ± 0.00 | n/a / +0.07 ± 0.01 | 4346 ± 206 | None / 2.0 | 2897 | 0 |
| R rival | n/a | 3.00 ± 0.00 | n/a / +0.04 ± 0.01 | 4980 ± 192 | None / 2.0 | 3550 | 0 |
| D ambition-prompt | n/a | 3.00 ± 0.00 | n/a / -0.04 ± 0.06 | 7084 ± 1877 | None / 2.5 | 6697 | 1 |

## Task: jobpost

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 0.00 ± 0.00 | n/a / +0.35 ± 0.06 | 4297 ± 68 | None / 0.62 | 46 | 0 |
| B prompt-master | n/a | 0.00 ± 0.00 | n/a / -0.90 ± 0.08 | 3156 ± 60 | None / 2.88 | 2668 | 0 |
| R rival | n/a | 2.42 ± 0.12 | n/a / +0.62 ± 0.02 | 2532 ± 63 | None / 2.88 | 4274 | 1 |
| D ambition-prompt | n/a | 2.42 ± 0.12 | n/a / -0.07 ± 0.08 | 2140 ± 18 | None / 2.88 | 4799 | 1 |

## Task: trial

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 2.75 ± 0.12 | n/a / -0.05 ± 0.15 | 3162 ± 200 | None / 0.5 | 101 | 0 |
| B prompt-master | n/a | 2.92 ± 0.12 | n/a / +0.05 ± 0.11 | 3566 ± 43 | None / 2.25 | 2619 | 0 |
| R rival | n/a | 2.92 ± 0.12 | n/a / -0.01 ± 0.14 | 4032 ± 139 | None / 2.25 | 2109 | 0 |
| D ambition-prompt | n/a | 3.00 ± 0.00 | n/a / +0.01 ± 0.00 | 4580 ± 25 | None / 2.75 | 6384 | 1 |

## Task: relnotes

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | n/a | 2.75 ± 0.35 | n/a / +0.25 ± 0.32 | 1227 ± 16 | None / 1.75 | 305 | 0 |
| B prompt-master | n/a | 2.75 ± 0.35 | n/a / +0.11 ± 0.10 | 1170 ± 107 | None / 1.75 | 1925 | 0 |
| R rival | n/a | 2.75 ± 0.35 | n/a / -0.25 ± 0.40 | 1026 ± 18 | None / 1.75 | 1851 | 0 |
| D ambition-prompt | n/a | 1.58 ± 1.30 | n/a / -0.11 ± 1.29 | 1645 ± 6 | None / 1.75 | 3557 | 1 |

## Prompt rubric by criterion (mean over tasks and both judges, 0–3)

| Arm | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Infeasible-demand flags (judge-listed / keyword hits) |
|---|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.60 | 0.00 | 0.00 | 0.40 | 0.40 | 0.40 | 1.60 | 2.40 | 0 / 0 |
| B prompt-master | 2.00 | 2.00 | 1.20 | 2.40 | 2.00 | 2.80 | 3.00 | 2.40 | 1 / 0 |
| R rival | 2.20 | 1.80 | 1.20 | 2.40 | 1.60 | 2.80 | 3.00 | 2.40 | 1 / 1 |
| D ambition-prompt | 2.40 | 2.40 | 1.20 | 2.60 | 2.60 | 3.00 | 3.00 | 2.40 | 1 / 3 |

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
| csat | D vs B | NVIDIA | 1 | 0 | 3 | 0.25 | 1/2 |
| csat | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| csat | D vs R | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| jobpost | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| jobpost | D vs B | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| jobpost | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| jobpost | D vs R | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| trial | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| trial | D vs B | NVIDIA | 3 | 0 | 1 | 0.75 | 1/2 |
| trial | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| trial | D vs R | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| relnotes | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| relnotes | D vs B | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| relnotes | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| relnotes | D vs R | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| all | D vs B | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| all | D vs B | NVIDIA | 12 | 0 | 8 | 0.60 | 8/10 |
| all | D vs R | OpenAI | 0 | 0 | 0 | n/a | 0/0 |
| all | D vs R | NVIDIA | 12 | 0 | 8 | 0.60 | 10/10 |

## Judge agreement (OpenAI vs NVIDIA)

- Output scores: n/a
- Prompt scores: Pearson r = n/a
- Pairwise winners: 0/0 comparisons agree

## Length vs score

- Pearson r between output chars and output score: OpenAI n/a, NVIDIA 0.15 (n=40)

## Verdict on headline metrics (D vs B and C; n=3, no significance test)

- duration, D vs B: tests 89% vs 79%; output (OpenAI) n/a; output (NVIDIA) 0.92 vs 0.33
- duration, D vs R: tests 89% vs 68%; output (OpenAI) n/a; output (NVIDIA) 0.92 vs 0.33
- csat, D vs B: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 3.00
- csat, D vs R: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 3.00
- jobpost, D vs B: output (OpenAI) n/a; output (NVIDIA) 2.42 vs 0.00
- jobpost, D vs R: output (OpenAI) n/a; output (NVIDIA) 2.42 vs 2.42
- trial, D vs B: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 2.92
- trial, D vs R: output (OpenAI) n/a; output (NVIDIA) 3.00 vs 2.92
- relnotes, D vs B: output (OpenAI) n/a; output (NVIDIA) 1.58 vs 2.75
- relnotes, D vs R: output (OpenAI) n/a; output (NVIDIA) 1.58 vs 2.75

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
