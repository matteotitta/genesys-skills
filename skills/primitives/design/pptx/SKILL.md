---
name: pptx
version: "3.0"
last_updated: 2026-05-04
author: genesys-growth
description: |
  Brand-agnostic PowerPoint renderer. Applies any client's brand kit (or
  Genesys's own kit) to a slide outline and produces a styled.pptx. Resolves
  brand via a 5-layer waterfall (--brand-kit-path → client kit → Genesys kit →
  gdrive-config → fallback). Reads the FULL DESIGN.md token surface — colors,
  typography, spacing, rounded, components, signature elements, presentation
  guidance, voice overrides — and applies them through a 12-type slide grammar
  bound to a locked grid system. Inherits the design library at composition
  time: impeccable banned-pattern guards, design-reviewer scoring phases,
  quantitative budgets (≤2 brand colors per slide, ≤2 font weights per slide,
  one primary per slide). Same render code path produces a ClientCo deck, an
  ClientCo deck, or a Genesys deck — only the resolved BrandConfig differs.
  Takes outlines from /sales-deck, /proposal, /webinar, /product-launch,
  /case-study, or authored manually. NOT for: writing the outline (that's the
  upstream author skills), Google Slides (use create-slides.mjs), PDF docs
  (use document-skills:pdf). Triggers: /pptx, "render this deck as PPTX",
  "make a powerpoint", "build a pptx", "branded pptx for [client]", "apply
  [client] brand to this deck", "convert this outline to slides".
goal: Apply any resolved brand kit to a slide outline and render a consistent, design-reviewed.pptx.
outcome: Validated, brand-applied.pptx with locked grid placement across slides, 12-type grammar consistency, banned-pattern-free composition, voice-override-clean text, and design-reviewer scoring.

primitive: design
sub_primitive: null
ontology_type: sales-enablement-asset
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
    - /pptx
  natural_language:
    - render this as pptx
    - make a powerpoint
    - build a pptx
    - branded pptx for
    - apply brand to this deck
    - convert this outline to slides

status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# /pptx — brand-agnostic, design-library-bound PowerPoint renderer

Apply any resolved brand kit to a slide outline and render a `.pptx` that meets the design library's quality bar. Brand-agnostic: same code path produces a ClientCo deck, an ClientCo deck, or a Genesys deck — only the resolved BrandConfig differs.

This skill is **renderer-only**, not author. The outline (titles, body, speaker notes, source-attributed claims) comes from `/sales-deck`, `/proposal`, `/webinar`, `/product-launch`, `/case-study`, or you. This skill turns that outline into a brand-applied, design-reviewer-clean deck.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Renderer skill — inherits doctrine from consuming author skills (sales-deck, proposal, webinar, etc.). Applies [[feedback_execution_doctrine_refinements_step6]] R3 (template caption library defaults to product-update tone — no "thrilled" defaults), R9 (slide-title templates verb-led). R1/R2/R5/R6/R7/R8 cascade from authoring skills per slide content.

The skill sits in `primitives/design/` next to `/dashboard`, `/figma-prototype`, `/vibe-coding` and inherits the design library at composition time:
- Layout / typeset / distill / polish / cognitive-load principles via the wrapper references

Adapted from Anthropic's `document-skills:pptx` example skill — see [`ATTRIBUTION.md`](ATTRIBUTION.md). Python tooling (XML pack/unpack, ECMA/ISO validators, soffice → pdf → jpg pipeline) preserved unchanged.

For full brand-resolution waterfall, parser spec, and token → pptxgenjs field map → the premium reference. For the 12-type slide grammar → the premium reference. For the locked-zone grid → the premium reference.

---

## Triggers

**Invoke when user says:**
- `/pptx` (with an outline path or upstream skill output)
- "render this deck as pptx"
- "make a powerpoint for [client]"
- "build a branded pptx"
- "apply [client] brand to this deck"
- "convert this outline to slides"

**Do NOT invoke when:**
- User wants to **write** a deck from positioning/messaging (use `/sales-deck`)
- User wants Google Slides output (use `cd.claude/mcp/gdrive && node create-slides.mjs`)
- User wants a PDF (use `document-skills:pdf`)
- User wants to read/extract text from an existing pptx without rendering (use `python -m markitdown file.pptx` directly)

---

## Inputs

**Required:**
- `slide_outline` — markdown file (or upstream skill output) with H1 = deck title, H2 = slide titles, bullets/paragraphs = body, optional speaker notes blocks (`> notes:` or HTML comments)

**Recommended:**
- `client_slug` — drives brand resolution. Any active client, archived client, `genesys-growth`, or whatever's defined in `gdrive-config.json`.
- `brand-kit` — pass `--brand-kit-path` for one-off external clients or non-canonical kits

