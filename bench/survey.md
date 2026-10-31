# Prompt-optimizer survey (competitive analysis)

Retrieved 2026-10-30 with `gh search repos` / `gh api` (read-only). Stars and last push are from the GitHub API on that date. "License" is the SPDX id read from the repo's own LICENSE file; where GitHub's detector disagrees, both are shown. Every row below was judged from its actual instruction file (path given), not its README.

Purpose: (a) find techniques `ambition-prompt` lacks, (b) pick a second benchmark rival besides prompt-master.

Search queries: `prompt engineering skill`, `SKILL.md prompt`, `claude skill prompt optimizer`, `prompt improver`, `meta prompt`, `prompt generator claude code`, `prompt optimizer`, `prompt architect`, `prompt enhancer`, `prompt coach`, `superprompt`, `lyra prompt optimizer`, `prompt optimizer skill`, `awesome claude skills`, `awesome agent skills`. I also grepped the READMEs of the five largest awesome-lists (ComposioHQ, travisvn, BehiSecc, VoltAgent and heilcheng) for prompt-related entries.

## 1. Candidates (21)

| # | Repo | ★ | Last push | License | Format | Instruction file read |
|---|---|---|---|---|---|---|
| 1 | [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) | 15,302 | 2026-10-22 | MIT | Claude skill | `SKILL.md` + `references/` (already vendored) |
| 2 | [ckelsoe/prompt-architect](https://github.com/ckelsoe/prompt-architect) | 327 (35 forks, npm 212 dl/mo) | 2026-07-24 | MIT | Agent skill + universal system prompt | `skills/prompt-architect/SKILL.md`, `adapters/system-prompt.md` |
| 3 | [severity1/claude-code-prompt-improver](https://github.com/severity1/claude-code-prompt-improver) | 1,965 | 2026-10-01 | MIT | Claude Code plugin (UserPromptSubmit hook + skill) | `skills/prompt-improver/SKILL.md`, `nudges/*.json` |
| 4 | [linshenkx/prompt-optimizer](https://github.com/linshenkx/prompt-optimizer) | 40,026 | 2026-10-30 | AGPL-3.0-only (GH: NOASSERTION) | Web app / extension / MCP; templates are system prompts | `packages/core/src/services/template/default-templates/{optimize,user-optimize,iterate,evaluation-structured-compare}/*.ts` |
| 5 | [langgptai/LangGPT](https://github.com/langgptai/LangGPT) | 12,655 | 2026-09-11 | Apache-2.0 | Structured-prompt framework + templates | `LangGPT/templates/Role.md`, `baseRole.md` |
| 6 | [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) (metaprompt) | 53,982 | 2026-10-29 | MIT | Metaprompt (system prompt in a notebook) | `misc/metaprompt.ipynb` (25.6k-char prompt) |
| 7 | [openai/openai-cookbook](https://github.com/openai/openai-cookbook) (optimizer) | 76,881 | 2026-10-31 | MIT | Multi-agent checker pipeline + GPT-5 optimizer guide | `examples/Optimize_Prompts.ipynb`, `examples/gpt-5/prompt-optimization-cookbook.ipynb` |
| 8 | [k-vaca/prompt-engineering-skill](https://github.com/k-vaca/prompt-engineering-skill) | 7 | 2026-08-03 | MIT | Agent skill (evidence-cited) | `prompt-engineering/SKILL.md` (40 KB) |
| 9 | [treylom/prompt-engineering-skills](https://github.com/treylom/prompt-engineering-skills) | 193 | 2026-09-26 | MIT text + 3rd-party credits (GH: NOASSERTION) | Claude Code command + skills; GPTs/Gems ports (Korean) | `commands/prompt.md` (132 KB), `skills/*/SKILL.md` |
| 10 | [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | 64,187 | 2026-05-31 | MIT | Spec-driven meta-prompting system | `get-shit-done/references/questioning.md`, `workflows/discuss-phase-assumptions.md` |
| 11 | [ndpvt-web/prompt-improver](https://github.com/ndpvt-web/prompt-improver) | 86 | 2026-05-15 | MIT | Claude skill | `SKILL.md` |
| 12 | [CR-730/agent-system-prompt-architect-skill](https://github.com/CR-730/agent-system-prompt-architect-skill) | 24 | 2026-09-16 | MIT | Agent skill (system prompts) | `skills/agent-system-prompt-architect/SKILL.md` |
| 13 | [bergr7/claude-skill-prompt-optimizer](https://github.com/bergr7/claude-skill-prompt-optimizer) | 5 | 2026-02-27 | none | Claude skill (eval loop) | `skill/SKILL.md` |
| 14 | [Prestigious-Fan118/Lyra-Prompt-Optimizer-v1](https://github.com/Prestigious-Fan118/Lyra-Prompt-Optimizer-v1) | 200 | 2025-06-30 | none | Custom GPT / system prompt | `Lyra v2 beta - The Cognitive Prompt Architect` |
| 15 | [NeoVertex1/SuperPrompt](https://github.com/NeoVertex1/SuperPrompt) | 6,428 | 2026-04-26 | none | System prompt (symbolic "meta" prompt) | `Readme.md` prompt block |
| 16 | [hancengiz/claude-code-prompt-coach-skill](https://github.com/hancengiz/claude-code-prompt-coach-skill) | 148 | 2026-01-24 | none | Claude skill (log analysis) | `Skill.md` |
| 17 | [chengzhongwei/Prompt-sensei](https://github.com/chengzhongwei/Prompt-sensei) | 109 | 2026-07-13 | Apache-2.0 | Claude Code / Codex skill (coach) | `SKILL.md` |
| 18 | [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) (prompt-engineering) | 1,795 | 2026-08-26 | GPL-3.0 | Reference skill | `plugins/customaize-agent/skills/prompt-engineering/SKILL.md` |
| 19 | [microsoft/PromptWizard](https://github.com/microsoft/PromptWizard) | 4,026 | 2025-10-13 | MIT | Python framework (needs dataset) | `promptwizard/glue/promptopt/techniques/critique_n_refine/prompt_pool.yaml` |
| 20 | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | 38,861 | 2026-10-30 | MIT | Python framework (MIPROv2) | `dspy/propose/grounded_proposer.py` |
| 21 | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) (enhance-prompt) | 8,643 | 2026-08-17 | Apache-2.0 | Domain skill (UI prompts) | `plugins/stitch-utilities/skills/enhance-prompt/SKILL.md` |

### Core techniques per candidate

| # | Core techniques |
|---|---|
| 1 prompt-master | Routes to 30+ named target tools and models, each with its own syntax notes, behind a "model recency gate". Asks at most 3 clarifying questions. Bans high-fabrication techniques (ToT, GoT, MoE, USC) in single prompts and never requests hidden CoT, asking for "auditable reasoning" instead. Ends with a 6-point verify lock (critical constraints in the first 30%, token-efficiency audit). |
| 2 prompt-architect | Scores the prompt 1–10 on 5 dimensions with rubric anchors and shows the scores. Routes by intent (7 categories) to 31 frameworks, and when two frameworks would emit the same prompt it says so and picks the simpler. Asks 3–5 questions per framework, always including "paste the actual material". **Never defaults a fact about the user's world**: it emits a `[you fill this in: …]` placeholder instead. Never softens or drops a prohibition. Strips framework headers from the emitted prompt. |
| 3 claude-code-prompt-improver | A hook classifies every prompt as clear or vague and lets clear ones bypass. Mandatory research first (codebase, git log, web) through an Explore subagent. Then 1–6 multiple-choice questions whose options come from that research, then it executes directly. It never emits a rewritten prompt. |
| 4 linshenkx/prompt-optimizer | No questions: a one-shot rewrite into a LangGPT persona scaffold (Role/Profile/Skills/Rules/Workflows/Initialization) or a "precision" rewrite of a user prompt. Wraps the original prompt in JSON as "evidence, not a task to execute", and must preserve every `{{var}}` (self-check). An iterate template merges a requested change into the prompt, with ✅/❌ examples of the mistake of answering instead of editing. A pairwise judge compares test outputs and flags `overfitWarnings`. |
| 5 LangGPT | Prompt as code: a Markdown Role / Profile / Skills / Rules / Workflow / Initialization schema. Ships variables, commands and reusable templates. Mostly a template library, with no interview or verification step. |
| 6 Anthropic metaprompt | Long worked examples of task→instructions pairs, then a fixed procedure: `<Inputs>` (minimal variables), `<Instructions Structure>` (plan where each variable goes; long inputs before the directions), `<Instructions>`. Notes: put the justification before the score, use a scratchpad only for complex tasks, and give an explicit "I don't know" line for unanswerable questions. |
| 7 OpenAI cookbook optimizer | Parallel checker agents (contradictions, format spec, few-shot-vs-rules consistency) return structured `Issues`, then a rewriter fixes only those. The GPT-5 notebook measures baseline vs optimized prompts on 30 generations with an LLM-as-judge. |
| 8 k-vaca | Profiles the task (type, reasoning vs non-reasoning target, output consumer, stakes, 3–5 gold I/O pairs that define "good"). "Resolve ambiguity by choosing, not interrogating": state the reading chosen plus the main alternative. Gives a placement anatomy (data → instructions → examples → contract → query last), edge-behavior and abstention paths, untrusted input treated as data, and CoT only for non-reasoning models. Iteration protocol: an eval set with a held-out split, one change at a time, a robustness re-run. |
| 9 treylom | Two inviolable principles: name a **real expert** in `<role>`, and route to the target model by auto-detecting it. "Explicit element expansion" infers missing elements per purpose. Requires an intermediate structuring step (storyboard or outline) before the prompt. Lets the user pick from 5 options after output (run / edit / …). Ships pass/fail fixture files for its own output gate. |
| 10 GSD | Questioning as "dream extraction": start open, follow the user's energy, challenge vague words ("fast how?"), 2–4 concrete options plus "let me explain". **Assumptions mode**: read the codebase, then present assumptions, each with evidence and the consequence if wrong, so the user only corrects (about 2–4 corrections instead of 15–20 questions). Fixed scope guardrail. |
| 11 ndpvt prompt-improver | The emitted prompt makes the executor reason from first principles: GIVEN AXIOMS (known context baked in), TASK, METHOD (find axioms, then build deductively), VERIFICATION against the axioms. |
| 12 CR-730 | The response *is* the deployable prompt. Drafts in the same turn and asks only if domain and task are unknown, then for one sample input plus the desired output. Writes assumptions inline. Uses a 9-layer system-prompt architecture. **Prompt-vs-runtime separation**: rewrite pipeline and schema jargon into what the agent actually sees. Each rule is stated once. |
| 13 bergr7 | Eval-gated loop: baseline pass@k, diagnose failures by taxonomy, minimal edit, spot-check, then targeted, then regression; keep or `git checkout` revert. The eval budget is counted. |
| 14 Lyra | Welcome gate: the user picks the target AI and a depth (Quick / Deep / Revolutionary). Progressive questioning (goal → audience → constraints → format → criticality). Picks a CoT/ToT/GoT/AoT framework. Adds CoVe or self-correction only for high-stakes work. |
| 15 SuperPrompt | Symbolic "holographic" persona prompt that sets no task. Not an optimizer, so there are no transferable techniques. |
| 16 prompt-coach | Mines `~/.claude` logs and scores the user's past prompts. Counts brief prompts that carry rich context as good, and context-poor prompts as bad. |
| 17 Prompt-sensei | Stage-aware scoring (exploration / diagnosis / execution / verification): only the dimensions relevant to the stage count. Gives one canonical habit tip per prompt, e.g. "end with the command, test or edge case that proves the work". |
| 18 NeoLabHQ | Teaching reference (few-shot, CoT, templates, instruction hierarchy, progressive disclosure). Doesn't rewrite prompts. |
| 19 PromptWizard | Mutates the instruction using "thinking styles", then runs critique → refine against training examples. Synthesizes examples and reasoning chains. Needs a labeled dataset and code. |
| 20 DSPy MIPROv2 | Writes instructions grounded in a dataset summary, a program summary, the instructions already tried with their scores, and a "tip". Bayesian search over instruction × demos. Needs a metric. |
| 21 Stitch enhance-prompt | Gap table (platform, page type, structure, style, colors). Injects the project's DESIGN.md into the prompt. Domain-specific. |

## 2. Technique matrix

Columns: **Ours** = ambition-prompt; **PM** = prompt-master; **PA** = prompt-architect; **S1** = severity1 prompt-improver; **LO** = linshenkx prompt-optimizer; **AM** = Anthropic metaprompt; **OC** = OpenAI cookbook optimizer; **KV** = k-vaca; **TL** = treylom.
● = core, explicit; ◐ = partial or implicit; · = absent. **LACK** marks rows where we are absent or weaker than at least two rivals.

| Technique | Ours | PM | PA | S1 | LO | AM | OC | KV | TL |
|---|---|---|---|---|---|---|---|---|---|
| Look up facts before asking | ● | · | · | ● | · | · | · | ◐ | ◐ |
| Clarifying questions | ● rounds, ≤5 | ◐ ≤3 | ● 3–5 | ● 1–6 | · | · | · | ◐ only if costly | ● |
| Ask for the raw material itself ("paste it") | ◐ | · | ● | · | · | · | · | ◐ | · |
| Assumption ledger (evidence + what changes if wrong) **LACK** | · (no defaults by design) | · | ◐ | · | · | · | · | ● | ◐ |
| Visible placeholder instead of invented user fact **LACK** | · | ◐ | ● | · | ◐ `{{var}}` | ● `{$VAR}` | · | ◐ | · |
| Preserve every user prohibition/requirement (diff check) **LACK** | ◐ "raw prompt is settled" | · | ● | · | ● vars only | · | · | ◐ | · |
| Target-model adapter (syntax and model class) **LACK** | ◐ executor capability only | ● | · | · | ◐ | · | ◐ | ● | ● |
| Role / persona | ◐ crew does the work | ● | ● | · | ● | ◐ | · | ◐ voice only | ● named expert |
| XML / sectioned structure | ● | ● | ◐ headers stripped | · | ● | ● | ◐ | ● | ● |
| Few-shot examples | ◐ when format matters | ● | ● never invent | · | · | ● | ● | ● | ◐ |
| Examples-vs-rules consistency check **LACK** | · | · | · | · | · | · | ● | ◐ | · |
| Reasoning / CoT control **LACK** | · (no-op lint only) | ● | ● | · | · | ◐ | · | ● | ● |
| Output contract / schema | ● | ● | ◐ | · | ◐ | ◐ | ● | ● | ● |
| Edge behavior (empty / malformed / out of scope) **LACK** | ◐ infeasible → report | ◐ | · | · | · | ● | ◐ | ● | ◐ |
| Grounding / anti-fabrication | ● | ● | ● | ◐ | ◐ | ◐ | · | ● | ● |
| Success / done criteria | ● + outside judge | ● | ◐ | ◐ | · | · | · | ● gold I/O | ● |
| Gold input→output pairs define done **LACK** | · | · | · | · | · | · | · | ● | · |
| Eval / test generation | ◐ short check list | · | · | · | ● | · | ● | ● | ◐ |
| Self-critique / lint before delivery | ● 9 checks | ● 6 checks | ◐ | · | ◐ | · | ● agents | ● | ● |
| Contradiction detection | ● | ◐ | · | · | · | · | ● | ◐ | · |
| Before/after quality score **LACK** | · | · | ● 5-dim | ◐ | ◐ | · | ◐ | · | · |
| Quick/deep modes or bypass for clear prompts **LACK** | · | ◐ | ● | ● | ● | · | · | ● | ● |
| Length / compactness control | ● | ● | ◐ | · | · | · | · | ● | · |
| Untrusted input treated as data **LACK** | · | ● | · | · | ● | ◐ | · | ● | · |
| Placement (long data first, query last) **LACK** | · | ● | ◐ | · | · | ● | · | ● | ● |
| Stop / hand-back rules, action limits | ● | ● | ◐ | · | · | · | · | ◐ | ● |
| Approval gate, then run in session | ● | · | ◐ | ● | · | · | · | ◐ | ● |
| Iteration loop on measured results | ◐ | · | ● | · | ● | · | ● | ● | ● |
| **Raise the target** (altitude / depth / range, outside judge) | ● unique | · | · | · | ◐ specificity | · | · | · | ◐ expansion |

Read-out: no rival raises the target. They all optimize clarity and fit for the target tool. Our gaps are in prompt hygiene (placeholders, prohibition preservation, model-class adapters, placement, edge behavior, injection) and in defining "done" by example.

## 3. Steal list (ranked by expected gain in output quality)

Ranking logic: how directly the technique would have changed the final output on our two bench tasks (dedupe hidden tests tagged raw/persona/expert; churn analysis with planted traps), weighted by how often it applies outside the bench.

| Rank | Technique | What to add to SKILL.md | Source repo (file) | License | Copy text? |
|---|---|---|---|---|---|
| 1 | **Gold I/O pairs as the definition of done** | Contract: 3–5 input→expected-output pairs (≥1 hard or ambiguous case, resolved) go in `<done>`. They double as few-shot examples and as the judge. Confirm them with the user in grilling, or build them silently from the facts. | k-vaca (`prompt-engineering/SKILL.md` "What good looks like"); Anthropic metaprompt (worked examples) | MIT; MIT | Yes, with attribution |
| 2 | **Never invent a user-world fact; use a visible placeholder** | When a grilling answer is missing (round cap hit, user skipped), emit `[you fill this in: …]` and list it under Prerequisites. Don't settle it with a "sensible default" if the fact is about the user's business, data or policy. | prompt-architect (`SKILL.md` §5) | MIT | Yes, with attribution |
| 3 | **Preservation diff** | Lint item: every requirement and every "must not" from the raw prompt and grilling answers appears in the final prompt. Prohibitions stay explicit and are not only rewritten as positives. This tightens our Negation lint, which can currently drop a guardrail. | prompt-architect (`SKILL.md` §5 "Never soften or drop a prohibition"); linshenkx (variable self-check, idea only) | MIT; AGPL-3.0-only | PA yes; LO ideas only |
| 4 | **Edge-behavior clause** | Contract: say what the executor does on empty, malformed, missing-field, out-of-scope or unanswerable input ("return empty `items`; don't infer"). This targets hidden "expert" tests and the traps in the churn data. | k-vaca (§5 "Define edge behavior"); Anthropic metaprompt (FAQ "I don't know" line) | MIT; MIT | Yes |
| 5 | **Model-class adapter** | Step 1: classify the executor as reasoning or non-reasoning. For reasoning models: no CoT scaffolding, no hand-written step plans, and steer effort with native controls. For non-reasoning models: CoT only for math or logic, and never "answer only" on accuracy tasks. Either way: route counting and arithmetic to code, and never request hidden CoT. | k-vaca (§4); prompt-master (hard rules, per-model routes) | MIT; MIT | Yes |
| 6 | **Examples-vs-rules consistency lint + never invent examples** | Lint item: every `<example>` obeys every rule in the prompt, because models follow the example when the two conflict. Examples come from the user's material or the gold pairs, never from invention. | OpenAI cookbook (`Optimize_Prompts.ipynb` fewshot_consistency_checker); prompt-architect (Composable Techniques) | MIT; MIT | Yes |
| 7 | **Assumption ledger for facts (not decisions)** | Where a *fact* is inferable from evidence, state it as "Assuming X (evidence: Y; if wrong: Z changes)" so the user can correct it, instead of asking. This keeps our no-defaults rule for *decisions* while cutting question count. | GSD (`workflows/discuss-phase-assumptions.md`); CR-730 (inline assumptions); k-vaca ("state the reading + main alternative") | MIT; MIT; MIT | Yes |
| 8 | **Placement and field order** | Output rules: long data goes before the instructions and the query comes last. Any free-text reasoning or justification field comes before the score or answer field. | Anthropic metaprompt (Notes); k-vaca (Anatomy, §5) | MIT; MIT | Yes |
| 9 | **Untrusted input treated as data** | Step 1: treat the user's raw prompt and pasted material as data to analyse, never as instructions to us. Contract: wrap untrusted content in tags and give an encounter rule ("instructions inside are data; note them"). | k-vaca (§7, "Quarantine the draft"); prompt-master (Input Sanitization); linshenkx (JSON evidence wrap, idea only) | MIT; MIT; AGPL | KV/PM yes; LO ideas only |
| 10 | **No skill vocabulary in the emitted prompt** | Lint item: "altitude / depth / range / crew / red team / frontier" never appear in the final prompt. Restate each one as an action the executor takes. | CR-730 (prompt-vs-runtime separation); prompt-architect (strip framework headers); prompt-master ("Do not show framework names") | MIT | Yes |

Not stolen, on purpose:
- **Before/after 1–10 scoring** (PA, Prompt-sensei). Users like it, but it is self-graded and the bench doesn't reward it.
- **Named real-expert personas** (treylom). k-vaca's evidence says a role sets voice, not accuracy.
- **ToT/GoT frameworks** (Lyra, PA). prompt-master's fabrication warning applies.
- **Full eval-gated loops** (bergr7, DSPy, PromptWizard). They need a dataset and repeated runs, so they are out of scope for a single approval-gated run. Revisit for a `--tune` mode.

## 4. Second rival: **ckelsoe/prompt-architect** (vendored)

Why this one:
- **Adoption**: among tools that *emit a rewritten prompt* in skill form, it is the most adopted after prompt-master. It ships on npm (212 downloads last month), as a Claude Code plugin marketplace entry, through a ChatGPT skill upload, and through Gemini CLI.
- **Different method**: prompt-master routes by *target tool*; prompt-architect scores the prompt and routes by *user intent* to one of 31 published frameworks. It asks 3–5 material-first questions, and guards against fabrication with placeholders rather than with grounding rules. Neither one tries to raise the target, so both test our core claim.
- **Runnable**: `adapters/system-prompt.md` is a self-contained universal system prompt (314 lines, 23 KB) written for "any LLM with a system prompt field". That fits our harness exactly. The SKILL.md loads 31 reference files (about 450 KB), which can't be used as a system prompt.
- **License**: MIT, so redistribution is allowed.

Runners-up and why not:
- **linshenkx/prompt-optimizer** (40k★). Highest adoption, but it is an app with about 10 optimize templates, so which one is "the rival" would be our own choice, which weakens validity. It is also AGPL-3.0-only: verbatim redistribution is allowed, but copyleft is friction in an MIT launch repo. Good third arm if needed: `user-optimize/user-prompt-professional_en.ts`.
- **severity1** (2k★, MIT). Closest to our flow (research → grounded questions → execute), but it never emits a prompt, and it needs a hook plus Explore and AskUserQuestion tools. That doesn't fit the optimize-then-execute harness.
- **Anthropic metaprompt** (MIT). A strong, different template-centric method, but it is a 2024-era prompt with no questions. It is a reasonable baseline arm, not a "skill" competitor.

Vendored into `bench/optimizers/prompt-architect/` at commit `6c7a2c7b5a15cbb918828c7878c226a592985702` (v3.5.1):

| File | Source path | Use |
|---|---|---|
| `adapters/system-prompt.md` | `adapters/system-prompt.md` | **The system prompt for the arm.** sha256 `9d4aeb1a9215b01e80325df4ee82e28e5607f8343ecba4964bed818637fcf0d5`. Strip the "How to use this file" header (lines 1–6, through the first `---`) before sending, as the file itself instructs. |
| `SKILL.md` | `skills/prompt-architect/SKILL.md` | Reference only (it points to `references/` and `assets/` files that were not vendored). |
| `LICENSE` | `LICENSE` | MIT, © 2025 prompt-architect contributors |

Harness note for whoever wires the arm: prompt-architect ends its reply with the prompt in a fenced block and nothing after it. Its questions come as a numbered list without our `Q1:` format, so the persona simulator must accept free-form question lists.
