---
name: demo-script
version: '1.1'
last_updated: 2026-02-06
author: genesys-growth
description: Writes structured demo scripts with talk tracks, click paths, timing guides, and objection handlers for product
  demonstrations. Produces scripts tailored for sales demos, marketing webinars, and video recordings. Consumes positioning
  and product-messaging to translate strategic framing into compelling live walkthroughs. Sibling of /sales-deck and /battlecards
  under the /sales-enablement orchestrator. Triggered by "demo script", "product demo", "demo flow", "write a demo", or "demo
  talk track".
goal: Writes structured demo scripts with talk tracks, click paths, timing guides, and objection handlers for product demonstrations.
outcome: Writes structured demo scripts with talk tracks, click paths, timing guides, and objection handlers for product demonstrations.
  Produces scripts tailored for sales demos, marketing webinars, and video recordings. Consumes positioning and product-messaging
  to translate strategic framing into...
primitive: sales-enablement
ontology_type: sales-enablement-asset
review_gate: 2
inputs:
  required:
  - battlecards
  - product-messaging
  recommended: []
- type: sales-enablement-asset
  feeds_into: []
depends_on:
- battlecards
- product-messaging
owned_by_agent: sales
mcps_used: []
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
effort: medium
---

# Demo Script

Create structured product demo scripts that translate positioning and messaging into compelling live demonstrations. Output includes talk tracks, click paths, timing guides, and objection handlers for sales demos, marketing webinars, and video recordings.

The body of this file holds decision-grade context (when to invoke, inputs, demo-length structure tables, anti-hallucination guardrails, integration). Step-by-step process, output template + craft library, quality gates, and feedback loops live in the premium reference.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in demo-script |
|---|---|---|
| **R1** | Source placement (three layers) | Demo scripts are **internal rep-facing** (live-call scripts). Inline source notes stay for QA auditability. Reps don't read the script live — they study it before the call. |
| **R3** | Product-update tone | When the script introduces a capability, rep voice frames as "we built X to do Y" not "we are thrilled to show you X." Even on launch-day demos. |
| **R6** | CTA hierarchy | The closing of the demo names the next step appropriate to the deal stage — trial / pilot for cold, signed proposal for warm. Never blog or "let me follow up" as the close. |
| **R9** | Action-oriented section names | "Open the demo / Land the capability / Handle the question / Close on next step" — verb-led throughout. |

---

## Claude Code triggers

**Invoke this skill when user says:**
- "Write a demo script"
- "Create demo flow"
- "Demo talk track"
- "Product demo script"
- "Sales demo script"
- "Demo narrative"
- "Walkthrough script"
- "Product tour script"
- "Demo for [persona]"
- "How to demo [feature]"

**Do NOT invoke when:**
- User wants explainer video script → Different format
- User wants onboarding flow → Use `lifecycle-marketing` skill
- User wants webinar content → Use `webinar-brief` skill
- User wants sales deck → Use `/sales-deck` skill
- User wants battlecards → Use `/battlecards` skill

---

## Input requirements

### Required inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Product context** | What the product does | User or company-context |
| **Target persona** | Who's watching the demo | User or ICP research |
| **Demo goal** | What action you want after | User specifies |

### Optional inputs (improve quality)

| Input | How it helps |
|-------|--------------|
| Product messaging | Ensures demo aligns with positioning |
| Competitor context | Enables differentiation moments |
| Common objections | Builds in objection handling |
| Demo environment | Specific clicks/screens to show |
| Time constraint | Shapes depth and pacing |
| Previous demos | Patterns that work |

### Input validation checklist

Before proceeding, verify:
- [ ] Product capabilities understood
- [ ] Target persona defined
- [ ] Demo duration known (5/15/30 min)
- [ ] Primary use case identified

**If inputs are missing:** Ask for product overview, target persona, and desired demo length. Offer to run product-messaging or icp-behavioural first.

---

## Process at a glance

| Phase | Purpose | Output |
|-------|---------|--------|
| 1. Demo strategy | Define aha moment, map persona pain to flow, set timing | Strategic framework |
| 2. Script development | Write hook, sections (talk track + click path), objections, close | Draft script |
| 3. Demo polish | Add engagement checkpoints, backup paths, one-pager | Polished script + one-pager |

Full step-by-step (with checkpoints, flowchart, review gate) in the premium reference.

---

## Demo structure templates (decision-grade)

### 15-minute sales demo

| Section | Time | Purpose | Key elements |
|---------|------|---------|--------------|
| **Hook** | 0:00-1:00 | Capture attention | Pain statement, promise |
| **Context** | 1:00-3:00 | Establish relevance | "What I've heard from you..." |
| **Demo Part 1** | 3:00-7:00 | Core workflow | Primary use case |
| **Demo Part 2** | 7:00-10:00 | Differentiation | What competitors can't do |
| **Demo Part 3** | 10:00-12:00 | Depth/expansion | Secondary features |
| **Close** | 12:00-15:00 | Drive action | Summary, next step |

### 30-minute discovery + demo

| Section | Time | Purpose |
|---------|------|---------|
| **Discovery** | 0:00-8:00 | Understand their world |
| **Positioning** | 8:00-10:00 | How we help people like you |
| **Demo** | 10:00-25:00 | Tailored walkthrough |
| **Close** | 25:00-30:00 | Next steps |

### 5-minute video demo (marketing)

| Section | Time | Purpose |
|---------|------|---------|
| **Hook** | 0:00-0:15 | Pain + promise |
| **Context** | 0:15-0:45 | Who this is for |
| **Demo** | 0:45-4:00 | Core flow only |
| **Close** | 4:00-5:00 | CTA |

---

## Anti-hallucination guardrails

1. **Don't invent features.** Only script features you know exist.
2. **Mark assumptions.** Use "[CONFIRM: click path]" for unverified flows.
3. **No fake metrics.** Don't promise specific outcomes in talk track.
4. **Persona-specific.** Adapt language to actual persona, not generic buyer.
5. **Time-realistic.** Verify timing works in actual demo environment.

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **product-messaging** | Provides input | Messaging informs talk track |
| **icp-behavioural** | Provides input | Persona pain points drive demo flow |
| **sales-enablement** | Parent skill | Orchestrator for all sales assets |
| **sales-deck** | Sibling skill | Deck presentations from same context |
| **battlecards** | Sibling skill | Competitive intel feeds objection handlers |
| **webinar-brief** | Related output | Demo can be core of webinar |

---

## MCP data integration

**Level:** 2 — PM Execution (demo-specific pulls)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Granola** | Previous demo recordings/notes | `search_meetings` | Always (demo-specific) |

### Fallback (no MCP)

- User-provided demo recordings or notes
- Manual product walkthrough documentation

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

