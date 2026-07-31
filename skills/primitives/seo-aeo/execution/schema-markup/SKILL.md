---
name: schema-markup
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Generates validated JSON-LD schema markup per page type (Product, Article, Organization, FAQ, HowTo, Review, BreadcrumbList, Person, Event, LocalBusiness) with eligible-rich-result mapping and Google Rich Results Test validation flow. Pairs `@graph` composition for multi-type pages. Chains off aeo-content outputs to enforce structured-data discipline at publish time. Triggered by "schema markup", "structured data", "JSON-LD", "rich results", "schema audit", or "add schema to [page]". NOT for general SEO audits — use /website-audit instead.
goal: Generate validated JSON-LD schema markup that maps page content to eligible Google rich results.
outcome: Produces a complete JSON-LD code block (or `@graph` composition for multi-type pages) ready to paste into `<head>` or end of `<body>`, plus a validation checklist confirming Rich Results Test passes and content alignment is intact.
primitive: seo-aeo
sub_primitive: execution
ontology_type: aeo-content
review_gate: 2
inputs:
  required: []
  recommended:
  - aeo-content
  - product-messaging
  - company-context
- type: aeo-content
  feeds_into:
  - aeo-content
depends_on: []
- aeo-content
owned_by_agent: content
mcps_used:
- exa
- firecrawl
triggers:
  slash_commands:
  - /schema-markup
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /schema-markup — JSON-LD generation + validation

Generate validated JSON-LD schema markup for a page (or batch of pages) based on the page type, available data, and target rich results. Output is paste-ready code plus a validation checklist.

This is a **page-level execution skill**, not a strategic SEO planning skill. Decide *what* content to produce via `/aeo-strategy` or `/content-strategy` first; this skill structures the markup once the content exists.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied to this skill (internal-reference floor):**

| Code | Refinement | How it lands in schema-markup |
|---|---|---|
| **R1** | Source placement | JSON-LD output is structured data, not narrative — internal-reference. Schema property attribution stays inline. |
| **R3** | Product-update tone | Skill-summary reports (validation pass/fail) frame as operator-direct. |
| **R9** | Action-oriented section names | "Generate / Validate / Paste" — verb-led. |

Note: internal-reference skill; R2/R5/R6/R7/R8 do not apply.

---

## When to invoke

- A page is shipping (new or refresh) and needs structured data before publish.
- An audit found pages missing schema or with invalid markup.
- A client is getting cited by AI engines (Perplexity, ChatGPT, Claude) but lacks validated schema to lock in eligibility.
- A `/aeo-content` run is complete and you want the schema layer applied alongside.

Do NOT invoke when:
- The page content doesn't exist yet (write copy first via `/aeo-content` or `/landing-page-copy`).
- The audit is broader than schema (`/website-audit` covers crawlability, Core Web Vitals, on-page).

---

## Workflow

### Step 1 — Page-type assessment

Identify the page's content type. Match to schema.org type + eligible rich result:

| Page type | Schema type | Eligible rich result |
|---|---|---|
| Product detail (SaaS or physical) | `Product` (+ `Offer`, `AggregateRating`) | Product snippet, price, review stars |
| Pricing page | `Product` (one per tier) or `Offer` list | Price + availability |
| Blog post / article | `Article` or `BlogPosting` | Article rich result (image, date, byline) |
| Long-form guide | `Article` + `HowTo` (if step-by-step) | Article + HowTo rich result |
| FAQ page or FAQ section | `FAQPage` | FAQ rich result |
| Company about | `Organization` | Knowledge panel, logo |
| Founder / author bio | `Person` | Knowledge panel for the person |
| Event landing page | `Event` | Event rich result (date, location) |
| Case study | `Article` + `Review` (if customer testimonial-anchored) | Article rich result; review stars |
| Local-service page | `LocalBusiness` (+ `Service`) | Local pack eligibility, hours |
| Software comparison page | `SoftwareApplication` + `Review` per option | Software rich result + review stars |
| Job posting | `JobPosting` | Job rich result on Google for Jobs |
| Breadcrumb (every page) | `BreadcrumbList` | Breadcrumb rich result |

