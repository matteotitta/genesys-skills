---
name: niche-signal-discovery
version: '1.1'
last_updated: 2026-05-01
author: genesys-growth
description: 'Discovers buying signals, timing triggers, and intent indicators for target accounts using Deepline signal plays
  plus MCP enrichment. Answers "when to reach out" — not "who to reach out to" (that''s /clay-search or /build-tam) or "how
  to enrich contacts" (that''s /deepline-enrich). Covers 9 signal categories: hiring signals, fundraising alerts, competitive
  displacement, champion tracking, deal risk, company news, ad intelligence, closed-lost recovery, and custom signal classification.
  Outputs signal-enriched account lists that feed into /lead-scoring, /outreach-emails, and /abm-campaign. Triggered by "find
  buying signals", "which accounts are ready", "timing triggers", "intent signals", "who''s hiring for X", "fundraising alerts",
  or "competitive displacement".'
goal: Discovers buying signals, timing triggers, and intent indicators for target accounts using Deepline signal plays plus
  MCP enrichment.
outcome: Discovers buying signals, timing triggers, and intent indicators for target accounts using Deepline signal plays
  plus MCP enrichment. Answers "when to reach out" — not "who to reach out to" (that's /clay-search or /build-tam) or "how
  to enrich contacts" (that's /deepline-enrich). Covers 9 signal...
primitive: outbound
sub_primitive: list-building
ontology_type: lead-assessment
review_gate: 1
inputs:
  required: []
  recommended:
  - deepline-enrich
  - company-context
  - icp-research
  - competitor-research
- type: signal-enriched-account-list
  feeds_into:
  - lead-scoring
  - outreach-emails
  - abm-campaign
- type: competitive-displacement-opportunities
  feeds_into:
  - battlecards
  - outreach-emails
- type: deal-risk-assessment
  feeds_into:
  - sales-enablement
depends_on: []
- abm-campaign
- battlecards
- lead-scoring
- outreach-emails
- sales-enablement
owned_by_agent: operator
mcps_used:
- apify
- apollo-io
- deepline
- exa
- gdrive
- notion
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

# /niche-signal-discovery — Buying signals, timing triggers, intent intelligence

Find the signals that tell you WHEN to reach out — not who. Signal-based outreach achieves ~18% response rates vs ~3.4% for generic cold email. First responder post-trigger event is 5× more likely to win the deal.

**Research substrate (Exa):** primary tool `web_search_exa` for company news / fundraising / hiring confirmation. Citations per `.claude/rules/exa-protocol.md`. Date-filter mandatory for any "recent" claim.

**Extracted from:** `/deepline-enrich` Phase F split (2026-04-04). Apify slot integration aligns with `.claude/rules/apify-credits.md`.

---

## When to use this vs. other skills — voice-locked routing

| Skill | Question it answers |
|-------|-------------------|
| `/clay-search` or `/build-tam` | **Who** should we target? (People discovery) |
| `/deepline-enrich` | **How** do we reach them? (Emails, phones, enrichment) |
| `/niche-signal-discovery` | **When** should we reach out? (Timing + intent) |
| `/lead-scoring` | **How ready** are they? (Qualification + prioritization) |
| `/outreach-emails` | **What** do we say? (Personalized sequences) |

**Handoff pattern:** `/deepline-enrich` (enriched list) → `/niche-signal-discovery` (signal overlay) → `/lead-scoring` (prioritize) → `/outreach-emails` (write sequences)

---

## Signal categories — 9 total

Hiring · Fundraising · Competitive displacement · Champion tracking · Deal risk · Company news · Ad intelligence · Closed-lost recovery · Signal classification (custom).

Each category has a Deepline play + MCP alternative + signal strength + output shape. Full catalog with commands in the premium reference.

---

## Signal stacking — voice-locked decision logic

Individual signals are noisy. Stacking multiple signals creates high-confidence triggers.

| Signal combo | Confidence | Action |
|-------------|-----------|--------|
| Hiring + Fundraising | Very High | Immediate outreach — budget AND need confirmed |
| Competitor engagement + Champion move | Very High | Warm intro via champion at new company |
| Job change + ICP fit | High | Personalized re-engagement |
| Fundraising alone | High | Outreach within 30 days of announcement |
| Hiring alone | Moderate | Monitor for additional signals |
| Company news alone | Low | Add to nurture, don't cold outreach |
| Competitor engagement alone | Moderate | Personalized displacement pitch |

---

## Thin-input guard — voice-locked safety rule

**Rule:** If the signal inventory for a segment has fewer than 3 active (STRONG or MODERATE recency) signals across 5+ sampled accounts, **do not recommend a signal-based outbound play for that segment**. Report the thin-signal finding back to the user and suggest either (a) broadening the segment, (b) switching to `/build-tam` for fit-based targeting, or (c) waiting for signal density to build.

Adopted from Gooseworks `industry-scanner` (via `/steal` 2026-04-21). Forcing a signal-based play on sparse data produces false-confident campaign plans — the signals exist, but they're too thin to justify the strategy hanging on them.

---

## Credit gate — voice-locked

Signal discovery uses the same Deepline credit system as `/deepline-enrich`. Apollo enrichment overlays follow `.claude/rules/apollo-credits.md`. Apify scrapes follow `.claude/rules/apify-credits.md`.

| Batch size | Gate level | Action |
|------------|-----------|--------|
| 1-10 accounts | No gate | Run immediately |
| 11-50 accounts | Soft gate | Show estimate, proceed unless user objects |
| 51+ accounts | Hard gate | Show estimate, wait for explicit approval |

---

## Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Target account list** | Domain + company name, ideally ICP-fit pre-filtered | `/build-tam`, `/clay-search`, `/deepline-enrich` |
| **Pipeline deal list** | Active deals (for deal-risk plays) | CRM export (Attio, HubSpot, Salesforce) |
| **Competitor list** | 2-3 key competitors (for displacement) | `/competitor-research` upstream |
| **Lost deals** | Closed-lost recoveries (90+ days) | CRM export |

---

## Process

**Three primary workflows:** Signal-based outbound campaign (classify → category-specific plays → merge → score → personalize), Competitive displacement campaign (Mentions + Intel + Email waterfall + Displacement angle), Pipeline risk monitoring (CRM export → Deal Risk Combos → Champion Tracking → risk report). Step-by-step + MCP integration in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent signals.** Cite source per `.claude/rules/exa-protocol.md` for any external evidence.
2. **Don't fabricate recency.** Always include the signal date; mark `[UNAVAILABLE]` if unknown.
3. **Verify ICP fit before signal harvest.** Signals on bad-fit accounts = wasted credits.
4. **Don't escalate single weak signals to outreach.** Stack first per the matrix above.
5. **Respect signal decay.** Stale signals get demoted, not surfaced as fresh.

---

## Quality

Pre-delivery checks cover coverage (≥80% classified, CONTRACTION filtered), quality (stacking applied, thin-input guard tested, citations present), and cost discipline (gates respected). Common-mistakes table (single-signal escalation, stale signal acted-on, force-fit on thin data) + worked example (3-signal Series B / hiring / competitor-engagement stack) + anti-examples + quality gate (active-signal density ≥60%, ≥20% Very High band) in the premium reference.

---

## Integration with the engagement workflow

Assigned to the **Researcher** role-agent (or Operator for batch runs). Slots into:
- **Context refresh:** Monthly signal refresh on active target accounts
- **Outbound:** Signal overlay step between enrichment and sequence writing
- **Sales pipeline:** Pipeline risk monitoring as recurring task

---

## Handoff Patterns

| From | To | What passes |
|------|----|-------------|
| `/deepline-enrich` | `/niche-signal-discovery` | Enriched account list for signal overlay |
| `/build-tam` | `/niche-signal-discovery` | Target account list for signal classification |
| `/niche-signal-discovery` | `/lead-scoring` | Signal-enriched accounts for prioritization |
| `/niche-signal-discovery` | `/outreach-emails` | Signal context for personalization angles |
| `/niche-signal-discovery` | `/abm-campaign` | Tiered signal accounts for ABM tiers |
| `/niche-signal-discovery` | `/battlecards` | Competitive displacement intelligence |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

