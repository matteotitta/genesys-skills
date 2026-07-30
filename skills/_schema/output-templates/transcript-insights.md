---
knowledge_type: transcript-insights
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Transcript Insights — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Extracts verbatim quotes, themes, and action items from one or many call/meeting transcripts. Distinct from win-loss-analysis (which synthesizes across many calls); transcript-insights is the per-transcript or small-batch synthesis layer that win-loss + expert-pov + customer-interviews consume.

## Required frontmatter fields

```yaml
client: {slug}
skill: transcripts                   # renamed from transcript-analysis in Phase 2
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: transcript-insights
transcripts_analyzed: {n}
transcript_sources:                  # array of source identifiers (Granola IDs, YouTube URLs, file paths)
  - {source-id}
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

1. **Executive summary** — 3-5 sentences distilling the key takeaways
2. **Themes** — 3-7 recurring themes with frequency + which transcripts surfaced each
3. **Verbatim quotes** — speaker, role, transcript source, timestamp, quote text (organized by theme)
4. **Action items** — concrete next steps with owners + dates (when applicable)
5. **Open questions** — what the transcripts surfaced but didn't resolve

## Optional body sections

- **Sentiment summary** — overall positive/negative/mixed per topic
- **Speaker patterns** — when one speaker drives the themes more than others
- **Cross-references** — links to win-loss / expert-pov / case-study outputs that should consume these insights

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified.

Verbatim quotes: every quote requires `[VERIFIED: {source-type}, {source-id}, timestamp {HH:MM:SS}, accessed YYYY-MM-DD]`.

Themes inherit confidence from the quotes that ground them.

Action items: each tagged with the speaker who suggested it (or "INFERRED from theme X" if synthesized).

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Quotes as block-quotes with attribution line: "{Speaker} ({Role}) — {Source} — {Timestamp}"
- Themes as numbered list with frequency badge

### gdrive (Slides) — N/A
### gdrive (Sheet) — for batches > 10 transcripts

Sheet variant: one row per quote with columns: theme, speaker, role, source, timestamp, quote, sentiment.

### notion (Page render)

- Overview = executive summary
- H1 = "{Client} — Transcript Insights ({YYYY-MM})"
- Themes section as toggle blocks (one toggle per theme, expandable to see all quotes)
- Action items as a Notion task list

## Validation rules

1. All required frontmatter fields present
2. `transcripts_analyzed` matches `transcript_sources` array length
3. Every quote has full attribution (speaker + role + source + timestamp)
4. Themes section: ≥3 themes
5. No quotes without a verifying source

## Examples in the wild

- `projects/consulting/active/ClientCo/win-loss/0326-new-transcripts-analysis.md` (when conforming)
- Phase 4 will produce conforming examples during rollout
