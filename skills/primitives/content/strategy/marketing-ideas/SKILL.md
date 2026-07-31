---
name: marketing-ideas
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Structured brainstorm skill that produces a ranked list of campaign / content / experiment / lead-magnet ideas from a brief (audience + goal + constraints). Pairs with /thought-leadership for weekly ideation cadence — feeds the candidate queue that downstream content skills execute against. Triggered by "ideate", "brainstorm content", "marketing ideas", "campaign ideas", "what should we run next", "ideation session". NOT for executing the idea — hand off to /thought-leadership, /aeo-content, /linkedin-content, /lead-magnets, /webinar-brief downstream.
goal: Surface ranked candidate ideas (campaign / content / experiment / lead-magnet) from a structured brief.
outcome: Produces (1) brief restatement, (2) 8–12 candidate ideas across 4 modes, (3) ranking by audience-pain-match × proof-asset-availability × competitive-whitespace, (4) recommended next-3 with downstream skill handoffs.
primitive: content
sub_primitive: strategy
ontology_type: content-strategy
review_gate: 1
inputs:
  required: []
  recommended:
  - icp-research
  - positioning
  - content-strategy
  - expert-pov
- type: content-strategy
  feeds_into:
  - thought-leadership
  - aeo-content
  - linkedin-content-guide
depends_on: []
- thought-leadership
- aeo-content
- linkedin-content-guide
- webinar-brief
owned_by_agent: content
mcps_used:
- exa
- gdrive
triggers:
  slash_commands:
  - /marketing-ideas
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /marketing-ideas — structured ideation upstream of content

Produce a ranked list of marketing ideas from a brief. Sits *upstream* of execution skills — `/thought-leadership` writes the piece; this skill surfaces *which* topic to write.

---

## When to invoke

- Weekly Genesys ideation cadence — before the content calendar push.
- Client kickoff — surface candidate plays before committing to a content plan.
- Stuck moment — campaign / quarter calendar empty, need 8–12 starter ideas.
- Reactive moment — competitor moved, new tool surfaced, signal from sales — generate ideas to address.

---

## Workflow

### Step 1 — Brief intake

Capture in order:
- **Audience**: ICP segment or persona (e.g., "GTM Engineers at 50–500 person B2B SaaS").
- **Goal**: pipeline / brand / activation / retention / category-building.
- **Constraints**: budget, team capacity, deadline, voice-of-customer evidence available, brand voice rules.
- **Context**: existing content in the cluster (so we don't duplicate); recent client wins / losses (so we feed proof).

If any field is unclear, ask once — don't generate against ambiguous briefs.

### Step 2 — Generate across 4 modes (2–3 ideas per mode)

| Mode | Examples |
|---|---|
| **Campaign** (multi-asset, multi-week arc) | Launch series, narrative-driven nurture, product-led contest |
| **Content piece** (single asset) | Thought-leadership post, AEO article, comparison page, podcast episode |
| **Experiment** (test a hypothesis) | New CTA on landing page, signup flow A/B, pricing test |
| **Lead magnet** (gated asset for capture) | Calculator, template, benchmark report, framework |

Aim for 8–12 total ideas. Quantity-then-quality — pull more than you'll keep so ranking has options.

### Step 3 — Rank by 3-factor scoring

Score each on:

| Factor | Weight | Question |
|---|---|---|
| Audience pain match | 40% | Does this directly address a top-3 pain in the ICP? |
| Proof asset availability | 30% | Do we have customer evidence / data / story to back this credibly? |
| Competitive whitespace | 30% | Is the angle non-obvious — i.e., not the top-10 result for the query? |

Total / 100. Top 3 land in the recommended queue.

### Step 4 — Recommended next-3 with downstream handoffs

For each of the top 3:
- Restate the idea in one sentence.
- Name the downstream skill (`/thought-leadership` / `/aeo-content` / `/linkedin-content` / `/lead-magnets` / `/webinar-brief`).
- Note the brief the downstream skill will need (target keyword, hook, proof asset, format).

---

## {Client / Genesys} ideation — {date}

### Brief
- Audience:...
- Goal:...
- Constraints:...
- Context:...

### Candidate ideas (8–12)
| # | Mode | Idea (1 sentence) | Pain match (0-40) | Proof (0-30) | Whitespace (0-30) | Total |
|---|---|---|---|---|---|---|
| 1 | Campaign |... | 35 | 25 | 25 | 85 |
| 2 | Content |... | 30 | 30 | 20 | 80 |
|... |

### Recommended next-3
1. **{Idea}** — handoff to `/thought-leadership` with brief: {target keyword, hook, proof asset, format}.
2. **{Idea}** — handoff to `/aeo-content` with brief:...
3. **{Idea}** — handoff to `/lead-magnets` with brief:...

### Backlog (rank 4–8)
-...
```

---

## Anti-patterns

- ❌ Generate ideas without a brief. Output reads generic.
- ❌ Skip the ranking step — "here are 12 ideas, pick one" pushes the work back to the user.
- ❌ Optimize for whitespace alone (everything contrarian). Some obvious-angle posts are obvious because the audience needs them.
- ❌ Recommend an idea we have no proof asset for. Sounds smart, fails on execution.
- ❌ Generate without naming downstream handoffs. The idea dies in a doc.

---

## Integration with other skills

- **Upstream:** `/icp-research` + `/positioning` + `/content-strategy` + `/expert-pov` provide brief inputs.
- **Downstream:** Top-3 hand off to `/thought-leadership`, `/aeo-content`, `/linkedin-content`, `/lead-magnets`, `/webinar-brief`.
- **Cadence:** weekly Genesys ideation runs; ad-hoc client kickoff or quarterly refresh.

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/marketing-ideas/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/marketing-ideas/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice with explicit downstream-skill handoffs.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

