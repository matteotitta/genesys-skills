---
name: design-incident-response
version: '1.0'
last_updated: 2026-05-13
author: genesys-growth
description: 'Triage decision tree for design incidents flagged by /design-reviewer
  or surfaced from a symptom report. Branches on 5 incident types: banned-pattern
  detection, contrast/a11y failure, cardocalypse (nested cards), motion overload,
  token drift. Per branch: first action, fix-time estimate, Day-0/Day-1/Day-14 sequenced
  actions, atomic-commit + before/after-screenshot pattern, hand-off target. Triggers:
  "design incident", "design triage", "what do I fix first", "design review failed",
  "fix the slop". Pairs with /design-reviewer per the audit-triage-pairing rule —
  design-reviewer measures; this decides. NOT for measurement (use /design-reviewer)
  or for content voice issues (use /voice-reviewer).'
goal: Decide what to fix first when /design-reviewer surfaces multiple findings, and sequence the remediation across Day-0/Day-1/Day-14 windows.
outcome: Triage report with branch identified, first action specified, fix-time estimate, sequenced 3-window action plan, atomic-commit + screenshot evidence pattern documented, hand-off target named.
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended:
  - design-reviewer
- type: runbook
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands:
  - /design-incident-response
  natural_language:
  - "design incident"
  - "design triage"
  - "what do I fix first"
  - "design review failed"
  - "fix the slop"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: medium
disable-model-invocation: true
---

# /design-incident-response — Triage what to fix first

`/design-reviewer` measures the design. This skill **decides what to fix first**. The pairing matters: an audit that scores 5 dimensions and surfaces 12 findings is not a remediation plan — it's a list. This skill is the decision tree.

Required pre-input: either a fresh `/design-reviewer` report OR a symptom report (the user describes what feels wrong; e.g., "this card section looks like AI slop").

For the pairing contract → see [`.claude/rules/audit-triage-pairing.md`](../../../rules/audit-triage-pairing.md).

---

## Workflow at a glance

| Step | Purpose | Output |
|---|---|---|
| 1. Read the input | Parse `/design-reviewer` report OR ask the symptom-classification questions | Symptom mapped to one of 5 branches |
| 2. Pick the branch | Match symptom to incident type (decision tree below) | Branch identified |
| 3. First action | Apply the per-branch first action (Day-0 win) | Visible change in <30 min |
| 4. Sequence Day-0/1/14 | Order remaining work across three time windows | 3-window action plan |
| 5. Atomic-commit + screenshot | One commit per fix, before/after screenshot in commit message | Reviewable git history |
| 6. Hand-off | Name the next skill that owns the next step | Hand-off log entry |

The first action is non-negotiable per branch. The full sequence is the recommended order; deviate only if the symptom report names a different priority explicitly.

---

## The 5 incident branches

### Branch 1 — Banned pattern detected

**Symptoms.** `/design-reviewer` flagged one or more banned-pattern hits from `anti-patterns.md`. Top offenders by frequency: gradient text (`background-clip: text` with a gradient), side-stripe borders (`border-left` ≥2px as a colored stripe), generic drop shadows on rounded rectangles, hero-metric template layouts (giant number + tiny label as the hero), icon-tile-above-heading template layouts, glassmorphism (`backdrop-filter: blur(...)`) on arbitrary surfaces, cardocalypse (3+ nested cards), centered prose paragraphs (>1 sentence centered).

**First action (Day-0, <30 min).** Pick the SINGLE most visible offender on the homepage / hero / landing-page-above-fold. Remove it. Don't replace it yet — just remove. Take a before/after screenshot. Commit: `fix(design): remove {pattern} from {component}`.

**Day-0 (rest).** Sweep the rest of the homepage for the same pattern. Remove all instances. One commit per component, with before/after screenshot.

**Day-1.** Sweep the remaining pages (pricing, product, blog template). Apply the same sweep. Re-run `/design-reviewer` on the homepage to confirm the branch is closed.

**Day-14.** Add the banned pattern to the project's CI lint (CSS lint rule, eslint rule, or stylelint plugin) so the pattern can't be reintroduced. Cite `anti-patterns.md` in the lint rule comment.

