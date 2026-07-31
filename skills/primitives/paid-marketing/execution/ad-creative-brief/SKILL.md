---
name: ad-creative-brief
version: '1.2'
last_updated: 2026-07-30
author: genesys-growth
description: Generates creative briefs for ad designers and video production teams, bridging ad copy (what it says) with creative
  direction (what it looks like). Produces visual concept descriptions, format specifications, brand alignment notes, asset
  checklists, and production-ready handoff documents per ad variant. Requires google-ads-copy or linkedin-ads-copy output
  as input. Consumes tov-guidelines, brand-kit, and product-messaging for brand consistency. Terminal deliverable — handed
  to designer, no downstream skills. Triggered by "creative brief", "ad creative", "ad visuals", "display ads", "video ads",
  "carousel design", or "ad design brief". NOT for writing ad copy — use /google-ads-copy or /linkedin-ads-copy first.
goal: Generates creative briefs for ad designers and video production teams, bridging ad copy (what it says) with creative
  direction (what it looks like).
outcome: Generates creative briefs for ad designers and video production teams, bridging ad copy (what it says) with creative
  direction (what it looks like). Produces visual concept descriptions, format specifications, brand alignment notes, asset
  checklists, and production-ready handoff documents per...
primitive: paid-marketing
sub_primitive: execution
ontology_type: ad-creative-brief
review_gate: 2
inputs:
  required:
  - product-messaging
  - paid-campaign-strategy
  recommended:
  - tov-guidelines
  - brand-kit
  - product-messaging
- type: ad-creative-brief
  feeds_into:
  - ad-creative
depends_on:
- product-messaging
- paid-campaign-strategy
- ad-creative
owned_by_agent: paid
mcps_used: []
- gdrive
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

# Ad Creative Brief

Generate creative briefs for ad designers and video teams. Extracts messaging angles from copy skill outputs, adds visual direction, format specs per platform, and A/B test variants. Outputs a structured brief ready for design production.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`design-production.md`](../../../../../rules/design-production.md)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in ad-creative-brief |
|---|---|---|
| **R1** | Source placement | Brief is **client-team review surface** (designer hand-off). Cleaned `[VERIFIED:...]` tags in a collapsed appendix. No tags on the per-platform spec sheets. |
| **R2** | Single-doc-with-toggles | Multi-platform brief ships as one doc with toggle per platform (LinkedIn 1.91:1, LinkedIn 1:1, Meta 1:1, Meta 4:5, Meta 9:16) — not 5 sub-docs. |
| **R3** | Product-update tone | Ad copy directions frame as "[Product] does X" not "thrilled to introduce." |
| **R5** | Blog as voice anchor | When the campaign has an anchor blog, the brief specifies the blog's opening line as the hero headline across all formats. |
| **R6** | CTA hierarchy | Market-facing ads → sign-up primary, blog as fallback. Retargeting / warm-base → product-action. |
| **R9** | Action-oriented section names | "Strategy / Hero overlay / Visual direction" — action/noun-led. |

---

## Triggers

Run this skill when:

- Ad copy is written (via `/google-ads-copy` or `/linkedin-ads-copy`) and creative production needs to start
- A designer or video producer is being briefed for new campaign creative
- Existing creative is fatigued and needs refresh angles before re-shoot
- A new platform/format is being added to an existing campaign

Do NOT run when:

- Copy isn't written — run `/google-ads-copy` or `/linkedin-ads-copy` first
- The ask is a single image (not a brief) — use a designer directly
- DESIGN.md doesn't exist — pause and run `/brand-kit`

---

## The Iron Law — voice-locked

**VISUAL DIRECTION IS NOT A MOCKUP.**

The creative brief bridges copy and design. It tells the designer *what the ad should communicate* and *what it should feel like* — not pixel-perfect layouts. Overly prescriptive briefs kill creative quality. Under-specified briefs waste revision cycles.

**No exceptions:**

- "Make it blue with the logo top-left" → That's art direction, not a brief. Describe the *feeling* and *message*, let the designer compose.
- "Just use the copy as-is on a background" → Every format needs a visual concept. Text-on-gradient is not a concept.
- "We need 20 variants" → Test fewer, learn faster. 2-3 variants per test variable. Start with concept/angle, not color swaps.
- "Skip the specs, the designer knows" → Platform specs change constantly. Always include dimensions + file size limits. Google will reject non-compliant assets.

