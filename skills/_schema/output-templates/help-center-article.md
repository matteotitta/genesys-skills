---
knowledge_type: help-center-article
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion, intercom-json]
canonical_render: intercom-json
---

# Help Center Article — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Intercom-bound product KB / FAQ article. One article per (product, persona, collection, article_type) cell. Closes the activation lifecycle — the canonical link target for onboarding emails, in-product tooltips, and Intercom Fin AI agents. Distinct from `aeo-content` (SEO surface for prospects) and `lifecycle-campaign` (the email sequences that link to KB articles).

## Required frontmatter fields

```yaml
client: {slug}
skill: help-center
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: help-center-article

# Identity
product: {product slug}
persona: {persona slug — from 00-personas.md}
collection: {one of: getting-started, account-and-profile, settings-and-configuration, integrations, advanced-workflows, troubleshooting, billing-and-plans, admin-sso-user-management, surfaces, developer-api, privacy-and-compliance, whats-new}
article_type: {one of: capabilities, benefits, setup, aha-moment, habit-moment, profile-setup, organization-setup, team-management, integration-overview, integration-specific, admin-controls, permissions, billing, power-user-workflow, troubleshooting-symptom}

# Content
title: {Article title — Intercom renders as H1}
meta_description: {≤140 chars, contains JTBD verb + product noun}
jtbd: {1-sentence Job To Be Done framing}
related_articles:
  - {slug-of-sibling-article}
  - {slug-of-sibling-article}

# Lifecycle
upstream_messaging: {path to product-messaging output}
upstream_tov: {path to tov-guidelines output}
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (per article-type)

The body structure varies by `article_type`. Templates live in `.claude/skills/primitives/lifecycle/help-center/references/article-templates.md`.

**Universal requirements (all article types):**

1. **Hook paragraph** — 1-3 sentences framing the JTBD; never starts with "In this article…"
2. **Body sections** — H2 + (optional) H3 only; NO H1 (Intercom renders title as H1)
3. **Screenshot placeholders** — `{{screenshot:filename.png}}` for any UI claim that benefits from visual
4. **Related articles block** — final section, ≥2 links to sibling articles in same collection (`{{link:other-article-slug}}`)

**Per-article-type required beats** (see article-templates.md for full skeletons):

| article_type | Required beats (in order) |
|---|---|
| `capabilities` | What it does / Three things you'll do most / When to use (and not) |
| `benefits` | The problem it solves / What changes / Three biggest wins / How this maps to your day |
| `setup` | Before you start / Steps 1..N (one screenshot per step) / Confirm setup is complete / What's next |
| `aha-moment` | What you'll do / Steps 1..3 / See the result / If something looks off / Make it a habit |
| `habit-moment` | The repeating loop / How to make it stick / When you're ready for more |
| `integration-overview` | Available integrations / How they work / Pick the integration |
| `integration-specific` | What it does / Before you start / Connect / Configure / Test / Troubleshooting |
| `troubleshooting-symptom` | What's happening / Most common cause + fix / Other causes / When to contact support |
| (other types) | See article-templates.md |

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified.

Body copy is customer-facing — confidence tags go in HTML comments, stripped at export. Sections requiring tags:

- Every product capability claim → traces to `product-messaging`
- Every metric, customer name, time-to-value claim → `[VERIFIED]` or `[NOT AVAILABLE]`
- Every screenshot reference → traces to a real screenshot file in `screenshots/`

If a claim cannot be verified, omit it — do not invent.

## Render rules per target

### intercom-json (canonical)

- Run `scripts/export-intercom.py` against the per-product output directory
- Produces `intercom-import.json` at the directory root
- One JSON file contains all collections + all articles for the product
- Client CX team imports via Intercom Articles API per the `import_instructions` block in the JSON

### gdrive (Doc — review surface)

- One Google Doc per article, organized by collection in `PJ - {Client}` Drive folder
- Inter font, justified body, sentence-case headings
- Screenshot placeholders rendered as inline placeholder labels for reviewer's reference

### notion (Page render — collaboration surface)

- One Notion page per article under a `{Product} Help Center` parent page
- Collections rendered as sub-pages (parent-child hierarchy)
- Toggle blocks for "Related articles" and "Troubleshooting" sub-sections

## Validation rules

1. All required frontmatter fields present (per `_schema/validate-frontmatter.py`)
2. `collection` value is one of the canonical 12 modules
3. `article_type` value is one of the canonical 15 article types
4. `meta_description` ≤140 chars
5. `related_articles` ≥2 entries
6. Body has no H1 (Intercom renders title)
7. Body has at least one `## ` H2 section
8. Every `{{screenshot:...}}` placeholder references a real file in `screenshots/` (warned at validation, blocked at publish)
9. JTBD-confirming hook present in first paragraph (no "In this article…" preamble)
10. Per-article-type required beats present (templated check against article-templates.md)

## Examples in the wild

- Real-test run against ClientCo report-generator × financial-adviser cell (Step 9 of skill runbook)
- Phase 4 of skill rollout will produce additional conforming examples per client engagement
