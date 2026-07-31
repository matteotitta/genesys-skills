---
name: session-wrap
version: '1.0'
last_updated: 2026-03-09
author: genesys-growth
description: 'Extracts learnings at end-of-session by scanning the conversation for corrections, decisions, patterns, and
  context changes. Produces structured learning entries written to MEMORY.md, suggests CLAUDE.md rule updates, and identifies
  skill improvement opportunities. Triggers: "/session-wrap", "wrap up", "session done", "log learnings", "what did we learn
  today", "close out this session". NOT for searching past sessions — use /recall instead. NOT for daily briefings — use /today
  instead. Only run at end of session, not mid-conversation.'
goal: Extracts learnings at end-of-session by scanning the conversation for corrections, decisions, patterns, and context
  changes.
outcome: 'Extracts learnings at end-of-session by scanning the conversation for corrections, decisions, patterns, and context
  changes. Produces structured learning entries written to MEMORY.md, suggests CLAUDE.md rule updates, and identifies skill
  improvement opportunities. Triggers: "/session-wrap",...'
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
  - /session-wrap
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: low
---

# /session-wrap — Extract learnings and close the feedback loop

Run at the end of a work session to capture what was learned, decided, and built. Prevents knowledge loss between sessions and creates a compounding improvement loop for the skill system.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "/session-wrap"
- "Wrap up"
- "Session done"
- "Log learnings"
- "What did we learn today?"
- "Close out this session"

**Do NOT invoke when:**
- User wants to search past sessions (use `/recall`)
- User wants a daily summary (use `/today`)
- Mid-session — this is an end-of-session skill

---

## Process

### Step 1: Scan for corrections

Review the conversation for moments where the user corrected you or redirected your approach. These are the highest-value learnings.

**Look for patterns like:**
- "No, that's wrong" / "Actually..." / "Don't do that"
- User rejecting a tool call or approach
- User providing a better way to do something
- Repeated mistakes that suggest a missing rule

**Output format:**
```
### Corrections found
- [CORRECTION] {what was wrong} → {what's correct}
  Suggested rule: {rule to prevent recurrence}
  Scope: [LOCAL] or [GLOBAL]
```

### Step 2: Scan for decisions

Extract decisions made during the session — direction changes, approach selections, scope choices.

**Look for patterns like:**
- "Let's go with..." / "We'll use..." / "The approach is..."
- Choosing between alternatives
- Committing to a specific implementation
- Client-facing decisions (positioning choices, messaging direction, etc.)

**Output format:**
```
### Decisions made
- [DECISION] {what was decided}
  Context: {why it was decided}
  Client: {client name if applicable}
```

### Step 3: Scan for patterns

Identify workflow patterns that emerged — things that worked well, processes that could become skills or rules.

**Look for patterns like:**
- Multi-step processes that were repeated
- Tool combinations that proved effective
- Prompting strategies that produced good results
- Workflow shortcuts discovered

**Output format:**
```
### Patterns discovered
- [PATTERN] {description}
  Potential: {skill improvement / new rule / new command}
```

### Step 4: Scan for new context

Identify new information gathered that should persist — client context, project state, tool configurations.

**Look for patterns like:**
- New client details or preferences
- Project milestones or status changes
- MCP/tool configuration changes
- File structure changes

**Output format:**
```
### New context
- [CONTEXT] {what's new}
  Update target: {CLAUDE.md / client CLAUDE.md / MEMORY.md}
```

### Step 5: Deduplicate against existing memory

Before suggesting any updates, read:
- `/Users/matteotittarelli/.claude/projects/-Users-matteotittarelli-Desktop-CORE-WORK-CLAUDE-CODE/memory/MEMORY.md`
- `/Users/matteotittarelli/.claude/projects/-Users-matteotittarelli-Desktop-CORE-WORK-CLAUDE-CODE/memory/learnings.md` (if exists)

Skip any finding that's already captured. Flag updates to existing entries if the new info refines or corrects them.

### Step 6: Present findings

Show the user a structured summary:

```
SESSION WRAP — {date}
═══════════════════════════════════════

### Corrections ({count})
{corrections from Step 1}

### Decisions ({count})
{decisions from Step 2}

### Patterns ({count})
{patterns from Step 3}

### New context ({count})
{context from Step 4}

═══════════════════════════════════════

### Suggested actions
1. [WRITE] Add to learnings.md: {learning}
2. [UPDATE] MEMORY.md: {what to change}
3. [UPDATE] CLAUDE.md: {new rule}
4. [UPDATE] {client}/CLAUDE.md: {context update}
5. [IMPROVE] {skill-name}: {suggestion}

Approve actions? (all / select by number / skip)
```

