---
name: figma-to-prototype
version: '1.0'
last_updated: 2026-03-09
author: genesys-growth
description: 'Converts Figma mockups into working prototypes by extracting design tokens (colors, typography, spacing, layout)
  and generating static HTML or interactive React code. Accepts screenshots, Figma URLs, or Figma MCP data as input. Produces
  production-ready prototype files. Triggers: "/figma-to-prototype", "turn this mockup into code", "prototype this design",
  "build this from the Figma", "convert this screenshot to a working page", user pastes screenshot with "make this work".
  NOT for wireframe descriptions — use /mockup. NOT for copy only — use /landing-page-copy. NOT for exploring Figma files
  — use Figma MCP directly.'
goal: Converts Figma mockups into working prototypes by extracting design tokens (colors, typography, spacing, layout) and
  generating static HTML or interactive React code.
outcome: Converts Figma mockups into working prototypes by extracting design tokens (colors, typography, spacing, layout)
  and generating static HTML or interactive React code. Accepts screenshots, Figma URLs, or Figma MCP data as input. Produces
  production-ready prototype files. Triggers:...
primitive: design
ontology_type: landing-page-copy
review_gate: 2
inputs:
  required:
  - landing-page-wireframe
  - brand-kit
  recommended: []
- type: landing-page-copy
  feeds_into: []
depends_on:
- landing-page-wireframe
- brand-kit
owned_by_agent: operator
mcps_used:
- figma
- gdrive
- notion
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

# /figma-to-prototype — Turn mockups into working code

