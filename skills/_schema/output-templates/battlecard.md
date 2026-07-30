---
knowledge_type: battlecard
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Battlecard — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

One-competitor sales-enablement card with talk tracks, sharpeners, do-not-says, and proof points. Live-fire artifact reps consult mid-call. Depends on locked competitor-intel + win-loss-analysis + messaging.

## Required frontmatter fields

```yaml
client: {slug}
skill: battlecards
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: battlecard
competitor_name: {Competitor}
threat_level: PRIMARY | ENTERPRISE | DIRECT | STEALTH | LOW | DEFUNCT
upstream_competitor_intel: {path}
upstream_win_loss: {path}
upstream_messaging: {path}
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order — sales-rep-readable anatomy)

1. **Header block** — competitor name, threat level, last refresh date, owner
2. **Who they are** — 2-3 sentence factual summary (no editorializing)
3. **Their pitch** — what they say to prospects (verbatim from their site/sales)
4. **Our counter** — how we reframe their pitch
5. **Sharpener** — the one-line trump card (memorable phrase)
6. **The gap** — where they leave room (objective product/GTM weakness)
7. **Demo moment** — specific demo step that lands the differentiation
8. **Don't say** — phrases that backfire (inflammatory, untrue, easily disproved)
9. **Proof points** — customer logos, win quotes, head-to-head metrics
10. **Common objections + responses** — top 3-5 objections specific to this competitor

## Optional body sections

- **Pricing comparison** — when pricing is a primary differentiator
- **Loss patterns** — when win-loss-analysis surfaces specific losing patterns to address
- **Trade-offs we'd accept** — when honesty about our weakness wins trust

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified.

**Inline tags ARE used** (audit-grade) — battlecards are interrogated live by reps and prospects; tags need to be visible for the rep to defend a claim mid-call.

Sections requiring tags:
- Their pitch (verbatim from competitor source: URL + access date)
- Proof points (every metric: source + date)
- The gap (claims about competitor weakness: customer quote, public review, demo observation)
- Don't say (phrases banned because they were tested and failed: source from sales call review)

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Each section visually distinct (clear H2 + dense body)
- Comparison data as Drive native tables

### gdrive (Slides) — for sales kickoff briefings

Slides: 1 cover (competitor + threat), 1 their pitch, 1 our counter, 1 sharpener, 1 gap, 1 demo moment, 1 don't say, 1 proof points.

### gdrive (Sheet) — for battlecard suite tracking

Sheet aggregate: one row per competitor with battlecard age, last refresh, top objection, sharpener.

### notion (Page render)

- Overview = competitor name + threat level + sharpener
- H1 = "{Client} vs {Competitor} — Battlecard"
- Each H2 = toggle block (collapsed); demo moment + don't say toggles especially load-bearing

## Validation rules

1. All required frontmatter fields present
2. `threat_level` enum check (matches competitor-intel)
3. Their pitch is verbatim (quoted from competitor source)
4. Sharpener is one line (≤220 chars)
5. Don't say section: ≥3 banned phrases with reason
6. Proof points: ≥3 with verifying source
7. Common objections: 3-5 with rep-ready response

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
