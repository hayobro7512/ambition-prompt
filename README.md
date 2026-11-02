# ambition-prompt

**Get the most ambitious version of what you're asking for, then have Claude do it.**

A Claude Code skill that turns a rough prompt into a higher target with a real way to check the result. It asks only for the decisions and facts that are yours, writes the prompt as a contract, and runs it once you approve.

## Install

```
/plugin marketplace add hayobro7512/ambition-prompt
/plugin install ambition-prompt@ambition-prompt
```

Or copy `skills/ambition-prompt/` into `~/.claude/skills/`.

## Usage

```
/ambition-prompt write a python function that counts business days between two dates
/ambition-prompt attached is our support data. who should get coaching?
/ambition-prompt write a note to my team telling them we're cancelling the project
/ambition-prompt our office lease is up in June. renew, downsize or go remote?
```

Or just say "make this more ambitious" or "aim higher".

## What it does

- **Aims higher.** It works out what you actually want to happen next, then raises the target: a better outcome, the methods a top expert would use, and the traps they'd check for.
- **Asks only what's yours.** It looks up what it can find. You get a short round of numbered questions covering just your decisions and the facts only you have, so you can reply "Q2: 1".
- **Builds in a real check.** Done criteria, worked examples and an outside judge such as tests, a script or a reviewer, so the model isn't grading its own work.
- **Asks only for what can be delivered.** Every demand is capped by what the model running the prompt can really do, so depth doesn't turn into invented numbers.
- **Keeps your requirements intact.** A final lint checks that every requirement and ban survives at the strength you gave it, then checks feasibility, workload and length.
- **Does the work.** Once you approve the prompt, it runs in the same session and finishes by running the check.

## Before and after

A real example from our benchmark (Project Harbor and its team are fictional). The prompt:

> write a note to my team telling them we're cancelling Project Harbor

**Sent as is,** the model has to guess, so it leaves gaps:

> I wanted to share some difficult news: we've decided to cancel Project Harbor, effective [date].
>
> [Brief reason, e.g., "This decision comes after a review of shifting company priorities and resource constraints."...]

**With ambition-prompt,** it first asks what should happen after people read the note, how much of the reason to share, and for the facts only you have. Then it writes:

> Team, Harbor is cancelled, and there are no layoffs.
>
> The CEO and CFO made the call on Thursday, and it's final. Both design partners pulled out, one in September and one in October, and our 2027 revenue projection fell from $4M to under $1M. That is the reason. It was not the team's work.
>
> You spent eight months on Harbor, including the nights before the September demo, and I know it's hard to watch that work stop.
>
> Here's what happens next. 9 of you move to Dispatch and 5 move to Billing Reliability. The rate-normalization library moves into Dispatch, and the rest of the code is archived. Q4 bonuses are not affected. I'm not saying who goes where here, because I'll confirm that with each of you personally.
>
> - 1:1s with me on Monday and Tuesday
> - Assignments confirmed by Wednesday, Nov 4
> - Team Q&A on Thursday at 2 p.m.
>
> Bring any questions to me. The Thursday Q&A is open to any question you have.
>
> Noor

## Best for

**Where it scored best across our last two benchmark runs:**

| Kind of work | Example tasks | Result |
|---|---|---|
| **Data questions with a trap** | A seasonal rise that looks like a launch win; an overall average that points at the wrong person | Highest score of all four approaches in both runs |
| **Code where edge cases decide** | Business-day counting; version comparison | Passed 100% of hidden tests on every sample in both runs |
| **Messages built on facts only you have** | An outage email to customers; a project cancellation | Highest or tied-highest score in both runs: 2.75 of 3, against 0.17 and 0.83 for the raw prompt |

**It's also built for ambitious projects.** It looks for the lasting outcome behind a task, not just the next deliverable. On long runs it tracks state in files, commits at milestones and stops to ask for missing access instead of quietly scaling the work down. It finishes by running the outside check.

**Use something lighter for** quick lookups and web searches, and for prompts that already say exactly what you want. Those don't need a round of questions.

## Benchmark

We test against two popular open-source prompting skills, [prompt-master](https://github.com/nidhinjs/prompt-master) and [prompt-architect](https://github.com/ckelsoe/prompt-architect), on tasks written fresh for each run. Claude runs every prompt, and judges from other model families score the anonymized outputs against answer keys. The pass bar is set before each run: against each rival, a head-to-head win rate of at least 0.60 and a higher score on at least 3 of 5 tasks.

**Latest run: it cleared the bar against both.** Five new tasks, two samples per approach, primary judge OpenAI GPT-5.6 Sol.

| | vs prompt-master | vs prompt-architect |
|---|---|---|
| Head-to-head win rate (bar: 0.60) | **0.82** | **0.85** |
| Tasks with a higher score (bar: 3 of 5) | **3** | **3** |
| Hidden tests on the coding task | **100%** vs 90% | **100%** vs 100% |

Method, every run and all judges' scores are in [`bench/README.md`](bench/README.md) and [`bench/v5/RESULTS-r1.md`](bench/v5/RESULTS-r1.md).

## Beta testing

Real use tells us what a benchmark can't, so reports are very welcome. Please [open an issue](https://github.com/hayobro7512/ambition-prompt/issues) with:

- the prompt you started with, with anything private removed;
- whether the questions helped or got in your way;
- whether the final result beat what you'd have got without the skill, and why.

## Credits

See `NOTICE`. The ambition framing comes from Felix Rieseberg's essay "How to Be More Ambitious: A Tutorial for Humans with Models". Several techniques are adapted from MIT-licensed skills (Matt Pocock's `grilling`, prompt-master, prompt-architect and others), each credited there.

MIT License.
