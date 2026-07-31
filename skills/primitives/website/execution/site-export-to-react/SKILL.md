---
name: site-export-to-react
version: '1.0'
last_updated: 2026-07-13
author: genesys-growth
description: 'Migrates a no-code site export into a code-owned React app on TanStack Start (SSR) + Netlify, pixel-parity via verbatim vendor CSS + class names and a Storybook-first Source-of-Truth component hierarchy. Two adapters — Webflow (reconstruct from the static HTML/CSS/JS export) and Framer (orchestrate the live unframer MCP React export) — feed one shared scaffold/ship backbone. Triggers: /site-export-to-react, "migrate this Webflow site to React", "convert this Framer project to code", "own the code for my no-code site", or a repo that already contains a Webflow export at its root. Recommends brand-kit for net-new components added after parity. NOT for: cloning a live URL you don''t hold the export for (use /website-clone), Figma→React (use /figma-prototype), or a fresh build from positioning (use /website-build).'
goal: Migrate a Webflow or Framer no-code site into a pixel-parity, code-owned React app on TanStack Start + Netlify.
outcome: 'A deployable TanStack Start (SSR) codebase matching the source no-code site pixel-for-pixel: vendor CSS kept as the parity anchor, a Storybook-backed SOT component hierarchy, the vendor runtime re-implemented in React, shipped to Netlify. Ready for /website-score.'
primitive: website
sub_primitive: execution
ontology_type: landing-page-copy
review_gate: 3
inputs:
  required:
  - source_export
  recommended:
  - brand-kit
  - target_netlify_site
- type: deployed-website
  feeds_into:
  - website-pm-score
