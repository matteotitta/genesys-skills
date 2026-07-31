---
name: paid-ads-audit
version: '1.2'
last_updated: 2026-07-14
author: genesys-growth
description: Audits existing paid ad campaigns across Google Ads and LinkedIn Ads using a structured checklist. Covers account
  health, campaign structure, targeting configuration, creative quality, conversion tracking, and budget efficiency. Produces
  a scored audit report with prioritized recommendations and quick wins. Runs standalone with campaign data — no upstream
  dependencies required. Feeds findings into paid-campaign-strategy for strategy refresh, and into google-ads-copy or linkedin-ads-copy
  for creative improvements. Triggered by "ad audit", "campaign audit", "PPC audit", "paid performance review", "ads not working",
  "CPL too high", or "quarterly campaign health check". NOT for building new campaigns from scratch — use /paid-campaign-strategy
  instead.
goal: Audits existing paid ad campaigns across Google Ads and LinkedIn Ads using a structured checklist.
outcome: Audits existing paid ad campaigns across Google Ads and LinkedIn Ads using a structured checklist. Covers account
  health, campaign structure, targeting configuration, creative quality, conversion tracking, and budget efficiency. Produces
  a scored audit report with prioritized recommendations...
primitive: paid-marketing
sub_primitive: audit
ontology_type: content-audit
review_gate: 1
inputs:
  required: []
  recommended:
  - paid-campaign-strategy
- type: paid-ads-audit
  feeds_into:
  - paid-campaign-strategy
  - google-ads-copy
  - linkedin-ads-copy
depends_on: []
- google-ads-copy
- linkedin-ads-copy
- paid-campaign-strategy
owned_by_agent: paid
mcps_used: []
- gdrive
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Paid Ads Audit

Audit existing paid ad campaigns across Google Ads and LinkedIn Ads. Structured checklist covering account health, campaign structure, targeting, creative quality, tracking, and budget efficiency. Run quarterly or when performance degrades. No live API access required — works from campaign data provided by the user (screenshots, CSV exports, or verbal summary of metrics).

**Live LinkedIn Ads data (optional):** when the `linkedin-ads` MCP is authenticated, pull metrics directly instead of pasted CSVs — `get_campaign_performance`, `get_creative_performance`, `get_audience_demographics`, `get_daily_trends`, `compare_performance`. All reads are free and ungated; the MCP's write tools stay gated by `.claude/rules/linkedin-ads-spend.md`. Dormant until credentialed — see `.claude/mcp/linkedin-ads/README.md`.

---

## Triggers

Run this skill when:

- Quarterly campaign health check is due
- CPL has spiked and the cause is unclear
- A new client is inheriting an account from a prior agency or in-house team
- Performance regressed and a structural review is needed before strategy refresh

Do NOT run when:

- Building a new campaign from scratch — use `/paid-campaign-strategy`
- Single ad copy is the issue — use `/google-ads-copy` or `/linkedin-ads-copy`
- Landing page is the issue — use `/landing-page-audit`

---

## The Iron Law — voice-locked

**EVERY FINDING MUST BE BACKED BY DATA OR FLAGGED AS UNAVAILABLE.**

An audit built on assumptions is worse than no audit. If data is missing, say so. If a check can't be evaluated, mark it [UNAVAILABLE] and explain what data is needed.

**No exceptions:**

- "The account is probably fine" → Without data, you don't know. Flag the gap.
- "CPL seems high" → Compared to what? Cite the benchmark or mark as [ESTIMATED].
- "Just pause everything and restart" → Audit first. Most accounts need fixes, not demolition.
- "We can skip tracking" → Tracking is always the first audit category. No tracking = no optimization.

---

## Fix-priority order — voice-locked

Always tracking first, creative last. Fixing creative without tracking is optimizing blind.

