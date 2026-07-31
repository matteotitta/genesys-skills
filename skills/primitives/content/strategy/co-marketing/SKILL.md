---
name: co-marketing
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Finds non-competing co-marketing partners via audience-overlap analysis and 6-factor partner scoring (audience fit, size, brand alignment, engagement quality, reciprocity, execution ease). Designs joint campaigns (content swap, webinar, integration, community activation) with lead-sharing structure and execution timeline. Triggered by "co-marketing", "partner campaigns", "joint webinar", "find partners", "partnership marketing". NOT for sales partnerships or reseller channels — different dynamic.
goal: Identify non-competing partners with shared audiences and design joint campaigns that reach beyond solo organic reach.
outcome: Produces (1) scored partner shortlist, (2) 2–3 campaign ideas with execution timelines, (3) lead-sharing structure + asset commitments, (4) outreach templates for partner contact.
primitive: content
sub_primitive: strategy
ontology_type: content-strategy
review_gate: 2
inputs:
  required: []
  recommended:
  - icp-research
  - positioning
  - company-context
- type: content-strategy
  feeds_into:
  - content-strategy
depends_on: []
- content-strategy
- product-launch
owned_by_agent: growth
mcps_used:
- exa
- firecrawl
- gdrive
triggers:
  slash_commands:
  - /co-marketing
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /co-marketing — partner finding + joint campaign design

Find non-competing companies that share your audience and design joint campaigns. The leverage: when both sides promote, distribution roughly doubles for both — at half the asset cost.

---

## When to invoke

- Distribution is organic-only and partner channel is untapped.
- A product launch needs amplified reach (pair with `/directory-submissions` + `/product-launch`).
- Genesys-internal cross-promotion with adjacent tools (Clay, Apollo, Smartlead, Instantly).
- Client needs joint plays with integration partners or vertical-adjacent SaaS.

---

## Step 1 — Audience overlap analysis

The core test: **does the partner serve our same buyer persona but solve a different problem?** Same audience, non-competing solution.

Validate via:
- Account-overlap tools (Crossbeam, Reveal) — exact-match overlap data.
- LinkedIn job-title overlap (export both companies' followers, intersect).
- Newsletter sub-audience overlap (if both publish).
- Conference / event co-attendance.

**Sharp rule:** partners who share <30% audience are noise; >70% audience overlap with no competition is the gold zone.

---

## Step 2 — 6-factor partner scoring

Score each candidate on 5 each:

| Factor | Question | Weight |
|---|---|---|
| Audience fit | Same ICP, non-competing? | High |
| Size | Audience reach roughly equivalent (within 3× either direction)? | High — asymmetric partnerships are short-lived |
| Brand alignment | Voice, professionalism, ethics compatible? | Medium |
| Engagement quality | Their audience actively responds (LinkedIn comments, email open rates) — not just numbers | High |
| Reciprocity history | Have they done co-marketing before? Reliable? | Medium |
| Execution ease | Geography, timezone, calendar friction | Medium |

Total ≥ 22/30 = green-light. 18–21 = yellow (start with low-effort format). <18 = pass.

---

## Step 3 — Campaign type selection

Order by effort (low → high) and depth (light → heavy):

| Format | Effort | Depth | Best for |
|---|---|---|---|
| Social swap (mutual share / quote post) | Very low | Light | First partnership; brand-warm-up |
| Newsletter cross-promo (sponsored slot) | Low | Light | Audience introduction |
| Joint blog post / co-authored content | Medium | Medium | SEO + thought leadership |
| Joint webinar / panel | Medium-high | Medium | Lead capture + relationship |
| Integration play (real product integration) | High | Deep | Long-term partnership |
| Joint research report / data study | High | Deep | PR + earned media |
| Joint conference / community activation | Very high | Very deep | Established partnership |

**Sharp rule:** start with the lowest-effort format. Prove reciprocity, then escalate. Skipping to a research report on partnership #1 is overcommitting.

---

## Step 4 — Structure the partnership

Document upfront, in writing:

- **Lead ownership:** which side keeps which leads? Default split: webinar attendees split 50/50; native-channel sign-ups stay with the channel owner.
- **Promotion commitments:** each side commits to N social posts, M newsletter inclusions, K direct emails.
- **Asset creation responsibility:** who builds the deck, who hosts, who edits the recording.
- **Success metrics:** registrations, attendance rate, post-event email conversion, qualified leads.
- **Timeline:** kickoff → promo start → event → post-event nurture handoff.

Without this written, the partnership stalls within 2 weeks.

---

## Step 5 — Outreach template

```
Subject: {your_company} × {partner_company} — quick co-marketing idea

Hi {first_name},

Noticed we both serve {shared audience} — {partner's customer segment} folks who care about {shared concern}.

We just launched {your relevant artifact / content} and saw it pulled in {evidence of audience fit, e.g., "200 sign-ups from {their audience segment} in week 1"}.

I'm thinking a {specific low-effort format, e.g., "joint webinar on {topic}"} could land well with both sides. Rough shape:
- You bring {their unique angle}
- We bring {our unique angle}
- Co-promo to both lists
- Split leads 50/50

Quick call next week to scope?

— {your name}
```

**Sharp rule:** specific format + specific value > generic "let's partner". Generic asks convert at <5%; specific asks convert at 25%+.

---

## Worked example — Genesys-internal first

**Use case:** joint webinar with Clay on "Cold outreach in 2026 — agent stack walkthrough".

- **Audience overlap:** Clay's audience = GTM engineers (~85% overlap with Genesys's audience). Non-competing — Clay enriches, we structure.
- **Partner score:** Audience 5 + Size 4 + Brand 5 + Engagement 5 + Reciprocity 4 + Execution 4 = 27/30. Green.
- **Format:** joint webinar (medium effort, medium depth — appropriate for partnership #1).
- **Structure:** Clay brings the enrichment workflow demo; Genesys brings the skill-orchestrator end-to-end; co-promo to both lists; 50/50 lead split; Clay hosts; Genesys edits the recording.
- **Timeline:** Week 1 kickoff → Week 3–4 promotion → Week 5 webinar → Week 6 nurture.

---

## Anti-patterns

- ❌ Partner with a competitor under the guise of co-marketing. Distribution gain ≠ trust loss.
- ❌ Skip the written structure. Lead-split disputes kill the relationship.
- ❌ Start with a research report. Too high commitment for partnership #1.
- ❌ Asymmetric partnerships (size delta > 3×). Smaller side gets more value; bigger side disengages.
- ❌ Generic "let's partner" outreach. Convert at <5%.

---

## Integration with other skills

- **Upstream:** `/icp-research` defines the shared audience; `/positioning` clarifies non-competition story.
- **Downstream:** `/content-strategy` integrates partner campaigns into the calendar; `/lifecycle-marketing` runs the post-event nurture.
- **Companion:** `/product-launch` may coordinate partner amplification at launch moment.

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/co-marketing/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/co-marketing/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice. Lane B: Genesys-internal partnerships first.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

