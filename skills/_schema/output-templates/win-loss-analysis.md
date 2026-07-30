---
knowledge_type: win-loss-analysis
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Win/Loss Analysis — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Synthesizes patterns from won and lost sales calls to surface deal-driving themes, objection clusters, and competitive positioning learnings. Drives positioning, messaging, ICP, and battlecards.

**Additive convention** per `.claude/rules/orchestration-patterns.md` § Orchestration mechanics → Lock-down state: this output is NEVER locked. Each cycle's output extends the cumulative knowledge base. The `status` field stays at `draft` permanently; team review applies but locking is intentional non-policy here.

## Required frontmatter fields

```yaml
client: {slug}
skill: win-loss
version: 1
status: draft                       # always 'draft' — additive, never locks
generated: {YYYY-MM-DD}
ontology_type: win-loss-analysis
analysis_cycle: {YYYY-MM}            # which monthly/quarterly cycle this aggregates
transcripts_analyzed: {n}
outcome_breakdown:
  won: {n}
  lost: {n}
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

1. **Executive summary** — win drivers + loss drivers + top recommendation in 5 sentences
2. **Win drivers by dimension** — Product / Messaging / Pricing / Sales process / Competitive position / Customer fit (each with 3-5 themes)
3. **Loss drivers by dimension** — same dimensions
4. **Verbatim quotes** — speaker, role, call date, quote text (10+ across won + lost)
5. **Objection clusters** — recurring objections with frequency
6. **Competitive mentions** — which competitors come up, how often, in what contexts
7. **Recommendations** — what to change in positioning / messaging / sales motion

## Optional body sections

- **Segment cuts** — patterns by ARR / industry / geography
- **Sales-cycle timing** — patterns by cycle length (fast wins vs slow losses)
- **Cross-cycle deltas** — what's changed since last analysis

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Verbatim quotes section: every quote requires `[VERIFIED: Granola call transcript, {meeting-id}, accessed YYYY-MM-DD]`.

Win/loss drivers + objection clusters: claims grounded in quoted evidence (which carries the tag).

Recommendations may use `[INFERRED]` from the patterns above.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Quotes as block-quotes with attribution line below
- Win/loss driver dimensions as 2-column Drive native table (left: dimension, right: themes)

### gdrive (Slides) — for sales team review (occasionally)

When team requests a presentation summary, slides render: 1 title slide, 1 executive summary, 1 per dimension (won), 1 per dimension (lost), 1 recommendations.

### gdrive (Sheet) — for cumulative tracking

Sheet aggregates: row per call analyzed, columns: outcome, segment, dimensions, top driver, top objection, competitor mentioned. Updated each cycle.

### notion (Page render)

- Overview = executive summary
- H1 = "{Client} — Win/Loss Analysis ({YYYY-MM})"
- Each H2 = toggle block (collapsed); quotes toggle is heaviest

## Validation rules

1. All required frontmatter fields present
2. `transcripts_analyzed` ≥1; `outcome_breakdown` sums match
3. Quotes section: ≥10 verbatim quotes with full attribution
4. Win drivers + loss drivers each cover all 6 dimensions (or explicitly note "no signal")
5. Recommendations section ≥3 specific actions
6. `status` is always `draft` (additive convention — locking is non-policy)

## Examples in the wild

- `projects/consulting/active/ClientCo/win-loss/0326-win-loss.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
