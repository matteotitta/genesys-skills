---
name: brand-kit
version: '4.1'
last_updated: 2026-05-13
author: genesys-growth
description: 'Extracts visual identity from screenshots (primary) or website URLs (fallback) and compiles into a DESIGN.md-format
  brand system file: YAML token frontmatter (colors, typography, rounded, spacing, components, logo) + 9 ordered prose sections
  (Overview, Logo, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do''s and Don''ts). Screenshot-first for higher
  fidelity — Claude''s vision extracts exact colors, spacing, and component patterns directly from pixels. The YAML tokens
  are machine-authoritative and consumed directly by landing-page-wireframe, landing-page-copy, landing-page-playground, landing-page-audit,
  vibe-coding, website-build, website-copy, figma-to-prototype, dashboard, and downstream visual-brief skills (linkedin-carousels,
  linkedin-infographics, sales-deck, one-pager, ad-creative-brief). Triggers: "brand kit", "brand guidelines", "brand identity",
  "extract brand", "design system", "design tokens", "visual identity", "brand file for [client]", "DESIGN.md for [client]".
  Upstream: recommended company-context. NOT for voice/messaging context — use brand-context instead. Authority: see `.claude/rules/design-production.md`
  for the integration contract with shadcn and downstream consumers.'
goal: 'Extracts visual identity from screenshots (primary) or website URLs (fallback) and compiles into a DESIGN.md-format
  brand system file: YAML token frontmatter (colors, typography, rounded, spacing, com'
outcome: 'Extracts visual identity from screenshots (primary) or website URLs (fallback) and compiles into a DESIGN.md-format
  brand system file: YAML token frontmatter (colors, typography, rounded, spacing, components) + 8 ordered prose sections
  (Overview, Colors, Typography, Layout, Elevation & Depth,...'
primitive: research
ontology_type: brand-kit
review_gate: 2
inputs:
  required: []
  recommended:
  - company-context
outputs:
- type: brand-kit
  feeds_into:
  - landing-page-wireframe
  - website-copy
  - vibe-coding
  - website-build
  - website-copy
  - figma-to-prototype
  - dashboard
  - linkedin-carousels
  - linkedin-infographics
  - sales-deck
  - one-pager
  - ad-creative-brief
  - pptx
depends_on: []
feeds_into:
- ad-creative-brief
- dashboard
- figma-to-prototype
- website-copy
- landing-page-wireframe
- linkedin-carousels
- linkedin-infographics
- one-pager
- pptx
- sales-deck
- vibe-coding
- website-build
- website-copy
owned_by_agent: researcher
mcps_used:
- exa
- figma
- firecrawl
push_targets:
- gdrive
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

## Research substrate (Exa)

**Default:** Exa, per `.claude/rules/exa-protocol.md` (auto-loaded for research, audit, competitor, ICP, AEO, content sourcing, sales prospecting work).

**Primary tools:** `web_search_exa, web_fetch_exa`. **Use case:** fallback visual-identity reference harvest when screenshots unavailable.

**Citation:** every Exa-derived claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` per `.claude/rules/ontology.md`. **Quality gate:** ≥3 sources per major claim, ≥50% `[VERIFIED]` confidence.

---

# Brand Kit

Extract visual identity from screenshots and compile into a **DESIGN.md-format** brand system file: YAML token frontmatter (machine-authoritative) + 8 ordered prose sections (human rationale). Screenshot-first approach for pixel-perfect fidelity — URL scraping available as supplementary input.

**Scope:** Visual identity only. Voice, copy, and messaging live in TOV guidelines and client CLAUDE.md — not in the brand kit. Use `/brand-context` for voice sync.

**Authority:** This skill produces the canonical input for every downstream visual-production skill. The integration contract (how DESIGN.md flows to shadcn primitives, Figma variables, and non-web tools) is defined in `.claude/rules/design-production.md` — that file auto-loads when working on visual production. Read it before invoking this skill.

---

## Output format — DESIGN.md + HTML preview sibling

The skill emits **two files atomically** (never one without the other):

1. **Canonical `.md`** at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md` — machine-authoritative YAML frontmatter (colors, typography, rounded, spacing, components, optional logo with `{path.to.token}` cross-refs) + up to 9 ordered prose sections (Overview → Logo → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts; Logo omitted when no logo files exist).
2. **HTML preview** at `projects/consulting/{client}/brand/{MMYY}-brand-kit.html` — single self-contained page rendering the YAML tokens as visual swatches, type ramp, button states, and spacing scale. Inline CSS, no external assets. Built for stakeholder visual sign-off, not for skill consumption.

**The `.md` is canonical; the `.html` is a deterministic preview.** When prose names a color "Boston Clay" and the token is `tertiary: "#B8422E"`, the token is what renders into the HTML. The HTML can be regenerated from the `.md` at any time; the reverse is not true.

Full spec — YAML schema + all 8 section definitions: `references/output-format.md`. HTML template: `references/preview-template.html`.

**Sync between the two files is enforced by four mechanisms** (see "HTML preview sync" section below): atomic emission in this skill, pre-commit hook, stale-banner in the HTML itself, and a no-clobber guard that preserves hand-authored previews.

---

## Claude Code triggers

**Invoke when:**
- "extract brand from [company]"
- "brand kit for [client]"
- "brand guidelines for [URL]"
- "brand identity for [company]"
- "design system extraction"
- "get colors and fonts from [screenshots/URL]"
- "create brand file for [client]"
- "build brand system for [client]"
- "design tokens from [company]"
- "visual identity extraction"
- After completing initial client onboarding when brand assets are available

**Do NOT invoke when:**
- User wants TOV/voice guidelines → use `/tov-guidelines`
- User wants messaging/positioning → use `/product-messaging`
- User wants competitor analysis → use `/competitor-research`
- User wants the Genesys Growth brand → load `/genesys-brand` directly

---

## Modes

### Quick mode (default)

Use when you have screenshots and/or a website URL. Analyze screenshots → extract visual identity → compile into template → mark gaps as `[NEEDS VERIFICATION]`.

**Time:** ~10 minutes. **Quality:** Good for drafts, internal use, early engagement.

### Full mode

Use when you have brand guidelines PDF, Figma access, or prior work alongside screenshots. Gather all sources → cross-reference for accuracy → populate all 8 sections with verified data → self-review.

**Time:** ~20 minutes. **Quality:** Production-ready, client-facing.

**Trigger:** Use full mode when user says "full brand kit" or provides multiple source types.

---

## Proactive input prompting

When invoked, immediately ask for these inputs before starting:

> **Before I create the brand kit, I need:**
>
> 1. **Client name** — which client is this for?
> 2. **Screenshots** — paste or provide paths to 3-5 screenshots (homepage, about, pricing, feature page)
> 3. **Website URL** (optional) — I'll use this for supplementary CSS extraction
> 4. **Mode** — Quick (screenshots only) or Full (with brand PDF/Figma/prior work)?
> 5. **Any brand assets?** — Figma files, brand PDF, style guide, logo files?
>
> _If you give me just a URL, I'll take screenshots via Playwright and run in Quick mode._

Skip prompting if all inputs are already clear from context.

---

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Screenshots** (primary) | 3-5: homepage, about, pricing, feature page | User pastes images, file paths, or URL for auto-capture |
| **Client name** | Company name | User specification |

### Optional (improve quality significantly)

| Input | How it helps |
|-------|--------------|
| Website URL | Supplementary CSS extraction — exact hex values, font imports, variable names |
| Figma URL | Exact tokens via Figma MCP (`get_screenshot` + `get_variable_defs`) |
| Brand PDF / style guide | Official brand assets — verified colors, fonts, usage rules |
| Logo files | Logo variants + colourways for the Logo section (Section 2). File names populate the `logo:` tokens; the skill never invents variants |

### Validation

Before proceeding: at least one source available (screenshots, URL, or brand PDF); client project folder exists at `projects/consulting/{slug}/` (or will be created); template file exists at `references/BRAND-KIT-TEMPLATE.md`.

---

## Process

The brand kit runs in 4 phases. Read `references/process.md` for the full step-by-step.

Phase summary:

0. **8-dim brief parse (preprocessing).** Before any of the phases below, run the closed-vocab parser at `references/8-dim-brief-parser.md` on the client's brief. Resolves 8 dimensions (palette / accent / typography / display / layout / mood / density / constraints) + Genesys 9th dimension (evidence_weight) into closed-vocab values. Default-resolves missing dimensions transparently. Forces decision on ambiguous brief language ("professional" / "minimal" / "premium") BEFORE the open-ended interview runs.
1. **Capture & analyze** — collect screenshots, visual analysis (colors / typography / spacing / components / effects / layout), optional CSS extraction with platform detection, cross-reference and score confidence (0-5).
2. **Visual description** — mood, metaphor, color story, typography personality, spatial rhythm, signature elements, texture, motion, component character, prompt for reproduction.
3. **Compile DESIGN.md** — YAML tokens FIRST (Step 3.0), then 8 prose sections in canonical order. Tokens are machine-authoritative; prose explains.
4. **Write, lint & verify** — write file, run 8 lint rules (3 mandatory: broken-ref, primary-defined, section-order; 5 strong recommendations: contrast-ratio, typography-defined, orphaned-tokens, one-primary-per-screen, two-font-weights-max), self-review, update client CLAUDE.md, suggest downstream actions.

---

## Anti-hallucination guardrails

1. **Never invent hex values.** If you can't extract a color with confidence, mark it as `[NEEDS VERIFICATION]` with your best approximation and confidence score.
2. **Never invent font names.** If you can't identify the font, describe the letterform shape and suggest likely candidates marked `[NEEDS VERIFICATION]`.
3. **Never invent logo variants.** Only document logo files that actually exist in the project folder.
4. **Mark confidence levels.** Every token gets a 0-5 confidence score.
5. **Source every section.** Note whether each value came from screenshot analysis, CSS extraction, or brand PDF.
6. **Screenshots are visual truth.** When CSS and screenshots disagree, trust what you see in the screenshot — the CSS may be overridden or compiled differently.

---

## Quality

Pre-delivery checklist + confidence scoring + worked example (Linear.app) + anti-examples + iteration prompts library: `references/quality.md`.

---

## Integration with other skills

The DESIGN.md output is the canonical input for every visual-production skill. The contract — how tokens flow to shadcn primitives (web), Figma variables, and non-web tools — is defined in `.claude/rules/design-production.md`.

| Skill | Relationship | What it reads from DESIGN.md |
|-------|--------------|------------------------------|
| **company-context** | Upstream | (Provides company description / ICP — input, not output) |
| **brand-context** | Sibling sync | Reads voice signals → updates client CLAUDE.md |
| **landing-page-wireframe** | Downstream (web) | All tokens → wireframe spec |
| **landing-page-copy** | Downstream (web) | colors, typography, Do's/Don'ts |
| **landing-page-playground** | Downstream (web) | All tokens → multiple variants |
| **landing-page-audit** | Downstream (web) | All tokens (used as the rubric) |
| **vibe-coding** | Downstream (web) | All tokens → CSS vars + Tailwind config + shadcn components |
| **website-build** | Downstream (orchestrator) | All tokens (orchestrates brand → wireframe → copy → deploy) |
| **website-copy** | Downstream (web) | colors (semantic), typography, Do's/Don'ts |
| **figma-to-prototype** | Downstream (Figma) | All tokens → Figma variables |
| **dashboard** | Downstream (web) | colors, typography, spacing → React + shadcn + recharts |
| **linkedin-carousels** | Downstream (brief) | colors, typography, Do's/Don'ts |
| **linkedin-infographics** | Downstream (brief) | colors, typography, components |
| **sales-deck** | Downstream (brief) | colors, typography, components |
| **one-pager** | Downstream (brief) | colors, typography, spacing, components |
| **ad-creative-brief** | Downstream (brief) | colors, typography, components |

---

## MCP data integration

**Level:** 0 — Context (heavy pulls)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Playwright** | Screenshots of website pages | `browser_take_screenshot` | When user provides URL instead of screenshots |
| **Figma** | Design tokens and screenshots | `get_screenshot`, `get_variable_defs` | When user provides Figma URL |
| **Firecrawl** | Website CSS for supplementary extraction | `firecrawl_scrape` | Optional — URL provided |
| **Exa** | Brand mentions, visual identity references | `web_search_exa` | Optional enrichment |

### Fallback (no MCP)

- User-provided screenshots (always works — no MCP needed)
- WebFetch for website pages
- WebSearch for brand references

---

## HTML preview sync (4-layer defense against staling)

The `.html` preview is, by default, regenerated *from* the `.md` tokens — not edited directly. A client can opt into a richer hand-authored preview instead (see layer 4). Drift is prevented by:

1. **Atomic emission in this skill.** The Phase 3 compile step always writes *both* `.md` and `.html` in the same run. Both files carry a shared `sync_version` integer (frontmatter field on the `.md`; meta tag in the `.html`) that increments on every run.
2. **Pre-commit hook.** `.claude/hooks/pre-commit.sh` (step 6) fires on any commit touching `**/brand/MMYY-brand-kit.md`. It pipes the changed paths to `scripts/regenerate-preview.py --changed`, which reads the YAML token frontmatter, regenerates the sibling `.html` from `references/preview-template.html`, and re-stages both files. Mirrors the `skill-catalog` auto-sync pattern.
3. **Stale banner inside the HTML.** The HTML's inline script fetches its sibling `.md` on load. If the `.md` `sync_version` exceeds the HTML's embedded `sync_version`, the page renders a red banner: *"⚠ This preview is stale. Source DESIGN.md has been updated. Re-run /brand-kit to refresh."*
4. **No-clobber guard for hand-authored previews.** The regenerator never overwrites a preview a human authored. The template stamps a `brand-kit:autogen` marker into every generated file; a preview lacking that marker (or carrying an explicit `brand-kit:no-regen` comment) is treated as hand-authored and left untouched. On a source change the regenerator still bumps `sync_version` so layer 3 fires — the hand-authored preview shows the stale banner, prompting a manual refresh — but it is never clobbered. Escape hatches: delete the `.html` to get a fresh autogen preview on the next commit, or run `scripts/regenerate-preview.py <md> --force`.

Combined: drift is structurally prevented (layer 1), automatically corrected for autogen previews (layer 2), visibly flagged if both fail (layer 3), and hand-authored previews are protected from silent overwrite while still being told when they've gone stale (layer 4).

**Design decision (2026-06-30): custom previews are supported (option a), not "enrich the template until autogen always suffices" (option b).** A per-client brand kit can carry a four-tier palette, multiple typefaces, and bespoke graphic devices (e.g. ClientCo' journey-line) that a fixed 7-swatch template structurally can't represent. Rather than grow the template into an open-ended generator chasing every client's bespoke layout, the regenerator yields to a hand-authored preview when one exists. The bare template stays the zero-effort default for clients who don't need more.

### What's in the preview

The `references/preview-template.html` renders:
- **Logo grid** — the brand's logo variants (horizontal / stacked / icon) in full-colour and reversed, each on its approved background, plus clear-space + min-size rules. Rendered from the `logo:` tokens; the regenerator drops the whole section automatically when the kit has no `logo:` group
- **Color swatches** — one tile per palette color with hex label, named role (primary / secondary / tertiary / neutral / surface / on-surface / error)
- **Typography ramp** — display-lg / headline-lg / body-md / label-sm with sample text in the brand's font family
- **Button states** — primary / secondary / ghost in resting + hover styling, using the components.button-* tokens
- **Spacing scale** — visual bars showing xs / sm / md / lg / xl
- **Do's and Don'ts call-outs** — text excerpts from the prose body, surfaced visually

Stakeholder workflow: client opens HTML in browser → sees the actual palette in context → approves visually or sends back specific token-level feedback.

---

## Reference files

| File | Purpose |
|------|---------|
| `references/process.md` | Full 4-phase step-by-step (capture / describe / compile / lint) |
| `references/output-format.md` | DESIGN.md spec — YAML schema + 8 section definitions |
| `references/preview-template.html` | HTML preview template — sibling output to canonical `.md` |
| `references/quality.md` | Pre-delivery checklist + Linear.app worked example + iteration prompts |
| `references/BRAND-KIT-TEMPLATE.md` | Template with placeholder sections |
| `references/example-genesys-growth.md` | Reference implementation: Genesys Growth |
| `references/example-cursor.md` | Reference implementation: Cursor |
| `references/visual-artifact-template.md` | React component for interactive design system preview |

---

