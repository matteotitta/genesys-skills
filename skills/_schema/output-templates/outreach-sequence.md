---
knowledge_type: outreach-sequence
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Outreach Sequence — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Cold/proactive outbound multi-step cadence — emails + LinkedIn + sometimes calls. Distinct from lifecycle-campaign (triggered by behavior/state) — outreach is list-based and proactive.

## Required frontmatter fields

```yaml
client: {slug}
skill: outreach                      # renamed from outreach-emails in Phase 2
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: outreach-sequence
campaign_name: {Campaign}
target_icp: {ICP segment}
target_persona: {Persona — title + level}
list_source: {Apollo search ID / Clay table / CSV}
list_size: {n}
sender: {From name + email}
sender_domain: {domain — for warmup tracking}
total_steps: {n}                     # 4-8 typical
total_duration_days: {n}             # 14-30 typical
email_validation_passed: {bool}      # gate before launch per apollo-credits.md
upstream_messaging: {path}
upstream_icp: {path}
upstream_lead_assessment: {path}     # if list came from /lead-scoring
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

**Locking gate:** outreach-sequence cannot launch (`status: locked`) until `email_validation_passed: true` (per `apollo-credits.md` — ZeroBounce / BetterContact validation pass).

## Required body sections (in order)

1. **Campaign overview** — ICP, persona, list source, sender, primary CTA, success metric
2. **Cadence map** — step-by-step diagram: day 0, day 3, day 7, etc. with channel + intent per step
3. **Per-step blocks** — H2 per step: timing, channel, subject (if email), body, CTA, response handling
4. **Follow-up logic** — if reply / if open-no-reply / if no engagement (suppression vs continue)
5. **Personalization tokens** — fields used (firstName, company, recent funding, hire signal)
6. **Apollo credit budget** — total credits to be spent + per-account cap (per `apollo-credits.md`)
7. **Validation + warmup** — email validation pass evidence + sender domain warmup status

## Optional body sections

- **A/B test plan** — when testing subject lines or angle hooks
- **LinkedIn integration** — when sequence includes LI connect/comment/DM steps
- **Tier-specific variants** — when STRONG_FIT vs MODERATE_FIT accounts get different sequences

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Execution outputs require ≥60% verified.

**HTML comment tags** for confidence audit (stripped at publish — copy goes to outreach platform):

Sections requiring (commented) tags:
- Per-step claims (every product capability claim, customer name, metric)
- Personalization token sources (Apollo enrichment field, lead-assessment signal)

Body copy itself does NOT carry visible tags.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Cadence map as Drive native table
- Per-step blocks with body in code-block (paste-ready for outreach platform)

### gdrive (Slides) — N/A
### gdrive (Sheet) — for response tracking

Sheet variant: list tracker (rows: accounts; columns: step 1-N statuses, replies, meetings booked, status).

### notion (Page render)

- Overview = campaign overview
- H1 = "{Client} — {campaign_name}"
- Each H2 (step) = toggle block

### Direct publish (channel-native)

Body migrates to outreach platform (Smartlead, Lemlist, Instantly, Apollo Sequences, HeyReach). Doc remains source of truth.

## Validation rules

1. All required frontmatter fields present
2. `email_validation_passed: true` required before locking
3. `total_steps` is 4-8 (sweet spot)
4. Per-step blocks: every step has timing, body, CTA, response logic
5. Personalization tokens: every token has a verified data source
6. Apollo credit budget: total ≤ approved budget per `apollo-credits.md`
7. Sender domain warmup status documented

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
