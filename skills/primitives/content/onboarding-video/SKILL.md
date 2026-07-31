---
name: onboarding-video
version: '1.0'
last_updated: 2026-05-13
author: genesys-growth
description: Renders short, punchy onboarding videos that demonstrate a single product feature in action by animating cropped pieces of the UI (not whole screens). Output is a brand-bound MP4 via the Hyperframes engine, governed by four craft rules — UI-pieces doctrine, caption discipline, cursor discipline, stills-intake gate. Required inputs are locked brand-kit, locked positioning, locked product-messaging, and 2–4 stills per onboarding screen with intent statement per screen. Triggers on "onboarding video", "product feature demo video", "app preview video", "first-run video", "render onboarding clip", "stills-driven onboarding video". Sibling to onboarding-video-script (script-only) and product-ui-frames (generic engine).
goal: Render a brand-bound onboarding MP4 that demonstrates one product feature working, with UI pieces animated against brand-bound chrome.
outcome: A locked onboarding-video artifact — `index.html` source + MP4 output + sidecar metadata — bound to a specific brand-kit, locked positioning, locked product-messaging, and the supplied stills. The MP4 is the consumed asset; the HTML enables re-render when brand or positioning refreshes.
primitive: content
sub_primitive: motion
ontology_type: video-composition
review_gate: 3
inputs:
  required:
  - brand-kit
  - positioning
  - product-messaging
  - stills
  recommended:
  - icp-behavioural
  - tov-guidelines
  - onboarding-video-script
- type: video-composition
  feeds_into:
  - lifecycle-marketing
  - email-nurture
  - linkedin-weekly-content
depends_on:
- brand-kit
- positioning
- product-messaging
- lifecycle-marketing
- email-nurture
- linkedin-weekly-content
owned_by_agent: content
mcps_used:
- firecrawl
- notion
- gdrive
triggers:
  slash_commands:
  - /onboarding-video
  natural_language:
  - "onboarding video"
  - "product feature demo video"
  - "app preview video"
  - "first-run video"
  - "render onboarding clip"
  - "stills-driven onboarding video"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: max
---

# Onboarding Video

Renders a short, punchy onboarding video that demonstrates one product feature in action. Output is brand-bound MP4 via the Hyperframes engine. Length: 3–8 seconds per beat, stitched into a ~15–30 second video. Style: cropped pieces of the UI animating through the interaction that proves the feature works — never the whole screen.

This is the *rendered* counterpart to [`/onboarding-video-script`](../../product-marketing/execution/onboarding-video-script/SKILL.md). The script skill writes the talk track for a founder to read aloud over a screen-recorded video; this skill renders the video itself, motion-graphics style, from stills. They compose — script the talk track first, then render the visual layer (optional pairing).

Inherits the rendering engine, brand-kit binding, and DESIGN.md token contract from [`/product-ui-frames`](../product-ui-frames/SKILL.md) (the generic product-UI animation engine). Adds four craft rules on top: UI-pieces doctrine, caption discipline, cursor discipline, stills-intake gate.

The body holds decision-grade context (when to invoke, validation gate, the four rules summarised). Full craft for each rule lives in the premium reference.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`design-production.md`](../../../../rules/design-production.md) — DESIGN.md contract for visual output
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in onboarding-video |
|---|---|---|
| **R1** | Source placement (three layers) | Rendered MP4 is **end-customer-facing**. **No source frames in the video itself.** Brand-kit citations + DESIGN.md tokens live in sidecar metadata for QA only. Captions never carry `[VERIFIED:...]` overlays. |
| **R3** | Product-update tone | Captions frame as "[Product] does X" not "we are thrilled to introduce X." Even on launch-day onboarding videos. The visual demonstrates; the caption labels — neither oversells. |
| **R6** | CTA hierarchy | End-card CTA names the product-action tied to the feature being demonstrated — "open [Feature] in the dashboard" — NOT sign-up (viewer already signed up to see onboarding). Per Step 6 warm-base = product-action rule. |
| **R9** | Action-oriented section names | Caption beats are verb-led ("Connect / See the runway / Open Reporting") — not status-led ("Setup / Dashboard view / Features"). |

---

## Claude Code triggers