1. **Tracking** — foundation; nothing else matters without it
2. **Structure** — architecture; affects everything downstream
3. **Targeting** — audience; right message to wrong people = waste
4. **Creative** — messaging; right people, now optimize the message
5. **Budget** — efficiency; optimize spend after everything else is clean

This order is non-negotiable. A high-priority creative fix never outranks a tracking gap, no matter how impactful the creative looks. If tracking is broken, every "creative win" is unprovable.

---

## Scoring bands — voice-locked

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100% | A | Well-optimized, minor tweaks only |
| 75-89% | B | Solid foundation, clear improvement areas |
| 60-74% | C | Structural issues, needs strategic attention |
| <60% | D | Major gaps, consider pause + restructure |

Each check is pass (1), warning (0.5), or fail (0). Category score = points earned / total possible. Overall score = average of category scores, weighted equally.

---

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **Campaign performance data** | Screenshots, CSV exports, verbal summary of metrics | Required |
| **paid-campaign-strategy** | Compare actual vs planned | Recommended |
| **Google Ads / Campaign Manager access** | Direct view-only access | Recommended |
| **GA4 conversion data** | For tracking-category checks | Recommended |
| **CRM lead data** | For attribution checks | Recommended |

---

## Process

**Five-phase flow:** Platform identification → Google Ads audit (6 categories, 45 checks) → LinkedIn Ads audit (5 categories, 25 checks) → Cross-platform checks → Scoring + 30/60/90 day recommendations. Full flowchart, scoring methodology, and B2B SaaS benchmarks in the premium reference. The full check library lives in the premium reference.

---

## Performance frameworks

The 75-check library finds configuration gaps; three diagnostic lenses read the numbers on top of it — the **KPI ladder** (Delivery → Engagement → Outcome, to localize where the leak is), **spend concentration + wasted spend** (the dollars sitting on ads with 0 conversions past the attribution window), and **ad bucketing** (drivers / promising / non-converters / too-early, with dollars attached). Every call obeys [`quantitative-evidence-floors.md`](../../../../rules/quantitative-evidence-floors.md) — no "top performer" or "pause" verdict below the volume floor; state the count, name the lag. Full frameworks in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent benchmark figures.** Cite the band from `process.md` or mark `[ESTIMATED]` with reasoning.
2. **Never assume tracking is fine.** If you can't verify GCLID flow / Insight Tag firing, mark Cat 1 / Cat 5 checks `[UNAVAILABLE]`.
3. **Never recommend pausing everything.** Audit-driven fixes preserve the parts that work.
4. **Never invent CPL / CAC / CTR numbers.** If client didn't share, list as `[UNAVAILABLE]` and ask.
5. **Never skip cross-platform checks.** A platform-only audit misses budget-allocation and attribution problems.
6. **Never crown a winner/loser below the volume floor.** Per [`quantitative-evidence-floors.md`](../../../../rules/quantitative-evidence-floors.md) — state the count behind any "top performer" or "pause" call. Below the floor (e.g. <3 conversions, <~100 clicks, before a full attribution window), it's a directional read with a "too early" caveat, not a verdict.

---

## Quality

Pre-delivery checklist (categories scored, fixes ordered, recommendations actionable, benchmarks cited, gaps flagged), worked example, anti-examples (vague CPL, skipped tracking, generic creative recs, wrong fix order), and failure-mode triage in the premium reference.

---

## Integration with Other Skills

### Upstream (consumes)

| Skill | What it provides | Required? |
|-------|-----------------|-----------|
| `paid-campaign-strategy` | Planned architecture for actual-vs-planned comparison | Recommended |

### Downstream (feeds into)

| Skill | How output is used |
|-------|-------------------|
| `paid-campaign-strategy` | Strategy refresh based on audit's priority fixes |
| `google-ads-copy` | Copy refresh when Ad Copy Quality category < 75% |
| `linkedin-ads-copy` | Creative refresh when Creative Health category < 75% |
| `landing-page-audit` | Page audit when Landing Pages category < 75% |

---