**Optional:**
- `template.pptx` — existing deck to use as layout source (overrides default 12-type grammar)
- `output_path` — defaults to `projects/consulting/active/{client}/sales/execution/{MMYY}-{topic}.pptx` (or `projects/genesys/...` for Genesys)
- `--no-strict` — fall through to generic palette when no brand source resolves

---

## Prerequisites

1. **Python deps** — `pip install "markitdown[pptx]" Pillow defusedxml`
2. **pptxgenjs** — `npm install -g pptxgenjs` (set `NODE_PATH=$(npm root -g)` when running)
3. **LibreOffice** — `soffice` on PATH (for jpg renders during QA loop)
4. **Poppler** — `pdftoppm` on PATH (PDF → jpg)

The skill fails loud, not silent, when any of these are missing.

---

## Workflow at a glance (6 phases)

| # | Phase | Purpose | Output |
|---|-------|---------|--------|
| 1 | **Resolve brand** | `python3 scripts/brand_loader.py <slug> --json > /tmp/brand.json` — extracts the FULL token surface (colors, typography, spacing, rounded, components, signature elements, presentation guidance, voice overrides) | BrandConfig JSON |
| 2 | **Plan grammar** | Read outline. Pick exactly one of 12 slide types per slide. Document picks: `slide N → type=<name> reason=<why>`. Surface picks before render. | Slide-type plan |
| 3 | **Compose** | Instantiate each slide's grammar class with content + BrandConfig. Grammar classes enforce locked grid zones, banned-pattern guards, quantitative budgets. | pptxgenjs build script |
| 4 | **Render** | `BRAND_JSON=/tmp/brand.json OUT=<file>.pptx NODE_PATH=$(npm root -g) node <build>.js` | Local.pptx |
| 5 | **QA** | (a) Visual subagent jpg inspection (b) Grammar consistency audit (c) Grid-zone audit (d) Banned-pattern audit (e) Brand-agnostic audit. Loop until clean. | Audit report + clean.pptx |
| 6 | **Push** | `cd.claude/mcp/gdrive && node upload-pptx.mjs <file> <slug> "Title"` → native Google Slides URL | Drive URL |

For full per-phase detail → the premium reference.

---

## Brand resolution waterfall (5 layers, brand-agnostic)

| Layer | Source | When it fires |
|-------|--------|---------------|
| 1 | `--brand-kit-path <path>` | Explicit override — one-off / external clients / non-canonical kits |
| 2 | `projects/consulting/active/{slug}/brand/*-brand-kit.md` (latest MMYY) | Standard active-client path |
| 3 | `projects/genesys/brand/0226-design.md` | When `client_slug == "genesys-growth"` |
| 4 | `.claude/mcp/gdrive/gdrive-config.json` `clients[slug].brand` block | Legacy clients without a full kit |
| 5 | Generic fallback | Only with `--no-strict` |

Smoke-tested against ClientCo, ClientCo, ClientCo, Pivot, ClientCo, Genesys, ClientCo. Any new client onboarded via `/brand-kit` resolves immediately with zero `/pptx` code change.

For the parser spec + DESIGN.md token mapping → the premium reference.

---

## The 12-type slide grammar

Each type is a first-class artifact named for the verb of the slide's job. One type per slide.

| # | Type | Job | When to use |
|---|------|-----|-------------|
| 1 | `cover` | anchor | slide 1, establish brand + headline |
| 2 | `agenda` | map | slide 2 of decks ≥6 slides |
| 3 | `section-divider` | break | between thematic sections in 8+ slide decks |
| 4 | `narrative` | explain | text-heavy slide explaining a concept |
| 5 | `proof` | show numbers | stats, KPIs, traction metrics |
| 6 | `comparison` | contrast | before/after, with/without, us-vs-them |
| 7 | `roles` | enumerate personas | what each ICP role gets |
| 8 | `process` | show steps | how it works, timeline, sequence |
| 9 | `feature` | highlight one thing | single feature deep-dive |
| 10 | `quote` | let customer speak | testimonial, founder POV |
| 11 | `cta` | call to action | closing slide |
| 12 | `appendix` | back-pocket support | FAQ, methodology, deeper data |

Full specs (zones + token application + banned-pattern guards) → the premium reference.

---

## The locked grid system

Every slide places eyebrow / title / subtitle / body / footer / wordmark in identical zones. Zones in inches assuming `LAYOUT_WIDE` (13.333 × 7.5):

