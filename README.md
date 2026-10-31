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

The goal was to beat prompt-master and ckelsoe/prompt-architect on held-out tasks, with Claude running every prompt and non-Claude judges blind-scoring the results. The decision rule was fixed in advance (`bench/v3/README.md`). **That claim is not yet supported.**

- The primary judge (OpenAI) had no credits for v2 or v3, so every v3 output was scored only by NVIDIA `openai/gpt-oss-20b`. This judge is crude, and its scores move by up to 0.5 on a 0–3 scale between identical runs.
- The latest run (v3-r2) followed a fix round that used v3's own failures, so it is not a clean held-out result.

Latest numbers (v3-r2, n = 2 samples per arm, NVIDIA judge):

| | vs prompt-master | vs prompt-architect |
|---|---|---|
| Pairwise win rate (bar ≥ 0.60) | 0.60 | 0.60 |
| Tasks with higher mean output score (bar ≥ 3 of 5) | 3 | 2 |
| Hidden tests, coding task | 89% vs 79% | 89% vs 68% |

Where it does well: tasks where the user's unstated choices decide the result (edge cases in code, facts only the user knows). Where it loses: an already well-specified rewrite task (release notes), where its questions added options that hurt the output.

Full method, every protocol deviation and per-task results: `bench/README.md`, `bench/v2/`, `bench/v3/`. Raw model outputs stay local (NVIDIA trial terms); only aggregates are published. To reproduce, run `python3 bench/run.py --suite v3 --stage all` with `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` and `NVIDIA_API_KEY` set (the role models and spend caps are in `bench/v3/README.md`).

## Credits

See `NOTICE`. The ambition framing comes from Felix Rieseberg's essay "How to Be More Ambitious: A Tutorial for Humans with Models". Several techniques are adapted from MIT-licensed skills (Matt Pocock's `grilling`, prompt-master, prompt-architect and others), each credited there.

MIT License.
