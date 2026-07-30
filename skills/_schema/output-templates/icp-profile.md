---
knowledge_type: icp-profile
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# ICP Profile — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Captures the ideal customer profile across firmographics + champion persona + economic buyer + voice-of-customer. The substrate for positioning, messaging, content strategy, and outbound targeting.

## Required frontmatter fields

```yaml
client: {slug}
skill: icp-research                  # or icp-behavioural for synthetic-persona variant
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: icp-profile
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

- `tam_analysis` — TAM/SAM/SOM breakdown
- `firmographics` — ARR range, employee count, industry, geography
- `champion_persona` — title, level, day-to-day pain, buying triggers
- `economic_buyer_persona` — title, level, success metrics, sign-off threshold

Optional: `negative_icp`, `customer_proof_points`, `voice_of_customer`, `intent_signals`, `prompt_bank`.

## Required body sections (in order)

1. **Executive summary** — 3-5 sentences on who the ICP is and why
2. **TAM analysis** — total addressable, serviceable, obtainable; with sizing math
3. **Firmographics** — ARR, employee count, industry, geography, tech stack hints (table)
4. **Champion persona** — title, day-to-day pain, jobs-to-be-done, buying triggers
5. **Economic buyer persona** — title, success metrics, sign-off threshold, deal-breakers
6. **Voice of customer** — verbatim quotes from forums/reviews/calls (3+ per pain theme)
7. **Negative ICP** — explicit anti-fit; companies that should be disqualified

## Optional body sections

- **Customer proof points** — named customers + their use cases
- **Intent signals** — observable triggers that indicate buying readiness
- **Prompt bank** — synthetic persona prompts for icp-behavioural variant

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Sections that require inline tags:
- TAM analysis (every sizing claim)
- Firmographics (every range claim)
- Voice of customer (every quote: source platform + url + date)
- Customer proof points (every named customer)

Champion + economic buyer personas use `[INFERRED]` from voice + firmographics where direct evidence is unavailable.

## Render rules per target

### gdrive (Doc — canonical)

Per architecture decision 6:
- Inter, black, plain header, page-numbered footer, native TOC
- Firmographics as Drive native table
- VoC quotes as block-quotes with attribution line

### gdrive (Slides) — N/A
### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = executive summary
- H1 = "{Client} — ICP Profile"
- Each H2 = toggle block (collapsed); voice-of-customer toggle keeps each pain theme expandable

## Validation rules

1. All required frontmatter fields present
2. `ontology_type` equals `icp-profile`
3. Champion persona section + economic buyer persona section both present
4. ≥3 voice-of-customer quotes, each with source url + date
5. Negative ICP section present (≥3 explicit anti-fit criteria)
6. TAM analysis: sizing math shown (not just final numbers)

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
