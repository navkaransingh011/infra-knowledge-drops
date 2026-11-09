# Infrastructure Knowledge Drops

One 5–8 minute infrastructure microtopic a day, delivered at 09:00 IST.

How it works:

1. A Claude Code cloud routine runs daily at 09:00 IST (`30 3 * * *` UTC) and follows [ROUTINE.md](ROUTINE.md).
2. [`scripts/pick.py`](scripts/pick.py) picks the topic from [topics.csv](topics.csv) using [RULES.md](RULES.md).
3. The routine writes `lessons/<date>-<ID>.md` in the [LESSON_FORMAT.md](LESSON_FORMAT.md) structure and pushes a `claude/drop-<date>` branch.
4. [deliver-lesson](.github/workflows/deliver.yml) merges it to main and opens an issue labelled `lesson`. GitHub sends the notification.
5. **Notes:** reply to a lesson email (or comment on the issue) and [capture-notes](.github/workflows/feedback.yml) files it into `notes/<ISO week>.md`, grouped by lesson. Paragraphs that start with `feedback:` go to `feedback.md` instead, and later lessons take them into account.
6. **Weekly review:** every Sunday at 10:00 IST a second routine follows [REVIEW.md](REVIEW.md) and sends `reviews/<week>.md`: recall questions on the week's lessons, revisit questions on lessons from about 1 and 3 months ago, your notes for the week with answers to any questions in them, one hands-on exercise, and the answers at the bottom. Replies to the review are saved to your notes too.

## For the Procol team: run your own daily drops

This setup is shared for people at Procol who want their own daily infrastructure lessons. Your copy runs entirely on your personal accounts: no company GitHub org, no API key, no server.

What you need: a GitHub account and a Claude plan that includes Claude Code (for example Pro or Max). The routine counts against your plan's usage; GitHub Actions on your personal repo uses about 5 minutes a month, which fits easily in the free quota.

1. **Copy the repo.** Create a new repo under your *personal* GitHub account and push this repo's contents to it. A fork also works, but Actions start disabled on forks: enable them in the fork's Actions tab.
2. **Reset the progress** so your copy starts from zero:
   ```bash
   python3 scripts/pick.py reset
   rm -rf lessons/*.md notes reviews feedback.md
   git commit -am "Start fresh" && git push
   ```
3. **Give Claude access to your copy only.**
   - Connect GitHub at https://claude.ai/code. If it warns that the Procol-Tech org couldn't be linked, that's expected and harmless: you aren't an org owner, so nothing was requested from the org.
   - Install the Claude GitHub App at https://github.com/apps/claude/installations/select_target. Pick your **personal** account, choose *Only select repositories* and select just your copy. Without this step the routine can read the repo but its push fails with a 403.
   - In the cloud environment's settings (https://claude.ai/code, environment menu), set network access to **Full**. The default allowlist blocks most docs sites, so lessons can't be fact-checked.
4. **Create the routine** at https://claude.ai/code/routines (or ask Claude Code to `/schedule` it):
   - Repository: your copy
   - Schedule: `30 3 * * *` (UTC) = 09:00 IST. Change it to suit you.
   - Prompt: *"Read ROUTINE.md at the repo root and follow it exactly. Push to a branch named claude/drop-&lt;YYYY-MM-DD&gt;, never main, and do not open issues or PRs."*
   - Connectors: none needed.
   - Optional weekly review: a second routine with schedule `30 4 * * 0` (Sunday 10:00 IST) and the prompt *"Read REVIEW.md at the repo root and follow it exactly. Push to a branch named claude/review-&lt;week&gt;, never main, and do not open issues or PRs."*
5. **Get notified:** GitHub emails you about new issues on repos you own. Install the GitHub mobile app for push notifications.

To customise it, edit `topics.csv` (add or remove topics), `domains.csv` (domain priorities) or `LESSON_FORMAT.md` (lesson style). To tell your drops what you think, comment on a lesson issue; the next lessons read those comments.

Keep your copy **private** if you'd rather your lessons and feedback comments weren't visible outside Procol.

Files:
- `topics.csv`: topic bank and status. Add rows to extend it.
- `domains.csv`: domain priorities used for weighting.
- `history.csv`: one row per delivered lesson.
- `lessons/`: archive of every lesson.
- `notes/`: your own notes, one file per ISO week.
- `reviews/`: weekly reviews.
