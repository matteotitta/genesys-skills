---
name: referral-program
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Designs customer referral programs with the Trigger Moment → Share → Convert → Reward loop, incentive structure selection (single-sided / double-sided / tiered), share-mechanism hierarchy, and launch checklist. References benchmark LTV uplift (16–25% higher LTV, 2–3× refer rate, 18–37% lower churn for referred customers). Triggered by "referral program", "design a referral mechanic", "viral loop", "customer advocacy program", "incentivized referrals". NOT for affiliate / partner networks — separate dynamic.
goal: Design a customer-referral program that converts existing users into a measurable growth channel.
outcome: Produces (1) trigger-moment selection, (2) share-mechanism design, (3) incentive structure with cost modeling, (4) launch checklist + email sequences, (5) KPI targets + measurement framework.
primitive: lifecycle
sub_primitive: null
ontology_type: lifecycle-campaign
review_gate: 2
inputs:
  required: []
  recommended:
  - icp-behavioural
  - product-messaging
  - lifecycle-marketing
- type: lifecycle-campaign
  feeds_into:
  - lifecycle-marketing
depends_on: []
- lifecycle-marketing
owned_by_agent: growth
mcps_used:
- exa
- gdrive
triggers:
  slash_commands:
  - /referral-program
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /referral-program — customer-referral loop design

Design a customer-referral mechanic where existing users become a measurable growth channel. Distinct from affiliate / partner programs (different intent, different incentive math).

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`marketing-psychology.md`](../../../../rules/marketing-psychology.md)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in referral-program |
|---|---|---|
| **R1** | Source placement | Referral copy on emails / in-product nudges / share pages → end-customer-facing → **no sources block.** Program-design doc (internal) carries cites for QA only. |
| **R2** | Single-doc-with-toggles | Multi-touch referral program (invite email + reminder + share-page + reward-claim email) ships as one doc with toggle per asset. |
| **R3** | Product-update tone | Reward framing — "earn X for sharing" not "we are thrilled to reward you." |
| **R6** | CTA hierarchy | Sender-side (existing user) → product-action ("share your link"). Receiver-side (referred prospect) → sign-up primary, blog as fallback. |
| **R9** | Action-oriented section names | "How to share / How to claim your reward" — verb-led. |

---

## Why bother — the benchmark

Per source data (cite-verified, MIT):
- Referred customers show **16–25% higher LTV** than typical customers.
- Referred customers refer at **2–3× the rate** of typical customers (compounding).
- Referred customers have **18–37% lower churn**.

Net: a referral loop with even modest uptake is one of the highest-ROI growth investments available — but only if the trigger moment, share mechanism, and incentive math are all dialed.

---

## The loop — 4 stages

```
Trigger Moment → Share Action → Convert Referred → Reward → (back to Trigger)
```

If any stage breaks, the loop stalls. Audit each stage independently when diagnosing a stalled program.

---

## Workflow

### Step 1 — Trigger Moment selection

The high-intent moment when a customer is most likely to share. Candidates ranked by typical conversion:

| Moment | Why it works | Typical timing |
|---|---|---|
| Post-aha (immediately after the first wow) | Emotion is peak | Within minutes of activation |
| Post-milestone (e.g., 10 reports generated, 1 month anniversary) | Reflection moment | At the milestone event |
| Post-positive-support interaction | Reciprocity is fresh | Within 24 hours of resolution |
| In-app sustained-use moment (e.g., login streak) | Habit signal | When tracked behavior hits threshold |

**Sharp rule:** never trigger on signup or trial-start. Customer hasn't felt the value yet; share fires hollow.

### Step 2 — Share Mechanism — hierarchy by conversion

Order share mechanisms by conversion rate (highest first):

1. **In-product native share** (one-click within the product) — highest conversion.
2. **Personalized link with name + context** (e.g., "Matteo invited you").
3. **Personalized email referral** (sender adds note in their own voice).
4. **Generic share via email / SMS** (template).
5. **Social share** (LinkedIn, X) — high reach, low conversion per share.
6. **Referral code** (manually entered) — lowest conversion; reserve for offline channels.

**Sharp rule:** every program needs at minimum the top 3. Generic-code-only programs underperform by 5–10×.

### Step 3 — Incentive structure

Three patterns:

