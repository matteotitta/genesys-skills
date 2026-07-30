---
knowledge_type: lifecycle-campaign
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Lifecycle Campaign — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Multi-channel triggered campaign — emails + in-app + SMS sequences mapped to lifecycle moments (welcome, activation, expansion, win-back). Distinct from outreach-sequence (cold/proactive list-based) — lifecycle is triggered by behavior or state.

## Required frontmatter fields

```yaml
client: {slug}
skill: lifecycle                     # renamed from lifecycle-marketing in Phase 2
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: lifecycle-campaign
campaign_name: {Campaign}
segment: {target segment}
entry_trigger: {behavior or state event}
exit_trigger: {success state or suppress event}
sender: {From name + email}
primary_cta: {what we want them to do}
utm_pattern: {utm_source/medium/campaign template}
upstream_messaging: {path}
upstream_icp: {path}
upstream_funnel: {path}
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order)

1. **Campaign header** — segment, entry/exit triggers, sender, primary CTA, UTM pattern, channel mix
2. **Sequence map** — full sequence diagram: emails / in-app / SMS in order with timing
3. **Per-message blocks** — H2 per message: timing, channel, subject (email), body, CTA, suppression rules
4. **Suppression + exit logic** — when to remove from sequence (success, opt-out, supersede)
5. **Measurement plan** — metrics per message + overall campaign (open, click, conversion)
6. **QA checklist** — pre-launch verification (links, UTMs, render, suppression test)

## Optional body sections

- **A/B test plan** — when testing variants of subject lines or CTAs
- **Personalization tokens** — dynamic fields used (firstName, plan, lastAction)
- **Deliverability notes** — when domain warmup, sender reputation, or content compliance matters

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified.

**HTML comment tags** for confidence audit (stripped at publish — copy goes to ESP):

Sections requiring (commented) tags:
- Per-message claim: every metric, customer name, comparison fact (source from upstream)
- Personalization tokens: each token's data source verified

Body copy itself should NOT carry visible tags — it's customer-facing.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Sequence map as Drive native table (rows: messages; columns: timing, channel, subject/title, summary)
- Per-message blocks: H2 with full body in code-block (paste-ready for ESP)

### gdrive (Slides) — N/A
### gdrive (Sheet) — for live tracker companion

Sheet variant: campaign tracker (rows: messages; columns: timing, channel, status, draft, review, ship date, actuals — open/click/convert).

### notion (Page render)

- Overview = campaign header summary
- H1 = "{Client} — {campaign_name}"
- Each H2 (message) = toggle block; full message body inside
- Suppression + measurement toggles default-collapsed

### Direct publish (channel-native)

Per-message body migrates to ESP (Customer.io, Iterable, HubSpot, Mailchimp). Doc remains source of truth for review; ESP is execution.

## Validation rules

1. All required frontmatter fields present
2. `entry_trigger` + `exit_trigger` non-empty
3. Sequence map: ≥2 messages (single-email isn't a campaign)
4. Per-message blocks: every message has timing, subject, body, CTA, suppression rule
5. UTM pattern follows utm_source/medium/campaign convention
6. QA checklist present + ≥5 items
7. Measurement plan: ≥1 metric per message + overall conversion goal

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
