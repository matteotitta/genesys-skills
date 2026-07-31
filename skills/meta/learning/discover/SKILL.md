---
name: discover
version: '1.0'
last_updated: 2026-04-09
author: genesys-growth
description: 'Proactive skill and automation discovery. Scans 6 data sources (sessions, Linear, Slack, Gmail, Granola, Calendar)
  to identify repeatable work patterns that should become skills, hooks, scheduled agents, prompt chains, or MCP workflows.
  Tracks patterns across runs in a persistent SQLite database with BUILD/DEFER/KILL scoring. Triggers: "/discover", "what
  should I automate?", "find repeatable patterns", "what skills should I build?", "discovery scan".'
goal: Proactive skill and automation discovery.
outcome: Proactive skill and automation discovery. Scans 6 data sources (sessions, Linear, Slack, Gmail, Granola, Calendar)
  to identify repeatable work patterns that should become skills, hooks, scheduled agents, prompt chains, or MCP workflows.
  Tracks patterns across runs in a persistent SQLite...
primitive: meta
sub_primitive: learning
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended: []
- type: discovery-report
  feeds_into:
  - skill-catalog
depends_on: []
- skill-catalog
owned_by_agent: operator
mcps_used:
- gmail
- granola
- linear
- slack
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

# /discover — Weekly Skill & Automation Discovery

Proactively identifies repeatable work patterns across your tools and recommends what to automate.

For full process (subcommands, 6 phases, scoring, persistence) → the premium reference.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "/discover"
- "What should I automate?"
- "Find repeatable patterns"
- "What skills should I build?"
- "Discovery scan"
- "What am I doing repeatedly?"

**Do NOT invoke when:**
- User wants to run a specific skill (run that skill directly)
- User wants to create a specific skill (use `/skill-creator`)
- User wants to audit workspace health (use `/audit`)

---

## Subcommands quick reference

| Command | Action | Detail |
|---------|--------|--------|
| `/discover` | Run full discovery scan (default) | 6-phase scan |
| `/discover status` | Pattern DB stats + top 5 BUILD candidates | SQL summary |
| `/discover dismiss <name>` | Mark pattern dismissed | Excluded from future reports |
| `/discover built <name> <path>` | Mark pattern as built | Links to artifact |
| `/discover history` | Pattern evolution over time | Top 20 by recency |

Parse `$ARGUMENTS` to determine subcommand. Default (no args) = full scan.

For full SQL queries per subcommand → the premium reference.

---

## Core decisions

### Scoring framework (8 dimensions, 0 or 1 each)

| # | Dimension | Question |
|---|-----------|----------|
| 1 | **frequency** | Will this run 5+ times per month? |
| 2 | **time_savings** | Saves 30+ minutes vs. doing it manually? |
| 3 | **quality** | Automation produces better/more consistent output? |
| 4 | **context_dep** | Inherits context from other skills? |
| 5 | **distinct** | Fills a gap no existing skill covers? |
| 6 | **reuse** | Works for multiple clients with minimal adaptation? |
| 7 | **measurable** | Clear criteria for good vs. bad output? |
| 8 | **recurrence** | Pattern appeared in 3+ separate weekly scans? |

### Verdicts
- Score 6-8 = **BUILD** — create the automation
- Score 4-5 = **DEFER** — watch for another week
- Score 0-3 = **KILL** — not worth automating

### Automation type selector

| Type | When to recommend |
|------|------------------|
| **skill** | Multi-step process with structured output, repeatable across clients |
| **hook** | Automatic trigger before/after a specific tool use |
| **scheduled-agent** | Time-based recurring task |
| **prompt-chain** | Sequence of skills that always run together |
| **mcp-workflow** | Cross-tool data movement or enrichment |

### Auto-promotion rule

If a pattern's `occurrence_count >= 3` in the database and it was previously DEFER, set `recurrence: 1` which may push to BUILD.

For full classification guide and per-pattern JSON schema → the premium reference.

---

## Data Sources (6)

1. Session recall DB (last 7 days)
2. Linear (last 7 days)
3. Slack (last 7 days)
4. Gmail (last 7 days)
5. Granola (last 7 days)
6. Google Calendar (last 14 days, catches biweekly patterns)

Full SQL queries + MCP calls per source live in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Verify against existing catalog.** Don't mark "distinct" without checking `.claude/skills/meta/catalog/skill-catalog/SKILL.md`.
2. **Use real evidence.** Each pattern needs source-cited snippets — no invented examples.
3. **Update existing patterns.** Set `is_existing: true` if the pattern already exists in the DB; don't create duplicates.
4. **MCP failures don't block scan.** Log the failure, continue with available sources.

---

## Notes

- The session recall DB is the richest source. Linear, Slack, Gmail, Granola, and Calendar add cross-tool visibility.
- Pattern hash uses first 16 chars of SHA-256 — sufficient for personal scale.
- Dismissed patterns stay in DB for history but are excluded from future reports.
- Scheduled-agent runs should complete in 5-10 min. Prioritize sessions + Slack if MCPs are slow.

---

