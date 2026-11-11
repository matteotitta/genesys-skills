---
name: product-launch
description: Plans a product launch from a brief: launch tier, 5-8 launch tactics, narrative angle, objectives, then the assets and a T-14 to T+30 timeline built from those tactics. Use when asked to plan a launch, a launch strategy or a go-to-market for a feature.
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

**Do NOT invoke when** the user wants only landing page copy, product messaging, LinkedIn content, email copy, or live event production.

---

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Product feature brief** | What's launching, target release date | User provides |
| **Product messaging** | Capabilities, benefits, differentiators | User provides or existing doc |
| **ICP research** | Target personas, pain points, proof points | User provides or existing doc |

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

If inputs are missing: ask the user for the brief, the messaging and the target personas, or draft them from the product page and confirm before going further.

---

## Core frameworks

### Launch philosophy

The old launch playbook is dead. Most marketers launch by writing "we're excited to announce" on LinkedIn, ticking off a channel checklist (Product Hunt / Hacker News / Reddit / LinkedIn / X), and wondering why their CEO asks "wait, did we even launch?" the following Monday.

A great launch is built on the **tactics around** the launch — not the channel checklist. The skill encodes 16 tactics in the premium reference. Strategy phase picks 5–8 of them. Development phase derives assets **from the chosen tactics**, not from a default 18-asset list.

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

Every launch happens in a cultural context. Check for adjacent cultural moments (±14 days from launch), score alignment fit (Strong/Medium/Weak/Negative), choose strategy (ride the wave, counter-program, ignore, or avoid), and adapt messaging (hooks, imagery, CTAs). See the premium reference.

---

## Tactic library — Strategy starts here

Before anything else in the Strategy phase, pick 5–8 tactics from the premium reference. The 16-tactic menu covers waitlist, ambassador army, partner co-launch, channel-specific copy, founder personal posts, gamified drops, filtered giveaways, weird swag, audience-as-detective narratives, named versions, public roadmap voting, grandfather policy, teaser videos, live events, recap cadences, and 60-day relaunches.

Selection criteria: launch tier, audience size, ICP shape, resource constraints, existing community signal. The chosen tactics drive the Development phase asset list — **not** a default 18-asset checklist.

Three battle-tested stacks live in the premium reference as starting points:

- **Clicky stack** — Waitlist → Teaser → Live event → Recap. Best for momentum into a live event.
- **Long-tail stack** — Ambassador army → Partner co-launch → 60-day relaunch. Best for cold audiences and limited founder time.
- **Drama stack** — Narrative campaign → Named version → Recap. Best for personality-led brands.

Most launches won't match a stack cleanly — combine across stacks. The 5–8 selection rule is the discipline.

---

## Process

The launch runs in three phases. Read the premium reference for the full step-by-step (5 strategy steps, 8 development steps, 4 deployment steps, plus per-phase checkpoints and the process flowchart).

Phase summary:

1. **Strategy (T-14 to T-10)** — feature brief, **5–8 tactics selected from the tactic menu**, narrative angle, business objectives, kick-off agenda
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
