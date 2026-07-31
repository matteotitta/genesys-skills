---
name: today
version: '1.0'
last_updated: 2026-03-03
author: genesys-growth
description: 'Generates a daily productivity briefing by chaining Gmail, Calendar, Linear, and Slack into a single actionable
  summary with priorities, blockers, and recent decisions from the recall index. Produces a structured morning briefing or
  end-of-day status. Triggers: "/today", "what''s on my plate today", "morning briefing", "daily summary", "daily status",
  session start. NOT for checking a single tool — use Gmail MCP, Calendar MCP, or Linear directly. NOT for creating tasks
  — use Linear.'
goal: Generates a daily productivity briefing by chaining Gmail, Calendar, Linear, and Slack into a single actionable summary
  with priorities, blockers, and recent decisions from the recall index.
outcome: 'Generates a daily productivity briefing by chaining Gmail, Calendar, Linear, and Slack into a single actionable
  summary with priorities, blockers, and recent decisions from the recall index. Produces a structured morning briefing or
  end-of-day status. Triggers: "/today", "what''s on my plate...'
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
effort: low
---

# /today — Daily productivity briefing

Pull a structured daily briefing from all connected productivity tools in one shot. Designed to replace the morning ritual of checking 4 separate apps.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "/today"
- "What's on my plate today?"
- "Morning briefing"
- "Daily summary"
- "What do I need to focus on?"

**Do NOT invoke when:**
- User asks about a single tool only (e.g., "check my email" → use Gmail MCP directly)
- User asks for a specific Linear issue or calendar event
- User wants to send an email or create a task (action, not briefing)

---

## Modes

### `/today` (default) — Morning briefing

Start-of-day overview. What happened overnight, what's coming up, what needs attention.

### `/today wrap` — End-of-day wrap-up

What was done today, what's still pending, what to prep for tomorrow.

### `/today focus` — Quick focus check

Minimal output. Just the top 3 things that need attention right now.

---

## Process

### Phase 1: Gather data (parallel)

Pull from all 4 sources simultaneously using parallel tool calls. Do NOT run these sequentially.

**1a. Gmail** — Use `mcp__google-workspace__search_gmail_messages`
- Morning mode: `query: "newer_than:12h"`, `page_size: 15`
- Wrap mode: `query: "newer_than:24h"`, `page_size: 20`
- Always pass `user_google_email: "matteo@genesysgrowth.com"`
- Then batch-fetch content for the returned message IDs using `get_gmail_messages_content_batch`

**1b. Calendar** — Use `mcp__google-workspace__get_calendar_events`
- Morning mode: today's events
- Wrap mode: today's events + tomorrow's first 3
- Always pass `user_google_email: "matteo@genesysgrowth.com"`
- Use calendar ID: `matteo@genesysgrowth.com`

**1c. Linear** — Use `mcp__plugin_linear_linear__list_issues`
- `assignee: "me"`, `limit: 15`
- Filter to active states: In Progress, In Review, Next Up
- Sort by priority (Urgent > High > Medium > Low)

**1d. Slack** — Use `mcp__claude_ai_Slack__slack_search_public_and_private`
- Morning mode: search for mentions in last 12 hours
- Wrap mode: search for mentions in last 24 hours
- Query: `from:me OR to:me` or recent channel activity

**1e. Recent decisions** — Pull from session recall index
```bash
python3.claude/hooks/session-indexer.py --decisions --days 1
```
- Morning mode: last 24h of decisions
- Wrap mode: today's decisions only
- If recall.db doesn't exist, skip this source silently

### Phase 2: Synthesize

Process raw data into a structured briefing. Apply these rules:

**Email triage:**
- Categorize: Action required / FYI / Can wait
- Flag emails from clients (match against known client names from CLAUDE.md)
- Surface any emails with deadlines or time-sensitive language

**Calendar awareness:**
- Flag meetings starting in the next 2 hours
- Note prep needed (if meeting has agenda or docs linked)
- Identify back-to-back blocks with no buffer

**Linear priorities:**
- Group by project (ClientCo, Genesys, GTM Engineer School, etc.)
- Highlight blockers or overdue items
- Note cycle progress if relevant

**Slack highlights:**
- Summarize unread mentions
- Flag any DMs that need responses
- Note active threads you're part of

### Phase 3: Output

Format as a structured briefing following the template below.

---

## Tool Reference

| Tool | MCP | Purpose |
|------|-----|---------|
| Gmail search | `mcp__google-workspace__search_gmail_messages` | Find recent emails |
| Gmail read | `mcp__google-workspace__get_gmail_messages_content_batch` | Read email content |
| Calendar | `mcp__google-workspace__get_calendar_events` | Today's schedule |
| Linear | `mcp__plugin_linear_linear__list_issues` | Active tasks |
| Slack search | `mcp__claude_ai_Slack__slack_search_public_and_private` | Recent mentions |
| Slack channel | `mcp__claude_ai_Slack__slack_read_channel` | Channel activity |

---

## Notes

- Always run Phase 1 sources in parallel — do not wait for one before starting the next
- If any source fails (MCP unavailable), skip it and note "[Source] unavailable" in the briefing
- Client name matching: use client names from CLAUDE.md (ClientCo, ClientCo, GTM Engineer School, etc.)
- The user's email is always `matteo@genesysgrowth.com`
- Calendar ID is `matteo@genesysgrowth.com`
- Keep the briefing scannable — no walls of text, use the structured format

---

## End-of-run HTML render (optional, prompted)

After the markdown briefing is produced and shown to the user, the skill asks:

> *"Render this as a shareable HTML file too? (y/n)"*

- **`y`** → emit a sibling `.html` file in the same location: a single self-contained page (inline CSS, no external assets) with the same content laid out as: priority section at top, agenda + Linear queue + decisions in two columns below, source-of-data footer. Filename: `today-{YYYYMMDD}.html`.
- **`n`** → stop; markdown stays primary.

**Rationale:** most `/today` runs are terminal-only (just for me); occasional runs get forwarded to the team or a client weekly. The prompt keeps the choice in the moment of "I just saw the output, do I want to share it?" rather than buried in a flag I'd forget. Convention from `.claude/rules/throwaway-editor-pattern.md` (output-not-export variant — no copy-back button, since this is a one-way shareable).
