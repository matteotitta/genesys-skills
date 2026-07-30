---
knowledge_type: competitor-intel
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Competitor Intel — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Captures one competitor's profile across 11 strategic dimensions, plus an aggregate-insights variant when multiple competitors are analyzed together. Drives positioning, messaging, battlecards, and sales enablement.

## Required frontmatter fields

```yaml
client: {slug}
skill: competitor-research
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: competitor-intel
sources_count:
  verified: {n}
  inferred: {n}
  estimated: {n}
  unavailable: {n}
locked_by: null
locked_date: null
review_gate_passed: null
```

Plus type-specific required fields per ontology.md:

- `competitor_name` — official entity name
- `dimensions` — object with all 11 dimensions filled (see body sections)
- `executive_summary` — 3-5 sentences distilling threat + differentiation
- `threat_level` — one of: PRIMARY, ENTERPRISE, DIRECT, STEALTH, LOW, DEFUNCT

Optional: `data_gaps`, `comparison_matrix` (when comparing vs client), `aggregate_insights` (only on aggregate variant).

## Required body sections (in order)

1. **Executive summary** — threat level + headline differentiator + recommended response
2. **Company snapshot** — founded, HQ, funding, employee count, customer logos (table)
3. **Product + positioning** — what they sell, how they describe it, anchor metaphors
4. **Pricing + packaging** — model, tiers, anchor price, free tier
5. **Target customer** — ICP they aim at, segments served
6. **Go-to-market motion** — sales-led / product-led / community-led; channels
7. **Marketing presence** — content cadence, channels, voice attributes
8. **Differentiation claims** — what they say makes them better
9. **Customer voice** — review themes, common praise, common complaints
10. **Recent moves** — funding, launches, hires, partnerships (last 6 months)
11. **Threats + gaps** — where they could win, where they leave room

## Optional body sections

- **Comparison matrix** — when output is per-competitor vs client (Drive native table)
- **Aggregate insights** — only on aggregate variant: themes across all competitors

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Sections that require inline tags:
- Pricing + packaging (every tier price)
- Target customer (segment claims)
- Customer voice (every quote: source + url + date)
- Recent moves (every signal)

Narrative sections (executive summary, threats + gaps) inherit confidence from cited facts.

## Render rules per target

### gdrive (Doc — canonical)

Per architecture decision 6:
- Inter, black, plain header, page-numbered footer, native TOC
- Company snapshot + pricing tiers as Drive native tables
- Comparison matrix as Drive native table when present

### gdrive (Slides) — N/A
### gdrive (Sheet) — for aggregate variant only

When aggregate-insights output covers 5+ competitors, render the comparison matrix as a Sheet with one column per competitor.

### notion (Page render)

- Overview paragraph = executive summary's first 2 sentences
- H1 = "{Competitor} — Competitor Intel"
- Each H2 section = toggle block (collapsed)
- Sources nested per section

## Validation rules

1. All required frontmatter fields present
2. `ontology_type` equals `competitor-intel`
3. `threat_level` is one of the 6 enum values
4. All 11 dimensions present in body (sections 2-11 + executive summary)
5. ≥3 entries in customer voice section, each with source + url
6. Pricing section: each tier has `[VERIFIED]` or marked `[UNAVAILABLE]`

## Examples in the wild

- `projects/consulting/active/ClientCo/competitors/0326-classy.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
