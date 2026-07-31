---
name: google-ads-copy
version: '1.1'
last_updated: 2026-05-01
author: genesys-growth
description: 'Creates Google Ads Responsive Search Ad (RSA) copy for B2B SaaS campaigns structured around a 5-pillar model:
  brand, competitor, high-intent, problem-aware, and remarketing. Produces 15 headlines (30 chars) and 4 descriptions (90
  chars) per ad group, organized by campaign pillar with pinning recommendations and keyword insertion tokens. Depends on
  paid-campaign-strategy as required input. Feeds into ad-creative-brief for visual production. Triggered by "Google Ads copy",
  "RSA headlines", "search ad copy", "competitor ads", "PPC copy", or "ad headlines". NOT for LinkedIn ad formats — use /linkedin-ads-copy
  instead. NOT for strategy — use /paid-campaign-strategy first.'
goal: 'Creates Google Ads Responsive Search Ad (RSA) copy for B2B SaaS campaigns structured around a 5-pillar model: brand,
  competitor, high-intent, problem-aware, and remarketing.'
outcome: 'Creates Google Ads Responsive Search Ad (RSA) copy for B2B SaaS campaigns structured around a 5-pillar model: brand,
  competitor, high-intent, problem-aware, and remarketing. Produces 15 headlines (30 chars) and 4 descriptions (90 chars)
  per ad group, organized by campaign pillar with pinning...'
primitive: paid-marketing
sub_primitive: execution
ontology_type: landing-page-copy
review_gate: 2
inputs:
  required:
  - paid-campaign-strategy
  recommended:
  - competitor-research
  - product-messaging
  - icp-behavioural
- type: google-ads-copy
  feeds_into:
  - ad-creative-brief
depends_on:
- paid-campaign-strategy
- ad-creative-brief
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
effort: medium
---

# Google Ads Copy

Generate Responsive Search Ad (RSA) copy for B2B SaaS campaigns. Structured around the 5-pillar campaign model. Enforces Google Ads character limits. Outputs in TSV format ready for Google Sheets or Google Ads Editor import.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in google-ads-copy |
|---|---|---|
| **R1** | Source placement | RSA copy is **end-customer-facing**. No source tags. |
| **R3** | Product-update tone | Headlines + descriptions frame as "[Product] does X" not "introducing." |
| **R5** | Blog as voice anchor | When campaign has anchor blog, RSA headline 1 mirrors blog opener (within character limit). |
| **R6** | CTA hierarchy | Display URL + final URL → trial / sign-up primary. "Learn more" only when intent is research-stage. |
| **R9** | Action-oriented section names | Headline + description structures verb-led. |

---

## Triggers

Run this skill when:

- Paid-campaign-strategy is locked and Google Ads RSA copy is the next step
- A client wants competitor / brand / high-intent / problem-aware / remarketing copy
- Existing RSAs have low Ad Strength or CTR and need a refresh
- A new competitor enters scope and a dedicated campaign needs copy

Do NOT run when:

- Strategy isn't locked — run `/paid-campaign-strategy` first
- Target channel is LinkedIn — use `/linkedin-ads-copy`
- Ad extensions (sitelinks, callouts, structured snippets) are the ask — separate workflow

---

## RSA constraints — voice-locked

| Element | Limit | Count |
|---------|-------|-------|
| Headlines | ≤30 characters each | Up to 15 |
| Descriptions | ≤90 characters each | Up to 4 |
| Display URL path | ≤15 characters each | 2 paths |
| Pinning | Optional | Max 3 headlines per position |

**Critical rules:**
- Headlines must work independently and in any combination
- Google shows 2-3 headlines and 1-2 descriptions per impression
- Never use Dynamic Keyword Insertion on competitor campaigns
- Ad strength target: "Good" or "Excellent"
- Include at least 4 ad extensions per ad group (handled separately)

---

## The Iron Law — voice-locked

**EVERY CHARACTER COUNT MUST BE VERIFIED.**

Google Ads will reject any headline over 30 characters or description over 90 characters. There is no "close enough." Count every character including spaces and punctuation.

**No exceptions:**

- "It's only 1 character over" → Google rejects it. Trim it.
- "Can we use the full 150 chars?" → Google RSA limits are 30/90. Not 150.
- "These headlines need to go together" → RSA headlines display in ANY combination. Each must work alone.
- "Use Dynamic Keyword Insertion" → NEVER on competitor campaigns (trademark risk).

---

## 5-pillar invariants — voice-locked

- **One ad group per competitor.** Mixing competitors in one ad group inflates CPCs and confuses match-type matching.
- **Each competitor campaign attacks a *different* weakness.** Recycling the same attack across competitors wastes budget.
- **Brand campaign always runs.** Even if low-volume, it protects branded search from competitor encroachment.
- **Remarketing audiences progress through warmth.** Educational (1-7d) → case study (7-30d) → demo CTA (30-90d). Don't lead with demo CTAs to fresh visitors.
- **Headline diversity across categories** — attack (3-5) + benefit (4-6) + proof (2-3) + CTA (2-3). Skewed sets produce Poor Ad Strength.

---

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **paid-campaign-strategy** | Campaign architecture, keywords, audiences | Required |
| **competitor-research** | Competitor weaknesses for attack headlines | Recommended (required for competitor campaigns) |
| **product-messaging** | Value props, proof points, differentiators | Recommended |
| **icp-behavioural** | Customer language, pain phrasing | Recommended |

---

## Process

**Four-phase flow:** Campaign-type selection → Headline generation (15 per ad group, 4 categories) → Description generation (4 per ad group, D1-D4 framework) → Verification + TSV output. Full flowchart, 5-pillar campaign types, headline strategy, description framework, pinning rules, negative keyword seed list, and budget guidance in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent customer counts, awards, or rankings.** If not in product-messaging or proof points, mark `[NOT AVAILABLE]` and remove the headline.
2. **Never approximate character counts.** Count every char including spaces; one over = trim or rewrite.
3. **Never use DKI on competitor campaigns.** Trademark risk; Google will pause the campaign.
4. **Never put a competitor's name in the display URL or final URL.** Same trademark issue.
5. **Never repeat an attack headline across competitors.** Each competitor campaign needs its own weakness, not a paraphrase.

---

## Quality

Self-evaluation checklist (char compliance, no DKI on competitor, headline independence, diversity, no invented proof), worked example (ClientCo vs Saturn campaign), anti-examples (31-char headlines, mixed competitor ad groups, paraphrased attacks, generic verbs), failure-mode triage in the premium reference.

---

## Integration with Other Skills

### Upstream (consumes)

| Skill | What it provides | Required? |
|-------|-----------------|-----------|
| `paid-campaign-strategy` | Campaign architecture + keywords | Required |
| `competitor-research` | Competitor weaknesses for attacks | Required for competitor campaigns |
| `product-messaging` | Value props + proof points | Recommended |
| `icp-behavioural` | Customer language + pain framing | Recommended |

### Downstream (feeds into)

| Skill | How output is used |
|-------|-------------------|
| `ad-creative-brief` | Source headlines + descriptions for visual brief |
| `paid-ads-audit` | Baseline reference for RSA Ad Strength + CTR review |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

