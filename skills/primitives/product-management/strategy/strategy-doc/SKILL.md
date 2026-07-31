---
name: strategy-doc
version: '1.0'
last_updated: 2026-05-05
author: genesys-growth
description: 'Produces a 5-part GSBS (Good Strategy Bad Strategy) product strategy document via guided interview: target problem, approach (guiding policy not features), who-for (one persona ideally), key metrics (SMART, anti-vanity), and 2-4 tracks. Anchors the agent-native PM operating loop with /product-pulse and /ship-learnings. Triggers: "product strategy", "strategy doc", "GSBS strategy", "what should we build", "strategy interview". Recommended upstream: company-context, icp-research, positioning. Feeds product-pulse + ship-learnings. NOT for positioning/messaging (use /positioning + /product-messaging) or feature specs (use external product-management:write-spec).'
goal: Produce a locked 5-part product strategy doc that anchors the strategy ↔ pulse ↔ ship feedback loop.
outcome: Produces a 5-part GSBS strategy doc — target problem, approach, who-for, key metrics, tracks — that downstream /product-pulse skill measures against and /ship-learnings feeds back into. Refreshes quarterly.
primitive: product-management
sub_primitive: strategy
ontology_type: product-strategy
review_gate: 3
inputs:
  required: []
  recommended:
  - company-context
  - icp-research
  - positioning
  - win-loss-analysis
- type: product-strategy
  feeds_into:
  - product-pulse
  - ship-learnings
depends_on: []
- product-pulse
- ship-learnings
owned_by_agent: product-manager
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /strategy-doc
  natural_language:
  - "product strategy"
  - "strategy doc"
  - "GSBS strategy"
  - "what should we build"
  - "strategy interview"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Product strategy doc — 5-part GSBS structure

Produce a locked product strategy document that anchors the agent-native PM operating loop. Adapted from `/ce-strategy` in [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT). Based on Marcus Moretti's AI PM Guide (Every.to) and Richard Rumelt's *Good Strategy Bad Strategy*.

This is **not** a spec or PRD. Strategy describes the **guiding policy** (what we'll do and why); requirements describe the **artifacts** (what we'll build). Keep them separate.

## When to run

Invoke when the user says:
- "Run product strategy for [Genesys ship / client product]"
- "What's our strategy for [product]?"
- "Time for the quarterly strategy refresh"
- "Run the strategy interview"

Do NOT invoke when:
- User wants positioning / category framing → `/positioning` (PMM-side, different artifact)
- User wants a feature spec / PRD → external `product-management:write-spec` plugin
- User wants the daily product pulse → `/product-pulse` (downstream of this skill)
- User wants post-ship learnings → `/ship-learnings`

Workflow sequences:
- New product: `company-context → icp-research → positioning → strategy-doc → product-pulse → ship-learnings`
- Refresh: `ship-learnings (last cycle) + product-pulse (last cycle) → strategy-doc (refreshed)`

## Inputs

**Required:**
- Product name + 1-line description
- Stakeholder for review (founder / PM / ops lead)

**Recommended (improve quality):**
- `company-context` — firmographics, traction, qualification context
- `icp-research` / `icp-behavioural` — sharpens the "who-for" section
- `positioning` — gives anchors and differentiators (the "approach")
- `win-loss-analysis` — what users actually pay for vs. ignore
- Latest `product-pulse` and `ship-learnings` from prior cycle (for refresh runs)

**If inputs missing:** Run a 5-section guided interview anyway. Flag data gaps. Recommend running upstream skills before lock.

## The 5 parts (GSBS structure)

The doc has exactly 5 sections. Don't add more. Don't merge them.

### 1. Target problem

A recurring, expensive problem worth solving. Not "better tools for X." Specific. Cite evidence (user quotes, win-loss patterns, support tickets).

**Anti-pattern:** "Help users [verb] better." Vague. Reject.

### 2. Approach (guiding policy, not features)

How we'll solve the target problem. The **policy** that guides every feature decision — not the features themselves. One-paragraph statement that someone could apply to a feature decision without seeing this doc.

