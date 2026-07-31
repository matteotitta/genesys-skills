---
name: metadata-lint
version: '1.0'
last_updated: 2026-05-01
author: genesys-growth
description: 'Audits and fixes HTML metadata in code: page titles, meta descriptions, canonical URLs, Open Graph tags, Twitter cards, favicons, JSON-LD structured data, robots directives. Use when adding SEO metadata, fixing social share previews, reviewing OG tags, setting up canonical URLs, or shipping new pages that need correct meta tags. Triggered by "metadata audit", "fix OG tags", "social share preview broken", "canonical URL", "JSON-LD", or "lint my page metadata". Code-level lint with priority-ordered fixes. Feeds into website-pm-score and aeo-strategy.'
goal: Lint HTML head metadata across pages and propose minimal targeted fixes ordered by impact.
outcome: Per-page audit report listing metadata violations with severity, the rule violated, and a code-level fix; downstream skills (website-pm-score, aeo-strategy) consume the findings to prioritise crawl-budget, social-share, and structured-data work.
primitive: website
sub_primitive: audit
ontology_type: content-audit
review_gate: 1
inputs:
  required: []
  recommended:
  - company-context
- type: content-audit
  feeds_into:
  - website-pm-score
  - aeo-strategy
depends_on: []
- website-pm-score
- aeo-strategy
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands:
  - /metadata-lint
  natural_language:
  - "audit my page metadata"
  - "fix OG tags"
  - "social share preview is broken"
  - "lint canonical URLs"
  - "review JSON-LD structured data"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: low
---

<!-- Sourced from ibelick/ui-skills (MIT). https://github.com/ibelick/ui-skills/blob/main/skills/fixing-metadata/SKILL.md. See../../../meta/catalog/design-reviewer/NOTICE.md for the MIT attribution block. -->

# Metadata lint

Audits HTML head metadata against a priority-ordered rule set and proposes minimal, scoped fixes. The output is the audit report — not a refactor, not a strategy doc. Pair with `/website-pm-score` (broader page audit) or `/aeo-strategy` (search-visibility strategy) to act on the findings.

