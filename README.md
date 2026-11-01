# ambition-prompt

A Claude Code skill that turns a rough prompt into the most ambitious version that can still be checked, then runs it.

It looks up the facts it can find, asks you only for decisions and facts that are yours, and raises the target: a higher outcome, the methods a top expert would use, and an outside check instead of the model grading itself. It writes the prompt as a contract (done criteria with worked examples, edge behavior, grounding, limits, output) and lints it before you see it. Ambition here means a deeper task, not a longer one. Every demand is capped by what the model running the prompt can actually do.

## Install

As a plugin:

```
/plugin marketplace add <this repo>
/plugin install ambition-prompt@ambition-prompt
```

Or copy `skills/ambition-prompt/` into `~/.claude/skills/`.

Use it with `/ambition-prompt <your prompt>`, or say "make this more ambitious".

## What it does

1. **Gathers facts silently**: files, data size, tools, and what the executor (the model that will run the prompt) can do.
2. **Drafts a plan along three axes**: the outcome behind the task, expert methods plus an outside judge, and the people the work calls for, including a hostile reviewer.
3. **Grills you in rounds**: at most 5 numbered questions per round, no recommended answers, result-changing edge cases treated as your call.
4. **Writes the contract and lints it**: preservation of every requirement at its original strength, feasibility, workload, length, and examples that obey the rules.
5. **Shows the prompt for approval**, then runs it in the same session.

## Benchmark: honest status

The goal was to beat prompt-master and ckelsoe/prompt-architect on held-out tasks, with Claude running every prompt and non-Claude judges blind-scoring the results. The decision rule was fixed in advance: against each rival, a pairwise win rate of at least 0.60 and a higher mean output score on at least 3 of 5 tasks. **It beats prompt-master but not prompt-architect, so the overall claim is not supported.**

Latest clean held-out run (v4-r1: five fresh tasks written after the last skill change, n = 2 samples per arm, Claude Sonnet 5.5 in every role, primary judge NVIDIA `nemotron-3-ultra`):

| | vs prompt-master | vs prompt-architect |
|---|---|---|
| Pairwise win rate (bar ≥ 0.60) | **0.62** | 0.50 |
| Tasks with higher mean output score (bar ≥ 3 of 5) | **3** | **3** |
| Hidden tests, coding task | 100% vs 26% | 100% vs 53% |

- **Where it wins:** tasks where the user's unstated choices decide the result. On the coding task, both of its samples passed all 19 hidden tests; the raw prompt got 68%. On a data question with a seasonal trap, it scored 3.00 of 3, against 1.83 and 2.17 for the rivals.
- **Where it loses:**
  - The control task, a prompt that was already fully specified. All three optimizers scored below the raw prompt there. This skill widened the user's "open questions" line and let back in ideas the user had excluded; a preservation fix followed, but it hasn't been tested.
  - The build-vs-buy decision memo, where prompt-architect's output was preferred.
- **Caveats:**
  - Both judges are free NVIDIA models from one family, because the planned OpenAI judge had no credits.
  - Scores move by up to 0.5 on the 0–3 scale between identical runs.
  - One author wrote both the tasks and the skill.
  - There is no significance test.

Full method, every protocol deviation and per-task results: `bench/README.md`, `bench/v2/`–`bench/v4/`. Raw model outputs stay local (NVIDIA trial terms); only aggregates are published. To reproduce, run `python3 bench/run.py --suite v4 --stage all` with `ANTHROPIC_API_KEY` and `NVIDIA_API_KEY` set (the role models and spend caps are in `bench/v4/README.md`).

## Credits

See `NOTICE`. The ambition framing comes from Felix Rieseberg's essay "How to Be More Ambitious: A Tutorial for Humans with Models". Several techniques are adapted from MIT-licensed skills (Matt Pocock's `grilling`, prompt-master, prompt-architect and others), each credited there.

MIT License.
