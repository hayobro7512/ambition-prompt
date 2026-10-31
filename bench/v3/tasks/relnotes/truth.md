# Answer key (judge only)
1. At the very top: API tokens created before 2024-06-01 stop working with this release; admins must regenerate them in Settings > API (from #820).
2. New: bulk-approve up to 100 expense reports from the approvals list; receipt photos auto-cropped and rotated.
3. Improved: approvals list ~3x faster for workspaces with 10k+ reports.
4. Fixed: CSV export date format follows workspace locale (EU); mileage totals could be off by up to $0.04 on long trips; duplicate Slack notifications; security fix for removed approvers viewing reports via a cached link, stated plainly without exploit detail.
5. Left out: CI, dependency bump, tests, docs, the internal impersonation tool.
6. Under 300 words, no PR numbers, plain language, no invented features.
Weak: burying or omitting the token change; including internal items; exploit detail; over 300 words; invented content.
