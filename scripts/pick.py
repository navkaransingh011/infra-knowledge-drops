#!/usr/bin/env python3
"""Topic picker and bookkeeping for Infrastructure Knowledge Drops.

Selection rules come from RULES.md. All randomness is seeded by the IST date,
so re-running on the same day gives the same pick.

  python3 scripts/pick.py pick              -> prints JSON for today's topic
  python3 scripts/pick.py record --id INF-004 --file lessons/....md
  python3 scripts/pick.py record --new --domain D --parent P --microtopic M \
        --objective O --file lessons/....md
"""
import argparse
import csv
import json
import random
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "topics.csv"
DOMAINS = ROOT / "domains.csv"
HISTORY = ROOT / "history.csv"

IST = timezone(timedelta(hours=5, minutes=30))
WEIGHT = {"Very high": 3, "High": 2, "Medium": 1}
REPEAT_WINDOW_DAYS = 90
DISCOVERY_RATE = 0.20


def today_ist() -> date:
    return datetime.now(IST).date()


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def delivered_recently(t, today):
    if not t["Last delivered"]:
        return False
    last = date.fromisoformat(t["Last delivered"])
    return (today - last).days < REPEAT_WINDOW_DAYS


def prereqs_met(t, delivered_names, all_names):
    # Prerequisites is free text that may contain commas inside topic names,
    # so match known microtopic names as substrings. Names not in the bank
    # are treated as background knowledge (already met).
    p = t["Prerequisites"]
    if not p:
        return True
    needed = [n for n in all_names if n in p]
    return all(n in delivered_names for n in needed)


def pick(day):
    topics = read_csv(TOPICS)
    domains = read_csv(DOMAINS)
    history = read_csv(HISTORY)

    if any(h["date"] == day.isoformat() for h in history):
        print(json.dumps({"mode": "already_delivered", "date": day.isoformat()}))
        return 3

    rng = random.Random(day.isoformat())
    last_domain = history[-1]["domain"] if history else None
    all_names = {t["Microtopic"] for t in topics}
    delivered_names = {t["Microtopic"] for t in topics if t["Last delivered"]}

    # Stage 1: weighted random domain, avoiding yesterday's domain.
    dom_pool = [d for d in domains if d["Domain"] != last_domain] or domains
    dom_weights = [WEIGHT.get(d["Priority"], 1) for d in dom_pool]

    if rng.random() < DISCOVERY_RATE:
        d = rng.choices(dom_pool, dom_weights)[0]["Domain"]
        existing = [t["Microtopic"] for t in topics if t["Domain"] == d]
        print(json.dumps({"mode": "discovery", "date": day.isoformat(),
                          "domain": d, "existing_microtopics": existing}, indent=2))
        return 0

    # Stage 2: weighted microtopic inside the domain. Retry other domains if a
    # domain has nothing eligible.
    while dom_pool:
        d = rng.choices(dom_pool, dom_weights)[0]["Domain"]
        cands = [t for t in topics if t["Domain"] == d and not delivered_recently(t, day)]
        if cands:
            w = []
            for t in cands:
                x = WEIGHT.get(t["Importance"], 1)
                x *= 1.0 if prereqs_met(t, delivered_names, all_names) else 0.15
                x *= 2.0 if t["Status"] == "Unseen" else 1.0
                w.append(x)
            t = rng.choices(cands, w)[0]
            print(json.dumps({"mode": "bank", "date": day.isoformat(), **t}, indent=2))
            return 0
        i = [x["Domain"] for x in dom_pool].index(d)
        dom_pool.pop(i)
        dom_weights.pop(i)

    print(json.dumps({"mode": "exhausted", "date": day.isoformat()}))
    return 4


def record(a, day):
    topics = read_csv(TOPICS)
    fields = list(topics[0].keys())
    if a.new:
        n = max(int(t["ID"].split("-")[1]) for t in topics) + 1
        t = {k: "" for k in fields}
        t.update({"ID": f"INF-{n:03d}", "Domain": a.domain, "Parent topic": a.parent,
                  "Microtopic": a.microtopic, "Importance": "High", "Difficulty": "2",
                  "Learning objective": a.objective, "Status": "Discovered"})
        topics.append(t)
    else:
        t = next((x for x in topics if x["ID"] == a.id), None)
        if t is None:
            sys.exit(f"unknown id {a.id}")
        t["Status"] = "Delivered"
    t["Last delivered"] = day.isoformat()
    write_csv(TOPICS, topics, fields)

    hist = read_csv(HISTORY)
    hist.append({"date": day.isoformat(), "id": t["ID"], "domain": t["Domain"],
                 "microtopic": t["Microtopic"], "mode": "discovery" if a.new else "bank",
                 "lesson_file": a.file})
    write_csv(HISTORY, hist, ["date", "id", "domain", "microtopic", "mode", "lesson_file"])
    print(t["ID"])


def reset():
    """Start fresh: clear delivery state, drop discovered topics, wipe history."""
    topics = read_csv(TOPICS)
    fields = list(topics[0].keys())
    kept = [t for t in topics if t["Status"] != "Discovered"]
    for t in kept:
        t["Status"], t["Last delivered"], t["Feedback"] = "Unseen", "", ""
    write_csv(TOPICS, kept, fields)
    write_csv(HISTORY, [], ["date", "id", "domain", "microtopic", "mode", "lesson_file"])
    print(f"reset {len(kept)} topics; history cleared")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("reset")
    p = sub.add_parser("pick")
    p.add_argument("--date")
    r = sub.add_parser("record")
    r.add_argument("--date")
    r.add_argument("--id")
    r.add_argument("--new", action="store_true")
    r.add_argument("--domain")
    r.add_argument("--parent")
    r.add_argument("--microtopic")
    r.add_argument("--objective")
    r.add_argument("--file", required=True)
    a = ap.parse_args()
    if a.cmd == "reset":
        return reset()
    day = date.fromisoformat(a.date) if a.date else today_ist()
    if a.cmd == "pick":
        sys.exit(pick(day))
    record(a, day)


if __name__ == "__main__":
    main()
