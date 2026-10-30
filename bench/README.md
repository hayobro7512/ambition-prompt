# ambition-prompt benchmark

Does the `ambition-prompt` skill write better prompts, and do those prompts get better final outputs, than current prompt optimizers? This folder is a pre-registered, replicable test of that question. It is designed to be credible if the skill loses.

The tasks, personas, hidden tests, rubric and harness were committed (`bench: pre-register tasks, personas, rubric`) before any real model call. Skill version under test: `skills/ambition-prompt/SKILL.md` sha256 `ac227f7fc81531a96347472bfd033262e4e941222d7fcb8d0de8beb8cc8f277c`. Each optimize record also stores the sha256 of the exact system prompt sent.

## Design

**Two tasks**, each a short raw prompt of the kind people actually type:

| Task | Raw prompt | Scored by |
|---|---|---|
| `dedupe` (objective, code) | [`tasks/dedupe/prompt.txt`](tasks/dedupe/prompt.txt): write `dedupe_contacts(rows)` | 20 hidden tests ([`hidden_tests/test_dedupe.py`](hidden_tests/test_dedupe.py)) + rubric |
| `churn` (open-ended analysis) | [`tasks/churn/prompt.txt`](tasks/churn/prompt.txt) + a 600-row synthetic CSV | rubric, with a judge-only answer key |

The churn data comes from [`tasks/churn/make_data.py`](tasks/churn/make_data.py) (deterministic). It plants a story with traps: tenure bias, onboarding confounding the channel effect, a support-ticket red herring and a small Team plan. The answer key ([`tasks/churn/truth.md`](tasks/churn/truth.md)) is computed from the file and shown only to judges. Each hidden test is tagged `[raw]`, `[persona]` or `[expert]`, depending on whether its requirement is in the raw prompt, can be learned only by asking the user, or is a default a careful engineer would apply.

**Four arms per task.** Every optimizer arm uses the same optimizer model, with the full text of its skill or prompt as the system prompt:

| Arm | System prompt | Source |
|---|---|---|
| A, raw | none (the raw prompt is sent as-is) | |
| B, prompt-master | `SKILL.md` + `references/*.md`, vendored verbatim in [`optimizers/prompt-master/`](optimizers/prompt-master/) | v1.8.0, MIT, Nidhin Joseph Nelson, github.com/nidhinjs/prompt-master |
| C, OpenAI guide | [`optimizers/openai_guide.md`](optimizers/openai_guide.md), written for this bench | OpenAI, *GPT-5 prompting guide*, developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide (retrieved 2026-10-29). Uses its metaprompting, no-contradiction, stop-condition, structured-spec and verbosity advice, in a Goal/Context/Constraints/Done layout. |
| D, ambition-prompt | [`../skills/ambition-prompt/SKILL.md`](../skills/ambition-prompt/SKILL.md), unmodified | the skill under test |

Every optimizer gets the same appended *harness note* (`harness_note()` in `run.py`). It covers what the optimizer can't look up from inside a plain chat API:
- the target is a single-shot chat model with no tools;
- for churn, the CSV header and first rows;
- questions are allowed for at most 3 rounds;
- the final prompt goes inside `<final_prompt>` tags.

**Simulated user.** Each task has a persona ([`personas/`](personas/)) with the user's hidden goals, data facts, constraints, tools, budget and risk tolerance. Any message from an optimizer that lacks a final prompt goes to a simulated user, an LLM that sees only the persona and the questions, and its reply comes back. Every arm has the same access to the persona, and only through its own questions. The cap is 3 rounds of questions for every arm; prompt-master limits itself to 3 questions. Each question and answer is logged in `runs/<id>/optimize/<task>_<arm>.json`.

