---
knowledge_type: aeo-content
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# AEO Content — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

AI-engine-optimized blog content — articles structured to be cited by ChatGPT, Claude, Perplexity, Google AI Overviews. Produced per article brief from aeo-strategy + content-strategy.

## Required frontmatter fields

```yaml
client: {slug}
skill: aeo-content
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: aeo-content
target_query: {primary AI engine query this article targets}
query_cluster: {cluster name from aeo-strategy}
content_tier: TOFU | MOFU | BOFU
gap_priority_tier: 1 | 2 | 3        # per aeo-strategy gap analysis
upstream_aeo_strategy: {path}
upstream_messaging: {path}
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order — AEO-optimized anatomy)

1. **Direct answer block (top 200 words)** — the article's thesis in scannable form for AI extraction
2. **Article H1 + meta description** — published title + meta (≤155 chars)
3. **Introduction** — frames the problem in ICP language (with confidence tags inline — research-anchored)
4. **Body sections** — H2 per query subcluster, with structured answers (definitions, lists, comparisons)
5. **Comparison table** — when relevant, compare options head-to-head (Drive native table)
6. **FAQ section (schema-friendly)** — 5-8 Q&A with ICP-pain-grounded questions
7. **Sources + citations** — every claim with source URL + access date
8. **CTA block** — natural, low-friction, in-article CTA

## Optional body sections

- **Glossary** — for term-defining articles (high citation value)
- **Examples / case patterns** — when an explainer article needs concrete grounding
- **Related reading** — internal-linking section (drives content-strategy cluster integrity)

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified.

**Inline tags ARE used** for AEO content (unlike landing-page-copy) — AI engines cite well-sourced articles preferentially. Sources and citations section makes the trail explicit.

Sections requiring tags:
- Direct answer block (every factual claim: source URL + date)
- Body sections (every numbered fact, statistic, comparison data)
- Comparison tables (every cell sourced)

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Comparison table as Drive native table
- FAQ section with H3 per question, body answer below
- Direct answer block visually emphasized (boxed callout)

### gdrive (Slides) — N/A
### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = direct answer block (first 100 words)
- H1 = article title
- Each H2 = toggle block (collapsed); FAQ + Sources toggles default-open for stakeholder review

### Direct publish (channel-native)

When deployed via Framer / Webflow / Substack: convert this Doc to native CMS format. Maintain comparison tables, FAQ schema markup, and source links. Updates to the published article propagate the manifest line back per `notion-protocol.md`.

## Validation rules

1. All required frontmatter fields present
2. `target_query` non-empty + present in upstream aeo-strategy query-index
3. `content_tier` enum check
4. Direct answer block ≤250 words
5. FAQ section: 5-8 questions
6. Every body section claim has confidence tag
7. ≥10 distinct sources cited (AEO citation-bait threshold)
8. Article length ≥1200 words (typical AEO floor)

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