**Anti-pattern:** A list of features ("we'll build X, Y, Z"). Reject — that's a roadmap.

### 3. Who-for (one persona, ideally)

The persona we focus on first. Per *Crossing the Chasm*: "ideally one." If two, justify why and which leads. If three or more, reject — the strategy isn't focused enough.

**Anti-pattern:** "PMs, marketers, and founders." Reject — that's an audience, not a persona.

### 4. Key metrics (SMART, anti-vanity)

2-4 metrics. Each must:
- Be **Specific** (named, not "engagement")
- Be **Measurable** (have a data source — name it)
- Be **Achievable** (target value, not aspirational)
- Be **Relevant** (ties back to target problem)
- Be **Time-bound** (deadline)

Apply the K2 anti-vanity-metrics rule: page views, impressions, MAU without conversion are **rejected**. Per Moretti: "Pick the metrics that undeniably show people are getting value."

**Anti-pattern:** "Increase engagement." Reject. Specify *what* engagement, *measured how*, *to what target*, *by when*.

### 5. Tracks (2-4 core capabilities)

The 2-4 capabilities the team will build to deliver the approach. Not features — capability *areas* (e.g., "fast onboarding," "AI-native search," "collaborative workflows").

If you have >4, you're not focused. Cut. If you have <2, the strategy is probably a single feature dressed as strategy.

## Steps

1. **Phase 1 — Pre-interview load.** Read recommended inputs (`company-context`, `icp-research`, `positioning`, latest `ship-learnings`). Surface data gaps before starting the interview.
2. **Phase 2 — Guided interview.** Walk the user through 5 questions, one per section. Push back when answers are vague (the anti-patterns above are common). The interview is the work — the doc is the artifact.
3. **Phase 3 — Draft.** Compose the 5-section doc. Apply length discipline: each section ≤ 250 words, total ≤ 1500 words.
4. **Phase 4 — Self-roast.** Run the checks below. Surface any failures before review.
5. **Phase 5 — Review gate (Level 3).** Stakeholder review. Iterate until approved.
6. **Phase 6 — Lock.** Set `status: locked`, `locked_by`, `locked_date`, `lock_version: 1`. Doc is now the canonical strategy reference for the cycle.
7. **Phase 7 — Schedule next refresh.** Schedule a quarterly refresh via the `/schedule` skill or Trigger.dev cron. Default: 90 days.

## Self-roast (run before review)

- [ ] Target problem cites specific evidence (user quote, win-loss pattern, ticket count) — not generic
- [ ] Approach is a *policy*, not a feature list
- [ ] Who-for is **one** persona (or 2 with justification); not an audience
- [ ] Each metric passes SMART; no vanity metrics (page views / impressions / MAU without conversion)
- [ ] Tracks count 2-4; each is a capability area, not a feature
- [ ] Total word count ≤ 1500 (single-document discipline; if longer, the strategy is unfocused)
- [ ] No requirements / specs leaked in (K6: strategy ≠ PRD)
- [ ] Refresh date scheduled

# {Product name} — Product strategy

**Locked:** {date} · **Stakeholder:** {name} · **Refresh:** {next date}

## 1. Target problem
{specific, evidence-backed statement}

## 2. Approach
{guiding policy paragraph}

## 3. Who-for
{persona — ideally one}

## 4. Key metrics
| Metric | Source | Target | By when |
|---|---|---|---|
|... |... |... |... |

## 5. Tracks
1. **{Track 1}** — {capability description}
2. **{Track 2}** —...
```

## Composition rule reference

This skill is the anchor of the **PM closed loop** (P3 in `.claude/discovery/0526-every-ai-pm-guide-steal-analysis.md`). See [.claude/rules/pm-loop.md](../../../../../rules/pm-loop.md) for how `strategy-doc` ↔ `product-pulse` ↔ `ship-learnings` compose.

## Attribution

Adapted from [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT). Source pattern: `/ce-strategy`. Framework basis: Richard Rumelt, *Good Strategy Bad Strategy*. Persona constraint basis: Geoffrey Moore, *Crossing the Chasm*.