**Execution.** Each final prompt goes to the same executor model, single shot, with no tools, at temperature 0.7, for n=3 samples per arm per task. The churn CSV is appended after every prompt. For `dedupe`, the last ```python block that defines `dedupe_contacts` is extracted and run against the hidden tests, each test in its own subprocess with a 30 s timeout. Output length is recorded.

**Judging.** The rubric is in [`RUBRIC.md`](RUBRIC.md). Each criterion is scored 0–3 against an anchor for every level: 8 criteria for prompts and 6 for outputs.
- Judge 1 (primary) is an OpenAI model, picked from `/v1/models` by the preference list in `run.py`.
- Judge 2 is an NVIDIA-hosted model from a different family than the executor.
- Judges see anonymized items in seeded random order and score them absolutely. They are told that length isn't quality and that the executor has no tools. They also list any prompt demand a no-tool executor can't meet. A keyword screen (`INFEASIBLE_RX`) flags the same kind of demand independently.
- Pairwise D-vs-B and D-vs-C comparisons run on every executor sample in both orderings, which cancels position bias.
- The report includes a length-controlled view: the residual left after regressing output score on log(chars), fit per task and per judge. It also reports the correlation between length and score, and agreement between the two judges.

**Headline metrics:** the hidden-test pass rate and output quality, including the pairwise results. The prompt-rubric score is secondary (see the threats below).

## Reproduce

Requirements: Python 3.10+, standard library only. pytest is optional, since the harness has its own runner.

```bash
cd bench
python3 run.py --dry-run                       # mocks every LLM call; checks the whole pipeline without keys

export NVIDIA_API_KEY=...                      # free key from build.nvidia.com (~40 req/min; run.py throttles to ~37)
export OPENAI_API_KEY=...                      # judge 1 only; hard-capped at 40 calls per run, retries included
python3 ~/.claude/skills/nvidia-free/scripts/nv.py --task chat --pick   # optional: list working NVIDIA model ids
python3 run.py --seed 7                        # all stages; ~100 NVIDIA calls and 33 OpenAI calls (planned)

