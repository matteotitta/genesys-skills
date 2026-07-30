---
knowledge_type: funnel-strategy
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Funnel Strategy — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Captures the GTM motion (PLG / SLG / hybrid), pre-close stages, post-close stages, qualification criteria, and FETE pipeline mapping. Drives outbound, lifecycle, and content-strategy decisions.

## Required frontmatter fields

```yaml
client: {slug}
skill: funnel-strategy
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: funnel-strategy
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

- `gtm_motion` — one of: PLG, SLG, hybrid, community-led, channel-led
- `pre_close_stages` — ordered array of pipeline stages from awareness → close
- `post_close_stages` — ordered array of stages from onboarding → expansion → renewal

Optional: `qualification_criteria`, `closed_lost_reentry`, `fete_mapping`.

## Required body sections (in order)

1. **Motion summary** — 3-5 sentences on the GTM motion + why it fits this client
2. **Pre-close funnel** — stage-by-stage with entry triggers, exit criteria, key metrics
3. **Post-close funnel** — onboarding → activation → expansion → renewal
4. **Qualification criteria** — fit + intent + budget + authority signals per stage
5. **FETE mapping** — find / engage / track / enrich pipeline mapping

## Optional body sections

- **Closed-lost re-entry** — when/how lost deals get re-prospected
- **Channel attribution** — which channels feed which stages
- **Conversion benchmarks** — stage-to-stage conversion rates (own data or industry baseline)

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Sections that require inline tags:
- Conversion benchmarks (every rate: source + date)
- Qualification criteria (when derived from win-loss-analysis or buyer interviews)

Motion summary + funnel stage descriptions inherit confidence from cited evidence.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Funnel stages as numbered Drive native tables (one row per stage)

### gdrive (Slides) — N/A
### gdrive (Sheet) — for clients with complex multi-segment funnels

When a client has 3+ distinct funnels (e.g., self-serve + mid-market + enterprise), aggregate view renders as Sheet with one tab per segment.

### notion (Page render)

- Overview = motion summary
- H1 = "{Client} — Funnel Strategy"
- Each H2 = toggle block; pre-close + post-close funnels are heaviest sections

## Validation rules

1. All required frontmatter fields present
2. `gtm_motion` enum check
3. `pre_close_stages` array has ≥3 stages
4. `post_close_stages` array has ≥2 stages (minimum onboarding + retention)
5. Qualification criteria section present + ≥1 criterion per stage
6. FETE mapping section present (even if mapping is "manual / no automation yet")

## Examples in the wild

- `projects/consulting/active/ClientCo/funnel/0226-funnel-strategy.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
