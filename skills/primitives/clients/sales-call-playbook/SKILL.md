---
name: sales-call-playbook
version: '1.0'
last_updated: 2026-04-16
author: genesys-growth
description: Generates a phase-by-phase during-call reference guide for sales conversations. Produces a cheat sheet covering
  diagnosis questions, summary template, tour checklist, ROI math, investment script, objection handlers, and close protocol.
  Designed to be open on a second screen during the call. Consumes client-discovery output as upstream input. Feeds into client-proposals
  as post-call context. Triggered by "sales call playbook", "call playbook for [company]", "prepare call guide", "sales framework
  for [prospect]", or "call cheat sheet".
goal: Generates a phase-by-phase during-call reference guide for sales conversations.
outcome: Generates a phase-by-phase during-call reference guide for sales conversations. Produces a cheat sheet covering diagnosis
  questions, summary template, tour checklist, ROI math, investment script, objection handlers, and close protocol. Designed
  to be open on a second screen during the call....
primitive: clients
ontology_type: sales-enablement-asset
review_gate: 2
inputs:
  required:
  - product-messaging
  - battlecards
  recommended: []
- type: sales-enablement-asset
  feeds_into: []
depends_on:
- product-messaging
- battlecards
owned_by_agent: operator
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
context: fork
effort: medium
paths: projects/consulting/**, projects/prospects/**
---

# Sales call playbook

Generate a during-call reference guide tailored to a specific prospect. Produces a phase-by-phase cheat sheet you have open on a second screen while running the sales conversation.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (playbook is internal rep-facing — inline cites stay for QA), R2 (multi-phase playbook ships as one doc with toggles per phase), R3 (talking-point framing operator-direct), R6 (close phase names stage-appropriate next step), R9 (verb-led phase names).

---

## Process at a glance

```
INPUT VALIDATION → DIAGNOSIS → SUMMARY + MATH → TOUR + CLOSE → REVIEW & CHAIN
```

Five steps:
1. Adapt diagnosis questions (reorder discovery + add PMM funnel layer + follow-up branches)
2. Build summary + entry-point template (3 pillars + anonymised client parallels)
3. Create tour checklist (ALWAYS / SOMETIMES / NEVER tiers, conditional on prospect type)
4. Pre-fill math template (prospect's likely numbers, blanks for live confirmation)
5. Generate close sections (investment script + 6-8 objection cards + close protocol)

Output: 8-phase during-call cheat sheet (diagnosis → summary → tour → math → investment → reaction → objections → close).

Full flowchart, step-by-step runbook, and operational rules in the premium reference.

---

## Claude Code triggers

**Invoke this skill when user says:**
- "Sales call playbook for [company]"
- "Call playbook for [prospect]"
- "Prepare call guide for [company]"
- "Sales framework for [prospect]"
- "Call cheat sheet"

**Do NOT invoke when:**
- User wants pre-call research only → Use `client-discovery` skill
- User wants a product demo script → Use `demo-script` skill
- User wants to create a proposal → Use `client-proposals` skill

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Client-discovery output** | Prospect context, opening playbook, questions, qualification criteria | Output from `/client-discovery` |

### Optional (improve quality)

| Input | How it helps |
|-------|--------------|
| Known pricing context | Pre-fills investment section more accurately |
| Prior meeting notes | Adapts diagnosis to what's already been discussed |
| Competitor intel | Sharpens positioning in summary and tour |
| Engagement type | Tailors math and investment to specific offer |

**If inputs are missing:** Ask user to run `/client-discovery` first, or provide company name/URL to run both in sequence.

---

## Operational rules (carry into every playbook)

These are the non-negotiable behaviors the playbook must encode at every phase. They're embedded in the templates but worth surfacing here so the agent doesn't dilute them when adapting:

- **Listen 75%, talk 25% in diagnosis.** Never pitch before completing diagnosis.
- **Summarize in your own words before presenting your offer.** Reflect back what you heard.
- **Show the real workspace, not a slide deck.** Tour is the proof.
- **Use prospect's numbers, calculate conservatively.** Never overestimate.
- **Name the price after tour and math, never before.**
- **Don't defend the price — say it, stop, wait.** Silence does the work.
- **Offer payment flexibility, never discounts.**
- **If not a match, refer them elsewhere.** Walking away protects future trust.

---

## Anti-hallucination guardrails

1. **Never fabricate client results.** If you're unsure whether a result is accurate, don't mention it. An exaggerated claim costs more trust than a good story earns.
2. **Never invent financial projections.** Use prospect's real numbers or leave blanks.
3. **Anonymise all client references.** Use role + situation, never names.
4. **Mark estimates.** If pre-filling math with researched numbers, note they're estimates to confirm on the call.

---

## Integration with other skills

| Skill | Relationship |
|-------|--------------|
| **client-discovery** | Upstream — provides prospect context, opening playbook, questions |
| **client-proposals** | Downstream — create proposal after the call using discovery + call notes |
| **win-loss-analysis** | Optional — analyse recorded call against framework |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

