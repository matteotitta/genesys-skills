---
knowledge_type: sales-enablement-asset
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Sales Enablement Asset — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Polymorphic execution-tier output covering 8 distinct asset formats sales reps consume: talk track, demo script, sales deck, one-pager, objection handler, discovery questions, ROI calculator brief, pricing proposal template. Body structure varies by `asset_format`.

## Required frontmatter fields

```yaml
client: {slug}
skill: {sales-enablement-index | demo-script | sales-deck | one-pager | battlecards}
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: sales-enablement-asset
asset_format: talk_track | demo_script | sales_deck | one_pager | objection_handler | discovery_questions | roi_calculator_brief | pricing_proposal_template
target_audience: {persona — e.g., "Champion", "Economic Buyer", "Procurement"}
target_use_moment: {when in cycle — e.g., "first call", "demo", "negotiation", "close"}
upstream_positioning: {path}
upstream_messaging: {path}
upstream_competitors: {path}             # only when competitive context matters
upstream_win_loss: {path}                # only when objection patterns matter
upstream_brand_kit: {path}               # for sales_deck + one_pager (visual)
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (vary by asset_format)

### talk_track
1. Opening — hook / framing / first 60 sec
2. Discovery — questions to ask + listening cues
3. Pitch — Say / Sharpener / Don't say (3-column structure)
4. Objection handling — top 3-5 with response patterns
5. Close — concrete next step

### demo_script
1. Setup — what's been established before demo, what they expect
2. Demo flow — minute-by-minute with showcase moments + check-ins
3. Wow moments — 2-3 specific features to land
4. Recovery paths — when demo derails (questions, technical, objections)
5. Wrap — summary + clear next step

### sales_deck
1. Cover (title + ICP framing)
2. Status quo problem
3. Why now (market shift)
4. Solution introduction
5. How it works
6. Differentiation (per messaging)
7. Proof (case-studies + metrics)
8. Pricing teaser (or full)
9. Clear next step

### one_pager
1. Headline + sub-headline (per messaging)
2. Problem (3 bullets)
3. Solution (3 bullets)
4. Proof (logos + metric strip)
5. CTA + contact

### objection_handler
1. Top 5-10 objections (by frequency from win-loss-analysis)
2. Per objection: surface form (what they actually say), root cause, response, evidence

### discovery_questions
1. Pre-call research checklist
2. Question bank organized by funnel stage (pain, impact, decision criteria, success criteria)
3. Listening cues (what answers tell us about fit)

### roi_calculator_brief
1. ROI logic (inputs → calculation → outputs)
2. Default assumptions (defensible defaults with sources)
3. Sensitivity analysis (which input moves the result most)
4. Output framing (how to present to the buyer)

### pricing_proposal_template
1. Context summary (per consulting-clients.md context formula)
2. Scope of work
3. Investment + payment terms
4. Timeline + milestones
5. Success criteria + how we measure
6. Exclusions / out-of-scope

## Optional body sections (cross-cutting)

- **Internal coach notes** — for new reps, common pitfalls
- **Variant by ICP** — when same asset has buyer-specific tweaks
- **Update log** — version history when asset gets refreshed

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified.

**Inline tags for talk-track + objection-handler + discovery-questions** (audit-grade — reps need to defend claims live).

**HTML comment tags** for sales_deck + one_pager + roi_calculator_brief + pricing_proposal_template (customer-facing — comments stripped at publish).

Sections requiring tags (across all formats):
- Proof points (every metric: source + date)
- Competitive claims (every "we beat X because" — source from competitor-intel)
- Customer quotes (full attribution)

## Render rules per target

### gdrive (Doc — canonical for talk_track, demo_script, objection_handler, discovery_questions, roi_calculator_brief, pricing_proposal_template)

- Inter, black, plain header, page-numbered footer, native TOC
- Talk track + demo script: Say / Sharpener / Don't-say sections as Drive native 3-column tables

### gdrive (Slides — canonical for sales_deck)

When `asset_format: sales_deck`, render as Slides directly (not Doc → Slides). Slide template per architecture decision 6 — TBD specific Slides rules in Phase C build of `slides.mjs` adapter.

### gdrive (Sheet — for roi_calculator_brief companion)

When `asset_format: roi_calculator_brief`, an interactive Sheet companion may exist alongside the Doc. Sheet is the calculator; Doc is the brief.

### notion (Page render)

- Overview = asset_format + target_audience + target_use_moment
- H1 = "{Client} — {Asset name}"
- Each H2 = toggle block

## Validation rules

1. All required frontmatter fields present
2. `asset_format` is one of the 8 enum values
3. Required body sections per asset_format are all present
4. talk_track: Say / Sharpener / Don't-say structure complete
5. sales_deck: ≥9 slides per anatomy
6. one_pager: ≤1 page when rendered (validate by section count + word count)
7. roi_calculator_brief: assumptions documented with sources
8. pricing_proposal_template: investment section uses context formula per consulting-clients.md

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
