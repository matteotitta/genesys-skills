---
knowledge_type: landing-page-copy
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Landing Page Copy — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Section-by-section copy for a landing page (homepage, product page, feature page, pricing page). Consumes locked positioning + messaging + ICP + brand-kit + tov-guidelines.

## Required frontmatter fields

```yaml
client: {slug}
skill: website-copy                  # renamed from landing-page-copy in Phase 2
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: landing-page-copy
page_type: homepage | product | feature | pricing | comparison | use-case
target_url: {URL or path}
upstream_messaging: {path}
upstream_icp: {path}
brand_kit_source: {path}             # DESIGN.md path per design-production.md
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order — canonical landing page anatomy)

1. **Page summary** — purpose, target persona, primary CTA
2. **Hero block** — H1 (≤100 chars), sub-headline (≤150 chars), primary CTA, secondary CTA, hero visual brief
3. **Social proof block** — logos / metrics / testimonial (1-3 elements)
4. **Problem statement block** — what's broken in the status quo (paired with ICP pain)
5. **Solution overview block** — how this product addresses it (anchored in messaging primary value prop)
6. **Feature blocks** — 3-5 feature/benefit pairs (each with brief, headline, body, optional visual brief)
7. **Comparison block (optional)** — vs competitors or vs status quo
8. **Testimonial / case-study block** — named customer, role, quote, outcome
9. **CTA block** — final conversion ask with supporting reassurance
10. **FAQ block** — 5-8 questions with answers

## Optional body sections

- **Pricing teaser block** — only on homepage / pricing-page-teaser
- **Trust block** — security, compliance, certifications
- **Integrations block** — when product is in an ecosystem

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified — but landing-page-copy is a **copy-heavy output**, so inline tags break readability.

**Use `<!-- HTML comment tags -->` for confidence audit trail** (stripped at publish):

```html
<!-- VERIFIED: 'Cuts 30% off proposal time' from messaging proof_points {path} -->
The fastest way to close more deals.
```

Substantive claims (metrics, customer names, comparison facts) inherit `[VERIFIED]` from upstream messaging + case-study; the comment trail proves the chain.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Each block as H2 section with H3 sub-blocks
- Headline + sub-headline rendered in larger size for visual emphasis (custom Drive style)
- Headline + sub-headline char counts shown next to each (operator preview before paste)

### gdrive (Slides) — N/A
### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = page summary
- H1 = "{Client} — {page_type} Copy"
- Each H2 (block) = toggle block; copy inside the toggle as plain text (paste-ready)

### Direct publish (channel-native)

When deployed via Framer / Webflow / website-build skill, the copy migrates from this Doc into the page's CMS. The Doc remains the source of truth for copy review.

## Validation rules

1. All required frontmatter fields present
2. `page_type` is one of the enum values
3. Hero H1 ≤100 chars; sub-headline ≤150 chars (per CLAUDE.md voice rules)
4. Active sentence structure: active verb → gerund → "so what" (per CLAUDE.md)
5. ≥3 feature blocks (rarely meaningful below)
6. FAQ block: 5-8 questions
7. CTA block has primary + optional secondary CTA
8. Banned buzzwords ("innovative", "leverage", "synergy", "solutions") absent — per CLAUDE.md voice

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
