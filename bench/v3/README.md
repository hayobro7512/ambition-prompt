# Bench v3: fresh held-out set, run through the Anthropic API

Pre-registered on 2026-10-31, before any v3 arm ran. v2 stopped being a clean held-out set when its failures were used to fix the skill (deviation 10 in `../README.md`). These five tasks were written after the last skill change in this commit and are never used to tune the skill.

## Tasks
| Task | Kind | Objective check |
|---|---|---|
| duration | coding | hidden tests (`hidden_tests/test_duration.py`, 19 tests; the reference passes 19/19, a naive regex parser 6/19) |
| csat | data analysis (24-row CSV) | answer key `tasks/csat/truth.md`, numbers from `make_data.py` (mix shift, a planted false belief, a noisy week) |
| jobpost | writing for an audience | fact and cliché list in `truth.md` |
| trial | decision from supplied sources | evidence-quality, power and deadline-effect points in `truth.md` |
| relnotes | transformation of a supplied changelog; the raw prompt is already well specified | inclusion/exclusion list in `truth.md`. This is a control: asking questions should add little, so it checks that the skill does no harm to a good prompt |

Each task has a raw prompt (`prompt.txt`), a persona with a hidden goal (`personas/`), and an answer key the judges see but the methods don't.

## Arms
A raw prompt · B prompt-master (vendored, MIT) · R ckelsoe/prompt-architect v3.5.1 (same file and commit as v2) · D ambition-prompt (`skills/ambition-prompt/SKILL.md` at the commit that adds this file).

## Roles
- Optimizer, simulated user and executor: `claude-sonnet-5-5` through the Anthropic Messages API (`run.py --suite v3 --stage optimize` and `--stage execute`), default settings, the same model for every arm. This replaces v2's Claude Code subagents; the instructions are the same (`harness_note`, `SIMUSER_RULES`, persona), and the executor gets the final prompt plus the attachment as a single user message with no tools.
- Up to 3 question rounds; n = 2 executor samples per (task, arm).
- Judges, non-Claude only: OpenAI (`judge_oa`, cap 140 calls) as primary, NVIDIA `openai/gpt-oss-20b` as second, with the same rubric (`../RUBRIC.md`), anonymized and shuffled, pairwise in both orders. If the OpenAI account has no credits, the run is reported as NVIDIA-only and the decision rule is not applied.
- Spend caps: Anthropic $15 and 200 calls in total (`runs/anthropic_spend.json`), OpenAI 140 calls.

## Decision rule (same as v2, fixed in advance)
ambition-prompt "beats the field" only if, against **each** of B and R, its pairwise win rate (OpenAI judge, both orders, all tasks) is ≥ 0.60, **and** its mean OpenAI output score is higher on at least 3 of 5 tasks. Otherwise the README reports the honest result and what it is best at.

## Known limits
- The tasks were written by the same author who changed the skill, knowing its approach (it asks about edge behavior and user facts). The relnotes control and the mixed task kinds are there to limit that bias; outside task authors would be better.
- The simulated user answers truthfully from its persona, so arms that ask more get more facts. That is part of what is measured.
- One run, n = 2: no significance test.
