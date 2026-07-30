---
knowledge_type: youtube-strategy
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 1 Strategy"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# YouTube Strategy — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

YouTube channel launch strategy: keyword demand + competitor channel buckets + gap analysis + 6 video ideas + Month-1 TOFU/BOFU mix. The most fully-specified Strategy-tier type — ontology.md lines 91-105 has explicit entity schema.

## Required frontmatter fields

```yaml
client: {slug}
skill: youtube-strategy
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: youtube-strategy
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

- `keyword_demand_table` — keywords with monthly volume + competition bucket
- `competitor_channel_scan` — analyzed competing YouTube channels
- `competitor_buckets` — channels grouped by competition level
- `gap_statement` — articulated gap this client can win
- `video_ideas` — 6+ video concepts with all required fields
- `month_1_plan` — Month-1 mix (TOFU/BOFU split)

Optional: `top_ranking_video_gaps`, `case_study_framework`, `case_study_shortlist`, `niche_hypothesis`, `publishing_cadence`.

Per ontology, video idea fields: `working_title`, `target_keywords`, `proven_demand`, `the_gap`, `your_edge`, `format`.

Per ontology enums:
- `competition_buckets`: very_low, low, medium, medium_high, high, high_but_growing_fast
- `bofu_formats`: case_study, testimonial
- `month_1_mix_variants`: default_2_2, new_channel_3_1, bofu_constrained_2_cs

## Required body sections (in order)

1. **Executive summary** — niche hypothesis + gap + Month-1 plan in 5 sentences
2. **Keyword demand** — table: keyword, monthly volume, competition bucket, our angle
3. **Competitor channel scan** — analyzed channels with subs, video count, top videos
4. **Competitor buckets** — channels grouped by competition level (per enum)
5. **Gap statement** — articulated gap + why we win it
6. **Video ideas** — 6+ ideas with all required fields per idea
7. **Month-1 plan** — TOFU/BOFU mix per chosen variant; publish cadence; success metrics
8. **Case study shortlist** — when client has customers, candidates for BOFU case-study videos

## Optional body sections

- **Top-ranking video gaps** — high-volume queries with weak existing top results
- **Niche hypothesis testing plan** — how to validate the niche before scaling
- **Publishing cadence** — multi-month cadence beyond Month-1
- **Repurposing plan** — how YouTube content cascades to LinkedIn, blog, newsletter

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Strategy outputs require ≥60% verified.

Sections that require inline tags:
- Keyword demand table (every volume + competition: source — Ahrefs, GSC — + access date)
- Competitor channel scan (every metric: source URL + date)
- Top-ranking video gaps (claims about weak results: SERP screenshot or query timestamp)

Niche hypothesis + gap statement are strategic synthesis; inherit from cited evidence.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Keyword demand + competitor scan + competitor buckets as Drive native tables
- Video ideas as numbered list with H3 per idea (working title) + nested fields

### gdrive (Slides) — for client briefings

Slides: 1 niche, 1 keyword demand, 1 competitor buckets, 1 gap, 6 video ideas (1 per slide), 1 Month-1 mix.

### gdrive (Sheet) — for keyword research data

Sheet variant: full keyword research data (rows: keywords; columns: volume, competition, intent, angle, target video).

### notion (Page render)

- Overview = niche hypothesis + Month-1 plan
- H1 = "{Client} — YouTube Strategy"
- Each H2 = toggle block; video ideas toggle is heaviest (one nested toggle per idea)

## Validation rules

1. All required frontmatter fields present
2. `keyword_demand_table` has ≥10 keywords
3. `competitor_channel_scan` covers ≥5 channels
4. Every channel placed in a `competitor_buckets` enum value
5. `video_ideas` has ≥6 entries; each has all 6 required fields
6. `month_1_plan` selects one of the 3 mix variants
7. BOFU formats use only enum values (case_study or testimonial)

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
