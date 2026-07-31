---
name: vertical-messaging
version: '1.0'
last_updated: 2026-07-02
author: genesys-growth
description: Adapts a locked messaging library across segments using the buying trigger as the entry point. For each vertical/segment,
  extracts the trigger from VOC evidence, defines the buying lens and must-have outcome, assigns ONE leading messaging
  pillar, and writes an entry-point message — producing a per-segment routing map (trigger → lens → outcome → pillar →
  entry point). Triggers on "vertical messaging", "segment messaging", "adapt messaging for [segment/industry]", "messaging
  map", "what do we say to [vertical]". Requires product-messaging as upstream input; icp-research and win-loss sharpen
  triggers. Feeds into landing-page-copy, outreach-emails, abm-campaign, lifecycle-marketing. NOT for building the core
  messaging library (use product-messaging) or role-based personas (use icp-behavioural).
goal: Adapts a locked messaging library across segments using the buying trigger as the entry point, producing a per-segment
  routing map.
outcome: Adapts a locked messaging library across segments using the buying trigger as the entry point. For each vertical/segment,
  extracts the trigger from VOC evidence, defines the buying lens and must-have outcome, assigns ONE leading messaging
  pillar, and writes an entry-point message...
primitive: product-marketing
sub_primitive: strategy
ontology_type: segment-messaging-map
review_gate: 2
inputs:
  required:
  - product-messaging
  recommended:
  - icp-research
  - win-loss
  - positioning
  - customer-interviews
- type: segment-messaging-map
  feeds_into:
  - landing-page-copy
  - outreach-emails
  - abm-campaign
  - lifecycle-marketing
  - email-nurture
depends_on:
- product-messaging
- landing-page-copy
- outreach-emails
- abm-campaign
- lifecycle-marketing
- email-nurture
owned_by_agent: pmm
mcps_used:
- gdrive
- notion
- gdrive
- notion
triggers:
  slash_commands:
  - /vertical-messaging
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Vertical messaging

Adapts a locked messaging library across segments without rebuilding it. One core message, multiple entry points — each segment routed to its leading pillar by the buying trigger that sent that buyer searching. Output is a per-segment routing map that answers "what do we say to this buyer?" for every downstream surface (industry pages, ABM, outreach, launches). Knowledge type: `segment-messaging-map` (per `.claude/rules/ontology.md`); maturity: emergent → validated after client review → canonical when locked.

Adapted from Diane Wiredu's (Lion Words) trigger-based segment messaging framework — cite-only, re-voiced. Full provenance: `.claude/discovery/0726-lion-words-vertical-messaging-steal-analysis.md`.

## When to run

Invoke when the user asks for: `vertical messaging for [client]`, `adapt messaging for [industry/segment]`, `segment messaging map`, `messaging rollout across segments`, `what do we say to [vertical]?`, `entry-point messages per segment`. The tell that this skill applies: messaging is locked (or near-locked) AND the client sells one product into multiple segments that buy differently.

Segment messaging usually fails one of two ways: it's so simplified it can't drive targeted copy (one pitch broadcast everywhere), or so complex it never gets used (a full messaging track per segment, 3× the work). This skill is the middle path — the core library stays untouched; only the entry point changes per segment.