Paste a Figma screenshot or provide a Figma URL and get a working prototype. Extracts design tokens (colors, typography, spacing, layout), maps components to code, and produces production-ready output. Goes beyond wireframing — this builds the actual thing.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`design-production.md`](../../../../rules/design-production.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (prototype code is internal — DESIGN.md cites inline for engineering), R3 (placeholder copy capability-led), R9 (verb-led component names).

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "/figma-to-prototype [URL or description]"
- "Turn this mockup into code"
- "Prototype this design"
- "Build this from the Figma"
- "Convert this screenshot to a working page"
- User pastes a screenshot with "make this work"

**Do NOT invoke when:**
- User wants a wireframe description (use `/mockup`)
- User wants landing page copy only (use `/landing-page-copy`)
- User wants to explore a Figma file without building (use Figma MCP directly)

---

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| Design source | Yes | Figma URL, pasted screenshot, or file path to mockup image |
| Scope | No | `static` (HTML/CSS) / `interactive` (React with state) / `full` (React with routing) — default: `static` |
| Target | No | `html-only` / `framer` / `lovable` / `local` — default: `html-only` |
| Brand hub | No | Client brand hub file for design token validation (colors, typography, components) |

---

## Design integration — DESIGN.md → Figma variables

**Upstream contract:** When prototyping for a client, this skill consumes the client's DESIGN.md file at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md`. DESIGN.md tokens map 1:1 to Figma variables via the Figma MCP.

**Token → Figma variable mapping:**

| DESIGN.md token group | Figma variable collection |
|-----------------------|---------------------------|
| `colors.*` | "Colors" collection (mode-aware: light/dark) |
| `typography.*` | "Typography" styles (text style per token) |
| `rounded.*` | "Radius" number variables |
| `spacing.*` | "Spacing" number variables |
| `components.*` | Component variants (`button-primary`, `button-primary-hover` → variant property) |

**Cross-references:** DESIGN.md `{path.to.token}` references become Figma variable aliases. `button-primary.backgroundColor: "{colors.primary}"` → Figma component variable bound to `Colors/primary`.

**Required workflow:**
1. Read DESIGN.md tokens at the start of the prototype session
2. Use Figma MCP `figma:figma-create-design-system-rules` to seed the file with brand-correct variables
3. Use `figma:figma-generate-design` to produce branded screens that reference those variables
4. Validate via `mcp__claude_ai_Figma__get_variable_defs` — every component should reference a variable, never a hardcoded value

**Forbidden:**
- Hardcoded color/font/radius values in Figma frames when a DESIGN.md token exists
- Creating prototype components that don't trace back to a DESIGN.md `components.*` entry

**Authority:** Full integration contract in `.claude/rules/design-production.md` (auto-loaded). When in doubt, that file wins.

**If no DESIGN.md exists:** pause and recommend running `/brand-kit` first. Do not invent tokens.

**Bidirectional mode.** This skill supports both directions:
- **Forward (Figma → prototype):** the original mode — read a Figma frame and generate working React code (Steps 1–5 below).
- **Inverse (DESIGN.md → Figma variables):** read the client's DESIGN.md and seed a Figma file with brand-correct variable collections (Colors / Typography / Radius / Spacing) + component variants. Use `figma:figma-create-design-system-rules` to seed, then `mcp__claude_ai_Figma__get_variable_defs` to validate. Useful for new-client onboarding (replaces manual variable setup, ~1–2 hours saved per client). The inverse mode is conceptually attributed to [`nexu-io/open-design/skills/figma-create-design-system-rules`](https://github.com/nexu-io/open-design/tree/main/skills/figma-create-design-system-rules) + the [`figma/skills`](https://github.com/figma/skills) upstream that the open-design stub points to (Apache-2.0, /steal lift 2026-05-13).

---

## Process

### Step 1: Capture the design

**From Figma URL:**
Extract `fileKey` and `nodeId` from the URL, then use Figma MCP:

```
get_design_context(fileKey, nodeId) → code hints + screenshot
get_screenshot(fileKey, nodeId) → visual reference
get_variable_defs(fileKey) → design tokens (if defined)
```

**From pasted screenshot:**
The image is already in context. Analyze it visually.

**From file path:**
Read the image file directly.

### Step 2: Analyze the design

Extract from the visual:

1. **Layout structure** — Grid system, column count, section hierarchy, responsive breakpoints
2. **Component inventory** — Header, hero, features, testimonials, CTA, footer, cards, forms, etc.
3. **Design tokens:**
   - Colors (primary, secondary, accent, background, text)
   - Typography (font families, sizes, weights, line heights)
   - Spacing (padding, margins, gaps — identify the base unit)
   - Border radius, shadows, opacity
4. **Content** — Headlines, body text, button labels, image placeholders
5. **Interactive elements** — Buttons, links, forms, toggles, tabs, modals

**Output as structured inventory:**
```
DESIGN ANALYSIS
═══════════════════════════════════════

Layout: {single-column / 2-column / grid / etc.}
Sections: {count} — {list}
Components: {list of detected components}

Tokens:
  Primary: #XXXXXX
  Secondary: #XXXXXX
  Background: #XXXXXX
  Text: #XXXXXX
  Font: {detected font or best match}
  Base spacing: {Xpx}

Interactive: {buttons, forms, etc.}
═══════════════════════════════════════
```

### Step 3: Map components to code

For each detected component, choose the implementation approach:

| Component | Static (HTML/CSS) | Interactive (React) |
|-----------|-------------------|---------------------|
| Header/Nav | Semantic HTML + Tailwind | React component with mobile menu state |
| Hero | CSS grid/flexbox | Same + CTA button handler |
| Features grid | CSS grid | Same + optional toggle/tab state |
| Testimonials | Static cards | Carousel with state |
| Pricing | Static table | Toggle (monthly/annual) |
| Form | HTML form | React form with validation |
| Footer | Semantic HTML | Same |

### Step 4: Generate code

**Static (`html-only`):**
- Single `index.html` with inline Tailwind CSS (via CDN)
- Responsive design with mobile breakpoints
- All content from the mockup included
- Placeholder images using neutral gradients or SVG patterns

**Interactive (`local`):**
- Vite + React + TypeScript + Tailwind
- Component-per-section architecture
- State management for interactive elements
- Responsive with mobile-first approach

**For Framer:**
- Use Framer MCP to create pages and components directly
- Map design tokens to Framer's styling system

**For Lovable:**
- Generate specification for `/vibe-coding` skill
- Include all design tokens and component specs

### Step 5: Verify fidelity

After generating code, create a fidelity report:

```
FIDELITY REPORT
═══════════════════════════════════════

Accurately reproduced:
  [x] Layout structure and hierarchy
  [x] Color palette (extracted tokens)
  [x] Typography hierarchy
  [x] Component placement
  [x] Responsive behavior

Interpreted (not exact):
  [~] Exact spacing values (estimated from visual)
  [~] Font choice (closest web-safe match)
  [~] Shadow values (approximated)

Missing (needs manual refinement):
  [ ] Custom illustrations (used placeholders)
  [ ] Animations/transitions
  [ ] Micro-interactions

═══════════════════════════════════════
```

### Step 6: Deploy (if target specified)

- **html-only:** Save file, open in browser for review
- **local:** Run `npm run dev` for local preview
- **framer:** Push via Framer MCP
- **lovable:** Hand off to `/vibe-coding` with Lovable target

---

## Design Token Extraction

When Figma MCP provides design variables (`get_variable_defs`), map them to a tokens file:

```json
{
  "colors": {
    "primary": "#XXXXXX",
    "secondary": "#XXXXXX",
    "accent": "#XXXXXX",
    "background": "#XXXXXX",
    "surface": "#XXXXXX",
    "text": "#XXXXXX",
    "textMuted": "#XXXXXX"
  },
  "typography": {
    "fontFamily": "Inter, sans-serif",
    "h1": { "size": "48px", "weight": "700", "lineHeight": "1.1" },
    "h2": { "size": "36px", "weight": "600", "lineHeight": "1.2" },
    "h3": { "size": "24px", "weight": "600", "lineHeight": "1.3" },
    "body": { "size": "16px", "weight": "400", "lineHeight": "1.6" },
    "small": { "size": "14px", "weight": "400", "lineHeight": "1.5" }
  },
  "spacing": {
    "base": "8px",
    "sectionGap": "96px",
    "containerMax": "1200px"
  },
  "borderRadius": {
    "small": "4px",
    "medium": "8px",
    "large": "16px",
    "full": "9999px"
  }
}
```

If no Figma variables are available, extract tokens visually from the screenshot using best judgment.

---

## Integration with existing skills

- **`/mockup`** — Can accept mockup output as input (wireframe description → prototype)
- **`/landing-page-wireframe`** — Can accept wireframe output and convert to code
- **`/vibe-coding`** — Build engine for interactive prototypes
- **`/brand-kit`** — Validates extracted tokens against established brand
- **Figma MCP** — Primary data source for design context and tokens
- **Framer MCP** — Deployment target for Framer sites

---

## Notes

- For simple screenshots, `static` mode is usually sufficient and much faster
- The quality of the prototype depends heavily on the clarity of the screenshot — high-res, full-page captures work best
- Custom illustrations and complex SVGs will be replaced with placeholders — flag these for manual replacement
- This skill produces code, not design — refinement happens in code, not back in Figma
- For client landing pages, combine with `/landing-page-copy` to ensure the copy is optimized, not just visually matched

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