### Step 7: Execute approved actions

On approval:

1. **Write learnings** — Append to `learnings.md` with `[LOCAL]` or `[GLOBAL]` tags and today's date
2. **Update MEMORY.md** — Edit existing entries or add new sections
3. **Update CLAUDE.md** — Add new rules to the appropriate section
4. **Update client CLAUDE.md** — Add context to the relevant client folder
5. **Log skill improvements** — Note in the skill's folder or flag for next session

### Step 8: Index the session

Run the session indexer to capture this session in the recall database:

```bash
cd "$CLAUDE_CODE_ROOT" && python3.claude/hooks/session-indexer.py
```

### Step 9: Lightweight consolidate-memory pass

After indexing, invoke `anthropic-skills:consolidate-memory` in **lightweight surface-only mode** — surface anomalies, don't auto-prune. Cadence: every session-wrap.

**What runs:**

1. Read all memory files at `~/.claude/projects/-Users-matteotittarelli-Desktop-CORE-WORK-CLAUDE-CODE/memory/`
2. Surface (don't fix) any of:
   - **Duplicates** — two files saying substantively the same thing (e.g., two voice-rule files banning the same word with different phrasing)
   - **Contradictions** — two files giving conflicting guidance on the same topic
   - **Orphans** — files with zero `[[link]]` references (per `.claude/rules/auto-memory.md` cross-link floor)
   - **Stale entries** — files referencing engagements / people / decisions that haven't appeared in any session in 90+ days
   - **Index drift** — entries in MEMORY.md whose linked files don't exist (or files in memory/ not referenced by MEMORY.md)
3. Output a compact summary (≤10 lines):

   ```
   CONSOLIDATE-MEMORY ({date})
   ────────────────────────────
   N memories scanned
   {X} duplicates flagged
   {Y} contradictions flagged
   {Z} orphans (zero [[link]]s)
   {W} stale (no session reference in 90d)
   {V} index drift items

   Run `/consolidate-memory` for full mode to fix.
   ```

**Discipline:**

- **Surface only.** Don't auto-delete, auto-merge, or auto-rewrite. The author (in the moment) has more context than the consolidator weeks later — surface; let the author decide.
- **Skip if nothing surfaced.** Common case is 0 issues; skip the summary entirely with a single line: `✓ Memory consolidation pass: 0 issues.`
- **Don't block session close.** The pass runs at the end of /session-wrap; the user sees the result and the session exits regardless.
- **One-line in MEMORY.md history.** If issues surfaced, append a one-line note to MEMORY.md's bottom: `<!-- consolidate: YYYY-MM-DD — X issues surfaced; full fix deferred -->`

**Why this exists.** Per the 2026-05-23 gbrain /steal analysis (item G10), `consolidate-memory` exists but only fires on user invocation. Manual = it rarely runs = drift accumulates. Chaining it into /session-wrap (which is already the natural per-session maintenance hook) catches drift before it spreads.

---

## Escalation Rules

From CLAUDE.md — determines where learnings are written:

- `[LOCAL]` — Stays in project CLAUDE.md or client CLAUDE.md (project-specific context, client preferences)
- `[GLOBAL]` — Goes to macro CLAUDE.md (voice rules, formatting standards, tool usage patterns)
- Patterns that repeat 3+ times across sessions → promote to permanent rules

---

## Edge Cases

- **Empty session** (short Q&A, no meaningful work): Skip with "No significant learnings to capture."
- **Pure research session** (reading, no decisions): Focus on Step 4 (new context) only
- **Multi-client session**: Group findings by client
- **Skill-building session**: Focus on Step 3 (patterns) and capture skill governance insights

---

## Notes

- This skill complements `/recall` — recall searches past sessions, session-wrap writes to them
- This skill complements `/today` — today chains productivity tools, session-wrap chains learning tools
- The learnings file uses reverse-chronological order (newest first)
- Keep individual learnings to 1-2 sentences — context lives in the session itself (searchable via `/recall`)

---

## End-of-run HTML render (optional, prompted)

After the session wrap-up is produced and learnings are logged, the skill asks:

> *"Render this as a shareable HTML file too? (y/n)"*

- **`y`** → emit a sibling `.html` file: structured retro layout (decisions / blockers / learnings / next steps as separate cards), timestamps preserved, link-out to any cited skill or client folder. Filename: `session-wrap-{YYYYMMDD-HHMM}.html`.
- **`n`** → stop; markdown stays primary.

**Rationale:** session wraps are usually internal but occasionally get shared as a "here's what we did today" client recap. HTML render makes that one-paste-away. Convention from `.claude/rules/throwaway-editor-pattern.md` (output-not-export variant).
