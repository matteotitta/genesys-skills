---
name: landing-page-wireframe
version: '1.0'
last_updated: 2026-01-17
author: genesys-growth
description: Creates visual page layouts using Framer-ready component blocks. Produces block sequences, component specs, and
  responsive layout guidance for developer or designer handoff. Triggers on "wireframe", "page layout", "Framer components",
  "block sequence", "page structure", or "visual layout". Consumes landing-page-copy or product-messaging as upstream input.
  Feeds into landing-page-playground for interactive preview and Framer/Figma handoff. NOT for writing copy — use landing-page-copy
  instead.
goal: Creates visual page layouts using Framer-ready component blocks.
outcome: Creates visual page layouts using Framer-ready component blocks. Produces block sequences, component specs, and responsive
  layout guidance for developer or designer handoff. Triggers on "wireframe", "page layout", "Framer components", "block sequence",
  "page structure", or "visual layout"....
primitive: website
sub_primitive: execution
ontology_type: landing-page-copy
review_gate: 2
inputs:
  required:
  - product-messaging
  recommended: []
- type: landing-page-copy
  feeds_into:
  - website-copy
depends_on:
- product-messaging
- website-copy
owned_by_agent: growth
mcps_used:
- a1
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

# Landing Page Wireframe

Generate structured, production-ready landing page wireframes that translate positioning and messaging into visual layouts. Output as HTML/React components ready for Framer implementation or developer handoff.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`design-production.md`](../../../../../rules/design-production.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (wireframe + brief is client-team review surface — cleaned cites in appendix toggle), R3 (placeholder copy capability-led), R6 (CTA placement positions sign-up primary in hero, demo as fallback), R9 (verb-led section names + visual-component labels).

---

## Process Flowchart

Input validation → Phase 1 strategic foundation → Phase 2 section architecture → Phase 3 component output → self-evaluation → Gate 2 spot check → chain suggestions. Full ASCII flowchart in the premium reference.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Wireframe a landing page"
- "Create a landing page layout"
- "Design a homepage structure"
- "Landing page sections for [product]"
- "Page structure for [campaign]"
- "Wireframe for [URL]"
- "Layout for landing page"
- "Build a landing page"
- "Homepage wireframe"
- "LP structure"

**Do NOT invoke when:**
- User wants copy only (no structure) → Use `landing-page-copy` skill
- User wants website audit → Use `website-pm-score` skill
- User wants full brand identity → Use `brand-kit` skill
- User wants positioning strategy → Use `product-messaging` skill

---

## Input Requirements

### Required Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Product/company context** | What is being sold | User provides or fetch from company-context |
| **Page purpose** | Homepage, feature page, campaign LP, pricing | User specifies |
| **Target audience** | Who this page is for | User provides or ICP research |

### Optional Inputs (improve quality)

| Input | How It Helps |
|-------|--------------|
| Existing messaging/positioning | Ensures wireframe aligns with strategy |
| Competitor pages | Enables differentiated structure |
| Brand hub | Provides design tokens (colors, typography, components, spacing) for on-brand wireframes |
| Brand guidelines | Applies correct visual constraints |
| Conversion goal | Optimizes CTA placement and hierarchy |
| Content assets available | Photos, videos, testimonials, logos |

### Input Validation Checklist

Before proceeding, verify:
- [ ] Product/service is understood
- [ ] Page type determined (homepage, feature, campaign, pricing)
- [ ] Primary CTA defined
- [ ] Key sections identified

**If inputs are missing:** Ask for product context and page purpose. Run company-context or landing-page-copy skill first if needed.

---

## Design integration — DESIGN.md + shadcn

**Upstream contract:** This skill consumes the client's DESIGN.md file at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md`. The YAML token frontmatter (colors, typography, rounded, spacing, components) is the source of truth. The prose body explains *how to apply* the tokens.

**Web rendering path:**
1. Read DESIGN.md tokens at the start of the skill
2. Reference token names by their canonical identifier in every section spec (`colors.primary`, `typography.headline-lg`, `rounded.lg`, `spacing.md`)
3. The wireframe spec assumes downstream rendering via shadcn primitives — `<Button>`, `<Card>`, `<Form>`, `<Input>`, `<Dialog>`, `<NavigationMenu>` — composed into branded blocks (HeroSection, FeatureGrid, PricingTable, FAQ)
4. Map tokens to CSS variables in the implementation hand-off note (`--primary`, `--radius-lg`, `--font-sans`)

**Forbidden:**
- Hardcoded hex values, font names, or radii in the wireframe spec
- Recommending custom button/card/input components when shadcn primitives exist
- Section dimensions that violate the brand's spacing scale (`spacing.*`)

**Required:**
- Cite the source DESIGN.md path at the top of the wireframe spec
- Apply the brand's "Do's and Don'ts" section as wireframe constraints (one primary CTA per screen, no mixed corner radii)
- Use Tailwind utility names (`bg-primary`, `text-headline-lg`, `rounded-lg`, `p-md`) that resolve to CSS variables

**Authority:** Full integration contract in `.claude/rules/design-production.md` (auto-loaded). When in doubt, that file wins.

**If no DESIGN.md exists:** pause and recommend running `/brand-kit` first. Do not invent tokens.

**Visual-direction anchor (variant mode).** When generating variants (formerly the `/landing-page-playground` skill, merged into this skill 2026-04-29), accept a `direction=` parameter from the 5 named directions in `../../../../meta/catalog/design-reviewer/the premium reference: Editorial / Modern Minimal / Tech Utility / Brutalist / Soft Warm. Each direction maps to default dial settings per `positive-controls.md` (variance / motion / density / decoration / contrast) + 2–4 anchor brands in the 149-brand library at `projects/research/taste-library/resources/0526-open-design-design-md-library/`. Variant mode holds 4 dials constant and varies 1 to produce comparable wireframes within a direction.

---

## A1 Gallery reference (Phase 1 — visual-direction grounding)

**Default:** a1.gallery MCP, per `.claude/rules/a1-gallery-protocol.md` (auto-loaded for website-lane skills).

**When to call:** before Phase 2 Section Architecture, whenever a `direction=` parameter is supplied OR the brand has a defined visual direction in its DESIGN.md. Pulls 4–8 live reference landing pages so the wireframe is anchored against real-world precedent, not memory.

**Primary tool:** `mcp__a1__browse_websites` with these inputs:
- `typeSlug='landing'` (or `'one-page'` for single-screen builds)
- `categorySlug={resolved from client vertical — e.g. 'finance', 'ai', 'software', 'design'}`
- `styleSlugs=[...]` from the direction-to-slug mapping in `a1-gallery-protocol.md`→ a1 slug mapping":
  - Editorial → `['serif','big-type','typographic','pattern']`
  - Modern Minimal → `['minimal','clean','sans-serif','light']`
  - Tech Utility → `['techy','monospaced','dark','bento','lines']`
  - Brutalist → `['big-type','display-font','pattern','colourful','shapes']`
  - Soft Warm → `['pastel','hand-drawn','illustration','clean']`
- `mode='discovery'` (default — keeps reference sets varied per session)
- `limit=8`, `includeImages=true`

**If slugs are uncertain:** call `mcp__a1__get_design_filters` first (free, no inputs) to validate against the live taxonomy. The mapping above was probed 2026-05-17 and refreshes quarterly.

**How to use the result:** scan the returned thumbnails to confirm the direction reads correctly for the target audience; pull section-structure cues (where hero sits, how proof is sequenced, what CTA cadence looks like) into Phase 2. Cite as `[REFERENCE: a1.gallery, {slug}, accessed YYYY-MM-DD]` per `ontology.md`. NEVER copy a reference site's structure verbatim — the wireframe must apply the client's positioning + messaging, not the reference's.

**Fallback:** if a1 returns 0 results for the filter combination, drop the most specific `styleSlugs` first (e.g., remove `'bento'` before removing `'dark'`), then re-call. If still empty, fall back to the 149-brand offline taste library at `projects/research/taste-library/resources/0526-open-design-design-md-library/` and flag the gap.

**Skip the call when:** user has provided their own reference URLs (use those directly via Firecrawl); the wireframe is a refresh of an existing wireframe (use the prior reference set); the brand has no defined direction yet (run `/brand-kit` first).

---

## Process (Step-by-Step)

**Phase 1 — Strategic Foundation:** define page purpose (primary CTA + secondary goals), map visitor journey (entry, awareness, key questions), identify required sections.

**Phase 2 — Section Architecture:** design each section (hero, problem, solution, proof, objection, final CTA) with copy zones, visual hierarchy, CTA placement.

**Phase 3 — Component Output:** choose format (HTML/Tailwind, React/JSX, Markdown), generate code section-by-section with responsive + placeholder discipline, write implementation notes.

Full step-by-step methodology with checkpoints per phase in the premium reference.

---

## Section Library

3 page-type catalogs: **Homepage** (10 sections, hero → footer with required/recommended/optional flags), **Feature page** (7 sections focused on specific benefit), **Campaign landing** (6 sections optimized for single conversion). Full tables in the premium reference.

---

## Iteration Prompts

After reviewing the wireframe, ask:
1. "Want me to generate the full copy for each section?"
2. "Should I export this to Framer directly?"
3. "Want me to create mobile-specific wireframes?"
4. "Should I add animation/interaction notes?"

---

## Quality discipline

Before Gate 2 review: run the full pre-delivery quality checklist (structure + copy zones + implementation), apply Iron Law anti-hallucination guardrails (no invented logos, no fabricated metrics, all placeholders marked, copy from approved sources, asset requirements explicit). Worked example (B2B SaaS hero) + full checklist + guardrails in the premium reference.

---

## Integration with Other Skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **landing-page-copy** | Provides copy | Use copy output to fill wireframe zones |
| **website-pm-score** | Informs structure | Low-scoring categories guide section emphasis |
| **product-messaging** | Provides positioning | Messaging informs headline hierarchy |
| **brand-kit** | Provides tokens | Apply brand colors, fonts, spacing |
| **company-context** | Provides background | Understand product for accurate structure |

---

## Framer MCP Integration

When Framer MCP is connected, this skill can:

1. **Export directly to Framer** — Push wireframe as draft page
2. **Apply brand styles** — Use existing Framer design tokens
3. **Update existing pages** — Modify sections without rebuilding

**To use:** Ensure FRAMER_MCP_URL is configured in Claude Code settings.

---

## Skill Auto-Update Protocol

This skill learns from feedback and proposes its own improvements. Feedback signal detection table + reference-example capture + improvement tracking + pattern detection rules (3+ occurrence trigger) + proposed skill update format → all in the premium reference.

---

## Design cycle (post-authoring phases)

Wireframes are early-stage — only Layout / Distill / limited Typeset apply. Polish, Harden, Delight, Onboarding, Cognitive-load all happen post-wireframe in downstream skills (vibe-coding, dashboard, website-build). Each reference lives at `../../../meta/catalog/design-reviewer/the premium reference.

- **Layout** — `layout-tenets.md` (alignment grid, density budget appropriate to wireframe stage)
- **Distill** — `distill-principles.md` (every section earns its place; if a section feels speculative, mark it for the wireframe-second pass)
- **Typeset (limited)** — `typeset-principles.md` (hierarchy through size only; final type comes later)
- **Final review** — run `/design-reviewer` (note: Motion craft + A11y + Responsive integrity dimensions will be N/A for early-stage wireframes)

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

