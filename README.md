# ambition-prompt

A Claude Code skill that turns a rough prompt into the most ambitious version that can still be checked, then runs it.

It looks up the facts it can find, asks you only for decisions and facts that are yours, and raises the target: a higher outcome, the methods a top expert would use, and an outside check instead of the model grading itself. It writes the prompt as a contract (done criteria with worked examples, edge behavior, grounding, limits, output) and lints it before you see it. Ambition here means a deeper task, not a longer one. Every demand is capped by what the model running the prompt can actually do.

## Install

As a plugin:

```
/plugin marketplace add hayobro7512/ambition-prompt
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

The goal was to beat prompt-master and ckelsoe/prompt-architect on held-out tasks, with Claude running every prompt and non-Claude judges blind-scoring the results. The decision rule was fixed before each run: against each rival, a pairwise win rate of at least 0.60 and a higher mean output score on at least 3 of 5 tasks.

**The latest clean run met that rule against both rivals, on its primary judge. The second judge doesn't back it up, and the margin on substance is small.** Treat it as promising, not proven.

Latest run (v5-r1: five fresh tasks written after the last skill change, n = 2 samples per arm, Claude Sonnet 5.5 in every role, primary judge OpenAI `gpt-5.6-sol`):

| | vs prompt-master | vs prompt-architect |
|---|---|---|
| Pairwise win rate (bar ≥ 0.60) | **0.82** | **0.85** |
| Tasks with higher mean output score (bar ≥ 3 of 5) | **3** | **3** |
| Hidden tests, coding task | 100% vs 90% | 100% vs 100% |
| Second judge's pairwise win rate (`laguna-xs-2.1`) | 0.45 | 0.45 |

Read that table with these in mind:

- **The second judge disagrees.** The judges picked the same winner in only 18 of 40 comparisons. The second judge chose whichever output it saw first in 30 of 40, which suggests a position effect, while the primary judge showed no such lean.
- **On substance, the optimizers were close.** Keyword checks against the answer keys found that every arm, including the raw prompt, reached the right recommendation on the data and decision tasks. The wins mostly reflect fit to the brief. On the coding task prompt-architect tied on hidden tests and scored higher with the primary judge.
- **It hasn't always won.** The previous clean run (v4-r1) met the rule against prompt-master but not prompt-architect (win rate 0.50). The skill was then fixed using v4's failures, so v5 tests a newer version on new tasks, and the fixes rest on that one run.
- **The evidence is thin:** one run, two samples per arm, no significance test, and one author for both the tasks and the skill. The primary judge replaced an overloaded NVIDIA model before any scores were seen (logged as a deviation).

**Where it helps most:** tasks where the user's unstated choices or facts decide the result. Against the raw prompt, it took a team announcement from placeholders to a note with the real facts, and in v4 it took a coding task from 68% to 100% of hidden tests.

**Where to be careful:** prompts that are already complete. It still asks more questions than they need. In the latest run that did no harm, but earlier runs lost those tasks.

Full method, every protocol deviation and per-task results: `bench/README.md`, `bench/v2/`–`bench/v5/`. Raw model outputs stay local (NVIDIA trial terms); only aggregates are published. To reproduce, run `python3 bench/run.py --suite v5 --stage all --optimizer claude-sonnet-5-5 --simuser claude-sonnet-5-5 --executor claude-sonnet-5-5 --judge-nv poolside/laguna-xs-2.1` with `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` and `NVIDIA_API_KEY` set (spend caps are in `bench/run.py`).

## Beta testing

Real use is the evidence this benchmark can't give, so reports are very welcome. Please [open an issue](https://github.com/hayobro7512/ambition-prompt/issues) with:

- the prompt you started with, with anything private removed;
- whether the questions helped or got in your way;
- whether the final result beat what you'd have got without the skill, and why.

## Credits

See `NOTICE`. The ambition framing comes from Felix Rieseberg's essay "How to Be More Ambitious: A Tutorial for Humans with Models". Several techniques are adapted from MIT-licensed skills (Matt Pocock's `grilling`, prompt-master, prompt-architect and others), each credited there.

MIT License.
