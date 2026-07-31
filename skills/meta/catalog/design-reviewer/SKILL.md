---
name: design-reviewer
version: '1.0'
last_updated: 2026-05-01
author: genesys-growth
description: 'Reviews implemented React/Tailwind/CSS output for design quality across 5 dimensions scored 0-4: anti-patterns
  (slop catalog), DESIGN.md token compliance, motion craft, accessibility essentials, responsive integrity. Produces a scored
  design-review-report with P0-P3 severity findings, anti-pattern verdict, and prioritized remediation. Triggers: "design check",
  "is this AI-slop", "audit this UI", "design quality review", "review the design", "ship-ready check". Recommended upstream:
  brand-kit (token contract). Run before shipping any visual deliverable. NOT for content voice review (use voice-reviewer)
  or skill structural review (use skill-reviewer). Hosts the shared design-quality library that output skills reference for
  internal phase work.'
goal: Score implemented design output across 5 dimensions and surface remediation actions before ship.
outcome: Scored design-review-report with anti-pattern verdict, token-citation findings, motion-craft check, P0-P3 severity tags, and prioritized remediation; unblocks the ship decision on visual deliverables. Also serves as the canonical home for shared design-quality references consumed by output skills.
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended:
  - brand-kit
- type: runbook
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /design-reviewer
  natural_language:
  - "design check this"
  - "is this AI-slop"
  - "review the design"
  - "audit this UI"
  - "design quality review"
  - "ship-ready check"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: medium
disable-model-invocation: true
---

# Design Reviewer

Review any visual deliverable for design quality across 5 dimensions, scored 0–4 each (Nielsen-style rubric, 20 points max). Produces a P0–P3 severity-tagged report with token-cited findings and prioritized remediation. Mirrors voice-reviewer's role for content — but for visual output.

This skill also hosts the **shared design-quality library** at the premium reference. Output skills (vibe-coding, dashboard, figma-prototype, website-build, website-wireframe, product-ui-frames) relative-link into these references for their internal design-cycle phases. Reference-only consumption does not require invoking this skill.

---

## Claude Code Triggers

**Invoke this skill when:**
- "design check this"
- "is this AI-slop?"
- "audit this UI"
- "review the design"
- "design quality review"
- "ship-ready check"

**Do NOT invoke when:**
- User wants content voice review → use `/voice-reviewer` instead
- User wants SKILL.md review → use `/skill-reviewer` instead
- User wants to generate UI → use `/vibe-coding`, `/dashboard`, `/website-build`, or `/figma-prototype`
- User wants brand strategy work → use `/brand-kit` instead

---

## Input Requirements

### Required inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Output to review** | The implemented UI (React/Tailwind code, screenshots, deployed URL, or Figma file) | User provides — file paths, URL, or screenshot |

### Optional inputs (improve quality)

