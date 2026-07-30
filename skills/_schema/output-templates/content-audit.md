---
knowledge_type: content-audit
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Content Audit — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Inventories existing content (blog, landing pages, social, video, gated assets), grades performance, identifies gaps against ICP + funnel + AEO opportunities. Drives content-strategy and content-ops decisions.

## Required frontmatter fields

```yaml
client: {slug}
skill: content-audit
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: content-audit
audit_scope: {channels-or-domain}    # e.g., "blog only" | "full domain" | "blog + LinkedIn"
content_pieces_analyzed: {n}
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

1. **Executive summary** — total pieces, top performers, biggest gaps, recommendations
2. **Inventory** — every piece: URL, title, channel, format, publish date, performance metrics (table)
3. **Performance distribution** — top 20% / middle 60% / bottom 20% breakdown
4. **Gap analysis** — missing pillars vs ICP pain points, missing funnel stages, missing AEO clusters
5. **Quality assessment** — voice consistency, SEO health, AEO readiness scores
6. **Recommendations** — keep / refresh / consolidate / kill / create-new (per piece or theme)

## Optional body sections

- **Channel breakdown** — per-channel metrics + observations
- **Competitive content landscape** — what competitors publish that this client doesn't
- **Messaging alignment matrix** — which pieces align with locked messaging vs drift

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Sections that require inline tags:
- Inventory (each piece's metrics: source GSC / GTM / analytics + access date)
- Performance distribution (cuts grounded in inventory data)
- Gap analysis when claiming "competitor publishes X but we don't" (cite competitor URL)

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Inventory as Drive native table; large inventories may render as a linked Sheet companion

### gdrive (Slides) — N/A
### gdrive (Sheet) — for inventory > 50 pieces

Sheet variant: one row per piece with columns matching inventory fields. Doc body remains the synthesis; Sheet is the data layer.

### notion (Page render)

- Overview = executive summary
- H1 = "{Client} — Content Audit ({YYYY-MM})"
- Inventory as Notion native database when piece count ≤ 50; link to Sheet otherwise
- Each H2 = toggle block

## Validation rules

1. All required frontmatter fields present
2. `content_pieces_analyzed` matches inventory row count
3. Inventory has all required columns per piece
4. Gap analysis section present + ≥3 named gaps
5. Recommendations section: every piece in inventory has a verdict (keep/refresh/consolidate/kill/create-new) — no orphans
6. Performance metrics tagged with source (GSC / GA / GTM)

## Examples in the wild

- `projects/consulting/active/pivot/content/audit/0326-content-audit.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
