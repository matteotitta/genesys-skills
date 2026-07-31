---
name: linkedin-carousels
version: '1.0'
last_updated: 2026-04-16
author: genesys-growth
description: 'Creates LinkedIn carousel blueprints — story arc, slide-by-slide copy, wireframe briefs, and post captions ready
  for Figma/Canva handoff. Supports 5 content types: "How I", "How to", Case study, Framework, and Listicle. Produces 12-15
  slide blueprints following Nick Broekema''s 6-part carousel framework (Cover → Context → Breakdown → Results → Recap/Bonus
  → CTA). Triggers: "carousel", "LinkedIn carousel", "slide deck for LinkedIn", "multi-slide post", "carousel about [topic]".
  Optionally consumes linkedin-content-guide for ICP alignment, tov-guidelines for voice, and brand-kit for visual identity.
  Feeds into linkedin-content for post caption generation.'
goal: Creates LinkedIn carousel blueprints — story arc, slide-by-slide copy, wireframe briefs, and post captions ready for
  Figma/Canva handoff.
outcome: 'Creates LinkedIn carousel blueprints — story arc, slide-by-slide copy, wireframe briefs, and post captions ready
  for Figma/Canva handoff. Supports 5 content types: "How I", "How to", Case study, Framework, and Listicle. Produces 12-15
  slide blueprints following Nick Broekema''s 6-part carousel...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 3
inputs:
  required: []
  recommended:
  - linkedin-content-guide
  - tov-guidelines
  - brand-kit
  - linkedin-hooks
  - genesys-design
- type: carousel-blueprint
  feeds_into:
  - linkedin-weekly-content
  - linkedin-algo-audit
depends_on:
- genesys-design
- linkedin-algo-audit
- linkedin-weekly-content
owned_by_agent: content
mcps_used: []
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

# LinkedIn Carousels

Create LinkedIn carousel blueprints that people actually finish reading. This skill produces slide-by-slide copy with wireframe briefs for Figma/Canva handoff — covering story arc, copy, layout, navigation cues, and design direction.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md), [`design-production.md`](../../../../../rules/design-production.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (slide copy is end-customer-facing — no source tags on slides; cleaned cites in caption appendix), R2 (carousel + caption + designer brief ship as one doc with toggles), R3 (slide copy capability-led, never "thrilled"), R5 (anchor post / blog opener mirrors carousel slide 1), R6 (closing slide = sign-up primary, blog as fallback), R9 (verb-led slide titles).

**Source:** Nick Broekema's carousel framework — "Create Carousels That Attract and Convert" methodology. His carousels consistently hit 68K-183K impressions with 15-27 page documents.

**What this produces:**
1. **Story arc outline** — which of the 6 framework sections each slide belongs to
2. **Slide-by-slide copy** — headline, body text, annotations per slide
3. **Wireframe brief** — layout type, visual elements, color zone, navigation cues per slide
4. **Post caption** — the LinkedIn text post that accompanies the carousel
5. **Design handoff notes** — dimensions, font hierarchy, color palette, navigation system

**How it differs from `linkedin-infographics`:** That skill creates single-image visual frameworks (Vince Pierri methodology). This skill creates multi-slide narrative documents (12-15 pages) that guide readers through a complete story arc.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Create a carousel about [topic]"
- "LinkedIn carousel for [topic]"
- "Multi-slide post about [topic]"
- "Carousel breakdown of [topic]"
- "Slide deck for LinkedIn"
- "Turn this into a carousel"

**Do NOT invoke when:**
- User wants a single-image infographic → Use `linkedin-infographics`
- User wants a text-only LinkedIn post → Use `linkedin-expert-posts` or `linkedin-personal-posts`
- User wants hook variations only → Use `linkedin-hooks`
- User wants a presentation deck → Use `pptx` skill

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Topic/angle** | What the carousel teaches | User provides |
| **Content type** | How I / How to / Case study / Framework / Listicle | User selects or inferred |
| **Target audience** | Who this is for (ICP) | User provides or from linkedin-content-guide |

### Optional (improve quality)

| Input | How It Helps |
|-------|--------------|
| Brand guidelines | Colors, fonts, visual identity for wireframe brief |
| Tone of voice | Voice calibration for slide copy |
| Proof points | Real metrics, screenshots, testimonials for Results section |
| Visual references | Example carousels to match style |
| Hook library | Pre-generated hooks from `/linkedin-hooks` |

**If inputs are missing:** Ask for topic, content type, and audience.

**Validation:**
- [ ] Topic is specific enough for 1 carousel (not 3 topics crammed together)
- [ ] Content type selected
- [ ] Target audience is clear
- [ ] Any metrics/results provided are real (not fabricated)
- [ ] Rule of Ones applies: 1 audience, 1 problem, 1 solution

---

## Design integration — DESIGN.md tokens for slide briefs

**Upstream contract:** This skill consumes the client's DESIGN.md file at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md` (or the user's own brand kit for personal-brand carousels). The YAML token frontmatter supplies the values; the prose body's "Do's and Don'ts" supplies the design guardrails.

**Carousel brief production rules:**
1. **Quote exact token values** — never describe by prose name alone:
   - ✅ `Slide background: colors.surface (#FFFFFF). Headline: typography.headline-lg (Inter 32px / 600 / 1.1 / -0.02em). Brand accent: colors.primary (#1A1C1E)`
   - ❌ `Use the brand's primary color for headlines`
