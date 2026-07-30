---
knowledge_type: brand-kit
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 0 Context"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Brand Kit — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md` + `.claude/rules/design-production.md` (DESIGN.md spec)

## Purpose

Captures the visual identity system: design tokens (colors, typography, spacing, radii, components) plus the prose rationale (8-section markdown body per `.claude/rules/design-production.md`). The single source of truth for every visual deliverable — landing pages, decks, infographics, web builds.

## Required frontmatter fields

```yaml
client: {slug}
skill: brand-kit
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: brand-kit
sources_count:
  verified: {n}
  inferred: {n}
  estimated: {n}
  unavailable: {n}
locked_by: null
locked_date: null
review_gate_passed: null
```

Plus the **DESIGN.md token frontmatter** per `design-production.md`:

```yaml
name: "Client Brand Name"
description: "One-sentence brand identity description"

colors:
  primary: "#000000"
  # ... full palette
typography:
  display-lg: { fontFamily, fontSize, fontWeight, lineHeight, letterSpacing }
  # ... full type scale
rounded:
  sm: 4px
  # ...
spacing:
  base: 8px
  # ...
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    # ...
```

Token references use `{path.to.token}` syntax. At minimum: `colors.primary` required.

## Required body sections (in order — per design-production.md spec)

1. **Overview (or "Brand & Style")** — brand personality, target emotional response
2. **Colors** — palette rationale, semantic role per palette
3. **Typography** — typeface choices, voice expressed through type
4. **Layout (or "Layout & Spacing")** — grid model, rhythm
5. **Elevation & Depth** — visual hierarchy strategy
6. **Shapes** — corner radii, geometry language
7. **Components** — component-by-component application guidance
8. **Do's and Don'ts** — opinionated guardrails

Section order is FIXED per design-production.md.

## Optional body sections

None — the 8-section structure is the contract. Sections may be omitted if a brand truly has no convention there, but order cannot change.

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Context-tier requires ≥50% verified for source-derived claims.

Tokens themselves are authoritative declarations (not claims) — no tags needed.

Prose sections requiring tags:
- Colors section (every palette rationale grounded in client material or design audit)
- Typography section (when claiming specific typefaces from existing brand)

## Render rules per target

### gdrive (Doc — canonical)

Per architecture decision 6:
- Inter, black, plain header, page-numbered footer, native TOC
- The brand-kit's OWN colors/fonts do NOT override the Doc's render typography — the Doc renders in the canonical Genesys template (Inter, black). Tokens live in YAML for downstream consumers (Figma, web, ad creative); the Doc is a reference reader.

### gdrive (Slides) — N/A (Brand kits don't render as slides; client-facing brand decks are a separate `sales-enablement-asset`)
### gdrive (Sheet) — N/A

### notion (Page render)

- Overview = brand personality first paragraph
- H1 = "{Client} — Brand Kit"
- Each H2 = toggle block; Components toggle is the heaviest, default-collapsed
- Embed the YAML token block as a Notion code block at top of page

## Validation rules

1. All required frontmatter fields present (both Genesys + DESIGN.md token frontmatter)
2. `ontology_type` equals `brand-kit`
3. At least `colors.primary` defined in tokens
4. All 8 body sections present in canonical order
5. Token references resolve (no broken `{path.to.token}` references)
6. Components section: every defined component reuses tokens (no hardcoded hex/font/radius)
7. Contrast ratios meet WCAG AA where component backgroundColor + textColor pairs exist

## Examples in the wild

- `projects/research/taste-library/resources/0426-google-design-md/source/examples/` — DESIGN.md reference examples
- Phase 4 will produce conforming examples during rollout