# or stage by stage (later stages default to the latest run; --run picks one)
python3 run.py --stage optimize --seed 7
python3 run.py --stage execute
python3 run.py --stage judge
python3 run.py --stage report                  # writes runs/<id>/RESULTS.md and bench/RESULTS.md
python3 run.py --stage report --excerpts       # also prints prompts, Q&A and judge flags to your terminal only
```

Override models with `--optimizer`, `--simuser`, `--executor` and `--judge-nv`. A run saves its models and seed in `runs/<id>/config.json` and keeps them on every later stage. Before calling anything, the harness checks that each NVIDIA model is still served. NVIDIA retires model IDs often: `z-ai/glm-5.3` and `moonshotai/kimi-k3` were gone by 2026-10-29.

Default models, checked live on 2026-10-29:

| Role | Model |
|---|---|
| Optimizer (all arms) | `nvidia/nemotron-3-ultra-550b-a55b` |
| Simulated user | `deepseek-ai/deepseek-v4.1-flash` |
| Executor | `nvidia/nemotron-3-super-120b-a12b` |
| Judge 2 | `moonshotai/kimi-k2.6` |
| Judge 1 | first available of `gpt-5.6-sol`, `gpt-5.6`, `gpt-5.6-terra`, `gpt-5.5`, `gpt-5.2`, `gpt-5.1`, `gpt-5`, `o3`, `gpt-4.1` (the one used is recorded in `config.json` and `RESULTS.md`) |

**Budget.** The OpenAI plan is 1 model listing, 2 prompt-scoring calls, 6 output-scoring calls and 24 pairwise calls, for 33 in total. Every attempt increments a counter in `runs/<id>/openai_calls.json`, and the harness refuses call 41. Each judge call scores a whole batch: 4 prompts, or 4 outputs (one per arm).

**Caching and audit.** Every LLM response is saved as JSON in `runs/<id>/cache/`, with the request, model and timestamp. The per-stage records go in `optimize/`, `execute/` and `judge/`. To re-run a stage, delete its records; cached responses are reused, so re-judging the same items is free.

### Why raw outputs are not shipped

The optimizer, simulated user, executor and second judge run on NVIDIA's API trial. Its terms limit use to internal testing and evaluation (§1.2, §1.4) and forbid distributing generated content (§4.2). So `bench/runs/` is gitignored, and `RESULTS.md` holds only aggregate numbers that our code computes, plus the hand-written raw prompts. To see the actual prompts and outputs, run the harness with your own keys and use `--excerpts`.

### Safety note

The `dedupe` stage executes code an LLM wrote. Each test runs as `python -I` in a fresh temp directory with a timeout, but nothing is sandboxed beyond that. Run the benchmark in a VM or container if that matters to you.

## Limitations

- **The skill's in-session run is not tested.** `ambition-prompt` is meant to run the approved prompt itself, in the same Claude Code session, with tools, subagents, tests and git (its step 7). Here every prompt goes to a no-tool, single-shot executor. That tests the prompt as a portable artifact, not the full workflow. A prompt that says "run the tests" is flagged and loses rubric points here, though it could be the right call in-session.
- **Skill steps are compressed.** Step 1 (looking up facts) is replaced by the harness note. Step 6 (user approval) is skipped: the job ends at `<final_prompt>`. The grilling is capped at 3 rounds.
- **Non-Claude models.** The skills were written with Claude in mind; the optimizer and executor here are NVIDIA-hosted open models.
- **Two tasks.** These are not a representative sample of prompts.
- **One optimization per arm per task.** The n=3 covers executor variance only, not optimizer variance.

## Threats to validity

1. **Judges prefer longer, more elaborate text.** LLM judges are known to favor length and visible structure. The mitigations are an explicit instruction, absolute anchors, a length-controlled residual, the reported length–score correlation, and a hidden-test metric that can't be swayed by prose. None of these fully removes the bias.
2. **The prompt rubric partly rewards what ambition-prompt asks for.** Altitude, depth, range and an outside judge (P1–P4) are the skill's own vocabulary. That is why the prompt score is secondary, and the headline is hidden tests plus output quality. Read a D win on the prompt score alone as close to circular.
3. **The simulated user.** An LLM playing a persona is more cooperative and consistent than a real person. It may leak more or less than a real user would. Arms that ask more questions get more information; that is part of what is being measured, but its size depends on how the simulated user behaves. Arm A asks nothing by design.
4. **n=3, two tasks, one seed.** There is no significance testing. Differences within about one standard deviation should be read as ties.
5. **The second judge and the optimizer and executor all come from the NVIDIA catalog.** The second judge is chosen from a different family than the executor, but self-preference across hosted models can't be ruled out. The primary judge is OpenAI.
6. **Personas and tests were written by the people evaluating the skill.** They were pre-registered before any run to limit tuning to a result. Strangers should check the `[persona]`-tagged tests and decide whether they are fair.
7. **Answer key exposure.** Churn judges see the answer key, which helps them score correctness but may also anchor them on the planted story over other valid findings. The rubric tells them to score against the data.

## Files

```
bench/
  run.py                      harness (stdlib only)
  RUBRIC.md                   prompt + output rubric with 0–3 anchors; judges get it verbatim
  tasks/dedupe/prompt.txt     raw prompt, task 1
  tasks/churn/prompt.txt      raw prompt, task 2
  tasks/churn/customers.csv   synthetic data (600 rows)
  tasks/churn/make_data.py    generator for the CSV + answer key
  tasks/churn/truth.md        judge-only answer key
  personas/{dedupe,churn}.md  simulated-user personas
  hidden_tests/test_dedupe.py 20 hidden tests (pytest-compatible)
  hidden_tests/reference_solution.py  proves the suite is passable (20/20); used by --dry-run
  optimizers/prompt-master/   vendored competitor (MIT)
  optimizers/openai_guide.md  OpenAI-guide optimizer prompt
  runs/                       gitignored: cached responses and per-stage records
```

## Protocol deviations (after pre-registration)

1. **2026-10-29, harness invocation note.** In the first real run the optimizer, given ambition-prompt's SKILL.md as its system prompt, decided it had not been invoked: the raw prompt arrived without a trigger phrase. It solved the task itself and returned the raw prompt unchanged. The harness note, which is identical for all arms, now states that the user has explicitly invoked the optimizer on the raw prompt. All arms were re-optimized from scratch after the fix.
2. **2026-10-29, model swaps.** NVIDIA's `/v1/models` lists ids that return 404 or 410 for free accounts. Swaps: simulated user `deepseek-v4.1-flash` (repeated 504s) → `nemotron-3.5-lightning-30b-a3b`; executor `nemotron-3-super-120b` (404) → `nemotron-3-ultra-550b` (the same model as the optimizer); second judge `kimi-k2.6` (404) → `openai/gpt-oss-20b`. That makes both judges OpenAI-made models, which weakens their independence. The startup check now pings each model instead of trusting the list.
3. **2026-10-29, skill version.** The skill under test is commit `80e56b5` (questions listed without recommended answers, per the author's preference). The pre-registration recorded an earlier hash.
