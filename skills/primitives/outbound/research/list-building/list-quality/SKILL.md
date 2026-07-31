---
name: list-quality
version: '1.0'
last_updated: 2026-05-04
author: genesys-growth
description: 'Pre-send mechanical grade of any contact list CSV across 8 content-side dimensions: title relevance vs. ICP, bad-title detection (intern/coordinator/student), per-domain concentration cap, ICP firmographic fit, name quality, plus 3 email-side dimensions delegated to deepline-enrich (verification, dupes, catch-all). Outputs an A+ to F letter grade + top 5 issues to fix + a pre-send checklist. Catches bad lists BEFORE enrichment spend (deepline-enrich runs $0.05-0.20 per row) and BEFORE sequence enrollment. Triggers: "grade this list", "is this list ready to send", "list quality check", "list scorecard", "what''s wrong with my list". Upstream: any list-builder (apollo-find, clay-search, jobs-signal, niche-signal). Downstream: feeds deepline-enrich (only after grade ≥ B), apollo-sequences, outreach (runner mode), and abm-campaign. NOT for per-account fit assessment (use /lead-scoring) or post-send measurement (use /reply-scoring).'
goal: Grade a contact list CSV across 8 content-side dimensions and surface the top issues to fix before enrichment or sending.
outcome: A markdown scorecard with letter grade A+ to F, dimension-by-dimension scores 0-100, top 5 issues with row counts, and a pre-send checklist that gates the next pipeline step.
primitive: outbound
sub_primitive: research
ontology_type: list-grade
review_gate: 1
inputs:
  required: []
  recommended:
  - icp-research
  - apollo-find
  - clay-search
- type: list-grade
  feeds_into:
  - deepline-enrich
  - outreach-emails
  - abm-campaign
depends_on: []
- deepline-enrich
- outreach-emails
- abm-campaign
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands:
  - /list-quality
  natural_language:
  - grade this list
  - list quality check
  - is this list ready to send
  - list scorecard
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# List quality

A CSV of 5,000 leads is not the same as a good list of 5,000 leads. This skill grades any list across 8 content-side dimensions BEFORE you spend on enrichment or burn inbox reputation on bad sends. Catches preventable waste in 5 minutes.

## Claude Code triggers

**Invoke when user says:**
- "Grade this list"
- "List quality check"
- "Is this list ready to send"
- "List scorecard for [file]"
- "What's wrong with my list"
- "Should I enrich this or fix it first"

**Do NOT invoke when:**
- User wants per-account fit assessment → `/lead-scoring`
- User wants email validation only (no content-side checks) → `/deepline-enrich` already covers this
- User wants post-send reply analysis → `/reply-scoring`
- List is < 100 rows → sample too small for the rubric; just eyeball

**Auto-suggest after:** any list-building skill (`apollo-find`, `clay-search`, `jobs-signal`, `niche-signal`) produces a CSV. The pipeline order is:

```
list-builder → list-quality → deepline-enrich → outreach/apollo-sequences
```

Running list-quality BEFORE deepline-enrich saves $0.05-0.20 per row in wasted enrichment spend on lists that wouldn't pass the gate anyway.

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **CSV file** | Contact list with at minimum: `email`, `first_name`, `last_name`, `title` (or `job_title`), `company_name` (or `company`) | Output from any list-builder |

### Optional (improves quality significantly)

| Input | Purpose |
|-------|---------|
| `company_domain` (CSV column) | If absent, derived from email; explicit column improves dedup accuracy |
| `company_industry` (CSV column) | Required for the `icp_fit` dimension |
| `company_headcount` (CSV column) | Required for the `icp_fit` dimension |
| **ICP file path** | `projects/consulting/active/{client}/icp/MMYY-icp-research.md` — provides the title taxonomy, target industries, headcount range. Without this, `icp_fit` and `title_relevance` fall back to defaults. |
| **Verification status** | If column `verification_status` exists with values `valid|catch-all|invalid|unknown` (from prior `/deepline-enrich` run), the email-side dimensions use it. If absent, those dimensions are deferred to deepline-enrich. |

**Validation:** CSV is parseable; ≥100 rows; required columns present. If <100 rows, refuse with: "Sample too small (N rows). Eyeball it instead."

## Process

Five phases — full step detail in the premium reference.

1. **Phase 1 — Load + normalize.** Parse CSV, lowercase emails, derive `company_domain` from email if missing, mark missing columns.
2. **Phase 2 — Score 8 dimensions.** Apply per-dimension scoring rules from the premium reference. Each dimension returns a 0-100 score.
3. **Phase 3 — Composite + grade.** Weighted average across the 8 dimensions (verification + ICP fit weighted 2× per dimension docs); map composite to A+ to F via the premium reference.
4. **Phase 4 — Top issues + checklist.** Surface the 5 highest-impact problems in priority order with row counts and concrete fix actions; emit pre-send checklist.
5. **Phase 5 — Write report.** Markdown scorecard per the premium reference saved alongside the input CSV.

## MCP data integration

**Pulls fresh:** none — this skill is pure CSV analysis, no MCP calls. Uses the Genesys Deepline waterfall's verification status if present in the CSV (column `verification_status`), but does not call Deepline directly.

**Fallback:** if `verification_status` column is missing AND the email-side dimensions can't run (verification, catch-all density), the report explicitly says "EMAIL-SIDE DIMENSIONS DEFERRED TO DEEPLINE-ENRICH" and grades only the 5 content-side dimensions, with a note that the final grade may shift after enrichment.

**Validation:** every dimension score is reproducible — running the skill twice on the same CSV produces identical results.

## Quality

Pre-delivery checklist + minimum row threshold + composite weighting: the premium reference.

Headline rules:
- Minimum row count: 100. Below that → refuse to grade.
- Composite weighting: verification + ICP fit weighted 2× the others (these two are the load-bearing dimensions for outbound success).

## Anti-hallucination guardrails

1. **Never invent ICP fit if no ICP file is provided.** Surface as "ICP_FIT: NOT EVALUATED — provide --icp-file to enable" rather than guessing.
2. **Never invent title relevance.** Without an ICP file, fall back to a default seniority filter (Director+ counts; Manager and below flagged) but explicitly mark as "DEFAULT FILTER — provide ICP for accurate scoring."
3. **Don't hide failed dimensions.** If a dimension can't run (missing column, no ICP file), it appears in the report with status NOT EVALUATED, not omitted.
4. **Cite row counts for every issue.** "23 emails are duplicates" — never "many duplicates."
5. **Never auto-modify the input CSV.** This skill grades; it doesn't fix. Fixes happen in the next step (back to list-builder, or via a separate cleanup script).

## Integration with other skills

**Upstream (recommended, not required):**
- `apollo-find`, `clay-search`, `jobs-signal`, `niche-signal` — produce the CSVs this skill grades
- `icp-research` — the `icp/MMYY-icp-research.md` provides the title taxonomy + industry filter for ICP-based dimensions

**Downstream (gated on grade ≥ B):**
- `deepline-enrich` — only run on lists that pass list-quality at B+. Saves $0.05-0.20/row on bad lists.
- `apollo-sequences` — only enroll on lists at B+ (lower grades burn inbox reputation)
- `outreach` (runner mode) — only batch-generate on B+ lists
- `abm-campaign` — account-level overlay on a graded list

**Sideways:**
- `lead-scoring` — different layer (per-account fit + signals); list-quality runs first (mechanical hygiene), lead-scoring after on the qualified subset
- `/reply-scoring` — closes the measurement loop: list-quality before send, reply-scoring after

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

