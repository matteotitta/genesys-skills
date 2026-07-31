---
name: runbook
version: '1.0'
last_updated: 2026-03-09
author: genesys-growth
description: 'Synthesizes documentation sources (SKILL.md files, MCP configs, code comments, client docs) into structured
  runbooks with step-by-step procedures, troubleshooting sections, common gotchas, and recovery steps. Produces a runbook
  markdown document. Triggers: "/runbook [topic]", "create a runbook for", "document how to", "write a troubleshooting guide
  for", "write onboarding docs for". NOT for one-off answers — just answer directly. NOT for client proposals — use /client-proposals.
  NOT for content strategy docs — use /content-strategy.'
goal: Synthesizes documentation sources (SKILL.md files, MCP configs, code comments, client docs) into structured runbooks
  with step-by-step procedures, troubleshooting sections, common gotchas, and recover
outcome: 'Synthesizes documentation sources (SKILL.md files, MCP configs, code comments, client docs) into structured runbooks
  with step-by-step procedures, troubleshooting sections, common gotchas, and recovery steps. Produces a runbook markdown
  document. Triggers: "/runbook [topic]", "create a runbook...'
primitive: meta
sub_primitive: learning
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
- gdrive
- gdrive
- notion
triggers:
  slash_commands:
  - /runbook
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# /runbook — Synthesize docs into actionable runbooks

Turn scattered documentation, config files, and tribal knowledge into a structured runbook that anyone can follow. Produces step-by-step procedures with troubleshooting sections, common gotchas, and recovery steps.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "/runbook [topic or path]"
- "Create a runbook for..."
- "Document how to..."
- "Write a troubleshooting guide for..."
- "How do I set up...?" (when the answer should be saved as a runbook)
- "Write onboarding docs for..."

**Do NOT invoke when:**
- User wants a one-off answer (just answer directly)
- User wants a client proposal (use `/client-proposals`)
- User wants content strategy docs (use `/content-strategy`)

---

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| Source(s) | Yes | File paths, folder paths, or topic description to synthesize |
| Type | No | `setup` / `troubleshooting` / `onboarding` / `workflow` / `reference` (default: inferred) |
| Audience | No | `self` (personal reference) / `client` (handoff doc) / `team` (onboarding guide) (default: `self`) |

---

## Process

### Step 1: Gather sources

Read all provided source documents. If a folder is given, scan for relevant files:
- `.md` files (SKILL.md, CLAUDE.md, README)
- `.mjs` / `.js` / `.py` files (read header comments and docstrings)
- `.json` config files (extract structure and key settings)
- `.sh` scripts (extract usage patterns and flags)

If only a topic is given (no paths), search the codebase for relevant files:
```
Glob for: **/*{topic}*
Grep for: relevant terms in.claude/ and project files
```

### Step 2: Identify runbook type

Based on the sources and user intent, classify the runbook:

- **Setup** — "How to install/configure/initialize X from scratch"
- **Troubleshooting** — "When X breaks, here's how to diagnose and fix it"
- **Onboarding** — "New to X? Here's everything you need to know"
- **Workflow** — "How to do X step-by-step (recurring process)"
- **Reference** — "Quick reference card for X (flags, configs, common commands)"

### Step 3: Extract and organize

From the source material, extract:
1. **Prerequisites** — What's needed before starting
2. **Core procedure** — Step-by-step instructions
3. **Failure modes** — What can go wrong (from code comments, error handling, gotchas in MEMORY.md)
4. **Recovery steps** — How to fix each failure mode
5. **Verification** — How to confirm everything worked

### Step 4: Write the runbook

Use the output format below. Adjust depth based on audience:
- `self` — Terse, assumes context, focuses on commands and quick reference
- `client` — Clear, explains why, includes screenshots/examples
- `team` — Balanced, includes context but stays focused

### Step 5: Save and optionally export

Save the runbook as markdown in the appropriate location:
- Internal runbooks → `.claude/runbooks/{topic}.md`
- Client runbooks → `projects/consulting/{client}/docs/{topic}-runbook.md`
- Course runbooks → `projects/courses/{course}/docs/{topic}-runbook.md`

Optionally export to Google Docs for client delivery:
```bash
cd.claude/mcp/gdrive && node create-doc-unified.mjs "/path/to/runbook.md" "Title" --client {slug}
```

---

# {Title} — Runbook

> **Type:** {setup|troubleshooting|onboarding|workflow|reference}
> **Audience:** {self|client|team}
> **Last updated:** {date}
> **Source files:** {list of files synthesized}

---

## Prerequisites

- [ ] {prerequisite 1}
- [ ] {prerequisite 2}

---

## Procedure

### 1. {First major step}

{Explanation if audience is client/team}

```bash
{command}
```

**Expected output:** {what you should see}

### 2. {Second major step}

{...}

---

## Troubleshooting

### Symptom: {what the user sees}

**Cause:** {why it happens}

**Fix:**
```bash
{recovery command}
```

**Verify:** {how to confirm the fix worked}

### Symptom: {another failure mode}

{...}

---

## Common gotchas

- {gotcha 1 — discovered from experience or MEMORY.md}
- {gotcha 2}

---

## Quick reference

| Action | Command |
|--------|---------|
| {action} | `{command}` |

---

## Related

- {link to related runbook}
- {link to source skill or MCP}
```

---

## First Use Cases

Priority runbooks to create when this skill is built:

1. **MCP server troubleshooting** — workspace-mcp OAuth gotchas, Xero token refresh, GDrive script failures (sources: MEMORY.md gotchas, `.claude/mcp/` scripts, `gdrive-protocol.md`)
2. **New client setup** — End-to-end from prospect to active client (sources: `consulting-clients.md`, `/new-client` command, `gdrive-config.json`)
3. **Skill creation** — How to build a new skill from scratch (sources: `_schema/SKILL.template.md`, `_schema/AUTHORING.md`, `skill-catalog`, `skill-reviewer`)
4. **Session recall** — How the recall system works and how to maintain it (sources: `recall/SKILL.md`, `session-indexer.py`, MEMORY.md)

---

## Notes

- Runbooks should be living documents — update them when new gotchas are discovered
- `/session-wrap` can flag potential runbook updates when troubleshooting patterns emerge
- Keep runbooks under 200 lines — if longer, split into multiple focused runbooks
- Use the `self` audience for internal tooling, `client` for handoff docs, `team` for GTM-E School materials
