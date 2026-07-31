---
name: orchestrator
version: '2.0'
last_updated: 2026-04-30
author: genesys-growth
description: 'Routing convention that maps user intent to the correct skill or multi-skill chain. Reads the skill-catalog
  for metadata lookup, validates input/output dependencies, surfaces the right review gate. Today the orchestrator is invoked
  manually via slash commands; tomorrow it can be dispatched automatically by the Agent / Workflow tools per.claude/rules/orchestration-patterns.md. Triggers: ambiguous
  user requests that map to one or more skills, multi-step workflows, "run the chain for [client]". NOT a skill that produces
  artifacts — it coordinates other skills.'
goal: Route user intent to the correct skill or skill chain, citing ontology.md as the chain reference.
outcome: A correct dispatch — the right skill runs, with the right upstream inputs and the right review gate.
primitive: meta
sub_primitive: orchestration
ontology_type: runbook
review_gate: 0
inputs:
  required:
  - skill-catalog
  recommended: []
- type: skill-execution
  feeds_into: []
depends_on:
- skill-catalog
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: low
disable-model-invocation: true
---

# Orchestrator

The orchestrator is a **routing convention**, not an executor.

Today: routing happens manually — the user types a slash command (`/positioning`, `/aeo-content`, `/competitor-research`), and that skill runs in the current session. When the user types something ambiguous ("help me launch this product"), the orchestrator surface is the catalog + ontology chain reference, and the operator picks the right entrypoint.

Tomorrow: the Agent / Workflow tools dispatch role-based agents to execute these same chains automatically, with locked-down state preserved across cycles. See `.claude/rules/orchestration-patterns.md` for the patterns + the tool-agnostic mechanics.

This file describes what the orchestrator IS, not what it DOES. The doing happens in the skills themselves.

---

## What the orchestrator decides

When a user request maps to multiple possible skills, the orchestrator answers three questions:

1. **What is the user actually asking for?** Map intent to an ontology output type (positioning, messaging, competitor-intel, etc.).
2. **What chain is this in?** Look up the chain in `.claude/rules/ontology.md`. Identify which step the user is at.
3. **What's blocked vs ready?** Check upstream skill outputs are present + locked-down for the current client. If not, route to the upstream skill first.

That's the entire decision space. Routing logic doesn't live in this file — it lives in the catalog (which lists every skill, owner, ontology type, gate) and the ontology (which lists every chain).

---

## Routing reference — by user intent

| User intent | Primary chain | Entrypoint skill |
|-------------|---------------|------------------|
| New client engagement | New client (full) chain | `/company-context` |
| Competitive refresh | Competitive positioning refresh | `/competitor-research` |
| Content engine ramp-up | Content engine | `/content-strategy` |
| YouTube channel launch | YouTube channel launch | `/youtube-strategy` |
| Account prioritization (TAM scoring) | Account prioritization | `/lead-scoring` |
| Sales enablement build | Sales enablement | `/battlecards` |

For the canonical chain definitions (slugs and order), read `.claude/rules/ontology.md`. Don't duplicate them here — chains drift, and one source of truth prevents that.

---

## Where decisions live

| Decision | Source of truth |
|----------|-----------------|
| Skill metadata (deps, gate, owner, ontology type) | `.claude/skills/meta/catalog/skill-catalog/SKILL.md` (auto-generated) |
| Chain definitions (which skill follows which) | `.claude/rules/ontology.md`|
| Locked-down state (which client outputs are canonical) | Per-client `goals/`, `latest.md`, and the `status:` field in skill outputs |
| Role-agent dispatch + lock-down state | `.claude/rules/orchestration-patterns.md`|

Add new skills by writing a SKILL.md under the right primitive folder. The catalog regenerates on commit; chain-lint surfaces broken edges. Don't update this orchestrator file unless the routing principle itself changes.

---

## When NOT to invoke

- The user asks for a specific skill by name → run that skill directly.
- The user asks for a single artifact in isolation → just produce it.
- The user is mid-execution → finish the current step, don't re-route.
- The chain is one skill long → no orchestration needed.

---

## Operational footer

DO NOT add new logic here without first updating `ontology.md` (chain definitions) or the catalog (skill metadata). The orchestrator describes; ontology + catalog prescribe. Aspirational pseudocode and "future state" architecture diagrams have been intentionally removed from this file (Phase 5, 2026-04-30) — orchestration patterns + mechanics now live in `.claude/rules/orchestration-patterns.md`.
