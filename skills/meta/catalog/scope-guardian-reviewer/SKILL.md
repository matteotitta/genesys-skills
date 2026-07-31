---
name: scope-guardian-reviewer
version: '1.0'
last_updated: 2026-05-05
author: genesys-growth
description: 'Reviews client proposals, statements of work, and engagement scope documents for scope creep, mission drift, and unrealistic delivery commitments. Catches the common B2B SaaS consulting failure modes — open-ended deliverable lists, unbounded revision counts, undefined acceptance criteria, dependencies on undelivered client inputs. Produces a scope-risk-report with FAIL/WARN/PASS verdicts and tighter-scope rewrites. Triggers: "scope guard", "scope review", "is this proposal tight enough", "scope creep check". Recommended upstream: client-discovery-proposals, win-loss-analysis. Run before sending any proposal, scope-of-work, or change order. Composes with product-lens-reviewer and voice-reviewer.'
goal: Catch scope creep risks in proposals and engagement docs before they become unbillable rework.
outcome: Produces a scope-risk-report flagging open-ended deliverables, unbounded revisions, missing acceptance criteria, and dependencies on undelivered client inputs — with specific tighter-scope rewrites.
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended: []
- type: scope-risk-report
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /scope-guardian-reviewer
  natural_language:
  - "scope guard"
  - "scope review"
  - "is this proposal tight enough"
  - "scope creep check"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: low
disable-model-invocation: true
---

# Scope-guardian reviewer

Review proposals, scope-of-work documents, and engagement plans for scope creep risks before they become unbillable rework. Adapted from `ce-scope-guardian-reviewer` agent in [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT).

The most expensive bug in a B2B SaaS consultancy is a proposal that promises everything. This reviewer catches it before send.

## When to run

Invoke when the user says:
- "Run scope guard on [proposal]"
- "Is this proposal tight enough?"
- "Scope creep check"
- "Pre-send review on [SOW]"
- "Will this scope kill us?"

Do NOT invoke when:
- User wants voice review → `voice-reviewer`
- User wants product strategy review → `product-lens-reviewer`
- User wants legal contract review → `legal:review-contract`

Composes with: `product-lens-reviewer`, `voice-reviewer`. Run as the **last** step before sending any client-facing scope document.

## Inputs

**Required:**
- Proposal / SOW / engagement document text

**Recommended:**
- `win-loss-analysis` — what scope patterns won/lost in the past
- Prior client engagement records (in `projects/consulting/active/{client}/`)

## The 5 dimensions

| # | Dimension | Trigger |
|---|---|---|
| 1 | **Open-ended deliverables** | "ongoing support," "as needed," "TBD," "iterative refinement" without count → FAIL |
| 2 | **Unbounded revisions** | "unlimited revisions," "until satisfied," missing revision count → FAIL |
| 3 | **Missing acceptance criteria** | Each deliverable should have a measurable "done" definition. No criteria → WARN |
| 4 | **Client-input dependencies** | Deliverable depends on data/access/feedback the client hasn't committed to providing on a date → WARN/FAIL |
| 5 | **Mission drift** | Are deliverables in the original engagement's lane? A messaging engagement that includes "build a website" → FAIL |

## Verdict logic

| Inputs | Verdict |
|---|---|
| All PASS | **Send it** |
| Any WARN, no FAIL | **Tighten before send** |
| Any FAIL | **Don't send — rewrite** |

## Anti-hallucination guardrails

1. **Quote the actual text.** When flagging an issue, quote the open-ended phrase.
2. **Don't flag standard practice as creep.** "30-day support window" with end date = PASS, not FAIL.
3. **Be specific about fixes.** "Tighten this" is not a fix. "Replace 'ongoing support' with 'two 30-min check-ins, one each at week 4 and week 8'" is a fix.
4. **Don't moralize.** This isn't about whether the price is right; it's about whether the scope is bounded.

## Self-roast (pre-delivery)

- [ ] All 5 dimensions evaluated
- [ ] Each finding has quoted evidence
- [ ] Fixes are specific enough to drop into the proposal
- [ ] If a dimension PASSed because of an explicit bound (date, count, criteria), the bound is quoted

# Scope-guardian review: {proposal name} ({YYYY-MM-DD})

**Verdict:** Send it | Tighten before send | Don't send — rewrite

## Score table
| Dimension | Verdict | Notes |
|---|---|---|
| 1. Open-ended deliverables | PASS/WARN/FAIL |... |
|... |... |... |

## Findings
**§{N} {Dimension}** — {verdict}
> "{quoted text}"
**Fix:** {specific bounded replacement}

## Suggested tighter-scope rewrites
{paste-ready replacements for each FAIL}
```

## Composition rule reference

Scope-guardian-reviewer is one node in the **lens-reviewer pattern** (P6). See [.claude/rules/pm-loop.md](../../../../rules/pm-loop.md). Most useful when run alongside `product-lens-reviewer` (catches strategy creep) and `voice-reviewer` (catches tone drift).

## Attribution

Adapted from [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT). Source agent: `ce-scope-guardian-reviewer`. Pattern: pluggable lens-reviewers (P6 from /steal Phase 4).

