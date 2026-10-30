---
name: ambition-prompt
description: Turn the user's prompt into the most ambitious version that can still be checked, then run it in this session once the user approves it. The skill grills the user for the facts it can't look up, sets the target with Felix Rieseberg's altitude, depth and range moves, writes a contract (done criteria, limits, output), and lints the prompt before review. Use when the user says "/ambition-prompt", "make this more ambitious", "ambition this", "aim higher", "improve this prompt and run it", or "what's the ambitious version of this prompt".
---

# Ambition prompt

Turn the user's prompt (the args, or their last request if no args) into the most ambitious version that still has a clear outcome and can be checked, then run it. Source: Felix Rieseberg, "How to Be More Ambitious: A Tutorial for Humans with Models" (2026-10-13), plus Anthropic's and OpenAI's prompting guides.

Aim for **a deeper version of the task, not a bigger one**. Ambition means a higher goal, more expert methods and a check from outside the model. It does not mean more words or more deliverables.

## 1. Gather facts silently

Before asking anything, find out what you can yourself: the files and repos involved, the connectors, tools and data that are available, and what a computer can install or run. Don't ask the user for facts you could look up.

Pin down the **executor**: whoever will run the final prompt, and what it can actually do there. That might be this session with tools, or a single-shot chat model with no tools. Every rung of ambition is capped by the executor's real capabilities. A method the executor can't carry out doesn't make the result deeper; it makes the executor invent results.

## 2. Draft the ambition tree

Work out where the prompt sits on each axis and what the next step up would be:

- **Altitude (outcome over task).** What does the user want to happen next? Move from "do X" to "make sure X keeps being true", then to "design a better system than the one that produces X". Ask what lasting workflow would remove the human from the loop, and what access that workflow needs, such as logs, version-to-commit maps, test machines or connectors.
- **Depth (work like a top expert in the field).**
  - What would a top professional do here that the prompt doesn't ask for?
  - What is the rawest material they'd start from?
  - Which real tools and methods would they use, such as databases, statistical models or simulations instead of markdown tables? Keep only the ones the executor can actually run on the data it has. Anything stronger becomes a prerequisite for the user to grant, not a demand in the prompt.
  - What unreasonable target can be stated as reasonable, like 200ms instead of 5s? It must be reachable by real work with the executor's tools and data. A target that can only be met by inventing numbers (a p-value, an AUC, a benchmark the executor can't run) produces fabrication, not depth.
  - Which belief should be tested against raw data?
  - What new knowledge could come out, such as a signal or prediction checked on data the model hasn't seen?
  - Above all, what **outside judge** checks the result? Prefer a tool the executor can run itself, never the model grading its own work. If the executor can't run anything, the judge sits outside the deliverable (the user's tests, a reviewer, real data next week), and the prompt asks only for what that judge needs, such as the computation shown or a short list of checks. It doesn't ask for a test suite or benchmark that would crowd out the main deliverable.
- **Range (bring in more fields).** Restate the task with verbs instead of nouns. A QBR is not "a deck"; it is "getting busy people to believe a cause-and-effect story and decide under uncertainty in 30 minutes". Then pick the crew those verbs call for, including a hostile red team. Each crew member must *do* that job's work, for example research the way a short seller does, never just *write like* one.

Skip Speed (the same work, faster), because it isn't ambition. Skip altitude for purely creative work, where it fits poorly.

## 3. Grill

