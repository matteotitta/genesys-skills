---
name: extrovert-sync
version: '1.0'
last_updated: 2026-05-28
author: genesys-growth
description: 'Detects drift in Extrovert seed source files (voice bundle, AI-speak rules, brand TOV, positioning, CLAUDE.md) and re-pushes only the affected layers. Runs ambiently at every session start via SessionStart hook with a 6-hour rate limit and a 10-second timeout. Also invokable ad-hoc via /extrovert-sync. Triggers: "sync extrovert", "push extrovert seed", "extrovert is stale", "re-seed extrovert".'
goal: Keep Extrovert workspace in sync with Genesys voice + context as it evolves in the repo, with no manual prompts.
outcome: 'Silent no-op when nothing changed; one-line status when a layer drifted and re-pushed; clean error when push fails. State persists in gitignored.sync-state.json; ambient hook never blocks session start.'
primitive: social
sub_primitive: null
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
- extrovert
triggers:
  slash_commands:
  - /extrovert-sync
  natural_language:
  - sync extrovert
  - push extrovert seed
  - extrovert is stale
  - re-seed extrovert
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: low
disable-model-invocation: true
---

# Extrovert ambient sync

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Operational sync skill — internal-reference floor. Applies [[feedback_execution_doctrine_refinements_step6]] R1 (status reports stay internal-only), R3 (operator-direct report voice), R9 (verb-led status section names). No customer-facing surface; R2/R5/R6/R7/R8 not applicable.

## Why this exists

When Genesys voice rules, brand TOV, or positioning change in the repo, Extrovert keeps serving the old guidance until someone manually re-runs `push.mjs`. This skill closes the gap: a hash-tracked check at every session start re-pushes only the layers whose source files actually changed.

## What it does

`.claude/mcp/extrovert/sync.mjs` maps each of the 6 Extrovert resource layers (style, context, comment-examples, monitored-topics, dm-playbook, insights) to the source files that feed it. At each invocation it computes a composite SHA-256 per layer, compares against `.sync-state.json` (gitignored, per-machine), and re-pushes only stale layers via `node push.mjs --only=<csv>`.

Rate-limited: at most one sync run per 6 hours unless `--force`. Initialized so the first ambient run after seeding is guaranteed to be a no-op (state file written immediately after Step 8 push with hashes-at-that-time).

## How to invoke

| Use case | Command |
|---|---|
| Manual ad-hoc resync (respects rate limit) | `node.claude/mcp/extrovert/sync.mjs` |
| Manual force resync (ignores rate limit) | `node.claude/mcp/extrovert/sync.mjs --force` |
| Report what would re-push without acting | `node.claude/mcp/extrovert/sync.mjs --dry-run` |
| Re-baseline hashes (no push) | `node.claude/mcp/extrovert/sync.mjs --init` |

The ambient SessionStart hook at `.claude/hooks/extrovert-sync-hook.sh` runs the no-flag form silently every time Claude opens. It caps at 10 seconds and always exits 0 — sync failures never block session start.

## Source-file → layer map

| Layer | Source files (composite hash) |
|---|---|
| style | `0526-context-bundle.md`, `0526-ai-speak-anti-patterns.md`, `brand/0226-tov.md`, `genesys/CLAUDE.md` |
| context | `0526-context-bundle.md`, `genesys/CLAUDE.md`, `positioning/0526-positioning.md` |
| comment-examples | `0526-context-bundle.md`, `0526-ai-speak-anti-patterns.md` |
| monitored-topics | `0526-context-bundle.md` |
| dm-playbook | `0526-context-bundle.md` |
| insights | `0526-context-bundle.md` |

Editing any source file invalidates the composite hash for every layer that references it. The push then re-creates that layer's content on Extrovert.

## Known v1 trade-off — duplication on real content drift

`push.mjs` is **create-only** for list-style resources (comment-examples, topics, dm-playbook, insights). Style and context have find-or-update logic; the other four do not.

Practical effect: the very first ambient sync after seeding is a no-op (hashes match). But if a source file genuinely changes and triggers a re-push of a list-style layer, the new entries land on top of the existing ones — duplicates accumulate.

Mitigation when this bites:
1. Note which layer(s) have duplicates by running `node.claude/mcp/extrovert/verify.mjs` and comparing counts to expected.
2. Manually delete the stale duplicates in the Extrovert UI (workspace `<id>`).
3. Re-run `node.claude/mcp/extrovert/sync.mjs --force` to confirm clean state.

v2 (when triggered) will add idempotent text-hash lookup to the four list-style layers so re-pushes update in place.

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Hook hangs >10s at session start | Network slow to mcp.goextrovert.com | Hook auto-times-out at 10s; if persistent, set `EXTROVERT_SYNC_DISABLED=1` in env |
| Sync reports `FAIL: push.mjs exited N` | OAuth expired / Extrovert API down | Re-run OAuth via `node.claude/mcp/extrovert/oauth-helper.mjs`; then `--force` retry |
| Sync runs every session but always "no-op" | Working correctly — state file confirms no drift | This is the happy path |
| `.sync-state.json` missing | Never initialized OR machine moved | Run `node.claude/mcp/extrovert/sync.mjs --init` |

## Final ship gate

**Not applicable** — this is internal infrastructure tooling, not a client-facing output skill. The `/premortem --output` convention (per `.claude/rules/premortem-production.md`) targets skills producing deliverables that land in front of clients, prospects, or external audiences. This skill produces an internal sync runbook (analog to `meta/infra/` utilities) and runs as a background SessionStart hook with no external surface.

