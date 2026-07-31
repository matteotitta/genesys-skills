---
name: website-clone
version: '1.1'
last_updated: 2026-05-01
author: genesys-growth
description: 'Reverse-engineers a live website URL into a deployable Next.js + shadcn + Tailwind clone. Five-phase workflow — Reconnaissance, Foundation, Component Spec & Dispatch, Page Assembly, Visual QA — with mandatory getComputedStyle() extraction, all-states capture, interaction-model classification, and spec-file-as-handoff-contract discipline. Dispatches parallel builder agents in git worktrees during a single session. Triggers: /website-clone, "clone this site", "rebuild this page", "reverse-engineer this URL", "pixel-perfect copy of [URL]". Requires a browser-automation MCP (Chrome DevTools MCP recommended). NOT for: phishing, impersonation, ToS-violating clones, or new-from-scratch landing pages (use /website-build).'
goal: Reverse-engineer a live URL into a pixel-perfect, deployable Next.js + shadcn + Tailwind clone.
outcome: 'A deployable Next.js codebase that visually matches the target URL at desktop, tablet, and mobile viewports — with extracted design tokens, downloaded assets, real text content, and accurate interaction behaviors. Output: working site ready for /vercel deploy + /website-pm-score evaluation.'
primitive: website
sub_primitive: execution
ontology_type: landing-page-copy
review_gate: 3
inputs:
  required:
  - source_url
  recommended:
  - brand-kit
  - target_vercel_project
- type: deployed-website
  feeds_into:
  - website-pm-score
