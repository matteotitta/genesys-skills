---
knowledge_type: expert-pov
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Expert POV — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Captures a founder/expert's belief system — core philosophy, differentiated takes, origin stories, OBI (Operating Belief Inventory). Drives thought-leadership, LinkedIn personal posts, newsletter, and the founder voice referenced in TOV.

## Required frontmatter fields

```yaml
client: {slug}
skill: expert-pov
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: expert-pov
expert_name: {Full Name}
expert_role: {Role at company}
calibration: "v1.0 — {n} founder feedback points integrated"   # iteration tracking
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

1. **Executive summary** — who the expert is + their 3 most distinctive beliefs
2. **Core philosophy** — the meta-thesis that connects all takes
3. **Belief map** — 7-12 specific beliefs with explanations + supporting evidence
4. **Differentiated takes** — where this expert disagrees with conventional wisdom
5. **Origin stories** — 3-5 narrative arcs that shaped the philosophy (with timing)
6. **OBI (Operating Belief Inventory)** — the prescriptive principles the expert operates by

## Optional body sections

- **Implicit assumptions** — what the expert takes for granted that others might not
- **Pushback themes** — where the expert has been challenged + how they respond
- **Future-tense beliefs** — predictions / where they expect the world to move

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Beliefs + takes require source evidence:
- `[VERIFIED: {LinkedIn post / podcast / interview / Granola call}, url/id, accessed YYYY-MM-DD]`
- `[INFERRED: from {a} + {b}]` only when synthesizing a belief from multiple expressions
- Founder feedback annotations: when the founder has personally validated a belief, mark `[VERIFIED: founder feedback {YYYY-MM-DD}]`

Origin stories require a verifying source (the founder's own retelling — Granola, LinkedIn, podcast).

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Belief map as numbered list (each belief has H3 + body); evidence as nested bullets

### gdrive (Slides) — N/A (founder thought leadership decks are sales-enablement-asset)
### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = executive summary's first 2 sentences
- H1 = "{Expert Name} — Expert POV (v{calibration})"
- Each H2 = toggle block (collapsed); belief map is the heaviest

## Validation rules

1. All required frontmatter fields present
2. `expert_name` + `expert_role` present
3. Belief map: ≥7 beliefs, each with ≥1 source
4. Differentiated takes: ≥3 explicit "disagrees with conventional wisdom" statements
5. Origin stories: ≥3 narratives with dated context
6. OBI section present (operating principles in imperative voice)
7. `calibration` updates with each founder review cycle

## Examples in the wild

- `projects/consulting/active/ClientCo/expert-pov/0326-alan-gurung-expert-pov.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