### Step 2 — Required properties check

Each schema type has required properties Google enforces. Cross-check before generation:

- `Organization` → `name`, `url`. Recommended: `logo`, `sameAs` (social URLs).
- `Article` → `headline`, `image`, `datePublished`, `author` (Person or Organization).
- `Product` → `name`, `image`, `offers` (with `price`, `priceCurrency`). Recommended: `aggregateRating`, `review`.
- `FAQPage` → `mainEntity` array of `Question` objects, each with `acceptedAnswer`.
- `Event` → `name`, `startDate`, `location`. Recommended: `offers`, `performer`.
- `HowTo` → `name`, `step` array (each step with `name` + `text`).
- `Review` → `itemReviewed`, `reviewRating`, `author`.

Pull values from existing page content. If a required value is missing from the page, do not invent it — flag as a content gap to fix before adding schema.

### Step 3 — `@graph` composition for multi-type pages

When a page has multiple eligible schema types (e.g., article + author + organization + breadcrumb), wrap in a single `@graph` rather than emitting four separate `<script>` blocks. One `@type: ItemList` parent with referenced child entities reduces collisions and is Google's recommended pattern.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://example.com/#org", "name": "...", "url": "..." },
    { "@type": "Person", "@id": "https://example.com/#author", "name": "..." },
    { "@type": "Article", "@id": "https://example.com/post/#article", "headline": "...", "author": { "@id": "https://example.com/#author" } },
    { "@type": "BreadcrumbList", "itemListElement": [...] }
  ]
}
```

### Step 4 — Generate JSON-LD

Output the complete `<script type="application/ld+json">` block ready to paste into the page's `<head>` (preferred) or end of `<body>`. Always JSON-LD format (Google's recommended approach); never microdata or RDFa.

### Step 5 — Validate

Provide the validation checklist:

1. Paste the URL into Google's [Rich Results Test](https://search.google.com/test/rich-results) — confirm zero errors and the expected rich-result types detected.
2. Verify the markup represents *actual visible page content*. Schema-content mismatch is Google's #1 manual-action trigger.
3. Confirm Search Console "Enhancements" report picks up the new markup within 7–14 days of publish.
4. For JavaScript-injected schema, confirm via Rich Results Test (Google fetches it) — `web_fetch` and similar tools cannot detect JS-injected markup.

---

## Sharp rules + anti-patterns

- ✅ JSON-LD only. Never microdata or RDFa for new work.
- ✅ Schema reflects visible content. If it's in schema, it must be on the page.
- ✅ One `@graph` per page, not multiple `<script>` blocks.
- ✅ Required properties present per type before publish.
- ❌ Hidden content in schema only ("invisible" reviews, prices not shown on the page). Manual-action territory.
- ❌ Wishful properties (`aggregateRating` with 1 review and rating 5.0). Google may treat as spam.
- ❌ Inventing `sameAs` URLs to social profiles that don't exist. Validation catches it.
- ❌ Schema for navigational pages that don't have rich-result eligibility — wastes review effort.

---

## Page: {url or path}

### Page type assessment
- Detected: {ArticleType / Product / FAQ / etc.}
- Eligible rich results: {list}

### Required properties — fill / gap check
- ✅ {property}: {value pulled from page}
- ⚠️ {property}: {GAP — value missing from page, flag to content owner}

### Generated JSON-LD

\`\`\`html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [... ]
}
</script>
\`\`\`

### Validation checklist
- [ ] Paste URL into Rich Results Test — zero errors
- [ ] Detected rich-result types match expectations
- [ ] No schema-content mismatch (manual eyeball check)
- [ ] Search Console Enhancements report updated within 14 days
```

---

## Integration with other skills

- **Upstream:** `/aeo-content` produces the page content; this skill structures it. `/website-audit` may flag missing schema and route here.
- **Downstream:** `/aeo-strategy` consumes the citation lift; `/website-audit` re-checks via the validation step.
- **Companion:** `/aeo-content` (write the page) → `/schema-markup` (structure it) → publish.

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/schema/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/schema/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice and integrated with our existing AEO chain.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

