---
knowledge_type: pricing-strategy
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 1 Strategy"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Pricing Strategy — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Pricing model + packaging tiers + value metric + competitive pricing analysis + WTP basis. Drives the pricing page, sales deck pricing slides, proposal scoping, and outbound pricing references.

Competitor pricing claims have an elevated verification threshold (≥90% verified) — fabricated competitor pricing is high-stakes. Always cite source URL + access date.

## Required frontmatter fields

```yaml
client: {slug}
skill: pricing-strategy
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: pricing-strategy
upstream_positioning: {path}
upstream_competitors: {path}
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

1. **Executive summary** — pricing model + value metric + headline tier prices + primary recommendation
2. **Pricing model** — one of: per-seat, consumption-based, tiered-flat, hybrid, usage, freemium (+ rationale)
3. **Value metric** — what the buyer pays for in their unit of value (seats / events / volume / outcomes)
4. **Tier structure** — each tier: name, price, included quotas, target persona, expected ARR
5. **Competitive pricing analysis** — 3-5 competitors: pricing model, anchor price, included quotas (table)
6. **Willingness-to-pay basis** — evidence supporting the price points (customer interviews, market research, baseline benchmarks)
7. **Discount + expansion policy** — when discounts apply, how expansion paths up the curve
8. **Recommendations** — concrete actions: launch tier X, kill tier Y, raise anchor by Z%

## Optional body sections

- **Pricing page recommendations** — how to present this on the website
- **Status quo alternative cost** — what buyers spend today on the do-nothing alternative
- **Negotiation playbook** — for sales team, when to flex vs hold

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Strategy outputs require ≥60% verified.

**Elevated threshold for competitive pricing analysis: ≥90% verified.** Every competitor tier price requires `[VERIFIED: pricing page URL, accessed YYYY-MM-DD]`. Use `[UNAVAILABLE: gated pricing — contact required]` rather than `[ESTIMATED]` when pricing is hidden.

Other sections requiring tags:
- Willingness-to-pay basis (every customer quote / market benchmark)
- Tier expected ARR (when claiming pipeline data: source from CRM)

Pricing model + tier structure recommendations are strategic synthesis; inherit from cited evidence.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Tier structure as Drive native table (rows: tiers; columns: price, quota, persona, expected ARR)
- Competitive pricing as Drive native table (rows: competitors; columns: model, anchor, included quotas)

### gdrive (Slides) — for executive review

Slides: 1 model, 1 per tier, 1 competitive comparison, 1 WTP evidence, 1 recommendations.

### gdrive (Sheet) — for ongoing competitive pricing tracking

Sheet variant: competitive pricing observatory (one row per competitor + tier, with first-observed and last-checked dates).

### notion (Page render)

- Overview = pricing model + value metric + headline tier
- H1 = "{Client} — Pricing Strategy"
- Each H2 = toggle block

## Validation rules

1. All required frontmatter fields present
2. `pricing_model` is one of the enum values
3. Tier structure: ≥1 tier (rarely meaningful below 2)
4. Competitive pricing analysis: ≥3 competitors
5. Every competitor pricing claim has `[VERIFIED]` source URL OR `[UNAVAILABLE: gated]`
6. WTP basis: ≥2 evidence sources

## Examples in the wild

- `projects/consulting/active/ClientCo/pricing/0426-pricing-strategy.md` (when conforming)
- `projects/consulting/active/ClientCo/pricing/0426-pricing-strategy-v2.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
