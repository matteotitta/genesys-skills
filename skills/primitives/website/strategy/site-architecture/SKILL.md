---
name: site-architecture
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Plans page hierarchies, navigation systems, URL structures, and internal linking with sharp heuristics — 3-click rule, 4–7 primary nav items, 5–10 internal links per 1k words, 2–4 hierarchy levels optimal, no orphan pages. Produces ASCII hierarchy + Mermaid diagram + URL map + internal-linking plan ready for developer implementation. Triggered by "site architecture", "URL structure", "navigation plan", "internal linking strategy", "site map plan", "hub and spoke". NOT for auditing existing architecture — use /website-audit for the inverse direction.
goal: Plan a page hierarchy + URL + nav + internal-linking system that supports both user navigation and search-engine crawlability.
outcome: Produces (1) ASCII hierarchy diagram, (2) Mermaid network diagram, (3) URL map table, (4) navigation zone spec (header / footer / sidebar / breadcrumbs), (5) internal-linking plan (hub-and-spoke), (6) developer-ready implementation spec.
primitive: website
sub_primitive: strategy
ontology_type: content-strategy
review_gate: 2
inputs:
  required: []
  recommended:
  - content-strategy
  - icp-research
  - aeo-strategy
- type: content-strategy
  feeds_into:
  - website-pm-score
depends_on: []
- website-pm-score
- landing-page-wireframe
owned_by_agent: growth
mcps_used:
- exa
- firecrawl
- gdrive
triggers:
  slash_commands:
  - /site-architecture
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /site-architecture — page hierarchy + URL + internal linking plan

Plan the bones of a site: hierarchy, URLs, navigation, internal linking. SEO outcomes (crawl budget, authority distribution, ranking ceiling) and UX outcomes (findability, navigability) both depend on this layer being right.

---

## When to invoke

- Building a new site or microsite.
- Major content-library expansion (e.g., ClientCo adding 50+ articles, content needs structural discipline).
- Multi-product site restructure (e.g., ClientCo product-A + product-B).
- Pre-launch: never ship a new site without an explicit architecture plan.

---

## Workflow

### Step 1 — Hierarchy decisions

Choose between flat and deep:

| Style | Levels | Best for |
|---|---|---|
| Flat | 2 levels | Single-product SaaS, small content library (<30 pages) |
| Optimal | 2–4 levels | Standard SaaS with content marketing |
| Deep | 5+ levels | Enterprise with multi-product / multi-vertical |

**Sharp rule:** the 3-click rule — every important page should be reachable from the homepage within 3 clicks. If a page is 4+ clicks deep, it's effectively invisible to most users + crawlers.

### Step 2 — Hub-and-spoke content model

For content / blog: cluster around pillar pages.

| Component | Role |
|---|---|
| Pillar / hub page | Comprehensive overview of a topic — long-form, evergreen |
| Spoke pages | Drill-down articles on sub-topics, each linking back to the pillar |
| Cross-spokes | Articles linking to related spokes in adjacent clusters |

Hub-and-spoke concentrates topical authority; flat blog libraries dissipate it.

### Step 3 — Navigation zone design

| Zone | Role | Max items |
|---|---|---|
| Primary nav (header) | Core navigation paths | 4–7 |
| Footer | Comprehensive map (Product, Resources, Company, Legal) | 4 columns |
| Sidebar (if any) | Contextual to section | 5–10 |
| Breadcrumbs | Path-tracking on every interior page | 1 per page |

**Sharp rule:** 4–7 primary-nav items. Below 4 → site feels stub. Above 7 → cognitive load + mobile-menu pain.

### Step 4 — URL pattern decisions

Lock the patterns up-front:

| Section | Pattern | Example |
|---|---|---|
| Product | `/product/{product-name}` | `/product/report-generator` |
| Pricing | `/pricing` | `/pricing` |
| Blog | `/blog/{slug}` (no date — date URLs age badly) | `/blog/cold-email-templates` |
| Use case | `/use-cases/{slug}` | `/use-cases/financial-advisers` |
| Comparison | `/compare/{us}-vs-{them}` | `/compare/ClientCo-vs-iress` |
| Alternative | `/alternatives/{tool}` | `/alternatives/iress` |
| About | `/about` (singular; not `/company/about`) | `/about` |
| Resources | `/resources/{type}/{slug}` | `/resources/guides/lead-magnets` |

