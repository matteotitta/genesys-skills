---
name: brand-kit
version: "3.0"
author: genesys-growth
last_updated: 2026-04-07
description: >
  Extracts visual identity from screenshots (primary) or website URLs
  (fallback) and compiles into a standardized brand system file with 8
  sections: visual identity description, colors, typography, components,
  data viz, logo usage, spacing, and signature elements. Screenshot-first
  for higher fidelity. Produces a brand-kit markdown file consumed by
  landing-page-copy, landing-page-wireframe, vibe-coding, and dashboard
  skills. Upstream: recommended company-context. NOT for voice/messaging
  context — use tov-guidelines instead.
---

# Brand Kit

Extract visual identity from screenshots and compile into a standardized brand system file. Screenshot-first approach for pixel-perfect fidelity — URL scraping available as supplementary input.

**Scope:** Visual identity only. Voice, copy, and messaging live in TOV guidelines and client CLAUDE.md — not in the brand kit.

---

## Claude Code Triggers

**Invoke this skill when:**
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
- User wants TOV/voice guidelines (use `/tov-guidelines`)
- User wants messaging/positioning (use `/product-messaging`)
- User wants competitor analysis (use `/competitor-research`)

---

## Modes

### Quick mode (default)

Use when you have screenshots and/or a website URL.

1. Analyze screenshots (or take screenshots via Playwright if URL provided)
2. Extract visual identity (colors, typography, components, effects)
3. Compile into brand system template
4. Mark gaps as [NEEDS VERIFICATION]

**Time:** ~10 minutes. **Quality:** Good for drafts, internal use, early engagement.

### Full mode

Use when you have brand guidelines PDF, Figma access, or prior work alongside screenshots.

1. Gather all sources (screenshots, Figma tokens, brand PDF)
2. Cross-reference sources for accuracy — screenshots for visual truth, docs for official values
3. Populate all 8 sections with verified data
4. Self-review against quality checklist

**Time:** ~20 minutes. **Quality:** Production-ready, client-facing.

**Trigger:** Use full mode when user says "full brand kit" or provides multiple source types.

---

## Proactive Input Prompting

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

## Input Requirements

### Required inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Screenshots** (primary) | 3-5 screenshots: homepage, about, pricing, feature page | User pastes images, provides file paths, or gives URL for auto-capture |
| **Client name** | Company name | User specification |

### Optional inputs (improve quality significantly)

| Input | How it helps |
|-------|--------------|
| Website URL | Supplementary CSS extraction — provides exact hex values, font imports, variable names |
| Figma URL | Exact tokens via Figma MCP (`get_screenshot` + `get_variable_defs`) |
| Brand PDF / style guide | Official brand assets — verified colors, fonts, usage rules |
| Logo files | Exact logo variants for Section 5 |

---

## Process (step-by-step)

### Phase 1: Capture & Analyze

**Purpose:** Collect visual data and extract design tokens from screenshots.

**Steps:**

1. **Step 1.1: Collect screenshots**
   - If user provided screenshots → use directly (images in context or file paths via Read tool)
   - If user provided URL only → use Playwright `browser_take_screenshot` on homepage, about, pricing pages
   - If user provided Figma URL → use Figma MCP `get_screenshot` + `get_design_context`
   - **Output:** 3-5 screenshots in context

2. **Step 1.2: Visual analysis of each screenshot**
   Extract from the visuals:
   - **Colors** — primary, secondary, accent, background, text, borders, gradients. Sample hex values from visible elements
   - **Typography** — font families (identify by letterform shape), sizes, weights, line heights
   - **Spacing** — padding, margins, gaps, section spacing. Identify the base unit
   - **Components** — buttons (states, shapes), cards (borders, shadows, radius), navigation, inputs
   - **Effects** — border radius scale, shadows, blur, gradients, overlays
   - **Layout** — grid system, column structure, responsive patterns
   - **Output:** Raw token inventory with confidence scores

