---
name: wiki
version: '1.0'
last_updated: 2026-04-11
author: genesys-growth
description: 'Per-client-folder hygiene and semantic drift detection. Runs structured checks inside a single client engagement
  folder: contradictions between canonical files (e.g., positioning v1 vs. v5 language still in docs/), stale claims superseded
  by newer research, orphan files referenced nowhere, missing hot.md/log.md scaffolding, and new-source candidates from gaps.
  Produces a lint report with flagged items + suggested fixes. Triggers: "/wiki", "/wiki lint {client}", "lint this client
  folder", "check this engagement for drift". NOT for global workspace audit (use /audit) and NOT for absorbing new source
  material (use /learn).'
goal: Per-client-folder hygiene and semantic drift detection.
outcome: 'Per-client-folder hygiene and semantic drift detection. Runs structured checks inside a single client engagement
  folder: contradictions between canonical files (e.g., positioning v1 vs. v5 language still in docs/), stale claims superseded
  by newer research, orphan files referenced nowhere,...'
primitive: meta
sub_primitive: learning
ontology_type: runbook
review_gate: 1
inputs:
  required: []
  recommended: []
- type: wiki-lint-report
  feeds_into:
  - learn
  - session-wrap
depends_on: []
- learn
- session-wrap
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
effort: medium
paths: projects/consulting/**
---

# /wiki — per-client-folder hygiene and drift detection

Runs inside a single client engagement folder. Catches semantic drift, stale references, and structural gaps before they contaminate a deliverable.

`/audit` covers the whole workspace. `/workspace-cleanup` covers file-system hygiene globally. `/wiki` covers *content consistency inside one client folder* — which neither of the other two can do.

---

## Triggers

**Invoke when user says:**
- `/wiki` (run lint against the current client folder, auto-detected from cwd)
- `/wiki lint {client-slug}` — run lint against a specific active client
- `/wiki status` — show which clients are missing hot.md / log.md
- `/wiki status {client-slug}` — show hot.md + last 10 log.md entries for a client
- "lint this client folder"
- "check this engagement for drift"
- "what's stale in {client}?"

**Do NOT invoke when:**
- User wants to clean up the global workspace (use `/workspace-cleanup`)
- User wants a full workspace health audit (use `/audit`)
- User wants to absorb new source material (use `/learn`)
- User wants to run structured research (use `/company-context`, `/competitor-research`, etc.)

---

## Subcommands

| Command | Action |
|---------|--------|
| `/wiki` | Lint the current client folder (auto-detect from cwd) |
| `/wiki lint {client-slug}` | Lint a specific active client |
| `/wiki status` | Show which clients have complete operations layer (CLAUDE.md + hot.md + log.md) |
| `/wiki status {client-slug}` | Show the current hot.md + recent log.md for one client |
| `/wiki history {client-slug}` | Parse log.md and show the full operation timeline |

Parse `$ARGUMENTS` to route. Default (no args) = lint current folder.

---

## Subcommand: `status` (no client)

Walk `projects/consulting/active/*/` and report which clients have the full operations layer:

| Client | CLAUDE.md | hot.md | log.md | Last log entry |
|--------|-----------|--------|--------|----------------|
| ClientCo | ✓ | ✓ | ✓ | 2026-04-11 init |
| ClientCo | ✓ | ✓ | ✓ | 2026-04-11 init |

Flag any client missing `hot.md` or `log.md`. Suggest creating them per the shared template in `projects/consulting/CLAUDE.md`.

---

## Subcommand: `status {client-slug}`

1. Read `projects/consulting/active/{client-slug}/hot.md` — display verbatim
2. Read `projects/consulting/active/{client-slug}/log.md` — display last 10 entries
3. If either is missing, say so and offer to create it

---

## Subcommand: `history {client-slug}`

1. Read `projects/consulting/active/{client-slug}/log.md` in full
2. Parse `## [YYYY-MM-DD] {operation} | {subject}` entries
3. Present as a chronological table grouped by operation type:
   - `lock` events (canonical deliverables)
   - `review` events (gate outcomes)
   - `ingest` events (source material absorbed)
   - `decision` events (direction changes)
4. Highlight the most recent `lock` for each major deliverable type (positioning, messaging, ICP, competitors)

---

## Default command: `lint {client}`

### Phase 1: Resolve the target client

1. If a client slug was passed, use `projects/consulting/active/{slug}/`
2. Else, check `cwd` — if inside an active client folder, use that one
3. Else, ask the user which client to lint (via AskUserQuestion)

Confirm the target path before running any checks.

### Phase 2: Load the operations layer

Read, in this order:
1. `{client}/CLAUDE.md`
2. `{client}/hot.md` (if present)
3. `{client}/log.md` (if present)

If `hot.md` or `log.md` are missing, flag as a **structural gap** and continue — don't block.

### Phase 3: Catalogue the canonical files

From `CLAUDE.md`, extract every explicitly referenced file path (positioning, messaging, ICP, competitors, brand, pricing, etc.). These are the "canonical" files — the current source of truth for each deliverable type.

