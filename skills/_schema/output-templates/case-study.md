---
knowledge_type: case-study
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Case Study — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Customer success story with metrics — before / change / after structure. Consumes transcript-insights + win-loss-analysis + messaging. Feeds landing-page-copy, lifecycle-campaign, sales-enablement-asset, aeo-content.

**Customer-specific claims (metrics, quotes, named outcomes) MUST be `[VERIFIED]`** — `[ESTIMATED]` is forbidden on customer data. This is the strictest validation rule of any execution-tier schema.

## Required frontmatter fields

```yaml
client: {slug}                       # the consulting client whose customer this is
skill: case-study
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: case-study
customer_name: {Customer Name}
customer_industry: {industry}
customer_size: {employees / ARR}
consent_status: verbal_unwritten | written_email | signed_release | published_already
upstream_transcripts: {path}
upstream_messaging: {path}
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

**Locking gate:** case-study cannot move to `status: locked` unless `consent_status` is at minimum `written_email`.

## Required body sections (in order — before / change / after)

1. **Customer snapshot** — name, role of champion, company size, industry, use case
2. **Before** — the world before the product (problems, pain, status quo cost)
3. **The change** — what they did (chose this product, implemented it, rolled it out)
4. **After** — the world after (metrics, qualitative outcomes, time to value)
5. **Customer quote** — verbatim, attributed (name + role + company)
6. **Key metrics** — table of before/after numbers (with source: customer-provided or estimated)
7. **Lessons / takeaways** — what made this work (transferable insight)

## Optional body sections

- **Implementation timeline** — when speed-to-value is part of the proof
- **Stack / integrations** — when ecosystem fit is part of the story
- **Quotes from other roles** — when a multi-stakeholder buy-in story strengthens it
- **Photo / video pointer** — when assets exist for the published version

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified.

**Customer-specific claims (metrics, quotes, named outcomes) MUST be `[VERIFIED]`.** No `[ESTIMATED]` or `[INFERRED]` allowed on customer data. Use `[UNAVAILABLE: customer didn't share]` rather than estimating.

Sections requiring inline tags:
- Customer snapshot (firmographics: customer-provided or public source)
- Before / After metrics (every number: customer-provided + customer-approved)
- Customer quote (Granola call ID + timestamp + customer email confirming usage)

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Key metrics as Drive native table (rows: metrics; columns: before, after, change %)
- Customer quote as block-quote (visual emphasis)

### gdrive (Slides) — for sales decks

Slides: 1 customer snapshot, 1 before, 1 change, 1 after (with metrics), 1 quote, 1 takeaways. Often embedded in larger sales-deck.

### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = customer + headline metric + one-line story
- H1 = "{Customer} — Case Study"
- Each H2 = toggle block; key metrics table inline (not toggled — hero element)

### Direct publish (channel-native)

Published case studies often go to client website (Framer/Webflow), aeo-content (citation source), and sales enablement (deck + one-pager). The Doc is source of truth.

## Validation rules

1. All required frontmatter fields present
2. `consent_status` is one of the enum values
3. **`status: locked` requires `consent_status: written_email` minimum** (hard gate)
4. Before / After / The change sections all present
5. Customer quote section has full attribution
6. Key metrics: ≥1 quantitative metric with `[VERIFIED]` source
7. Customer snapshot has full firmographics
8. **No `[ESTIMATED]` tags on customer data sections** — fail validation otherwise

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
