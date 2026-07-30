# Output Templates — Canonical Schemas

This directory contains 33 schema files — one per ontology knowledge type — that define the contract every skill output must conform to. Phase 4 of the master skill refactor lints every skill's output against the matching schema; the unified push API (`.claude/mcp/push.mjs`) reads these schemas to apply per-target render rules.

## How to read a schema

Each `{type}.md` file has a fixed structure:

1. **YAML frontmatter** — declares the knowledge type, ontology cross-reference, render targets, and canonical render path
2. **Purpose** — 1-2 sentences on what this knowledge type captures
3. **Required frontmatter fields** — the YAML the source md must carry
4. **Required body sections** — ordered, with min content rules
5. **Optional body sections** — when to include
6. **Confidence-tag conventions** — which sections require `[VERIFIED]` etc., per `.claude/rules/exa-protocol.md` thresholds
7. **Render rules per target** — how the adapter renders for gdrive (Doc/Slides/Sheet) and Notion
8. **Validation rules** — what the lint script checks
9. **Examples in the wild** — pointer to actual conforming outputs (or "Phase 4 will produce")

## How Phase 4 uses these

Phase 4 runs parallel batches (one per knowledge type cluster). Each batch:

1. Reads the canonical schema for its types
2. Edits every skill that produces that type to match
3. Adds the schema reference to the skill's `references/output-template.md`
4. Lints existing client outputs against the schema; spot-fixes drift

## How push.mjs uses these

The unified push API reads `canonical_render` and `render_targets` to:

- Route gdrive pushes to the right doc type (Doc / Slides / Sheet) by schemaType
- Apply target-specific transformations (Notion turns H2 into toggle blocks; gdrive applies page-numbered footer)
- Validate the source md before publishing (warn-only at first; hard-fail post-Phase-4)

## Index — all 33 types grouped by tier

### Level 0 — Context (11 types, research substrate)

| Type | File | Description |
|------|------|-------------|
| company-context | [company-context.md](company-context.md) | Firmographics, funding, team, traction, qualification |
| competitor-intel | [competitor-intel.md](competitor-intel.md) | 11-dimension competitor analysis, comparison matrices |
| icp-profile | [icp-profile.md](icp-profile.md) | Synthetic personas, pain points, buying simulation |
| tone-of-voice | [tone-of-voice.md](tone-of-voice.md) | Voice patterns, vocabulary, frequency scores |
| brand-kit | [brand-kit.md](brand-kit.md) | Visual identity, design tokens, brand system file |
| funnel-strategy | [funnel-strategy.md](funnel-strategy.md) | GTM motion, stages, qualification criteria |
| win-loss-analysis | [win-loss-analysis.md](win-loss-analysis.md) | Sales call patterns, objection themes |
| content-audit | [content-audit.md](content-audit.md) | Content inventory, gap analysis |
| transcript-insights | [transcript-insights.md](transcript-insights.md) | Extracted quotes, themes, action items |
| expert-pov | [expert-pov.md](expert-pov.md) | Founder expertise, thought leadership angles |
| client-engagement | [client-engagement.md](client-engagement.md) | Discovery research, proposals, scope |

### Level 1 — Strategy (7 types, inherits context)

| Type | File | Description |
|------|------|-------------|
| positioning | [positioning.md](positioning.md) | Anchors, differentiators, positioning statements |
| messaging | [messaging.md](messaging.md) | 10-component messaging library, value props |
| content-strategy | [content-strategy.md](content-strategy.md) | Multi-year roadmap, channel mix, format priorities |
| pricing-strategy | [pricing-strategy.md](pricing-strategy.md) | Pricing model, packaging, competitive pricing |
| website-score | [website-score.md](website-score.md) | PM evaluation score (0-100) |
| lead-assessment | [lead-assessment.md](lead-assessment.md) | Fit + signals + routing recommendation per account |
| youtube-strategy | [youtube-strategy.md](youtube-strategy.md) | YouTube channel launch with keyword demand, gap analysis, video ideas |

### Level 2 — Execution (8 types, produces deliverables)

| Type | File | Description |
|------|------|-------------|
| landing-page-copy | [landing-page-copy.md](landing-page-copy.md) | Headlines, sections, CTAs |
| aeo-content | [aeo-content.md](aeo-content.md) | AI-optimized blog content |
| battlecard | [battlecard.md](battlecard.md) | Competitive battlecard content |
| launch-plan | [launch-plan.md](launch-plan.md) | Cross-functional launch orchestration |
| lifecycle-campaign | [lifecycle-campaign.md](lifecycle-campaign.md) | Multi-channel lifecycle campaigns |
| case-study | [case-study.md](case-study.md) | Customer stories with metrics |
| outreach-sequence | [outreach-sequence.md](outreach-sequence.md) | Cold/follow-up email sequences |
| sales-enablement-asset | [sales-enablement-asset.md](sales-enablement-asset.md) | Talk tracks, demo scripts, decks |

### Level 3 — Content (4 types, channel-native)

| Type | File | Description |
|------|------|-------------|
| linkedin-post | [linkedin-post.md](linkedin-post.md) | Hook + body + CTA |
| youtube-script | [youtube-script.md](youtube-script.md) | Retention-optimized scripts |
| newsletter | [newsletter.md](newsletter.md) | GTM Pulse + Genesys newsletter synthesis |
| thought-leadership | [thought-leadership.md](thought-leadership.md) | Long-form founder content |

### Meta tier (3 types, internal working docs)

| Type | File | Description |
|------|------|-------------|
| runbook | [runbook.md](runbook.md) | Step-by-step procedures, troubleshooting guides |
| experiment-log | [experiment-log.md](experiment-log.md) | Hypotheses, variants, results, learnings |
| dashboard | [dashboard.md](dashboard.md) | Data visualization app specifications |

## Editing rules

- **Don't hand-edit a schema** without a corresponding plan update. Schemas are part of the canonical contract.
- **New knowledge types** require an ontology.md update first (lines 11–105 are the source of truth).
- **Render rule changes** require a `push.mjs` minor-version bump and adapter regression test.
- **Sentence case headings**, em dashes with spaces, no emojis (per global CLAUDE.md voice).

## Cross-references

- `.claude/rules/ontology.md` — knowledge type definitions + entity schemas (canonical source)
- `.claude/rules/exa-protocol.md` — confidence-tag standards + quality thresholds per output type
- `.claude/rules/design-production.md` — DESIGN.md format + canonical render rules
- `.claude/mcp/push.mjs` — unified push API that consumes these schemas
- `.claude/mcp/push-adapters/README.md` — adapter contract reference