Then walk the client folder and list every `.md` file. Classify each as:
- **Canonical** — referenced in CLAUDE.md
- **Superseded** — earlier dated version of a canonical file (e.g., `0226-positioning-v4.md` when `0326-positioning-v5.md` is canonical)
- **Orphan** — not referenced anywhere in CLAUDE.md, hot.md, or log.md, and not a superseded canonical
- **Support** — notes, docs, raw transcripts (under `notes/`, `docs/`) — not subject to drift checks

### Phase 4: Run the five drift checks

#### Check 1: Contradictions between canonical files

For each pair of canonical files that cover overlapping topics (positioning + messaging, messaging + sales enablement, ICP + competitors), compare the core claims:
- Product naming (e.g., "Atlas platform" vs. "Atlas product family")
- Key differentiators
- ICP segment definitions
- Pricing figures
- Competitor threat level assignments

Flag any pair where the claims appear to contradict. **Quote the conflicting lines verbatim** — don't paraphrase.

#### Check 2: Stale references to superseded files

Grep the canonical files, `docs/`, and `notes/` for references to superseded files (e.g., `0226-positioning-v4.md` when v5 exists). Stale references in:
- **Canonical files** → flag as critical (could produce wrong output)
- **docs/** → flag as warning (client-provided, may be intentional history)
- **notes/** → flag as informational (historical context is fine)

#### Check 3: Orphan files

For each orphan file identified in Phase 3, ask:
- Is this a draft that was never promoted? → suggest `/learn` to integrate or delete
- Is this a leftover from a superseded version? → suggest moving to an `archive/` subfolder
- Is this a file created by a different agent that never updated CLAUDE.md? → suggest adding a CLAUDE.md reference

#### Check 4: Operations layer gaps

- **hot.md missing** → flag + offer to create from template
- **log.md missing** → flag + offer to create from template
- **hot.md stale** — `Updated:` timestamp older than 14 days AND log.md has newer entries → flag as stale cache
- **hot.md over word cap** — word count > 500 → flag + suggest trimming
- **log.md entries without proper prefix** — entries not matching `## [YYYY-MM-DD] {operation} | {subject}` → flag as format drift

#### Check 5: New-source candidates from gaps

From the canonical files, identify claims marked with `[UNAVAILABLE]`, `[ESTIMATED]`, or "TBD / TBC". These are known data gaps. Surface them as research candidates — files that could be produced by `/learn`, `/company-context`, `/competitor-research`, etc.

Don't propose BUILDs — just name the gap and suggest the skill that could fill it.

### Phase 5: Produce the lint report

Write the report to `{client}/wiki-lint-{date}.md`. Structure:

```markdown
# Wiki lint report — {client}

**Ran:** {date} {time}
**Operations layer:** {CLAUDE.md: ✓/✗} {hot.md: ✓/✗} {log.md: ✓/✗}
**Files scanned:** {N canonical, M superseded, K orphans, J support}

---

## Critical (could produce wrong output)

### Contradiction: {file-a} vs {file-b}
{quote from file-a}
{quote from file-b}
**Suggested fix:** {one line}

### Stale reference to superseded file
**Found in:** {canonical file path}
**Points to:** {superseded file}
**Current canonical:** {current file}
**Suggested fix:** {one line}

---

## Warnings (should address soon)

### Orphan file: {path}
**Content summary:** {one line}
**Suggested action:** {integrate / archive / reference in CLAUDE.md}

### Operations layer: {specific issue}
**Suggested fix:** {one line}

---

## Informational (data gaps, historical drift)

### Data gap: {claim} marked [UNAVAILABLE]
**Found in:** {file path}
**Suggested skill:** {which skill could fill this}

---

## Summary

- **Critical:** N items
- **Warnings:** N items
- **Informational:** N items
- **Operations layer health:** {complete / partial / missing}
- **Recommended next action:** {one line}
```

Also append an entry to `{client}/log.md`:

```markdown
## [{date}] lint | wiki check | {N} critical, {N} warnings
Report: wiki-lint-{date}.md
```

---

## Quality checks before presenting the report

- [ ] Every "contradiction" flag has both conflicting lines quoted verbatim
- [ ] Every "stale reference" flag names both the old and new file
- [ ] Every orphan has a summary of its content (not just the path)
- [ ] No false positives from `docs/` (client-provided history is often intentional)
- [ ] No false positives from `notes/` (raw material is meant to be raw)
- [ ] The log.md entry for the lint run was appended

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Flagging every dated file as "stale" | Only flag if CLAUDE.md points elsewhere *and* the old file is referenced from a canonical |
| Flagging orphans under `notes/` or `docs/` | Only canonical + compiled topic folders are subject to orphan checks |
| Running global lint across all clients | `/wiki` is always per-client; use `/audit` for global |
| Producing a fix without quoting the evidence | Every flag must cite the exact line that triggered it |
| Silently rewriting files | Lint is diagnostic only — never edits canonical files; only the report + log.md entry are written |
