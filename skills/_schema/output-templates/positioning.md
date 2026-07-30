---
knowledge_type: positioning
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 1 Strategy"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Positioning — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Defines the binary positioning strategy, primary anchor, differentiators, and one-line positioning statement. The strategic spine that messaging, content-strategy, landing-page-copy, and battlecards all consume.

## Required frontmatter fields

```yaml
client: {slug}
skill: positioning
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: positioning
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

- `binary_strategy` — the two-option choice (e.g., "category creator vs disruptor")
- `primary_anchor` — the dominant frame buyers use to evaluate
- `differentiators` — 3-5 named differentiators with proof
- `positioning_statement` — one-line "for [ICP] who [pain], [product] is [category] that [benefit]"

Optional: `secondary_anchor`, `market_focus`, `hero_recommendation`, `one_liners`.

## Required body sections (in order)

1. **Executive summary** — binary choice + primary anchor + positioning statement
2. **Binary strategy** — the two options and why this one wins (with evidence)
3. **Primary anchor** — the frame; how buyers think about this category
4. **Differentiators** — 3-5 with proof for each (customer evidence, product capability, GTM motion)
5. **Positioning statement** — the one-line for/who/is/that
6. **One-liners** — 3-5 alternative concise phrasings for different contexts (homepage, sales, ads)
7. **What we are NOT** — explicit anti-positioning to prevent drift

## Optional body sections

- **Secondary anchor** — when a sub-segment uses a different frame
- **Hero recommendation** — for landing-page hero block downstream
- **Category narrative** — when positioning includes category creation

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Strategy outputs are client deliverables requiring ≥60% verified.

Sections that require inline tags:
- Binary strategy (evidence for why option A beats option B: customer voice, competitor gaps, market signals)
- Differentiators (every differentiator backed by competitor-research finding or customer quote)

Positioning statement + one-liners are derived synthesis; tags inherit from the cited evidence.

## Render rules per target

### gdrive (Doc — canonical)

Per architecture decision 6:
- Inter, black, plain header, page-numbered footer, native TOC
- Binary strategy: render as centered callout with the two options + the chosen one bolded
- Positioning statement: render as bordered single-cell Drive native table (visual emphasis)

### gdrive (Slides) — for executive briefings

Convert positioning Doc to Slides: 1 cover, 1 binary choice, 1 primary anchor, 1 per differentiator, 1 positioning statement, 1 anti-positioning.

### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = positioning statement
- H1 = "{Client} — Positioning"
- Each H2 = toggle block (collapsed); differentiators toggle is heaviest

## Validation rules

1. All required frontmatter fields present
2. `binary_strategy` non-empty (must include both options + the choice)
3. `differentiators` array has 3-5 entries
4. `positioning_statement` follows for/who/is/that pattern
5. Anti-positioning section present (≥3 explicit "we are NOT" statements)
6. Differentiators section: each backed by ≥1 source (competitor or customer)

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
