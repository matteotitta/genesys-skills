---
name: hype-man
version: '1.0'
last_updated: 2026-03-09
author: genesys-growth
description: 'Designs "hype man" LinkedIn brand awareness programs where a non-founder social persona builds brand through
  humor, personality, and algorithmic reach. Produces a program brief covering persona design, content pillars, posting cadence,
  engagement playbook, and success metrics. Triggers: "hype man", "hype monkey", "algorithmic brand play", "hire someone to
  post on LinkedIn", "brand character", "second voice on LinkedIn". Feeds into linkedin-content and linkedin-comment for execution.
  NOT for founder-led LinkedIn — use linkedin-content or linkedin-content-guide instead.'
goal: Designs "hype man" LinkedIn brand awareness programs where a non-founder social persona builds brand through humor,
  personality, and algorithmic reach.
outcome: 'Designs "hype man" LinkedIn brand awareness programs where a non-founder social persona builds brand through humor,
  personality, and algorithmic reach. Produces a program brief covering persona design, content pillars, posting cadence,
  engagement playbook, and success metrics. Triggers: "hype...'
primitive: social
ontology_type: thought-leadership
review_gate: 3
inputs:
  required: []
  recommended:
  - icp-behavioural
  - tov-guidelines
  - company-context
  - competitor-research
  - positioning
  - product-messaging
- type: hype-man-program-brief
  feeds_into:
  - linkedin-weekly-content
  - linkedin-comment
  - linkedin-social-selling
depends_on: []
- linkedin-comment
- linkedin-weekly-content
- linkedin-social-selling
owned_by_agent: content
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /hype-man
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# Hype Man Program

Design a dedicated "hype man" LinkedIn program that builds brand awareness through personality-driven, non-product content and algorithmic amplification. Based on the Marketing Ideas playbook — one salary, zero ad spend, LinkedIn's algorithm does the distribution.

**Source:** [Marketing Ideas — Get yourself a "hype monkey"](https://www.marketingideas.com/p/get-yourself-a-hype-monkey)

For full process, flywheel diagram, humor calibration matrix, and real-world examples → the premium reference.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (program design doc is client-team review; rendered hype content is end-customer-facing — no sources either side), R3 (humor-tier content stays product-update-tone-aware), R9 (verb-led playbook section names).

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "hype man program for [client]"
- "hype monkey strategy"
- "brand awareness through personal posting"
- "hire someone to post on LinkedIn for us"
- "algorithmic brand play"
- "non-founder LinkedIn presence"
- "dedicated social media character"
- "LinkedIn brand ambassador program"

**Do NOT invoke when:**
- User wants a single LinkedIn post → Use `linkedin-content` skill
- User wants founder-led content → Use `founder-linkedin` skill
- User wants LinkedIn outreach/DMs → Use `social-selling` skill
- User wants LinkedIn comments strategy → Use `linkedin-comment` skill

---

## Input Requirements

### Client context (auto-loaded)

If working on a client project, the client CLAUDE.md is auto-loaded. Check for these sections and apply automatically — do not ask the user to re-specify what's already documented:

| Section | How it informs the program |
|---------|---------------------------|
| **ICP** | Connection targets, humor calibration |
| **Voice & Messaging** | Persona tone boundaries |
| **Competitor quick-ref** | Audiences to poach via connection flywheel |
| **Messaging framework** | Value props the hype man reinforces implicitly |
| **Positioning** | Market category the hype man builds awareness for |

### Required
| Input | Description | Source |
|-------|-------------|--------|
| **Client/company** | Who this program is for | User or client CLAUDE.md |
| **ICP** | Who the hype man targets | Client CLAUDE.md or `/icp-research` |

### Optional (improve quality)
| Input | How it helps |
|-------|--------------|
| TOV guidelines | Calibrates persona tone to brand voice |
| Competitor landscape | Identifies audiences for connection flywheel |
| Messaging framework | What the hype man implicitly reinforces |
| Positioning | Category awareness goals |
| Existing team members | Helps decide: existing employee vs hire vs actor |
| Budget constraints | Test with existing person vs hire |
| Event calendar | Feeds omnipresence planning |

### Validation checklist

Before proceeding, verify:
- [ ] Client/company identity is clear
- [ ] ICP is defined (job titles, industries, pain points)
- [ ] Brand voice boundaries are understood (TOV or conversation)

If inputs missing: check client CLAUDE.md first. If still missing, offer to run `/icp-research`, `/tov-guidelines`, `/company-context`.

---

## Core decisions

### Character type selector

| Option | When to choose | Risk profile |
|--------|---------------|--------------|
| **Real employee (loudest person)** | Already has personality + bandwidth in-house | Low cost; risk if they leave |
| **Contracted actor** | Want full character control + brand-safe casting | Higher cost; requires direction |
| **Fictional persona** | Need maximum creative freedom + identity flexibility | Brand-safe; works long-term |

### The "never say" list (universal)

- Product features
- Pricing
- Direct CTAs ("Book a demo")
- Customer logos as bragging
- Founder name-drops in promotional context

### Posting cadence

- **Minimum:** 5x/week
- **Target:** Daily
- **Time allocation:** 2-3 hours daily for content creation + engagement

### Connection flywheel volume

- 50-100 targeted connection requests per week from hype man profile
- Employee amplification: full team likes/comments daily, staggered

For full humor calibration matrix and real-world examples → the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent client ICP data.** Pull from client CLAUDE.md or ask user to provide.
2. **Never fabricate engagement metrics.** Use `[to be baselined]` for unknown starting points.
3. **Don't guess competitor audiences.** Use actual competitor research or flag as needing `/competitor-research`.
4. **Mark assumptions explicitly.** If inferring humor style without TOV data, say `[INFERRED: from ICP persona]`.
5. **No invented event calendars.** Use `[to be confirmed]` for omnipresence touchpoints.

---

## Process, Output, Quality

| Topic | Reference |
|-------|-----------|
| 5-phase process + flywheel diagram + humor matrix + real-world examples | the premium reference |
| Output template + iteration prompts + downstream handoff | the premium reference |
| Pre-delivery checklist + worked example + anti-examples + quality gate | the premium reference |
| Distilled Marketing Ideas article with full playbook | the premium reference |

---

## Integration with Other Skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **icp-behavioural** | Upstream | Defines targets + humor calibration |
| **tov-guidelines** | Upstream | Persona voice and tone boundaries |
| **company-context** | Upstream | Company positioning and product context |
| **competitor-research** | Upstream | Competitor audiences for flywheel |
| **positioning** | Upstream | Market category to reinforce |
| **product-messaging** | Upstream | What to reinforce implicitly |
| **linkedin-content** | Downstream | Generate posts for the persona |
| **linkedin-comment** | Downstream | Engagement plays for the hype man |
| **social-selling** | Downstream | Convert signals to pipeline |
| **founder-linkedin** | Sibling | Founder's brand alongside hype man |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

