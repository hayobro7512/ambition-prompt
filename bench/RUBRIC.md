# Rubric

Both judges get the relevant section of this file verbatim (run.py splits it on the `## ` headings below). Score each criterion 0–3 using the anchors. Score absolutely, against the anchors, not relative to the other items in the batch.

## Judge instructions

- Items are anonymized and shuffled. Do not guess which method produced which item.
- Length is not quality. A longer or more elaborate item earns a higher score only where the anchors reward what the extra text does. Padding, repetition and ceremony count against concision and clarity.
- The target executor is a single-shot chat model with **no tools**: it cannot run code, open files, browse, query databases, spawn agents or ask follow-up questions. Any data it needs is pasted after the prompt.
- Use only what is in front of you: the raw prompt, the persona (the user's real situation), the answer key if given, and the items. Do not reward claims you cannot check.
- When unsure between two levels, pick the lower one.

## Prompt rubric

Applies to the final prompt each arm sends to the executor. The raw prompt (arm A) is scored too.

**P1. Outcome altitude.** Does the prompt aim at what the user is trying to make happen, not just the literal task?
- 0: Restates the literal task only.
- 1: Mentions a purpose but the deliverable is still only the literal task.
- 2: Frames the deliverable around the user's real outcome (e.g. a re-runnable import step, a board decision), and the done criteria reflect it.
- 3: As 2, and makes the result durable or decision-ready (e.g. reusable across runs, states how the user will know it keeps working), without inflating scope beyond the persona's needs.

**P2. Expert depth.** Does it ask for the methods, raw material and stretch target a top practitioner would use?
- 0: No method guidance; invites a generic answer.
- 1: Generic quality words ("thorough", "best practices") with no concrete method.
- 2: Names at least two concrete, correct methods for this domain (e.g. union-find for transitive matching; tenure-corrected churn rates, segment comparison) or names the raw material to start from.
- 3: As 2, and sets a concrete stretch target that is still feasible for a no-tool executor (e.g. linear time on 40k rows; a falsifiable test of the leading hypothesis), and asks it to test a stated belief against the data.

**P3. Range.** Does it bring in the relevant disciplines and an adversarial check?
- 0: Single viewpoint.
- 1: Mentions other perspectives without assigning them work.
- 2: Assigns concrete work to at least one other relevant discipline or stakeholder (e.g. data-quality edge cases from an ops view; finance impact on MRR).
- 3: As 2, plus a red-team step that actually attacks the conclusion or code (e.g. confounders, false merges) and says what to do with what it finds.

**P4. Verifiable done criteria and outside judge.** Can someone check whether the output met the bar?
- 0: No done criteria.
- 1: Vague criteria ("make it accurate").
- 2: Specific checkable criteria (listed edge cases, required numbers, required sections).
- 3: As 2, plus an outside check the user can run or apply that does not rely on the model grading itself (e.g. tests the user can run, a metric to watch in 60 days), and that the no-tool executor can actually produce.

**P5. Limits and stop rules.** Does it say what to do when stuck, what is out of scope, and when to stop?
- 0: None.
- 1: One of these, vaguely.
- 2: Clear scope limits and an instruction for ambiguity (state assumptions and proceed, or flag).
- 3: As 2, plus explicit handling of infeasibility or insufficient data (say so rather than fabricate) and clear priority when constraints conflict.

**P6. Output spec.** Is the shape of the deliverable defined?
- 0: None.
- 1: Format named only ("write a memo").
- 2: Format, sections or signature, and length or audience specified.
- 3: As 2, and fitted to the persona's actual use (e.g. drop-in function with the exact signature; a 10-minute memo convertible to 2 slides).

**P7. Internal consistency.** Are the instructions free of contradictions and impossible demands?
- 0: Contains a direct contradiction or a central demand the no-tool executor cannot meet (run code, open a file, browse, ask the user).
- 1: Contains a minor contradiction or a peripheral impossible demand.
- 2: Consistent; any tension is acknowledged.
- 3: Consistent, and where a stretch target could clash with a constraint, states which side wins.

**P8. Concision.** Is every line doing work?
- 0: Mostly boilerplate, repetition or ceremony; core instructions are hard to find.
- 1: Noticeable padding or repeated instructions.
- 2: Mostly tight; a few lines could go.
- 3: Every line is load-bearing; length is proportional to the task.

## Output rubric

Applies to the executor's reply to each final prompt. For task 1 (code), the hidden-test pass rate is computed separately by running the code; judges do not see it.

**O1. Correctness and faithfulness.**
- 0: Wrong on the central question, or invents data, numbers or facts not supported by the input (any fabricated statistic scores 0).
- 1: Partly correct; at least one material error or unsupported claim.
- 2: Correct on the central question; minor slips only; numbers consistent with the data (or answer key) within reasonable rounding.
- 3: Correct and careful: states uncertainty where the data is thin, and every number is traceable to the input.

**O2. Depth and use of expert methods.**
- 0: Generic; could apply to any similar request.
- 1: Some domain-specific reasoning but misses the main methodological issue (task 1: transitive matching or blank-value handling; task 2: tenure bias or confounding).
- 2: Uses the right methods for the main issue.
- 3: As 2, and handles a second-order issue a strong expert would catch (task 1: performance at 40k rows, merge conflict policy; task 2: small cells, the support-ticket confound).

**O3. Actionability and specificity.**
- 0: Nothing the user can act on directly.
- 1: Actions named but vague.
- 2: Concrete actions or drop-in code the user can use this week.
- 3: As 2, prioritized, with expected effect or exact usage, and the first step obvious.

**O4. Built-in verification.**
- 0: None.
- 1: Says "test it" or "monitor" with no specifics.
- 2: Gives concrete checks (test cases, sanity checks, a metric with a threshold).
- 3: As 2, and the checks would catch the most likely failure (false merges; mistaking correlation for cause), e.g. runnable tests or an experiment with a control group.

**O5. Fit to the persona's real constraints.** (Judge against the persona, even though arms may not have learned it.)
- 0: Violates a hard constraint (task 1: uses non-stdlib libraries, wrong signature; task 2: needs a data team, rolls back price for everyone).
- 1: Ignores important constraints (scale, budget, team size, deadline).
- 2: Respects the hard constraints.
- 3: Respects them and uses them (e.g. fits the cron timeout and CSV import; fits the $3k budget, the sprint cadence and the board deadline).

**O6. Clarity.**
- 0: Hard to follow.
- 1: Followable but disorganized or padded.
- 2: Clear structure; easy to scan.
- 3: Clear, tight, and the length suits the persona's use.

## Pairwise comparison

Given two anonymized outputs X and Y for the same task and persona, pick the one that better serves this user overall, weighing the output rubric above with O1 (correctness) first. Length is not quality. Answer `X`, `Y` or `tie`.
