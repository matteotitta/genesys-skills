---
name: ab-testing
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Designs statistically valid A/B tests with hypothesis formulation, ICE prioritization, sample-size calculation (550/variant at 10% baseline + 50% lift up to 150k/variant at 1% baseline + 10% lift), pre-committed duration, 95% confidence threshold (p<0.05), no-peeking discipline, and 20–30% target win rate. Distinct from /experiment (which tracks hypothesis-results-learnings across experiments) — this skill is the per-test design layer. Triggered by "ab test design", "test hypothesis", "sample size", "split test", "experiment design", "statistical significance". NOT for analyzing results post-hoc — use /experiment or /dashboard.
goal: Design statistically valid A/B tests that produce trustworthy winners, not false positives.
outcome: Produces (1) hypothesis in canonical form, (2) ICE score, (3) sample-size calculation, (4) pre-committed duration, (5) variant designs, (6) success-metric definition, (7) results-evaluation rubric.
primitive: website
sub_primitive: execution
ontology_type: experiment-log
review_gate: 2
inputs:
  required: []
  recommended:
  - analytics-tracking-plan
  - signup-onboarding-audit
  - landing-page-audit
- type: experiment-log
  feeds_into:
  - experiment
depends_on:
- analytics-tracking-plan
- experiment
owned_by_agent: growth
mcps_used:
- exa
- gdrive
triggers:
  slash_commands:
  - /ab-testing
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /ab-testing — statistically valid test design

Design A/B tests that produce trustworthy winners. The bar: pre-commit to sample size, hold the line on duration, only call results at 95% confidence.

Without this discipline, tests yield false-positive "winners" that don't replicate in production — and the team loses trust in the experimentation program within 2 quarters.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (test brief is client-team review surface — cleaned cites in appendix), R3 (test-result reports operator-direct), R6 (variant CTA hierarchy explicit per stage), R9 (verb-led test-design section names).

---

## When to invoke

- Landing-page test on hero copy / CTA / pricing variant.
- Signup-flow optimization (paired with `/signup-onboarding-audit` findings).
- Email subject-line test in lifecycle sequence.
- In-product popup variant (per `/in-app-popups` A/B hypothesis output).
- Pricing-page test on tier presentation / CTA copy.

Do NOT invoke when:
- Traffic / volume is too low for statistical power (see Step 3 — sample-size table).
- The hypothesis is "let's try this" with no observation-based reasoning.
- Multi-variable changes simultaneously — confounded; can't isolate cause.
- The decision is reversible at near-zero cost (just ship and observe).

---

## Workflow

### Step 1 — Hypothesis in canonical form

Use the format:

> "Because **{observation}**, we believe **{change}** will cause **{outcome}** measured by **{metric}** within **{timeframe}**."

Example:
> "Because 47% of users drop off at the company-size field, we believe removing the field will increase signup completion by 25% measured by signup-completion-rate within 2 weeks."

Each component is mandatory:
- **Observation:** evidence-based, not gut.
- **Change:** single-variable. Don't bundle.
- **Outcome:** direction + magnitude prediction.
- **Metric:** specific event name (per `/analytics-tracking-plan`).
- **Timeframe:** pre-committed; matches sample-size duration.

### Step 2 — ICE prioritization

Score backlog hypotheses on three factors (1–10 each):

| Factor | Question |
|---|---|
| Impact | If true, how much does this move the metric? |
| Confidence | How sure are we the hypothesis is correct? |
| Ease | How quickly can we ship + measure? |

ICE score = Impact × Confidence × Ease.

Test the highest ICE first. Run 4–8 tests/month at 2–4 week durations is the source's recommended cadence — caps simultaneous tests at 1–2 per traffic source to avoid interaction effects.

### Step 3 — Sample-size calculation

The non-negotiable math. Use this table as default (from source, MIT):

