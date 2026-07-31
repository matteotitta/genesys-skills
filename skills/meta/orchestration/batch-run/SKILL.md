---
name: batch-run
version: '1.0'
last_updated: 2026-04-09
author: genesys-growth
description: 'Fan out any skill across N entities in parallel. Takes a skill name + entity list (products, competitors, pages,
  clients) + shared context, dispatches N subagents simultaneously via the Agent tool, then aggregates outputs into a single
  deliverable folder. Triggers: "/batch-run", "run X for all Y", "fan out [skill] across [entities]", "parallelize [skill]",
  "run [skill] for each of [list]". Upstream: skill-catalog (for validation). Downstream: any skill. NOT for sequential chains
  — use /website-build or workflow-design. NOT for one-off runs — invoke the skill directly.'
goal: Fan out any skill across N entities in parallel.
outcome: 'Fan out any skill across N entities in parallel. Takes a skill name + entity list (products, competitors, pages,
  clients) + shared context, dispatches N subagents simultaneously via the Agent tool, then aggregates outputs into a single
  deliverable folder. Triggers: "/batch-run", "run X for all...'
primitive: meta
sub_primitive: orchestration
ontology_type: runbook
review_gate: 0
inputs:
  required:
  - skill-catalog
  recommended: []
- type: batch-execution-report
  feeds_into:
  - orchestrator
depends_on:
- skill-catalog
- orchestrator
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
paths:.claude/skills/**
---

# /batch-run — Fan Out Any Skill Across N Entities

Dispatches N parallel subagents to run the same skill across a list of entities, with shared upstream context injected into each run.

---

## Claude Code Triggers

**Invoke when user says:**
- "/batch-run <skill> --entities 'a,b,c'"
- "Run product-messaging for all 8 ClientCo products"
- "Fan out competitor-research across these 5 competitors"
- "Parallelize landing-page-copy across home, pricing, about"
- "Run [skill] for each of [list]"

**Do NOT invoke when:**
- User wants a single skill run (invoke the skill directly)
- User wants a sequential chain (use `/website-build` or workflow-design)
- Entities have cross-dependencies (shared state breaks parallelization)

---

## Input Format

```
/batch-run <skill-name> \
  --entities "entity1, entity2, entity3" \
  [--client <slug>] \
  [--context <path-to-upstream-output>] \
  [--output-dir <path>] \
  [--max-parallel <N>]
```

**Required:**
- `<skill-name>` — must exist in skill-catalog (e.g., `product-messaging`, `competitor-research`)
- `--entities` — comma-separated list of entity names

**Optional:**
- `--client` — client slug for folder routing (e.g., `ClientCo`, `ClientCo`)
- `--context` — path to upstream deliverable that provides shared context (e.g., positioning doc)
- `--output-dir` — override default output location
- `--max-parallel` — cap concurrent agents (default: 5, max: 10)

---

## Execution Workflow

### Phase 1: Validate inputs

1. Check `<skill-name>` exists in `.claude/skills/` — fail fast if unknown
2. Read the skill's SKILL.md to extract:
   - Required dependencies (upstream skills)
   - Output type + default location
   - Review gate level
3. Verify `--context` file exists if provided
4. Resolve `--client` slug against `.claude/rules/consulting-clients.md` folder structure

### Phase 2: Build shared context package

For each subagent, the context package contains:
- **Skill SKILL.md** — the full skill instructions
- **Shared upstream context** — from `--context` flag or auto-detected (e.g., positioning.md in client folder)
- **Entity-specific input** — the current entity name + any entity-specific context in the client folder (e.g., `projects/consulting/ClientCo/docs/treasury.md`)
- **Client CLAUDE.md** — voice, brand, quality bar

### Phase 3: Dispatch parallel subagents

Use the Agent tool with `subagent_type: general-purpose` (or matching specialist if one exists, e.g., `product-marketer` for messaging skills).

**Batching:** if entity count > `--max-parallel`, process in waves. Wait for wave N to complete before starting wave N+1.

**Agent prompt template:**
```
You are running the {skill-name} skill for entity: {entity}.

SKILL INSTRUCTIONS:
{contents of SKILL.md}

SHARED CONTEXT:
{contents of upstream context}

ENTITY CONTEXT:
{any entity-specific inputs from client folder}

CLIENT VOICE:
{client CLAUDE.md voice/brand rules}

Produce the output per the skill's format. Save to: {output-dir}/{entity}.md
Return a 3-line summary: entity, output path, key insight.
```

### Phase 4: Aggregate results

Collect all subagent summaries into a batch-execution-report:

```markdown
# Batch Run Report — {skill-name} × {N} entities

**Date:** {timestamp}
**Client:** {client}
**Shared context:** {context-path}

## Results

| Entity | Output | Key insight |
|--------|--------|-------------|
| {entity} | [{path}]({path}) | {1-line summary} |

## Aggregate insights
- Cross-entity patterns worth noting
- Entities that failed or need re-runs

## Next steps
- Review individual outputs at review gate {N}
- Aggregate into {next-skill} if applicable
```

### Phase 5: Surface failures

If any subagent failed (timeout, error, empty output):
- Mark in the report with a ⚠ flag
- Offer to re-run just the failed entities: `/batch-run {skill} --entities "failed1,failed2" --retry`

---

## Example invocations

**ClientCo product messaging fan-out (the pattern that triggered this skill):**
```
/batch-run product-messaging \
  --entities "treasury, payroll, bookkeeping, team-cards, business-account, invoice-pay, reporting, integrations" \
  --client ClientCo \
  --context projects/consulting/active/ClientCo/strategy/0426-positioning.md
```

**Competitor research parallel:**
```
/batch-run competitor-research \
  --entities "brex, ramp, mercury, rho, moss" \
  --client ClientCo \
  --max-parallel 3
```

**Landing page copy across pages:**
```
/batch-run landing-page-copy \
  --entities "home, pricing, about, treasury, payroll" \
  --client ClientCo \
  --context projects/consulting/active/ClientCo/strategy/0426-product-messaging.md
```

---

## Edge cases

- **Entity overlap:** If two entities have the same name (e.g., two "payroll" files in different subfolders), fail with an explicit path disambiguation error.
- **Rate limits:** If hitting Anthropic rate limits, reduce `--max-parallel` to 2-3 and add 30s delay between waves.
- **Skill with required MCP data:** If the skill needs fresh MCP pulls (e.g., company-context), each subagent pulls independently — context isolation is intentional, don't share raw MCP responses.
- **Cross-entity dependencies:** If entities must share generated data (e.g., running positioning per-segment where each informs the next), use workflow-design instead — this skill is for truly independent fan-outs.

---

## Notes

- Check the skill-catalog first to verify the target skill exists and understand its output format
- Parallel fan-out is a read-heavy operation; don't use for skills that mutate shared state (e.g., skill-catalog updates)
- The batch-execution-report is the single source of truth for the run — link to it from any downstream aggregation
- For task-tracker integration: each entity can become a Linear task with the subagent results posted as comments
