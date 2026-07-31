---
name: paid-campaign-strategy
version: '1.0'
last_updated: 2026-03-23
author: genesys-growth
description: Develops paid advertising strategy across Google Ads and LinkedIn Ads for B2B SaaS. Produces campaign structure,
  budget allocation by channel and funnel stage, audience targeting strategy, bid strategy recommendations, and a measurement
  plan with KPIs. Depends on product-messaging and icp-behavioural as required inputs. Feeds into google-ads-copy, linkedin-ads-copy,
  and ad-creative-brief as the upstream strategy layer for all paid execution. Triggered by "paid ads strategy", "campaign
  structure", "ad budget", "PPC plan", "paid acquisition strategy", or "media plan". NOT for auditing existing campaigns —
  use /paid-ads-audit instead.
goal: Develops paid advertising strategy across Google Ads and LinkedIn Ads for B2B SaaS.
outcome: Develops paid advertising strategy across Google Ads and LinkedIn Ads for B2B SaaS. Produces campaign structure,
  budget allocation by channel and funnel stage, audience targeting strategy, bid strategy recommendations, and a measurement
  plan with KPIs. Depends on product-messaging and...
primitive: paid-marketing
sub_primitive: strategy
ontology_type: launch-plan
review_gate: 2
inputs:
  required:
  - product-messaging
  - icp-behavioural
  recommended:
  - competitor-research
  - funnel-strategy
  - company-context
- type: paid-campaign-strategy
  feeds_into:
  - google-ads-copy
  - linkedin-ads-copy
  - ad-creative-brief
depends_on:
- product-messaging
- icp-behavioural
- ad-creative-brief
- google-ads-copy
- linkedin-ads-copy
owned_by_agent: paid
mcps_used: []
- gdrive
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Paid Campaign Strategy

Design paid advertising campaign architecture for B2B SaaS. Determines which campaigns to run, budget allocation, targeting strategy, and account structure across Google Ads and LinkedIn Ads. This is the upstream skill that feeds all copy and creative skills.

**Live LinkedIn Ads data (optional):** when the `linkedin-ads` MCP is authenticated, ground the strategy in the account's actual performance — read current spend, CPL, audience response, and top creatives (`get_campaign_performance`, `get_audience_demographics`, `compare_performance`) before allocating budget or setting KPI targets. Reads are free; write tools gated by `.claude/rules/linkedin-ads-spend.md`. See `.claude/mcp/linkedin-ads/README.md`.

---

## Process Flowchart

```
┌──────────────────────────────────────────────────────────────┐
│ PAID CAMPAIGN STRATEGY PROCESS │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ INPUT VALIDATION │
│ Required: │
│ □ product-messaging (value props, differentiators) │
│ □ icp-behavioural (personas, firmographics, pain points) │
│ Optional: competitor-research, funnel-strategy, company-context│
│ □ Monthly budget range │
│ □ Campaign objective (awareness / leads / demos / trials) │
│ → If missing: Suggest upstream skills first │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 1: PLATFORM SELECTION │
│ Step 1.1: Apply platform selection matrix │
│ Step 1.2: Determine primary vs support platform │
│ Step 1.3: Allocate budget split across platforms │
│ → Output: Platform recommendation with rationale │
│ ✓ Checkpoint: Platform(s) selected with budget split │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 2: CAMPAIGN ARCHITECTURE │
│ Step 2.1: Google Ads — select from 5-pillar model │
│ Step 2.2: LinkedIn Ads — select funnel stages │
│ Step 2.3: Map campaigns to objectives and budget tiers │
│ Step 2.4: Define ad group structure per campaign │
│ → Output: Campaign list with objectives and budget │
│ ✓ Checkpoint: Every campaign has objective + budget + KPI │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 3: TARGETING + TRACKING │
│ Step 3.1: Map ICP → Google keyword strategy │
│ Step 3.2: Map ICP → LinkedIn audience filters │
│ Step 3.3: Define UTM taxonomy │
│ Step 3.4: Define negative keyword seed list (Google) │
│ Step 3.5: Set KPI targets per campaign │
│ → Output: Targeting specs + UTM structure + KPI targets │
│ ✓ Checkpoint: Every campaign has targeting + tracking defined │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ SELF-EVALUATION │
│ □ Budget allocation totals to 100% │
│ □ Every campaign has objective, budget, targeting, KPI │
│ □ Platform selection justified by ICP signals │
│ □ Negative keywords included for Google │
│ □ UTM taxonomy defined and consistent │
│ □ Timeline accounts for 60-90 day B2B learning window │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ CHAIN SUGGESTIONS │
│ → google-ads-copy (generate RSA copy per campaign) │
│ → linkedin-ads-copy (generate ad copy per funnel stage) │
│ → ad-creative-brief (visual direction for designers) │
└──────────────────────────────────────────────────────────────┘
```

