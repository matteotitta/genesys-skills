---
knowledge_type: messaging
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 1 Strategy"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Messaging — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

The 10-component messaging library — value propositions, key differentiators, taglines, CTA variants, proof points, status quo alternatives. The library every downstream copy output (landing-page-copy, ads, outreach, sales-deck) reads from.

Depends on locked positioning per `orchestration-patterns.md` § Orchestration mechanics → Lock-down state.

## Required frontmatter fields

```yaml
client: {slug}
skill: messaging
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: messaging
upstream_positioning: {path}        # path to locked positioning output
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

- `positioning_statement` — copied from upstream positioning (locked)
- `value_propositions` — primary + secondary value props
- `key_differentiators` — 3-5 with proof points

Optional: `taglines`, `cta_variants`, `proof_points`, `messaging_hierarchy`, `status_quo_alternatives`.

## Required body sections (in order)

1. **Executive summary** — positioning statement + 3 primary value props
2. **Value propositions** — primary (1) + secondary (2-3); each with target audience + outcome
3. **Key differentiators** — 3-5 with proof (customer quotes, product capabilities, metrics)
4. **Status quo alternatives** — what buyers do today + why it's broken (3-5 options)
5. **Taglines** — 3-5 variants for different contexts (homepage, ads, signature)
6. **CTA variants** — 5-10 calls-to-action by funnel stage (TOFU/MOFU/BOFU)
7. **Proof points** — customer logos, metrics, case-study pointers
8. **Messaging hierarchy** — which message leads on which page/channel/persona

## Optional body sections

- **Voice tweaks per channel** — how messaging shifts for LinkedIn vs ads vs sales
- **Anti-messages** — what we don't say (banned buzzwords, weak claims)
- **Channel-specific message map** — each channel's lead message

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Strategy outputs are client deliverables requiring ≥60% verified.

Sections that require inline tags:
- Value propositions (each backed by ICP pain or customer voice quote)
- Key differentiators (each grounded in competitor-research or customer quote)
- Proof points (every metric: source + date; every customer logo: permission status)
- Status quo alternatives (each grounded in customer/buyer evidence)

Taglines + CTA variants are derived; inherit from cited evidence.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Value propositions as Drive native table (3 columns: prop / audience / outcome)
- Messaging hierarchy as Drive native table (rows: page/channel; columns: lead message, secondary)

### gdrive (Slides) — for sales enablement spinoff

When sales team wants a deck, render: 1 positioning, 1 per value prop, 1 per differentiator, 1 proof points.

### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = positioning statement + 3 primary value props
- H1 = "{Client} — Messaging"
- Each H2 = toggle block; CTA variants toggle is heaviest

## Validation rules

1. All required frontmatter fields present
2. `upstream_positioning` resolves to existing locked positioning output
3. `value_propositions` has ≥1 primary + ≥2 secondary
4. `key_differentiators` has 3-5 entries
5. Status quo alternatives: ≥3 options
6. Taglines: ≥3 variants
7. CTA variants: ≥5 across funnel stages
8. Every proof point metric has `[VERIFIED]` source

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
