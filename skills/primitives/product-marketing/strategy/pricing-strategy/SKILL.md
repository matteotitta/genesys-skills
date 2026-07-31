---
name: pricing-strategy
version: '1.0'
last_updated: 2026-01-21
author: genesys-growth
description: Designs a pricing model with tier structure, value metrics, and packaging recommendations. Produces pricing page
  copy guidance, competitive pricing comparisons, and monetization strategy. Triggers on "pricing strategy", "pricing tiers",
  "packaging", "value metric", "monetization", or "pricing page". Requires positioning and competitor-research as upstream
  inputs. NOT for price sensitivity surveys or WTP data collection — use pricing-research instead.
goal: Designs a pricing model with tier structure, value metrics, and packaging recommendations.
outcome: Designs a pricing model with tier structure, value metrics, and packaging recommendations. Produces pricing page
  copy guidance, competitive pricing comparisons, and monetization strategy. Triggers on "pricing strategy", "pricing tiers",
  "packaging", "value metric", "monetization", or "pricing...
primitive: product-marketing
sub_primitive: strategy
ontology_type: pricing-strategy
review_gate: 2
inputs:
  required: []
  recommended:
  - product-messaging
  - icp-behavioural
  - competitor-research
- type: pricing-strategy-document
  feeds_into:
  - website-copy
  - sales-enablement
  - product-messaging
depends_on: []
- website-copy
- product-messaging
- sales-enablement
owned_by_agent: pmm
mcps_used:
- exa
- gdrive
- notion
- gdrive
- notion
triggers:
  slash_commands:
  - /pricing-strategy
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Pricing strategy

Develop a data-informed B2B SaaS pricing strategy through customer research, competitive analysis, and structured framework application. Output guides pricing decisions, tier structure, value metric selection, and pricing page optimization. Knowledge type: `pricing-strategy` (per `.claude/rules/ontology.md`); maturity: emergent → validated after team review → canonical when locked. Visual phase map + triggers + input checklist → the premium reference.

## When to run

Invoke when the user asks for: `pricing strategy for [product/company]`, `help me figure out pricing for [product]`, `how should I price [product]?`, `Van Westendorp analysis for [product]`, `MaxDiff for feature prioritization`, `design pricing tiers for [product]`, `what's the right value metric for [product]?`, `pricing page optimization for [company]`, `compare competitor pricing in [category]`. Do **NOT** invoke for: pricing page copy only (use `/landing-page-copy` — run this first if strategy needed), competitor research only (use `/competitor-research`), product messaging only (use `/product-messaging`), or quick single-element questions (answer directly without full framework). Full trigger + invocation rules → the premium reference.

**The Iron Law:** no pricing recommendation without source verification. Every competitor price cites URL + access date. Price points are ranges, never single points of false precision. Customer willingness data is collected (Van Westendorp / MaxDiff) or explicitly marked as `[Customer research required]` — never invented. Full guardrails → the premium reference.

## Inputs

**Required:**

- `product name` — product being priced.
- `current pricing` — existing pricing if any (or explicit "no current pricing").

**Recommended (improve quality):**

- `competitor pricing` — provides market anchors.
- `ICP research` — identifies willingness to pay by segment.
- `product messaging` — clarifies value prop for pricing alignment.
- `customer feedback` — direct willingness-to-pay signals.

**Upstream skill outputs (if available, read first):**

- `competitor-research` — provides pricing dimension data; market anchoring.
- `icp-behavioural` — segment-level WTP signals.
- `product-messaging` — value proposition alignment.
- `positioning` — frames whether to price above/below market.

If product name is missing, ask. If current pricing status is ambiguous (new product vs. optimization), confirm research mode (full strategy vs. specific component) before starting.

## Steps

1. **Validate inputs** → confirm product name + current pricing status + research mode. Pull upstream skill outputs (competitor-research, icp-behavioural, product-messaging, positioning) into context if available. Skip Exa/Firecrawl pulls if competitor-research already covers pricing depth (per the premium reference MCP table).
2. **Phase 1.1 — Competitive pricing analysis** → research 3-5 direct competitors' pricing pages via `web_fetch_exa` (per `.claude/rules/exa-protocol.md`). Document pricing model, tiers, price points, value metrics. Flag public pricing vs. "contact sales". Output: competitive pricing matrix with URLs + access dates.
3. **Phase 1.2 — Value metric analysis** → identify what competitors charge for (seats / usage / features / flat / hybrid). Score options against Value Metric Selection framework (the premium reference): alignment, predictability, growth-friendly, measurable, competitive. Output: ranked options with pros/cons.
4. **Phase 1.3 — Customer willingness research design** → design Van Westendorp survey (4 questions: too cheap / cheap / expensive / too expensive). Identify target segments + sample size (100+). Methodology details → the premium reference (and the premium reference summary). Output: survey ready for deployment.
5. **Phase 1.4 — Feature value ranking design** → design MaxDiff study (4-5 features per set, MOST/LEAST important rotation). Identify features to test (50+ respondents minimum). Methodology → the premium reference. Output: study ready for deployment.
6. **Phase 2.1 — Tier structure design** → apply Good-Better-Best framework (the premium reference). Define feature fencing per tier across usage / access / feature gates / support levels. Establish upgrade triggers (usage 80%, team growth, feature request, success/maturity). Output: tier structure with rationale.
7. **Phase 2.2 — Price point recommendations** → develop ranges per tier (never single points). Document confidence level + rationale per range. Anchor against competitive prices and (if available) Van Westendorp PMC-PME range. Output: price recommendations with ranges.
8. **Phase 2.3 — Pricing page optimization** → select 3-5 experiments from canonical library (the premium reference — annual default, savings %, tier count, enterprise visibility, comparison table, social proof, "most popular" badge, price ending, free trial CTA, per-seat framing). Define A/B hypotheses + success metrics + copy recommendations.
9. **Apply attribution standards** → per `.claude/rules/ontology.md`: `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]`, `[INFERRED: from X + Y]`, `[ESTIMATED: reasoning]`, `[UNAVAILABLE]`. Quality threshold for client-deliverable strategy outputs: ≥60% verified, ≤10% estimated.
10. **Self-evaluate against quality gates** → the premium reference. Run completeness, evidence-quality, and guardrail checks. Answer self-roast questions honestly. If invented WTP data found → strip and replace with `[Customer research required]`.
11. **Write to client folder** per output template → the premium reference. File path: `{client}/pricing/MMYY-pricing-strategy.md` (or per client CLAUDE.md folder map). Header includes skill name, generated date, font (Inter), version. Include data gaps section + recommended next steps.
12. **Push** to Notion (Pricing Strategy Database) and Google Docs (`client_folder/strategy/`) per push targets in frontmatter. Refresh runs UPDATE existing pages — don't duplicate.
13. **Offer iteration prompts** post-delivery → the premium reference. Surface refinement / expansion / quality offers based on data gaps detected in step 10.

