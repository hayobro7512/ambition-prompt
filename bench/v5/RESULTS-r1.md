# Results — run `v5-r1`

Aggregate numbers computed by `run.py report`. No model-generated text is reproduced here (NVIDIA trial terms); run `python3 run.py --stage report --excerpts` locally to see prompts and outputs.

Models: optimizer `claude-sonnet-5-5`, simulated user `claude-sonnet-5-5`, executor `claude-sonnet-5-5`, judge 1 (primary) `gpt-5.6-sol`, judge 2 `poolside/laguna-xs-2.1`. Seed 7. n=2 executor samples per arm per task. OpenAI calls used: 56/70.

Headline metrics are the hidden-test pass rate (task 1) and output quality (both tasks). The prompt score partly rewards what ambition-prompt asks for; treat it as secondary.

## Task: versions

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Hidden tests pass rate | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|---|
| A raw prompt | 1.83 ± 0.00 | 0.58 ± 0.82 | -0.11 ± 0.03 / -0.03 ± 0.96 | 88% ± 4% | 1912 ± 166 | 0.88 / 1.12 | 116 | 0 |
| B prompt-master | 1.83 ± 0.24 | 1.50 ± 0.71 | -0.54 ± 0.26 / -0.74 ± 0.61 | 90% ± 0% | 5586 ± 360 | 2.62 / 1.88 | 2065 | 0 |
| R rival | 2.83 ± 0.00 | 2.92 ± 0.12 | +0.47 ± 0.03 / +0.72 ± 0.02 | 100% ± 0% | 5440 ± 342 | 2.5 / 3.0 | 4312 | 1 |
| D ambition-prompt | 2.33 ± 0.00 | 1.50 ± 0.71 | +0.17 ± 0.05 / +0.06 ± 0.50 | 100% ± 0% | 3312 ± 453 | 2.88 / 3.0 | 3749 | 2 |

Hidden-test failures (count of samples failing, per arm):

| Test | A | B | R | D |
|---|---|---|---|---|
| test_ascii_order_in_prerelease | 1 | 0 | 0 | 0 |
| test_malformed_suffix_raises | 2 | 2 | 0 | 0 |
| test_non_strings_raise_type_error | 2 | 2 | 0 | 0 |

## Task: handle

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.50 ± 0.00 | 2.92 ± 0.12 | +0.04 ± 0.03 / +0.09 ± 0.13 | 1908 ± 101 | 0.38 / 0.0 | 141 | 0 |
| B prompt-master | 2.42 ± 0.12 | 2.50 ± 0.71 | -0.09 ± 0.09 / -0.30 ± 0.70 | 1769 ± 72 | 2.38 / 2.88 | 2615 | 0 |
| R rival | 2.25 ± 0.35 | 3.00 ± 0.00 | +0.02 ± 0.34 / +0.07 ± 0.01 | 2790 ± 73 | 2.12 / 2.88 | 3091 | 0 |
| D ambition-prompt | 2.75 ± 0.12 | 2.83 ± 0.24 | +0.02 ± 0.10 / +0.14 ± 0.23 | 1224 ± 30 | 2.38 / 3.0 | 3736 | 1 |

## Task: cancel

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 0.83 ± 0.00 | 0.00 ± 0.00 | -0.16 ± 0.06 / -0.21 ± 0.09 | 1490 ± 29 | 0.88 / 0.0 | 68 | 0 |
| B prompt-master | 2.50 ± 0.00 | 2.92 ± 0.12 | -0.39 ± 0.17 / -0.43 ± 0.40 | 779 ± 45 | 2.0 / 3.0 | 2070 | 1 |
| R rival | 2.67 ± 0.00 | 2.92 ± 0.12 | +0.13 ± 0.11 / +0.15 ± 0.30 | 878 ± 33 | 2.12 / 3.0 | 2634 | 1 |
| D ambition-prompt | 2.75 ± 0.12 | 2.92 ± 0.12 | +0.42 ± 0.01 / +0.49 ± 0.30 | 942 ± 35 | 2.12 / 3.0 | 2504 | 1 |

