---
name: vibe-coding
version: '2.1'
last_updated: 2026-07-09
author: genesys-growth
description: 'Plans app or lead magnet builds using Lovable or Claude Code for non-technical users. Produces a project spec,
  design brief, tech stack recommendation, and step-by-step guided build plan. Depends on brand-kit for design tokens and
  visual consistency. Triggers: "vibe coding", "build an app", "lead magnet tool", "build me a calculator", "create an interactive
  tool", "plan a Lovable project". NOT for full-stack engineering — this is guided planning and iterative prompting, not direct
  code writing.'
goal: Plans app or lead magnet builds using Lovable or Claude Code for non-technical users.
outcome: 'Plans app or lead magnet builds using Lovable or Claude Code for non-technical users. Produces a project spec, design
  brief, tech stack recommendation, and step-by-step guided build plan. Depends on brand-kit for design tokens and visual
  consistency. Triggers: "vibe coding", "build an app",...'
primitive: design
ontology_type: landing-page-copy
review_gate: 2
inputs:
  required:
  - brand-kit
  - product-messaging
  recommended: []
outputs:
- type: landing-page-copy
  feeds_into: []
depends_on:
- brand-kit
- product-messaging
feeds_into: []
owned_by_agent: content
mcps_used:
- a1
push_targets:
- gdrive
- notion
triggers:
  slash_commands:
  - /vibe-coding
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Vibe coding

