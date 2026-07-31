---
name: skill-catalog
version: '2.0'
last_updated: 2026-02-13
author: genesys-growth
description: 'Maintains the central registry of all skills with dependencies, trigger phrases, review gates, and chaining
  metadata. Produces skill-metadata records consumed by the orchestrator for routing decisions and dependency resolution.
  Triggers: "skill catalog", "list skills", "what skills exist", "skill dependencies", "check triggers". Upstream: none (root
  reference). Downstream: orchestrator, skill-reviewer. NOT for executing skills — use the orchestrator instead.'
goal: Maintains the central registry of all skills with dependencies, trigger phrases, review gates, and chaining metadata.
outcome: 'Maintains the central registry of all skills with dependencies, trigger phrases, review gates, and chaining metadata.
  Produces skill-metadata records consumed by the orchestrator for routing decisions and dependency resolution. Triggers:
  "skill catalog", "list skills", "what skills exist",...'
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended: []
- type: skill-metadata
  feeds_into:
  - orchestrator
depends_on: []
- orchestrator
owned_by_agent: operator
mcps_used: []
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
effort: low
paths:.claude/skills/**
disable-model-invocation: true
slim_exemption: auto-generated-catalog-body
---

# Skill Catalog

Central registry of all Claude skills. The body of this file is **auto-generated** from each SKILL.md frontmatter by `scripts/regenerate-catalog.py`, run on every commit via the pre-commit hook. The 107-row table + edge index that follows is the skill's actual deliverable, not bloat — hence the `slim_exemption`.

To use this catalog, scan the table by primitive (research, content, social, etc.) for the skill you need. Each row shows ontology type, review gate, owning agent, and edge counts. The edge index at the end lists every dependency relationship in flat form for quick grep.

## Claude Code Triggers

**Invoke when:**
- "What skills do I have?" / "Show me the skill catalog"
- "What skill should I use for [task]?"
- "What does [skill] need as input?" / "What can I do after [skill]?"
- "Show skill dependencies" / "Skill registry"

**Do NOT invoke when:**
- User wants to run a specific skill → Run that skill directly
- User wants to create a new skill → Use `prompt-design` or `workflow-design`

## How to update the catalog

Don't hand-edit between the BEGIN/END markers. Edit individual `SKILL.md` frontmatter — the pre-commit hook regenerates this section automatically. To regenerate manually:

```bash
bash.claude/skills/meta/catalog/skill-catalog/scripts/regenerate-catalog.sh
```

To validate chains without regenerating:

```bash
bash.claude/skills/meta/catalog/skill-catalog/scripts/chain-lint.sh --validate-ontology
```

For a one-glance catalog state + health check (totals by primitive / status / owner, graph health, recency) — read-only, built on chain-lint:

```bash
bash.claude/skills/meta/catalog/skill-catalog/scripts/catalog-query.sh # human summary
bash.claude/skills/meta/catalog/skill-catalog/scripts/catalog-query.sh --json # machine-readable
```

---

<!-- BEGIN AUTO-CATALOG -->

## Skill catalog (auto-generated)

**167 active skills.** Last commit touching `.claude/skills/`: `2026-07-27T15:47:14+01:00`

> AUTO-GENERATED — do not hand-edit between the BEGIN/END markers. Edit individual `SKILL.md` frontmatter; the pre-commit hook regenerates this section. To regenerate manually: `bash.claude/skills/meta/catalog/skill-catalog/scripts/regenerate-catalog.sh`.

Skills under `meta/` are graph-exempt by design (utilities, indexes, session helpers, learning loops). They have no `depends_on`/`feeds_into` edges and chain-lint exempts them.

### research (14)

#### (no sub-primitive)

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `brand-kit` | brand-kit | 2 | researcher | 0 | 13 | `.claude/skills/research/brand-kit/SKILL.md` |
| `company-context` | company-context | 1 | researcher | 0 | 3 | `.claude/skills/research/company-context/SKILL.md` |
| `competitor-research` | competitor-intel | 1 | researcher | 0 | 3 | `.claude/skills/research/competitor-research/SKILL.md` |
| `customer-interviews` | transcript-insights | 1 | researcher | 0 | 4 | `.claude/skills/research/customer-interviews/SKILL.md` |
| `expert-pov` | expert-pov | 2 | researcher | 0 | 5 | `.claude/skills/research/expert-pov/SKILL.md` |
| `funnel-strategy` | funnel-strategy | 2 | researcher | 0 | 4 | `.claude/skills/research/funnel-strategy/SKILL.md` |
| `icp-behavioural` | icp-profile | 2 | researcher | 0 | 7 | `.claude/skills/research/icp-behavioural/SKILL.md` |
| `icp-research` | icp-profile | 1 | researcher | 0 | 7 | `.claude/skills/research/icp-research/SKILL.md` |
| `marketing-team-tracker` | temporal-signal-brief | 1 | researcher | 0 | 5 | `.claude/skills/research/marketing-team-tracker/SKILL.md` |
| `read-book` | source-notes | 1 | researcher | 0 | 2 | `.claude/skills/research/read-book/SKILL.md` |
| `signal-scan` | temporal-signal-brief | 1 | researcher | 0 | 4 | `.claude/skills/research/signal-scan/SKILL.md` |
| `tov-guidelines` | tone-of-voice | 2 | researcher | 0 | 5 | `.claude/skills/research/tov-guidelines/SKILL.md` |
| `watch-video` | transcript-insights | 1 | researcher | 0 | 2 | `.claude/skills/research/watch-video/SKILL.md` |
| `win-loss-analysis` | win-loss-analysis | 1 | researcher | 0 | 4 | `.claude/skills/research/win-loss/SKILL.md` |

### clients (7)

#### (no sub-primitive)

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `client-discovery` | client-engagement | 2 | b2b-consultant | 0 | 2 | `.claude/skills/primitives/clients/discovery/SKILL.md` |
| `client-onboarding` | client-engagement | 2 | b2b-consultant | 2 | 0 | `.claude/skills/primitives/clients/client-onboarding/SKILL.md` |
| `client-proposals` | client-engagement | 4 | b2b-consultant | 1 | 5 | `.claude/skills/primitives/clients/proposal/SKILL.md` |
| `consultation` | client-engagement | 2 | b2b-consultant | 0 | 1 | `.claude/skills/primitives/clients/consultation/SKILL.md` |
| `contract-redline` | client-engagement | 3 | b2b-consultant | 0 | 1 | `.claude/skills/primitives/clients/contract-redline/SKILL.md` |
| `sales-call-playbook` | sales-enablement-asset | 2 | operator | 2 | 0 | `.claude/skills/primitives/clients/sales-call-playbook/SKILL.md` |
| `team-hiring` | client-engagement | 3 | b2b-consultant | 0 | 0 | `.claude/skills/primitives/clients/team-hiring/SKILL.md` |

### content (11)

#### audit

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `content-audit` | content-audit | 2 | operator | 0 | 1 | `.claude/skills/primitives/content/audit/content-audit/SKILL.md` |

#### execution

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `gtme-podcast` | content-strategy | 2 | operator | 0 | 0 | `.claude/skills/primitives/content/execution/gtme-podcast/SKILL.md` |
| `technical-paper-writer` | technical-paper | 3 | content | 1 | 0 | `.claude/skills/primitives/content/execution/technical-paper-writer/SKILL.md` |
| `thought-leadership` | thought-leadership | 2 | content | 2 | 1 | `.claude/skills/primitives/content/execution/thought-leadership/SKILL.md` |

#### motion

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `onboarding-video` | video-composition | 3 | content | 3 | 3 | `.claude/skills/primitives/content/onboarding-video/SKILL.md` |
| `product-ui-frames` | video-composition | 3 | content | 1 | 4 | `.claude/skills/primitives/content/product-ui-frames/SKILL.md` |
| `video-pipeline` | video-composition | 3 | content | 1 | 0 | `.claude/skills/primitives/content/motion/video-pipeline/SKILL.md` |

#### strategy

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `co-marketing` | content-strategy | 2 | growth | 0 | 2 | `.claude/skills/primitives/content/strategy/co-marketing/SKILL.md` |
| `content-operations` | content-strategy | 2 | operator | 1 | 0 | `.claude/skills/primitives/content/strategy/content-ops/SKILL.md` |
| `content-strategy` | content-strategy | 2 | pmm | 1 | 4 | `.claude/skills/primitives/content/strategy/content-strategy/SKILL.md` |
| `marketing-ideas` | content-strategy | 1 | content | 0 | 4 | `.claude/skills/primitives/content/strategy/marketing-ideas/SKILL.md` |

### design (5)

#### (no sub-primitive)

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `dashboard` | dashboard | 2 | operator | 0 | 0 | `.claude/skills/primitives/design/dashboard/SKILL.md` |
| `figma-to-prototype` | landing-page-copy | 2 | operator | 2 | 0 | `.claude/skills/primitives/design/figma-prototype/SKILL.md` |
| `genesys-design` | brand-kit | 2 | growth | 0 | 9 | `.claude/skills/primitives/design/genesys-design/SKILL.md` |
| `pptx` | sales-enablement-asset | 2 | growth | 0 | 0 | `.claude/skills/primitives/design/pptx/SKILL.md` |
| `vibe-coding` | landing-page-copy | 2 | content | 2 | 0 | `.claude/skills/primitives/design/vibe-coding/SKILL.md` |

### lifecycle (4)

#### (no sub-primitive)

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `email-nurture` | lifecycle-campaign | 2 | growth | 1 | 0 | `.claude/skills/primitives/lifecycle/email-nurture/SKILL.md` |
| `help-center` | help-center-article | 3 | growth | 1 | 2 | `.claude/skills/primitives/lifecycle/help-center/SKILL.md` |
| `lifecycle-marketing` | lifecycle-campaign | 2 | growth | 2 | 1 | `.claude/skills/primitives/lifecycle/lifecycle/SKILL.md` |
| `referral-program` | lifecycle-campaign | 2 | growth | 0 | 1 | `.claude/skills/primitives/lifecycle/referral-program/SKILL.md` |

### outbound (16)

#### email-copywriting

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `outreach-emails` | outreach-sequence | 2 | b2b-consultant | 2 | 0 | `.claude/skills/primitives/outbound/execution/email-copywriting/outreach/SKILL.md` |

#### enrichment

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `deepline-enrich` | company-context | 1 | researcher | 0 | 4 | `.claude/skills/primitives/outbound/execution/enrichment/deepline-enrich/SKILL.md` |

#### execution

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `apollo-sequences` | outreach-sequence | 1 | operator | 1 | 1 | `.claude/skills/primitives/outbound/execution/apollo-sequences/SKILL.md` |
| `directory-submissions` | launch-plan | 2 | growth | 0 | 1 | `.claude/skills/primitives/outbound/execution/directory-submissions/SKILL.md` |
| `linkedin-engagement-prospects` | outreach-sequence | 1 | content | 0 | 4 | `.claude/skills/primitives/outbound/execution/linkedin-engagement/SKILL.md` |
| `linkedin-prospecting-loop` | outreach-sequence | 3 | growth | 1 | 0 | `.claude/skills/primitives/outbound/execution/linkedin-prospecting-loop/SKILL.md` |
| `outbound-send-orchestrator` | outreach-sequence | 2 | operator | 1 | 0 | `.claude/skills/primitives/outbound/execution/outbound-send-orchestrator/SKILL.md` |

#### list-building

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `apollo-find-companies` | lead-assessment | 1 | operator | 0 | 2 | `.claude/skills/primitives/outbound/research/list-building/apollo-find/SKILL.md` |
| `clay-search` | lead-assessment | 1 | sales | 0 | 2 | `.claude/skills/primitives/outbound/research/list-building/clay-search/SKILL.md` |
| `jobs-signal` | lead-assessment | 1 | researcher | 0 | 3 | `.claude/skills/primitives/outbound/research/list-building/jobs-signal/SKILL.md` |
| `niche-signal-discovery` | lead-assessment | 1 | operator | 0 | 5 | `.claude/skills/primitives/outbound/research/list-building/niche-signal/SKILL.md` |
| `technographics-from-website` | lead-assessment | 2 | operator | 0 | 4 | `.claude/skills/primitives/outbound/research/list-building/technographics-from-website/SKILL.md` |

#### research

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `list-quality` | list-grade | 1 | operator | 0 | 3 | `.claude/skills/primitives/outbound/research/list-building/list-quality/SKILL.md` |

#### strategy

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `abm-campaign` | launch-plan | 2 | sales | 2 | 1 | `.claude/skills/primitives/outbound/strategy/abm/SKILL.md` |
| `lead-scoring` | lead-assessment | 1 | operator | 0 | 4 | `.claude/skills/primitives/outbound/strategy/lead-scoring/SKILL.md` |
| `reply-scoring` | reply-classification | 1 | operator | 0 | 2 | `.claude/skills/primitives/outbound/strategy/reply-scoring/SKILL.md` |

### paid-marketing (10)

#### audit

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `paid-ads-audit` | content-audit | 1 | paid | 0 | 3 | `.claude/skills/primitives/paid-marketing/audit/paid-audit/SKILL.md` |

#### execution

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `ad-creative` | ad-creative-asset | 3 | paid | 0 | 0 | `.claude/skills/primitives/paid-marketing/execution/ad-creative/SKILL.md` |
| `ad-creative-brief` | ad-creative-brief | 2 | paid | 2 | 1 | `.claude/skills/primitives/paid-marketing/execution/ad-creative-brief/SKILL.md` |
| `google-ads-copy` | landing-page-copy | 2 | paid | 1 | 1 | `.claude/skills/primitives/paid-marketing/execution/google-ads-copy/SKILL.md` |
| `google-ads-weekly` | experiment-log | 2 | paid | 0 | 2 | `.claude/skills/primitives/paid-marketing/execution/google-ads-weekly/SKILL.md` |
| `linkedin-ads-copy` | linkedin-post | 2 | content | 1 | 1 | `.claude/skills/primitives/paid-marketing/execution/linkedin-ads-copy/SKILL.md` |
| `paid-ads-experiment-log` | experiment-log | 1 | paid | 0 | 2 | `.claude/skills/primitives/paid-marketing/execution/paid-ads-experiment-log/SKILL.md` |
| `paid-ads-report` | dashboard | 2 | paid | 0 | 1 | `.claude/skills/primitives/paid-marketing/execution/paid-ads-report/SKILL.md` |

#### strategy

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `linkedin-ad-teardown` | competitor-intel | 1 | paid | 0 | 3 | `.claude/skills/primitives/paid-marketing/strategy/linkedin-ad-teardown/SKILL.md` |
| `paid-campaign-strategy` | launch-plan | 2 | paid | 2 | 3 | `.claude/skills/primitives/paid-marketing/strategy/paid-strategy/SKILL.md` |

### product-marketing (12)

#### execution

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `case-study` | case-study | 2 | growth | 2 | 0 | `.claude/skills/primitives/product-marketing/execution/case-study/SKILL.md` |
| `event-pipeline` | launch-plan | 2 | growth | 2 | 3 | `.claude/skills/primitives/product-marketing/execution/event-pipeline/SKILL.md` |
| `onboarding-video-script` | onboarding-video-script | 2 | pmm | 2 | 0 | `.claude/skills/primitives/product-marketing/execution/onboarding-video-script/SKILL.md` |
| `storytelling` | thought-leadership | 2 | growth | 1 | 1 | `.claude/skills/primitives/product-marketing/execution/storytelling/SKILL.md` |
| `webinar-brief` | launch-plan | 2 | growth | 2 | 0 | `.claude/skills/primitives/product-marketing/execution/webinar/SKILL.md` |

#### strategy

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `domain` | domain-shortlist | 1 | pmm | 0 | 0 | `.claude/skills/primitives/product-marketing/strategy/domain/SKILL.md` |
| `positioning` | positioning | 2 | pmm | 0 | 3 | `.claude/skills/primitives/product-marketing/strategy/positioning/SKILL.md` |
| `pricing-research` | pricing-strategy | 2 | pmm | 0 | 1 | `.claude/skills/primitives/product-marketing/strategy/pricing-research/SKILL.md` |
| `pricing-strategy` | pricing-strategy | 2 | pmm | 0 | 3 | `.claude/skills/primitives/product-marketing/strategy/pricing-strategy/SKILL.md` |
| `product-launch` | launch-plan | 2 | growth | 2 | 6 | `.claude/skills/primitives/product-marketing/strategy/product-launch/SKILL.md` |
| `product-messaging` | messaging | 2 | pmm | 0 | 5 | `.claude/skills/primitives/product-marketing/strategy/messaging/SKILL.md` |
| `vertical-messaging` | segment-messaging-map | 2 | pmm | 1 | 5 | `.claude/skills/primitives/product-marketing/strategy/vertical-messaging/SKILL.md` |

### sales-enablement (9)

#### (no sub-primitive)

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `battlecards` | battlecard | 2 | sales | 0 | 3 | `.claude/skills/primitives/sales-enablement/battlecards/SKILL.md` |
| `call-coaching` | call-coaching-report | 2 | sales | 0 | 1 | `.claude/skills/primitives/sales-enablement/call-coaching/SKILL.md` |
| `demo-script` | sales-enablement-asset | 2 | sales | 2 | 0 | `.claude/skills/primitives/sales-enablement/demo-script/SKILL.md` |
| `one-pager` | sales-enablement-asset | 2 | content | 0 | 2 | `.claude/skills/primitives/sales-enablement/one-pager/SKILL.md` |
| `revops` | content-audit | 2 | sales | 0 | 2 | `.claude/skills/primitives/sales-enablement/revops/SKILL.md` |
| `revops-incident-response` | revops-incident-report | 3 | sales | 0 | 3 | `.claude/skills/primitives/sales-enablement/revops-incident-response/SKILL.md` |
| `sales-deck` | sales-enablement-asset | 2 | sales | 0 | 3 | `.claude/skills/primitives/sales-enablement/sales-deck/SKILL.md` |
| `sales-enablement` | sales-enablement-asset | 2 | sales | 0 | 2 | `.claude/skills/meta/orchestration/sales-enablement-index/SKILL.md` |

#### execution

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `sales-tracks` | sales-enablement-asset | 3 | sales | 0 | 4 | `.claude/skills/primitives/sales-enablement/sales-tracks/SKILL.md` |

### seo-aeo (6)

#### audit

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `local-seo-audit` | content-audit | 1 | operator | 0 | 3 | `.claude/skills/primitives/seo-aeo/audit/local-seo/SKILL.md` |

#### execution

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `aeo-content` | aeo-content | 3 | content | 0 | 1 | `.claude/skills/primitives/seo-aeo/execution/aeo-content/SKILL.md` |
| `gbp-review-strategy` | content-audit | 1 | operator | 0 | 1 | `.claude/skills/primitives/seo-aeo/execution/gbp-suite/SKILL.md` |
| `programmatic-seo` | aeo-content | 2 | operator | 0 | 2 | `.claude/skills/primitives/seo-aeo/execution/programmatic-seo/SKILL.md` |
| `schema-markup` | aeo-content | 2 | content | 0 | 1 | `.claude/skills/primitives/seo-aeo/execution/schema-markup/SKILL.md` |

#### strategy

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `aeo-strategy` | content-strategy | 2 | operator | 0 | 1 | `.claude/skills/primitives/seo-aeo/strategy/aeo-strategy/SKILL.md` |

### social (21)

#### (no sub-primitive)

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `extrovert-sync` | runbook | 0 | operator | 0 | 0 | `.claude/skills/primitives/social/extrovert-sync/SKILL.md` |
| `hype-man` | thought-leadership | 3 | content | 0 | 3 | `.claude/skills/primitives/social/hype-man/SKILL.md` |

#### linkedin

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `linkedin-algo-audit` | content-audit | 0 | content | 0 | 1 | `.claude/skills/primitives/social/linkedin/linkedin-algo-audit/SKILL.md` |
| `linkedin-carousels` | linkedin-post | 3 | content | 1 | 2 | `.claude/skills/primitives/social/linkedin/linkedin-carousels/SKILL.md` |
| `linkedin-comment` | linkedin-post | 2 | content | 1 | 0 | `.claude/skills/primitives/social/linkedin/linkedin-comment/SKILL.md` |
| `linkedin-content-audit` | content-audit | 1 | content | 0 | 3 | `.claude/skills/primitives/social/linkedin/linkedin-content-audit/SKILL.md` |
| `linkedin-content-guide` | linkedin-post | 2 | content | 0 | 4 | `.claude/skills/primitives/social/linkedin/linkedin-content-guide/SKILL.md` |
| `linkedin-content-guide-founders` | linkedin-post | 3 | content | 1 | 0 | `.claude/skills/primitives/social/linkedin/linkedin-content-guide-founders/SKILL.md` |
| `linkedin-expert-posts` | linkedin-post | 2 | content | 0 | 1 | `.claude/skills/primitives/social/linkedin/linkedin-expert-posts/SKILL.md` |
| `linkedin-hooks` | linkedin-post | 2 | content | 0 | 1 | `.claude/skills/primitives/social/linkedin/linkedin-hooks/SKILL.md` |
| `linkedin-infographics` | linkedin-post | 3 | content | 1 | 1 | `.claude/skills/primitives/social/linkedin/linkedin-infographics/SKILL.md` |
| `linkedin-personal-posts` | linkedin-post | 3 | content | 0 | 1 | `.claude/skills/primitives/social/linkedin/linkedin-personal-posts/SKILL.md` |
| `linkedin-profile-optimization` | linkedin-post | 3 | content | 0 | 2 | `.claude/skills/primitives/social/linkedin/linkedin-profile/SKILL.md` |
| `linkedin-sales-posts` | linkedin-post | 3 | content | 1 | 1 | `.claude/skills/primitives/social/linkedin/linkedin-sales-posts/SKILL.md` |
| `linkedin-social-selling` | outreach-sequence | 2 | content | 1 | 0 | `.claude/skills/primitives/outbound/execution/social-selling/SKILL.md` |
| `linkedin-weekly-content` | linkedin-post | 2 | content | 1 | 1 | `.claude/skills/primitives/social/linkedin/linkedin-weekly-content/SKILL.md` |

#### newsletter

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `gtme-pulse` | newsletter | 2 | operator | 0 | 0 | `.claude/skills/primitives/social/newsletter/gtme-pulse/SKILL.md` |
| `skill-of-the-week` | newsletter | 2 | operator | 0 | 2 | `.claude/skills/primitives/social/newsletter/genesys-newsletter/SKILL.md` |

#### youtube

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `transcript-analysis` | transcript-insights | 2 | researcher | 0 | 2 | `.claude/skills/primitives/social/youtube/transcripts/SKILL.md` |
| `youtube-scripts` | youtube-script | 2 | content | 1 | 0 | `.claude/skills/primitives/social/youtube/youtube-scripts/SKILL.md` |
| `youtube-strategy` | youtube-strategy | 2 | content | 1 | 1 | `.claude/skills/primitives/social/youtube/youtube-strategy/SKILL.md` |

### website (12)

#### audit

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `metadata-lint` | content-audit | 1 | operator | 0 | 2 | `.claude/skills/primitives/website/audit/metadata-lint/SKILL.md` |
| `signup-onboarding-audit` | content-audit | 2 | growth | 0 | 2 | `.claude/skills/primitives/website/audit/signup-onboarding-audit/SKILL.md` |
| `website-pm-score` | website-score | 2 | operator | 0 | 2 | `.claude/skills/primitives/website/audit/website-score/SKILL.md` |

#### execution

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `ab-testing` | experiment-log | 2 | growth | 1 | 1 | `.claude/skills/primitives/website/execution/ab-testing/SKILL.md` |
| `in-app-popups` | landing-page-copy | 2 | growth | 0 | 1 | `.claude/skills/primitives/website/execution/in-app-popups/SKILL.md` |
| `landing-page-wireframe` | landing-page-copy | 2 | growth | 1 | 1 | `.claude/skills/primitives/website/execution/website-wireframe/SKILL.md` |
| `site-export-to-react` | landing-page-copy | 3 | operator | 0 | 1 | `.claude/skills/primitives/website/execution/site-export-to-react/SKILL.md` |
| `website-build` | landing-page-copy | 3 | operator | 2 | 2 | `.claude/skills/primitives/website/execution/website-build/SKILL.md` |
| `website-clone` | landing-page-copy | 3 | operator | 0 | 1 | `.claude/skills/primitives/website/execution/website-clone/SKILL.md` |
| `website-copy` | landing-page-copy | 3 | operator | 2 | 2 | `.claude/skills/primitives/website/execution/website-copy/SKILL.md` |

#### strategy

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `analytics-tracking-plan` | content-strategy | 2 | growth | 0 | 5 | `.claude/skills/primitives/website/strategy/analytics-tracking-plan/SKILL.md` |
| `site-architecture` | content-strategy | 2 | growth | 0 | 2 | `.claude/skills/primitives/website/strategy/site-architecture/SKILL.md` |

### meta (36)

#### catalog

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `brand-context-sync` | runbook | 1 | operator | 0 | 7 | `.claude/skills/meta/catalog/brand-context/SKILL.md` |
| `design-incident-response` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/catalog/design-incident-response/SKILL.md` |
| `design-reviewer` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/catalog/design-reviewer/SKILL.md` |
| `eval-harness` | runbook | 1 | operator | 0 | 3 | `.claude/skills/meta/catalog/eval-harness/SKILL.md` |
| `product-lens-reviewer` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/catalog/product-lens-reviewer/SKILL.md` |
| `scope-guardian-reviewer` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/catalog/scope-guardian-reviewer/SKILL.md` |
| `skill-catalog` | runbook | 0 | operator | 0 | 1 | `.claude/skills/meta/catalog/skill-catalog/SKILL.md` |
| `skill-reviewer` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/catalog/skill-reviewer/SKILL.md` |
| `voice-reviewer` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/catalog/voice-reviewer/SKILL.md` |

#### infra

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `connect-mcp` | runbook | 1 | operator | 0 | 0 | `.claude/skills/meta/infra/connect-mcp/SKILL.md` |
| `gdrive-create` | runbook | 1 | operator | 0 | 0 | `.claude/skills/meta/infra/create-gdrive/SKILL.md` |
| `mermaid-diagrams` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/infra/mermaid-diagrams/SKILL.md` |
| `plugin-scaffold` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/infra/plugin-scaffold/SKILL.md` |
| `web-task-agent` | runbook | 2 | operator | 0 | 1 | `.claude/skills/meta/infra/web-task-agent/SKILL.md` |

#### learning

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `discover` | runbook | 0 | operator | 0 | 1 | `.claude/skills/meta/learning/discover/SKILL.md` |
| `experiment` | experiment-log | 0 | operator | 0 | 0 | `.claude/skills/meta/learning/experiment/SKILL.md` |
| `learn` | runbook | 1 | operator | 0 | 5 | `.claude/skills/meta/learning/learn/SKILL.md` |
| `level` | runbook | 0 | operator | 0 | 1 | `.claude/skills/meta/learning/level/SKILL.md` |
| `opportunity-scan` | runbook | 0 | operator | 0 | 2 | `.claude/skills/meta/learning/opportunity-scan/SKILL.md` |
| `quickstart-onboarding` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/learning/quickstart-onboarding/SKILL.md` |
| `runbook` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/learning/runbook/SKILL.md` |
| `steal` | runbook | 2 | operator | 0 | 1 | `.claude/skills/meta/learning/steal/SKILL.md` |
| `wiki` | runbook | 1 | operator | 0 | 2 | `.claude/skills/meta/learning/wiki/SKILL.md` |

#### orchestration

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `batch-run` | runbook | 0 | operator | 1 | 1 | `.claude/skills/meta/orchestration/batch-run/SKILL.md` |
| `context-setup` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/orchestration/context-setup/SKILL.md` |
| `orchestrator` | runbook | 0 | operator | 1 | 0 | `.claude/skills/meta/orchestration/orchestrator/SKILL.md` |
| `premortem` | runbook | 1 | operator | 0 | 0 | `.claude/skills/meta/orchestration/premortem/SKILL.md` |
| `prompt-design` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/orchestration/prompt-design/SKILL.md` |
| `workflow-design` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/orchestration/workflow-design/SKILL.md` |

#### session

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `recall` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/session/recall/SKILL.md` |
| `session-wrap` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/session/session-wrap/SKILL.md` |
| `think` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/session/think/SKILL.md` |
| `today` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/session/today/SKILL.md` |
| `weekly-plan` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/session/weekly-plan/SKILL.md` |
| `why-slow` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/session/why-slow/SKILL.md` |
| `workspace-cleanup` | runbook | 0 | operator | 0 | 0 | `.claude/skills/meta/session/workspace-cleanup/SKILL.md` |

### ops (1)

#### execution

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `company-cfo` | financial-report | 3 | operator | 0 | 0 | `.claude/skills/primitives/ops/company-cfo/SKILL.md` |

### product-management (4)

#### audit

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `product-pulse` | product-pulse | 1 | product-manager | 1 | 2 | `.claude/skills/primitives/product-management/audit/product-pulse/SKILL.md` |

#### strategy

| name | ontology_type | gate | agent | deps | feeds | path |
|------|---------------|------|-------|------|-------|------|
| `business-brainstorm` | idea-validation | 2 | product-manager | 0 | 1 | `.claude/skills/primitives/product-management/strategy/business-brainstorm/SKILL.md` |
| `ship-learnings` | ship-learnings | 1 | product-manager | 1 | 1 | `.claude/skills/primitives/product-management/strategy/ship-learnings/SKILL.md` |
| `strategy-doc` | product-strategy | 3 | product-manager | 0 | 2 | `.claude/skills/primitives/product-management/strategy/strategy-doc/SKILL.md` |

---

## Edge index

Flat list of every `depends_on` → consumer edge across all active skills. Useful for quick grep.

| consumer | depends on |
|----------|------------|
| `ab-testing` | `analytics-tracking-plan` |
| `abm-campaign` | `company-context`, `lead-scoring` |
| `ad-creative-brief` | `paid-campaign-strategy`, `product-messaging` |
| `apollo-sequences` | `lead-scoring` |
| `batch-run` | `skill-catalog` |
| `case-study` | `product-messaging`, `win-loss-analysis` |
| `client-onboarding` | `client-discovery`, `client-proposals` |
| `client-proposals` | `client-discovery` |
| `content-operations` | `content-strategy` |
| `content-strategy` | `product-messaging` |
| `demo-script` | `battlecards`, `product-messaging` |
| `email-nurture` | `lifecycle-marketing` |
| `event-pipeline` | `icp-research`, `product-messaging` |
| `figma-to-prototype` | `brand-kit`, `landing-page-wireframe` |
| `google-ads-copy` | `paid-campaign-strategy` |
| `help-center` | `product-messaging` |
| `landing-page-wireframe` | `product-messaging` |
| `lifecycle-marketing` | `icp-behavioural`, `product-messaging` |
| `linkedin-ads-copy` | `paid-campaign-strategy` |
| `linkedin-carousels` | `genesys-design` |
| `linkedin-comment` | `linkedin-content-guide` |
| `linkedin-content-guide-founders` | `linkedin-content-guide` |
| `linkedin-infographics` | `genesys-design` |
| `linkedin-prospecting-loop` | `icp-research` |
| `linkedin-sales-posts` | `linkedin-content-guide` |
| `linkedin-social-selling` | `linkedin-content-guide` |
| `linkedin-weekly-content` | `linkedin-content-guide` |
| `onboarding-video` | `brand-kit`, `positioning`, `product-messaging` |
| `onboarding-video-script` | `positioning`, `transcript-analysis` |
| `orchestrator` | `skill-catalog` |
| `outbound-send-orchestrator` | `outreach-emails` |
| `outreach-emails` | `lead-scoring`, `niche-signal-discovery` |
| `paid-campaign-strategy` | `icp-behavioural`, `product-messaging` |
| `product-launch` | `positioning`, `product-messaging` |
| `product-pulse` | `strategy-doc` |
| `product-ui-frames` | `brand-kit` |
| `sales-call-playbook` | `battlecards`, `product-messaging` |
| `ship-learnings` | `strategy-doc` |
| `storytelling` | `expert-pov` |
| `technical-paper-writer` | `expert-pov` |
| `thought-leadership` | `content-strategy`, `expert-pov` |
| `vertical-messaging` | `product-messaging` |
| `vibe-coding` | `brand-kit`, `product-messaging` |
| `video-pipeline` | `brand-kit` |
| `webinar-brief` | `expert-pov`, `product-messaging` |
| `website-build` | `positioning`, `product-messaging` |
| `website-copy` | `product-messaging`, `tov-guidelines` |
| `youtube-scripts` | `youtube-strategy` |
| `youtube-strategy` | `positioning` |

<!-- END AUTO-CATALOG -->
