---
name: weekly-plan
version: '1.0'
last_updated: 2026-03-30
author: genesys-growth
description: 'Orchestrates weekly planning by scanning client communications (Gmail, Slack, Granola, Calendar), checking Linear
  task state and engagement progress, then suggesting and creating tasks in Paperclip + Linear for agent execution. Produces
  a prioritized weekly task list with skill assignments and agent routing. The entry point for the weekly execution cadence.
  Triggers: "/weekly-plan", "let''s plan the week", "what should we work on this week", "weekly planning". NOT for creating
  a single task — just create it directly. NOT for daily briefings — use /today instead.'
goal: Orchestrates weekly planning by scanning client communications (Gmail, Slack, Granola, Calendar), checking Linear task
  state and engagement progress, then suggesting and creating tasks in Paperclip +
outcome: Orchestrates weekly planning by scanning client communications (Gmail, Slack, Granola, Calendar), checking Linear
  task state and engagement progress, then suggesting and creating tasks in Paperclip + Linear for agent execution. Produces
  a prioritized weekly task list with skill assignments and...
primitive: meta
sub_primitive: session
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended: []
- type: runbook
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used:
- gmail
- google-calendar
- granola
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
context: fork
effort: max
disable-model-invocation: true
---

# /weekly-plan — Weekly planning orchestrator

Plan the week's work across all active clients. Scan communications, check engagement state, suggest tasks with the right skills and agents, then create them in Paperclip and Linear for automated execution.

For full 6-phase process (gather / state-check / suggest / approve / create / summary) → the premium reference. For agent IDs, project IDs, status IDs, and other Linear lookups → the premium reference.

---

## Triggers

**Invoke when user says:**
- "/weekly-plan"
- "Let's plan the week"
- "What should we work on this week?"
- "Weekly planning"

**Do NOT invoke when:**
- User wants to create a single task (just create it directly)
- User asks for a daily briefing (use `/today`)
- User wants to run a specific skill (invoke that skill directly)

---

## Prerequisites

- Paperclip server running at `http://127.0.0.1:3100`
- Linear API key available (Paperclip secrets as `LINEAR_API_KEY`)
- Gmail and Calendar MCPs connected

---

## Process at a glance

| Phase | Purpose | Output |
|-------|---------|--------|
| **1. Gather** | Pull from Gmail, Slack, Granola, Calendar (parallel) | `notes/MMYY-weekly-context.md` per client |
| **2. State check** | Linear issues + client folders + ontology dependency check | Current-state map |
| **3. Suggest** | Group tasks by client; assign skill + agent + dependencies | Structured task list |
| **4. Approve** | Wait for user to approve / edit / reject | Approved task set |
| **5. Create** | Linear issue + Paperclip task per approved item | Created task IDs |
| **6. Summary** | Present what was created with agent routing | Summary report |

For full per-phase commands and curl payloads → the premium reference.

---

## Agent routing (quick reference)

| Agent | Skills it runs |
|-------|----------------|
| Researcher | company-context, competitor-research, ICP, TOV, transcripts, win-loss, brand-kit |
| Product Marketer | positioning, product-messaging, content-strategy, pricing |
| Growth Marketer | landing pages, case-study, lifecycle, email-nurture, webinar-brief |
| Content Creator | LinkedIn (all variants), youtube-scripts, aeo-content, thought-leadership, hype-man, newsletter |
| Sales | battlecards, demo-script, sales-deck, outreach-emails, abm-campaign, clay-search |
| Paid Marketer | ad-creative-brief, google-ads, linkedin-ads, paid-ads-audit, paid-campaign-strategy |
| Operator | skill-catalog, reviewers, brand-context, runbook, dashboard, experiment, workflow-design, recall |

For full agent IDs and Linear project/status/label IDs → the premium reference.

---

## Critical rules

1. **Always assign Linear issues to Matteo** (`assigneeId: <id>`). Even though Paperclip agents execute, Matteo is assignee for visibility.
2. **Always run Phase 1 sources in parallel.** Sequential pulls are 4x slower for no benefit.
3. **Don't fabricate communications.** If an MCP fails, note "[Source] unavailable" and proceed with what's available.
4. **Status logic:** No dependencies → "Next up". Has unresolved dependencies → "Backlog".
5. **Task title prefix:** AD —, SP —, GG —, GES —, PV — per client.

---

## Notes

- User email: `matteo@genesysgrowth.com`
- Paperclip company ID: `<id>`
- Agents pick up tasks on heartbeat (default 1 hour). For immediate execution: `POST http://127.0.0.1:3100/api/agents/{agentId}/heartbeat`

---

## End-of-run HTML render (optional, prompted)

After the weekly plan is produced and shown to the user, the skill asks:

> *"Render this as a shareable HTML file too? (y/n)"*

- **`y`** → emit a sibling `.html` file: visual weekly grid (Monday → Friday columns × time blocks × commitments), priority items highlighted, source attribution footer (Gmail / Slack / Granola / Calendar). Filename: `weekly-plan-{ISO-week}.html`.
- **`n`** → stop; markdown stays primary.

**Rationale:** weekly plans are the most likely synthesis output to get forwarded — to clients ("here's our focus this week"), to teammates ("here's what I'm prioritising"), or pinned in Slack. HTML render is the highest-leverage audience-external use case. Convention from `.claude/rules/throwaway-editor-pattern.md` (output-not-export variant).
