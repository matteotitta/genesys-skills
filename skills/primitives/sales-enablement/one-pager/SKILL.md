---
name: one-pager
version: '1.0'
last_updated: 2026-04-08
author: genesys-growth
description: 'Creates single-page enablement documents combining design wireframe, structured content, and polished copy.
  Supports multiple one-pager types: product overview, feature spotlight, solution brief, event recap, insight summary, competitive
  comparison. Three-phase process: wireframe layout → content structuring → copy polish. Produces markdown ready for GDocs
  or Framer export. Triggers: "one-pager", "one pager", "single page", "leave-behind", "solution brief", "product brief",
  "feature brief", "recap sheet". Consumes product-messaging and icp-behavioural for voice calibration. Feeds into content-cascade
  as a format option, sales-enablement as a leave-behind asset. NOT for multi-page landing pages — use landing-page-wireframe
  + landing-page-copy. NOT for competitive-only comparisons with feature tables — use sales-enablement/competitive-onepager-template
  directly.'
goal: Creates single-page enablement documents combining design wireframe, structured content, and polished copy.
outcome: 'Creates single-page enablement documents combining design wireframe, structured content, and polished copy. Supports
  multiple one-pager types: product overview, feature spotlight, solution brief, event recap, insight summary, competitive
  comparison. Three-phase process: wireframe layout →...'
primitive: sales-enablement
ontology_type: sales-enablement-asset
review_gate: 2
inputs:
  required: []
  recommended:
  - product-messaging
  - icp-behavioural
  - tov-guidelines
  - brand-kit
- type: one-pager
  feeds_into:
  - sales-enablement
  - gdrive-create
depends_on: []
- gdrive-create
- sales-enablement
owned_by_agent: content
mcps_used: []
- framer
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# One-Pager

Single-page enablement documents that communicate a product, feature, solution, event, insight, or competitive comparison in a format scannable in 30 seconds. Three-phase process: design the wireframe layout, fill with structured content, then polish the copy.

The body of this file holds decision-grade context (when to invoke, inputs, type-selection table, anti-hallucination guardrails, gotchas, integration). Step-by-step process, output template + worked example, quality gates, and DESIGN.md integration spec live in the premium reference.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`doc-output-structure.md`](../../../../rules/doc-output-structure.md) — GDoc/Notion structural defaults
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in one-pager |
|---|---|---|
| **R1** | Source placement (three layers) | One-pagers are **end-customer-facing** (leave-behinds, exec briefs). **No sources block.** Citations stay in working markdown for QA review only; stripped before publish. The page IS the doc. |
| **R3** | Product-update tone | Product overview / feature spotlight / solution brief variants frame as "we shipped X" not "we are thrilled to announce." Even Tier 1 launches. |
| **R6** | CTA hierarchy | Market-facing variants (product overview, feature spotlight, solution brief) → sign-up primary, blog/longer-read as fallback. Warm-base variants (event recap, insight summary) → product-action CTA. Never both. |
| **R8** | Entity-name headings | When the one-pager features a specific product/feature/event, headings repeat the entity name ("What [Product] does," "Who [Product] is for," "How [Product] is different") — not pronoun headings ("What it does"). |
| **R9** | Action-oriented section names | Use "How to sign up to [Product]" instead of "What happens next." "The problem we're solving" instead of "The problem we built for." Action over status. |

---

## Claude Code triggers

**Invoke this skill when user says:**
- "One-pager for [topic]"
- "Create a one-pager"
- "Solution brief"
- "Product brief"
- "Feature brief"
- "Leave-behind for [meeting/event]"
- "Recap sheet"
- "Single page summary"
- "One page overview"

**Do NOT invoke when:**
- User wants a multi-page landing page → Use `landing-page-wireframe` + `landing-page-copy`
- User wants a detailed competitive comparison with feature tables → Use `sales-enablement` (competitive one-pager template)
- User wants a full case study with narrative → Use `case-study`
- User wants a slide deck → Use `sales-deck`

---

## Input requirements

### Required inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Topic/subject** | What the one-pager is about | User provides |
| **One-pager type** | product / feature / solution / event recap / insight / competitive | User selects or skill infers from topic |
| **Target audience** | Who will read this (buyer persona, role, awareness level) | User provides or inferred from ICP |

### Optional inputs (improve quality)

| Input | How it helps |
|-------|--------------|
| Product messaging | Provides verified headlines, value props, proof points |
| ICP research | Calibrates language, sophistication, pain points |
| TOV guidelines | Ensures voice consistency with other client materials |
| Brand-kit | Design tokens, colors, fonts for formatted output |
| Source material | Transcript insights, research output, brief — raw content to structure |
| Metrics/data | Specific numbers to feature as callouts |
| Quotes | Verbatim customer or stakeholder quotes |

