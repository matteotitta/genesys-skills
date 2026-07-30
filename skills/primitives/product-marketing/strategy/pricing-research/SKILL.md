---
name: pricing-research
version: '1.0'
last_updated: 2026-03-25
author: genesys-growth
description: Conducts structured pricing research using Van Westendorp, Gabor-Granger, and competitive pricing intelligence
  methods. Produces willingness-to-pay data, optimal price point ranges, and price sensitivity analysis. Triggers on "pricing
  research", "willingness to pay", "Van Westendorp", "price sensitivity", "pricing survey", "WTP research", or "optimal price
  points". Feeds into pricing-strategy for packaging and monetization decisions. NOT for tier design or packaging — use pricing-strategy
  instead. This skill gathers evidence; pricing-strategy makes packaging decisions.
goal: Conducts structured pricing research using Van Westendorp, Gabor-Granger, and competitive pricing intelligence methods.
outcome: Conducts structured pricing research using Van Westendorp, Gabor-Granger, and competitive pricing intelligence methods.
  Produces willingness-to-pay data, optimal price point ranges, and price sensitivity analysis. Triggers on "pricing research",
  "willingness to pay", "Van Westendorp", "price...
primitive: product-marketing
sub_primitive: strategy
ontology_type: pricing-strategy
review_gate: 2
inputs:
  required: []
  recommended:
  - icp-research
  - competitor-research
outputs:
- type: pricing-research
  feeds_into:
  - pricing-strategy
depends_on: []
feeds_into:
- pricing-strategy
owned_by_agent: pmm
mcps_used: []
push_targets:
- gdrive
- notion
triggers:
  slash_commands:
  - /pricing-research
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Pricing research skill

Gather evidence-based pricing data through structured methodologies. Produces willingness-to-pay ranges, price sensitivity curves, and competitive pricing intelligence that feed into `/pricing-strategy` for packaging decisions.

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| Product/feature to price | Yes | User specifies what's being priced |
| ICP profile | Recommended | `/icp-research` output |
| Competitor pricing data | Recommended | `/competitor-research` output or manual gathering |
| Current pricing (if exists) | Optional | User provides existing pricing |
| Target sample size | Optional | Default: 30-50 respondents per segment |

## Scope boundary

This skill produces **research data**. It answers "what are people willing to pay?" and "what does the market charge?"

