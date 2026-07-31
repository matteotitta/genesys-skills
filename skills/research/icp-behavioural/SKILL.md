---
name: icp-behavioural
version: '1.1'
last_updated: 2026-03-15
author: genesys-growth
description: 'Creates synthetic buyer personas that simulate real purchase decisions, then runs those personas through website
  evaluation and messaging tests. Produces behavioural persona profiles, buying simulation results with objection patterns,
  and a prompt bank for AEO/SEO tracking. Triggers: "behavioural personas", "buyer simulation", "synthetic personas", "test
  messaging against buyers", "predictive persona", or "AEO prompt bank". Upstream: depends on icp-research and win-loss-analysis
  for grounded simulation. Downstream: feeds positioning, product-messaging, linkedin-content, landing-page-copy, and aeo-content.
  NOT for static ICP profiles (use /icp-research) or interview preparation (use /customer-interviews).'
goal: Creates synthetic buyer personas that simulate real purchase decisions, then runs those personas through website evaluation
  and messaging tests.
outcome: Creates synthetic buyer personas that simulate real purchase decisions, then runs those personas through website
  evaluation and messaging tests. Produces behavioural persona profiles, buying simulation results with objection patterns,
  and a prompt bank for AEO/SEO tracking. Triggers:...
primitive: research
ontology_type: icp-profile
review_gate: 2
inputs:
  required: []
  recommended:
  - company-context
- type: icp-behavioural
  feeds_into:
  - positioning
  - product-messaging
  - website-copy
  - aeo-content
  - outreach-emails
  - sales-enablement
  - competitor-research
depends_on: []
- aeo-content
- competitor-research
- website-copy
- outreach-emails
- positioning
- product-messaging
- sales-enablement
owned_by_agent: researcher
mcps_used:
- exa
- gdrive
- notion
triggers:
  slash_commands:
  - /icp-behavioural
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# ICP Behavioural

Build behavioral buyer personas from website data, sales calls, and review signals — then simulate their buying decisions against any URL. Produces predictive personas (how buyers behave) rather than descriptive profiles (who buyers are), plus a prompt bank for AEO/SEO tracking.

**Renamed from:** `icp-synthetic` v1.0. For structured ICP research reports, see `icp-research`.
**Knowledge type:** `icp-profile` (see `.claude/rules/ontology.md`)
**Maturity on first run:** emergent → validated after simulation or client feedback

## When to run

**Two modes** (full diagram → the premium reference):

- **Mode 1 — Build:** First run for a new company. Produces persona cards saved as artifacts. Phases 1, 2, 3, 5, 6.
- **Mode 2 — Simulate:** Independent re-runs against any URL (different page, competitor site, post-redesign). Reuses saved persona cards. Phase 4 only.

**Invoke when user says:** "ICP research for [company/URL]", "Synthetic personas for [company]", "Buyer research for [URL]", "Build personas for [company]", "Test [URL] against buyer personas", "Simulate [URL] with [company] personas" (Mode 2), "Run personas against [page]" (Mode 2).

**Do NOT invoke when:**
- Competitor research only → use `competitor-research`
- Brand/design extraction → use `brand-kit`
- Messaging without customer research → use `product-messaging`
- Direct content creation → use the relevant content skill

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Website URL** (Mode 1) | Primary company website to research | User specification |
| **Target URL + persona cards** (Mode 2) | Page to simulate + previously saved personas | User + Mode 1 output |

### Optional (improve enrichment tier — see the premium reference)

| Input | Enrichment Impact | Accepted Formats |
|-------|-------------------|------------------|
| Sales call transcripts | Tier 1→3 (biggest jump) | Raw transcript OR transcript-analysis output |
| Customer interviews | Tier 2→3 | Raw transcript OR structured notes |
| CRM notes | Tier 3→4 | Summary notes, deal notes |
| Support tickets / community posts | Tier 3→4 | Raw text, forum links |
| Existing ICP docs | Validates/expands | Any format |
| Case studies URL | Improves Tier 1 | Direct link |
| G2/review links | Improves Tier 1 | Direct links |

### Transcript format auto-detection

