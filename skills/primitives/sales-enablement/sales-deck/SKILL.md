---
name: sales-deck
version: '1.0'
last_updated: 2026-02-06
author: genesys-growth
description: Creates sales presentation decks for prospect meetings. Produces slide-by-slide content with speaker notes, exported
  to PPTX, Google Slides, or Google Docs format. Depends on product-messaging for value propositions and consumes icp-behavioural,
  competitor-research, and positioning for audience-specific framing. Feeds into product-launch, outreach-emails, and demo-script.
  Sibling of /battlecards and /demo-script under the /sales-enablement orchestrator. Triggered by "sales deck", "pitch deck",
  "sales presentation", "slide deck", or "build a deck for [prospect]".
goal: Creates sales presentation decks for prospect meetings.
outcome: Creates sales presentation decks for prospect meetings. Produces slide-by-slide content with speaker notes, exported
  to PPTX, Google Slides, or Google Docs format. Depends on product-messaging for value propositions and consumes icp-behavioural,
  competitor-research, and positioning for...
primitive: sales-enablement
ontology_type: sales-enablement-asset
review_gate: 2
inputs:
  required: []
  recommended:
  - product-messaging
  - icp-behavioural
  - competitor-research
  - positioning
- type: sales-deck
  feeds_into:
  - product-launch
  - outreach-emails
  - demo-script
depends_on: []
- demo-script
- outreach-emails
- product-launch
owned_by_agent: sales
mcps_used:
- gdrive
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

# Sales deck

Build a 10-slide sales deck for a prospect meeting: insight-driven slide titles, speaker notes per slide, sourced claims, exportable to PPTX, Google Slides, or Google Docs. Markdown outline first, then format on user approval.

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`design-production.md`](../../../../rules/design-production.md) — DESIGN.md contract for the rendered deck
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in sales-deck |
|---|---|---|
| **R1** | Source placement (three layers) | The rendered deck is **client-team-facing** (prospect meeting). Cleaned `[VERIFIED: source, MMM YYYY]` tags live in speaker notes (rep references them on the call) and in an appendix slide if the deal requires sources. No inline source tags on the customer-facing slides themselves. |
| **R2** | Single-doc-with-toggles | Multi-deck variants for a single deal (cold pitch / discovery / pricing-conversation) ship as **one Notion doc with one toggle per variant** — not three separate PPTX exports until the variant is locked. |
| **R3** | Product-update tone | Slide titles + speaker notes frame as "we ship X" not "we are thrilled to announce." Even hero capability slides. |
| **R5** | Blog as voice anchor | When the deck is paired with an anchor blog or whitepaper, the opening slide's headline mirrors the blog's opening line. Voice consistency across deck + blog reads as one story. |
| **R6** | CTA hierarchy | Closing slide names the next step appropriate to the deal stage. Trial / pilot for cold pitch; signed proposal for warm; PoC scope for enterprise. Never "thanks for your time" close. |
| **R9** | Action-oriented section names | Insight-driven slide titles (verb-led claim) beat status-titles ("Overview / Background / About us"). |

## When to run

- User says "sales deck", "pitch deck", "sales presentation", "slide deck", or "deck for [prospect]"
- After `/messaging` completes — natural chain into a sales asset
- Sales asks for a customizable prospect deck before a demo or pitch
- Skip when the ask is competitor research (`/competitor-research`), a battlecard (`/battlecards`), a demo script (`/demo-script`), or marketing slides (different asset type)

## Inputs

**Required (at least one of each):**
- Product context — capabilities, what it does (from `/messaging`, URL, or attachment)
- Target audience — persona or segment (from `/icp-behavioural` or user)

**Recommended:** `/messaging` (value props, proof), `/icp-behavioural` (pain, triggers), `/competitor-research` (differentiation), `/positioning` (anchors), `/win-loss` (FAQ + proof).

**Optional:** brand source — `/brand-identity` DESIGN.md tokens, brand doc, or inline color/font specs. Existing template — PPTX file, Google Slides URL, or markdown outline (overrides the default 10-slide structure).

