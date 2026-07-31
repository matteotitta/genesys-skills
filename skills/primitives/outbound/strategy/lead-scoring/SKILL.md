---
name: lead-scoring
version: '1.0'
last_updated: 2026-03-31
author: genesys-growth
description: Evaluates accounts and prospects for fit and readiness using signal-based scoring. Produces a fit verdict (STRONG_FIT
  through NO_FIT), signal inventory, situation hypothesis, and routing recommendation per account. Outputs feed into outreach-emails,
  abm-campaign, sales-enablement, and client-discovery. Triggered by "score this lead", "evaluate this account", "prioritize
  these accounts", "is this a good fit", "should we pursue [company]", or "rank these prospects". Consumes icp-research and
  company-context as upstream inputs. NOT a numeric score — produces situational understanding per account.
goal: Evaluates accounts and prospects for fit and readiness using signal-based scoring.
outcome: Evaluates accounts and prospects for fit and readiness using signal-based scoring. Produces a fit verdict (STRONG_FIT
  through NO_FIT), signal inventory, situation hypothesis, and routing recommendation per account. Outputs feed into outreach-emails,
  abm-campaign, sales-enablement, and...
primitive: outbound
sub_primitive: strategy
ontology_type: lead-assessment
review_gate: 1
inputs:
  required: []
  recommended:
  - icp-research
  - company-context
- type: lead-assessment
  feeds_into:
  - outreach-emails
  - abm-campaign
  - sales-enablement
  - client-discovery
depends_on: []
- abm-campaign
- client-discovery
- outreach-emails
- sales-enablement
owned_by_agent: operator
mcps_used:
- gdrive
- notion
- gdrive
- notion
triggers:
  slash_commands:
  - /lead-scoring
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Lead scoring

Evaluate accounts through three layers — fit (structural), signals (temporal), interpretation (synthesized) — to produce a routing recommendation per account. NOT a composite numeric score. Compressing fit, timing, and context into one number destroys the information operators need to act.

## When to run

- User asks "score this lead", "is X a good fit", "should we pursue X", "prioritize these accounts", "rank these prospects"
- ABM campaign needs account tiering input
- Pre-discovery account brief, sales pipeline qualification gate

Skip when: user wants full research without assessment angle (`/company-context`), ICP definition (`/icp-research`), ABM tactics on already-tiered accounts (`/abm-campaign`), outreach copy (`/outreach-emails`).

## Inputs

**Required:** at least one company identifier (URL, LinkedIn URL, or name).

**Recommended (lift quality):** client ICP doc (`/icp-research`), CRM engagement history, competitor list, prior `/company-context` output.

**Mode detection:** single account → deep assessment. Batch (5+ accounts) → lightweight pass + priority matrix. >15 accounts → calibration round + parallel waves (see the premium reference).

If ICP doc missing: proceed with generic B2B SaaS criteria, flag as "generic ICP" in output, suggest `/icp-research` upstream.

## Steps

1. **Validate input** — confirm company identifier(s), determine mode (single/batch), identify ICP reference.
2. **Fit assessment (Phase 1)** — score firmographic, technographic, use case, negative-fit dimensions per the premium reference. Output verdict: STRONG_FIT | MODERATE_FIT | WEAK_FIT | NO_FIT with evidence + confidence per dimension.
3. **Signal detection (Phase 2)** — catalog leadership, growth, intent, operational, engagement signals per the premium reference. Tag each with category, recency (strong/moderate/weak/expired per decay table), source URL, confidence level.
4. **Apply recency decay** — drop expired signals from active inventory; weak-recency signals provide background only, don't drive routing. Decay table in the premium reference.
5. **Interpret signal clusters (Phase 3)** — identify reinforcement, contradictions, dominant story. Write 2-4 sentence situation hypothesis: "Based on [cluster], [company] appears to be [situation]. This suggests [implication]. The window is [timeframe] because [decay reasoning]."
6. **Confidence assessment** — rate HIGH (dense + fresh + diverse) | MODERATE (2 of 3) | LOW (sparse or stale).
7. **Routing recommendation (Phase 4)** — apply fit × signals matrix in the premium reference. Output: SALES | MARKETING | MONITOR | EVALUATE | DEPRIORITIZE | DISQUALIFY + 2-3 sentence rationale + 1-3 specific next actions.
8. **Optional — activation score** — if client wants auditable math: `signal_activation = strength × recency × fit × tier_weight`, sum top-3 per account, bucket into Hot/Warm/Nurture/Cold. Formula in the premium reference.
9. **Optional — tier mode (numeric)** — if client CRM needs a `lead_score` field or sales ops wants a single-column sort: compute weighted tier_score (0-5) and bucket Tier 1 / 2 / 3 / Disqualify. Formula + alignment-with-routing check in the premium reference.
10. **Self-evaluation gate** — every signal has source + recency tag, fit dimensions have evidence (not assumption), interpretation reads as narrative not list, routing follows fit×signals matrix, gaps marked [UNAVAILABLE], confidence levels per ontology.
11. **Format output** — single account: full template in the premium reference. Batch: priority matrix template.
12. **Review gate (Level 1)** — present fit verdict, signal summary, situation hypothesis, routing recommendation. Actions: [Approve] [Challenge fit] [Add signals] [Change routing].
13. **Suggest chain** — if SALES routing → `/outreach-emails`. If batch → `/abm-campaign`. If fit uncertain → `/company-context`. If no ICP → `/icp-research`.

## Scoring validity — before fit-rules count as predictive

When the fit rubric or ICP rules are **derived from a client's own customers** (won deals, a "good-fit" list), they fit those examples by construction and routinely fail on the wider universe. Before treating derived rules as predictive — or locking a numeric tier/activation model (steps 8–9) tuned on a small known-positive set — clear the pre-lock gate in [`.claude/rules/scoring-validity.md`](../../../../../rules/scoring-validity.md): ground-truth provenance, base rate + discriminative ratio (≥2.0), holdout, backwards-reasoning check. Below the sample floor (our client set is often N≈8), ship a **directional hypothesis**, not a locked rule. Scoring a single account against an *already-validated* rubric doesn't trigger this — *deriving* the rubric from outcomes does.

## What good looks like

- `projects/research/taste-library/resources/0626-sales-qualification-frameworks/health-rubrics.md` — deal-health (10-dim) + account-health (9-dim) rubrics; bolt onto fit+signal scoring when the account is an open opportunity, not just a prospect (re-weight per client motion)

**Examples:** none baked into skill (every assessment is account-specific). Pull patterns from `projects/consulting/{client}/sales/` lead-assessment outputs when present.

**Evaluations — output passes if:**
- Fit verdict cites evidence per dimension (not asserted)
- Every signal tagged with category + recency + source URL + confidence
- Situation hypothesis reads as 2-4 sentence narrative, not a list
- Routing follows fit×signals matrix (divergence flagged with rationale)
- No invented data; gaps marked [UNAVAILABLE]
- If tier mode active: tier and routing align (or divergence has 1-sentence rationale)
- Decay applied: weak-recency signals don't drive routing, expired excluded

**Anti-patterns (auto-fail):**
- Compressing into single composite score without preserving fit/signal/interpretation layers
- Binary STRONG_FIT or NO_FIT verdicts (full 4-tier range required)
- Score with no routing recommendation
- Months-old signals treated as fresh
- Employee count as primary fit indicator (revenue model, tech stack, growth trajectory often matter more)

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
