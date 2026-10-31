# Changelog since v4.1.3 (from git, merged PRs)

- #812 feat: bulk-approve expense reports from the approvals list (select up to 100)
- #815 chore(ci): move pipeline to new runners
- #817 fix: CSV export used the wrong date format (MM/DD) for EU workspaces; now follows workspace locale
- #820 refactor(auth): replace legacy token service. NOTE: API tokens created before 2024-06-01 stop working on release; customers must regenerate them in Settings > API
- #821 feat: receipt photos are auto-cropped and rotated on upload
- #823 chore(deps): bump lodash 4.17.20 -> 4.17.21
- #824 fix(security): approvers could view reports from workspaces they had been removed from, via a cached link. Fixed; access is checked on every request
- #826 perf: approvals list loads about 3x faster for workspaces with 10k+ reports
- #827 test: add e2e coverage for reimbursement flow
- #829 fix: mileage rates rounded to whole cents too early, causing totals off by up to $0.04 on long trips
- #830 feat(internal): admin impersonation tool for support staff (internal only, not customer-facing)
- #832 docs: update README for local dev
- #834 fix: Slack notifications sometimes sent twice for the same approval
