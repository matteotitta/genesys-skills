---
knowledge_type: website-score
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 1 Strategy"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Website Score — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

PM-style 0-100 evaluation of a website (or specific page) across named dimensions, with screenshot evidence and prioritized recommendations. Drives website-strategy and website-execution decisions.

Sits at the audit/strategy boundary — the score is strategic input, but the verb is "score" so it routes to `website/audit/` per CLAUDE.md auto-routing.

## Required frontmatter fields

```yaml
client: {slug}
skill: website-score
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: website-score
target_url: {URL}
score_total: {0-100}
evaluator: PM-style                # PM-style | buyer-style | hybrid
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

1. **Executive summary** — total score + 3 biggest opportunities + verdict (ship / fix / rebuild)
2. **Dimension scores** — named rubric (Clarity, Proof, CTA, Trust, Speed, Mobile, etc.) with 0-100 per dimension + evidence
3. **Top 3 recommendations** — high-impact changes ranked by effort × impact
4. **Evidence per dimension** — screenshot annotations + specific page elements scored
5. **Quick wins** — sub-2-hour fixes the team can ship this week
6. **Strategic gaps** — multi-month or rebuild-level recommendations
7. **Re-score plan** — when to re-evaluate, what changed since last score

## Optional body sections

- **Competitor score comparison** — same rubric applied to 1-2 competitors
- **Before/after pairs** — for re-scores, paired screenshots showing changes
- **Page-level scores** — when site has multi-page audit (homepage, pricing, product)

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Strategy outputs require ≥60% verified.

Sections that require inline tags:
- Dimension scores (each backed by screenshot evidence + observed element)
- Top 3 recommendations (effort estimates + impact projections grounded in baseline data)
- Competitor score comparison (every score with screenshot URL + access date)

Verdicts (ship/fix/rebuild) are derived synthesis; inherit from cited evidence.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Dimension scores as Drive native table (rows: dimensions; columns: score, weight, evidence summary)
- Embed annotated screenshots inline (Drive native image insertion)

### gdrive (Slides) — for stakeholder briefings

Slides: 1 total score, 1 per dimension (with screenshot), 1 top 3 recs, 1 quick wins.

### gdrive (Sheet) — for ongoing tracking

Sheet variant: scoring observatory (one row per re-score over time, columns: date, total, per-dimension scores, change since last).

### notion (Page render)

- Overview = total score + verdict + 3 biggest opportunities
- H1 = "{Client} — Website Score: {score}/100"
- Each H2 = toggle block; evidence per dimension toggle holds screenshots

## Validation rules

1. All required frontmatter fields present
2. `score_total` is 0-100
3. Dimension scores: ≥4 named dimensions, each scored 0-100
4. Sum of weighted dimension scores = `score_total`
5. Top 3 recommendations section has exactly 3 items (not 4, not 2)
6. Every dimension has at least one screenshot or specific element cited
7. `target_url` resolves (live URL at time of score)

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