It does NOT answer:
- How to package features into tiers (that's `/pricing-strategy`)
- How to structure a freemium vs. trial model (that's `/pricing-strategy`)
- How to design a pricing page (that's `/landing-page-copy`)
- Whether to do usage-based vs. seat-based (that's `/pricing-strategy` informed by this research)

Think of this as the evidence gathering that makes pricing-strategy decisions defensible instead of gut-feel.

## Methodologies (overview)

Four methodologies are documented in `references/methodologies.md`. Choose by goal:

| Methodology | Best for | Sample size | Output |
|-------------|----------|-------------|--------|
| **1. Van Westendorp PSM** | Establishing acceptable price range from scratch | 30-50 per segment | PMC / OPP / IDP / PME points + range |
| **2. Gabor-Granger** | Testing a shortlist of candidate prices | 30-50 per segment | Demand curve + revenue-max price |
| **3. Conjoint analysis** | Pricing multi-feature products with modular packaging | 200+ | Per-attribute utility incl. price |
| **4. Competitive intel** | Mapping the market before primary research | Desk research | Competitive pricing matrix |

**Default starting point for B2B SaaS under $10M ARR:** Van Westendorp + Gabor-Granger + competitive intel. That's 80% of the insight at 20% of the cost. Reach for conjoint only when packaging is genuinely complex.

### Van Westendorp — the four questions (most-used pattern)

Present in this exact order:

1. **Too cheap:** "At what price would you consider [product] to be so inexpensive that you'd question its quality?"
2. **Cheap (good value):** "At what price would you consider [product] to be a bargain — a great buy for the money?"
3. **Expensive (getting pricey):** "At what price would you consider [product] to be starting to get expensive — not out of the question, but you'd have to think about it?"
4. **Too expensive:** "At what price would you consider [product] to be so expensive that you'd never consider buying it?"

The four cumulative-distribution intersections produce **PMC** (point of marginal cheapness), **PME** (point of marginal expensiveness), **OPP** (optimal price point), and **IDP** (indifference price point). Acceptable range = PMC→PME. Optimal zone = OPP→IDP. Full curve plotting + sample survey + practical notes: `references/methodologies.md`.

### When to use Gabor-Granger instead

You already have 3-5 candidate price points; you need a demand curve, not just a range; you want to estimate revenue impact of price changes; you're testing a price increase on existing customers.

### Competitive pricing intel — do this first

Desk research before primary research, so you have context for interpreting WTP data. Public pricing pages + review sites + sales intelligence + indirect signals (ARPU implied from customer count + revenue). Track price points per tier, feature gates, billing options, pricing model, discounting signals.

---

## Output template

The skill produces a pricing research report with these sections:

### 1. Research summary

- Methodology used (Van Westendorp, Gabor-Granger, or both)
- Sample size and composition
- Segments analyzed
- Data collection period
- Confidence level in findings

### 2. Willingness-to-pay findings

**Van Westendorp results (if used):**

| Metric | Value |
|--------|-------|
| Point of marginal cheapness (PMC) | $X |
| Optimal price point (OPP) | $X |
| Indifference price point (IDP) | $X |
| Point of marginal expensiveness (PME) | $X |
| Acceptable price range | $X - $X |
| Optimal pricing zone | $X - $X |

**Gabor-Granger results (if used):**

| Price point | % willing to buy | Implied revenue index |
|-------------|-----------------|----------------------|
| $X | X% | X |

### 3. Competitive pricing landscape

- Competitive pricing matrix (filled in)
- Market positioning map (price vs. feature completeness)
- Pricing model trends in the category
- Gaps and white space

### 4. Segment-level analysis

Break out findings by ICP segment. Different buyer types will have different WTP.

| Segment | Acceptable range | Optimal zone | Key value drivers |
|---------|-----------------|--------------|-------------------|
| SMB | $X - $X | $X - $X | [What they value most] |
| Mid-market | $X - $X | $X - $X | [What they value most] |
| Enterprise | $X - $X | $X - $X | [What they value most] |

### 5. Price range recommendation

Based on the research data, provide:

- **Recommended price range** with rationale
- **Risk assessment** for pricing at different points within the range
- **Segment-specific pricing signals** (where different segments diverge)
- **Data gaps** that should be filled before making final pricing decisions
- **Confidence level** per finding: `[VERIFIED]`, `[INFERRED]`, or `[ESTIMATED]`

This output feeds directly into `/pricing-strategy` for packaging, tier design, and go-to-market pricing decisions.

---

## Anti-patterns

**Don't do these:**

- Asking WTP questions without qualifying respondents first. Non-buyers will skew your data low.
- Blending segments in analysis. Enterprise and SMB WTP data mixed together is useless.
- Treating survey data as ground truth. WTP research shows what people SAY they'd pay, not what they'll actually pay. Real prices are typically 10-20% lower than stated WTP.
- Ignoring competitive context. WTP in a vacuum means nothing. Buyers compare.
- Running pricing research once and treating it as permanent. Markets shift. Re-run annually or when entering new segments.
- Skipping value anchoring. If respondents don't understand the value before you ask about price, their answers are noise.
- Using this skill to make packaging decisions. This is research. Packaging is strategy. Use `/pricing-strategy` for that.
- Small sample overconfidence. Under 30 respondents, treat everything as directional, not definitive.

---

## Reference files

| File | Purpose |
|------|---------|
| `references/methodologies.md` | Full deep-dive on Van Westendorp, Gabor-Granger, conjoint, and competitive intel — survey templates, plotting, tools, sample sizes |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