3. **Step 1.3: (Optional) Supplementary CSS extraction**
   If URL provided, fetch pages via WebFetch or Firecrawl for:
   - CSS custom properties (`:root` variables)
   - Google Fonts imports (exact font names)
   - Tailwind config or CSS framework detection
   - Exact hex values from stylesheets

   **Platform detection strategy:**
   | Platform | Detection Signal | Extraction Strategy |
   |----------|------------------|---------------------|
   | Framer | `framerusercontent.com` URLs | Visual analysis primary (CSS compiled away) |
   | Webflow | `.w-` class prefixes | Check compiled CSS for variables |
   | Next.js | `_next/static/` paths | Parse CSS files for tokens |
   | WordPress | `/wp-content/themes/` | Theme CSS files |
   | Tailwind | Utility classes in HTML | Extract config values |
   | Custom | CSS variables in `:root` | Direct extraction |

   - **Output:** Supplementary token data

4. **Step 1.4: Cross-reference and score confidence**
   - Where visual analysis and CSS agree → confidence 5
   - CSS-only values → confidence 4
   - Visual-only values (strong evidence) → confidence 3
   - Inferred from patterns → confidence 2
   - Approximated, needs verification → confidence 1
   - Unknown/placeholder → confidence 0
   - **Output:** Final token inventory with confidence scores

**Phase 1 checkpoint:**
- [ ] At least 3 screenshots analyzed
- [ ] Colors extracted with hex values
- [ ] Typography identified (families + scale)
- [ ] Key components captured (buttons, cards minimum)
- [ ] Confidence scores assigned to all tokens

### Phase 2: Visual Description

**Purpose:** Write natural language description for vibe coding reproduction.

**Steps:**

1. **Step 2.1: Mood & atmosphere** — Emotional feeling of the design
2. **Step 2.2: Visual metaphor** — What the design evokes (specific, memorable)
3. **Step 2.3: Color story** — How colors create hierarchy and flow
4. **Step 2.4: Typography personality** — Character of the text
5. **Step 2.5: Spatial rhythm** — How space is used
6. **Step 2.6: Signature elements** — 3-5 elements that make this instantly recognizable
7. **Step 2.7: Texture & depth** — Surface quality description
8. **Step 2.8: Motion philosophy** — How things move (infer from component design)
9. **Step 2.9: Component character** — How UI elements feel
10. **Step 2.10: Prompt for reproduction** — Consolidated natural language design brief

**Phase 2 checkpoint:**
- [ ] Visual description captures design essence
- [ ] Metaphors are evocative and specific (not generic like "modern" or "clean")
- [ ] Description is reproducible by AI tools

### Phase 3: Compile Brand System

**Purpose:** Populate the brand kit template with extracted data.

**Steps:**

1. **Step 3.0: Section 0 — Visual Identity** from Phase 2 output
2. **Step 3.1: Section 1 — Colors** — primary palette (8-15 colors), text colors, color ramp, dark/light mode rules
3. **Step 3.2: Section 2 — Typography** — typefaces with fallbacks, type scale, letter spacing, CSS quick reference
4. **Step 3.3: Section 3 — Components** — primary button, secondary button, cards, navigation (all with CSS)
5. **Step 3.4: Section 4 — Data visualization** — chart color ramp, container styles, label fonts
6. **Step 3.5: Section 5 — Logo usage** — variants, rules, file paths
7. **Step 3.6: Section 6 — Spacing** — base unit, scale, container widths
8. **Step 3.7: Section 7 — Signature elements** — 3-5 distinguishing visual elements
9. **Step 3.8: "How to apply"** — consolidated rules for HTML/CSS, data viz, presentations

**Phase 3 checkpoint:**
- [ ] All 8 sections populated (or marked [NEEDS INPUT])
- [ ] Color hex values verified (not approximated without flagging)
- [ ] CSS code blocks are syntactically correct

### Phase 4: Write & Verify

**Purpose:** Write the brand kit file, verify quality.

**Steps:**

1. **Step 4.1: Write the file**
   - Use the BRAND-KIT-TEMPLATE.md structure
   - Include skill frontmatter
   - **Output:** Brand kit file written

2. **Step 4.2: Self-review**
   - Run quality checklist (see below)
   - Flag any issues before delivery
   - **Output:** Review passed or issues flagged

---

## Anti-Hallucination Guardrails