**Invoke when user says:**
- "Onboarding video"
- "Product feature demo video"
- "App preview / App Store preview"
- "First-run video"
- "Render onboarding clip"
- "Stills-driven onboarding video"
- "Onboarding MP4"

**Do NOT invoke when:**
- User wants a script for founder to read → [`/onboarding-video-script`](../../product-marketing/execution/onboarding-video-script/SKILL.md)
- User wants a generic brand video (no UI, no stills) → [`/product-ui-frames`](../product-ui-frames/SKILL.md)
- User wants a sales demo → `/demo-script`
- User wants a YouTube channel video → `/youtube-scripts`
- User wants in-product UI copy (tooltips, modals) — out of catalog

---

## Input requirements

### Required (all must be locked)

| Input | Description | Source |
|-------|-------------|--------|
| **brand-kit** | Locked DESIGN.md tokens (colors, typography, rounded, spacing) | `brand-kit` skill output (`status: locked`) |
| **positioning** | Locked primary anchor + differentiators the video reflects | `positioning` skill output (`status: locked`) |
| **product-messaging** | Locked messaging library — captions pull from value props | `product-messaging` skill output (`status: locked`) |
| **stills** | 2–4 screenshots per onboarding screen, with state label + intent statement per screen | User-uploaded, formatted per the premium reference |

### Recommended (improve quality)

| Input | How it helps |
|-------|--------------|
| `icp-behavioural` | Persona-specific framing of which feature to lead with |
| `tov-guidelines` | Caption tone — same rules as locked product-messaging but more granular |
| `onboarding-video-script` | If the script already exists, captions can pull headline phrasing directly |

### Validation gate — refuse to run if missing

- [ ] All four required inputs present and `status: locked` (not draft / review)
- [ ] At least one onboarding screen with 2–4 stills + state labels + intent statement
- [ ] Target duration chosen (15s / 30s / 60s)
- [ ] Aspect ratio chosen (1080×1920 portrait default; 1920×1080 landscape and 1080×1080 square allowed)

If any required input is missing or unlocked, ask before generating. Do **not** invent UI from descriptions — that's the failure this skill exists to prevent.

---

## The four craft rules (decision-grade)

Each rule has a dedicated reference file with quantitative thresholds, anti-patterns, and Hyperframes/GSAP code patterns. The summaries below are decision-grade — enough to know when a rule is violated, not enough to implement from scratch.

### Rule 1 — UI pieces, not whole screens

Each beat shows a *piece* of the feature in action: a button being tapped, a toggle flipping, a row reordering, a chart filling. Crop, mask, or extract the focal component from the supplied still and place it on a tinted brand-bound background. The rest of the UI is omitted, blurred, or implied.

Quantitative: focal element occupies ≥60% of canvas. Chrome blurred or tinted (never full opacity). One feature per beat.

Full craft → the premium reference

### Rule 2 — Caption discipline

Captions anchor to a fixed top band (200–240px reserve), rise from below (60px offset, `Easing.bezier(0.16, 1, 0.3, 1)`), ~54px @ 1080w default, weight 700. Persist across cuts when text is identical. Never below the focal UI; never drift between beats.

Full craft → the premium reference

### Rule 3 — Cursor discipline

Cursor leads every tap. Fades in at focal area center, moves in *one straight segment* to the target (any direction, including diagonal), then triggers the tap ripple. Persists across multiple taps on the same UI; resets (fade out + fresh fade-in) only on new UI. Forbidden: off-frame entry, multi-segment paths, curves, fade-out between same-UI taps.

Three primitives by function: `Pointer` (persistent dot, leads eye), `TapDot` (ripple at tap moment), `GlowRing` (illustrative-only, no tap implied). Code patterns parallel the source's Remotion components but built in Hyperframes/GSAP.

Full craft → the premium reference

### Rule 4 — Stills-intake gate

2–4 stills per onboarding screen, with state labels (resting / mid-interaction / result) and a one-sentence intent statement per screen. Refuse to run without them. This is the anti-hallucination gate — the model does not invent UI from descriptions.

Full craft → the premium reference

---

## Brand binding (required, not optional)

DESIGN.md tokens flow into the rendered output via the brand-kit-mapper inherited from `/product-ui-frames`. Per [`design-production.md`](../../../rules/design-production.md), this skill follows the canonical token-citation discipline: no hardcoded hex codes, font names, or radii in composition code. Captions, focal-area backgrounds, cursor colors, and overlay surfaces all reference DESIGN.md tokens.

