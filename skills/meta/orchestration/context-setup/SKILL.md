---
name: context-setup
version: '1.0'
last_updated: 2026-07-23
author: genesys-growth
description: 'Orchestrates a Lane-3 client context engagement end to end — scaffolds the Pattern A client folder, drives the
  canonical context spine as a locked, dependency-gated sequence, then generates the per-client context repo (context/ + workspace/
  + skills/ + agents/ + commands/ +.claude-plugin/) modelled on ClientCo-marketing. Start here when standing up a paid "build
  your context layer" engagement — the £9-10.8K/mo AI-transformation build (ClientCo live, ClientCo in-flight). Upstream:
  /discovery. Drives the spine skills (company-context → competitor-research →... → product-messaging) and emits a repo ready
  for its own GitHub remote. Triggers: "build the context OS for {client}", "stand up {client}''s context repo", "run the Lane-3
  context build". NOT for folder-only scaffolding (use /new-client), NOT for packaging existing skills into a plugin bundle
  (use /plugin-scaffold), NOT for producing a single spine artifact (run that skill directly).'
goal: Orchestrate a client context engagement — scaffold, drive the locked context spine, and generate the per-client context repo.
outcome: A scaffolded Pattern A client folder, a locked dependency-gated context spine (each output status-locked, owner-named, versioned), and a generated per-client context repo ready for its own GitHub remote — the reusable Lane-3 build the client's team runs against.
primitive: meta
sub_primitive: orchestration
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
triggers:
  slash_commands:
  - /context-setup
  natural_language:
  - build the context OS for {client}
  - stand up the context repo for {client}
  - run the Lane-3 context build
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
disable-model-invocation: false
---

# /context-setup — Orchestrate a client context engagement

**Situation.** Genesys sells "build your context layer" as a Lane-3 engagement — the £9-10.8K/mo AI-transformation build. It's live at ClientCo and in-flight at ClientCo.

**Complication.** The mechanics are ad-hoc. `/new-client` scaffolds Pattern A folders and *prompts* the spine chain but doesn't drive it. Nothing locks the sequence, so a downstream skill can run before its upstream is canonical. And the per-client context repo — the thing the client's team actually runs against, like `ClientCo-marketing` — is hand-built each time.

**Question.** What makes this build repeatable and sellable instead of a bespoke rebuild every engagement?

**Answer.** This skill. It does two jobs, in order: (1) drive the context spine as a **locked, dependency-gated sequence** — build the brain before any engine — and (2) **generate the per-client context repo** from the locked spine, ready for its own GitHub remote.

This is an orchestration runbook — it coordinates other skills and emits a repo. It does not itself produce a spine artifact; each spine skill does that.

The methodology adapts patterns surfaced in the `/steal` analysis at [`../../../../discovery/0726-jacob-dietle-context-os-steal-analysis.md`](../../../../discovery/0726-jacob-dietle-context-os-steal-analysis.md) (cite-only — the source author is a tracked Genesys competitor; adapt the ideas, never reproduce his brand terms).

---

## When to run

**Invoke when:**
- "build the context OS for {client}"
- "stand up {client}'s context repo"
- "run the Lane-3 context build for {client}"
- starting a paid AI-transformation engagement where the deliverable is a client's owned context system

**Do NOT invoke when:**
- The user only wants the empty folder scaffold → use `/new-client`.
- The user wants existing global skills packaged into a distributable bundle → use `/plugin-scaffold`.
- The user wants a single spine artifact (just positioning, just messaging) → run that skill directly.

---

## Composes with (don't duplicate)

- **Upstream: `/discovery`** (`primitives/clients/discovery`) — the discovery brief feeds the engagement scope this build runs against. Run it first; this skill assumes discovery is done.
- **After scaffold: `/client-onboarding`** — the human-facing onboarding steps run alongside this build's technical scaffold.
- **Drives: the spine skills** — `company-context` through `product-messaging` (see). This skill sequences and locks them; it does not reimplement them.
- **Reuses: `/plugin-scaffold`** ([`../../infra/plugin-scaffold/SKILL.md`](../../infra/plugin-scaffold/SKILL.md)) for the repo's `.claude-plugin/` manifest + skill symlink mechanics (see).

---

## Inputs

| Input | Required? | Source |
|-------|-----------|--------|
| Client name (kebab-case) | required | user |
| Discovery brief | recommended | `/discovery` output |
| Engagement scope + named owners per domain | recommended | contract / discovery |
| Transcripts (sales calls, interviews) | recommended | client — the highest-value buildtime seed (see Phase 3) |

If discovery hasn't run, name it and offer to run it first.

---

## The build — seven phases, in order

### Phase 1 — Scaffold

Invoke `/new-client` ([`../../../../commands/new-client.md`](../../../../commands/new-client.md)) to create the Pattern A structure (PMM core folders, `goals/`, `latest.md`, `history.md`, CLAUDE.md pointer table). Do not restate that template here — call the command.

### Phase 2 — Drive the spine (locked, dependency-gated)

