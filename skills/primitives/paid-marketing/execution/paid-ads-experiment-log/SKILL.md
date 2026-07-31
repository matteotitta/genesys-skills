---
name: paid-ads-experiment-log
version: "1.0"
last_updated: 2026-07-14
author: genesys-growth
description: |
  Hypothesis-first change journal for paid campaigns + directional before/after lift. Log every material change (budget shift, new creative, audience swap, bid change) with its hypothesis and expected direction; once the change is past its attribution window, pull the before/after metrics and report the lift — explicitly as a directional read, never a controlled experiment, with confounds named. Append-only JSONL so changes stay comparable over time. Reads the linkedin-ads MCP's free analytics tools only. Triggers: "log this ad change", "did that change work", "paid experiment log", "before/after on the budget shift", "change journal". NOT a controlled A/B test (use /ab-testing) and NOT a full account audit (use /paid-ads-audit).
goal: Log paid-campaign changes hypothesis-first and report directional before/after lift with confounds stated.
outcome: An append-only change journal plus a per-change lift read (before vs after, directional, floored, confounds named) that feeds the next audit and the strategy refresh.
primitive: paid-marketing
sub_primitive: execution
ontology_type: experiment-log
review_gate: 1
inputs:
  required: []
  recommended:
    - paid-campaign-strategy
    - paid-ads-audit
depends_on: []
owned_by_agent: paid
mcps_used:
  - linkedin-ads
triggers:
  slash_commands:
    - /paid-ads-experiment-log
  natural_language:
    - "log this ad change"
    - "did that change work"
    - "before/after on the budget shift"
    - "paid change journal"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# Paid Ads Experiment Log — hypothesis-first change journal + directional lift

Paid changes rarely get measured — the budget moves, the creative swaps, and three weeks later nobody can say whether it helped. This skill logs each change *with its hypothesis at the moment you make it*, then reads the before/after once the window closes — honestly, as a directional read on a live account, never a controlled experiment.

**Adapted from** `github.com/stan-default/liam`'s `compute_lift` + `liam-experiments` (MIT), accessed 2026-07-14, via /steal — see [`.claude/discovery/0726-liam-steal-analysis.md`](../../../../discovery/0726-liam-steal-analysis.md). Concept port; no code reused.

---

## Doctrine inherited

- [`quantitative-evidence-floors.md`](../../../../rules/quantitative-evidence-floors.md) — lift is directional and floored. No "it worked" below the volume floor; state the counts, name the lag.
- [`linkedin-ads-spend.md`](../../../../rules/linkedin-ads-spend.md) — **read tools only**. This skill never calls a write tool.
- [`financial-data.md`](../../../../rules/financial-data.md) + [`pii-redaction.md`](../../../../rules/pii-redaction.md) + [`storage-policy.md`](../../../../rules/storage-policy.md) — ads data is client-confidential. The journal lives in the client folder; never commit it or raw exports to git; never fabricate a figure the MCP didn't return.

---

## The honesty rule — voice-locked

**A before/after on a live account is NOT a controlled experiment.** No holdout, no randomization — just the same account before and after, with everything else in the market also moving. If two changes overlapped, or a named confound could own the delta, the answer is *inconclusive*, not "it worked." A logged "we think this helped, here's the confound that would flip it" beats a confident fabrication every time.

---

## The two moves

### 1. Log the change — at the change, not after

One appended JSONL line per material change, written *when you make it* (the hypothesis is the point — a change logged without one can only be rationalized later, not judged):

```jsonl
{"date":"2026-07-14","account":"<id>","scope":"campaign|ad|group","touched":["<name>"],"change_type":"budget|creative|audience|bid|schedule|offer|structure","from":"<before>","to":"<after>","hypothesis":"<what you expect and why>","expect_metric":"CPL","expect_direction":"down","baseline_window":"2026-06-30..2026-07-13","baseline":{"spend":0,"impressions":0,"clicks":0,"ctr":0,"conversions":0,"cpl":0,"conv_rate":0}}
```

Baseline = the pre-change metrics over a window the *same length* as the after-window you'll measure against. Store at `{client}/paid/execution/paid-change-journal.jsonl` (append-only, client-confidential).

### 2. Read the lift — once past the attribution window

1. **Pull the after-window** (same length as baseline) via the MCP read tools (`get_campaign_performance`, `get_daily_trends`, `compare_performance`). Never a write tool.
2. **Compute before → after** on the hypothesis metric + the guardrail metrics (don't let CPL drop while conversions crater).
3. **Floor it.** Below the volume floor (`quantitative-evidence-floors.md` — <3 conversions, <~100 clicks, before a full window) → "too early, re-read at N", not a verdict.
4. **Name the confounds.** Seasonality, other concurrent changes, audience fatigue, attribution lag, denominator swings. If one could own the delta, the read is inconclusive.
5. **Verdict language:** *directionally validated* / *directionally invalidated* / *inconclusive (confound: X)* — never "proven."

---

## Anti-patterns

- ❌ Logging a change with no hypothesis — then you're rationalizing, not measuring.
- ❌ Calling a before/after a "test" or the result "proven."
- ❌ Crowning lift below the volume floor (a 30% CPL move on 5 conversions is noise).
- ❌ Ignoring a concurrent change that could own the delta.
- ❌ Committing the journal or a raw export to git — client folder only.

---

## Integration with other skills

- **Feeds `/paid-ads-audit`** — the journal is the "what we changed and what happened" context the audit reads.
- **Feeds `/paid-campaign-strategy`** — validated changes inform the refresh.
- **Sibling to `/ab-testing`** — that's a controlled test (holdout, randomization); this is observational before/after. Reach for `/ab-testing` when you can run a real split; reach for this when you can't and just need an honest read on a live change.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains + output template.

---