---

## DESIGN.md token contract — voice-locked

Every brief consumes the client's DESIGN.md at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md` and cites tokens explicitly. Same brand contract as the rest of the marketing surface.

| Required in every brief | Forbidden |
|-------------------------|-----------|
| DESIGN.md path referenced at top | Color descriptions without token references |
| Token-cited colors (`colors.primary` etc.) | Type styles outside `typography.*` tokens |
| Token-cited type (`typography.headline-lg` etc.) | Off-brand corner radii, custom font sizes |
| Component specs cited (`components.button-primary`) | Ad treatments that compete visually with brand surfaces |
| Do's/Don'ts as guardrails (one primary per screen, two weights max) | Inventing colors or fonts when DESIGN.md doesn't have them |

**Authority:** Full integration contract in `.claude/rules/design-production.md` (auto-loaded). When in doubt, that file wins.

**If no DESIGN.md exists:** pause and recommend running `/brand-kit` first. Do not invent tokens.

---

## A/B test hierarchy — voice-locked

Test in order. Each level has diminishing returns compared to the one above:

| Priority | Variable | What to test |
|----------|----------|-------------|
| 1 (mandatory first) | Concept/angle | Pain point vs outcome vs social proof |
| 2 | Layout/composition | Image left vs right, text overlay vs clean |
| 3 | CTA | Direct vs soft vs proof-led |
| 4 (lowest) | Color/style | Photo vs illustration |

Never test color before concept. Concept gets the largest delta in performance; color almost never moves the needle when the angle is wrong.

**Which concept to test first is the angle matrix's job** ([the premium reference](the premium reference)) — it scores the candidate angles by evidence so the mandatory first test starts from the highest-opportunity cell, not a guess.

---

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **google-ads-copy or linkedin-ads-copy** | Source copy with headlines, descriptions, formats | Required (at least one) |
| **product-messaging** | Value props, differentiators | Required |
| **paid-campaign-strategy** | Campaign architecture | Required |
| **DESIGN.md (brand-kit)** | Tokens for color, type, components | Required |
| **tov-guidelines** | Voice patterns for hero text overlays | Recommended |
| **linkedin-ad-teardown** | Competitor gaps → the matrix's competition-density axis | Recommended |

---

## Process

**Six-phase flow:** Platform/format identification → **the angle matrix** (score angle × persona × awareness on evidence, brief the top band) → Visual direction per angle → Format specs per platform → A/B test plan → Structured brief output. Full flowchart, image specs per platform (Google Display + LinkedIn), test rules, and brief quality standards in the premium reference; the scored-matrix method in [the premium reference](the premium reference).

---

## Anti-Hallucination Guardrails

1. **Never invent customer stats.** "2,000 advisers trust us" needs a verified source. Otherwise mark `[NOT AVAILABLE]` and remove.
2. **Never invent token values.** If DESIGN.md doesn't define a needed color, pause — don't guess.
3. **Never approximate platform specs.** Use the table in `process.md` or pull current values from platform docs.
4. **Never collapse angles.** If you can only generate 2 distinct angles, say so — don't pad with paraphrases.
5. **Never strip the caption requirement from video briefs.** 85% of LinkedIn video is watched muted; captions are mandatory.

---

## Quality

Self-evaluation checklist (token coverage, distinct angles, spec accuracy, test ordering), worked example (suitability-report time-savings), anti-examples (orphan hex, pixel art direction, paraphrase angles), failure-mode triage in the premium reference.

---

## Integration with Other Skills

### Upstream (consumes)

| Skill | What it provides | Required? |
|-------|-----------------|-----------|
| `google-ads-copy` or `linkedin-ads-copy` | Source copy | Required (at least one) |
| `product-messaging` | Value props, proof points | Required |
| `paid-campaign-strategy` | Campaign architecture | Required |
| `brand-kit` | DESIGN.md tokens | Required |
| `tov-guidelines` | Voice patterns for overlays | Recommended |

### Downstream

Terminal deliverable — output goes directly to a designer or video producer. No Genesys-internal downstream skill consumes this output.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