Plan an app, lead magnet, or interactive tool build using Lovable or Claude Code. Produce a project spec, tech-stack recommendation, seed prompt, iteration plan, and deployment path. Knowledge type: `landing-page-copy` (per `.claude/rules/ontology.md`); maturity: emergent → validated after first deployment.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`design-production.md`](../../../../rules/design-production.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (project spec is client-team review surface — cites in appendix; rendered app is end-customer-facing — no source frames), R3 (app copy capability-led across hero + body), R6 (app close → sign-up primary for lead magnets, product-action for interactive tools), R9 (verb-led spec section names).

## When to run

Invoke when the user says: "vibe code [something]", "build an app for [purpose]", "create a tool that [does X]", "make a website for [purpose]", "deploy to Vercel", "Claude Code project", "Lovable project", "build a quiz / calculator / lead magnet", "I have an idea but don't know where to start". Do **NOT** invoke for: landing-page copy only (use `/landing-page-copy`), design guidelines (use `/brand-kit`), debugging existing code (handle directly), or in-tool prompt creation (use `/workflow-prompt-design`).

This skill is **guided planning + iterative prompting**, not direct code writing. The user (or another agent) executes the build inside Lovable or Claude Code; this skill produces the brief, the seed prompt, and the iteration coaching.

**The Iron Law:** one variable per iteration. Multi-variable edits degrade quality. If circling, re-anchor with stronger references — don't keep iterating against weak anchors.

## Inputs

**Required:**

- `project idea` — what the user wants to build (e.g., "GTM readiness quiz", "ROI calculator").
- `tool preference` — Lovable or Claude Code (or "help me choose").

**Recommended (improve quality):**

- `target user` — who uses it, what they care about, what action they take.
- `reference examples` — 10/10 anchors (e.g., "Typeform's aesthetic") + 1/10 anti-anchors.
- `technical requirements` — backend, integrations, AI features, data storage.
- `brand hub / DESIGN.md` — design tokens (colors, type, components, spacing) for on-brand builds.
- `MVP scope` — must-have v1 vs. nice-to-have v2+.

If inputs are missing, run interactive planning mode (see `references/project-planning.md`) — don't guess, ask.

## A1 Gallery reference (anchor-gathering)

**Default:** a1.gallery MCP, per `.claude/rules/a1-gallery-protocol.md` (auto-loaded for design-output skills).

**When to call:** during Step 2 (Four Definitions), specifically when populating the **Anchors** field. The whole skill's quality hinges on strong reference anchors — vague descriptions ("clean SaaS", "playful landing page") produce vague output. a1 resolves vague style language into concrete URLs + thumbnails before the seed prompt is generated.

**Primary tool:** `mcp__a1__search_websites(query='{user style language}', limit=6)` — natural-language search; common aliases resolve automatically ("SaaS" → software, "fintech" → finance).

**Refinement:** if the user's input already maps to clear filters (e.g., "dark Next.js portfolio"), prefer `mcp__a1__browse_websites(typeSlug='portfolio', styleSlugs=['dark'], technologySlugs=['next-js'], limit=6, mode='discovery', includeImages=true)` for tighter precision. Validate slugs against `mcp__a1__get_design_filters` if uncertain.

**How to use the result:**
1. Surface the 6 returned thumbnails to the user. Ask: "These match your description — which 2–3 are closest to what you want? Any anti-anchors (looks you want to AVOID)?"
2. Lock the user's selections as the project's Anchors (Step 2 of the Four Definitions).
3. Pass the locked anchor URLs into the seed prompt (Step 6) — Lovable / Claude Code can reference them as concrete visual targets, not vague descriptors.
4. Cite each surfaced reference as `[REFERENCE: a1.gallery, {slug}, accessed YYYY-MM-DD]` in the project plan.

**Why this matters:** the Iron Law ("one variable per iteration") only works if the anchor is strong enough to articulate gaps against. Weak anchors produce vague articulation, which produces vague edits, which kill output quality. a1 makes the anchor stage 5 minutes instead of 30.

**Skip when:** user has already provided concrete reference URLs (use those directly); the project is non-visual (CLI tool, backend script — anchors don't apply); the user explicitly wants to skip references and iterate from first principles (rare, but valid).

## Steps

1. **Confirm scope and tool fit** — verify project idea is buildable; pick tool (Lovable for web/UI-heavy, Claude Code for local/CLI). Tool selection matrix → `references/frameworks.md` ("Tool Selection Matrix").
2. **Run the Four Definitions** → `references/frameworks.md` ("The Four Definitions"). Object, Mood, Purpose, Anchors. If user can't answer anchors, stop and gather references first.
3. **Define MVP scope** — core features for v1, nice-to-haves for v2+, technical requirements (auth, DB, integrations, AI). Interactive planning playbook → `references/project-planning.md`.
4. **Read DESIGN.md tokens** (if client has one at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md`) — translate to CSS variables → Tailwind config → shadcn primitives. Pipeline contract → `references/design-pipeline.md`. Authority: `.claude/rules/design-production.md`. If no DESIGN.md, recommend `/brand-kit` first; do not invent tokens.
5. **Apply The Flip** — ask the AI / user "what info do you need from me to build this?" before generating the seed prompt. Surfaces gaps before they become problems.
6. **Generate seed prompt** — Lovable: component-based with style buzzwords; Claude Code: project setup + first-feature prompt. Library of 100+ copy-paste prompts → `references/prompt-library.md`. Project starters → `references/project-templates.md`. Lead-magnet-specific prompt template → `references/output-template.md` ("Lead magnet prompt template"). Lead-magnet pattern guide → `references/lead-magnets.md`. Named tool recipes (9 paste-ready builds — grader / calculator / generator / quiz / game + internal utilities) → `references/tool-recipes.md`. Lovable-specific prompting → `references/lovable-guide.md`. Claude Code terminal setup → `references/claude-code-setup.md`.
7. **Coach the iteration loop** → `references/frameworks.md` ("The Iteration Loop"). The Spread (3–10 variations) → The Articulation (one variable, named gap) → The Chisel (combine + lock) → The Re-Anchor (if circling). Bad-vs-good articulation examples in the same file.
8. **Plan deployment** — Lovable: automatic hosting (optional custom domain); Claude Code: GitHub → Vercel. Backend: Supabase for auth/DB/storage; API keys for AI features. Expect 1–5 error cycles on first deployment; copy entire error log → paste to AI → let it fix.
9. **Apply guardrails + verification loop** (for autonomous builds) → `references/frameworks.md` ("Anti-hallucination guardrails", "Verification loop"). Write → Build → Test → Lint → Fix → Repeat; stop after 3 failed attempts and ask the user.
10. **Self-evaluate against quality checklist** → `references/frameworks.md` ("Quality checklist"). Planning, prompt, execution gates.
11. **Deliver project plan** per output template → `references/output-template.md` (Project plan: tool recommendation, Four Definitions, MVP, seed prompt, execution roadmap, questions, iteration prompts, skill improvement notes).
12. **Push** — save plan inline in chat or as a markdown doc; if part of a client engagement, route to the client's `apps/{appname}/` folder per CLAUDE.md "App Repos — Push Routing Rules".
13. **Offer iteration prompts** post-delivery → `references/output-template.md` ("Post-output iteration prompts"). On positive signal ("deployed successfully", "prompt worked great"), capture as reference example and update the prompt library — auto-update protocol in `references/frameworks.md` ("Auto-update").

## What good looks like

### References

- **Core frameworks** → `references/frameworks.md` — Four Definitions, Iteration Loop (Flip / Spread / Articulation / Chisel / Re-Anchor), Tool Selection Matrix, Lead Magnet Types by Virality, anti-patterns, anti-hallucination guardrails, verification loop, auto-update protocol, quality checklist.
- **DESIGN.md → CSS → shadcn pipeline** → `references/design-pipeline.md` — token translation contract, forbidden / required patterns, integration with `.claude/rules/design-production.md`.
- **Output template + worked example** → `references/output-template.md` — full project plan template, lead magnet prompt template, GTM readiness quiz worked example, post-output iteration prompts.
- **Interactive planning framework** → `references/project-planning.md` — full guided session for gathering inputs when user shows up under-briefed.
- **Prompt library** → `references/prompt-library.md` — 100+ copy-paste prompts categorized by use case (Lovable + Claude Code).
- **Project templates** → `references/project-templates.md` — starter prompts for common project types (quizzes, calculators, generators, microsites).
- **Lead magnets** → `references/lead-magnets.md` — quiz / calculator / generator / analyzer / simulator patterns, virality features, email capture flows (the *strategy* layer: types, gating theory, virality, metrics).
- **Tool recipes** → `references/tool-recipes.md` — 9 named, paste-ready builds (grader, cost calculator, generator, quiz, game + UTM builder, content repurposer, subject-line previewer, brief generator), each with its build prompt, capture mechanic, and distribution play (the *recipe* layer — canonical for the concrete build).
- **Lovable guide** → `references/lovable-guide.md` — Lovable-specific prompting style, style buzzwords, component-based structure, common Lovable patterns.
- **Claude Code setup** → `references/claude-code-setup.md` — terminal setup, project scaffolding, common commands, GitHub → Vercel deployment.
- **Use cases** → `references/use-cases.md` — 50+ real examples of vibe-coded outputs from the workspace.
- **Troubleshooting** → `references/troubleshooting.md` — common errors and fixes (build failures, deploy failures, integration breakage).

### Examples

Successful vibe-coded outputs are captured under `references/examples/{date}-{project-type}.md` when the user signals approval ("deployed successfully", "prompt worked great"). See the auto-update protocol in `references/frameworks.md`.

### Evaluations (binary pass/fail before declaring "done")

- Four Definitions answered completely (Object, Mood, Purpose, Anchors).
- Tool selection justified with rationale tied to project shape (Lovable vs. Claude Code).
- MVP scope is clear, buildable, and explicit about what's NOT in v1.
- Technical requirements identified (auth, DB, integrations, AI).
- Seed prompt is ready to paste — no `[FILL THIS IN]` placeholders left.
- Iteration prompts follow the one-variable rule (no multi-variable requests).
- Deployment path is concrete (Lovable: hosting + domain; Claude Code: GitHub → Vercel).
- Anti-hallucination guardrails applied: no promised features that the chosen tool can't deliver.
- DESIGN.md tokens translated through CSS variables → Tailwind → shadcn (web stack only); no hardcoded hex / font / radius values in component code.
- Quality checklist gates passed (`references/frameworks.md` "Quality checklist").

## Push

- **Inline output** — project plan rendered in chat for immediate use.
- **Client app folder** (when part of engagement) — route to `projects/consulting/active/{client}/apps/{appname}/` per CLAUDE.md "App Repos — Push Routing Rules". Each app has its own GitHub remote; never push the app folder to the master claude-code repo.
- **Reference example capture** — on positive signal, save approved prompt + approach to `references/examples/{date}-{project-type}.md`.

## Integration with other skills

| Direction | Skill | What flows |
|-----------|-------|-----------|
| **Receives from** | `/brand-kit` | DESIGN.md tokens (colors, type, spacing, components) for on-brand builds |
| **Receives from** | `/dashboard` | Dashboard spec → React build hand-off |
| **Receives from** | `/figma-to-prototype` | Figma file → interactive React prototype hand-off |
| **Feeds into** | `/landing-page-copy` | Marketing pages around the deployed tool |
| **Pairs with** | `/workflow-prompt-design` | In-tool AI prompts (e.g., quiz scoring, generator logic) |

**Recommended chains:**

- New lead magnet: `/brand-kit → /vibe-coding → /landing-page-copy` (tool + marketing page on a shared brand contract).
- Interactive prototype: `/figma-to-prototype → /vibe-coding` (designer hands off; vibe-coding ships the React app).
- Internal dashboard: `/dashboard → /vibe-coding` (spec → build).

**Build-shape seam:** full hosted apps (Next.js/Vercel, backend, auth) live here. Single-file, single-purpose utilities with an export button — a UTM builder, a subject-line previewer — are better as throwaway HTML tools; see [`throwaway-editor-pattern.md`](../../../../rules/throwaway-editor-pattern.md). The recipe library (`references/tool-recipes.md`) tags each of the 9 builds with its shape.

## Design cycle (post-authoring phases)

After producing the happy-path output, walk these phases before ship. Each references the shared design-quality library at `../../meta/catalog/design-reviewer/references/`. Run `/design-reviewer` as the final ship-ready gate.

- **Layout** — `layout-tenets.md` (rhythm, alignment, density)
- **Distill** — `distill-principles.md` (strip-to-essence)
- **Typeset** — `typeset-principles.md` (measure, leading, scale)
- **Polish** — `polish-principles.md` (16 details + interaction states)
- **Harden** — `harden-checklist.md` (9-step production-readiness)
- **Cognitive load** — `cognitive-load-tenets.md` *(when output is data-dense — admin panels, settings, multi-field forms)*
- **Delight** — `delight-patterns.md` (1–3 moments per screen, brand-tone calibrated)
- **Onboarding** — `onboarding-patterns.md` *(when output is SaaS-shaped — multi-screen apps with first-run flows)*
- **Final review** — run `/design-reviewer` (5 dimensions × 0–4, P0–P3 severity)

## Pre-slim original

Pre-slim SKILL.md (788 lines, v2.0) archived at `.claude/skills/_archive/vibe-coding/SKILL-pre-slim-20260429.md`. Phase 3 lossless slim hoisted Four Definitions / Iteration Loop / Tool Matrix / guardrails / verification loop / auto-update protocol → `references/frameworks.md`; DESIGN.md → CSS → shadcn pipeline → `references/design-pipeline.md`; project plan template + lead magnet template + worked example → `references/output-template.md`. Existing references (project-planning, prompt-library, project-templates, lead-magnets, lovable-guide, claude-code-setup, use-cases, troubleshooting) untouched.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

