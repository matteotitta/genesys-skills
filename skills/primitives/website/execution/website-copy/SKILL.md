---
name: website-copy
version: '1.0'
last_updated: 2026-04-09
author: genesys-growth
description: 'Orchestrates 3-phase copy iteration (vomit → tight → voicey) across N pages with parallel agents per page and
  shared context per phase. Each phase runs a parallel fan-out; gates between phases ensure quality compounds. Wraps landing-page-copy
  at scale. Triggers: "/website-copy", "run the full site copy", "copy cycle for all pages", "vomit tight voicey across [pages]",
  "full-site copy refresh". Upstream: product-messaging, tov-guidelines, landing-page-wireframe. Downstream: website-audit.
  NOT for single-page copy — use landing-page-copy directly. NOT for brand/wireframe phases — use /website-build for the full
  pipeline.'
goal: Orchestrates 3-phase copy iteration (vomit → tight → voicey) across N pages with parallel agents per page and shared
  context per phase.
outcome: 'Orchestrates 3-phase copy iteration (vomit → tight → voicey) across N pages with parallel agents per page and shared
  context per phase. Each phase runs a parallel fan-out; gates between phases ensure quality compounds. Wraps landing-page-copy
  at scale. Triggers: "/website-copy", "run the full...'
primitive: website
sub_primitive: execution
ontology_type: landing-page-copy
review_gate: 3
inputs:
  required:
  - product-messaging
  - tov-guidelines
  recommended:
  - landing-page-wireframe
  - icp-behavioural
  - brand-kit
- type: landing-page-copy
  feeds_into:
  - website-pm-score
  - website-pm-score
