---
knowledge_type: thought-leadership
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 3 Content"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Thought Leadership — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Long-form founder/expert content — blog post, guest essay, or LinkedIn long-form. The strictest content-tier gate: every framing must trace back to a locked `expert-pov` output. Without expert-pov upstream, the piece is content-strategy commentary, not thought leadership.

## Required frontmatter fields

```yaml
client: {slug}
skill: thought-leadership
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: thought-leadership
governing_thought: {one-line thesis}
key_lines:                           # MECE supporting points
  - {key line 1}
audience_starting_point: {what reader believes / knows entering the piece}
target_word_count: {n}               # 800-2500 typical
publication_target: linkedin | blog | guest | newsletter
phase_approvals:                     # 3-phase gate trail
  - phase: outline
    status: pending | approved | revision
    reviewer: {name}
    date: null
  - phase: draft
    status: pending | approved | revision
    reviewer: {name}
    date: null
  - phase: final
    status: pending | approved | revision
    reviewer: {name}
    date: null
upstream_expert_pov: {path}          # REQUIRED — must resolve to existing locked expert-pov
evidence_anchored_by:
  - {path}
distribution_plan:                   # downstream artifacts that anchor back
  - linkedin-post: {path or null}
  - newsletter: {path or null}
  - youtube-script: {path or null}
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order)

1. **Hook + governing thought** — first 100 words; states the thesis with a specific lens
2. **Audience starting point** — establishes where reader is mentally before this piece
3. **Body sections** — H2 per key line; each line developed with founder voice + supporting evidence
4. **Differentiation moment** — explicitly where this take diverges from conventional wisdom (anchored in expert-pov differentiated takes)
5. **Concrete example / story** — narrative anchor that grounds the abstract argument
6. **Practical implication** — what the reader should DO differently after this piece
7. **Closing reframe** — restates the governing thought after the journey

## Optional body sections

- **Caveats / when this doesn't apply** — for nuanced takes
- **Counterpoint engagement** — when piece responds to a specific opposing view
- **Footnotes / sources** — for citation-heavy pieces

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Content tier requires ≥40% verified.

**No inline tags in body** — breaks reading flow.

`evidence_anchored_by` paths must include the upstream `expert-pov` (mandatory) plus any other research substrate (transcripts, win-loss, customer-interviews) the piece draws from.

For ClientCo: per `feedback_advisory_ai_em_dashes.md`, no em dashes in any thought-leadership for that client (validation rule below).

## Render rules per target

### gdrive (Doc — canonical, editorial collaboration surface)

- Inter, black, plain header, page-numbered footer, native TOC
- Body in editor-friendly format with section headers visible
- Phase approvals tracked in frontmatter (drives Phase 5 chain-lint validation that thought-leadership has all 3 approvals before locking)

### gdrive (Slides) — N/A
### gdrive (Sheet) — N/A

### notion (Page render — for collaborative editing)

- Overview = governing thought + audience starting point
- H1 = piece title (the published title, not the working title)
- Each H2 = toggle block (collapsed during edits; expanded during review)
- Phase approvals visible at top

### Channel-native (canonical end-state)

After Doc review + 3 phase approvals, piece publishes to:
- LinkedIn long-form (for `publication_target: linkedin`)
- Client blog via Framer/Webflow (for `publication_target: blog`)
- Guest publication (for `publication_target: guest`)
- Newsletter (for `publication_target: newsletter`)

`distribution_plan` frontmatter seeds linkedin-post / newsletter / youtube-script artifacts that evidence-anchor back to this piece.

## Validation rules

1. All required frontmatter fields present
2. `upstream_expert_pov` REQUIRED + must resolve to existing locked expert-pov output (hard gate)
3. All 3 `phase_approvals` entries must be `approved` before `status: locked`
4. `governing_thought` non-empty + ≤220 chars
5. `key_lines` are MECE — no overlap, mutually exclusive themes
6. `target_word_count` is 800-2500 (sweet spot for long-form)
7. Differentiation moment section explicitly references expert-pov differentiated takes
8. Practical implication section: concrete + specific (not generic advice)
9. **For ClientCo client:** validation fails if any em dash (`—`) appears in body (per `feedback_advisory_ai_em_dashes.md`)
10. `distribution_plan` populated before publishing (downstream artifacts seeded)

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
