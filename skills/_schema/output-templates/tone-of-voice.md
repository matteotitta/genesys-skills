---
knowledge_type: tone-of-voice
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Tone of Voice — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Captures the client's voice patterns, vocabulary, frequency scores, and do/don't guidance. Drives every downstream content output (LinkedIn posts, newsletters, landing page copy, sales decks) — without TOV, content drifts toward generic.

## Required frontmatter fields

```yaml
client: {slug}
skill: tov-guidelines
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: tone-of-voice
tov_phase: guidelines        # analysis (raw extraction) | guidelines (prescriptive system)
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

- `voice_patterns` — characteristic sentence shapes, openings, transitions
- `vocabulary` — preferred terms, banned buzzwords, signature phrases

Optional: `frequency_scores`, `do_dont_patterns`, `brand_voice_spectrum`.

## Required body sections (in order)

1. **Voice attributes** — 3-5 attributes with definitions (e.g., "Operator-first," "Warm but challenging")
2. **Sentence patterns** — characteristic openers, transitions, closers (with examples)
3. **Vocabulary** — preferred terms, banned buzzwords, signature phrases
4. **Anti-AI-speak** — explicit list of patterns to reject (the 100 Posts Test)
5. **Do's and don'ts** — concrete pairs with rewrite examples

## Optional body sections

- **Frequency scores** — quantitative analysis of voice attribute frequency in source corpus
- **Brand voice spectrum** — where the brand sits on warmth/authority/playfulness axes
- **Channel-specific overrides** — when LinkedIn voice differs from blog voice

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Sections that require inline tags:
- Voice attributes (every attribute backed by ≥3 source samples)
- Vocabulary (banned buzzwords backed by samples where they appeared)
- Anti-AI-speak (each pattern backed by an example detected in client material)

Do's and don'ts pairs may use `[INFERRED]` from the voice attributes.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Do's and don'ts as 2-column Drive native table

### gdrive (Slides) — N/A
### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = the 3-5 voice attributes in one sentence
- Each H2 = toggle block (collapsed)
- Do's/don'ts toggle expandable per pattern

## Validation rules

1. All required frontmatter fields present
2. `tov_phase` is one of: analysis, guidelines
3. ≥3 voice attributes named + defined
4. Anti-AI-speak section: ≥5 patterns listed
5. Do's and don'ts: ≥10 pairs
6. Banned buzzwords: ≥5 (per CLAUDE.md voice rule baseline)
7. Voice attributes carry source evidence (≥3 samples per attribute)

## Examples in the wild

- `projects/consulting/active/ClientCo/brand/0426-tov-guidelines.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