| Baseline conversion | Minimum detectable effect (relative lift) | Sample size per variant |
|---|---|---|
| 10% | 50% lift | ~550 |
| 10% | 25% lift | ~2,200 |
| 5% | 50% lift | ~1,200 |
| 5% | 25% lift | ~4,700 |
| 3% | 50% lift | ~2,100 |
| 3% | 25% lift | ~8,400 |
| 1% | 50% lift | ~6,500 |
| 1% | 25% lift | ~26,000 |
| 1% | 10% lift | ~150,000 |

(Assuming 80% statistical power, p<0.05 significance, 50/50 split.)

**Sharp rule:** if traffic is insufficient to reach sample-size within 2 months, don't A/B test. Use sequential ship-and-observe instead — A/B testing on noise is theatre.

### Step 4 — Pre-commit + no peeking

Two of the most-violated rules:
- **Pre-commit to sample size** before launching the test. Don't decide "we'll watch and stop when we see significance".
- **No peeking.** Looking at results before sample-size is reached **increases false-positive rate**. Wait until the pre-committed number.

If you must inspect mid-test, do so for **system-health** checks only (is data flowing? are events firing?) — not for results inference.

### Step 5 — Variant design

Variants are mockups + implementation specs:
- Control: current state (don't change).
- Variant B: the single change.
- (Variant C, D if multivariate test — but caps complexity; 2-variant tests are 90% of useful work.)

Design specs include the changed element, surrounding context preserved, and any analytics-event changes (per `/analytics-tracking-plan`).

### Step 6 — Success metric definition

Pre-commit to the single primary metric. List 2–3 secondary metrics (signals, not deciders).

| Type | Example |
|---|---|
| Primary | Signup-completion rate |
| Secondary | Time-to-completion, error rate, mobile vs. desktop split |
| Guardrail | Bounce rate, downstream activation (don't break the funnel for an upstream win) |

If the primary moves but a guardrail breaks, the test is a loss — even if the primary is statistically significant.

### Step 7 — Results-evaluation rubric

After sample-size is reached:
- **Significance check:** p < 0.05 → call result. p ≥ 0.05 → inconclusive (don't call winner).
- **Practical-significance check:** lift in absolute terms — is it meaningful for the business? A statistically-significant 0.2% lift may not be worth shipping.
- **Guardrail check:** any downstream metric break? If yes, reject.
- **Win rate:** track program-wide. Target 20–30%; higher suggests overly conservative hypotheses; lower suggests hypothesis quality issues.

### Step 8 — Document the playbook entry

Win or lose, the test produces a learning. Format:
- Hypothesis (verbatim from Step 1).
- Sample size + duration (actual vs. pre-committed).
- Result (winner / inconclusive).
- Lift (absolute + relative).
- Learning: what would we test next based on this?

Hand off to `/experiment` for accumulation in the experiment log.

---

## Anti-patterns

- ❌ "Just look at the numbers and stop when significant." → false-positive trap.
- ❌ Multi-variable variants. Confounded; can't isolate.
- ❌ Test on traffic too low for sample size in 2 months.
- ❌ No pre-commit to primary metric. Cherry-picking after results = science theatre.
- ❌ Ignore guardrails. Winning the homepage CTR test by breaking trial-to-paid is a loss.
- ❌ Skip post-mortem on the losing variant. Learnings come from losses too.

---

## Integration with other skills

- **Upstream:** `/analytics-tracking-plan` provides the events for measurement; `/signup-onboarding-audit`, `/landing-page-audit`, `/in-app-popups` produce A/B hypotheses ready for design.
- **Downstream:** `/experiment` tracks the test in the broader experiment log; winning variants ship via `/landing-page-copy` or `/signup-onboarding-audit` follow-up.
- **Companion:** `/marketing-psychology` rule informs hypothesis design (e.g., loss-frame variants per Heuristic 4).

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/ab-testing/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/ab-testing/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice. Sample-size table verbatim per Step 3.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