---

## The Iron Law

**NO CAMPAIGN STRATEGY WITHOUT UPSTREAM INPUTS.**

Campaign strategy requires product-messaging and icp-behavioural. Targeting must trace to ICP firmographics. Value props must come from messaging framework.

**No exceptions:**

- "I know the ICP" → Knowledge ≠ research. Run icp-behavioural or use existing.
- "Just run Google Ads" → Without campaign architecture you'll burn budget on low-intent traffic.
- "Start with $500/month" → Below minimum viable test budget. Be honest about what's achievable.
- "We need leads fast" → B2B SaaS needs 60-90 days for meaningful data. Set expectations.

---

## Platform Selection Matrix

| Signal | Google Ads | LinkedIn Ads | Both |
|--------|-----------|-------------|------|
| High-intent search volume exists | ✓ Primary | Support | ✓ |
| Enterprise ICP (Director+) | Support | ✓ Primary | ✓ |
| SMB/mid-market ICP | ✓ Primary | Awareness only | Depends |
| Competitor bidding opportunity | ✓ Primary | N/A | Google only |
| ABM motion | Remarketing only | ✓ Primary | ✓ |
| Product-led growth | ✓ Primary | TOFU awareness | ✓ |
| Sales-led motion | ✓ BOFU | ✓ Full-funnel | ✓ |

---

## Google Ads: 5-Pillar B2B SaaS Campaign Model

| Campaign | Purpose | Keywords | Ad group structure |
|----------|---------|----------|--------------------|
| **Brand** | Protect branded terms | `[brand]`, `[brand] pricing`, `[brand] reviews` | 1 ad group per brand term cluster |
| **Competitor** | Capture evaluators | `[competitor] alternative`, `[competitor] vs`, `[competitor] pricing` | 1 ad group per competitor (never mix) |
| **High-intent product** | Solution seekers | `[category] software`, `[use case] tool`, `[function] platform` | 1 ad group per product feature/use case |
| **Problem-aware** | Earlier-stage buyers | `how to [pain point]`, `why is [process] slow` | 1 ad group per pain point theme |
| **Remarketing** | Nurture long sales cycles | Audience-based (no keywords) | 3 ad groups: educational (1-7d), case study (7-30d), demo CTA (30-90d) |

---

## LinkedIn Ads: Full-Funnel Campaign Model

| Stage | Objective | Formats | Content type | Audience size |
|-------|-----------|---------|-------------|---------------|
| **TOFU** | Brand awareness / engagement | Single Image, Video, Thought Leader, Document | Industry insights, POV content, data reports | 30K-150K |
| **MOFU** | Website visits / engagement | Carousel, Document, Single Image | Product walkthroughs, comparison guides, webinars | 10K-50K |
| **BOFU** | Lead gen / conversions | Single Image + Lead Gen Form, Conversation Ads | Demo requests, free trials, case studies | 5K-30K |
| **Retargeting** | Conversions | Single Image, Conversation Ads | Social proof, urgency, direct CTA | Site visitors + engagers |

---