Sourced from [ibelick/ui-skills](https://github.com/ibelick/ui-skills/blob/main/skills/fixing-metadata/SKILL.md) under MIT (Julien Thibeaut, 2026). Adapted to the Genesys Phase 4 SKILL.md schema; substantive content preserved.

> **Design-contract exemption note:** This skill carries `primitive: website` but is NOT a design-output skill (the `design-production.md` applies to skills that produce visual deliverables — landing pages, wireframes, dashboards, decks). Metadata-lint produces a text audit report listing HTML head violations and code-level fixes; there is no DESIGN.md token consumption, no visual surface, no design-cycle phases to walk. The validator's design-contract warning is an expected false positive driven by the `primitive: website` taxonomy heuristic.

---

## Triggers

Run when:
- Adding or changing page titles, descriptions, canonical URLs, robots directives
- Implementing Open Graph or Twitter card metadata
- Setting favicons, app icons, manifest, theme-color
- Building shared SEO components or layout metadata defaults
- Adding structured data (JSON-LD)
- Changing locale, alternate languages, or canonical routing
- Shipping new pages, marketing pages, or shareable links

Do NOT run for:
- Strategic decisions about what TO put in metadata (that's `/aeo-strategy` or `/messaging`)
- Whole-page audits — use `/website-pm-score` instead; metadata-lint is the head-tags slice

---

## Inputs

| Input | Required | Notes |
|---|---|---|
| HTML file path or live URL | Yes | One target per run; loop the skill for multi-page audits |
| Brand context | Recommended | Read `projects/consulting/{client}/CLAUDE.md` if reviewing client work — title format + voice should match |
| Existing metadata system | Inferred from code | Next.js metadata API, react-helmet, manual `<head>`, Astro frontmatter — match the project's pattern |

---

## Workflow

1. Identify pages with missing or incorrect metadata (titles, descriptions, canonical, OG tags)
2. Audit against the priority rules below — fix critical issues (duplicates, indexing) first
3. Ensure title, description, canonical, and og:url all agree with each other
4. Verify social cards render correctly on a real URL, not localhost
5. Keep diffs minimal and scoped to metadata only — do not refactor unrelated code

---

## Rule categories by priority

| Priority | Category | Impact |
|---|---|---|
| 1 | Correctness and duplication | Critical |
| 2 | Title and description | High |
| 3 | Canonical and indexing | High |
| 4 | Social cards | High |
| 5 | Icons and manifest | Medium |
| 6 | Structured data | Medium |
| 7 | Locale and alternates | Low-medium |
| 8 | Tool boundaries | Critical |

---

## Quick reference

### 1. Correctness and duplication (critical)

- Define metadata in one place per page; avoid competing systems
- Do not emit duplicate `title`, `description`, `canonical`, or `robots` tags
- Metadata must be deterministic — no random or unstable values
- Escape and sanitize any user-generated or dynamic strings
- Every page must have safe defaults for title and description

### 2. Title and description (high)

- Every page must have a title
- Use a consistent title format across the site (e.g., `{Page} — {Brand}`)
- Keep titles short and readable; avoid stuffing
- Shareable or searchable pages should have a meta description
- Descriptions must be plain text — no markdown, no quote spam

### 3. Canonical and indexing (high)

- Canonical must point to the preferred URL for the page
- Use `noindex` only for private, duplicate, or non-public pages
- Robots meta must match actual access intent
- Previews or staging pages should be `noindex` by default when possible
- Paginated pages must have correct canonical behavior

### 4. Social cards (high)

- Shareable pages must set Open Graph title, description, and image
- Open Graph and Twitter images must use absolute URLs
- Prefer correct image dimensions and stable aspect ratios
- `og:url` must match the canonical URL
- Use a sensible `og:type`, usually `website` or `article`
- Set `twitter:card` appropriately, `summary_large_image` by default

### 5. Icons and manifest (medium)

- Include at least one favicon that works across browsers
- Include `apple-touch-icon` when relevant
- Manifest must be valid and referenced when used
- Set `theme-color` intentionally to avoid mismatched UI chrome
- Icon paths should be stable and cacheable

### 6. Structured data (medium)

- Do not add JSON-LD unless it clearly maps to real page content
- JSON-LD must be valid and reflect what is actually rendered
- Do not invent ratings, reviews, prices, or organization details
- Prefer one structured data block per page unless required

### 7. Locale and alternates (low-medium)

- Set the `html lang` attribute correctly
- Set `og:locale` when localization exists
- Add `hreflang` alternates only when pages truly exist
- Localized pages must canonicalize correctly per locale

### 8. Tool boundaries (critical)

- Prefer minimal changes — do not refactor unrelated code
- Do not migrate frameworks or SEO libraries unless requested
- Follow the project's existing metadata pattern (Next.js metadata API, react-helmet, manual head, Astro frontmatter, etc.)

---

## Common fixes

```html
<!-- Missing title: add one with consistent format -->
<!-- before --> <head><meta name="description" content="..." /></head>
<!-- after --> <head><title>Pricing — Acme</title><meta name="description" content="..." /></head>

<!-- og:url disagrees with canonical: align them -->
<!-- before -->
<link rel="canonical" href="https://acme.com/pricing" />
<meta property="og:url" content="https://acme.com/pricing/" /> <!-- trailing slash -->
<!-- after --> both URLs match exactly

<!-- Open Graph image is relative: must be absolute -->
<!-- before --> <meta property="og:image" content="/og.png" />
<!-- after --> <meta property="og:image" content="https://acme.com/og.png" />

<!-- Robots tag wrong on staging: add noindex -->
<!-- before --> (no robots tag on staging.acme.com)
<!-- after --> <meta name="robots" content="noindex,nofollow" />
```

```jsx
// Next.js 14+ metadata API — single source of truth per page
export const metadata = {
  title: "Pricing — Acme",
  description: "...",
  alternates: { canonical: "https://acme.com/pricing" },
  openGraph: {
    title: "Pricing — Acme",
    description: "...",
    url: "https://acme.com/pricing", // matches canonical
    images: ["https://acme.com/og.png"], // absolute
    type: "website",
  },
  twitter: { card: "summary_large_image" },
};
```

---

# Metadata lint — {page-or-url}
Date: 2026-05-01

## Critical (P1) — must-fix before ship
- [Rule 1.2 duplication] `<title>` defined in both layout.tsx:12 AND page.tsx:8 — emit one source of truth
  Fix: remove page-level title; rely on layout default with `metadata` export

## High (P2) — fix this cycle
- [Rule 4.3 OG image] og:image is relative `/og.png` — must be absolute
  Fix: prefix with site origin or move to env var SITE_URL

## Medium (P3) — backlog
- [Rule 6.2 JSON-LD] Organization schema missing `address` despite render of contact info
  Fix: add `address` field or remove the schema block

## Verified clean
- ✓ Title format consistent
- ✓ Canonical agrees with og:url
- ✓ robots:noindex correctly absent on production
```

---

## Review guidance (gate 1 — quick review)

- Fix critical issues first (duplicates, canonical, indexing)
- Ensure title, description, canonical, and og:url agree
- Verify social cards on a real URL, not localhost
- Prefer stable, boring metadata over clever or dynamic
- Keep diffs minimal and scoped to metadata only

---

## Self-roast checklist

Before delivering the audit report, ask:

- Did the lint catch ALL duplicate `<title>` / `<meta name="description">` / canonical / robots tags?
- Did `og:url` match the canonical exactly (trailing slashes, protocol, subdomain)?
- Was the social card actually tested on a real URL (LinkedIn / Twitter card validator), not just inspected locally?
- Did fixes stay scoped to metadata? (No drive-by refactors of unrelated head tags or layout components.)
- For multi-page audits: is the title format consistent across pages?

If any answer is "no" or "didn't check", re-run that section before shipping the report.

---

## Cross-references

- Broader page audit (perf + a11y + content + metadata) → `/website-pm-score`
- AI search visibility strategy + citation gap planning → `/aeo-strategy`
- Source skill (MIT) → [ibelick/ui-skills/skills/fixing-metadata](https://github.com/ibelick/ui-skills/blob/main/skills/fixing-metadata/SKILL.md)

---

