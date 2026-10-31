# Bench v2: held-out, Claude-run, blind-judged

Pre-registered on 2026-10-30, before any change to the skill made after this date and before any v2 arm ran. The v1 tasks (dedupe, churn) are now the **dev set** for tuning. These five tasks are the **held-out set** and are never used to tune the skill.

## Tasks
| Task | Kind | Objective check |
|---|---|---|
| split | coding | hidden tests (`hidden_tests/test_split.py`, 19 tests; the reference passes 19/19, a naive split passes 8/19) |
| abtest | data analysis (56-row CSV) | answer key `tasks/abtest/truth.md`, computed by `make_data.py` |
| priceemail | writing for an audience | fact and forbidden-claim list in `truth.md` |
| queue | research from supplied sources | conflict, headroom math and constraint list in `truth.md` |
| referral | planning / spec | requirement list in `truth.md` |

Each task has a lazy raw prompt (`prompt.txt`), a persona with a hidden goal (`personas/`), and an answer key the judges see but the methods don't.

## Arms
A raw prompt · B prompt-master (vendored, MIT) · R the strongest other GitHub prompting skill (chosen by `../survey.md` before any run; see the addendum below) · D ambition-prompt (`skills/ambition-prompt/SKILL.md` at run time).

## Roles (all Claude, run as Claude Code subagents, model `sonnet`, the same model for every arm)
- **Optimizer.** System instructions = the arm's instruction file + `run.py`'s `harness_note(task)`, which is identical for all arms. Up to 3 question rounds.
- **Simulated user.** One subagent per (task, arm): `SIMUSER_RULES` + persona. It is continued across rounds, so it remembers the conversation.
- **Executor.** One fresh subagent per sample, n = 2 per (task, arm). It gets the final prompt + attachment and writes one reply as a plain chat model would: no tools for the work itself.
- **Transport.** Messages move through files under `runs/<id>/claude/`. The only tool use a role may make is reading its inbox file and writing its outbox file. This is a known limit of the honour system: subagents have tools available, and they are told to use them only for delivery.
- **Judges.** Non-Claude only, to avoid self-preference: OpenAI (`judge_oa`, cap 150 calls for v2) and NVIDIA `gpt-oss-20b`, via `run.py --suite v2 --stage judge`, with the same rubric (`../RUBRIC.md`), anonymized and shuffled, pairwise in both orders.

## Decision rule (fixed in advance)
ambition-prompt "beats the field" only if, against **each** of B and R, its pairwise win rate (OpenAI judge, both orders, all tasks) is ≥ 0.60, **and** its mean OpenAI output score is higher on at least 3 of 5 tasks. Otherwise the README reports the honest result and what it is best at.

## Iteration
If D loses: diagnose on the dev set (free NVIDIA pipeline, v1 tasks), make only general fixes, then re-run D on the held-out set once and report both rounds. Budget: 100 subagent runs and 150 OpenAI calls in total.

## Reproduce
In Claude Code: follow the role definitions above (or `runs/<id>/claude/` packets), then `python3 run.py --suite v2 --run runs/<id> --stage judge` and `--stage report` with `OPENAI_API_KEY` and `NVIDIA_API_KEY` set.

## Addendum: rival choice
(filled in from survey.md before the first run)
