---
name: recall
version: '1.0'
last_updated: 2026-03-09
author: genesys-growth
description: 'Searches and recalls context from past Claude Code sessions via a SQLite FTS5 index with BM25 ranking. Produces
  relevance-ranked snippets, full session loads, and extracted decisions from across all past conversations. Supports filtering
  by topic, time range, and client. Triggers: "/recall [topic]", "what did we decide about", "pick up where I left off", "find
  the session where we", "what was I working on yesterday". NOT for searching current codebase files — use Grep/Glob instead.
  NOT for Slack/email/Linear search — use /today or direct MCP.'
goal: Searches and recalls context from past Claude Code sessions via a SQLite FTS5 index with BM25 ranking.
outcome: 'Searches and recalls context from past Claude Code sessions via a SQLite FTS5 index with BM25 ranking. Produces
  relevance-ranked snippets, full session loads, and extracted decisions from across all past conversations. Supports filtering
  by topic, time range, and client. Triggers: "/recall...'
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
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /recall
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: low
---

# /recall — Search past sessions and surface decisions

Search your Claude Code session history instantly. Instead of starting from zero each conversation, recall what was discussed, decided, and built in past sessions.

For full mode workflows (topic / temporal / client / decisions / stats), output formats, and indexer maintenance → the premium reference.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "/recall [topic]"
- "/recall yesterday" or "/recall last week"
- "/recall --client [name]"
- "/recall --decisions"
- "What did we decide about...?"
- "Pick up where I left off on..."
- "Find the session where we..."
- "What was I working on yesterday?"

**Do NOT invoke when:**
- User wants to search files in current codebase (use Grep/Glob)
- User wants to search Slack, email, or Linear (use `/today` or direct MCP)
- User is asking about something in the current conversation (just answer)

---

## Modes (quick reference)

| Mode | Purpose | Required arg |
|------|---------|--------------|
| `/recall [topic]` | BM25-ranked search across all sessions | topic |
| `/recall yesterday` / `last week` / `[date]` | Temporal browse | time range |
| `/recall --client [name]` | Filter by client | client name |
| `/recall --decisions` | Surface extracted decisions | optional client/days filter |
| `/recall --memory [topic]` | Tier-boosted search across durable memory pages (G13) | topic |
| `/recall --stats` | Index health stats (now includes memory page count + orphan count) | none |

For full mode workflows + output formats → the premium reference.

### `--memory` mode (G13 — added 2026-05-23)

Searches the `memory_pages` table (`~/.claude/.../memory/*.md`) with **tier-boosted ranking** distinct from session-content search. Use this mode when the question is about durable rules, voice, preferences, or canonical references rather than past session conversation.

**Tier boosts (multiplier on BM25 rank):**

| Type prefix | Boost | Reasoning |
|---|---|---|
| `feedback_*` | 1.5x | Durable voice/quality rules — highest signal |
| `reference_*` | 1.4x | Canonical references (people, repos, conventions) |
| `project_*` | 1.3x | Active engagement state |
| `user_*` | 1.2x | User preferences |
| unknown | 1.0x | Fallback |

Memory pages with ≥3 incoming `[[link]]`s get an additional +0.1x backlink boost.

**Mechanics:**

```bash
# Direct CLI use
python3.claude/hooks/session-indexer.py --memory "em-dash"
python3.claude/hooks/session-indexer.py --memory "outbound discipline"

# Memory index updates incrementally on every default indexer run.
# To force a memory-only reindex (e.g., after editing memory files):
python3.claude/hooks/session-indexer.py --index-memory
```

**Output includes** the page type, title (parsed past YAML frontmatter), slug, tier_boost actually applied, incoming-link count badge (`←N`), and BM25 snippet.

**When to use this mode vs. default `/recall`:**

| Question shape | Mode |
|---|---|
| "What did we decide about X in a past session?" | default `/recall [topic]` (session content) |
| "Do we have a voice rule about Y?" | `/recall --memory "Y"` (durable rules) |
| "What's our brain's canonical answer on Z?" | `/recall --memory "Z"` |
| "Pick up where I left off on...?" | default `/recall [topic]` |

In practice, this mode is invoked as Step 1 of `brain-first-lookup.md`'s ladder when the question is rule-shaped (voice / convention / preference) rather than session-shaped (decision / conversation / build).

Per G13 from the 2026-05-23 gbrain /steal — see [`.claude/discovery/0526-gbrain-steal-analysis.md`](../../../../discovery/0526-gbrain-steal-analysis.md).

---

## Database

**Location:** `.claude/sessions/recall.db`
**Tables:** `sessions`, `decisions`, `files_touched`, `sessions_fts` (FTS5 index)
**Indexer:** `.claude/hooks/session-indexer.py` (runs every 30 min via cron)

If DB doesn't exist, initialize it:

```bash
cd "$CLAUDE_CODE_ROOT" && python3.claude/hooks/session-indexer.py
```

For full schema queries and advanced SQL → the premium reference.

---

## FTS5 search syntax

| Syntax | Behavior |
|--------|----------|
| `"ClientCo positioning"` | All words match (AND default) |
| `'"funnel model"'` | Exact phrase match |
| `"positioning OR messaging"` | Either term |
| `"compet*"` | Prefix matches competitor, competitive, competition |

The index uses porter stemming, so "positioning" matches "positioned", "position", etc.

---

## Anti-Hallucination Guardrails

1. **Always run incremental indexer first.** Catches new sessions before searching.
2. **Don't fabricate session content.** Only return what's in the index or readable from JSONL.
3. **Loaded context stays focused.** When deep-loading a session, summarize what's relevant to the user's current task — not a full transcript dump.
4. **Sessions can be partial.** If FTS returns 0 results, say so — don't synthesize from nothing.

---

## Notes

- BM25 scores by term frequency × document rarity — short focused sessions score higher than long rambling ones
- Session slugs (e.g., "unified-wishing-lollipop") are searchable
- Indexer strips system reminders, tool results, IDE wrappers — only real conversation content is searchable
- Sessions with no user messages (metadata-only) are skipped during indexing

---

## End-of-run HTML render (optional, prompted)

After the recall results are shown in markdown, the skill asks:

> *"Render this as a shareable HTML file too? (y/n)"*

- **`y`** → emit a sibling `.html` file in the working directory: scannable results layout with each session as a card (title + date + snippet + relevance score), filterable client/topic tags at the top. Filename: `recall-{topic-slug}-{YYYYMMDD}.html`.
- **`n`** → stop; markdown stays primary.

**Rationale:** recall results occasionally get forwarded as context to teammates or clients ("here's what we discussed last quarter"). HTML is the right format for non-Claude-Code readers. Convention from `.claude/rules/throwaway-editor-pattern.md` (output-not-export variant).
