---
name: client-onboarding
version: '1.0'
last_updated: 2026-02-02
author: genesys-growth
description: Generates client onboarding materials after engagement is confirmed. Produces access checklists, asset gathering
  lists, kick-off meeting agendas, and first-month deliverable plans tailored to the project scope from the signed proposal.
  Depends on client-proposals for engagement scope and pricing context. Downstream of the client-discovery and client-proposals
  chain. Triggered by "onboarding", "new client", "kick-off", "first month", "onboard [client]", or "start engagement with
  [company]".
goal: Generates client onboarding materials after engagement is confirmed.
outcome: Generates client onboarding materials after engagement is confirmed. Produces access checklists, asset gathering
  lists, kick-off meeting agendas, and first-month deliverable plans tailored to the project scope from the signed proposal.
  Depends on client-proposals for engagement scope and...
primitive: clients
ontology_type: client-engagement
review_gate: 2
inputs:
  required:
  - client-proposals
  - client-discovery
  recommended: []
- type: client-engagement
  feeds_into: []
depends_on:
- client-proposals
- client-discovery
owned_by_agent: b2b-consultant
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
paths: projects/consulting/**
disable-model-invocation: true
---

# Client onboarding

Generate comprehensive onboarding materials for new client engagements. Creates access checklists, asset gathering lists, and kick-off meeting agendas tailored to the project scope.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`doc-output-structure.md`](../../../../rules/doc-output-structure.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (onboarding pack is client-team review surface — cites in appendix), R2 (multi-asset onboarding pack ships as one doc with toggles per asset: access checklist + assets list + kick-off agenda), R3 (welcome framing operator-direct, never "thrilled to have you"), R6 (close → kickoff scheduling primary), R9 (verb-led section names).

---

## Process at a glance

```
INPUT VALIDATION → ACCESS CHECKLIST → ASSETS GATHER → KICK-OFF AGENDA → REVIEW & CHAIN
```

Five steps:
1. Generate access checklist (tools by category, owners, access level)
2. Create asset gathering list (per deliverable, with rationale)
3. Design kick-off agenda (60-min, scope-specific context areas)
4. Scaffold client folder (`projects/consulting/active/{client}/` + CLAUDE.md template)
5. Create brand hub if visual assets available (run `/brand-kit` Quick mode), else schedule for Week 2

Full flowchart, step-by-step runbook, self-evaluation gate in the premium reference.

---

## Claude Code triggers

**Invoke this skill when user says:**
- "Onboarding for [client]"
- "New client [name]"
- "Kick-off prep for [client]"
- "Starting with [client] tomorrow"
- "Onboarding checklist"
- "What do I need for the kick-off"

**Do NOT invoke when:**
- User wants discovery call prep → Use `client-discovery` skill
- User wants to create a proposal → Use `client-proposals` skill
- User wants to scaffold folder only → Use `new-client` skill

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Client name** | Company name | User provides |
| **Project scope** | Deliverables for first month/engagement | User provides or proposal |

### Optional (improve quality)

| Input | How it helps |
|-------|--------------|
| Client industry | Tailors tool recommendations (FinTech needs compliance tools) |
| Known stakeholders | Pre-populates kick-off attendee list |
| Competitors | Adds competitor-specific assets to gather |
| Engagement length | Adjusts scope of onboarding materials |
| Prior discovery notes | Avoids re-asking known context |

**If inputs are missing:** Ask for project scope — what are you delivering in month 1?

---

## Deliverable-to-asset mapping

Use this framework to identify what assets are needed for common deliverables:

| Deliverable | Required assets | Why needed |
|-------------|-----------------|------------|
| **Win/loss analysis** | 3-5 lost deal recordings, 3-5 won deal recordings, deal context spreadsheet, sales notes | Pattern identification requires multiple calls; context helps cross-reference by segment |
| **Competitor research** | Existing battlecards, lost deals to competitors, sales team POV, competitor pricing intel | Avoid duplicating work; get ground-level intel beyond public info |
| **ICP refinement** | Current ICP doc, top 10 best customers, top 10 churned, CRM segment data, customer interviews | Pattern recognition requires both positive and negative examples |
| **Positioning/messaging** | Current positioning doc, investor deck, founder story, testimonials, G2 reviews | Build on existing work; use authentic voice and proof points |
| **Website copy** | Current analytics, heatmaps, current site access, brand guidelines | Baseline performance; design constraints |
| **Brand hub** | Figma access, brand PDF/style guide, logo files (SVG/PNG), brand colors doc | Visual identity for all downstream deliverables |
| **Sales deck** | Current deck, demo scripts, objection handling doc, competitive intel | Understand current narrative; address known objections |
| **Battlecards** | Win/loss insights, competitor research, sales team input | Evidence-based competitive positioning |

---

## Anti-hallucination guardrails

1. **Base on scope.** Only request assets needed for stated deliverables.
2. **Be specific.** Not "marketing materials" but "current positioning doc."
3. **Include rationale.** Every asset needs a "why you need it."
4. **Don't invent stakeholders.** Ask client for attendee list.
5. **Don't assume tools.** Ask what CRM, analytics, etc. they use.

---

## Integration with other skills

| Skill | Relationship |
|-------|--------------|
| **client-proposals** | Onboarding follows accepted proposal |
| **client-discovery** | Discovery may precede onboarding |
| **company-context** | Pre-research client before kick-off |
| **win-loss-analysis** | Common first deliverable |
| **competitor-research** | Common first deliverable |
| **icp-behavioural** | Common first deliverable |
| **brand-kit** | Create visual brand system from brand assets |

---

## MCP data integration

**Level:** 3 — Content Execution (client-specific pulls)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Slack** | Client channel history, prior discussions | `slack_read_channel` | If client Slack channel exists |
| **Granola** | Kick-off meeting notes, discovery calls | `search_meetings` | Always |

### Fallback (no MCP)

- User-provided meeting notes
- Manual Slack history review

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

