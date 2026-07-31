---
name: workspace-cleanup
version: '1.0'
last_updated: 2026-03-29
author: genesys-growth
description: 'Runs a structured workspace audit across 5 dimensions: root hygiene, client folder structure compliance, skill
  system health, git hygiene, and MCP/plugin status. Produces a pass/flag/action report with actionable next steps per dimension.
  Triggers: "clean up workspace", "audit workspace", "workspace hygiene", "spring clean", "check workspace health". NOT for
  auditing a specific client folder — use manual cleanup. NOT for auditing a specific skill — use /skill-reviewer. NOT for
  code quality review — use code review tools.'
goal: 'Runs a structured workspace audit across 5 dimensions: root hygiene, client folder structure compliance, skill system
  health, git hygiene, and MCP/plugin status.'
outcome: 'Runs a structured workspace audit across 5 dimensions: root hygiene, client folder structure compliance, skill system
  health, git hygiene, and MCP/plugin status. Produces a pass/flag/action report with actionable next steps per dimension.
  Triggers: "clean up workspace", "audit workspace",...'
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
- clay
- gdrive
- notion
triggers:
  slash_commands:
  - /workspace-cleanup
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
paths:.claude/**
disable-model-invocation: true
---

# Workspace cleanup

Periodic hygiene check for the Claude Code workspace. Runs 5 structured checks and produces a markdown report with pass/flag/action verdicts.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "clean up workspace"
- "audit workspace"
- "workspace hygiene"
- "spring clean"
- "check workspace health"

**Do NOT invoke when:**
- User wants to clean up a specific client folder (use manual cleanup)
- User wants to audit a specific skill (use `/skill-catalog`)
- User wants to review code quality (use code review tools)

---

## Input Requirements

### Required Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Workspace root** | Current working directory | Auto-detected |

### Optional Inputs

| Input | How It Helps |
|-------|--------------|
| Focus area | Run only specific checks (e.g., "just check clients") |

---

## Process (Step-by-Step)

### Check 1: Root folder hygiene

1. List all dot-folders at workspace root
2. Cross-reference against `.gitignore` — flag any dot-folder NOT gitignored that isn't a known system folder (`.git`, `.claude`, `.github`, `.cursor`, `.gitmodules`)
3. Check for folders >50MB that aren't known MCPs — flag with size
4. Verify `.gitignore` has no stale references to paths that don't exist

**Pass criteria:** No unexpected dot-folders, no stale gitignore entries.

### Check 2: Client structure compliance

For each folder in `projects/consulting/active/`:
1. Has `CLAUDE.md`? → **FLAG** if missing
2. Has `docs/` and `notes/`? → **FLAG** if missing
3. CLAUDE.md has `## Engagement goals` and `## Success metrics`? → **FLAG** if missing
4. Any files at root level that should be in topic folders? → **FLAG**
5. Last file modification date → **FLAG** if >30 days dormant (suggest archive discussion)

For each folder in `projects/prospects/`:
1. Last activity date → **FLAG** if >60 days dormant (suggest cleanup)
2. Count files — note if only 1-2 files (minimal engagement)

**Pass criteria:** All active clients have CLAUDE.md with goals/metrics, docs/, notes/.

### Check 3: Skill system health

1. Run `python3.claude/skills/_schema/validate-frontmatter.py --all` — verify all SKILL.md files parse cleanly
2. Check each skill's `last_updated` field — **FLAG** if >90 days old
3. List all commands in `.claude/commands/` — check each has a corresponding skill
4. Count total skills, agents, commands — report summary

**Pass criteria:** All skills parse, none >90 days stale, no orphaned commands.

### Check 4: Git hygiene

1. `git status` — check for untracked files that should be gitignored
2. Look for files >1MB that are tracked — **FLAG** with size
3. Verify `.gitignore` covers: `*.env*`, `**/credentials/`, `**/token.json`, `*.keys.json`
4. Check for any `.DS_Store` files tracked in git

**Pass criteria:** No credential files tracked, no large binary files, clean gitignore.

### Check 5: MCP & plugin health

1. Read `settings.local.json` — list all `mcp__*` permission entries
2. Cross-reference against available MCP tools in current session
3. **FLAG** any permission entry with no matching MCP tool (stale permission)
4. Check `.claude/mcp/` directories — flag any with node_modules >200MB
5. Run `list_subroutines` via Clay MCP — **FLAG** any subroutines not referenced in skills
6. Check for new MCP tools available that aren't referenced in any skill (capability gaps)

**Pass criteria:** All permissions have matching MCPs, no oversized node_modules, Clay subroutines mapped.

---

# Workspace cleanup report — {date}

## Summary

| Check | Verdict | Issues |
|-------|---------|--------|
| Root hygiene | PASS/FLAG | {count} |
| Client structure | PASS/FLAG | {count} |
| Skill health | PASS/FLAG | {count} |
| Git hygiene | PASS/FLAG | {count} |
| MCP & plugins | PASS/FLAG | {count} |

## Details

### Check 1: Root hygiene
{findings}

### Check 2: Client structure
{findings per client}

### Check 3: Skill health
{findings}

### Check 4: Git hygiene
{findings}

### Check 5: MCP & plugins
{findings}

## Action items
- [ ] {prioritized actions}
```

---

## Quality Checklist

- [ ] All 5 checks executed (not skipped)
- [ ] Each check has a clear PASS or FLAG verdict
- [ ] Flagged items have specific, actionable recommendations
- [ ] No false positives (verified before flagging)
- [ ] Report is concise — findings only, no filler