1. **Never invent hex values.** If you can't extract a color with confidence, mark it as `[NEEDS VERIFICATION]` with your best approximation and confidence score.
2. **Never invent font names.** If you can't identify the font, describe the letterform shape and suggest likely candidates marked `[NEEDS VERIFICATION]`.
3. **Never invent logo variants.** Only document logo files that actually exist in the project folder.
4. **Mark confidence levels.** Every token gets a 0-5 confidence score.
5. **Source every section.** Note whether each value came from screenshot analysis, CSS extraction, or brand PDF.
6. **Screenshots are visual truth.** When CSS and screenshots disagree, trust what you see in the screenshot — the CSS may be overridden or compiled differently.

---

## Confidence Scoring

| Score | Meaning |
|-------|---------|
| 5 | Cross-referenced: visual analysis + CSS/Figma agree |
| 4 | From CSS/code with minor inference |
| 3 | Strong visual evidence from screenshot, high confidence |
| 2 | Reasonable inference from patterns |
| 1 | Approximated, needs verification |
| 0 | Unknown, placeholder value |

---

## What Good Looks Like

### Example: Visual Description (Linear.app)

```markdown
### Mood & atmosphere
Dark, focused, and premium. The design feels like a mission control center
for serious builders — purposeful without being cold.

### Visual metaphor
"A high-end audio mixer in a professional recording studio at night —
every element precisely placed, dark surfaces that recede, and purple
accent lights that guide your attention."

### Color story
Deep black backgrounds create infinite depth while the signature purple
(#5E6AD2) marks every action point — buttons, links, and progress indicators.
The purple doesn't overwhelm; it guides. Gray text (#8A8F98) stays readable
but recessive, creating clear hierarchy.
```

**Why this is good:** Evocative metaphor, color story explains hierarchy (not just lists colors), specific hex values embedded in narrative.

### Example: Token with Confidence

```markdown
| Name | Hex | Usage | Confidence |
|------|-----|-------|------------|
| Primary | #5E6AD2 | CTAs, links, accents | 5 |
| Background | #000000 | Page background | 5 |
| Surface | #111111 | Cards, elevated surfaces | 3 |
| Text Secondary | #8A8F98 | Meta, captions | 4 |
```

### Anti-examples

| Bad | Why | Better |
|-----|-----|--------|
| "Blue color for buttons" | No hex, not reproducible | "#5E6AD2 for CTAs, hover: #4950A4" |
| "Modern sans-serif font" | Too generic | "Inter, 500 weight, via Google Fonts" |
| "Minimalist design" | Says nothing | "32px+ section padding, borderless cards on dark backgrounds" |
| Missing confidence | Can't assess reliability | Include 0-5 per token |

---

## Quality Checklist (pre-delivery)

### Extraction quality
- [ ] At least 3 screenshots analyzed
- [ ] All primary colors extracted with confidence >= 3
- [ ] Font families identified (with sources if possible)
- [ ] Key components captured with CSS

### Visual description quality
- [ ] Mood description is evocative, not generic
- [ ] Visual metaphor is specific and memorable
- [ ] Color story explains hierarchy, not just lists colors
- [ ] Signature elements are distinguishing

### Compilation quality
- [ ] All 8 sections present (even if some are [NEEDS INPUT])
- [ ] "How to apply" section covers at least 3 mediums
- [ ] Color hex values verified
- [ ] CSS code blocks are syntactically correct
- [ ] Type scale covers at least 5 sizes

---

## MCP Data Integration

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

## Reference Files

| File | Purpose |
|------|---------|
| `references/BRAND-KIT-TEMPLATE.md` | Template with placeholder sections for all 8 visual sections + How to Apply |
| `references/output-template.md` | Output documentation template |
| `references/example-genesys-growth.md` | Reference implementation: Genesys Growth extraction |
| `references/example-cursor.md` | Reference implementation: Cursor extraction |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | 2026-04-07 | Merged brand-hub compilation into brand-guidelines. Screenshot-first input. 8-section output (added Section 0: Visual Identity). Renamed to brand-kit. |
| 2.0 | 2026-01-16 | Refactored to v2.0: structured phases, Claude Code triggers, visual description framework, examples |
| 1.0 | 2025-XX-XX | Initial skill creation |