- Eyebrow row — `y=0.55, h=0.30` (0.45 on cover/cta), 12pt body-font, secondary color, charSpacing 4–6, uppercase
- Title row — `y=0.95, h=1.15`, serif heading-font, 38pt content / 54pt cover-cta / 32pt section-divider
- Hairline — `y=2.05, w=1.2", weight=2pt, color=secondary`
- Subtitle row — `y=2.20, h=0.45` (optional), 18pt body italic, muted
- Body zone — `y=2.55–6.85`, 12-col grid (col=0.92" + gutter=0.10")
- Footer — `y=7.00, h=0.30`, 10pt body-font muted, slug left + idx/total right
- Wordmark — top-right (content slides) or bottom-right (cover/cta)

No zone wanders ±0.05" between slides of the same type. Full diagram + composition budgets → the premium reference.

---

## Pre-render checklist (run before EVERY render)

- [ ] Brand resolved — `Resolved layer: N` printed (where N ≠ 5 unless explicit `--no-strict`)
- [ ] BrandConfig has full token coverage: colors + fonts + spacing + rounded + components + signature_elements + presentation_guidance + voice_overrides (warnings field flags any defaults supplied)
- [ ] Outline parsed — slide count matches user expectation
- [ ] Grammar plan written — exactly one type per slide
- [ ] No client name appears in render code (brand-agnostic check)
- [ ] No hardcoded hex codes / font names / radii / margins in render code — all values reference BrandConfig

---

## Anti-Hallucination + design-library guardrails

1. **No invented colors / logos / fonts.** Render fails loud if brand resolution falls back to defaults; never substitute "close enough" values.
2. **No invented metrics, customer logos, or quotes** in slide content. Mark unverifiable claims `[UNVERIFIED]` per `.claude/rules/ontology.md`.
3. **Voice overrides apply to ALL auto-text** (slide titles, eyebrows, footers, source citations). E.g., `no-em-dashes` strips " — " → ", ".
4. **Banned visual patterns refused at composition time** (per `.claude/rules/design-production.md` + impeccable rules in the premium reference): no gradient text, no side-stripes ≥2px, no generic drop shadows on cards, no glassmorphism, no hero-metric template, no icon-tile-above-heading template, no centered prose paragraphs, no bounce easing, no **accent line under titles** (the AI tell), and 7 more.
5. **Quantitative budgets enforced**: ≤2 brand colors per slide, ≤2 font weights per slide, 1 primary color per slide for the most important element, ≤7±2 visible options per decision point, ≤10% accent area per slide, mono font ONLY for numerical/technical content.

---

## Composition with other skills

| Stage | Skill | Why |
|-------|-------|-----|
| Before render | `/sales-deck` | Authors outline + speaker notes; chains directly into `/pptx` |
| Before render | `/proposal` | Authors proposal-shaped outline → PPTX for client meetings |
| Before render | `/case-study` | Authors customer-story outline → sales-enablement PPTX |
| Before render | `/webinar` | Authors webinar deck outline → live-event PPTX |
| Before render | `/brand-kit` | Run first if no `*-brand-kit.md` exists for the client |
| Different render target | `create-slides.mjs` | Same brand source, but Google Slides output |
| After render | `/design-reviewer` | **Final ship-ready gate** — required per `.claude/rules/design-production.md` |

---

## Design cycle (post-authoring phases)

After rendering, walk these phases. Run `/design-reviewer` as the final ship-ready gate.

- **Final review** — `/design-reviewer` (P0–P3 severity findings + remediation)

---

## Completion report

When done, output:
- Output path of rendered.pptx
- Brand source resolved (layer 1–5 + path)
- Slide count + grammar-type breakdown (e.g., "1 cover + 3 narrative + 1 proof + 1 cta")
- Logo / signature elements / voice overrides applied
- Validation status (`scripts/office/validate.py`)
- QA loop iterations to clean pass
- Brand-agnostic audit result (zero client-slug references in render code)
- Warnings (e.g., "fell through to gdrive-config layer", "no logo found")
- Suggested next: `/design-reviewer` for final ship-ready gate

---

## External References

- `.claude/rules/design-production.md` — DESIGN.md token format + shadcn integration contract + banned visual patterns + skill authorship contract
- `.claude/mcp/gdrive/gdrive-config.json` — brand-source layer 4
- `.claude/mcp/gdrive/create-slides.mjs` — sibling renderer (Google Slides flavour)
- `.claude/mcp/gdrive/upload-pptx.mjs` — auto-upload pptx to Drive folder, converts to native Google Slides
- [`LICENSE.txt`](LICENSE.txt) — Anthropic proprietary on inherited Python tooling
- [`ATTRIBUTION.md`](ATTRIBUTION.md) — lineage from `document-skills:pptx`

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