depends_on:
- product-messaging
- tov-guidelines
- website-pm-score
- website-pm-score
owned_by_agent: operator
mcps_used:
- gdrive
- notion
- trigger-dev
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
paths: projects/consulting/**/website/**,projects/apps/**
---

# website-copy — 3-phase × N-pages copy orchestrator

Runs the full vomit → tight → voicey copy cycle across all pages of a site in parallel. Each phase inherits the previous, so quality compounds without rework. Designed for the "website refresh" pattern. For single-page work, use the merged `landing-page-copy` workflow in the premium reference.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`marketing-psychology.md`](../../../../rules/marketing-psychology.md) — 8 anchored heuristics (loss aversion default, JTBD framing, choice limits)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in website-copy |
|---|---|---|
| **R1** | Source placement (three layers) | Live pages are **end-customer-facing**. **No sources block on rendered pages.** Working copy markdown carries `[VERIFIED:...]` tags for QA only; stripped before publish. |
| **R2** | Single-doc-with-toggles | Multi-page deliverable ships as **one Notion doc with one toggle per page** — not 7 separate files. Index up top; each page's copy expands inline. Tessa's Step 6 anchor. |
| **R3** | Product-update tone | Product / pricing / feature pages frame as "we shipped X" not "we are thrilled to announce." Even hero copy on launch pages. |
| **R5** | Blog as voice anchor | When the site has a published blog, the blog's opening line is the canonical voice anchor for hero copy across home/product pages. Verbatim. Channel-misaligned voice is the biggest tell of multi-author copy. |
| **R6** | CTA hierarchy | Market-facing pages (home, product, pricing, comparison) → sign-up or trial primary, blog as fallback. Warm-base surfaces (in-app, post-login) → product-action CTA. One primary per page. |
| **R8** | Entity-name headings | FAQ sections and product-explainer headings repeat the product name — "What [Product] does," "Who [Product] is for," "How [Product] is different." Not pronoun headings. |
| **R9** | Action-oriented section names | "How to start with [Product]" beats "Getting Started." "Why [Product]" beats "Overview." Action over status throughout. |

---

## When to run

**Invoke when user says:**
- "/website-copy --pages 'home, pricing, about'"
- "Run the full site copy for [client]"
- "Copy cycle for all pages"
- "Vomit → tight → voicey across [page list]"
- "Full-site copy refresh"

**Do NOT invoke when:**
- User wants AEO/SEO content → use `aeo-content`
- User wants email copy → use `outreach-emails` or `lifecycle-marketing`
- User wants social content → use `linkedin-content`
- User wants overall messaging strategy without page copy → use `product-messaging`
- Missing locked messaging or TOV → run `/product-messaging` + `/tov-guidelines` first
- User is in brand/wireframe phase → use `/website-build` for the full pipeline

**Decision tree:**

| Surface | Mode | Path |
|---------|------|------|
| Single landing page | `mode=landing_page` — single-page workflow | the premium reference |
| 3+ pages of a site | Multi-page orchestrator | This SKILL.md |
| Pipeline at scale | Trigger.dev pipeline (v3.0) | the premium reference (Pipeline Mode section) |

---

## Inputs

**Required:**
- `--client` — client slug
- `--pages` — comma-separated page list (use slashes for nested: `solutions/advisers`)
- Locked product-messaging output at `projects/consulting/{slug}/strategy/*product-messaging*.md`
- TOV guidelines at `projects/consulting/{slug}/brand/*tov*.md`
- ICP behavioural personas (pain points, outcomes, customer language)

**Recommended:**
- Wireframes at `projects/consulting/{slug}/website/*wireframe*` for each page
- Client CLAUDE.md voice section
- DESIGN.md at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md` (colors, typography, components, Do's/Don'ts)
- Brand voice guidelines (calibrates Phase 3)
- Competitor research (strengthens differentiation)
- Win-loss analysis (real objections for FAQs)
- VOC synthesis (authentic customer vocabulary)
- SEO keywords (headline optimization)
- Existing page URL (reference for structure/tone)

**Optional flags:**
- `--stack <framer|shadcn-vercel|webflow>` — target deployment (informs output format)
- `--phases "vomit,tight,voicey"` — customize phase sequence (default runs all 3)
- `--start-phase <vomit|tight|voicey>` — skip earlier phases
- `--max-parallel <N>` — concurrent page agents per phase (default: 5)

**Input validation checklist:**
- [ ] Messaging framework has ≥3 capabilities and ≥3 differentiators
- [ ] ICP research includes ≥1 persona with pain points and outcomes
- [ ] Page type confirmed with user
- [ ] If no DESIGN.md exists → pause and recommend `/brand-kit` first

If inputs missing → list gaps and recommend skills to fill them. The Iron Law: NO COPY WITHOUT UPSTREAM INPUTS. Full red-flag protocol in the premium reference (Iron Law + Red Flags sections).

---

## Steps

### 1. Preconditions check
Verify locked product-messaging, TOV, wireframes, client CLAUDE.md voice section. List gaps and run upstream skills if missing.

### 2. Confirm page list and structure
Per page, load relevant workflow:

### 3. Load DESIGN.md tokens (per.claude/rules/design-production.md)
Read: `colors.*` (semantic role per palette), `typography.*` (hierarchy tier per text block), `components.*` (canonical CTA style), Do's and Don'ts (emphasis guardrails). Required citations: DESIGN.md path at top of doc; per-page typography tokens (`typography.headline-lg`, `typography.body-md`, `typography.label-sm`); component tokens for CTAs (`components.button-primary`); WCAG AA contrast logic on dark surfaces. Forbidden: color-name copy ("the orange button") when token names exist; copy demanding shadcn primitives be restyled out of brand.

### 4. Map messaging framework to sections (per page)
Hero → positioning statement + primary differentiator. Problem → ICP pain points (top 3). Capabilities → value props (top 3). Differentiation → key differentiators (top 3). Proof → customer outcomes and logos. FAQs → sales objections. Output: section-to-messaging mapping.

### 5. Phase 1 — Vomit (parallel fan-out)
Per-page agent context: product messaging (shared), wireframe for this page (entity-specific), ICP behavioural insights (shared), page purpose + user intent.

Agent prompt: "Dump everything. For the {page} page following the {wireframe}, write a vomit draft of every section — headline, subhead, body, bullets, proof, CTA. Include 3-5 headline options per section. Don't filter. Don't polish. Aim for 2x the final length. Use the product messaging as source of truth. Apply headline formulas from the premium reference Mark unknowns as [NOT AVAILABLE] per voice rules."

Output: `projects/consulting/{slug}/website/0{MMYY}-copy/01-vomit/{page}.md`. Phase 1 checkpoint: all sections have headline + sub-headline minimum; each headline traces to a specific messaging framework component; no invented claims. Gate 1: auto-complete (vomit is intentionally rough).

### 6. Phase 2 — Tight (parallel fan-out)
Per-page agent context: Phase 1 vomit (entity-specific, read from previous phase), product messaging (shared), TOV "cut ruthlessly" section, character limits (Genesys defaults: headlines <100, sub-headlines <150).

Agent prompt: "Take the vomit draft at {path}. Cut it in half. Kill qualifiers ('really', 'very', 'actually'). Convert passive to active. Enforce headline/sub-headline character limits. Pick the single best headline option per section — delete alternatives. Preserve all value claims but tighten phrasing. Apply tight checklist from the premium reference Run anti-AI messaging check (see the premium reference Phase 2.3). Return tight version."

Word economy targets: hero headline 8-12 words; hero sub-headline 15-25 words; problem block 20-40 each; capability block 25-50 each; CTA headline 6-10 words.

Output: `projects/consulting/{slug}/website/0{MMYY}-copy/02-tight/{page}.md`. Phase 2 checkpoint: filler removed; passive→active; word counts within targets; no repetition between sections; anti-AI scan 0 failures. Gate 2: quick scan (headlines within limits? noticeably shorter? value props intact?).

### 7. Phase 3 — Voicey (parallel fan-out)
Per-page agent context: Phase 2 tight output (entity-specific), TOV guidelines (full doc), client CLAUDE.md voice section, Genesys voice rules (no em dashes without spaces, sentence case, contractions freely), client-specific vocabulary.

Agent prompt: "Take the tight draft at {path}. Layer voice. Apply TOV patterns from {tov-path}. Use client's sentence cadence. Add contractions where natural. Apply 'so what' test to every bullet — if reader could reply 'so what?', rewrite or cut. Apply voice techniques from the premium reference (≥3 per section). Generate 2-3 alternative hero headlines for A/B testing. Run Auto-Challenge Protocol from CLAUDE.md. Flag anything that fails Voice/Value/Quality checks."

Voice calibration scale: Conservative (1-3) professional/restrained; Balanced (4-6) confident/clear/some personality; Provocative (7-10) bold/irreverent/memorable.

Output: `projects/consulting/{slug}/website/0{MMYY}-copy/03-voicey/{page}.md`. Phase 3 checkpoint: ≥3 voice techniques per section; brand voice calibration matches guidelines; alternative headlines provided. Gate 3: deep review (user reviews each page for voice + value + quality). Pages that fail loop back to Phase 3 with specific feedback.

### 8. Phase 4 — Aggregate
Produce: (1) Master copy doc at `projects/consulting/{slug}/website/0{MMYY}-copy/FINAL.md` (all pages concatenated). (2) Per-page deliverables formatted for `--stack`: `shadcn-vercel` → JSX snippets; `framer` → plain text matching component names; `webflow` → spreadsheet (page + section + copy). (3) Change log: vomit → tight → voicey per page.

### 9. Self-evaluation + skill auto-update
Run completeness check, evidence quality check, guardrail check, self-roast questions. Detailed protocols in the premium reference (Self-Evaluation Protocol + Skill Auto-Update Protocol). Capture user-approved outputs as reference examples in the premium reference.

**Edge cases:**
- Page with no wireframe → fail fast; run `/landing-page-wireframe` first
- TOV conflict with client CLAUDE.md voice → client CLAUDE.md wins; log conflict for TOV refresh
- Phase 3 fails Auto-Challenge for a page → mark `needs-rework`, allow others to proceed, surface in Phase 4 aggregate
- Character limit violations in Phase 2 → agent iterates within phase; max 3 retries per headline
- Client vocabulary missing → fall back to Genesys voice defaults; log as TOV gap

**Pipeline mode (v3.0)** for 3+ pages via Trigger.dev: full spec including context slicing, batch grouping, and Trigger.dev task IDs in the premium reference (Pipeline Mode section).

---

## What good looks like

### Evaluations

**Quality discipline before delivery:** run the full pre-delivery quality checklist (content + format + Iron Law guardrails + Anti-AI detector + 5 self-roast questions) → see the premium reference.

If self-roast surfaces real weakness on any page, loop that page back to Phase 3 with specific feedback before shipping.

---

# ClientCo full site copy
/website-copy --client ClientCo --pages "home, pricing, about, treasury, payroll, bookkeeping, team-cards, invoice-pay, reporting, integrations" --stack shadcn-vercel

# ClientCo via Framer
/website-copy --client ClientCo --pages "home, solutions/advisers, solutions/operations, solutions/paraplanners, blog, pricing, case-studies, about" --stack framer

# Resume at voicey (tight already approved)
/website-copy --client ClientCo --pages "home, pricing, about" --start-phase voicey

# Refresh single section after Gate 3 feedback
/website-copy --client ClientCo --pages "home" --start-phase tight --max-parallel 1
```

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/voice-reviewer` — the content ship gate: voice + brand quality (pm-loop.md).

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