- **Raw transcript** (timestamps, speaker labels, conversational text) → extract quotes, objections, vocabulary, decision criteria inline.
- **Transcript-analysis output** (sections like "Key quotes", "Topic clusters") → use structured findings directly as enrichment data.

### Validation checklist

- [ ] Website URL valid and accessible
- [ ] Discoverable customer / case study content
- [ ] B2B SaaS (or similar) for framework applicability
- [ ] Transcript format detected and acknowledged (if provided)

If inputs are missing, ask for the website URL. State the enrichment tier and confidence ceiling based on what's provided. Suggest what additional inputs would lift fidelity.

## Steps

1. **Phase 1 — Input + tier assessment.** Validate URL, fetch source pages (`/customers`, `/case-studies`, `/pricing`, `/integrations`, G2, LinkedIn hiring), assess Tier 1-4, declare confidence ceiling, extract raw data, normalize attributes, process transcripts. Full procedure → the premium reference.
2. **Phase 2 — ICP foundation.** Define core use case, build firmographics + technographics, calculate TAM/SAM/SOM/ICP, define segments + negative ICP, identify intent signals. Full procedure → the premium reference.
3. **Phase 3 — Synthetic persona construction.** For each key persona (3-5 total — Champion + Economic Buyer per segment): build the 14-field card (Identity / Behavioral / Friction layers + Evidence), apply sales call enrichment, assign skepticism scores + friction attributes, map DMU for enterprise deals. Full procedure → the premium reference. Field schema → the premium reference. Bias mitigation → the premium reference.
4. **Phase 5 — Prompt bank (AEO bridge).** Generate 15-30 prompts per persona across awareness / consideration / decision intent levels using persona vocabulary; deduplicate, prioritize, map top 10 to content pieces. Full procedure → the premium reference. Templates → the premium reference.
5. **Phase 6 — Self-evaluation.** Run completeness, evidence quality, behavioral specificity checks; run self-roast questions; flag weak areas before delivery. Full procedure → the premium reference.
6. **Review gate (Level 2).** Present summary, enrichment tier, key personas, top gaps. Actions: Approve / Request changes / Run simulation now.
7. **Phase 4 — Website simulation (Mode 2).** Each persona evaluates target URL through 7 lenses (Clarity, Relevance, Proof, Objection handling, Language match, Next step clarity, Trust signals); run skeptical mode; generate per-persona conversion likelihood + ranked friction + recommendations. Full procedure → the premium reference. Scoring rubric → the premium reference.
8. **Save persona cards** to client folder as artifacts. Offer immediate Mode 2 simulation or chain forward.
9. **Assemble output** using the premium reference (Mode 1 = full template; Mode 2 = sections 4 + 5 only).

**Research substrate:** Exa per `.claude/rules/exa-protocol.md`. Primary tool: `web_search_exa` with `site:reddit.com` / `site:g2.com` filters for voice samples. Citation: `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]`. Quality gate: ≥3 sources per major claim, ≥50% verified, date filter on "recent / latest" claims. Full integration map → the premium reference.

**Search patterns** (research queries inherited + new behavioral queries) → the premium reference.

**Dimension schemas** (TAM methodology, firmographics, technographics, VOC, customer proof points, segments, sorting rules, intent signals) → the premium reference.

**Skeptical buyer simulator** (merged 2026-04-29 protocol) → the premium reference.

## What good looks like

### Evaluations

Quality gates (full checklist → the premium reference):

- [ ] All persona cards have 14 fields complete with source provenance + confidence levels
- [ ] Skepticism scores assigned per persona; vocabulary fields contain specific terms (not common words)
- [ ] Objections specific (not generic "price, competition"); ≥1 verbatim quote per persona (or marked "Not available")
- [ ] Core use case defined; firmographics normalized; TAM table includes ICP row; negative ICP documented with evidence
- [ ] 15-30 prompts per persona across all 3 intent levels using persona vocabulary; top 10 content pieces mapped with rationale
- [ ] (If Mode 2) all personas through 7 lenses; scores justified with specific page observations; skeptical mode run with concrete objections
- [ ] Source appendix has all URLs + access dates; enrichment tier accurately declared; inferred fields labeled; data gaps documented with how-to-fill suggestions
- [ ] ≥50% verified claims, ≤20% estimated per ontology

