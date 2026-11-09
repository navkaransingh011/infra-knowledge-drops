# Infrastructure Knowledge Drops — lesson format

Philosophy: **explain enough to understand, leave room to explore.**

Hard limits:
- 5–8 minutes of reading (roughly 900–1400 words including code). One specific microtopic only.
- No lengthy conclusion, no history lesson, no unnecessary theory.
- Every claim that depends on a version, provider, or default value must say which (e.g. "Linux ≥ 5.x", "AWS", "Kubernetes 1.29+") and be checked against official docs / RFCs / man pages.

The reader is a working infrastructure engineer. Do not assume they know the components involved: before explaining *how it works*, briefly name the moving parts (one or two sentences each: what it is, why it exists). Then explain the mechanism as a causal chain where each step leads to the next — never as a list of disconnected facts.

## Exact structure (use these headings)

```markdown
# <Microtopic>

`<ID>` · <Domain> › <Parent topic> · Difficulty <n>/3 · ~<n> min

> **Why this matters:** one or two sentences tying it to real production pain.

## The moving parts
Short definitions of each component the explanation leans on.

## How it works
The mechanism as a connected causal chain. A small ASCII diagram if it helps.

## In production
One realistic scenario: setup, what happened, what you saw (logs/metrics/symptoms), why, and the fix.

## The gotcha
One non-obvious trap that bites experienced people. Why it happens.

## Try it
Commands or config where useful (fenced code blocks with language tags), with one line on what to look for in the output. Prefer things runnable on a laptop or a throwaway container/VM.

## Think about it
One curiosity-driven reasoning question that requires reconstructing the mechanism (not a definition question). No answer given.

<sub>Sources: 2–4 links to official docs / RFCs / man pages actually used.</sub>
```
