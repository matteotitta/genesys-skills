---
name: connect-mcp
version: '1.0'
last_updated: 2026-06-29
author: genesys-growth
description: 'Step-by-step runbook to connect any custom MCP to Claude — choosing the source (official plugin / community / custom HTTP / local stdio), deciding the mounting tier, wiring credentials, registering the server, introspecting its tools, and integrating it into skills. Operationalizes the mcp-on-demand.md policy with the Extrovert and Spider MCPs as worked examples. Triggers: "connect an MCP", "add a custom connector", "wire up a new MCP", "set up an MCP server in Claude". NOT for credit/spend policy — that lives in the per-MCP credits rules; this covers setup.'
goal: Connect any custom MCP to Claude end to end — source, tier, credentials, registration, introspection, and skill integration — following mcp-on-demand policy.
outcome: A new MCP mounted at the right tier with credentials wired via.claude/apis + load-mcp-env.sh, its tools introspected, and a promotion-review date set — reusing the Extrovert/Spider setup pattern instead of re-deriving it each time.
primitive: meta
sub_primitive: infra
ontology_type: runbook
review_gate: 1
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
  - /connect-mcp
  natural_language:
  - connect an MCP
  - add a custom connector
  - wire up a new MCP
  - set up an MCP server in Claude
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: low
---

# Connect an MCP

The step-by-step procedure for adding any custom MCP to Claude. The policy — when an MCP earns always-on status versus project-scope versus deferred — lives in [`mcp-on-demand.md`](../../../../rules/mcp-on-demand.md). This runbook is the procedure that policy implies, with Extrovert (project-scope HTTP) and Spider (local stdio) as worked examples.

Born from the `/steal` of Gojiberry's "Connect Claude to LinkedIn via MCP" playbook: the generic "add a custom connector" mechanics were worth keeping; the vendor connector itself was not. See `.claude/discovery/0626-gojiberry-linkedin-mcp-steal-analysis.md`.

## When to use

- Adding a new MCP server (any client, any service)
- A `/steal` or MCP-registry pass surfaces an MCP worth trying
- Re-enabling a demoted MCP into a specific workspace

## Process

### Step 1 — Choose the source

| Source | Use when | Tier it implies |
|---|---|---|
| Official plugin | An official plugin exists (e.g., `exa@claude-plugins-official`) | C (deferred) — zero startup cost |
| Community MCP | A maintained community server fits | B (project-scope) to start |
| Custom HTTP | A hosted server with an API key (e.g., Extrovert) | B (project-scope) |
| Local stdio | A local binary (e.g., Spider `spider-mcp`) | B (project-scope) |

### Step 2 — Decide the tier

Follow the `mcp-on-demand.md` decision tree, do not restate it:

- Official plugin exists → install as plugin (tier C, deferred).
- Otherwise → `claude mcp add --scope project` (tier B). This is the default for anything new.
- Promote to tier A (`~/.claude/settings.json`, always-on) only after 2–4 weeks of proven >50%-session use and auth stability, and document the promotion in MEMORY.md.

Default to tier B/C. Never add a new MCP to user-scope "to have it ready" — every always-on MCP adds a handshake and a failure mode to every session.

### Step 3 — Wire credentials

For an MCP needing a key:

1. Drop the key in a gitignored file: `.claude/apis/{service}-api-key.txt`.
2. The SessionStart hook `.claude/hooks/load-mcp-env.sh` exports it as `{SERVICE}_API_KEY` (kebab → snake, uppercase). So `extrovert-api-key.txt` → `$EXTROVERT_API_KEY`.
3. Reference the env var in the MCP config — never hard-code the key.

Local stdio servers (e.g., Spider) need no key.

### Step 4 — Register the server

**Claude Code (this workspace) — preferred for our work:**

```bash
# Project-scope HTTP server with bearer auth (Extrovert pattern):
claude mcp add <name> --scope project --transport http https://mcp.example.com \
  --header "Authorization: Bearer ${SERVICE_API_KEY}"

# Project-scope local stdio binary (Spider pattern):
claude mcp add <name> --scope project /path/to/server-binary
```

Both land an entry in `.claude/.mcp.json`. Confirm the entry references the env var, not the literal key.

**Claude UI (claude.ai / Desktop) — for non-technical setup:**
Customize → Connectors → "+" → Add custom connector → name it → paste the MCP URL → Connect → enter the API key → enable it in the chat's "+" menu. This is the path the source playbook documented; it's the right one when handing setup to someone who doesn't use the CLI.

### Step 5 — Introspect the tool surface

Before wiring the MCP into skills, list what it actually exposes. The Extrovert setup does this with `.claude/mcp/extrovert/introspect.mjs`; generically, open a fresh session and call the MCP's tools via `ToolSearch`, or read the server's `tools/list`. Catalog the tool names + input schemas.

### Step 6 — Integrate into skills

Add the MCP to the `mcps_used` frontmatter of any skill that calls it, and reference its tools in the skill body. If the MCP costs credits, add or follow a credits rule (see `apollo-credits.md` / `apify-credits.md` / `mobbin-credits.md` as the pattern) and state which operations are credit-bearing.

### Step 7 — Document + set a promotion review

Note the new MCP, its tier, and a 2–4-week promotion-review date in MEMORY.md (the Extrovert entry is the template). Re-evaluate at the review date: promote to tier A only if usage + auth stability clear the bar.

## Worked examples

- **Extrovert** (project-scope HTTP): `.claude/.mcp.json` entry → `https://mcp.goextrovert.com`, `Authorization: Bearer ${EXTROVERT_API_KEY}`, key in `.claude/apis/extrovert-api-key.txt`, introspection + seed via `.claude/mcp/extrovert/`. Added 2026-05-27, promotion review 2026-06-24.
- **Spider** (local stdio): `~/.cargo/bin/spider-mcp`, no key, project-scope, free local crawl in front of metered Firecrawl/Exa per `crawl-cost-discipline.md`.

## Anti-patterns

- Defaulting to `--scope user` for a new or single-client MCP. Project-scope or plugin first.
- Hard-coding an API key in `.claude/.mcp.json` instead of the `${SERVICE_API_KEY}` env var.
- Wiring an MCP into skills before introspecting its real tool surface.
- Skipping the promotion-review note, so a never-used MCP lingers always-on.

## Troubleshooting

| Issue | Fix |
|---|---|
| Auth expired mid-session | Run the MCP's OAuth/refresh helper (Extrovert: `oauth-helper.mjs`); kill the wedged child so Claude respawns |
| Tools don't appear | Fresh session re-reads `.claude/.mcp.json`; confirm env var loaded by `load-mcp-env.sh` |
| Slow session start | A wedged always-on MCP — demote to project-scope per `mcp-on-demand.md` |
| Key not exported | Filename must be `{service}-api-key.txt`; check kebab→snake mapping |