| Input | How it helps |
|-------|--------------|
| Client name + brand-kit DESIGN.md | Activates token-compliance scoring against the client's actual tokens |
| Output type (landing page / dashboard / app / wireframe) | Adjusts dimension weighting (e.g., a wireframe doesn't need motion-craft scoring) |
| Source code context (if reviewing implemented UI) | Enables anti-pattern detection at the code level (gradient text bans, side-stripe checks, drop-shadow audits) |

### Input validation

Before proceeding, verify:
- [ ] Output is a visual deliverable (not raw text content — that's voice-reviewer's job)
- [ ] If reviewing code: source files are accessible
- [ ] If reviewing a deployed page: URL is reachable

---

## Process (step-by-step)

### Phase 1: Load context

1. **Step 1.1: Load global doctrine** — read `.claude/rules/design-production.md` (always applicable). Pull the banned-patterns list, quantitative rule patterns, and the doctrine's Do's/Don'ts.
2. **Step 1.2: Load client tokens** — if working in a client folder, read the client's brand-kit DESIGN.md. Extract the token contract (colors, typography, rounded, spacing, components). If no client context: proceed with global rules only.
3. **Step 1.3: Load shared design-quality library** — keep the premium reference, the premium reference, and the premium reference available for reference during scoring.

**Phase 1 checkpoint:**
- [ ] Doctrine loaded
- [ ] Client tokens loaded (or "global only")
- [ ] Reference library available

### Phase 2: Score 5 dimensions (0–4 each)

Use the Nielsen-style 0–4 scale per dimension. See the premium reference for full anchors. Quick form below.

1. **Dimension 1: Anti-patterns (slop catalog)** — see the premium reference for the full 25-rule catalog. Top tells: gradient text (`background-clip: text`), side-stripe borders >1px, generic drop shadows on rounded rectangles ("AI output fingerprint"), hero-metric template, icon-tile-above-heading template, glassmorphism, "gray on color" (a11y), bounce easing, overused fonts (Inter, Geist, Plus Jakarta, Fraunces, Mona Sans, Space Grotesk, Recoleta, Instrument Sans).
   - **4:** Zero anti-patterns. **3:** 1 minor tell. **2:** 2–3 tells. **1:** 4+ tells. **0:** Anti-pattern is structural (entire layout is a banned template).

2. **Dimension 2: DESIGN.md token compliance** — does the implementation cite tokens by reference, or are values hardcoded? Check for raw hex codes in component code, fonts referenced by name (not via token), radii as magic numbers.
   - **4:** All values via token references. **3:** 1–2 minor hardcodes. **2:** Several hardcodes; some tokens unused. **1:** Most values hardcoded. **0:** Component bypasses the token system entirely.

3. **Dimension 3: Motion craft** — see the premium reference. Check easing curves (no bounce/elastic for state transitions), duration (≤200ms for state, longer only with reason), `prefers-reduced-motion` respect, namespace conventions, transform-origin awareness.
   - **4:** Motion is crafted (spring physics where appropriate, reduced-motion guard, origin-aware). **3:** Generic but tasteful (linear/ease-out, ≤200ms). **2:** One issue (e.g., no reduced-motion guard). **1:** Bounce easing or generic decoration. **0:** Motion is the AI tell (animated everywhere, no purpose).
   - **N/A:** Static deliverable (wireframe, slide).

4. **Dimension 4: Accessibility essentials** — contrast ratios meet WCAG AA (4.5:1 normal, 3:1 large), semantic HTML, alt text, focus-visible states, keyboard navigation. Not a full a11y audit — just the essentials that affect ship-readiness.
   - **4:** All essentials pass. **3:** 1 minor (missing alt on decorative img). **2:** 1 contrast violation or 1 keyboard trap. **1:** Multiple essentials failing. **0:** Inaccessible (no semantic structure, no alt text, contrast violations everywhere).

5. **Dimension 5: Responsive integrity** — does the layout hold at all breakpoints? Check fixed-width violations, touch-target sizes (≥44×44px), horizontal-scroll bugs, text-scaling fallbacks, mobile-first breakpoint hygiene.
   - **4:** Holds across all breakpoints, tested. **3:** Minor issues at one breakpoint. **2:** One major issue (overflow, fixed-width hero). **1:** Multiple breakpoints broken. **0:** Desktop-only layout, mobile-broken.
   - **N/A:** Output type doesn't have multiple breakpoints (e.g., a Figma artboard locked to one device frame).

**Phase 2 checkpoint:**
- [ ] All 5 dimensions scored 0–4 (or N/A with reason)
- [ ] Each score has specific evidence (quoted code, screenshot location, or token mismatch)
- [ ] Senior-designer test: would a senior designer say this is overstyled? If yes, flag for restraint pass regardless of dimension scores. <!-- Adapted from forrestchang/andrej-karpathy-skills (MIT) -->

### Phase 3: Map findings to severity

For each finding (anything below score 4), assign severity:

- **P0** — blocks ship. Examples: contrast violation that fails WCAG AA on primary CTA, broken mobile layout, anti-pattern that defines the entire visual identity.
- **P1** — should fix before ship. Examples: gradient text on hero copy, hardcoded brand color, missing focus-visible state on primary action.
- **P2** — fix in next iteration. Examples: 1 hardcoded radius, motion duration slightly long, missing alt on decorative img.
- **P3** — log for backlog. Examples: minor copy length, optional polish missing.

### Phase 4: Generate report

Use the output format below. For each finding, quote the specific evidence (code line, hex value, breakpoint name) and suggest a concrete fix (replacement value, code pattern, or referenced design-quality library file).

---

## Motion craft — Dimension 3 in depth

Score Dimension 3 as a senior design engineer with a brutal eye for craft. The bias is toward motion that feels right, not motion that merely runs — a transition that "works" but lands from the wrong origin, fires too often, or drops frames is a regression, not a pass. Default to flagging; approval is earned. Pull the exact curves, durations, spring configs, and citations from the premium reference rather than approximating.

### The 10 non-negotiable motion standards

Every animation in the deliverable is measured against these — a violation is a finding.

1. **Justified motion** — every animation answers "why does this move?" (spatial continuity, state indication, feedback, explanation, or softening a jarring change). "It looks cool" on a frequently-seen element is a block.
2. **Frequency-appropriate** — match motion to how often it's seen. Keyboard-initiated and 100+/day actions get no animation; tens/day gets reduced motion; occasional gets standard; rare or first-time can earn delight.
3. **Responsive easing** — entering and exiting elements use `ease-out` or a strong custom curve. `ease-in` on UI is a block — it delays the moment the user watches most. Built-in easings are too weak; expect custom cubic-beziers.
4. **Sub-300ms UI** — UI animations stay under 300ms; anything slower on a UI element needs a stated reason. Per-element budgets live in the premium reference.
5. **Origin and physical correctness** — popovers, dropdowns, and tooltips scale from their trigger (`transform-origin`), never from center. Never animate from `scale(0)` — start from `scale(0.9–0.97)` + opacity. Modals are exempt — they stay centered.
6. **Interruptibility** — rapidly-triggered or gesture-driven motion (toasts, toggles, drags) must retarget from its current state — CSS transitions or springs, not keyframes that restart from zero.
7. **GPU-only properties** — animate `transform` and `opacity` only. Animating `width`/`height`/`margin`/`padding`/`top`/`left` (or Framer Motion `x`/`y` shorthands under load) is a performance finding.
8. **Accessibility** — honor `prefers-reduced-motion` (gentler, not zero: keep opacity and color, drop movement). Gate hover motion behind `@media (hover: hover) and (pointer: fine)`.
9. **Asymmetric enter/exit** — deliberate actions (a press, a hold, a destructive confirm) animate slower; system responses snap. Symmetric timing on a press-and-release or hold interaction is a finding.
10. **Cohesion** — motion matches the component's personality and the rest of the product: playful can bounce, a dashboard stays crisp. When unsure whether motion feels right, the strongest move is usually to delete it.

### Escalation triggers — flag on sight

- `transition: all` — unbounded property animation
- `scale(0)` or a pure-fade entrance with no initial transform
- `ease-in` on any UI interaction; weak built-in easing on a deliberate animation
- animation on a keyboard shortcut, command-palette toggle, or 100+/day action
- UI duration over 300ms with no stated reason
- `transform-origin: center` on a trigger-anchored popover, dropdown, or tooltip
- keyframes on toasts, toggles, or anything added or triggered rapidly
- animating layout properties — `width`/`height`/`margin`/`padding`/`top`/`left`
- Framer Motion `x`/`y`/`scale` props on motion that runs while the page is busy
- a parent CSS variable driving a child transform — a style-recalc storm
- missing `prefers-reduced-motion` handling on movement
- ungated `:hover` motion
- symmetric enter/exit timing on a press-and-release or hold interaction
- an everything-at-once entrance where a 30–80ms stagger belongs

### Remedial preference hierarchy — delete first

When proposing a fix, prefer the earliest move that resolves the finding over the later ones:

1. **Delete the animation** — high-frequency, no purpose, or keyboard-triggered.
2. **Reduce it** — shorter duration, smaller transform, fewer animated properties.
3. **Fix the easing** — swap `ease-in` → `ease-out` or a strong custom curve.
4. **Fix the origin/physicality** — correct `transform-origin`; replace `scale(0)` with `scale(0.95)` + opacity.
5. **Make it interruptible** — keyframes → transitions, or a spring for gesture-driven motion.
6. **Move it to the GPU** — layout props → `transform`/`opacity`; shorthand → the full `transform` string; WAAPI for programmatic CSS.
7. **Asymmetric timing** — slow the deliberate phase, snap the response.
8. **Polish** — blur to mask crossfades, stagger groups, `@starting-style` for entry, a spring for "alive" elements.
9. **Accessibility and cohesion** — add reduced-motion and hover gating; tune to the component's personality.

The 10 standards, escalation triggers, and remedial order are adapted from Emil Kowalski's animation philosophy (animations.dev), MIT © 2026 Emil Kowalski. As with the rest of this reviewer, the review method — non-negotiable standards, escalation triggers, and a remedial hierarchy — is adapted from aggressive code-quality review.

---

# Design Review

**Verdict:** [Ship it | Minor fixes | Fix before ship | Block]
**Total score:** X / 20
**Output type:** [Landing page | Dashboard | App | Wireframe | Other]
**Client context:** [client name or "global rules only"]

## Dimension scores

| # | Dimension | Score | Finding |
|---|-----------|-------|---------|
| 1 | Anti-patterns | 0–4 | [count of tells, top issue] |
| 2 | Token compliance | 0–4 | [hardcode count, top offenders] |
| 3 | Motion craft | 0–4 / N/A | [easing/duration verdict] |
| 4 | A11y essentials | 0–4 | [contrast/semantic/keyboard verdict] |
| 5 | Responsive integrity | 0–4 / N/A | [breakpoint verdict] |

## Findings (P0 → P3)

[For each finding:]

### [Severity] — [Dimension] — [Short label]
> [Quoted evidence — code line, hex, screenshot caption]

Fix: [specific replacement or referenced library file]

## Recommended next phases

[Pointer to relevant design-quality library files based on findings:]
- (etc.)

## Positive callouts

[Things done right — keep doing them]
```

---

## Self-roast (gut-check the report itself)

Before delivering the review, ask:

1. Is every finding backed by quoted evidence (not paraphrase)?
2. Did I score against the actual brand tokens, or against generic "good design"?
3. Are P0/P1 findings genuinely ship-blockers, or did I inflate severity?
4. Did I look for positive callouts, or only flag issues?
5. Would I be willing to defend this score to the client in a review meeting?

---

## Shared design-quality library

The 16 files inside the premium reference serve dual purpose: (a) source for design-reviewer's own scoring, (b) canonical library output skills consume via relative paths for their post-authoring phase walks.

- anti-patterns.md — 25-rule slop catalog (Apache-2.0 from impeccable)
- scoring-rubric.md — Nielsen 0–4 + P0–P3 severity
- motion-craft.md — UI motion principles
- harden-checklist.md — 9-step production-readiness pass
- polish-principles.md — 16 polish details + interaction states
- distill-principles.md — strip-to-essence guidance
- typeset-principles.md — typographic refinement
- delight-patterns.md — restrained delight (1–3 moments per screen)
- onboarding-patterns.md — in-app onboarding (welcome → first success)
- cognitive-load-tenets.md — decision-point analysis
- layout-tenets.md — spatial system (rhythm, alignment, density)
- accessibility-checklist.md — 9-priority WCAG lint, deeper than harden step 7 (MIT from ibelick/ui-skills)
- positive-controls.md — tunable design levers (bolder/softer/busier/quieter), peer to anti-patterns.md
- stack-tailwind-react.md — opinionated Tailwind + React + Motion + shadcn baseline (MIT from ibelick/ui-skills)
- visual-directions.md — 5 named visual directions with taste-library anchors
- example-report.md — anonymized worked example

---

## Anti-Hallucination Guardrails

1. **Quote actual evidence:** Every finding cites the specific code line, hex value, or screenshot location. No paraphrase.
2. **Score against tokens that exist:** If the client has no DESIGN.md, score Dimension 2 as "global rules only" and don't invent client tokens.
3. **Don't flag style preferences as violations:** Only flag rules documented in the premium reference or the client's DESIGN.md Do's/Don'ts.
4. **Be specific about fixes:** "Use a better color" is not a fix. "Replace `bg-purple-600` with `bg-primary` (resolves to the client's `colors.primary` token)" is a fix.

---

## Skill onboarding pass — for new design-output skills

When a new design-output skill is created (or significantly refactored), run this pass to verify it conforms to `.claude/rules/design-production.md`. This is the propagation hook — it ensures every future design skill (Hyperframes derivatives, dashboard variants, slide tools, etc.) inherits the design-quality discipline.

**How to invoke:** `/design-reviewer` against the new SKILL.md path. Reviewer detects target is a SKILL.md (not implemented UI) and switches to the onboarding pass.

**Six checks (mirror the doctrine's 6 contract requirements):**

1. **Brand-kit dependency** — `inputs.recommended` (or `inputs.required`) includes `brand-kit`. Severity: P1 if missing.
2. **Token-cite discipline** — body includes guidance that produced output cites DESIGN.md tokens, not hardcoded values. P2 if missing.
3. **Design cycle section present** — body has a `## Design cycle (post-authoring phases)` section walking the relevant phases per output type. P1 if missing.
4. **Cheat-sheet row added** — `.claude/rules/design-production.md` includes a row for this skill. P2 if missing.
5. **Final review gate** — body explicitly says "Run `/design-reviewer` as the final ship-ready gate". P1 if missing.
6. **Apache-2.0 attribution (if applicable)** — if the skill imports content from `design-reviewer/the premium reference (impeccable-sourced), NOTICE.md or inline attribution exists. P2 if missing.

**Runtime check:** the soft-warn version is wired into `_schema/validate-frontmatter.py` and runs on every commit. The full onboarding pass (with cheat-sheet row check + Apache attribution check) requires manual review here.

**Output format:** same scoring report as the standard 5-dimension review, but with the 6 onboarding checks substituted for the 5 dimensions. Pass = the new skill is propagation-conformant; future design output from this skill will inherit the doctrine automatically.

---

## Apache-2.0 attribution

The slop catalog (anti-patterns.md), Nielsen rubric (scoring-rubric.md), motion principles (motion-craft.md), 9-step harden checklist (harden-checklist.md), polish principles (polish-principles.md), distill principles (distill-principles.md), typeset principles (typeset-principles.md), delight patterns (delight-patterns.md), onboarding patterns (onboarding-patterns.md), cognitive-load tenets (cognitive-load-tenets.md), and layout tenets (layout-tenets.md) are sourced from [github.com/pbakaus/impeccable](https://github.com/pbakaus/impeccable) under Apache-2.0. See [NOTICE.md](./NOTICE.md) for full attribution.

---

