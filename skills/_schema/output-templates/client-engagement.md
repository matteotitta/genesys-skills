---
knowledge_type: client-engagement
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Client Engagement — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md` + `.claude/rules/consulting-clients.md`

## Purpose

Captures discovery research, proposals, and scope-of-work documents for prospects + active clients. The substrate for sales pipeline, onboarding, and KPI scoping.

## Required frontmatter fields

```yaml
client: {slug}                       # or "prospect-{slug}" for pipeline
skill: discovery | proposal | onboarding   # which client-engagement variant
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: client-engagement
engagement_phase: discovery | proposal | scope | onboarding | active
stakeholder_primary: {name + role}
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

Variant-specific. Common sections across all variants:

1. **Engagement overview** — who, what, why, when
2. **Stakeholders** — names, roles, decision-making authority

Variant-specific sections:

### Discovery variant
3. **Pre-call research** — company-context summary + open questions
4. **Discovery findings** — answers to key questions, surprises, red flags
5. **Recommended scope** — what we'd propose

### Proposal variant
3. **Context formula** — per `.claude/rules/consulting-clients.md` proposal format
4. **Scope of work** — deliverables, timeline, milestones
5. **Pricing + terms** — investment, payment terms, exclusions
6. **Success metrics** — how we'll measure outcome

### Onboarding variant
3. **Kickoff agenda** — first-week activities, intros, access setup
4. **Goals + KPIs** — references `goals/MMYY-scope.md` (per CLAUDE.md canonical-references rule)
5. **Voice + brand pointer** — references `brand/MMYY-tov-guidelines.md`
6. **Cadence** — sprint length, review rhythm, communication channels

## Optional body sections

- **Risk register** — what could derail the engagement
- **Stakeholder map** — champions vs detractors
- **Prior conversations** — Slack threads, Granola call IDs that informed this doc

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Sections that require inline tags:
- Pre-call research (every claim about the company: company-context output reference or external source)
- Discovery findings (every quote: Granola call ID + timestamp)
- Pricing benchmarks (when claiming market rates: source + date)

Proposals citing client metrics MUST be `[VERIFIED]` (source provided by client) or `[ESTIMATED: based on stated reasoning]` — never silently invented.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Stakeholder map as Drive native table
- Scope of work + pricing as structured tables

### gdrive (Slides) — for proposals when client requests deck format

Convert proposal Doc to Slides: 1 cover, 1 context, 1-3 scope slides, 1 pricing, 1 timeline, 1 success metrics.

### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = engagement overview
- H1 = "{Client} — {Variant}"
- Stakeholders + scope sections as toggle blocks (collapsed)

## Validation rules

1. All required frontmatter fields present
2. `engagement_phase` enum check
3. Variant-specific sections present per variant
4. Proposal variant: pricing section + success metrics section both present
5. Onboarding variant: goals/MMYY-scope.md reference must resolve to existing file
6. Stakeholder section: ≥1 named stakeholder with role + authority

## Examples in the wild

- `projects/consulting/active/pivot/docs/0226-proposal-v3.md` (when conforming)
- `projects/consulting/active/ClientCo/docs/0326-discovery-call-prep.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