Specific mappings → the premium reference.

---

## Process at a glance

| Phase | Purpose | Output |
|-------|---------|--------|
| 1. Intake | Gather brand-kit + positioning + messaging + stills with intent statements | Validation pass / fail |
| 2. Plan beats | One beat per onboarding screen; identify the focal UI piece for each | Beat list (3–5 typical) |
| 3. Compose | Build HTML composition per beat with Hyperframes blocks + craft rules | `index.html` + sidecar metadata |
| 4. Render + iterate | `npx hyperframes render` → preview → adjust timing/easing | MP4 + revision loop |

Full runbook → the premium reference.

---

## Anti-hallucination guardrails

1. **Don't invent UI from descriptions.** If a screen wasn't uploaded as a still, it doesn't go in the video. Mark missing screens as `[STILL MISSING — request from user]`.
2. **Don't invent features.** Only animate interactions the stills support (resting → mid → result).
3. **Don't invent metrics.** Captions pulled from locked product-messaging only; no "saves you N hours" claims unless that's a locked messaging value.
4. **Don't fake brand colors.** All chrome/caption/cursor colors must trace to DESIGN.md tokens; no approximation from prose.
5. **Don't skip the cursor on tap beats.** Every tap, click, or selection requires a `Pointer` that visibly travels to the target. No teleporting.

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **brand-kit** | Required upstream | DESIGN.md tokens for all visual binding |
| **positioning** | Required upstream | Primary anchor that captions reflect |
| **product-messaging** | Required upstream | Locked value props that captions pull from |
| **onboarding-video-script** | Sibling (script ↔ render pair) | Optional pairing: script first, render visual layer second |
| **product-ui-frames** | Parent (generic engine) | Inherits engine, brand-kit-mapper, output template |
| **icp-behavioural** | Recommended upstream | Persona-specific feature selection |
| **tov-guidelines** | Recommended upstream | Caption tone granularity |
| **lifecycle / email-nurture** | Downstream | Onboarding video embeds in onboarding email sequences |
| **linkedin-weekly-content** | Downstream | Short cut variant for LinkedIn distribution |
| **demo-script** | Sibling | Different audience (sales) and goal (close vs. activate) |

---

## MCP data integration

**Level:** 2 — Execution

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Product URL (web)** | Page content for caption sourcing if messaging is thin | `mcp__plugin_exa_exa__web_fetch_exa` per `.claude/rules/exa-protocol.md` | Only when locked messaging lacks specifics for a beat |
| **Product URL (clean extract)** | Rich page extract for dense feature tables | `mcp__firecrawl__firecrawl_scrape` | Fallback if Exa returns thin |
| **Stills** | User-uploaded screenshots | Direct file input | Always required |

**Fallback (no MCP):** Stills-only mode — all captions sourced from locked product-messaging, no web supplementation.

---

## Design cycle (post-authoring phases)

Per `.claude/rules/design-production.md`, run these phases before final delivery:

1. **Layout** — focal-element placement validated per `design-reviewer/the premium reference
2. **Distill** — caption text passes voice review (no banned buzzwords)
3. **Typeset** — typography tokens from brand-kit applied, no hardcoded font families
4. **Polish** — easing curves match canonical UI ease-out, no bounce on routine state transitions
5. **Harden** — passes `/design-reviewer` for final ship-ready gate
6. **Cognitive load** — ≤7±2 visible elements per beat
7. **Final review** — run `/design-reviewer` as universal review hook for visual output

---

## Attribution

This skill was developed via /steal analysis of [bidah/skill-set/create-onboarding-video](https://github.com/bidah/skill-set/blob/main/skills/create-onboarding-video/SKILL.md) (May 2026). The source repo has no LICENSE — cite-only attribution. The four craft rules (UI-pieces, caption, cursor, stills-intake) are adapted from the source's operating-rules section, rebuilt in our conventions (Hyperframes/GSAP engine, DESIGN.md token binding, B2B SaaS framing). See [`.claude/discovery/0526-bidah-create-onboarding-video-steal-analysis.md`](../../../discovery/0526-bidah-create-onboarding-video-steal-analysis.md) for the full analysis.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

