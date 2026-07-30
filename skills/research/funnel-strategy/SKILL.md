---
name: funnel-strategy
version: '1.0'
last_updated: 2026-02-13
author: genesys-growth
description: 'Maps a company''s GTM motion (PLG, SLG, or Hybrid) to concrete funnel stages with inputs, outputs, and qualification
  criteria per stage. Detects motion type from website analysis and Exa research, then produces pre-close and post-close stage
  definitions, FETE mapping, and closed-lost re-entry paths. Triggers: "funnel strategy", "funnel stages", "pipeline stages",
  "sales process", "lead qualification", "GTM motion mapping", or defining how leads flow through the business. Upstream:
  recommended company-context, icp-behavioural. Downstream: feeds lead-scoring, lifecycle-marketing, content-strategy, outreach-emails,
  and landing-page-copy. NOT for lead scoring logic (use /lead-scoring) or lifecycle email campaigns (use /lifecycle-marketing).'
goal: Maps a company's GTM motion (PLG, SLG, or Hybrid) to concrete funnel stages with inputs, outputs, and qualification
  criteria per stage.
outcome: Maps a company's GTM motion (PLG, SLG, or Hybrid) to concrete funnel stages with inputs, outputs, and qualification
  criteria per stage. Detects motion type from website analysis and Exa research, then produces pre-close and post-close stage
  definitions, FETE mapping, and closed-lost re-entry...
primitive: research
ontology_type: funnel-strategy
review_gate: 2
inputs:
  required: []
  recommended:
  - company-context
  - icp-behavioural
outputs:
- type: funnel-strategy
  feeds_into:
  - content-strategy
  - outreach-emails
  - sales-enablement
  - website-copy
depends_on: []
feeds_into:
- content-strategy
- website-copy
- outreach-emails
- sales-enablement
owned_by_agent: researcher
mcps_used:
- exa
push_targets:
- gdrive
triggers:
  slash_commands:
  - /funnel-strategy
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Funnel strategy

Infer and structure the complete sales funnel for a B2B SaaS company based on their GTM motion (PLG, SLG, or hybrid). Produces high-level stage definitions with strategy, leading-indicator inputs, and lagging-indicator outputs for each stage — including post-close stages (retention, expansion, churn prevention). A funnel is not a template you paste; it's an inference from how a company actually acquires, qualifies, and closes customers. This skill reads the company's GTM signals and produces a structured funnel model that other skills consume. Adopt the senior B2B SaaS GTM strategist persona detailed in `references/process-flowchart.md` (agent persona section).

## When to run

**Invoke when user says:** "Define the funnel for [company]" · "Sales funnel stages for [company]" · "Pipeline stages for [company]" · "Lead qualification criteria for [company]" · "GTM motion for [company]" · "Funnel strategy for [company]" · "How does [company] acquire customers?" · "What funnel stages should we use?" · "PLG vs SLG for [company]" · "Map the sales process for [company]".

**Do NOT invoke when:**
- User wants post-signup lifecycle campaigns → `/lifecycle-marketing`
- User wants content calendar → `/content-strategy`
- User wants outbound automation workflows → `/gtm-engineer`
- User wants ICP definition → `/icp-behavioural`
- User wants competitive analysis → `/competitor-research`

**Auto-suggest after:** `company-context` completes, or user mentions funnel/pipeline/lead-stages/qualification, or user asks about GTM motion / sales process. Always require confirmation before running.

**Research substrate:** Exa per `.claude/rules/exa-protocol.md` (auto-loaded). Primary tool `web_search_exa` for competitor GTM motion + funnel research. Plugin `mcp__plugin_exa_exa__web_search_exa` preferred; legacy `mcp__exa__web_search_exa` still mounted. Citations: `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]`. Quality gate: ≥3 sources per major claim, ≥50% `[VERIFIED]`, date filter for "recent/latest" claims.

## Inputs

**Required:**
- **Company URL** — website URL for the target company (user provides).

**Recommended (improve quality):**
- `company-context` output — ACV, team size, funding (improves motion detection accuracy)
- `icp-behavioural` output — persona buying triggers (informs qualification criteria)
- CRM screenshot or pipeline stages — real stages override inferred ones, increases confidence
- ACV or pricing information — directly determines PLG vs SLG likelihood

**Validation:** Company URL valid + accessible · ACV/team size extracted if company-context available · CRM stages complete if provided.

