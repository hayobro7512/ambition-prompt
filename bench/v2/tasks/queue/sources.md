# Source 1: Postmortem PM-112 (Platform team, 2024-07-02)
Three incidents in Q2 (Apr 9, May 21, Jun 18). Each time the `jobs` table grew past 40 GB of dead tuples, job pickup latency rose from ~20 ms to 4-9 s, and webhook deliveries backed up for 25-70 minutes. Root cause recorded as: "Postgres is not designed to be a queue; table bloat under high churn." Action item: evaluate a dedicated message broker.

# Source 2: Metrics snapshot (from Grafana, 2024-07-15)
- Peak throughput: 410 jobs/s (weekday 14:00 UTC). Average: 120 jobs/s.
- Growth: peak has grown ~15% month over month for the last 6 months.
- Job types: 70% webhook deliveries, 25% email sends, 5% report generation (long-running, up to 10 min).
- p99 pickup latency on normal days: 35 ms.

# Source 3: Engineer notes (Marta, 2024-07-10)
Re-ran the Q2 incidents in staging. The bloat happens because autovacuum is at defaults (scale_factor 0.2) and a reporting query holds a long transaction open for 20+ minutes, which blocks vacuum from removing dead rows. With autovacuum_vacuum_scale_factor=0.01 on `jobs`, the reporting query moved to the read replica, and completed jobs moved to a partitioned `jobs_archive` table, the same load ran 6 hours with no bloat. Benchmark on our prod-sized instance: FOR UPDATE SKIP LOCKED sustains ~2,000 jobs/s before pickup p99 exceeds 100 ms.

# Source 4: Vendor blog, "Why BrokerX beats databases" (BrokerX Inc.)
BrokerX handles 1M+ messages per second per cluster. Databases-as-queues "always fall over at scale." Our managed plan starts at $1,200/month for production with multi-AZ.

# Source 5: Team constraints (Eng manager, 2024-07-12)
- Platform team: 2 engineers. No capacity for on-call for new self-hosted infrastructure this year.
- Infra budget for a managed queue service: up to $500/month.
- Hard requirement: webhook jobs must never be lost (at-least-once delivery is fine, with idempotency keys already in place).
- Architecture review: July 24.
