---
name: ship-learnings
version: '1.0'
last_updated: 2026-05-05
author: genesys-growth
description: 'Captures post-ship compound-learnings for a completed feature, release, or experiment. Records what worked, what didn''t, what to do differently, and whether the underlying strategy hypothesis was validated or invalidated. Distinct from /session-wrap (session-scoped) — this is ship-scoped and accumulates evidence across cycles for the next strategy refresh. Triggers: "ship learnings", "we just shipped X — what did we learn", "post-mortem [feature]", "post-ship review". Required upstream: strategy-doc (the hypothesis being tested). Feeds strategy-doc refreshes and the broader compounding-learnings library. NOT for incident postmortems (engineering:incident-response) or session wrap-ups (/session-wrap).'
goal: Capture compound-learnings from a completed ship so the next strategy refresh has accumulated evidence.
outcome: Produces a ship-learnings record that feeds back into the next strategy-doc refresh, with explicit hypothesis validation/invalidation, what-worked/what-didn't analysis, and follow-on experiments.
primitive: product-management
sub_primitive: strategy
ontology_type: ship-learnings
review_gate: 1
inputs:
  required:
  - strategy-doc
  recommended:
  - product-pulse
- type: ship-learnings
  feeds_into:
  - strategy-doc
depends_on:
- strategy-doc
- strategy-doc
owned_by_agent: product-manager
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /ship-learnings
  natural_language:
  - "ship learnings"
  - "post-ship review"
  - "what did we learn from [feature]"
  - "compound learnings"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: low
---

# Ship-learnings — post-ship compound-learnings capture

Capture what we learned from a completed ship so the next strategy refresh has accumulated evidence. Adapted from `/ce-compound` in [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT).

Per Moretti's framing (K1): **everything that ships is an experiment.** Each ship tests a hypothesis from the strategy doc. Capture the result.

## When to run

Invoke when the user says:
- "We just shipped [feature] — what did we learn?"
- "Run ship-learnings on [release]"
- "Post-ship review for [experiment]"
- "Compound learnings"

Do NOT invoke when:
- The session is the unit (use `/session-wrap` for session-scoped wrap)
- The ship is broken / incident (use `engineering:incident-response`)
- No ship has occurred — this is post-ship only

## Distinct from /session-wrap

| Skill | Scope | When |
|---|---|---|
| `/session-wrap` | One Claude Code session | End of session |
| **`/ship-learnings`** | One ship / release / experiment | After feature ships, regardless of how many sessions it took |

A ship may span 5 sessions; one ship-learnings record captures all of them.

## Inputs

**Required:**
- Locked `strategy-doc` (the hypothesis being tested by this ship)
- Ship description: name, date shipped, scope summary

**Recommended:**
- Latest `product-pulse` (the metric movement post-ship)
- User feedback / quotes / support tickets from the ship period
- Original strategy track this ship belongs to

## Steps

1. **Phase 1 — Load context.** Read locked `strategy-doc` + latest `product-pulse`. Identify which strategy track this ship belonged to.
2. **Phase 2 — Pull ship signals.** Metric deltas (from pulse), user quotes, support volume changes, anomalies.
3. **Phase 3 — Run interview.** Walk the user through the 7-section structure. The hardest section is **§3 Result** — push back if the user says "kind of worked" without evidence.
4. **Phase 4 — Compose record.** Apply length discipline: ≤ 600 words total.
5. **Phase 5 — Self-roast.** Run checks below.
6. **Phase 6 — Push.** Save to ship-learnings folder + flag in next strategy refresh review.

## Self-roast (run before push)

- [ ] Hypothesis is quoted directly from strategy-doc (not paraphrased)
- [ ] §3 Result has explicit verdict (validated / partial / invalidated) — not vague
- [ ] §3 Result cites specific evidence (metric delta from pulse, user quote, ticket count) — not opinion
- [ ] §4 What worked and §5 What didn't are concrete (specific decisions / patterns) — not generic ("communication was good")
- [ ] §6 Action items have owners
- [ ] §7 Follow-on experiments are testable hypotheses, not vague ideas
- [ ] Total word count ≤ 600 (compounding-learnings should be easy to skim across many ships)
- [ ] Framing K1 applied: "shipping is an experiment" — verdict is data, not judgment

# Ship-learnings: {feature name} ({YYYY-MM-DD})

**Strategy track:** {track name from strategy-doc} · **Pulse ref:** {latest pulse path}

## Ship summary
{1-2 lines}

## Hypothesis (from strategy-doc)
> {direct quote from strategy-doc}

## Result: {validated | partially validated | invalidated}
{paragraph with evidence}

## What worked
-...

## What didn't work
-...

## What to do differently next time
- **{action}** — owner: {name}

## Follow-on experiments
-...
```

## Composition rule reference

Ship-learnings is the feedback node in the **PM closed loop** (P3). Strategy → pulse → ship → ship-learnings → strategy refresh. See [.claude/rules/pm-loop.md](../../../../../rules/pm-loop.md).

## Attribution

Adapted from [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT). Source pattern: `/ce-compound`. Framing basis: K1 "everything that ships is an experiment" from Marcus Moretti's AI PM Guide.

