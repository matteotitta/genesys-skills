---
name: programmatic-seo
version: '1.0'
last_updated: 2026-01-21
author: genesys-growth
description: Designs scaled content strategies producing hundreds or thousands of pages from structured data. Covers integrations
  directories, comparison pages, templates directories, use-case pages, and landing page factories. Produces page templates,
  data schemas, URL structures, internal linking maps, and deployment specifications. Triggered by "programmatic SEO", "pSEO",
  "scaled content", "landing page factory", "comparison pages at scale", or "template directory". Consumes icp-behavioural,
  competitor-research, and aeo-content as upstream context. Feeds into landing-page-copy and aeo-content for page-level execution.
  NOT for individual article writing — use /aeo-content instead.
goal: Designs scaled content strategies producing hundreds or thousands of pages from structured data.
outcome: Designs scaled content strategies producing hundreds or thousands of pages from structured data. Covers integrations
  directories, comparison pages, templates directories, use-case pages, and landing page factories. Produces page templates,
  data schemas, URL structures, internal linking maps,...
primitive: seo-aeo
sub_primitive: execution
ontology_type: aeo-content
review_gate: 2
inputs:
  required: []
  recommended:
  - icp-behavioural
  - competitor-research
  - aeo-content
- type: pseo-strategy
  feeds_into:
  - website-copy
  - aeo-content
depends_on: []
- aeo-content
- website-copy
owned_by_agent: operator
mcps_used:
- exa
- gdrive
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
---

# Programmatic SEO

Design scalable content strategies that produce hundreds or thousands of search-optimized pages from structured data. Match data assets to one of 12 proven playbooks, then specify the schema, URL structure, templates, internal linking, and quality controls needed to ship without thin content. Output is a strategy document — not page copy. Hand off to `/landing-page-copy` or `/aeo-content` for execution.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in programmatic-seo |
|---|---|---|
| **R1** | Source placement | Strategy doc → client-team review surface → cleaned tags in appendix toggle. Rendered template pages → end-customer-facing → no sources. |
| **R3** | Product-update tone | Template copy directions frame as capability-led. |
| **R6** | CTA hierarchy | Per-template CTA → sign-up primary for bottom-of-template, blog as fallback for top. |
| **R7** | FAQ titles + no sources block | Template URL patterns use FAQ shape where applicable ("X vs Y", "How to do X with Y"). |
| **R8** | Entity-name headings | Template section headings repeat the variable entity name. |
| **R9** | Action-oriented section names | "How [Entity] works / How to choose [Entity]" — verb-led. |

- User asks for "programmatic SEO", "pSEO", "scaled content", "landing page factory", "comparison pages at scale", "[X] vs [Y] pages", "alternative pages strategy", or "template directory"
- Client has structured data (integrations, locations, competitors, templates, glossary terms, entities) and wants traffic from long-tail patterned queries
- Strategy needed before execution: schema, URLs, templates, linking, quality gates

**Do NOT run when:** single landing page (use `/landing-page-copy`), broad content strategy (use `/aeo-content`), competitor research only (use `/competitor-research`).

Full trigger list + flowchart: the premium reference.

## Inputs

**Required:**

| Input | Description | Source |
|-------|-------------|--------|
| Business model | What the company does | User provides |
| Data assets | What structured data exists or can be created | User provides or discover |

**Recommended (improves quality):** competitor pSEO examples, search demand data, ICP research, existing content audit. Optional input table + validation checklist: the premium reference.

**Upstream skills:** `icp-behavioural`, `competitor-research`, `aeo-content` (recommended, not required).

## Steps

1. **Asset audit (Phase 1).** Inventory existing or creatable structured data. Confirm business model + goal (traffic / conversions / authority). If inputs missing, ask before proceeding.
2. **Match data to playbooks (Phase 2.1).** Use the 12-playbook matrix in the premium reference (Templates, Curation, Conversions, Comparisons, Examples, Locations, Personas, Integrations, Glossary, Translations, Directory, Profiles).
3. **Evaluate search demand (Phase 2.2).** Research keyword patterns, estimate volume, assess difficulty. Never invent volume — flag as "estimated, validate with keyword research" if no data.
4. **Assess competitive landscape (Phase 2.3).** Saturation, quality, authority, differentiation. Use `find_similar_links_exa` against client URL to surface competitor pSEO.
5. **Select 1-2 playbooks (Phase 2.4).** Use the prioritization matrix (data readiness × demand × competition) in the premium reference. Recommend starting with one playbook before expanding.
6. **Design data schema (Phase 3.1).** YAML schema for the entities powering pages. Example schemas per playbook: the premium reference.
7. **Define URL structure (Phase 3.2).** Hyphenated, keyword-bearing, predictable. Pattern table per playbook in the premium reference.
8. **Specify template sections (Phase 3.3).** Hero, quick answer, dynamic comparison/data block, use-case guidance, FAQ (with FAQ schema), CTA. Every page needs unique value, dynamic content, static framework, internal links, conversion path.
9. **Map internal linking (Phase 3.4).** Hub-and-spoke — every page → category hub, related pages cross-link, footer/sidebar navigation.
10. **Specify schema markup (Phase 3.5).** Pick primary + additional schema per playbook. JSON-LD templates: the premium reference. Schema-by-playbook table: the premium reference.
11. **Define quality controls (Phase 4).** Word-count thresholds (Comparison ≥1,000 / Template ≥500 / Glossary ≥300 / Directory ≥400), differentiation requirements, maintenance schedule. Full thresholds + checks: the premium reference.
12. **Run self-evaluation.** Completeness, evidence quality, guardrails, self-roast questions. Full protocol: the premium reference.
13. **Format output.** Use the standard 7-section structure (Executive Summary → Asset Inventory → Playbook Recommendation → Architecture → Schema Plan → Quality Controls → Roadmap → Success Metrics). Full template: the premium reference.
14. **Present at Review Gate 2 (Standard).** Actions: Approve / Validate demand / Pilot first. Recommend 10-page pilot before scaling to 100+.
15. **Suggest chain.** "Ready to write template copy with `/landing-page-copy`?" / "Want to detail the data schema?" / "Audit competitor pSEO with `/competitor-research`?"

## What good looks like

### Evaluations (binary)

- [ ] Playbook recommendation has explicit rationale (data readiness + demand + competitive gap)
- [ ] Search demand estimated with basis, not invented
- [ ] Data schema defined in YAML
- [ ] URL pattern documented with example
- [ ] Template sections specified (≥5 sections, mix of dynamic + static)
- [ ] Internal linking architecture mapped
- [ ] Schema markup types named per page type
- [ ] Word-count thresholds set per page type
- [ ] Differentiation requirements stated (no boilerplate-only)
- [ ] Maintenance schedule named with triggers
- [ ] No guaranteed rankings; thin-content risk flagged
- [ ] Pilot of 10 pages recommended before scaling

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