Interview the user in **rounds** (method adapted from Matt Pocock's MIT-licensed `grilling` skill). The decision tree is the ambition tree from step 2 plus the contract from step 4.

Each round asks the whole **frontier**: every decision whose prerequisites are already settled. A question that depends on another open question waits for a later round. Format each question like this:

```
❓ **Q1** - **<title>**: <question>
   Why it matters: <one line on what changes in the prompt depending on the answer>
   Options: <2–4 concrete options, most ambitious first, or omit for open questions>
```

List the questions and let the user think. **Give no recommended answers and no assumed defaults**, so that each answer is the user's own decision and the user isn't anchored on yours. If the user replies "you pick" to a question, choose the most ambitious option that is feasible with the access available, and say which one you chose. Wait for the answers, then recompute the frontier. Finding facts is your job: look them up instead of asking. Making decisions is the user's job. Grilling is done when the frontier is empty and the user agrees you understand each other.

Ask only about decisions that would change the prompt. Settle everything else from the facts in step 1 or with a sensible default. Typical frontier questions:

- **Outcome.** The real outcome behind the prompt, and how high to aim (task, ongoing state, or a redesigned system).
- **Target.** The unreasonable-but-stated-as-reasonable target.
- **Done and judge.** What counts as done, and who or what judges it.
- **Raw material and tools.** The raw material and expert tools to use, and whether the user can grant access to them.
- **Crew.** The crew and red team.
- **Budget.** The budget and the room to fail: time, money and risk tolerance, and what is out of bounds.
- **Audience and format.** Who reads the output, and in what format.

Order the options so the most ambitious feasible one comes first. If a higher rung needs access the user doesn't have, include that option anyway and say exactly what access to grant.

## 4. Write the contract

The rewritten prompt must carry all of these:

- **Done criteria.** A condition the agent can check and that demands real work ("every churn segment tested on held-out data", not "analyze churn"), plus the outside judge that confirms it.
- **Stop and hand-back rules.**
  - When to stop.
  - What to do when stuck: decide, record the assumption in the notes and continue, or ask if the decision is irreversible.
  - When the task itself turns out to be infeasible: report that, rather than working around it.
- **Limits.**
  - Local, reversible actions (edits, test runs, scratch files) go ahead freely.
  - Deleting, force-pushing, sending messages, posting, spending money or changing shared systems need the user's yes.
  - The riskier the tool, the higher the certainty needed before using it.
- **Grounding.** Every figure must be computed from the provided data or real tool output, and shown so it can be checked. Anything else is labeled as an assumption or a hypothesis to test. When the data can't answer a question, the output says so instead of estimating a result.
- **Output.** Audience, format, length budget and where it goes. The core deliverable comes first and must be complete. Extras such as tests, appendices and next steps take a small share of the budget, and only after it. Describe the target positively. Add 3–5 varied examples in `<example>` tags when the format matters.
- **Context.** The reason behind each constraint ("read aloud by TTS, so no ellipses"), so the model can generalize from it.

## 5. Lint the prompt

Before showing the prompt to the user, check it against this list and fix every hit:

- **Contradictions.** A stretch target that clashes with a constraint (200ms load vs. no infra changes). Resolve the clash, or state which side wins.
- **Feasibility.** Every method, tool, target and check is something the executor can do in this run with this data. Downgrade each one that fails this, or move it to Prerequisites. A demand the executor can only fake is worse than no demand.
- **Crowding.** The deliverable the user asked for still gets most of the length budget. Verification material, generated datasets, crew sections and appendices can't push it out.
- **Altitude.** Give heuristics with reasons rather than if/else rules, and pitch each one somewhere between rigid and vague.
- **No-ops.** Lines the model already follows by default ("be thorough", "double-check everything" on Opus 5). Delete them.
- **Negation.** Rewrite bans as the behavior you want. Keep a ban only as a hard guardrail, paired with that positive target.
- **Bloat.** Use the fewest words that still carry the meaning. Ambition should show in the target, not in the word count.
- **Colleague test.** Would a capable newcomer with no context follow it? If not, add the missing context.

Use XML tags for structure: `<goal>`, `<context>`, `<constraints>`, `<done>`, `<output>`.

## 6. Verify the prompt

When the frontier is empty and the user confirms you understand each other, output:

1. **The rewritten prompt** in a single fenced block.
2. **Prerequisites**: the access, connectors or machines it needs. List only what is missing.
3. **What changed**: one line each for altitude, depth and range.

Then ask the user to approve it, edit it, or send it back for another round. If they edit it, use their wording exactly as written. Don't start until they approve.

## 7. Run it yourself

Once the user approves, treat the approved prompt as the user's new request and carry it out in this same session. Don't tell them to paste it anywhere.

- **Earn the target honestly.** Write general solutions. Keep tests and judges unchanged, and use real logic rather than hardcoding expected outputs. If the target or a test is wrong or out of reach, tell the user instead of gaming it.
- **Keep state for long runs.** Track tasks and test status in a structured file (`tests.json` or a todo list) and freeform notes in `progress.md`. Commit to git at each milestone. Context gets compacted, so keep going instead of wrapping up early.
- **Ground every claim.** Read files before describing them, cross-check sources, and mark anything uncertain.
- **Use subagents only when they help.** Spawn them only for crew roles that can run in parallel, need their own context, or are independent pieces of work. Do sequential or small roles yourself.
- **Stop for missing access.** If prerequisites are still missing, stop at that point and ask the user to grant them, rather than quietly scaling the work down.
- **Finish with the judge.** Run the outside judge, then report the result against the target, including any shortfall.
