---
knowledge_type: company-context
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Company Context — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Captures the firmographic + traction + qualification snapshot of a company (prospect, client, or competitor's customer). Acts as the substrate every downstream skill inherits — positioning, ICP, competitor research, proposals all read this before pulling fresh data.

## Required frontmatter fields

```yaml
client: {slug}                       # client folder slug; or "prospect-{slug}" for pipeline
skill: company-context
version: 1
status: draft                        # draft | review | locked | superseded
generated: {YYYY-MM-DD}
ontology_type: company-context
sources_count:
  verified: {n}
  inferred: {n}
  estimated: {n}
  unavailable: {n}
locked_by: null
locked_date: null
review_gate_passed: null             # 0–4 per ontology.md
```

Plus type-specific required fields per ontology.md:

- `company_name` — official entity name
- `website` — primary URL
- `traction_signals` — array of dated signals (funding, hiring, launches, customer wins)
- `qualification_score` — fit verdict against caller's ICP
- `icp_fit_assessment` — narrative on fit dimensions

Optional: `red_flags`, `data_gaps`, `founded_year`, `employee_count`, `funding_total`, `revenue_model`.

## Required body sections (in order)

1. **Executive summary** — 3-5 sentences. What the company does, who they serve, the qualification verdict.
2. **Company snapshot** — table: founded, HQ, employee count, funding, revenue model, primary stack.
3. **Product + value proposition** — what they sell, to whom, against what status quo.
4. **Traction signals** — bulleted list of dated signals (each with confidence tag).
5. **ICP fit assessment** — fit-dimension breakdown: industry, ARR/employee size, motion, geography, intent.
6. **Red flags** (omit if none) — anything that disqualifies or warrants caution.
7. **Data gaps** — what's `[UNAVAILABLE]` and how to fill it.

## Optional body sections

- **Founder + leadership** — when relevant for proposals or expert-pov downstream
- **Competitive landscape** — when company-context informs a competitor's profile
- **Funding history** — detailed timeline when fundraising signals matter

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier outputs require ≥50% verified.

Sections that always require tags:
- Traction signals (every signal: `[VERIFIED: source, url, accessed YYYY-MM-DD]`)
- Company snapshot (employee count, funding, revenue model)
- Founder + leadership (every name + role)

Narrative sections (executive summary, ICP fit assessment) inherit confidence from the cited facts within them.

## Render rules per target

### gdrive (Doc — canonical)

Per `.claude/rules/design-production.md` and architecture decision 6:
- Inter, black, plain header, page-numbered footer, native TOC after H1
- Company snapshot renders as Drive native table
- Traction signals as bulleted list with confidence tags inline

### gdrive (Slides) — N/A
### gdrive (Sheet) — N/A

### notion (Page render)

- Overview paragraph = the executive summary's first 2 sentences
- H1 = company name + " — Company Context"
- Each H2 section = toggle block (collapsed)
- "Sources" toggle at end of each H2 with citations from that section

## Validation rules

1. All required frontmatter fields present + non-empty
2. `ontology_type` equals `company-context`
3. `sources_count` sums to > 0
4. ≥3 entries in `traction_signals`
5. `icp_fit_assessment` section present + ≥100 chars
6. Traction signals section: every bullet carries a confidence tag
7. No `[ESTIMATED]` tags on company snapshot fields (employee count, funding, revenue) — must be `[VERIFIED]` or `[UNAVAILABLE]`

## Examples in the wild

- `projects/consulting/active/ClientCo/docs/0326-company-context.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