Do **NOT** invoke for: building the core messaging library (use `/product-messaging` — run it first), positioning strategy (use `/positioning`), role-based buyer personas (use `/icp-behavioural` — personas are roles; segments here are verticals, industries, or product-line audiences), or account-level ABM plays (use `/abm-campaign` — it consumes this skill's output).

**The Iron Law:** no invented triggers. Every buying trigger cites VOC evidence (win-loss quote, interview, CRM note, ICP intent-signal research) or is marked `[ESTIMATED]` with a validation flag for client review. Pillar names are quoted verbatim from the messaging library — never paraphrased. One leading pillar per segment; a secondary pillar is allowed, a rebuild is not.

## Inputs

**Required:**

- `messaging library` — the locked (or review-stage) `/product-messaging` output. Without pillars there is nothing to route.
- `segment list` — the verticals/segments to map, from client-approved segmentation. If segmentation is unvalidated, confirm with the user before mapping — a map built on rejected segments gets thrown out whole.

**Recommended (improve quality):**

- `icp-research` output — §8 segments + §9 intent signals and buying triggers are the head start for trigger extraction.
- `win-loss` output — loss/win themes carry trigger language verbatim.
- `customer-interviews` / transcripts — richest trigger source when available.
- `positioning` — keeps entry points anchored to the committed position.

**Segment axis** — define per run: industry vertical (most common), product line, or persona-segment. One axis per map; don't mix axes in one table.

## Steps

1. **Validate inputs** → messaging library present and current (check for superseding versions), segment list client-approved, segment axis confirmed. Pull upstream outputs (icp-research, win-loss, positioning) into context.
2. **Assemble VOC evidence per segment** → brain-first per `.claude/rules/brain-first-lookup.md`: client win-loss files, interview outputs, ICP intent signals, CRM notes. Only reach for external research (per `.claude/rules/exa-protocol.md`) when internal VOC is thin — and flag the gap.
3. **Extract the buying trigger per segment** → the question to interrogate every source with: *what changed in this buyer's world that sent them looking for a solution?* A trigger is a specific moment, market event, or catalyst (a regulation landing, an audit failure, an M&A event, a launch into a new market) — not a standing pain. Standing pains explain why the category exists; triggers explain why the buyer moved this quarter. 1–2 triggers per segment; cite evidence per trigger.
4. **Define the buying lens + must-have outcome** → per segment: how this buyer evaluates solutions once triggered (what's non-negotiable, what they compare against) and the tangible result they need to see to buy. Pull from pain-point consequence chains and benefit sections of the messaging library, sharpened by segment VOC.
5. **Assign the leading pillar** → for each segment, pick the ONE messaging pillar most likely to resonate given trigger + lens. Quote the pillar verbatim from the library. A secondary pillar may support; if no pillar fits a segment, that's a messaging-library gap — flag it, don't invent a pillar.
6. **Write the entry-point message** → 1–2 lines per segment that meet the buyer in their trigger moment and open the leading pillar. Entry points are doorways into the core message, not new messaging. Apply client TOV rules.
7. **Assemble the map** → per the premium reference: the routing table + per-segment briefs + confidence tags per ontology (`[VERIFIED]`/`[INFERRED]`/`[ESTIMATED]`) + validation flags on every estimated row + data gaps.
8. **Write to client folder** → `messaging/MMYY-vertical-messaging-{axis-or-line}.md`. Push to GDoc/Notion per frontmatter targets. Hand off downstream: the map briefs `/landing-page-copy` (per-vertical pages), `/outreach-emails` and `/abm-campaign` (segment sequences), `/lifecycle-marketing` (segment nurture).

## What good looks like

### Evaluations (binary pass/fail before declaring "done")

- Every segment row is complete: trigger, lens, must-have outcome, leading pillar, entry-point message — or explicitly `[Not available]` with reason.
- Every trigger cites VOC evidence or carries `[ESTIMATED]` + a validation flag. Zero uncited triggers presented as fact.
- Every leading pillar is a verbatim quote from the messaging library (grep-checkable against the source file).
- One leading pillar per segment (secondary allowed and labeled as such; no segment gets a rebuilt message).
- Entry-point messages are 1–2 lines, trigger-specific, and would fail if swapped between segments (the swap test — if the line works for another segment, it isn't an entry point, it's a tagline).
- Segment axis is single and named; segments come from client-approved segmentation.
- Confidence distribution meets strategy-output thresholds (≥60% verified, ≤10% estimated per ontology).
- Data gaps section lists every segment where VOC was thin, with the recommended fill (interviews to run, transcripts to pull).

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
