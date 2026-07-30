---
knowledge_type: content-strategy
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 1 Strategy"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Content Strategy — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Multi-quarter content roadmap — content clusters/pillars, channel mix, format priorities, monthly phases, KPIs. The plan that drives content-ops weekly cycles + per-piece content outputs.

Depends on locked messaging + ICP + competitor-intel.

## Required frontmatter fields

```yaml
client: {slug}
skill: content-strategy
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: content-strategy
roadmap_horizon_days: 90              # typical: 90 or 365
upstream_messaging: {path}
upstream_icp: {path}
sources_count:
  verified: {n}
  inferred: {n}
  estimated: {n}
  unavailable: {n}
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order)

1. **Executive summary** — strategic thesis + 3-5 content clusters + primary channel
2. **Content clusters / pillars** — 3-7 themes with rationale + ICP-pain mapping
3. **Channel mix** — channels chosen + cadence per channel (LinkedIn daily, blog weekly, etc.)
4. **Format priorities** — which formats per channel (long-form, infographic, video, carousel)
5. **Monthly phases** — month-by-month roadmap with cluster focus + flagship pieces
6. **KPIs and targets** — measurable goals per channel (impressions, clicks, MQLs, citations)
7. **Repurposing plan** — how flagship content cascades into derivative formats
8. **Editorial calendar pointer** — link to the active calendar (a separate working artifact)

## Optional body sections

- **Channel playbooks** — per-channel detailed playbook (cadence, voice, examples)
- **AEO cluster overlay** — when content-strategy includes AEO citation targeting
- **Competitor content gap notes** — where competitors over-publish vs under-publish

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Strategy outputs are client deliverables requiring ≥60% verified.

Sections that require inline tags:
- KPIs and targets (every benchmark: source + date — own data, industry baseline, or estimated with reasoning)
- Channel mix (channel choice grounded in ICP-research or content-audit findings)
- Repurposing plan (when claiming workflow capacity: source from content-ops setup)

Strategic theses + cluster choices are derived; tags inherit from cited evidence.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Monthly phases as Drive native table (rows: months; columns: cluster, flagship, channels active)
- KPIs as Drive native table (rows: KPI; columns: baseline, target, deadline, owner)

### gdrive (Slides) — for stakeholder review

Convert to Slides: 1 thesis, 1 per cluster, 1 channel mix, 1 monthly phases, 1 KPIs.

### gdrive (Sheet) — for editorial calendar companion

Sheet variant: editorial calendar (one row per planned piece, columns: date, channel, cluster, format, owner, status).

### notion (Page render)

- Overview = strategic thesis
- H1 = "{Client} — Content Strategy ({Horizon})"
- Each H2 = toggle block; clusters and monthly phases are heaviest

## Validation rules

1. All required frontmatter fields present
2. `upstream_messaging` + `upstream_icp` resolve to existing locked outputs
3. `roadmap_horizon_days` is ≥30 (1 month minimum for meaningful planning)
4. Content clusters: 3-7 entries
5. Channel mix: ≥2 channels chosen (rarely makes sense to bet single-channel)
6. KPIs: ≥3 measurable targets with deadlines

## Examples in the wild

- `projects/consulting/active/pivot/content/strategy/0326-content-strategy-aeo-v2.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