| Structure | Mechanic | Best for |
|---|---|---|
| Single-sided | Referrer gets reward; referred gets nothing | When the product is the reward (cheap referrals) |
| Double-sided | Both get reward | Standard B2B SaaS pattern |
| Tiered | Reward escalates with referral count (e.g., 1 = $50, 5 = $500, 10 = $2k) | High-LTV products where compounding matters |

**Sharp rule:** double-sided is the default. Single-sided fails when the referred customer has zero curiosity reason. Tiered is for $1k+/year products where compounding is worth the complexity.

**Cost modeling:** target referral cost-per-acquisition (CPA) ≤ 30% of LTV. Above that, the program drains margin. Below that, the program isn't generous enough to drive participation.

### Step 4 — Launch checklist

- Trigger moment instrumented (event fires in analytics when the moment hits).
- Share mechanism live (in-product + personalized link, minimum).
- Incentive backend ready (reward delivery automated, not manual).
- Tracking attribution (referred-customer flag set at conversion; downstream LTV / churn dashboards segment by it).
- Email sequence (3-touch): Day 0 invitation, Day 7 nudge if no shares, Day 30 thank-you for any successful conversions.
- Anti-fraud rules (self-referrals blocked via email/IP match, duplicate accounts flagged).

### Step 5 — A/B variations + optimization

Test variables in priority order:
1. Trigger moment (try alternatives, measure share rate per trigger).
2. Incentive amount (10%, 30%, 50% of LTV — find the elbow).
3. Share-mechanism mix (in-product only vs. in-product + personalized link).
4. Messaging copy (the referrer's invitation language).
5. Reward delivery cadence (instant vs. milestone-locked).

---

## Worked example — Genesys-internal first

**Use case:** Genesys customers (GTM Engineers running our skills) refer peers from the niche.

- **Trigger moment:** when a Genesys customer has run 3+ skill-orchestrator chains over 30 days (clear sustained-use signal).
- **Share mechanism:** in-product banner ("Refer a GTM Engineer — both get $100 credit") + personalized link with the customer's name baked in.
- **Incentive:** double-sided $100 (referrer gets $100 credit on next renewal; referred gets $100 off first month).
- **Cost check:** assuming average LTV $5k, CPA target = $1.5k. Total $200 program cost = 4% of LTV. Sustainable.
- **Anti-fraud:** new account email must differ from existing customer's email + work-domain check.

After 90 days, productize to clients with viral-loop potential (ClientCo member→member, ClientCo adviser→adviser).

---

## {Client / Genesys} referral program design

### Trigger moment
- Chosen: {moment}
- Why: {evidence the moment correlates with willingness to share}
- Instrumentation: {analytics event}

### Share mechanism
- Tier 1 (in-product): {design}
- Tier 2 (personalized link): {design}
- Tier 3 (email referral): {design}

### Incentive structure
- Type: {single / double / tiered}
- Amount: {value, referrer + referred}
- LTV check: {CPA / LTV ratio}

### Launch checklist
- [ ] Trigger event instrumented
- [ ] Share mechanism live
- [ ] Incentive backend automated
- [ ] Attribution + tracking
- [ ] Email sequence (Day 0, 7, 30)
- [ ] Anti-fraud rules

### A/B test queue
- Test 1: {variable}
- Test 2: {variable}

### KPIs
- 30-day target: {shares / conversions / referred LTV}
- 90-day target: {compounding rate, churn delta}
```

---

## Anti-patterns

- ❌ Trigger on signup or trial-start. Hollow share.
- ❌ Referral code-only program. Conversion stays at 0.5–1%.
- ❌ Single-sided when the referred customer needs a reason to click.
- ❌ Incentive cost > 50% of LTV. Drains margin.
- ❌ Manual reward delivery. Friction kills compounding.
- ❌ No anti-fraud — self-referrals erode trust + tank CPA math.

---

## Integration with other skills

- **Upstream:** `/icp-behavioural` defines who refers and why; `/product-messaging` defines the value-prop the referrer sells.
- **Downstream:** `/lifecycle-marketing` runs the 3-touch email sequence; `/analytics-tracking-plan` instruments the trigger + attribution events.
- **Companion:** `/ab-testing` runs the optimization tests after launch.

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/referrals/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/referrals/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice. Lane B: Genesys-internal first deployment.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