2. **Reference the DESIGN.md path** at the top of the carousel brief so the Figma/Canva designer can validate
3. **Apply Do's and Don'ts as slide guardrails:**
   - "One primary color per screen" → primary used only on cover slide CTA + final CTA slide
   - "Two font weights max per surface" → no italic-bold-thin stacking on any single slide
   - "Don't mix rounded and sharp corners" → all slide elements use one radius family from `rounded.*`
4. **Include a per-slide spec table** with: token-cited background, headline type, body type, accent color, image treatment, padding from `spacing.*`
5. **Cover and CTA slides** get the strongest application of brand-primary; intermediate slides use neutrals + brand-surface

**Forbidden:** recommending color names ("vibrant orange") when token names exist; suggesting type styles outside the brand's defined `typography.*` tokens.

**Authority:** Full integration contract in `.claude/rules/design-production.md` (auto-loaded). When in doubt, that file wins.

**If no DESIGN.md exists:** pause and recommend running `/brand-kit` first. Do not invent tokens.

**Genesys render substrate:** for Genesys personal-brand carousels, use the **genesys-design** skill (`.claude/skills/primitives/design/genesys-design/`) — its `ui_kits/carousel/index.html` template + `colors_and_type.css` tokens (the CSS binding of Genesys `brand/0626-brand-kit.md`) turn the token-cited brief into a real branded HTML slide, not just a Figma/Canva handoff.

---

## The 6-Part Carousel Framework

Every carousel follows this structure. The framework is the same regardless of content type — what changes is the tone and approach within each section. Detailed per-content-type tables in the premium reference.

| # | Section | Slides | Purpose |
|---|---------|--------|---------|
| 1 | **Cover** | 1 | Grab attention. Hook headline (5-10 words, action+goal=result) + subheading + on-brand visual + author name. |
| 2 | **Context** | 1-3 | Set up the topic. Why you made this; what readers can expect. A 16-year-old should understand the topic after these slides. |
| 3 | **Breakdown** | 4-6 | Core teaching. One idea per slide. Lists over paragraphs. Visual storytelling preferred. |
| 4 | **Results** | 1-2 | Real evidence — metrics, screenshots, testimonials, before/after. Never fabricate. Mark missing data as `[NEED: real X]`. |
| 5 | **Recap/Bonus** | 1 | Reward readers. Either numbered recap or extra bonus tips beyond main content. |
| 6 | **CTA** | 1-2 | Promo CTA (conversion) + Growth CTA (follower) — best practice is both, Promo second-to-last + Growth last. |

**Total target:** 12-15 slides. Listicles can flex up to 18 when list items justify it.

---

## Slide Design Principles

Voice-locked rules — these stay in body.

### Navigation Is Everything

Navigation is the #1 reason people finish or abandon carousels. Every slide must have a forward momentum element:

| Navigation Element | Where to Use | Example |
|-------------------|-------------|---------|
| **Arrows** (→ ↓) | End of slides, next to CTAs | "Let's do a breakdown →" |
| **Breadcrumbs** | Section labels | "Framework breakdown 3/6 →" |
| **Section titles** | Top of slides | Framework section number in corner |
| **Transition prompts** | Bottom of slides | "So are carousels dead? Let's see →" |
| **Progress indicators** | Corner of slides | Section number badge (1-6) |

**Key insight from Nick:** "Have you noticed being (subconsciously) guided through this carousel with arrows, breadcrumbs, and titles? It makes people forget this carousel is 15 pages long."

### Color Breaks Signal Sections

Use different background colors for different framework sections:
- **Light** — Cover, Context slides (warm, inviting)
- **Dark** — Breakdown slides, key teaching (focus, authority)
- **Accent** — Results slides, CTA (energy, action)

### Mobile-First Design

- **Dimensions:** 1080 x 1350 pixels (portrait, optimized for mobile feed)
- **Text size:** Must be readable on phone — no tiny labels
- **Layout:** Simple, generous white space
- **Density:** Max 4-5 bullet points per slide, or 2-3 short sentences
- **Visual hierarchy:** Title → Body → Labels (3 sizes max)

### The Rule of Ones

Every carousel must follow:
- **1 audience** — Talk to one specific person
- **1 problem** — Address one specific pain
- **1 solution** — Teach one specific approach

### 5th-Grade Writing

- Simple language, short sentences
- Actionable: people understand it and can execute what you teach them TODAY
- Write in "How I..." so your audience can relate, understand, visualize, and learn

---

## Process

4-phase flow: Story Arc Design → Slide-by-Slide Copy → Wireframe Brief → Post Caption. Full step-by-step + per-content-type tables in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent metrics or results.** Mark as `[PLACEHOLDER: need real data]`
2. **Don't fabricate testimonials or screenshots.** Mark as `[NEED: real screenshot of X]`
3. **No invented case studies.** Only use real client examples
4. **Mark assumptions clearly.** Use "Example:" prefix for illustrations
5. **Results section must use real evidence** or be explicitly marked as needing it

---

## Quality

Pre-delivery checklist covers Rule of Ones, readability, story arc, navigation, and design contract (DESIGN.md token compliance). Worked examples ("How I" + Listicle) and anti-examples in the premium reference.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/voice-reviewer` — the content ship gate: voice + brand quality (pm-loop.md).

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

