---
title: NoReverseMatch: Reverse for 'instructor_detail' not found. 'instructor_detail' is not a valid view function or pattern name.
date: 2026-07-04
incident_id: 1
severity: 1
status: resolved
culprit: 7f6f36b4
fixing_commit: 172effab
---

# Postmortem: NoReverseMatch: Reverse for 'instructor_detail' not found. 'instructor_detail' is not a valid view function or pattern name.

## Summary

Incident **NoReverseMatch: Reverse for 'instructor_detail' not found. 'instructor_detail' is not a valid view function or pattern name.** (severity 1) was diagnosed with a likely code culprit (`7f6f36b4`) and resolved via fixing commit `172effab`.

## Impact

**Impact:** ~1 failed request(s) (method: Sentry issue.count (server-side error events, near-exact)) · est. ≈1 unique user(s) affected (method: Sentry userCount (IP-keyed per Sentry docs — an estimate))

## Timeline

- 2026-07-04 03:45 UTC — Deploy `7f6f36b4` shipped (the window head).
- 2026-07-04 03:46 UTC — First signal (sentry/issue) fired.
- 2026-07-04 03:46 UTC — Incident opened; Culprit posted the brief.
- 2026-07-04 04:00 UTC — Fix `172effab` shipped.
- 2026-07-04 23:08 UTC — Incident resolved (via manual).

## Root cause — ranked hypotheses

1. _[medium confidence]_ Likely code culprit: commit 7f6f36b4 — diff mentions 1 error symbol(s) (evidence #1)
2. _[low confidence]_ Insufficient additional evidence for a second suspect; an infrastructural or out-of-window cause cannot be ruled out.

## Resolution

Resolved (detected via **manual**). Fixing commit `172effab` shipped after the incident opened.

---

*Drafted by Culprit from persisted incident data. Culprit only offers this draft — a human reviews and merges it. Culprit never publishes unilaterally and never auto-merges.*