## Task: faq

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.08 ± 0.12 | 3.00 ± 0.00 | -0.19 ± 0.02 / +0.00 ± 0.00 | 875 ± 18 | 1.25 / 0.0 | 390 | 0 |
| B prompt-master | 2.50 ± 0.00 | 3.00 ± 0.00 | +0.14 ± 0.08 / +0.00 ± 0.00 | 858 ± 14 | 1.62 / 2.0 | 1267 | 0 |
| R rival | 2.50 ± 0.00 | 3.00 ± 0.00 | +0.12 ± 0.06 / +0.00 ± 0.00 | 855 ± 11 | 1.62 / 2.0 | 1574 | 0 |
| D ambition-prompt | 2.50 ± 0.00 | 3.00 ± 0.00 | -0.07 ± 0.02 / +0.00 ± 0.00 | 820 ± 4 | 1.88 / 2.0 | 2090 | 1 |

## Task: lease

| Arm | Output score (OpenAI) | Output score (NVIDIA) | Length-controlled (OpenAI / NVIDIA) | Output chars | Prompt score (OpenAI / NVIDIA) | Prompt chars | Q&A rounds |
|---|---|---|---|---|---|---|---|
| A raw prompt | 2.50 ± 0.47 | 2.83 ± 0.24 | +0.03 ± 0.50 / -0.03 ± 0.25 | 2894 ± 272 | 0.75 / 0.0 | 85 | 0 |
| B prompt-master | 2.50 ± 0.00 | 3.00 ± 0.00 | +0.15 ± 0.01 / +0.07 ± 0.00 | 4323 ± 107 | 2.0 / 3.0 | 2574 | 0 |
| R rival | 2.00 ± 0.71 | 2.83 ± 0.24 | -0.34 ± 0.71 / -0.10 ± 0.23 | 4548 ± 23 | 2.0 / 3.0 | 2770 | 0 |
| D ambition-prompt | 2.50 ± 0.24 | 3.00 ± 0.00 | +0.16 ± 0.23 / +0.07 ± 0.00 | 4478 ± 18 | 2.88 / 3.0 | 4059 | 1 |

## Prompt rubric by criterion (mean over tasks and both judges, 0–3)

| Arm | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | Infeasible-demand flags (judge-listed / keyword hits) |
|---|---|---|---|---|---|---|---|---|---|
| A raw prompt | 0.20 | 0.30 | 0.00 | 0.30 | 0.20 | 0.50 | 1.10 | 1.60 | 3 / 0 |
| B prompt-master | 2.00 | 2.50 | 2.10 | 2.50 | 2.30 | 2.70 | 2.00 | 2.60 | 2 / 2 |
| R rival | 2.20 | 2.60 | 2.20 | 2.60 | 2.50 | 2.70 | 2.20 | 2.40 | 3 / 1 |
| D ambition-prompt | 2.70 | 2.70 | 2.50 | 2.60 | 2.70 | 2.90 | 2.30 | 2.50 | 2 / 4 |

P1 altitude, P2 depth, P3 range, P4 done criteria + outside judge, P5 limits/stop rules, P6 output spec, P7 consistency, P8 concision.

## Pairwise (D vs competitor, both orderings, per executor sample)

D win rate = (D wins + 0.5 × ties) / comparisons. Position-consistent = same winner in both orderings.

