---
name: product-lens-reviewer
version: '1.0'
last_updated: 2026-05-05
author: genesys-growth
description: 'Reviews any document — strategy doc, spec, brief, launch plan, proposal — through a product POV across 6 dimensions: target-problem clarity, persona focus, metric quality (anti-vanity), differentiation defensibility, scope discipline, and shipping-as-experiment framing. Produces a scored product-review-report with FAIL/WARN/PASS verdicts and rewrite suggestions. Triggers: "product review", "review through product lens", "PM review", "is this strategy any good". Recommended upstream: strategy-doc, positioning, icp-research. Run before locking strategy docs, sending client proposals, or shipping launch plans. Composes with voice-reviewer and design-reviewer. NOT for code/PR review (engineering:code-review).'
goal: Review documents through a product POV across 6 dimensions and surface FAIL/WARN/PASS verdicts with rewrite suggestions.
outcome: Produces a scored product-review-report that catches the common product-thinking failure modes — vague target problem, unfocused personas, vanity metrics, undifferentiated approach, scope creep, missing experiment framing — before the document ships.
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended:
  - strategy-doc
  - positioning
  - icp-research
- type: product-review-report
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /product-lens-reviewer
  natural_language:
  - "product review"
  - "review through product lens"
  - "PM review"
  - "is this strategy any good"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: medium
disable-model-invocation: true
---

# Product-lens reviewer

Review any document through a product POV. Composes with `voice-reviewer` (style/voice) and `design-reviewer` (visual/UX). Adapted from `ce-product-lens-reviewer` agent in [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT).

This is the structural counterpart to voice-reviewer. Voice asks "does this sound right?"; product asks "does this *think* right?"

## When to run

Invoke when the user says:
- "Run product review on [doc]"
- "Review this through a product lens"
- "PM review this strategy"
- "Is this strategy any good?"
- "Pre-lock review on [strategy-doc / proposal / launch plan]"

Do NOT invoke when:
- User wants voice review → `voice-reviewer`
- User wants visual review → `design-reviewer`
- User wants code review → `engineering:code-review`

Composes with: `voice-reviewer`, `design-reviewer`, `scope-guardian-reviewer` (often run together as a review-pass family before locking strategic docs).

## Inputs

**Required:**
- The document to review (text)

**Recommended:**
- `strategy-doc` (if reviewing a strategy doc, comparing against itself; if reviewing a downstream artifact like a launch plan, comparing against the upstream strategy)
- `positioning` (cross-check differentiation defensibility)
- `icp-research` (cross-check persona focus)

## The 6 dimensions

Each dimension scores PASS / WARN / FAIL with quoted evidence.

| # | Dimension | Trigger |
|---|---|---|
| 1 | **Target-problem clarity** | Is the problem specific, recurring, expensive? Cited evidence vs. generic? |
| 2 | **Persona focus** | One persona ideally; if 3+ — FAIL (audience, not persona) |
| 3 | **Metric quality** | SMART criteria; anti-vanity-metrics rule — page views/impressions/MAU without conversion → FAIL |
| 4 | **Differentiation defensibility** | Would a skeptical buyer choose this over alternatives? Cite the alternative + why this beats it |
| 5 | **Scope discipline** | Does the doc stay in its lane? Strategy doesn't include requirements (K6); spec doesn't include strategy; proposal doesn't blur with positioning |
| 6 | **Shipping-as-experiment framing** | Is the ship treated as data generation (K1)? Hypothesis stated? Falsifiable? |

For full rule set with examples → the premium reference (deferred — created on first real run).

## Verdict logic

| Inputs | Verdict |
|---|---|
| All PASS | **Ship it** |
| Any WARN, no FAIL | **Minor fixes recommended** |
| Any FAIL | **Fix before shipping** |

## Anti-hallucination guardrails

1. **Quote the actual text** when flagging an issue. No paraphrase.
2. **Don't flag style preferences as violations.** This is product, not voice. If the issue is tone, route to voice-reviewer.
3. **Don't over-flag intentional choices.** A two-persona strategy might be intentional — check the doc's justification before flagging.
4. **Be specific about fixes.** "Sharpen the persona" is not a fix. "Drop 'marketers' — keep only 'product managers in B2B SaaS, 50-200 employees, post-Series A'" is a fix.

## Self-roast (pre-delivery)

- [ ] All 6 dimensions evaluated
- [ ] Each finding has quoted evidence
- [ ] Fixes are specific enough to implement without guessing
- [ ] Composition checked — voice/design issues routed to the right reviewer (don't report style issues here)
- [ ] At least one cross-reference to upstream artifact (strategy-doc / positioning / icp-research) when available

# Product-lens review: {doc name} ({YYYY-MM-DD})

**Verdict:** Ship it | Minor fixes | Fix before shipping

## Score table
| Dimension | Verdict | Notes |
|---|---|---|
| 1. Target-problem clarity | PASS/WARN/FAIL |... |
|... |... |... |

## Findings
**§{N} {Dimension}** — {verdict}
> "{quoted text}"
**Fix:** {specific replacement or reframe}

## Cross-references checked
- {strategy-doc / positioning / icp-research} — {alignment notes}
```

## Composition rule reference

Product-lens-reviewer is one node in the **lens-reviewer pattern** (P6). Composes with voice-reviewer (style), design-reviewer (visual), scope-guardian-reviewer (scope creep), coherence-reviewer (internal consistency, when built). See [.claude/rules/pm-loop.md](../../../../rules/pm-loop.md).

## Attribution

Adapted from [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT). Source agent: `ce-product-lens-reviewer`. Pattern: pluggable lens-reviewers applied to strategy docs (P6 from /steal Phase 4).