**Hand-off.** Back to `/design-reviewer` for re-measurement. If new patterns surface, re-enter this branch.

---

### Branch 2 — Contrast / a11y fail

**Symptoms.** `/design-reviewer` flagged WCAG AA contrast violations (text below 4.5:1 for normal, 3:1 for large), missing focus-visible outlines on interactive elements, "gray on color" findings (light label on accent background), color-only meaning (status indicated by hue alone).

**First action (Day-0, <30 min).** Run the page through a contrast checker (Stark, axe DevTools, or `mcp__chrome-devtools__lighthouse_audit`) and identify the WORST contrast violation (lowest ratio, most-visible component). Fix that one element. Screenshot before/after. Commit: `fix(a11y): contrast {component} {old-ratio}→{new-ratio}`.

**Day-0 (rest).** Fix every violation below 3:1. These are not WCAG AA failures only — they're often illegible to a sighted user too.

**Day-1.** Fix violations between 3:1 and 4.5:1 (large-text-safe but normal-text-failing). Add a `:focus-visible` style to every interactive element. Re-run `/design-reviewer` to confirm a11y dimension passes.

**Day-14.** Add automated a11y testing (axe-core, pa11y, or Lighthouse CI) to the deploy pipeline. Target: 0 contrast violations on PR. Document the policy in `docs/a11y-policy.md`.

**Hand-off.** Back to `/design-reviewer` for re-measurement. If the brand's tokens themselves are the problem (e.g., the brand's default body-on-surface fails 4.5:1), hand off to `/brand-kit` to revise the token values.

---

### Branch 3 — Cardocalypse (nested cards)

**Symptoms.** `/design-reviewer` flagged 3+ levels of nested cards. Symptom report: "this page feels visually noisy / busy / claustrophobic." Common cause: card-in-card-in-card pattern from a UI library default + a "make it more designed" iteration.

**First action (Day-0, <30 min).** Pick the deepest-nested card stack on the most-visible page. Flatten ONE level — promote the innermost card's content to a section with whitespace separation; delete the innermost card border / background. Screenshot before/after. Commit: `fix(design): flatten card nesting in {component}`.

**Day-0 (rest).** Walk the rest of the homepage. For each card stack >2 levels deep: flatten to ≤2 levels. Use whitespace, dividers, or section spacing instead of additional card frames.

**Day-1.** Sweep all pages. Establish a project-wide rule: max 2 levels of containment. Document in `docs/design-rules.md`.

**Day-14.** Audit the design system / token file. If the Card component defaults encourage nesting (e.g., the Card variant ships with internal padding that nests Cards visibly), revise the variant to discourage it.

**Hand-off.** `/landing-page-wireframe` or `/website-build` if the underlying layout decision needs rework. Otherwise back to `/design-reviewer`.

---

### Branch 4 — Motion overload

**Symptoms.** `/design-reviewer` flagged >3 motion moments per visible screen, or bounce easing (`cubic-bezier(...,1.55)`) on routine state transitions (hover/click on standard buttons), or motion durations >200ms on state transitions, or animations triggering simultaneously on scroll.

**First action (Day-0, <30 min).** Disable bounce easing on every routine state transition (hover, click, focus). Replace with standard ease (e.g., `cubic-bezier(0.4, 0, 0.2, 1)`) at 150ms duration. Screenshot before/after a hover state. Commit: `fix(motion): replace bounce easing on routine state transitions`.

**Day-0 (rest).** Audit the page for motion-on-scroll triggers. Disable everything except a single hero entrance (if any). Keep entry/exit motion for modal/drawer surfaces — those are functional, not decorative.