**Sharp rules:**
- Human-readable. `/blog/seo-guide` not `/blog/post-12345`.
- No date prefixes. Content gets refreshed; dates lock it in time.
- Hierarchical reflection. URL depth should match site hierarchy.
- No trailing slashes (or always — pick one, enforce).

### Step 5 — Internal linking plan

| Rule | Threshold |
|---|---|
| Internal links per 1k words of content | 5–10 |
| Every page must have ≥ 1 inbound internal link (no orphans) | mandatory |
| Anchor text varied (don't use the exact-match anchor on every link) | mandatory |
| Pillar-page link from every spoke article | mandatory |
| Cross-spoke links to related articles (3–5 per article) | recommended |

### Step 6 — Produce deliverables

The skill outputs four artifacts for the developer:

**A. ASCII hierarchy diagram:**

```
/
├── /product/
│ ├── /product/report-generator
│ └── /product/meeting-prep
├── /pricing
├── /resources/
│ ├── /resources/guides/{slug}
│ ├── /resources/templates/{slug}
│ └── /resources/calculators/{slug}
├── /compare/
│ └── /compare/ClientCo-vs-{competitor}
├── /alternatives/
│ └── /alternatives/{tool}
├── /blog/{slug}
├── /about
└── /contact
```

**B. Mermaid diagram (for the doc):**

```mermaid
graph TD
  Home[/] --> Product[/product/]
  Home --> Pricing[/pricing]
  Home --> Resources[/resources/]
  Product --> ProductA[/product/report-generator]
  Product --> ProductB[/product/meeting-prep]
  Resources --> Guides[/resources/guides/]
  Resources --> Templates[/resources/templates/]
```

**C. URL map table** with title / target keyword / status (per page).

**D. Internal-linking plan:** for each page, list inbound + outbound internal links with anchor text.

---

## Worked example — ClientCo multi-product

**Current state:** Two product domains live separately (ClientCo-website, ClientCo-homepage-v2). Architecture inconsistent.

**Proposed unified architecture:**

```
/
├── /product/
│ ├── /product/{product-A}
│ └── /product/{product-B}
├── /pricing
├── /resources/
│ ├── /resources/guides/{slug}
│ └── /resources/case-studies/{slug}
├── /compare/ClientCo-vs-{competitor}
├── /alternatives/{competitor}
├── /about
└── /contact
```

- Primary nav: 5 items (Product, Pricing, Resources, Compare, About).
- Hub-and-spoke: each product page is a hub for its product-specific guides / case studies.
- Internal linking: every blog post links to ≥ 1 pillar (product or use-case page); every product page links to ≥ 3 supporting articles.

---

## Anti-patterns

- ❌ Pages 4+ clicks deep from homepage. Invisible to crawlers + users.
- ❌ Primary nav > 7 items. Cognitive load + mobile-menu pain.
- ❌ Date-based URLs (`/blog/2026/05/post`). Lock content in time.
- ❌ Orphan pages (no inbound internal links). Crawl + authority black hole.
- ❌ Flat blog library with no pillar structure. Topical authority dispersed.
- ❌ Exact-match anchor text on every internal link. Reads as SEO manipulation.

---

## Integration with other skills

- **Upstream:** `/content-strategy` defines clusters → drives hub-and-spoke; `/aeo-strategy` defines target queries → informs URL pattern decisions; `/icp-research` informs navigation labels (audience language).
- **Downstream:** `/website-audit` audits the implemented architecture; `/landing-page-wireframe` builds individual pages within the hierarchy; `/aeo-content` produces hub + spoke content following the plan.

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/site-architecture/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/site-architecture/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice with Mermaid + ASCII output formats.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