## Steps

Three phases (visual flowchart + per-step narrative in `references/process-flowchart.md`).

1. **Phase 1.1 — Fetch company website** (WebFetch): Homepage primary CTA ("Sign up free" vs "Book a demo"), pricing page (visible plans, self-serve checkout vs "Contact sales"), product pages (signup flow, free trial, freemium), navigation (Docs/API = PLG signal).
2. **Phase 1.2 — Run Exa company search** (`company_research_exa`): Company size + stage, industry/category, funding, GTM team composition, market context, competitors.
3. **Phase 1.3 — Score signals + classify motion**: Apply the signal scoring table from `references/funnel-templates.md`. Rules: PLG ≥8 AND SLG ≤3 → PLG · SLG ≥8 AND PLG ≤3 → SLG · Both ≥5 → Hybrid · Else ask user. Cross-reference industry + ACV heuristics.
4. **Phase 1.4 — Declare motion with confidence**: "Based on [signals], this looks like a **[Motion]** GTM motion. Key evidence: [2-3 strongest signals]. Confidence: [High/Medium/Low]." If ambiguous, ask user to confirm. Phase 1 checkpoint: motion classified with evidence.
5. **Phase 2.1 — Select funnel template** from `references/funnel-templates.md`: PLG → ONLY PLG stages. SLG → ONLY SLG stages. Hybrid → both tracks with PQL escalation logic. No mixing.
6. **Phase 2.2 — Customize each stage**: Produce definition (1-2 sentences for THIS company), strategy (specific to product/market/resources), **inputs as LEADING indicators** with frequency (activities you control: "Publish 3 LinkedIn posts/week"), **outputs as LAGGING indicators** with target numbers (results you measure: "500 visitors/month"), cadence (weekly/monthly/quarterly), goal logic (work backwards: output target / conversion rate = input volume), owner. Never put metrics in inputs. Tailor to team size, channels, industry norms. Detail in `references/process-flowchart.md`.
7. **Phase 2.3 — Define qualification criteria**: 3-5 signals each for MQL (marketing→sales handoff), SQL (SDR confirms before AE), PQL (product usage signals — PLG/Hybrid only). Use templates from `references/funnel-templates.md`, customize.
8. **Phase 2.4 — Map Closed Lost re-entry paths**: Brief table — Loss Reason / Re-entry Stage / Trigger / Timing.
9. **Phase 3 — Post-close mapping** (4 stages, same definition+strategy+inputs+outputs format): Onboarding (path to first value — PLG in-app guided vs SLG CSM-driven). Retention (touchpoints, multi-threading, health scoring). Expansion (usage-limit/team-adoption/new-use-case signals → seat upgrade, tier upgrade, add-ons). Churn prevention (declining usage, champion departure, support escalations, renewal-without-engagement, competitive evaluation). Match motion: PLG = product-led; SLG = CSM-driven.
10. **Build output document** following the canonical scaffold in `references/output-format.md`: GTM motion assessment table → pre-close stages → qualification criteria → post-close stages → Closed Lost re-entry → full journey ASCII → FETE mapping (Find/Enrich/Transform/Export → funnel stages → activities) → gaps + recommendations → source appendix.
11. **If client has revenue targets** — apply backward funnel math from `references/guardrails-and-math.md` (Revenue → Deals needed → Opportunities → SQLs → MQLs → Leads → Traffic). Validate funnel capacity vs growth goals.
12. **Run guardrails** in `references/guardrails-and-math.md` (8 anti-hallucination rules: never invent stages, don't assume motion, criteria must be specific, mark inferred fields, don't fabricate ACV, post-close matches motion, source everything, don't invent KPI targets).
13. **Run quality checklist + 7-test self-eval** in `references/quality-checks.md` (CRM-ready, SDR, content strategist, specificity, motion consistency, dashboard, activity tests). If any fails: "Auto-review flagged: [issue]. Want me to fix this or ship as-is?"
14. **Present at Review Gate 2** (standard review): GTM motion + full stage map + qualification criteria. Actions: Approve / Adjust / Add stages.
15. **Suggest chains** post-delivery: gtm-engineer (FETE map) · content-strategy · outreach-emails · sales-enablement (battlecards) · landing-page-copy.

## What good looks like

### References

- **`references/funnel-templates.md`** — PLG/SLG/Hybrid stage templates (8 SLG stages, 7 PLG stages, Hybrid dual-track), signal scoring table, classification rules, ACV-to-motion + industry pattern heuristics. Source of truth for Step 5 + Step 7.
- **`references/lead-magnet-archetypes.md`** — 10 reusable lead-magnet archetypes (audit, data piece, competitive intel, template, intro, quick-win, observation, free tool, working session, benchmark) + 4-question intake + scoring rubric + combination patterns. Use when defining stage-level CTAs or when a campaign's offer feels weak. Stolen via /steal Phase 5–6 BUILD #4.
- **`references/process-flowchart.md`** — Three-phase ASCII flowchart, per-step narrative detail (Phase 1 motion detection, Phase 2 stage definition, Phase 3 post-close), agent persona, leading-vs-lagging distinction.
- **`references/output-format.md`** — Canonical output template (frontmatter, motion assessment, pre/post-close scaffolds, qualification criteria, Closed Lost, FETE mapping, source appendix), plus anti-examples table.
- **`references/guardrails-and-math.md`** — 8 anti-hallucination rules + backward funnel math formula (revenue → traffic).
- **`references/quality-checks.md`** — Pre-delivery binary checklist (content / leading-lagging / format / completeness) + 7-test self-eval protocol.
- **`references/auto-update-protocol.md`** — Feedback signal table, pattern detection rules (3+ trigger), upstream/downstream skill integration, recommended workflow sequences, MCP data integration, changelog.

### Examples

- **`references/examples/genesys-growth-funnel.md`** — Worked SLG example. Genesys Growth (B2B GTM consulting, solopreneur, "Book a call" CTA, ACV $22.5K-$240K, no public pricing). Motion: SLG (PLG: 1, SLG: 10, High confidence). 7 pre-close stages. Inputs: "3 LinkedIn posts/week", "1 newsletter/week", "1 warm intro ask/month". Outputs: "3,000 visitors/month", "4 discovery calls/month", "2 proposals/month". Goal logic: "150 posts → ~3K visits → 2% convert = 60 prospects/year". Why good: clean leading/lagging, hand-off-ready to a marketing coordinator, no PLG contamination.
- **`references/examples/ClientCo-funnel.md`** — Worked Hybrid example. ClientCo (£49/user/month, "Get Started for Free" + "Request Demo", 57% self-serve, enterprise consolidator customers). Motion: Hybrid (PLG: 13, SLG: 10, High confidence). 10 pre-close stages dual-track converging at Opportunity. PLG inputs: "2 review responses/month", "1 product update/sprint", "1 onboarding sequence/signup". SLG inputs: "1 industry event/quarter", "2 outbound sequences/month", "4 free template builds/month". Why good: separate dashboards possible per track, realistic for 11-person team, PQL escalation tied to financial-adviser industry.

### Evaluations

- GTM motion classified with 3+ supporting signals; motion exclusivity respected (no PLG stages in SLG output).
- Every input has a frequency; every output has a target number; every stage has a cadence.
- Goal logic connects input volume to output targets (work-backwards math).
- Inputs are leading indicators (activities); outputs are lagging (metrics) — never confused.
- Qualification criteria are measurable thresholds, not "good fit" platitudes.
- Post-close motion matches pre-close (PLG product-led retention; SLG CSM-driven retention).
- Closed Lost re-entry paths documented; FETE mapping included.
- Source appendix has URL + access date + confidence per signal.
- Stage format consistent across all stages (definition / strategy / inputs / outputs / cadence / goal logic / owner).
- Backward funnel math applied when revenue targets provided.
- All 7 self-eval tests pass: CRM-ready, SDR, content strategist, specificity, motion consistency, dashboard, activity.

## Push

| Target | When | Rationale |
|--------|------|-----------|
| `client_folder/context/` (Google Doc) | After Review Gate 2 approval | Stakeholder visibility on motion classification + stage map |
| `gtm-engineer` skill | When user asks for FETE pipeline build | Funnel stages map to Find/Enrich/Transform/Export |
| `content-strategy` skill | When user wants stage-aligned content | Stage inputs inform what content per stage |
| `outreach-emails` skill | When user wants stage-specific sequences | Stage-appropriate messaging |
| `sales-enablement` skill | When user wants battlecards | Qualification criteria → battlecard checklist |
| `landing-page-copy` skill | When user wants conversion-stage pages | Stage conversion points → which pages needed |
