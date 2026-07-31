---
name: abm-campaign
version: '1.0'
last_updated: 2026-03-25
author: genesys-growth
description: 'Designs account-based marketing campaigns with tiered outreach across three personalization levels: 1:1 bespoke
  plays for strategic accounts, 1:few for segments, and 1:many programmatic sequences. Produces target account programs, reactivation
  campaigns, and tiered engagement plans. Depends on icp-research and lead-scoring for account selection and tiering. Feeds
  into outreach-emails, lifecycle-marketing, and sales-enablement. Triggered by "ABM", "account-based", "target accounts",
  "reactivation campaign", or "tiered campaign". NOT for broad lifecycle marketing (use /lifecycle-marketing instead).'
goal: 'Designs account-based marketing campaigns with tiered outreach across three personalization levels: 1:1 bespoke plays
  for strategic accounts, 1:few for segments, and 1:many programmatic sequences.'
outcome: 'Designs account-based marketing campaigns with tiered outreach across three personalization levels: 1:1 bespoke
  plays for strategic accounts, 1:few for segments, and 1:many programmatic sequences. Produces target account programs, reactivation
  campaigns, and tiered engagement plans. Depends on...'
primitive: outbound
sub_primitive: strategy
ontology_type: launch-plan
review_gate: 2
inputs:
  required:
  - lead-scoring
  - company-context
  recommended:
  - icp-research
  - company-context
  - product-messaging
- type: launch-plan
  feeds_into:
  - outreach-emails
depends_on:
- lead-scoring
- company-context
- outreach-emails
owned_by_agent: sales
mcps_used:
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
effort: high
---

# ABM Campaign

Build and execute account-based marketing campaigns across three tiers of personalization. From fully bespoke 1:1 plays for strategic accounts to programmatic 1:many sequences at scale.

**Research substrate (Exa):** primary tools `company_research_exa`, `web_search_exa` for account-level intel + trigger events. Citations per `.claude/rules/exa-protocol.md` (`[VERIFIED: exa_search, {url}, accessed YYYY-MM-DD]`). Quality gate: ≥3 sources per major claim, ≥50% verified, date filter for any "recent" claim.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "build an ABM campaign"
- "account-based marketing for [client]"
- "target account list"
- "tiered outreach campaign"
- "reactivation campaign for [segment]"
- "re-engage churned accounts"
- "1:1 account plays"
- "programmatic ABM"

**Do NOT invoke when:**
- User wants broad lifecycle campaigns → use `lifecycle-marketing`
- User wants a single cold email → use `outreach-emails`
- User wants lead nurture sequences → use `lifecycle-marketing`
- User wants content strategy without account targeting → use `content-strategy`

---

## Three tiers of ABM (voice-locked)

ABM isn't one-size-fits-all. The tier determines how much time, research, and personalization goes into each account. Pick the right tier based on deal size, strategic value, and available bandwidth.

### Tier 1: 1:1 (strategic accounts)

| Dimension | Specification |
|-----------|---------------|
| **Account count** | 5-15 accounts |
| **Personalization** | Fully bespoke. Custom research, messaging, and assets per account |
| **Research depth** | Deep dive: org chart, trigger events, stakeholder mapping, competitive displacement |
| **Engagement model** | Multi-threaded. Target 3-5 stakeholders per account across roles |
| **Channel mix** | Email + LinkedIn + direct mail + personalized content + events/webinars |
| **Cadence** | 12-20 touches over 8-12 weeks per stakeholder |
| **When to use** | High ACV ($50K+), strategic logos, competitive displacement, expansion plays |

### Tier 2: 1:few (segment plays)

| Dimension | Specification |
|-----------|---------------|
| **Account count** | 50-100 accounts grouped into 3-5 segments |
| **Personalization** | Segment-level. Same pain points, same industry, same use case |
| **Research depth** | Segment research: common challenges, industry trends, shared triggers |
| **Engagement model** | Single-threaded initially, multi-thread on engagement signal |
| **Channel mix** | Email + LinkedIn + retargeting ads |
| **Cadence** | 8-12 touches over 6-8 weeks |
| **When to use** | Mid-market ACV ($10-50K), clear segment patterns, semi-automated execution |

### Tier 3: 1:many (programmatic)

| Dimension | Specification |
|-----------|---------------|
| **Account count** | 200-500+ accounts |
| **Personalization** | Dynamic. Merge fields for name, company, pain point, industry |
| **Research depth** | Enrichment-level: firmographics, technographics, intent data |
| **Engagement model** | Single-threaded, automated sequences |
| **Channel mix** | Email + LinkedIn automation + programmatic ads |
| **Cadence** | 6-8 touches over 4-6 weeks |
| **When to use** | Lower ACV ($5-15K), volume plays, market awareness, pipeline generation |

---

## Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Campaign goal** | Specific outcome with success metric | User specifies |
| **Target market/segment** | Who we're going after, why now | User + ICP context |
| **Account list or criteria** | Existing list OR rules to build one | User-provided / Clay / Apollo |
| **Channels available** | Email, LinkedIn, ads, direct mail | User specifies |
| **Tooling available** | CRM, enrichment, sequence platform | User specifies |

---

## Process

**Six-phase flow:** Account selection & tiering → Account intel → Play design → Content creation → Execution → Measurement. Each phase has tier-specific outputs. Full step-by-step + fit scoring + cadence templates + MCP integration in the premium reference.

**Reactivation play** (sub-workflow for cold/churned/dormant accounts) also documented in the premium reference.

---

## Anti-hallucination guardrails

1. **Never invent account data.** Only use verified firmographics from Clay, Apollo, or user-provided lists.
2. **Never fabricate engagement history.** Check CRM or Gmail for actual touchpoint history.
3. **Never assume stakeholder names.** Use enrichment tools or mark as `[PLACEHOLDER: champion name]`.
4. **Never invent intent signals.** Only reference verified intent data or observable behavior.
5. **Mark missing data explicitly.** Use `[PLACEHOLDER: description]` for anything unconfirmed.
6. **No fake urgency.** Only use urgency when there's a real trigger event or deadline.

Per Apollo credit gate (`.claude/rules/apollo-credits.md`): search is free; enrichment costs credits. Always confirm spend before bulk enrichment.

---

## Quality

Pre-delivery checks cover campaign structure (tiering rationale, cadence realism), content quality (Tier 1 hand-written feel, "would they forward?" test), and data quality (no invented stakeholders or engagement history). Worked example + anti-examples (over-tiering, generic Tier 1, Tier 3 cadence pretending to be Tier 2) + post-launch failure-mode triage in the premium reference.

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **icp-research** | `depends_on` | ICP criteria for account scoring and segmentation |
| **lead-scoring** | `depends_on` | Tier assignments use the scored account list |
| **company-context** | `feeds_into` | Deep account research for Tier 1 intelligence briefs |
| **product-messaging** | `feeds_into` | Value props and messaging for email and content creation |
| **outreach-emails** | `feeds_into` | Individual email drafts within ABM cadences |
| **lifecycle-marketing** | `feeds_into` | Post-conversion nurture for won ABM accounts |
| **sales-enablement** | `feeds_into` | Handoff materials when accounts hit engagement threshold |
| **competitor-research** | `enhances` | Competitive context for Tier 1 displacement plays |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

