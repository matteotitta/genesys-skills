---
name: website-build
version: '1.0'
last_updated: 2026-04-09
author: genesys-growth
description: 'Orchestrates full-site build pipeline from brand to deployed pages. Chains brand-kit → landing-page-wireframe
  → component scaffold (ShadCN/Figma/Framer) → landing-page-copy (3-phase) → deploy in sequence with review gates between
  phases. Triggers: "/website-build", "build the full website", "run the landing page pipeline", "scaffold all pages for [client]".
  Upstream: positioning, product-messaging. Downstream: landing-page-copy, website-audit. NOT for single-page builds — invoke
  landing-page-copy directly. NOT for copy-only work — use /website-copy instead.'
goal: Orchestrates full-site build pipeline from brand to deployed pages.
outcome: 'Orchestrates full-site build pipeline from brand to deployed pages. Chains brand-kit → landing-page-wireframe →
  component scaffold (ShadCN/Figma/Framer) → landing-page-copy (3-phase) → deploy in sequence with review gates between phases.
  Triggers: "/website-build", "build the full website",...'
primitive: website
sub_primitive: execution
ontology_type: landing-page-copy
review_gate: 3
inputs:
  required:
  - positioning
  - product-messaging
  recommended:
  - tov-guidelines
  - brand-kit
  - competitor-research
- type: deployed-website
  feeds_into:
  - website-pm-score
  - website-pm-score
