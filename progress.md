# Launch push (approved 2026-10-30)

Goal: held-out, blind-judged evidence that ambition-prompt beats prompt-master + strongest rival; launch-ready repo (push needs user yes).

## Budgets
- Subagent runs: 83 / 100 (survey 1, v2-r1 optimizers 15, simusers 7, executors 40; v2-r2 optimizers 5, simusers 5, executors 10)
- OpenAI calls (bench v2): 0 / 150

## Steps
- [ ] 1 Survey (bench/survey.md, 12+ skills, pick rival)
- [ ] 2 Improve skill
- [x] 3 Bench v2: 5 held-out tasks, pre-register commit (2a89b37); rival addendum pending
- [ ] 4 Judge
- [ ] 5 Iterate (dev set = dedupe/churn)
- [ ] 6 Launch prep (local)

## Notes
- v2 roles all Claude sonnet subagents; file transport under runs/<id>/claude; run.py --suite v2 --stage packets|ingest|judge|report.
- Don't tune skill on v2 tasks. Dev set = v1 dedupe/churn via free NVIDIA pipeline.

## 2026-10-31 v3
- v3-r1 (clean held-out, NVIDIA judge only, OpenAI out of credits): D 0.55 vs B, 0.35 vs R; duration tests D 89%.
- Fix round (0c93827): ask for user-only facts; keep requirement strength; harness stops calling a provider after its quota error.
- v3-r2 (fix round): D 0.60 vs B and 0.60 vs R; output higher on 3/5 vs B and 2/5 vs R. Rule not met (wrong judge, and not clean).
- Open: relnotes. The security fix is still over-generalized, and the offered "left out" list pulls internal items into the output. Not fixed, to avoid fitting v3.
- Anthropic spend $3.40 / 95 calls (cap $15 / 200). Top-level README written. Nothing pushed.
- For a clean claim: OpenAI credits plus a fresh v4 task set written before any further skill change.
