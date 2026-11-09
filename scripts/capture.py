#!/usr/bin/env python3
"""Files an issue comment into notes/<ISO week>.md (or feedback.md).

Called by the capture-notes workflow. Inputs come from environment variables
so comment text is never interpolated into shell code:
  TITLE    issue title, e.g. "[INF-251] Kafka ... · 2026-11-09" or "Weekly review · 2026-W46"
  BODY     comment body (replies to GitHub notification emails arrive here too)
  URL      comment URL
  CREATED  comment timestamp, ISO 8601 UTC

Paragraphs that start with "feedback:" go to feedback.md (lesson style / depth).
Everything else is a note, grouped under the lesson's heading in the weekly file.
"""
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IST = timezone(timedelta(hours=5, minutes=30))


def week_label(d):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def main():
    title = os.environ["TITLE"].strip()
    body = os.environ["BODY"].replace("\r\n", "\n").strip()
    url = os.environ.get("URL", "")
    created = datetime.fromisoformat(os.environ["CREATED"].replace("Z", "+00:00")).astimezone(IST)

    # File the note under the week the lesson belongs to, not the day you replied.
    m_week = re.search(r"(\d{4}-W\d{2})", title)
    m_date = re.search(r"(\d{4}-\d{2}-\d{2})", title)
    if m_week:
        week = m_week.group(1)
    elif m_date:
        week = week_label(datetime.fromisoformat(m_date.group(1)).date())
    else:
        week = week_label(created.date())

    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    feedback = [re.sub(r"(?i)^feedback\s*:\s*", "", p) for p in paras if re.match(r"(?i)^feedback\s*:", p)]
    notes = [p for p in paras if not re.match(r"(?i)^feedback\s*:", p)]
    stamp = created.strftime("%Y-%m-%d %H:%M IST")

    if feedback:
        fb = ROOT / "feedback.md"
        if not fb.exists():
            fb.write_text("# Feedback log\n\nNewest at the bottom. Written by the capture-notes workflow.\n")
        quoted = "\n>\n".join("\n".join("> " + l for l in p.splitlines()) for p in feedback)
        block = f"\n## {stamp} · {title}\n<!-- {url} -->\n{quoted}\n"
        with fb.open("a") as f:
            f.write(block)

    if notes:
        nf = ROOT / "notes" / f"{week}.md"
        nf.parent.mkdir(exist_ok=True)
        text = nf.read_text() if nf.exists() else f"# My notes · {week}\n"
        heading = f"## {title}"
        entry = f"\n<sub>{stamp} · [comment]({url})</sub>\n\n" + "\n\n".join(notes) + "\n"
        if heading in text:
            start = text.index(heading)
            nxt = text.find("\n## ", start + len(heading))
            text = text + entry if nxt == -1 else text[:nxt] + "\n" + entry + text[nxt:]
        else:
            text = text.rstrip("\n") + f"\n\n{heading}\n{entry}"
        nf.write_text(text)

    print(f"week={week} notes={len(notes)} feedback={len(feedback)}")


if __name__ == "__main__":
    main()
