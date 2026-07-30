---
knowledge_type: lead-assessment
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 1 Strategy"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-sheet
---

# Lead Assessment — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Per-account fit + signals + interpretation → routing recommendation. The output of lead-scoring runs across batches of accounts. Canonical render is **Sheet** (multi-account routing table) — the only Strategy-tier type that defaults to Sheet.

Per the wave-batch + calibration-round patterns (`orchestration-patterns.md` § Orchestration mechanics), batch sizes >15 accounts use a calibration sample first; batch sizes >5 use wave orchestration.

## Required frontmatter fields

```yaml
client: {slug}
skill: lead-scoring
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: lead-assessment
batch_size: {n}                       # number of accounts in this batch
calibration_round_done: {bool}        # true if >15 accounts and calibration sample run
wave_size: {n}                        # 5 default per BUILD #7
sources_count:
  verified: {n}
  inferred: {n}
  estimated: {n}
  unavailable: {n}
locked_by: null
locked_date: null
review_gate_passed: null
```

Plus type-specific required fields per ontology.md (per-account):

- `company_name` — account name
- `fit_verdict` — one of: STRONG_FIT, MODERATE_FIT, WEAK_FIT, NO_FIT
- `signal_inventory` — observed signals with recency tags
- `situation_hypothesis` — narrative on what's happening at this account
- `routing_recommendation` — one of: SALES, MARKETING, MONITOR, EVALUATE, DEPRIORITIZE, DISQUALIFY
- `signal_recency` — STRONG, MODERATE, WEAK, EXPIRED

Optional: `fit_dimensions`, `signal_clusters`, `confidence_assessment`, `data_gaps`, `next_actions`.

## Required body sections (in order)

When rendered as Sheet, the body is the spreadsheet itself. When a Doc version is requested:

1. **Batch summary** — total accounts, fit_verdict distribution, top routing recommendations
2. **Methodology** — fit dimensions weighted, signal types ingested, recency thresholds applied
3. **Calibration findings** — (only if batch >15) what the sample of 5-7 accounts surfaced before scoring the rest
4. **Account routing table** — one row per account with all required fields
5. **Top SALES routes** — accounts that should hit sales pipeline today (with justification)
6. **Data gaps + next steps** — accounts with insufficient data + how to fill it

## Optional body sections

- **Signal cluster analysis** — patterns across accounts (intent surge, hiring trend)
- **Cohort comparison** — this batch vs previous batches
- **Per-account briefs** — appendix with one-pager per STRONG_FIT account

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Strategy outputs require ≥60% verified.

Sections that require inline tags:
- Account routing table (every fit_verdict + routing_recommendation backed by evidence — Apollo enrichment, Granola call, website signal)
- Signal inventory per account (every signal: source + observed date)

Routing recommendations are derived; inherit from cited fit + signals.

References `apollo-credits.md` — every Apollo enrichment call confirmed before execution.

## Render rules per target

### gdrive (Sheet — canonical)

The default render. Sheet structure:
- One row per account
- Columns: company_name, domain, fit_verdict, fit_score, signal_inventory (compact), situation_hypothesis (truncated), routing_recommendation, signal_recency, source_apollo, source_granola, last_observed, next_action_owner, next_action_date

Cell-level color coding is OK (e.g., STRONG_FIT in green, NO_FIT in gray) — this is the one render that benefits from color since the matrix density is high.

### gdrive (Doc) — for narrative summary

When client requests narrative + table, render as Doc with the body sections above + the routing table embedded as Drive native table.

### gdrive (Slides) — N/A

### notion (Page render)

- Overview = batch summary
- H1 = "{Client} — Lead Assessment ({YYYY-MM} batch)"
- Routing table as Notion native database; per-account briefs as nested toggle pages

## Validation rules

1. All required frontmatter fields present
2. `batch_size` matches number of accounts in the routing table
3. If `batch_size > 15`, `calibration_round_done` must be true (BUILD #6)
4. Every account has all required per-account fields
5. `fit_verdict` and `routing_recommendation` use only enum values
6. Every signal has recency tag

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