### Input validation checklist

Before proceeding, verify:
- [ ] Topic/subject is clear
- [ ] One-pager type is confirmed (or default inferred)
- [ ] Target audience identified

**If inputs are missing:** Ask for topic and audience. Default to "product overview" type unless context suggests otherwise.

---

## One-pager types (decision-grade)

### Type selection guide

| Type | Sections | Best for | Typical source |
|------|----------|----------|----------------|
| **Product overview** | Hero → Problem → Solution → Features (3) → Proof → CTA | New prospect intro, trade show handout | Product messaging, ICP research |
| **Feature spotlight** | Hero → Use case → How it works (3 steps) → Metric → CTA | Product launch leave-behind, feature announcement | Product launch brief, release notes |
| **Solution brief** | Hero → Challenge → Approach (3 bullets) → Results (3 metrics) → Quote → CTA | Post-demo follow-up, RFP response attachment | Demo notes, case study data |
| **Event recap** | Hero → Key takeaways (3-5) → Quote → Next steps | Post-event distribution, conference recap | Transcript analysis, meeting notes |
| **Insight summary** | Hero → SCQA insight → Supporting evidence → Implications → CTA | Content cascade output, research distribution | Transcript analysis, thought leadership |
| **Competitive** | At-a-glance → Feature comparison → When to choose → CTA | Competitive evaluation, sales leave-behind | Competitor research, battlecards |

Each type has a reference template in the premium reference. Load the template in Phase 1 and adapt to the specific content.

---

## Process at a glance

| Phase | Purpose | Output |
|-------|---------|--------|
| 1. Wireframe layout | Define structure before writing — type, hierarchy, constraints, approval gate | Approved wireframe |
| 2. Content structuring | Hero, body sections, proof elements (metrics + pull quote), CTA | Filled draft |
| 3. Copy polish | Voice, tightening to 500-600 words, anti-hallucination, export format | Export-ready markdown |

Full step-by-step (with checkpoints, flowchart, review gate) in the premium reference.

---

## Design integration — DESIGN.md tokens

This skill consumes the client's DESIGN.md at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md`. The token frontmatter is the source of truth for visual treatment.

**Decision-grade rules:**
- Quote exact token values (no color names — `colors.primary`, not "the brand's primary color")
- One primary color per surface (header band + single CTA only)
- Two font weights max
- Spacing on the brand's `spacing.*` scale
- If no DESIGN.md exists → pause and recommend `/brand-kit` first; do not invent tokens

Full integration contract (spec rules, forbidden patterns, output-format specifics for PDF/PPTX/web) in the premium reference. Authoritative cross-skill rules in `.claude/rules/design-production.md` (auto-loaded).

---

## Anti-hallucination guardrails

1. **Never invent metrics.** If data isn't available, use `[METRIC NEEDED]` placeholder.
2. **Never fabricate quotes.** Use verbatim from source material or `[QUOTE NEEDED]`.
3. **Never invent customer names.** Use `[CUSTOMER REFERENCE NEEDED]` or "a mid-market e-commerce company."
4. **Source everything.** Include a source line at the bottom with access dates.
5. **Mark inferences.** If a claim is inferred (not directly sourced), note it: "[INFERRED: from X + Y]".

---

## Gotchas

- **Tries to cram too much content**: The #1 failure mode. One-pagers work because they're ruthlessly prioritized. If the draft exceeds 600 words, cut sections — don't shrink font.
- **Generic hero statement**: "Our product helps companies succeed" — too vague. The hero must be specific enough that only this company could say it.
- **Multiple CTAs**: Adding a "learn more" AND "book demo" AND "download whitepaper" splits attention. One CTA. One action. One destination.
- **Missing source attribution**: Easy to forget the source line at the bottom. Always include it, even if sources are minimal.
- **Competitive type scope creep**: If the competitive comparison needs a full feature table with 10+ rows, it's not a one-pager anymore — route to `sales-enablement/competitive-onepager-template` instead.

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **content-cascade** | Upstream orchestrator | Cascade invokes one-pager (insight-summary type) as one of 5 output formats |
| **product-messaging** | Upstream context | Provides verified headlines, value props, proof points |
| **icp-behavioural** | Upstream context | Calibrates language and sophistication level |
| **sales-enablement** | Sibling | Competitive one-pagers route here or to sales-enablement depending on complexity |
| **landing-page-wireframe** | Related | For multi-page layouts; one-pager handles single-page only |
| **case-study** | Related | For full narrative customer stories; one-pager handles condensed proof |
| **transcript-analysis** | Upstream source | Provides SCQA insights for insight-summary type |
| **brand-kit** | Upstream context | Provides design tokens for formatted output |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