Run the canonical new-client spine **in order**, gating each step on the prior carrying `status: locked`:

`company-context → competitor-research → icp-research → icp-behavioural → tov-guidelines → brand-kit → expert-pov → positioning → product-messaging → brand-context-sync → [execution fan-out]`

The authoritative ordering + dependency rationale live in [`../../../../rules/ontology.md`](../../../../rules/ontology.md)→ "New client (full engagement)". Do not re-derive it here. The gating mechanism is the sequential-pipeline + lock-down state in [`../../../../rules/orchestration-patterns.md`](../../../../rules/orchestration-patterns.md) (Pattern 1 +→ Lock-down state): step N does not start until step N-1 is `status: locked`.

After each step, set the lock-down frontmatter on its output (`status: locked` / `locked_by: {named owner}` / `lock_version: N`). A `lock_version` bump is a **release** — "ready for the team" is a decision an owner makes, not a save (steal I5). Mechanics + the exact frontmatter block + the rubric-as-scaffolding note (steal B, for any scoring step in the build) are in the premium reference.

### Phase 3 — Layer buildtime vs runtime

Label every artifact as one of two lifecycles (steal I1):
- **Buildtime** — the locked spine. Collective context built ahead, owned and versioned. This is what Phase 2 produces.
- **Runtime** — live pulls from the client's system of record (CRM, analytics, DB) via MCP. Fetched fresh, not owned, not versioned.

Build the brain before the engines — lock the buildtime spine before wiring any client-facing engine or asset (steal D). Transcripts are the highest-value buildtime seed: a CRM says *what* happened, transcripts say *why*, so seed the spine from calls and interviews first. Detail in the premium reference.

### Phase 4 — Structure knowledge packages (multi-suite clients)

For a multi-suite or multi-brand client (ClientCo's 4 product lines; ClientCo' multi-brand), structure `workspace/` as **owned packages per domain** rather than one flat pile (steal I4). Each package carries a dependency note (what it reads from) and a named owner. Single-product clients skip this — one package is enough. Package template in the premium reference.

### Phase 5 — Wire citation traceability

Every spine output carries `[VERIFIED: source]` tags per [`../../../../rules/ontology.md`](../../../../rules/ontology.md) + [`../../../../rules/evidence-bound-outputs.md`](../../../../rules/evidence-bound-outputs.md) (steal I2). For regulated clients (ClientCo / FCA), traceable-and-defensible AI output is the differentiator — every claim links to a source.

When the engagement ships AI-assisted content, attach an **Evidence Map** — a claim → source → type appendix as proof-of-work (steal A). Scope it per [`../../../../rules/output-simplicity.md`](../../../../rules/output-simplicity.md) §9: internal or client-team layer only (appendix / collapsible), **never** on customer-facing content, where a sources block is itself a robot tell. Detail in the premium reference.

### Phase 6 — Note runtime access technique

For wiring the client's system of record at runtime, the access technique is **agent-writes-code-to-query** — the agent discovers the schema and writes a query against it, instead of relying on a fixed set of predefined tools (steal E). Note this in the repo's `docs/MCP-CONNECTIONS.md`; it is a runtime-layer design choice, not a buildtime deliverable.

### Phase 7 — Generate the per-client context repo

Emit the `ClientCo-marketing`-style layout at `projects/consulting/active/{client}/workflows/{client}-marketing/`:

```
{client}-marketing/
├── README.md · STRUCTURE.md · settings.json ·.gitignore
├──.claude-plugin/plugin.json
├── context/ — condensed snapshots of the locked spine (fast skill-context loads)
├── workspace/ — canonical PMM-core artifacts (the shared brain; Phase 4 packages)
├── skills/ — client-wired SKILL.md (symlinks/copies of global skills)
├── agents/ — role-agents + specialists
├── commands/ — slash commands
└── docs/ — README, QUICKSTART, INSTALL, SKILL-INDEX, MCP-CONNECTIONS
```

Compose with `/plugin-scaffold` for the `.claude-plugin/plugin.json` + symlink mechanics. **Document** the dual-push routing (own GitHub remote + `git subtree`) per root CLAUDE.md— Push Routing Rules" — **do not create the remote or push.** Full layout spec, `context/` vs `workspace/` split, and the routing doc are in the premium reference.

---

## Self-roast (run before ship)

- **Gating held:** no spine step ran before its upstream was `status: locked`. If a step jumped the gate, flag it.
- **Owners named:** every locked output has a real `locked_by` owner, not a placeholder.
- **Buildtime before engines:** no client-facing engine or asset was wired before the buildtime spine locked.
- **Citations intact:** spine outputs carry `[VERIFIED:]` tags; any Evidence Map is internal/client-team only, never customer-facing.
- **No push side-effects:** the repo was generated and the dual-push routing documented — but no remote was created and nothing was pushed.
- **Cite-only respected:** no competitor brand terms reproduced; the methodology cites the discovery file.
- Voice + seven-tenet gate ([`../../../../rules/output-tenets.md`](../../../../rules/output-tenets.md)) passed.

---