depends_on: []
- website-pm-score
owned_by_agent: operator
mcps_used:
- chrome-devtools
- firecrawl
- a1
- gdrive
- notion
triggers:
  slash_commands:
  - /website-clone
  natural_language:
  - clone this site
  - reverse-engineer this URL
  - pixel-perfect copy of
  - rebuild this page
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 1
effort: high
paths: projects/consulting/**,projects/apps/**
---

# /website-clone — URL → deployable Next.js clone

Reverse-engineer a live website into a working Next.js + shadcn + Tailwind codebase. Five phases. Mandatory `getComputedStyle()` extraction. Spec-file handoff contract before any builder runs. Parallel builder agents in worktrees during a single session.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Internal-reference engineering skill — produces working code, not narrative. Applies [[feedback_execution_doctrine_refinements_step6]] R1 (spec-file cites stay inline for engineering QA), R3 (commit messages + spec language operator-direct), R9 (verb-led phase names). R2/R5/R6/R7/R8 not applicable.

This skill is **extraction-driven, not brief-driven**. It runs **backward from a URL**. For forward-from-positioning work, use `/website-build` instead.

Adapted from `JCodesMore/ai-website-cloner-template` per `/steal` analysis (2026-04-30). The source skeleton template lives at `projects/apps/_templates/website-clone-skeleton/`.

For full 5-phase process (Recon / Foundation / Spec & Dispatch / Assembly / Visual QA) → the premium reference.

---

## Triggers

**Invoke when user says:**
- `/website-clone <url>`
- "clone this site"
- "rebuild this page"
- "reverse-engineer this URL"
- "pixel-perfect copy of [URL]"
- "make a clone of [competitor's homepage]"

**Do NOT invoke when:**
- User wants a fresh site from positioning + messaging (use `/website-build`)
- User wants only a wireframe (use `/landing-page-wireframe`)
- User wants only copy on an existing page (use `/website-copy`)
- User wants to audit a site (use `/website-audit` or `/website-score`)
- The clone target violates ToS, enables phishing, or impersonates a brand the user doesn't own — refuse with a one-line reason

---

## Ethics guardrails (read FIRST)

This skill clones live websites. **Legitimate uses:**
- **Migration** — cloning the user's own old site (WordPress, Webflow, Framer) into a maintainable Next.js codebase
- **Recovery** — recovering source for a site whose original code was lost
- **Educational deconstruction** — studying a competitor's pattern with no intent to publish
- **Internal demo / prototype** — building a private internal demo, not a public clone

**Refuse the request if:**
- Clone target is intended for **phishing** or **brand impersonation**
- User does not own the target and intends to publish the clone publicly under similar branding
- Target's ToS explicitly prohibits derivative works AND user intends to publish

When in doubt, ask the user about intended use before proceeding. Treat as a Gate-2 check — log the answer in the spec doc and proceed only after confirmation.

---

## Inputs

**Required:**
- `source_url` — the live URL to clone (must be publicly accessible)

**Recommended (improves quality):**
- `brand-kit` — if cloning into the user's brand, the DESIGN.md tokens override extracted tokens during Phase 2
- `target_vercel_project` — the Vercel project to deploy into
- `fidelity_level` — pixel-perfect (default), structural, or layout-only

---

## A1 Gallery reference (input disambiguation — fires BEFORE Phase 1)

**When to call:** ONLY when the user's input is a fuzzy description rather than a concrete URL (e.g., "clone me something like Linear's pricing page", "rebuild a clean SaaS landing", "pixel-perfect copy of a dark fintech site"). When the user already pasted a concrete URL, **skip this entirely** and go straight to Prerequisites — don't burn calls when the source is already locked.

**Why:** the skill requires a `source_url` to operate. Fuzzy inputs without an explicit URL would otherwise stall the workflow with "which page?" questions. a1.gallery's curated catalog resolves the fuzzy description into 3 candidate URLs the user can pick from.

**Primary tool:** `mcp__a1__search_websites(query='{user description}', limit=3)` per `.claude/rules/a1-gallery-protocol.md`.

**Flow:**
1. Detect fuzzy input: if `source_url` is missing OR contains style language ("like", "similar to", "clean SaaS", "dark fintech") without a parseable URL.
2. Call `search_websites` with the user's description verbatim.
3. Surface the top 3 results with thumbnails and ask: "These match your description — pick one to clone (paste the URL), or refine the description."
4. Once the user confirms a URL, set `source_url` and proceed to Prerequisites + Phase 1 unchanged.
5. If `search_websites` returns 0 results, fall back to asking the user for a URL directly — don't guess.

**Skip when:**
- User pasted a concrete URL (`https://...` or `domain.tld/path`) — go straight to Prerequisites
- User invoked with `/website-clone <url>` slash form — URL is already the argument
- User is migrating their own site (they know the URL)

**Cite:** any reference surfaced from a1 in the eventual spec doc as `[REFERENCE: a1.gallery, {slug}, accessed YYYY-MM-DD]`. Note: the cloned output uses the chosen URL as the source — the other a1 candidates were discovery, not source-of-truth.

---

## Prerequisites

1. **Browser-automation MCP installed** — Chrome DevTools MCP (recommended), Playwright MCP, or Browserbase MCP. Without one, this skill cannot work. Run `claude mcp list | grep -E "chrome-devtools|playwright|browserbase"` to confirm.
2. **Next.js + shadcn + Tailwind v4 base scaffold** — run `npx shadcn@latest init` to bootstrap a fresh project, then apply the skeleton from `projects/apps/_templates/website-clone-skeleton/`.
3. **Disk space** — clone targets typically pull 50–500MB of images, videos, and fonts.

---

## Workflow at a glance

| Phase | Purpose | Sequential / parallel |
|-------|---------|----------------------|
| **1. Recon** | Screenshots, global extraction, animation primitives, logo classification, interaction sweep, post-click state capture, page topology | Sequential |
| **2. Foundation** | Fonts, globals.css, types, icons, asset download script, build verification | Sequential — do yourself, don't delegate |
| **3. Spec & dispatch** | Per section: extract → write spec file → dispatch builder in worktree | Parallel builders, sequential extraction |
| **4. Assembly** | Wire all sections in `src/app/page.tsx`, page-level behaviors, build verify | Sequential |
| **5. Visual QA** | Side-by-side diff at desktop + mobile; fix specs or components | Sequential, mandatory |

For full per-phase steps including mandatory extraction protocols (animation primitives, logo render-mode classification, post-click state capture) → the premium reference.

---

## Pre-dispatch checklist (run before EVERY builder dispatch)

If you can't check every box, go back and extract more. **Don't dispatch on incomplete specs.**

- [ ] Spec file written to `docs/research/components/<name>.spec.md` with ALL sections filled
- [ ] Every CSS value in the spec is from `getComputedStyle()`, not estimated
- [ ] Interaction model identified and documented (static / click / scroll / time)
- [ ] For stateful components: every state's content + styles captured
- [ ] For scroll-driven components: trigger threshold, before/after styles, transition recorded
- [ ] For hover states: before/after values + transition timing recorded
- [ ] All images identified (including overlays + layered compositions)
- [ ] Responsive behavior documented for at least desktop + mobile
- [ ] Text content verbatim (not paraphrased)
- [ ] Builder prompt under ~150 lines of spec — if over, split the section

---

## Anti-Hallucination Guardrails

1. **No estimated CSS values.** Every value comes from `getComputedStyle()` — no hand-measurements, no eyeballed approximations.
2. **No paraphrased copy.** Text content is captured verbatim from the DOM, including alt attributes, aria labels, placeholders.
3. **No static substitutes for dynamic primitives.** Canvas, WebGL, Lottie, RAF loops must be rebuilt as the same primitive — never approximated as static elements (Phase 1b.5 mandatory).
4. **No assumed logo colors.** SVG file alone doesn't determine rendered color — capture parent's computed `color` (Phase 1b.6).
5. **No spec-less dispatches.** Spec file is the contract. No spec → no dispatch.
6. **No skipped revealed states.** Every clickable that opens new DOM gets full extraction of the revealed subtree (Phase 1c.5).

---

## Composition with other skills

| Stage | Skill | Why |
|-------|-------|-----|
| Before clone | `/brand-kit` | If cloning into client brand, DESIGN.md tokens override extracted tokens in Phase 2 |
| After clone | `/website-score` | PM evaluation of the cloned site |
| Copy refresh | `/website-copy` | Replace extracted copy with positioning-driven copy |
| Different intent | `/website-build` | Forward-from-messaging build (NOT a clone) |

---

## Completion report

When done, output:
- Total sections built
- Total components created
- Total spec files written (should match components)
- Total assets downloaded (images, videos, SVGs, fonts)
- Build status (`npm run build` result)
- Visual QA results — discrepancies remaining, if any
- Vercel deploy URL (if deployed)
- Known gaps or limitations (e.g., "auth flow not cloned — out of scope")

---

## External References

- `projects/apps/_templates/website-clone-skeleton/` — bootstrap directories + reference inspection guide
- `.claude/discovery/0426-website-cloner-source/` — verbatim source files from JCodesMore/ai-website-cloner-template
- `.claude/rules/design-production.md` — DESIGN.md token format + shadcn integration contract

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

