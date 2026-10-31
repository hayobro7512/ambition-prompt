# Answer key (judge only)

1. The sources conflict: PM-112 blames Postgres-as-queue, but Marta's reproduction shows the bloat came from default autovacuum settings plus a long-running reporting transaction, and was fixed in staging. A strong answer names this conflict and weighs Marta's evidence (reproduced, measured) above the postmortem's untested label.
2. Headroom math: at 15%/month, 410 -> ~2,000 jobs/s takes about 11 months (log(2000/410)/log(1.15) ~ 11.3). A safer trigger (for example ~1,200-1,500 jobs/s, about 8-9 months) gives time to migrate.
3. The vendor blog is marketing, not evidence about their workload; its $1,200/month managed plan exceeds the $500 budget.
4. Constraints rule out self-hosting a broker (2 engineers, no on-call); any future move must be a managed service within $500/month, with at-least-once delivery.
5. Recommendation: keep Postgres now; apply Marta's fixes (autovacuum tuning on jobs, reporting off the primary, archive partitioning), add bloat/long-transaction alerts, and set a measurable migration trigger (throughput threshold or a repeat incident) with a dated review. Report jobs (long-running) may deserve separate handling.
Weak: recommending BrokerX or a self-hosted broker; ignoring the conflict; no numbers; inventing benchmarks not in the sources.