depends_on:
- positioning
- product-messaging
- website-pm-score
- website-pm-score
owned_by_agent: operator
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
paths: projects/consulting/**,projects/apps/**
---

# /website-build — Full Site Build Pipeline

Orchestrates the complete landing-page pipeline from brand extraction through deployment. Chains 5 phases with review gates, supports Framer/ShadCN/Vercel stacks, uses parallel agents within phases.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`design-production.md`](../../../../../rules/design-production.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (live pages end-customer-facing — no sources blocks), R2 (multi-page deliverable ships as one project with per-page toggles in working doc), R3 (page copy capability-led across all pages), R5 (anchor blog opener cascades to hero copy across pages), R6 (page-level CTA hierarchy: home/product → sign-up, in-app → product-action), R8 (entity-name headings on FAQ sections), R9 (verb-led page section names).

---

## Claude Code Triggers

**Invoke when user says:**
- "/website-build"
- "Build the full ClientCo website"
- "Run the landing page pipeline for [client]"
- "Scaffold all pages from the messaging"
- "Take this from brand kit to deployed site"

**Do NOT invoke when:**
- User wants just one page (use `/landing-page-copy` directly)
- User wants to refresh copy only on existing pages (use `/website-copy`)
- Client lacks locked positioning + messaging (run `/positioning` → `/product-messaging` first)

---

## Input Format

```
/website-build \
  --client <slug> \
  --pages "home, pricing, about, [product-pages], [solution-pages]" \
  --stack <framer|shadcn-vercel|webflow> \
  [--skip <phase1,phase2>] \
  [--start-at <phase>]
```

**Required:**
- `--client` — client slug matching `projects/consulting/{slug}/`
- `--pages` — comma-separated page list
- `--stack` — target build stack

**Optional:**
- `--skip` — skip phases that were already completed
- `--start-at` — resume from a specific phase (e.g., after fixing wireframe feedback)

---

## Design integration — DESIGN.md + shadcn (orchestrator level)

**Upstream contract:** This orchestrator chains brand-kit (DESIGN.md producer) → wireframe → copy → deploy. The DESIGN.md file at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md` is the single source of truth for all visual values across every phase.

**Pipeline-level token enforcement:**
- **Phase 1 (Brand Foundation)** must produce a valid DESIGN.md with all 8 lint rules passing (broken-ref, primary-defined, section-order, contrast-ratio, typography-defined, orphaned-tokens, one-primary-per-screen, two-font-weights-max). If lint fails, the pipeline halts at Gate 2.
- **Phase 2-4 (Wireframe → Copy → Component scaffold)** all read the same DESIGN.md tokens. Cross-phase consistency is mechanical, not aspirational — every page references identical token names.
- **Phase 5 (Deploy)** generates `app/globals.css` (CSS variables from tokens) + `tailwind.config.ts` (utilities mapped to vars) + shadcn primitive installs. The deployed site reads tokens at runtime via CSS variables; shadcn components consume them automatically.

**Forbidden across the pipeline:**
- Skipping Phase 1 — no pipeline run without a valid DESIGN.md
- Per-page brand drift — every page reads the same DESIGN.md
- Hardcoded brand values in any phase output

**Authority:** Full integration contract in `.claude/rules/design-production.md` (auto-loaded). When in doubt, that file wins.

**If no DESIGN.md exists at pipeline start:** Phase 1 must produce one before Phase 2 can begin. Halt and run `/brand-kit` if missing.

---

## Pipeline Phases

```
Phase 1: Brand Foundation → brand-kit (DESIGN.md) + tov-guidelines
         ↓ [Review Gate 2 + DESIGN.md lint rules pass]
Phase 2: Information Architecture → landing-page-wireframe (parallel per page)
         ↓ [Review Gate 3 — designer handoff]
Phase 3: Component Scaffold → stack-specific (ShadCN/Framer/Webflow)
         ↓ [Review Gate 2]
Phase 4: Copy Execution → /website-copy (3-phase × N-pages)
         ↓ [Review Gate 3]
Phase 5: Deploy → stack-specific deploy + website-audit
```

---

## Execution Workflow

### Phase 1: Brand foundation

**Preconditions:**
- Client folder exists at `projects/consulting/{slug}/`
- Client CLAUDE.md has voice section

**Actions:**
1. Check if `brand/` folder has current brand-kit output (< 90 days old)
2. If missing/stale: run `/brand-kit` with client website URL
3. Check TOV: if missing, run `/tov-guidelines` against win-loss transcripts + website
4. Output: `brand/0{MMYY}-brand-kit.md`, `brand/0{MMYY}-tov-guidelines.md`

**Review gate 2:** Quick scan — do brand colors, voice patterns, frequency scores look right for the client?

### Phase 2: Information architecture

**Preconditions:**
- Brand + TOV locked
- Product messaging locked (check `messaging/0{MMYY}-product-messaging.md`)

**Actions:**
1. Dispatch parallel agents via `/batch-run landing-page-wireframe --entities "{pages}"`
2. Each agent produces: block list, rationale, sequencing, data/MCP requirements
3. Aggregate into `website/0{MMYY}-wireframes/` folder with one file per page
4. Produce master sitemap: `website/0{MMYY}-sitemap.md`

**Review gate 3:** Designer handoff — wireframes get reviewed by designer/team before proceeding. This gate can take days; pipeline pauses here.

### Phase 3: Component scaffold

Branches by `--stack`:

**ShadCN + Vercel:**
1. Init Next.js project in `projects/apps/{slug}-website/` if missing
2. Install shadcn components via CLI
3. Scaffold page files per wireframe block-list
4. Apply brand-kit colors to tailwind.config + globals.css
5. Deploy preview to Vercel

**Framer:**
1. Use Framer MCP to read existing file structure
2. Map wireframe blocks to Framer components
3. Use Code Connect for component mappings
4. Apply brand tokens via Framer Variables

**Webflow:**
1. Manual handoff — produce a wireframe-to-webflow mapping doc
2. Skill ends here; team takes over in Webflow

**Output:** Scaffolded project with placeholder content + brand applied.

**Review gate 2:** Visual scan — does structure match wireframes? Branding applied correctly?

### Phase 4: Copy execution

Delegates to `/website-copy`:

```
/website-copy \
  --client {slug} \
  --pages "{pages}" \
  --stack {stack} \
  --phases "vomit,tight,voicey"
```

This runs the full 3-phase × N-pages orchestration. See `/website-copy` SKILL.md.

**Review gate 3:** Copy review by user — voice check, value check, quality check per Auto-Challenge Protocol in CLAUDE.md.

### Phase 5: Deploy

Branches by stack:

**Vercel:** `cd projects/apps/{slug}-website && vercel --prod --yes`
**Framer:** Publish via Framer UI (manual trigger, skill surfaces URL)
**Webflow:** Manual publish

**Post-deploy:**
1. Run `/website-audit` against live URL
2. Run `/website-score` for PM evaluation
3. Log to client wiki via `/wiki log --client {slug} "Website shipped — v{N}"`

---

## Example invocation

**ClientCo full site (the pattern this week):**
```
/website-build \
  --client ClientCo \
  --pages "home, pricing, about, treasury, payroll, bookkeeping, team-cards, invoice-pay, reporting, integrations" \
  --stack shadcn-vercel
```

**ClientCo via Framer:**
```
/website-build \
  --client ClientCo \
  --pages "home, solutions/advisers, solutions/operations, solutions/paraplanners, blog, pricing, case-studies, about" \
  --stack framer
```

**Resume at copy phase (if wireframes + scaffold already done):**
```
/website-build \
  --client ClientCo \
  --pages "..." \
  --stack shadcn-vercel \
  --start-at copy
```

---

## Edge cases

- **Designer handoff delay in Phase 2:** Pipeline can pause for days. Use `--start-at scaffold` to resume.
- **Stack mismatch:** If user starts with ShadCN then wants Framer, the pipeline must restart Phase 3 — scaffolds don't translate across stacks.
- **Page-level wireframe changes post-Phase 3:** Re-run just that page through `/batch-run landing-page-wireframe --entities "{page}"` then patch the scaffold manually.
- **Copy rejected at Gate 3:** Loop back to Phase 4 with updated TOV or messaging; no need to rebuild scaffold.

---

## Design cycle (post-authoring phases)

After producing the build, walk these phases before ship. Each references the shared design-quality library at `../../../meta/catalog/design-reviewer/the premium reference. Marketing pages skip Cognitive load (single CTA, not a decision tree) and Onboarding (CTAs, not first-run flows).

- **Layout** — `layout-tenets.md` (generous whitespace; 64–128px section gaps)
- **Distill** — `distill-principles.md` (one primary CTA per section; remove generic stock)
- **Typeset** — `typeset-principles.md` (measure 45–75ch for body prose)
- **Polish** — `polish-principles.md` (interaction states; concentric radius)
- **Harden** — `harden-checklist.md` (i18n if multi-language; responsive at all breakpoints)
- **Delight** — `delight-patterns.md` (custom 404 pages; restrained micro-interactions on primary CTA)
- **Final review** — run `/design-reviewer`

## Notes

- This pipeline maps to the "landing page" stage of a client engagement (positioning → wireframe → copy → deploy)
- Each phase produces artifacts dated with MMYY convention
- Client folder CLAUDE.md should be updated at the end to reference the shipped site
- For multi-round iteration (ClientCo pattern): run once for P1 pages (home/pricing/about), then again with `--pages` for P2/P3 product pages

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
