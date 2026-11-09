# Infrastructure Knowledge Drops

One 5–8 minute infrastructure microtopic a day, delivered at 09:00 IST.

How it works:

1. A Claude Code cloud routine runs daily at 09:00 IST (`30 3 * * *` UTC) and follows [ROUTINE.md](ROUTINE.md).
2. [`scripts/pick.py`](scripts/pick.py) picks the topic from [topics.csv](topics.csv) using [RULES.md](RULES.md).
3. The routine writes `lessons/<date>-<ID>.md` in the [LESSON_FORMAT.md](LESSON_FORMAT.md) structure and pushes a `claude/drop-<date>` branch.
4. [deliver-lesson](.github/workflows/deliver.yml) merges it to main and opens an issue labelled `lesson`. GitHub sends the notification.
5. Comments on a lesson issue get copied into `feedback.md` by [capture-feedback](.github/workflows/feedback.yml), and later lessons take them into account.

Files:
- `topics.csv`: topic bank and status. Add rows to extend it.
- `domains.csv`: domain priorities used for weighting.
- `history.csv`: one row per delivered lesson.
- `lessons/`: archive of every lesson.
