---
name: product-launch
version: '2.1'
last_updated: 2026-05-11
author: genesys-growth
description: Plans cross-functional product launches with timeline, channel mix, asset checklist, and team coordination across
  marketing, sales, and product. Produces launch brief, deployment calendar, and post-launch measurement plan. Triggers on
  "product launch", "feature release", "launch strategy", "launch plan", "go-to-market launch", or "release coordination".
  Requires positioning and product-messaging as upstream inputs.
goal: Plans cross-functional product launches with timeline, channel mix, asset checklist, and team coordination across marketing,
  sales, and product.
outcome: Plans cross-functional product launches with timeline, channel mix, asset checklist, and team coordination across
  marketing, sales, and product. Produces launch brief, deployment calendar, and post-launch measurement plan. Triggers on
  "product launch", "feature release", "launch strategy",...
primitive: product-marketing
sub_primitive: strategy
ontology_type: launch-plan
review_gate: 2
inputs:
  required:
  - product-messaging
  - positioning
  recommended: []
outputs:
- type: launch-plan
  feeds_into:
  - website-copy
  - email-nurture
  - webinar-brief
  - linkedin-weekly-content
  - sales-deck
  - storytelling
depends_on:
- product-messaging
- positioning
feeds_into:
- website-copy
- email-nurture
- webinar-brief
- linkedin-weekly-content
- sales-deck
- storytelling
owned_by_agent: growth
mcps_used: []
push_targets:
- gdrive
- notion
triggers:
  slash_commands:
  - /product-launch
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Product launch

Architect and execute B2B SaaS product launches that drive sustained pipeline. Launches are built on the tactics around the event — not the channel checklist. Pick 5–8 tactics from the 16-tactic library; derive assets from the chosen tactics; orchestrate across pre-launch, launch day, and post-launch.

---

## Claude Code triggers

**Invoke when user says:**
- "Product launch for [feature/product]"
- "Feature launch plan"
- "Launch strategy for [company]"
- "GTM launch plan"
- "New feature announcement"
- "Create launch assets"
- "Launch timeline for [feature]"
- "Launch checklist"
- "Plan a launch for [feature]"
- "Launch playbook"

**Do NOT invoke when:**
- User wants landing page copy only → use `website-copy`
- User wants product messaging only → use `product-messaging`
- User wants LinkedIn content only → use `linkedin-weekly-content` or `linkedin-content-guide`
- User wants email copy only → answer directly or use `email-nurture`
- User wants live event production only → use `webinar-brief`
- User wants a single launch tactic in isolation → go directly to its template-spec in `references/` rather than running the full skill

---

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Product feature brief** | What's launching, target release date | User provides |
| **Product messaging** | Capabilities, benefits, differentiators | `product-messaging` skill or existing |
| **ICP research** | Target personas, pain points, proof points | `icp-behavioural` skill or existing |

### Optional (improve quality)

| Input | How it helps |
|-------|--------------|
| TOV guidelines | Brand voice for all copy assets |
| Competitor launches | Differentiation framing |
| Sales objections | FAQ and enablement content |
| Customer feedback | Proof points and testimonials |
| Launch date | Timeline anchoring |

### Validation

Before proceeding, verify the feature brief includes name, category, description, target personas, key capabilities; product messaging available or generated; ICP research available or generated; launch date confirmed (or flexible window).

If inputs are missing: offer to run `product-messaging` and/or `icp-behavioural` first, or ask the user to provide the brief.

---

## Core frameworks

### Launch philosophy

The old launch playbook is dead. Most marketers launch by writing "we're excited to announce" on LinkedIn, ticking off a channel checklist (Product Hunt / Hacker News / Reddit / LinkedIn / X), and wondering why their CEO asks "wait, did we even launch?" the following Monday.

A great launch is built on the **tactics around** the launch — not the channel checklist. The skill encodes 16 tactics in `references/tactic-library.md`. Strategy phase picks 5–8 of them. Development phase derives assets **from the chosen tactics**, not from a default 18-asset list.

The order matters: tactics first, then assets. Reverse this and you're back to the channel checklist mentality.

A launch built this way:

- Pre-builds audience before launch day (waitlist, teaser, ambassador, partner)
- Stages a real moment (live event, drop, named version)
- Sustains attention for 2+ weeks post-launch (recap cadence)
- Compounds across cycles (60-day relaunch every quarter)

