# Bench v4: fresh held-out set

Pre-registered on 2026-10-31, before any v4 arm ran. v3 stopped being a clean held-out set when its failures were used to fix the skill (deviation 12 in `../README.md`). These five tasks were written after the last skill change (`c6aa381`) and are never used to tune the skill.

## Tasks
| Task | Kind | Objective check |
|---|---|---|
| bizdays | coding | hidden tests (`hidden_tests/test_bizdays.py`, 19 tests; the reference passes 19/19, a naive day-by-day loop 6/19) |
| activation | data analysis (26-row CSV) | answer key `tasks/activation/truth.md`, numbers from `make_data.py` (a seasonal rise read as a launch effect, an incomplete last month) |
| outage | writing for an audience | fact list in `truth.md`; every fact lives only in the persona |
| flags | decision from supplied sources | requirements, cost math, scale mismatch and seat-count points in `truth.md` |
| actions | transformation of a supplied transcript; the raw prompt is already fully specified | exact rows in `truth.md`. Control: asking questions should add nothing, so it checks that the skill does no harm |

Each task has a raw prompt (`prompt.txt`), a persona with a hidden goal (`personas/`), and an answer key the judges see but the methods don't.

## Arms
A raw prompt · B prompt-master (vendored, MIT) · R ckelsoe/prompt-architect v3.5.1 (same file and commit as v2/v3) · D ambition-prompt (`skills/ambition-prompt/SKILL.md` at the commit that adds this file).

## Roles
- Optimizer, simulated user and executor: `claude-sonnet-5-5` through the Anthropic Messages API, as in v3. Up to 3 question rounds; n = 2 executor samples per (task, arm).
- Judges, non-Claude only, same rubric (`../RUBRIC.md`), anonymized and shuffled, pairwise in both orders:
  - **Judge 1 (primary): NVIDIA `nvidia/nemotron-3-ultra-550b-a55b`.** OpenAI is out of credits (`credit_balance_exhausted` on 2026-10-31), so it can't be the primary judge. nemotron was the strongest live free model in a quick check (GLM 5.3 and Kimi K3 are end-of-life). A re-judge of v3-r2 outputs with it (not v4) was started before this file was committed; its result is reported but doesn't change this choice.
  - Judge 2: NVIDIA `nvidia/nemotron-3.5-lightning-30b-a3b`. The v2/v3 judge `openai/gpt-oss-20b` timed out on every call on 2026-10-31, and `deepseek-ai/deepseek-v4.1-flash` returned empty JSON-mode replies and took ~2 minutes per call. Judge 2 shares a model family with judge 1, so their agreement is weak evidence.
- Spend caps: Anthropic $15 and 200 calls in total across runs (`runs/anthropic_spend.json`); no OpenAI calls.

## Decision rule (same thresholds as v2/v3, judge 1 in place of OpenAI)
ambition-prompt "beats the field" only if, against **each** of B and R, its pairwise win rate (judge 1, both orders, all tasks) is ≥ 0.60, **and** its mean judge-1 output score is higher on at least 3 of 5 tasks. A higher hidden-test pass rate on bizdays counts as "higher" for that task when judge-1 scores tie. Otherwise the README reports the honest result.

## Known limits
- Same author for the tasks and the skill (see v3). The control task and the mixed task kinds limit the bias; outside task authors would be better.
- Both judges are open models on NVIDIA's free tier, weaker than the planned OpenAI judge. v3 showed output scores moving by up to 0.5 between identical runs.
- One run, n = 2: no significance test.