If both required inputs are missing: ask for product/company and target audience. Offer to run `/messaging` or `/icp-behavioural` first. Full input checklist + auto-routing in the premium reference.

## Steps

1. **Gather context.** Pull `/messaging`, `/icp-behavioural`, `/competitor-research`, `/positioning` outputs. Note brand source (DESIGN.md preferred). Note any user-provided template.
2. **Confirm structure.** Default = 10-slide structure (cover, social proof, problem, capabilities, differentiation, use cases/personas, how it works, pricing, CTA, FAQ — full specs in the premium reference). If user template differs, adapt: merge if fewer slides, split if more, preserve layout patterns.
3. **Apply DESIGN.md tokens.** Read `projects/consulting/{client}/brand/{MMYY}-brand-kit.md`. Quote exact token values in the spec (`colors.primary (#…)`, `typography.display-lg`). One primary color per slide. Two font weights max. Body slides never compete with title-slide primary strength. Full contract: the premium reference and `.claude/rules/design-production.md`. If no DESIGN.md exists, recommend `/brand-identity` first — never invent tokens.
4. **Generate slide outline.** Slide titles + 3-4 key points each, with content-source mapping. Insight-driven titles only ("Cut reporting time by 60%", not "Our Product Features"). Present for user approval before full content.
5. **Generate slide content.** One idea per slide, 6×6 rule (max 6 bullets, 6 words each). Headline = takeaway. Visuals over text. No invented metrics, logos, pricing, or quotes — mark unverifiable claims `[UNVERIFIED]` and ban "industry-leading", "best-in-class", "innovative".
6. **Write speaker notes per slide.** Format: WHAT TO SAY (2-3 talking-point sentences) → KEY DATA (specific numbers/dates/sources) → TRANSITION (bridge to next slide) → OBJECTION PREP (likely questions + responses).
7. **Source-validate.** Every factual claim cites a source per `.claude/rules/ontology.md` (`[VERIFIED: source]` / `[INFERRED: from X + Y]` / `[UNVERIFIED]`). Customer quotes verbatim only.
8. **Run pre-delivery checks.** Pre-delivery + self-eval rubric in the premium reference. Flag any check that fails: would this survive a CFO in the room? Does the problem slide create urgency? Is differentiation specific?
9. **Review gate (Level 2).** Present markdown deck for user approval. Actions: approve / adjust slides / change structure.
10. **Ask output format.** Markdown (default), PPTX, Google Slides, Google Docs.
11. **Export.**
    - PPTX → invoke `/pptx` (local, brand-aware) with slide content + speaker notes; `/pptx` resolves the brand kit and applies it. Falls back to `document-skills:pptx` only if the local skill is unavailable.
    - Google Slides → `cd.claude/mcp/gdrive && node create-slides.mjs "[deck.md]" "[Company]" --client {slug}`
    - Google Docs → `cd.claude/mcp/gdrive && node create-doc-unified.mjs "[deck.md]" "[Company]" --client {slug}`
12. **Suggest chains.** If approved → `/demo-script` (deck narrative informs demo flow), `/battlecards` (per competitor), `/product-launch` (deck as launch asset), `/outreach` (deck value props inform email copy).

## What good looks like

**Examples:**

**Evaluations (the deck is good when):**
- All 10 slides have insight-driven titles (passes "so what" test) and pass the 6×6 rule
- Every slide has speaker notes with WHAT TO SAY / KEY DATA / TRANSITION / OBJECTION PREP
- Every factual claim has `[VERIFIED]` / `[INFERRED]` / `[UNVERIFIED]` per ontology — no invented metrics, logos, or quotes
- Brand tokens applied: title slide uses primary color, body slides don't; two font weights max; WCAG AA on all text
- Prospect can self-identify by slide 6; clear CTA on slide 9; FAQ addresses top 5 objections from `/win-loss`
- Sales would present it without rewriting 80% of it

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/scope-guardian-reviewer` — the client-deliverable ship gate: scope-creep check on proposals/SOWs (pm-loop.md).

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
