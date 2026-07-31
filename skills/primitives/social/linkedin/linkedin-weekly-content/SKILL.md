---
name: linkedin-weekly-content
version: '1.0'
last_updated: 2026-03-29
author: genesys-growth
description: 'Runs the weekly LinkedIn content generation job for Matteo Tittarelli / Genesys Growth. Produces 4 posts (Story,
  Expert, Sales, Rotated) plus 2 visual briefs (infographic, carousel), appends output to a persistent Google Doc, and sends
  a Slack notification. Triggers: "weekly linkedin", "generate this week''s posts", "linkedin weekly content", "linkedin batch".
  Depends on linkedin-content-guide; orchestrates linkedin-expert-posts, linkedin-sales-posts, linkedin-personal-posts, linkedin-infographics,
  and linkedin-algo-audit. Triggered automatically every Friday via /schedule.'
goal: Runs the weekly LinkedIn content generation job for Matteo Tittarelli / Genesys Growth.
outcome: 'Runs the weekly LinkedIn content generation job for Matteo Tittarelli / Genesys Growth. Produces 4 posts (Story,
  Expert, Sales, Rotated) plus 2 visual briefs (infographic, carousel), appends output to a persistent Google Doc, and sends
  a Slack notification. Triggers: "weekly linkedin",...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 2
inputs:
  required:
  - linkedin-content-guide
  recommended:
  - linkedin-hooks
  - linkedin-expert-posts
  - linkedin-sales-posts
  - linkedin-personal-posts
  - linkedin-infographics
  - linkedin-algo-audit
  - voice-reviewer
- type: linkedin-weekly-batch
  feeds_into:
  - gdrive-create
depends_on:
- linkedin-content-guide
- gdrive-create
owned_by_agent: content
mcps_used:
- slack
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

# LinkedIn Weekly Content

Generate a full week of LinkedIn content for Matteo Tittarelli / Genesys Growth. Produces 4 posts + 2 visual briefs, appends to a persistent Google Doc, and sends a Slack notification.

---

## Weekly Schedule

Voice-locked operational constants — these stay in body.

- Monday: Claude Skills newsletter (separate pipeline — no LinkedIn post)
- **Tuesday: Story post** (35% pillar — personal experiences, founder journey)
- **Wednesday: Expert post** (40% pillar — give away the playbook)
- **Thursday: Sales post** (25% pillar — case study storytelling, offer integration)
- **Friday: Rotated post** (cycles: Story → Expert → Sales, ISO week mod 3)
- Sunday: GTM Pulse newsletter (separate pipeline)

**Visual briefs (one of each per week):**
- 1x Infographic brief (paired with any post)
- 1x Carousel brief (paired with any post)

---

## Process

9-phase orchestration:

```
Phase 1: Load Context → Phase 2: Generate Hooks → Phase 3: Generate 4 Posts
                                                              ↓
Phase 6: Photo Rec ← Phase 5: Visual Briefs ← Phase 4: Algo Audit
       ↓
Phase 7: GDrive Append → Phase 8: Slack Notify → Phase 9: Update Rotation Tracker
```

Phase-by-phase detail (skill invocations, post lengths, archetype rotation logic, MCP detection, GDrive append script) in the premium reference.

---

## Quality Gates (Applied Automatically)

Voice-locked rules — these stay in body.

- **Anti-AI detection:** No "Here's the thing:", no false contrast reframes, no wrapped-bow endings, no generic praise
- **100 Posts Test:** Each post must feel authentic for 100 consecutive posts
- **Offer integration:** Even non-sales posts subtly showcase what Genesys does (per Matteo's voice rules)
- **Wordiness check:** Trim 15-20% from first draft (Matteo's tendency)
- **No "genuinely asking":** Stop using pseudo-engagement closings
- **Source integrity:** No fabricated stories, metrics, or quotes — all from content banks

Full per-post and per-batch checks in the premium reference.

---

## Scheduling

This skill is triggered weekly via Claude Code `/schedule`:

```
/schedule create "LinkedIn Weekly Content" --cron "0 8 * * 5" --prompt "Run /linkedin-weekly-content for the upcoming week"
```

**Cron:** Every Friday at 08:00 UTC
**Why Friday:** Full weekend to review. Monday = newsletter. Tuesday's story post = first LinkedIn post of the week. 4 days of buffer.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
