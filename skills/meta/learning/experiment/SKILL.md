---
name: experiment
version: '1.1'
last_updated: 2026-03-25
author: genesys-growth
description: 'Tracks structured experiments for content, messaging, and workflow iterations in a SQLite database. Logs hypotheses,
  controlled dimensions, variants, and results; pulls past test data into context when designing new variations to prevent
  re-testing failures and compound learnings. Produces experiment records, review summaries, and next-test suggestions. Triggers:
  "/experiment new", "/experiment log", "/experiment review", "I want to test", "what experiments have we run on", "what should
  I test next". NOT for A/B testing in code — that is development work. NOT for general research — use context skills instead.'
goal: Tracks structured experiments for content, messaging, and workflow iterations in a SQLite database.
outcome: Tracks structured experiments for content, messaging, and workflow iterations in a SQLite database. Logs hypotheses,
  controlled dimensions, variants, and results; pulls past test data into context when designing new variations to prevent
  re-testing failures and compound learnings. Produces...
primitive: meta
sub_primitive: learning
ontology_type: experiment-log
review_gate: 0
inputs:
  required: []
  recommended: []
outputs:
- type: experiment-log
  feeds_into: []
depends_on: []
feeds_into: []
owned_by_agent: operator
mcps_used: []
push_targets:
- gdrive
- notion
triggers:
  slash_commands:
  - /experiment
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# /experiment — Track hypotheses, variants, and learnings

Stop re-testing what already failed. Stop forgetting what worked. This skill gives you a structured experiment tracking system that compounds knowledge across sessions — every test informs the next one.

For full schema, modes (new/log/review/suggest), and messaging-mode scoring → `references/process.md`.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "/experiment new [description]"
- "/experiment log [experiment-id or description]"
- "/experiment review [domain]"
- "/experiment suggest [domain]"
- "New experiment:" or "I want to test..."
- "Log experiment result:" or "The results are in..."
- "What experiments have we run on...?"
- "What should I test next for...?"

**Do NOT invoke when:**
- User is doing A/B testing in code (development work)
- User wants to track bugs (use `/track-bug`)
- User wants general research (use context skills)

---

## Modes (quick reference)

| Mode | Purpose | Required arg |
|------|---------|--------------|
| `/experiment new [description]` | Create experiment + variants | description (optional) |
| `/experiment log [id or description]` | Record results + learnings | id or description |
| `/experiment review [domain]` | Browse past experiments | domain (optional) |
| `/experiment suggest [domain]` | Recommend next test | domain |

For full mode workflows + output formats → `references/process.md`.

---

## Domains

| Domain | Use for |
|--------|---------|
| `content` | LinkedIn hooks, post formats, content angles, newsletter subjects |
| `messaging` | Value props, positioning variants, CTA wording, taglines |
| `workflow` | Skill parameters, MCP configurations, prompt engineering |
| `outreach` | Email subject lines, sequences, cold outreach approaches |
| `pricing` | Packaging variants, pricing page layouts, discount strategies |

---

## Database

**Location:** `.claude/experiments/experiments.db`
**Tables:** `experiments`, `variants`, `learnings`, `experiments_fts` (FTS5 index)

For full SQL schema + init script → `references/process.md`.

---

## Integration with Other Skills

- **`/session-wrap`** — Auto-detects experiments discussed in a session, offers to log results
- **`/linkedin-content`** — Before generating new posts, checks for content experiments and applies learnings
- **`/outreach-emails`** — Before generating sequences, checks for outreach experiments
- **`/product-messaging`** — Before generating messaging, checks for messaging experiments
- **`/recall`** — Promoted experiment learnings are searchable via the recall index

---

## Learning promotion

When a learning proves durable (validated by 2+ experiments), promote it:

1. **To MEMORY.md** — Add to relevant section as a permanent rule
2. **To CLAUDE.md** — If it's a formatting, voice, or workflow pattern
3. **To client CLAUDE.md** — If client-specific
4. Mark as `promoted = 1` in the learnings table

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/process.md` | Full SQL schema, init script, 4 modes with workflows + output formats, messaging-mode scoring framework, notes |
| `references/outbound-experiments.md` | Outbound-domain framework: 3 experiment types (list-only / copy-only / combined), sample-size table, 21-day measurement, 1% rule baseline check, prioritization order. Use for `/experiment new domain=outreach`. Stolen via /steal Phase 5–6 ADAPT #1. |

---

