---
name: genesys-design
version: "1.0"
last_updated: 2026-07-27
author: genesys-growth
description: |
  Generate well-branded Genesys visual assets — LinkedIn covers, Substack
  "skill of the week" covers, 1080×1350 carousels, infographics, and web
  mocks — for production or throwaway prototypes. Bundles the full Genesys
  design system: colors_and_type.css tokens (ink #181723, paper #FAFFF9,
  mint/teal #BAFDFF, lavender #939BED, violet #6400D7, General Sans Bold
  display), self-contained UI-kit HTML templates, the licensed General Sans
  family, brand assets, and impeccable-derived craft references (banned
  patterns, scoring rubric, quality library, post-render checklist). The CSS
  binding of the canonical brand kit at projects/genesys/brand/0626-brand-kit.md.
  Triggers: /genesys-design, "make a Genesys LinkedIn cover", "Genesys
  carousel", "Genesys infographic", "brand this in Genesys style".
goal: Produce on-brand Genesys visual artifacts (or production code) from the bundled tokens, UI kits, and craft references.
outcome: A brand-fidelity-checked Genesys artifact (cover / carousel / infographic / web mock) that cites colors_and_type.css tokens, passes the banned-pattern + scoring gates, and clears /design-reviewer.

primitive: design
sub_primitive: null
ontology_type: brand-kit
review_gate: 2

inputs:
  required: []
  recommended:
    - brand-kit
depends_on: []

owned_by_agent: growth
mcps_used: []

triggers:
  slash_commands:
    - /genesys-design
  natural_language:
    - make a Genesys LinkedIn cover
    - Genesys Substack cover
    - Genesys carousel
    - Genesys infographic
    - brand this in Genesys style

status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out of `assets/` and create static HTML files for the user to view, importing tokens from `colors_and_type.css`. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design (LinkedIn cover? Substack cover? Carousel? Infographic? Web mock?), ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Key files

- `README.md` — voice, content fundamentals, visual foundations, iconography
- `colors_and_type.css` — all design tokens (colors, type, spacing, radii, shadows, fonts, gradients)
- `assets/` — logos, headshots, abstract imagery, paper/print textures
- `ui_kits/{linkedin-cover,substack-cover,carousel,infographic}/` — pixel-accurate recreations
- the premium reference — non-negotiable craft guards (load every time)
- the premium reference — 5-dimension × 0-4 scorecard for self-review
- the premium reference — final ship gate
- the premium reference — distilled craft principles (layout, typeset, polish, motion, distill, harden, accessibility)
- `NOTICE.md` — Apache-2.0 attribution for impeccable-sourced content

## Brand summary

Ink (rgb 24,23,35) + paper (rgb 250,255,249) anchored by mint cyan (rgb 186,253,255); General Sans Bold display type; radial cover gradients; hard 0 4 4.25 print drop shadows; 1px black borders on infographic cards; lowercase eyebrows; right-aligned bold headlines on covers; no emoji.

## Design cycle (post-authoring phases)

Every artifact runs the relevant phases below before the model declares it complete. Skip phases that don't apply (LinkedIn covers don't need Motion or Harden; web mocks need both).

1. **Layout** → the premium reference. Confirm grid, balance, ≤7 visible decision points.
2. **Distill** → the premium reference. Cut content that doesn't serve the focal action.
3. **Typeset** → the premium reference. ≤2 font weights, General Sans Bold for display, no overused-fonts.
4. **Polish** → the premium reference. Refinement craft — corner-radius alignment, optical balance, focal hierarchy.
5. **Anti-pattern guard** → the premium reference. Non-negotiable. No gradient text, no side-stripes ≥2px, no hero-metric template, no icon-tile-above-heading, etc.
6. **Harden** (web-mock variant only) → the premium reference. Contrast, focus states, responsiveness.
7. **Self-score** → the premium reference. Score the artifact 0-4 across 5 dimensions; require ≥3/dim and zero P0/P1 findings.
8. **Final ship gate** → Run `/premortem --output` to surface failure modes, then `/design-reviewer` as the final ship-ready gate. If `/design-reviewer` is unavailable, run the premium reference end-to-end.

**Authority + shared library.** In the workspace, `.claude/rules/design-production.md` is the governing design doctrine — read it first. The four the premium reference here are self-contained copies (for cloud / portable runs) that mirror the canonical shared craft library at `.claude/skills/meta/catalog/design-reviewer/the premium reference (`anti-patterns.md`, `scoring-rubric.md`, `harden-checklist.md`, `accessibility-checklist.md`, `positive-controls.md`). Attribution for the impeccable-derived content is in `NOTICE.md`.

## Web-mock variant — chain rule

When the user requests a web mock (vs. LinkedIn/Substack/carousel/infographic):

1. Read the design-production rule (auto-loads in workspace; cite from memory if running cloud-only).
2. Convert genesys-design tokens (`colors_and_type.css`) to CSS variables in `app/globals.css`.
3. Invoke the `shadcn` Skill (via Skill tool) to install primitives.
4. Compose primitives into branded blocks; **never write custom button/card replacements** — shadcn primitives only.
5. Apply the full Design cycle including Harden (phase 6).
6. Run final `/design-reviewer` gate before declaring complete.

## Quality bar (always enforced)

- All colors reference `colors_and_type.css` tokens. No hardcoded hex.
- ≤2 brand colors per artifact. Mint cyan reserved for one focal element.
- ≤2 font weights per surface. General Sans Bold on display.
- One accent moment per surface (one CTA, one focal element).
- No emoji. Lowercase eyebrows. Right-aligned bold headlines on covers.
- 1px black borders on infographic cards. Hard 0 4 4.25 print drop shadows.
- Side-stripes ≤1px (or 0). Anything thicker reads as decoration.
- WCAG AA contrast on primary CTA and headlines (4.5:1 normal, 3:1 large).

## Final ship gate

Before declaring any artifact complete:

1. Run `/premortem --output` — surface the failure modes for this deliverable (brand drift, off-token color, illegible contrast, wrong platform dimensions) before ship.
2. Run `/design-reviewer` as the final ship-ready gate — the universal review hook for visual output. If unavailable, run the premium reference end-to-end and require the scoring-rubric total ≥14/20 with zero P0 findings.