**T-0 is the midpoint, not the destination. And the channel checklist is not the strategy.**

### Three-phase architecture

| Phase | Purpose | Duration | Deliverables |
|-------|---------|----------|--------------|
| **Strategy** | Pick 5–8 tactics; define narrative, objectives, positioning | T-14 to T-10 | Strategy brief with selected tactics, narrative angle, success metrics |
| **Development** | Produce assets derived from chosen tactics | T-10 to T-1 | Asset list scoped to tactics (not a default 18-asset checklist) |
| **Deployment** | Orchestrate timeline and amplification | T-14 to T+14 | Timeline, coordination playbook |

### Launch tiers

| Tier | Description | Tactic count | Asset scope |
|------|-------------|--------------|-------------|
| **Major** | New product, category entry, platform shift | 7–8 tactics | Live event + waitlist + teaser + ambassadors + partner + recap + relaunch + paid |
| **Significant** | Major feature, integration, pricing change | 5–7 tactics | Subset above; selective paid |
| **Standard** | Feature improvement, capability expansion | 4–6 tactics | Channel-specific copy + recap + founder personal posts + 1–2 others |
| **Minor** | Bug fix, UX improvement | 3–4 tactics | Channel-specific copy + recap + grandfather (if applicable) |

### Anything counts as a launch

The 16-tactic library doesn't only apply to product launches. The same machinery runs for:

- **Stealth exits** — coming out of stealth is a launch
- **Feature drops** — significant feature releases
- **Hiring announcements** — exec hires, team scale-ups
- **Pricing changes** — new tiers, plan refactors (always pair with grandfather policy)
- **Big blog posts** — flagship content, research releases
- **Funding announcements** — Series A/B/C, secondary rounds
- **Partnership reveals** — when a partner co-launch IS the launch
- **Geographic expansion** — entering a new market

If you've ever shipped something that got crickets, this skill fixes it. The trigger isn't "is this a product?" — it's "are we asking the audience to pay attention?" If yes, run the playbook.

### Seasonal alignment

Every launch happens in a cultural context. Check for adjacent cultural moments (±14 days from launch), score alignment fit (Strong/Medium/Weak/Negative), choose strategy (ride the wave, counter-program, ignore, or avoid), and adapt messaging (hooks, imagery, CTAs). See `references/seasonal-calendar.md`.

---

## Tactic library — Strategy starts here

Before anything else in the Strategy phase, pick 5–8 tactics from `references/tactic-library.md`. The 16-tactic menu covers waitlist, ambassador army, partner co-launch, channel-specific copy, founder personal posts, gamified drops, filtered giveaways, weird swag, audience-as-detective narratives, named versions, public roadmap voting, grandfather policy, teaser videos, live events, recap cadences, and 60-day relaunches.

Selection criteria: launch tier, audience size, ICP shape, resource constraints, existing community signal. The chosen tactics drive the Development phase asset list — **not** a default 18-asset checklist.

Three battle-tested stacks live in `tactic-library.md` as starting points:

- **Clicky stack** — Waitlist → Teaser → Live event → Recap. Best for momentum into a live event.
- **Long-tail stack** — Ambassador army → Partner co-launch → 60-day relaunch. Best for cold audiences and limited founder time.
- **Drama stack** — Narrative campaign → Named version → Recap. Best for personality-led brands.

Most launches won't match a stack cleanly — combine across stacks. The 5–8 selection rule is the discipline.

---

## Process

The launch runs in three phases. Read `references/process.md` for the full step-by-step (5 strategy steps, 8 development steps, 4 deployment steps, plus per-phase checkpoints and the process flowchart).

Phase summary:

1. **Strategy (T-14 to T-10)** — feature brief, **5–8 tactics selected from `tactic-library.md`**, narrative angle, business objectives, kick-off agenda
2. **Development (T-10 to T-1)** — derive assets from chosen tactics (not from a default 18-asset checklist), produce each via its template-spec
3. **Deployment (T-14 to T+14)** — pre-launch / launch-day / post-launch timelines + coordination playbook with RACI

---

## Anti-hallucination guardrails

1. **Ground all claims in inputs.** Feature benefits must come from product brief or messaging.
2. **No invented metrics.** Use provided proof points or mark as `[PLACEHOLDER: metric]`.
3. **Quote verbatim.** Customer quotes from ICP research only.
4. **Mark placeholders clearly.** Use `[PLACEHOLDER: description]` for unconfirmed details.
5. **Cite sources.** Link each asset to its input source.

