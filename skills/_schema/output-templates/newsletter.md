---
knowledge_type: newsletter
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 3 Content"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Newsletter — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Newsletter issue — GTM Pulse for GTM Engineer School audience, Genesys Newsletter for Genesys audience, or per-client newsletter when applicable. Drive Doc canonical (editorial review surface); Substack publishing is manual until Substack push adapter is built.

## Required frontmatter fields

```yaml
client: genesys | gtme-school | {client-slug}
skill: gtme-pulse | genesys-newsletter | newsletter
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: newsletter
issue_number: {n}                    # for series newsletters (GTM Pulse #16, etc.)
theme: {one-line theme}
sections:                            # array of section names
  - "Recent News"
  - "Hot Takes"
  - "Top GTMEs"
  - "Recommended Resources"
cohort_cta_status: active | waitlist | none   # when newsletter promotes a cohort/course
publish_target: substack | gdoc-share | other
evidence_anchored_by:
  - {path}
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order)

Section structure depends on newsletter format. For GTM Pulse:

1. **Editorial intro** — 2-3 paragraphs framing the week / theme
2. **Recent News** — 3-5 items with link, summary, "why it matters" line
3. **Hot Takes** — 1-2 opinion pieces (Matteo voice or guest)
4. **Top GTMEs** — featured creators / operators with links
5. **Recommended Resources** — 3-5 tools, articles, courses
6. **CTA block** — cohort enrollment / community join / podcast subscribe

For other newsletter formats: define sections in frontmatter, body follows declared section order.

## Optional body sections

- **Sponsor segment** — when paid sponsorship present
- **Reader Q&A** — when audience engagement segment included
- **Job board / hiring spotlight** — for community newsletters

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Content tier requires ≥40% verified.

**External URLs replace inline tags** for news/resource sections — every linked item has source URL + access date implicit in the URL.

Hot Takes section can use HTML-comment tags for substantive claims (stripped at publish).

## Render rules per target

### gdrive (Doc — canonical, for editorial review)

- Inter, black, plain header, page-numbered footer, native TOC
- Each section as H2; items within sections as bulleted lists with link, summary, why-it-matters
- For GTM Pulse, the existing `create-pulse.mjs` script is the publisher — uses Doc as input

### gdrive (Slides) — N/A
### gdrive (Sheet) — for content calendar tracking

Sheet variant: newsletter pipeline (rows: issues; columns: number, theme, draft_status, publish_date, open_rate, click_rate).

### notion (Page render — rare, when stakeholder review needed)

- Overview = editorial intro first paragraph
- H1 = "{Newsletter} #{issue_number} — {theme}"
- Each H2 (section) = toggle block

### Channel-native (canonical end-state)

After Doc review, the issue migrates to Substack (manual). The Doc remains source of truth + holds the Substack post URL once published (in `published_url:` frontmatter field).

## Validation rules

1. All required frontmatter fields present
2. `sections` array matches body section structure
3. Editorial intro: 2-3 paragraphs (not 1, not 5)
4. Each news/resource item has working URL
5. Recommended Resources section: ≥3 items
6. CTA block present (every issue has at least one ask)
7. `publish_target` enum check

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