| Task | Pair | Judge | D wins | Ties | D losses | D win rate | Position-consistent |
|---|---|---|---|---|---|---|---|
| versions | D vs B | OpenAI | 4 | 0 | 0 | 1.00 | 2/2 |
| versions | D vs B | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| versions | D vs R | OpenAI | 3 | 0 | 1 | 0.75 | 1/2 |
| versions | D vs R | NVIDIA | 0 | 0 | 4 | 0.00 | 2/2 |
| handle | D vs B | OpenAI | 4 | 0 | 0 | 1.00 | 2/2 |
| handle | D vs B | NVIDIA | 3 | 0 | 1 | 0.75 | 1/2 |
| handle | D vs R | OpenAI | 4 | 0 | 0 | 1.00 | 2/2 |
| handle | D vs R | NVIDIA | 1 | 0 | 3 | 0.25 | 1/2 |
| cancel | D vs B | OpenAI | 4 | 0 | 0 | 1.00 | 2/2 |
| cancel | D vs B | NVIDIA | 2 | 0 | 2 | 0.50 | 0/2 |
| cancel | D vs R | OpenAI | 4 | 0 | 0 | 1.00 | 2/2 |
| cancel | D vs R | NVIDIA | 2 | 0 | 2 | 0.50 | 0/2 |
| faq | D vs B | OpenAI | 1 | 3 | 0 | 0.62 | 1/2 |
| faq | D vs B | NVIDIA | 2 | 0 | 2 | 0.50 | 0/2 |
| faq | D vs R | OpenAI | 0 | 4 | 0 | 0.50 | 2/2 |
| faq | D vs R | NVIDIA | 2 | 0 | 2 | 0.50 | 0/2 |
| lease | D vs B | OpenAI | 2 | 0 | 2 | 0.50 | 2/2 |
| lease | D vs B | NVIDIA | 2 | 0 | 2 | 0.50 | 2/2 |
| lease | D vs R | OpenAI | 4 | 0 | 0 | 1.00 | 2/2 |
| lease | D vs R | NVIDIA | 4 | 0 | 0 | 1.00 | 2/2 |
| all | D vs B | OpenAI | 15 | 3 | 2 | 0.82 | 9/10 |
| all | D vs B | NVIDIA | 9 | 0 | 11 | 0.45 | 5/10 |
| all | D vs R | OpenAI | 15 | 4 | 1 | 0.85 | 9/10 |
| all | D vs R | NVIDIA | 9 | 0 | 11 | 0.45 | 5/10 |

## Judge agreement (OpenAI vs NVIDIA)

- Output scores: Pearson r = 0.73 (n=40); mean absolute difference = 0.56
- Prompt scores: Pearson r = 0.86 (n=20)
- Pairwise winners: 18/40 comparisons agree

## Length vs score

- Pearson r between output chars and output score: OpenAI -0.06 (n=40), NVIDIA -0.07 (n=40)

## Verdict on headline metrics (D vs B and R; n=2, no significance test)

- versions, D vs B: tests 100% vs 90%; output (OpenAI) 2.33 vs 1.83; output (NVIDIA) 1.50 vs 1.50
- versions, D vs R: tests 100% vs 100%; output (OpenAI) 2.33 vs 2.83; output (NVIDIA) 1.50 vs 2.92
- handle, D vs B: output (OpenAI) 2.75 vs 2.42; output (NVIDIA) 2.83 vs 2.50
- handle, D vs R: output (OpenAI) 2.75 vs 2.25; output (NVIDIA) 2.83 vs 3.00
- cancel, D vs B: output (OpenAI) 2.75 vs 2.50; output (NVIDIA) 2.92 vs 2.92
- cancel, D vs R: output (OpenAI) 2.75 vs 2.67; output (NVIDIA) 2.92 vs 2.92
- faq, D vs B: output (OpenAI) 2.50 vs 2.50; output (NVIDIA) 3.00 vs 3.00
- faq, D vs R: output (OpenAI) 2.50 vs 2.50; output (NVIDIA) 3.00 vs 3.00
- lease, D vs B: output (OpenAI) 2.50 vs 2.50; output (NVIDIA) 3.00 vs 3.00
- lease, D vs R: output (OpenAI) 2.50 vs 2.00; output (NVIDIA) 3.00 vs 2.83

## Raw prompts (hand-written, verbatim)

**versions:**

```
write a python function compare_versions(a, b) that compares two version strings and returns -1, 0 or 1. stdlib only
```

**handle:**

```
attached is last quarter's handle-time data for our support agents (handle.csv). who's slowest? i have budget to send one person to coaching.
```

**cancel:**

```
write a note to my team telling them we're cancelling Project Harbor
```

**faq:**

```
turn the policy below (policy.md) into a customer FAQ with exactly 5 questions, in this order: how long do i have to return something, what can't be returned, when do i get my refund, who pays return shipping, how do i start a return. each answer under 40 words. plain language. leave out anything internal (team names, fraud rules, staff discount stuff). output only the FAQ, nothing else.
```

**lease:**

```
our office lease is up in june. notes below (notes.md). renew, downsize or go remote?
```