## What good looks like

### Evaluations (binary pass/fail before declaring "done")

- 3-5 competitors documented with public pricing or "contact sales" status, source URL + access date per row.
- Value metric recommendation made with explicit scoring against alignment / predictability / growth-friendly / measurable / competitive (or marked `[Customer research required]`).
- Customer research design included: Van Westendorp survey (4 questions verbatim, target segment, sample size ≥100) and MaxDiff study (feature list, sample size ≥50) — or explicit reason omitted.
- Tier structure follows Good-Better-Best with target user + price range + features + upgrade trigger per tier (3 tiers minimum).
- Every price recommendation is a range (e.g., `$79-119/mo`), never a single point. Each range has a stated rationale.
- Feature fencing has explicit rationale per tier (usage / access / feature gates / support level).
- Pricing page section includes ≥3 experiments selected from canonical library, each with hypothesis + success metric.
- Data gaps section non-empty if ANY component lacks customer-research backing; "How to obtain" column populated.
- Every claim has source URL + access date; confidence level assigned (`[VERIFIED]` / `[INFERRED]` / `[ESTIMATED]` / `[UNAVAILABLE]`).
- ≥60% `[VERIFIED]` confidence; ≤10% `[ESTIMATED]` (per ontology threshold for client deliverables).
- No invented willingness-to-pay numbers — every WTP claim either cites primary research or is marked `[Customer research required]`.
- Output title is `# Pricing strategy: [Product Name]` exactly — no aliases.

## Pre-slim original

Pre-slim SKILL.md (774 lines, v1.0) archived at `.claude/skills/_archive/pricing-strategy/SKILL-pre-slim-20260429.md`. See the premium reference ("Changelog") for the v1.1 entry documenting the slim.

---

## Sourced patterns — paywall + upgrade-screen design

<!-- Sourced from coreyhaines31/marketingskills/paywalls/SKILL.md (MIT) — accessed 2026-05-17. Imported via /steal I1. -->

When the pricing strategy includes in-product upgrade moments (freemium → paid, trial → paid, usage-cap → upgrade), apply these trigger-design patterns:

- **Value-before-ask trigger logic.** Users need real product experience before the upgrade prompt fires. Never paywall a brand-new account; let them feel the value first. Trigger at: post-aha moments, usage-limit approach (80% of cap), trial-day-N nearing expiry.
- **Cooldown windows in days, not hours.** Once a paywall is dismissed, the cooldown before re-showing should be measured in days (3–7 days minimum), not hours. Hourly re-shows tank trust + product NPS.
- **Friction-free path from paywall to payment.** Once the user clicks "Upgrade", the steps to complete payment should be ≤ 3 (plan selection, payment details, confirm). Each additional step doubles drop-off.
- **Show, don't tell — feature gating.** When gating a feature, demonstrate the gated benefit through previews, comparisons, or read-only access rather than text-only descriptions. "See the report you'd get on Pro" beats "Pro includes advanced reports."
- **Respect the No — easy dismissal.** Visible close button (no hidden ❌, no microscopic dismiss). Easy "no" maintains trust for future conversion windows.
- **Dark-pattern anti-list:** hidden close buttons, confusing plan selection, guilt-trip messaging ("Are you SURE you don't want premium?"), forced sign-in to dismiss, modal that returns immediately on click-outside. All of these are short-term conversion uplifts that destroy long-term LTV.
- **Track paywall impression rate, click-through conversion, AND post-upgrade churn.** The "winning" paywall variant may convert at higher rate but produce upgraders who churn within 30 days — those upgraders cost more than they earn.

(Note: a dedicated `/pricing-audit` skill is on the backlog per `.claude/rules/audit-triage-pairing.md` — these patterns live here in the meantime.)

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