**Day-1.** Set project-wide motion budget: ≤3 motion moments per screen, all routine state transitions ≤200ms, only entry/exit motion may run 300–600ms. Document in `docs/motion-rules.md` (or extend `design-reviewer/the premium reference into the project repo).

**Day-14.** Add a `prefers-reduced-motion` media query that disables non-essential motion entirely. Re-run `/design-reviewer` on the homepage and a feature page to confirm motion dimension passes.

**Hand-off.** `/video-frames` if the issue is in a video composition. `/vibe-coding` if the motion is in shipped code. Otherwise back to `/design-reviewer`.

**Remedial preference hierarchy (delete first).** When you pick a fix for a motion finding, reach for the earliest move that resolves it before any later one:

1. **Delete** — high-frequency, no purpose, or keyboard-triggered motion. Removing it is the fix.
2. **Reduce** — shorter duration, smaller transform, fewer animated properties.
3. **Fix the easing** — swap `ease-in` → `ease-out` or a strong custom curve; drop bounce on routine states.
4. **Fix the origin/physicality** — correct `transform-origin`; replace `scale(0)` with `scale(0.95)` + opacity.
5. **Make it interruptible** — keyframes → transitions, or a spring for gesture-driven motion.
6. **Move it to the GPU** — layout props → `transform`/`opacity`; Framer Motion shorthand → the full `transform` string.
7. **Asymmetric timing** — slow the deliberate phase, snap the response.
8. **Polish** — blur to mask crossfades, stagger groups, `@starting-style` for entry.
9. **Accessibility and cohesion** — add reduced-motion and hover gating; tune to the component's personality.

Delete beats reduce; reduce beats re-tuning. Most motion-overload findings close at steps 1–3.

**Before / After findings.** Record each motion fix as a row, not a paragraph — one line per issue, so the commit log reads as a diff of intent:

| Before | After | Why |
| --- | --- | --- |
| bounce (`cubic-bezier(0.34,1.56,0.64,1)`) on button hover | `cubic-bezier(0.4,0,0.2,1)` at 150ms | Bounce is for celebration, not routine state — it reads as decoration |
| `transition: all 400ms` | `transition: transform 180ms ease-out` | Name the property; `all` animates unintended props off the GPU, and >300ms drags on UI |
| six scroll-triggered reveals firing at once | one hero entrance, the rest static | Over three motion moments per screen reads as noise |
| `@keyframes` slide-in on a toast | `transition` + `@starting-style` | Toasts stack rapidly — transitions retarget mid-flight; keyframes restart from zero |
| no `prefers-reduced-motion` guard | gentler variant — opacity only, no movement | Reduced motion means fewer and gentler, not zero |

**Verdict — block or approve.** Close the branch with an explicit call:

- **Block** while any of these stand — bounce on a routine state transition, motion on a keyboard or 100+/day action, a UI transition over 300ms with no reason, `scale(0)` or `ease-in` on UI, or a layout-property animation with an easy GPU fix.
- **Approve** once bounce is gone from routine states, the screen sits under three motion moments, state transitions run under 300ms on `ease-out`, rapidly-triggered motion is interruptible, and `prefers-reduced-motion` is respected.

---

### Branch 5 — Token drift (hardcoded values)

**Symptoms.** `/design-reviewer` flagged hex codes / font names / radii hardcoded in component code instead of referencing DESIGN.md tokens (`{colors.primary}` etc.). Symptom report: "I tried to change the brand color but it only changed in three places."

**First action (Day-0, <30 min).** Find the SINGLE most-used hardcoded hex in the codebase (`grep -rE '#[0-9a-fA-F]{6}'`). If the hex matches a DESIGN.md token, replace every occurrence with a `var(--token-name)` or Tailwind utility. Screenshot before/after a component using the color. Commit: `fix(tokens): replace hardcoded {hex} with var({token-name})`.

**Day-0 (rest).** Continue grep-and-replace for the top 3 hardcoded hex codes. Do not yet handle font / radius drift — colors first.

**Day-1.** Audit font-family declarations and `border-radius` values. Replace hardcoded values with token references. Verify Tailwind config maps utilities to the right CSS variables (see [`design-production.md`](../../../../rules/design-production.md) "Web rendering path — Step 4").

**Day-14.** Add a stylelint rule banning hardcoded hex / font-family / border-radius values in component code (allow only `var(--*)` or Tailwind utilities). Document the new rule in `docs/design-rules.md`.

**Hand-off.** `/vibe-coding` if the codebase is small and Claude can sweep it. `/website-build` if the codebase needs structural refactor. `/brand-kit` if the underlying DESIGN.md tokens are missing the values being hardcoded (i.e., the codebase is hardcoding because the token doesn't exist yet).

---

## Multi-branch incidents (when more than one branch fires)

Common case: `/design-reviewer` flagged 8 findings across 3 branches. Sequencing rule:

1. **Branch 2 (a11y) first, always.** A11y is the only branch where the cost of NOT fixing is legal/regulatory, not just aesthetic. Day-0 a11y fixes precede everything else.
2. **Branch 5 (token drift) second.** Token drift makes every subsequent fix harder — you can't fix banned patterns or cardocalypse cleanly if the tokens are also wrong.
3. **Branch 1 (banned patterns) third.** Most visible to the user; closes the "is this AI slop" perception fastest.
4. **Branch 3 (cardocalypse) fourth.** Often correlated with banned patterns; fixing those first usually drops the card-stack depth as a side effect.
5. **Branch 4 (motion) last.** Motion overload is usually a polish-pass issue; fix it after structural problems are resolved.

If two branches share a Day-0 window, split: one engineer takes Branch 2, another takes Branch 5. Don't try to triage motion overload while contrast is still failing.

---

## Atomic-commit + before/after screenshot pattern

Every fix is one commit. Every commit message includes:

```
fix(design): {branch}: {component} — {one-line description}

Before: [link to screenshot or inline base64]
After: [link to screenshot or inline base64]
Branch: {1-5}
Severity: P{0-3}
Re-run: /design-reviewer expects {dimension} to move from {x} to {y}
```

Screenshots can be:
- Saved to `docs/design-review-screenshots/{commit-sha-prefix}-{component}.png`
- Or inline base64 in the commit message body (small images only)
- Or linked from a GitHub Issue / PR comment

The point is: a future reviewer can read the commit log and see the visual evolution without re-running the audit.

---

## Anti-Hallucination Guardrails

1. **Never skip the audit.** If no `/design-reviewer` output exists, run it first. Don't triage off vibes.
2. **First action must be visible.** A Day-0 fix that the user can't see in <30 min is the wrong fix. Pick the most-visible offender, not the cleanest.
3. **One commit per fix.** Bundling 5 fixes into one commit makes review impossible and re-measurement misleading.
4. **Don't re-measure after every commit.** Run `/design-reviewer` only after Day-0 completes — re-measuring after each commit is noise.
5. **If the brand's tokens are wrong, stop.** Hand off to `/brand-kit`. Triage cannot fix bad tokens by working around them.

---

## Integration with other skills

| Triggers this skill | This skill hands off to |
|---|---|
| `/design-reviewer` failing dimension | `/vibe-coding` for code changes |
| Client says "this looks like AI slop" | `/brand-kit` for token revisions |
| Pre-launch design audit fails | `/landing-page-wireframe` for layout rework |
| `/video-frames` motion-craft check fails | `/video-frames` for motion budget revision |

This skill is a **decision tree**, not an executor. It tells you what to fix and in what order; the actual code/design changes happen in the hand-off target.

---

## Quality checks (pre-output)

- [ ] Symptom mapped to exactly one branch (or sequenced if multi-branch)
- [ ] First action is specific (named component, named pattern, named fix)
- [ ] Day-0 / Day-1 / Day-14 actions all named with concrete checklist items
- [ ] Hand-off target is a real existing skill (not invented)
- [ ] Atomic-commit pattern documented with example
- [ ] Re-measurement plan named

---

## Attribution

This skill's structure is conceptually attributed to the **Designer-Who-Codes** pattern documented in [`nexu-io/open-design/skills/design-review`](https://github.com/nexu-io/open-design/tree/main/skills/design-review) (Apache-2.0, snapshot 2026-05-13) and its upstream source [`garrytan/gstack`](https://github.com/garrytan/gstack). Both upstreams are catalogue-stub references in the Open Design repo; the actual workflow content here is Genesys-authored against our existing [`audit-triage-pairing.md`](../../../rules/audit-triage-pairing.md) rule.

The atomic-commit + before/after-screenshot pattern is from the same source.

Branch 4's motion depth — the delete-first remedial preference hierarchy, the Before/After findings table, and the block/approve close — is adapted from Emil Kowalski's animation review method (animations.dev), MIT © 2026 Emil Kowalski. As with `/design-reviewer` (which carries the full 10-standard lens), that review method — non-negotiable standards, escalation triggers, and a remedial hierarchy — is itself adapted from aggressive code-quality review.

---