## Budget Tier Recommendations

| Budget | Google Ads | LinkedIn Ads | Strategy |
|--------|-----------|-------------|----------|
| $0-5K/mo | High-intent product + brand only | Skip or minimal TOFU | Google-first, prove ROI |
| $5-15K/mo | + Competitor + remarketing | $3-5K TOFU + BOFU | Add LinkedIn for awareness |
| $15-40K/mo | Full 5-pillar | Full-funnel (TOFU/MOFU/BOFU) | Balanced dual-platform |
| $40K+/mo | + Performance Max, DSA | + ABM, Conversation Ads | Expand formats + verticals |

---

## CAC Benchmarks (B2B SaaS Reference)

| Channel | CAC range | MQL→SQL rate | Notes |
|---------|-----------|-------------|-------|
| Google Search | $80-250 | 15-25% | Highest intent, best for BOFU |
| LinkedIn Ads | $150-400 | 10-20% | Higher CPCs but higher lead quality |
| Blended target | <$300 | >15% | Adjust based on ACV |

**Attribution model:** W-Shaped (40-20-40) for hybrid PLG/Sales-Led. Last-Touch for direct response assessment.

---

## Targeting: ICP → Ad Platform Mapping

### Google Ads
- Map ICP pain points → keyword themes for problem-aware campaigns
- Map competitor landscape → competitor campaign keyword lists
- Map product features → high-intent product keyword groups
- Negative keyword seed list: "free", "open source", "jobs", "careers", "salary", "tutorial", "course", "login", "support"

### LinkedIn Ads
- Map ICP firmographics → company size + industry filters
- Map champion persona → job titles + seniority + function
- Map buying committee → multiple job function combinations
- Matched Audiences: CRM upload for ABM, website visitors for retargeting
- Lookalike expansion: 1-5% based on best-fit customers

---

## UTM Taxonomy

```
utm_source={channel} // linkedin, google
utm_medium={type} // cpc, display, social
utm_campaign={campaign-id} // q1-2026-google-competitor-saturn
utm_content={variant} // ad-variant-a
utm_term={keyword} // [Google only]
```

**Naming convention for campaigns:**
`{quarter}-{year}-{platform}-{campaign-type}-{detail}`

Examples:
- `q1-2026-google-competitor-saturn`
- `q1-2026-linkedin-tofu-industry-insights`
- `q1-2026-google-product-suitability-reports`

---

## Paid Campaign Strategy — [Client Name] — [Date]

### Platform selection
[Rationale based on ICP signals and budget]

### Campaign architecture

| Campaign | Platform | Type | Objective | Monthly budget | KPI target |
|----------|----------|------|-----------|---------------|------------|
|... |... |... |... | $X | CPL $X |

### Budget allocation
| Platform | Amount | % of total |
|----------|--------|-----------|
| Google Ads | $X | X% |
| LinkedIn Ads | $X | X% |
| **Total** | **$X** | **100%** |

### Targeting specs
[Per-campaign targeting details]

### UTM taxonomy
[UTM structure with examples]

### Negative keyword seed list (Google)
[Keyword list]

### KPI targets
[Per-campaign KPI targets with benchmarks]

### Timeline
- Weeks 1-2: Account setup, tracking verification, initial campaigns launch
- Weeks 3-8: Learning phase, gather data, weekly search term reviews
- Weeks 9-12: Optimize based on data, scale winning campaigns
- Quarterly: Full audit (→ paid-ads-audit)
```

---

## Self-Evaluation Checklist

- [ ] Budget allocation totals to 100%
- [ ] Every campaign has: objective, budget, targeting, KPI target
- [ ] Platform selection justified by ICP signals (not assumptions)
- [ ] Google negative keyword seed list included
- [ ] UTM taxonomy defined and consistent across platforms
- [ ] Attribution model selected
- [ ] Timeline accounts for 60-90 day B2B learning window
- [ ] No invented metrics or benchmarks (use ranges from research)

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
