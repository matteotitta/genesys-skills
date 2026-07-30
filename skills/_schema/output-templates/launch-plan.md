---
knowledge_type: launch-plan
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Launch Plan — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Cross-functional launch orchestration plan — phases, asset inventory, key moments, role assignments, success metrics, risk register. Drives launch execution across product marketing, content, sales, paid, lifecycle.

## Required frontmatter fields

```yaml
client: {slug}
skill: product-launch
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: launch-plan
launch_name: {Launch}
launch_date: {YYYY-MM-DD}
phase_count: {n}                     # typical 4 (pre-launch, soft-launch, GA, post-launch)
upstream_messaging: {path}
upstream_positioning: {path}
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order)

1. **Executive summary** — what's launching, when, success definition
2. **Phases** — phase-by-phase breakdown with start/end dates, primary activities, gate criteria
3. **Asset inventory** — every artifact needed: blog post, LP, deck, email, ad creative, demo video (per phase)
4. **Role assignments** — RACI-style table: who owns what, who reviews, who's informed
5. **Key moments** — anchor dates (announcement, GA, customer event, partner co-launch)
6. **Success metrics** — quantitative targets with baseline + deadline (per phase + overall)
7. **Risk register** — what could derail (with mitigation) — competitive, capacity, technical, legal
8. **Comms plan** — internal + external comms cadence per phase

## Optional body sections

- **Customer beta program** — when launch includes pre-GA customer testing
- **Partner co-launch** — when partners are part of the launch motion
- **Press / analyst briefings** — when seeking press or analyst pickup
- **Post-launch retrospective plan** — how the team evaluates after launch

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified.

**Inline tags used** — launch plans are working docs cross-functional teams interrogate.

Sections requiring tags:
- Asset inventory (every asset's status: draft / review / locked / shipped)
- Success metrics (every baseline + target: source — own data, market benchmark, or estimated with reasoning)
- Risk register (every risk: probability + impact + mitigation, with evidence where applicable)

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Phases as Drive native table (rows: phases; columns: dates, activities, owner, gate)
- Asset inventory as Drive native table
- RACI as Drive native table

### gdrive (Slides) — for stakeholder briefings (often used)

Slides: 1 launch summary, 1 timeline, 1 per phase, 1 success metrics, 1 risks, 1 comms plan.

### gdrive (Sheet) — for asset tracking

Sheet variant: asset inventory as live tracker with status updates per asset (rows: assets; columns: phase, owner, status, target date, actual date, notes).

### notion (Page render)

- Overview = launch summary
- H1 = "{Client} — {launch_name} Launch Plan"
- Each H2 = toggle block (collapsed); phases + asset inventory toggles heaviest

## Validation rules

1. All required frontmatter fields present
2. `phase_count` ≥1 (rarely below 2 in real launches)
3. Phases section has ≥`phase_count` entries with dates + gates
4. Asset inventory: every asset has owner + target date + status
5. Role assignments: every named asset has a clear owner
6. Success metrics: ≥3 measurable targets with deadlines
7. Risk register: ≥3 risks with mitigation

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
