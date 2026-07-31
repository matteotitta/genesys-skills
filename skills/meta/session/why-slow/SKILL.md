---
name: why-slow
version: '1.0'
last_updated: 2026-05-20
author: genesys-growth
description: 'In-session diagnostic for "why is Claude hanging / slow right now?" Reads recent startup-timing
  log entries, current MCP process list, latest sync-pull debug log, and worktree count, then prints a focused
  top-suspect report. Use when a session feels stuck or a tool call is taking too long. Triggers: "/why-slow",
  "why is this slow", "what is hanging", "diagnose this hang".'
goal: Produce a focused diagnostic of the current session's likely slowness culprit in <30 lines.
outcome: A short report identifying the top suspect (which MCP, which hook, which worktree-search) so the
  user can decide whether to restart, kill a process, or scope the next operation differently.
primitive: meta
sub_primitive: session
ontology_type: runbook
review_gate: 0
status: draft
inputs:
  required: []
  recommended: []
- type: runbook
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands:
  - /why-slow
  natural_language:
  - why is this slow
  - what is hanging
  - diagnose this hang
disable-model-invocation: false
---

# /why-slow — in-session perf diagnostic

When the user says "why is this slow" or invokes `/why-slow`, run the four checks below in parallel and emit a focused report. Goal: identify the top suspect in <30 lines so the user knows whether to restart, kill a process, or rephrase the query.

## Checks (run all four in parallel via Bash)

### 1. Recent startup-timing log (last 10 entries)
```bash
tail -10.claude/automation/sync-pull/startup-timing.log
```
Look for: rising `parent_age` values across recent sessions (cold-start getting slower) OR a row where `worktrees` count spiked.

### 2. Current MCP processes
```bash
ps aux | grep -E "(mcp|claude.*node)" | grep -v grep | head -15
```
Look for: any process with high CPU% (wedged), or duplicate processes (failed handshake retrying), or processes from MCPs the user no longer uses.

### 3. Latest sync-pull debug log (tail)
```bash
tail -30.claude/automation/sync-pull/session-start.debug.log
```
Look for: timeout errors ("timeout after 10s"), gdrive/notion error messages, OAuth failures.

### 4. Worktree count + size
```bash
git worktree list | grep -c worktrees/
du -sh.claude/worktrees/
```
Look for: count >20 or size >2GB (run the worktree-cleanup runbook).

## Report format (≤30 lines)

```
=== /why-slow diagnostic — {timestamp} ===

TOP SUSPECT: {one of: search-domain bloat | wedged MCP | OAuth-expired MCP | slow hook | no obvious slowness}

Evidence:
- {bullet 1 from the relevant check}
- {bullet 2}
- {bullet 3}

Recommended action:
- {one specific command or change}

Other observations:
- worktrees={N} ({GREEN if ≤15, YELLOW if 16-25, RED if >25})
- always-on MCPs={N} (target ≤14 per mcp-on-demand.md)
- last sync-pull: {status from debug log}
```

## Top-suspect heuristics (in priority order)

| Symptom | Top suspect | Action |
|---|---|---|
| Recent sessions show `parent_age` >10s | Slow MCP handshake | Read.claude/rules/mcp-on-demand.md; demote a B-tier MCP |
| MCP process at >100% CPU | Wedged MCP | `kill -9 <pid>` and the next tool call will respawn it fresh |
| sync-pull log shows `invalid_grant` | OAuth-expired MCP | Run the relevant recovery (see reference_gdrive_oauth_reauth.md, reference_xero_mcp_refresh.md) |
| Worktree count >25 | Search-domain bloat | Run worktree-cleanup runbook |
| All checks clean but tool calls slow | Bridge latency (/remote-control) or genuinely large search | Try the same query in CLI directly (not web); scope search to specific paths |

## When to escalate (the report says "no obvious slowness")

If all four checks come back clean and the user still feels slowness, the bottleneck is either:
1. Network latency (model inference) — `/remote-control` adds 100-500ms per tool roundtrip; nothing actionable
2. Genuinely large operation — the user's query asked for something that requires reading many files; encourage them to scope the query

Don't fabricate a culprit. "No obvious slowness — top phases were within normal ranges" is a valid answer.

## Anti-patterns

- ❌ Don't kill MCPs without checking CPU first — a quiet MCP process is fine, only kill if visibly wedged
- ❌ Don't recommend pruning worktrees inline — point at the runbook (it has the safety checks)
- ❌ Don't output more than 30 lines — defeats the "focused diagnostic" purpose
- ❌ Don't run heavy commands (broad grep, find on whole workspace) — defeats the purpose; this skill should add <2s

## Related

- Plan that birthed this skill: `~/.claude/plans/<plan>.md`
- Auto-loaded rule: `.claude/rules/mcp-on-demand.md`
- Audit snapshot: `.claude/automation/sync-pull/audit-2026-05-20.md`
- Worktree runbook: `.claude/automation/worktree-cleanup/cleanup-runbook.md`
- Timing log: `.claude/automation/sync-pull/startup-timing.log`
- Sync-pull debug log: `.claude/automation/sync-pull/session-start.debug.log`