depends_on: []
- website-pm-score
owned_by_agent: operator
mcps_used:
- unframer
- github
- github
triggers:
  slash_commands:
  - /site-export-to-react
  natural_language:
  - migrate this Webflow site to React
  - convert this Framer project to code
  - own the code for my no-code site
  - Webflow export to React
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 1
effort: high
paths: projects/consulting/**,projects/apps/**
---

# /site-export-to-react — no-code export → code-owned React

Migrate a **Webflow** or **Framer** no-code site into a maintainable, code-owned React app on **TanStack Start** (SSR) + **Netlify**. Two front-end adapters feed one shared backbone. The design already exists — the job is **fidelity**: keep the source's compiled CSS + class names verbatim so the site is pixel-parity and shippable at every intermediate commit.

Adapted from [`dmenchaca/webflow-to-react`](https://github.com/dmenchaca/webflow-to-react) (MIT © 2026 Diego Menchaca) per `/steal` analysis (`.claude/discovery/0726-webflow-to-react-steal-analysis.md`). The Framer adapter orchestrates the live `unframer` MCP — never vendoring its source. See [`NOTICE.md`](NOTICE.md).

Deploy discipline lives in [`.claude/rules/tanstack-netlify-deploy.md`](../../../../../rules/tanstack-netlify-deploy.md) (auto-loads on this stack).

---

## Triggers

**Invoke when user says:**
- `/site-export-to-react <export-path | framer-project>`
- "migrate this Webflow site to React" / "own the code for my no-code site"
- "convert this Framer project to code"
- The repo already contains a Webflow export (`index.html` + `css/` + `js/` + `images/` + `fonts/`) at its root

**Do NOT invoke when:**
- User only has a live URL, not the export → use `/website-clone` (DOM-scrape path)
- Source is Figma → use `/figma-prototype`
- Fresh site from positioning + messaging → use `/website-build`
- Webflow **CMS** dynamic collections are the ask — static export only; CMS is out of scope

---

## Inputs

| Input | Required? | Source |
|-------|-----------|--------|
| `source_export` | required | A Webflow static-export folder/ZIP **or** a Framer project ID (with the "React Export" plugin enabled) |
| `brand-kit` | recommended | DESIGN.md tokens — applied to **net-new** components added after parity (not to the preserved vendor CSS) |
| `target_netlify_site` | recommended | Existing Netlify site to deploy into |

If neither a Webflow export nor a Framer project is present, name what's missing and stop — don't guess.

---

## Adapter routing (detect the source first)

```
source_export
     │
     ├─ Webflow static export (index.html + css/ + js/ + fonts/ + images/)
     │ → the premium reference (reconstruct-from-export, 12 phases)
     │
     └─ Framer project (React-Export plugin enabled)
              → the premium reference (orchestrate unframer → real React components)
                       │
                       ▼
          shared backbone → the premium reference
          (TanStack Start scaffold · repo layout · Storybook parity · SSR guards)
                       │
                       ▼
          parity gates → the premium reference (review_gate: 3)
                       │
                       ▼
          ship →.claude/rules/tanstack-netlify-deploy.md
```

**Webflow** = reconstruct the DOM as owned components, keeping the vendor's compiled CSS + class names verbatim. **Framer** = the export can't be reconstructed the same way (obfuscated, motion-coupled), so delegate extraction to `unframer` (`mcp__unframer__exportReactComponents`), then wrap its emitted `.jsx`/`.css` in the same backbone. Both paths converge on the shared scaffold, Storybook SOT hierarchy, parity gates, and Netlify ship.

---

## Non-negotiable posture (both adapters)

1. **Export is a read-only reference, not the runtime.** Never `git`-edit the source export. Reconstruct it.
2. **No `dangerouslySetInnerHTML` for layout.** Banned for page structure. Allowed only for small, sanitized, content-shaped fragments (e.g. CMS body) when explicitly chosen.
3. **Vendor CSS + class names are preserved verbatim — this is the parity anchor, not a token-hardcoding violation.** The design-authorship "cite tokens, never hardcode" rule (`.claude/rules/design-production.md`) applies to **net-new** components added *after* parity; the migrated surface keeps the source's compiled CSS untouched so parity holds at every commit. Brand-kit DESIGN.md tokens style only what you add.
4. **Delete the vendor runtime.** Drop jQuery + `webflow.js` (Webflow) / re-map `framer-motion` runtime coupling (Framer); re-implement behaviors as React state/hooks. Keep GSAP — port to `useEffect` + `gsap.context()`, never rewrite to Framer Motion.
5. **Storybook-first Source of Truth.** UI primitives → section components → routes, each with a variant story, before composing routes. Storybook imports the **same CSS chain** as production.
6. **SSR-guard every browser API.** TanStack Start renders on the server — `window`/`document`/GSAP run in `useEffect` only.

---

## Workflow at a glance

| Step | Purpose | Adapter |
|------|---------|---------|
| **1. Detect + audit** | Identify Webflow export vs Framer project; catalog (don't edit) fonts, CSS, JS, sections | both |
| **2. Scaffold backbone** | TanStack Start in `web/`, Netlify plugin, Tailwind, root/proxy `package.json` | both — `backbone.md` |
| **3a. Webflow extract** | Migrate assets + verbatim CSS barrel; port `<head>`; build SOT hierarchy | Webflow — `webflow-adapter.md` |
| **3b. Framer extract** | Run `unframer` export; wrap emitted components; map Framer variables → props | Framer — `framer-adapter.md` |
| **4. Storybook SOT** | UI primitives + section stories with CSS parity, before routes | both |
| **5. Routes + runtime** | Compose sections in source order; re-implement interactions; GSAP in `useEffect` | both |
| **6. Parity gates** | Run the checklists (review_gate: 3) | both — `checklists.md` |
| **7. Ship** | Netlify deploy per the deploy rule; post-deploy verify | both |

---

## Anti-hallucination guardrails

1. **No estimated CSS.** Webflow keeps the vendor's compiled CSS verbatim; Framer keeps `unframer`'s emitted CSS. Never hand-measure.
2. **No paraphrased copy.** Source text is preserved character-for-character unless the user asks to edit.
3. **No raw export HTML in routes.** Once a section SOT/story exists, routes import it — never paste export markup.
4. **Never vendor `unframer`.** The Framer adapter calls the published MCP/CLI as a runtime dependency; nothing from its no-license source is copied into the repo.
5. **No stack-scanner fingerprints.** Strip `data-wf-*` / editor metadata from the document shell (Webflow); set `generator` meta to the real stack.
6. **No green-build-means-done.** A green Netlify build only validates bundling — hit the live URL to confirm the SSR function starts.

---

## Composition with other skills

| Stage | Skill | Why |
|-------|-------|-----|
| Before | `/brand-kit` | DESIGN.md tokens for net-new components added after parity |
| After | `/website-score` | PM evaluation of the migrated site |
| Copy refresh | `/website-copy` | Replace migrated copy with positioning-driven copy |
| Different intent | `/website-clone` (live URL) · `/website-build` (fresh) · `/figma-prototype` (Figma) | Not export-migration jobs |

---

## Design cycle (post-authoring phases)

The source design is inherited — parity is the goal, so most phases apply to **net-new** components added after parity. References at `../../../../meta/catalog/design-reviewer/the premium reference (adjust depth per this skill's location):

- **Layout** — `layout-tenets.md` (rhythm, alignment) — for net-new sections only
- **Typeset** — `typeset-principles.md` (measure, leading, scale) — verify migrated type matches source
- **Polish** — `polish-principles.md` (16 details + interaction states) — re-implemented behaviors
- **Harden** — `harden-checklist.md` (9-step production-readiness — code output)
- **Motion craft** — `motion-craft.md` — GSAP ports keep source timing
- Distill / Cognitive-load / Delight / Onboarding — **N/A** for a faithful migration (the design already exists)

---

## Final ship gate

Run `/premortem --output` before ship. See `.claude/skills/meta/orchestration/premortem/SKILL.md` for the 5 execution domains and output template.

Run `/design-reviewer` as the final ship-ready gate — after the premortem passes.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change`.

---

## External references

- `.claude/rules/tanstack-netlify-deploy.md` — deploy discipline (this skill's ship step)
- `.claude/rules/design-production.md` — DESIGN.md tokens for net-new components
- `.claude/discovery/0726-webflow-to-react-steal-analysis.md` — the /steal analysis

---