---

## Output

Produce a single launch-package markdown file. Template + iteration prompts library: `references/output-format.md`.

Pre-delivery quality checklist + worked example + anti-examples: `references/quality.md`.

Auto-update protocol (feedback signals, pattern detection, skill-update template): `references/auto-update.md`.

---

## Reference files

| File | Purpose |
|------|---------|
| `references/tactic-library.md` | **The 16-tactic menu. Strategy phase picks 5–8 of these.** |
| `references/process.md` | Full step-by-step across 3 phases + flowchart |
| `references/output-format.md` | Launch package template + iteration prompts |
| `references/quality.md` | Pre-delivery checklist + worked example + anti-examples |
| `references/auto-update.md` | Feedback signal detection + pattern rules |
| `references/strategy-template.md` | Complete strategy brief structure |
| `references/seasonal-calendar.md` | Cultural moments and alignment |
| `references/landing-page-spec.md` | Landing page requirements |
| `references/channel-copy-spec.md` | Per-platform copy (LinkedIn / X / Reddit / HN / PH / others) — was `linkedin-series-spec.md` |
| `references/email-announcement-spec.md` | Email templates |
| `references/sales-enablement-spec.md` | Enablement templates |
| `references/coordination-playbook.md` | RACI matrix and protocols |
| `references/blog-post-spec.md` | Blog post requirements |
| `references/founder-video-spec.md` | Founder video script + founder personal post + thought-leader ads |
| `references/waitlist-sequence-spec.md` | Tactic 1 — 6-email waitlist sequence + landing page |
| `references/ambassador-program-spec.md` | Tactic 2 — micro-influencer program rules + application form + payouts |
| `references/partner-colaunch-spec.md` | Tactic 3 — partner brief + joint announcement copy + decision tree |
| `references/gamification-spec.md` | Tactic 6 — drip-access codes + wave structure |
| `references/giveaway-spec.md` | Tactic 7 — team challenges + post-win amplification |
| `references/swag-spec.md` | Tactic 8 — weird swag framework + vendor brief |
| `references/narrative-campaign-spec.md` | Tactic 9 — multi-chapter audience-as-detective campaigns |
| `references/named-version-spec.md` | Tactic 10 — naming theme + lock-next-5 protocol |
| `references/grandfather-policy-spec.md` | Tactic 12 — pricing/access grandfather policy + amplification |
| `references/teaser-video-spec.md` | Tactic 13 — pre-launch teaser script + platform mix |
| `references/live-event-spec.md` | Tactic 14 — RSVP + 60-min event structure + day-of checklist |
| `references/recap-cadence-spec.md` | Tactic 15 — 8-format × 7-day post-launch squeeze |
| `references/relaunch-calendar-spec.md` | Tactic 16 — 9-angle 60-day relaunch calendar |
| `examples/` | Worked example launches |

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **product-messaging** | Required input | Capabilities, benefits, differentiators for all copy |
| **icp-behavioural** | Required input | Persona targeting, pain points, proof points |
| **tov-guidelines** | Optional input | Voice and tone for all copy assets |
| **website-copy** | Asset generation | Landing page development (waitlist + launch page) |
| **sales-deck** / **battlecards** / **one-pager** | Asset generation | Sales-enablement assets at launch |
| **linkedin-weekly-content** | Asset generation | Pre-launch / launch / post-launch LinkedIn series (expanded via `channel-copy-spec.md`) |
| **email-nurture** | Asset generation | 6-email waitlist sequence delivery (tactic 1) |
| **webinar-brief** | Asset generation | Live event production mechanics (tactic 14) |
| **storytelling** | Asset generation | Multi-chapter narrative campaigns (tactic 9) |
| **linkedin-content-guide-founders** | Asset generation | Founder personal post mechanics (tactic 5) |
| **expert-pov** | Optional input | Founder voice extraction for waitlist tease emails |
| **pricing-strategy** | Adjacent | Underlying pricing decision; grandfather policy layers on top (tactic 12) |

---

## MCP data integration

**Level:** 2 — PM Execution (inherits strategy, operational pulls)

**Inherits from:** product-messaging

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Slack** | Launch coordination threads | `slack_search_public` | Always |

### Fallback (no MCP)

- Use product-messaging output directly
- Manual launch coordination via shared docs
- User-provided timeline and stakeholder info

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

