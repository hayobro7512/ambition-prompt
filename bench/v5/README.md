# Bench v5: fresh held-out set

Pre-registered on 2026-11-01, before any v5 arm ran. v4 stopped being a clean held-out set when its outputs were used to fix the skill (deviations 15 and 16 in `../README.md`). These five tasks were written after those fixes and are never used to tune the skill.

## Tasks
| Task | Kind | Objective check |
|---|---|---|
| versions | coding, against a known standard that the persona adds to | hidden tests (`hidden_tests/test_versions.py`, 20 tests; the reference passes 20/20, a naive numeric-tuple comparison 10/20) |
| handle | data analysis (11-row CSV) | answer key `tasks/handle/truth.md`, numbers from `make_data.py` (overall averages point at the wrong person because of ticket mix; a new hire's small sample looks fastest) |
| cancel | writing for an audience | fact list in `truth.md`; the facts live only in the persona, and two names must stay out |
| faq | transformation of a supplied policy; the raw prompt is already fully specified | exact answers and a list of things that must be absent in `truth.md`. Control: asking questions should add nothing, so it checks that the skill does no harm |
| lease | decision from supplied sources | 5-year cost math and traps in `truth.md` (going remote costs more than downsizing; a self-selected survey; a contract clause) |

The set deliberately includes the kind of task the skill has been weakest on (`faq`, like `relnotes` in v3 and `actions` in v4). Each task has a raw prompt (`prompt.txt`), a persona with a hidden goal (`personas/`), and an answer key the judges see but the methods don't.

## Arms
A raw prompt · B prompt-master (vendored, MIT) · R ckelsoe/prompt-architect v3.5.1 (same file and commit as v2–v4) · D ambition-prompt (`skills/ambition-prompt/SKILL.md` at the commit that adds this file).

## Roles
- Optimizer, simulated user and executor: `claude-sonnet-5-5` through the Anthropic Messages API, as in v3 and v4. Up to 3 question rounds; n = 2 executor samples per (task, arm).
- Judges, non-Claude only, same rubric (`../RUBRIC.md`), anonymized and shuffled, pairwise in both orders:
  - **Judge 1 (primary): OpenAI `gpt-5.6-sol`**, the primary judge planned since v2. It replaced NVIDIA `nvidia/nemotron-3-ultra-550b-a55b` after pre-registration and before any v5 score was seen, because nemotron kept returning overload errors (503, 504) on judging requests and the user added OpenAI credits (deviation 17 in `../README.md`).
  - Judge 2: NVIDIA `poolside/laguna-xs-2.1`. It replaces v4's `nemotron-3.5-lightning` because it comes from a different model family, so agreement between the judges means more. It is a code-focused model, and in a spot check it sometimes left a score out of its reply; such gaps are dropped, as in earlier runs. `openai/gpt-oss-20b`, `z-ai/glm-5.3-flash`, `deepseek-ai/deepseek-v4.1-flash` and `meta/llama-3.2-90b-vision-instruct` all timed out at 75 s on 2026-11-01.
- Spend caps: Anthropic $15 in total across runs (`runs/anthropic_spend.json`; the call cap was raised to 500 at the user's request); OpenAI $5.50 and 70 calls for this run.

## Decision rule (same thresholds as v2–v4)
ambition-prompt "beats the field" only if, against **each** of B and R, its pairwise win rate (judge 1, both orders, all tasks) is ≥ 0.60, **and** its mean judge-1 output score is higher on at least 3 of 5 tasks. A higher hidden-test pass rate on versions counts as "higher" for that task when judge-1 scores tie. Otherwise the README reports the honest result.

The repository is published after this run whatever the result, so the result can't decide whether it's reported.

## Known limits
- Same author for the tasks and the skill (see v3). The control task and the mixed task kinds limit the bias; outside task authors would be better.
- Judge 2 is a code-focused open model. v3 showed output scores moving by up to 0.5 between identical runs.
- One run, n = 2: no significance test.
