# Selection and content rules

| Setting | Decision |
|---|---|
| Frequency | Daily |
| Delivery time | 09:00 Asia/Kolkata (IST) — cron `30 3 * * *` UTC |
| Delivery channel | GitHub Issue opened by `github-actions[bot]` (email + GitHub mobile push) |
| Lesson length | 5–8 minutes |
| Content balance | Fundamentals + production behavior/gotchas |
| Selection | Weighted random by domain importance, then microtopic (`scripts/pick.py`) |
| Repeat avoidance | Do not repeat a microtopic within 90 days |
| Consecutive domain rule | Avoid same domain on consecutive days where feasible |
| Discovery | ~20% of days: propose and teach a new microtopic not in the bank |
| Review | Optional reasoning question; issue comments land in `feedback.md` and inform future lessons |
| Accuracy | Use official docs, RFCs, and primary technical references for version-sensitive claims |
| History | `history.csv` tracks topic ID, date, mode, lesson file; `topics.csv` tracks status |
| Scope note | Label provider-specific behavior AWS/GCP/Azure and version/edition when relevant |
