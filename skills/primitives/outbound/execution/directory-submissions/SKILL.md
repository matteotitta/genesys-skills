---
name: directory-submissions
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Plans and executes systematic product listings across directories and review platforms (Product Hunt, BetaList, G2, Capterra, AI-engine citation surfaces, niche verticals). Produces a 13-tier sequenced submission schedule, Product Hunt 3-week warm-up + launch-day playbook, 10-in-30 reviews framework, and per-tier positioning variants. Triggered by "directory submissions", "Product Hunt launch", "G2 reviews protocol", "directory strategy", "where should we list our product". NOT for general SEO backlinks — use /seo-strategy for organic.
goal: Build compounding backlink and discovery foundations via systematic product listings in the right order with differentiated positioning per directory type.
outcome: Produces (1) readiness assessment, (2) tier selection with rationale, (3) phased submission schedule across 13 tiers, (4) per-tier positioning variants, (5) Product Hunt 3-week prep timeline + launch-day playbook, (6) 10-in-30 reviews protocol for G2/Capterra, (7) KPI targets + submission tracker.
primitive: outbound
sub_primitive: execution
ontology_type: launch-plan
review_gate: 2
inputs:
  required: []
  recommended:
  - product-messaging
  - positioning
  - company-context
  - aeo-content
- type: launch-plan
  feeds_into:
  - product-launch
depends_on: []
- product-launch
owned_by_agent: growth
mcps_used:
- exa
- firecrawl
- gdrive
triggers:
  slash_commands:
  - /directory-submissions
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /directory-submissions — 13-tier launch + listing playbook

Plan and execute systematic product listings across directories, review platforms, and AI-citation surfaces with the right sequence and positioning per tier. Closes the launch loop alongside `/product-launch` and `/aeo-content`.

---

## When to invoke

- A product is launching (new or major refresh) and needs a directory rollout plan.
- A client's directory presence is sparse and a structured audit + sequenced fill-in is needed.
- A Product Hunt launch is on the calendar and the 3-week warm-up needs scoping.
- G2 / Capterra reviews are absent or stalled and the 10-in-30 protocol needs deploying.

Do NOT invoke when:
- The destination pages aren't ready (comparison pages, alternative pages, ROI calculator) — get foundations in place first.
- The product hasn't hit its first 100 users — directory submissions before product-market signal wastes the launch window.

---

## The 3 hard rules

1. **Foundation before submission.** Destination pages (comparison, alternative, "vs.", ROI calculator, case studies) must exist before directories link to them. Otherwise link equity flows to a generic homepage that doesn't convert.
2. **Destination pages before directories.** Build the page the directory links to first; submit second. Reversed order leaves directory traffic landing on stub pages.
3. **Positioning varies by directory type.** What sells on Product Hunt (founder story + visual demo) does not sell on G2 (peer validation + feature depth) or on AI-engine citation pages (factual + comparison-honest). One positioning copy doesn't fit all.

---

## The 13-tier submission taxonomy

Submit in tier order. Each tier has different audience, mechanics, and positioning needs.

| Tier | Examples | Audience | Positioning angle |
|---|---|---|---|
| 1 — Flagship launch | Product Hunt, BetaList | Early adopters, makers | Founder story + 60-sec demo + community-relevant hook |
| 2 — General SaaS directories | SaaSHub, AlternativeTo, GetApp | Tool researchers | Feature-by-feature comparison + screenshots |
| 3 — Review platforms | G2, Capterra, TrustRadius, Software Advice | Buyers in evaluation | Peer reviews-first; 10-in-30 protocol applies |
| 4 — Comparison hubs | AlternativeTo, Slant, StackShare | Buyers comparing options | "How we differ from X" angles |
| 5 — Investor / startup databases | Crunchbase, F6S, AngelList | Investors, partner-seekers | Traction + funding-friendly positioning |
| 6 — Tech newsletter directories | TLDR, Indie Hackers, Hacker News listings | Niche operators | Founder voice + community participation |
| 7 — AI-engine citation surfaces | Perplexity-cited domains, ChatGPT-cited resources | AI-search audience | Honest comparison + structured data + GEO-optimized content |
| 8 — Industry-specific directories | (e.g., FinTech: Finovate, FintechWeekly; AdTech: AdAge tool lists) | Vertical operators | Industry-specific use case + integrations |
| 9 — Geographic directories | LocalBusiness directories, country-specific (e.g., StartupBlink UK, France Digitale) | Local market entrants | Local language + regulatory compliance |
| 10 — Maker / no-code platforms | Bubble showcase, Webflow showcase, Notion templates | Builder community | Behind-the-scenes build + remix angle |
| 11 — Integration ecosystem | Zapier App Directory, Make Integromat, Slack App Directory | Workflow-builders | Integration value + use case |
| 12 — Conference / event directories | Sponsorship logos, attendee directories | In-person network | Event-relevant offer |
| 13 — Niche vertical directories | Targeted to client niche (e.g., for FinTech: AdviserTech directories like AdviserSoftware.com) | Niche buyers | Niche-specific value prop |

---

## Sharp numbers (cite-verified from source, MIT)

| Metric | Number |
|---|---|
| Product Hunt: video uplift vs. no-video posts | 2.7× more upvotes |
| Product Hunt: optimal launch window | 12:01 AM Pacific Tuesday–Thursday only |
| Comparison / alternative page conversion rate | 5–15% vs. 0.5–2% generic content |
| AI-referred traffic conversion uplift vs. traditional search | 6–27× higher |
| Template-gallery LTV potential (e.g., Typeform) | Up to $3M/year |
| G2 / Capterra reviews protocol target | 10 reviews from 20 asks in 30 days post-launch |

---

## Product Hunt 3-week warm-up timeline

### Week –3 (3 weeks before launch)
- Identify and contact hunter (someone with 100+ followers + history of launching credibly).
- Build email list of ~200 "launch supporters" — opt-in commitments to upvote on day-of.
- Prepare assets: 240×240 logo, 4–6 product screenshots, 60-sec demo video (with captions).
- Draft 4 angle variants for the launch tagline; A/B-test internally.

### Week –2
- Brief launch supporters via email (no early sharing of the link — Product Hunt penalizes).
- Build the comments-pack: 6–10 thoughtful, on-topic responses to expected questions.
- Schedule social posts for launch day (LinkedIn, X, internal Slack-share with team).
- Test the demo video on mobile + desktop; fix any rendering bugs.

### Week –1
- Final hunter call — confirm timing, agree on the post title.
- Get 3 advance "first commenters" lined up (founders, advisors, customers) for the first hour.
- Schedule the launch post draft for 11:50 PM Pacific the night before.

### Day 0 — Launch day
- 12:01 AM Pacific (Tue–Thu only). Hunter posts the product.
- 12:05 AM — first commenter posts the lead comment.
- 12:10 AM — share to email list + Slack + Twitter + LinkedIn.
- 1:00 AM – 4:00 AM PT — respond to every comment within 15 minutes.
- 7:00 AM – 11:00 AM PT — follow-up wave to email list ("we're at #X — final push").
- 11:59 PM PT — post a thank-you comment on the listing.

### Day +1 / +2 — Post-launch
- DM new followers (genuine, not template).
- Convert top commenters to G2 / Capterra reviewers (start the 10-in-30 protocol).
- Repurpose launch content into LinkedIn carousel + newsletter.

---

## The 10-in-30 reviews framework

Goal: 10 published reviews within 30 days of launch from 20 review-asks.

Mechanics:
1. **Identify 20 customers.** Tenure ≥ 60 days, NPS ≥ 8, recent positive interaction. Mix sizes/segments.
2. **One-week cadence.** 5 asks/week × 4 weeks. Don't bulk-ask.
3. **Personal ask format.** Founder or CS owner messages 1:1 (email or LinkedIn). Template ≠ personal — write each.
4. **Include the link.** Pre-filled review URL (G2 supports direct review URLs).
5. **Offer reciprocity.** Small thank-you (swag, Amazon gift card under $25 — within G2 policy).
6. **Follow up at day 4.** One nudge max.

Expected conversion: 50% asks → reviews (10/20). If under 5/20 after week 1, the ask copy is wrong — rewrite.

---

## GEO / AI-citation optimization (Tier 7)

AI engines (Perplexity, ChatGPT, Claude, Google AI Overviews) cite domains they find authoritative and structurally rich. To improve citation eligibility:

- Single `<h1>` per page (matches `/schema-markup` rule).
- FAQ schema on every product / comparison / pricing page (per `/schema-markup`).
- Comparison tables in markdown / HTML format (parseable, not screenshots).
- Honest "Who it's for" sections on comparison pages (the `/aeo-content` pattern absorbed from I11).
- Track AI-engine citations weekly via Brand Radar / Profound / AirOps (per `/aeo-strategy`).

---

## {Product / Client} directory submissions — phase 1

### Readiness check
- Destination pages: ✅ / ⚠️ / ❌ (which gaps to fill first)
- Product-market signal: ✅ / ⚠️ (≥100 users / not yet)
- Positioning + messaging locked: ✅ / ⚠️

### Tier selection
- Tier 1 (flagship): Product Hunt, BetaList — yes/no, with reasoning
- Tier 2–13: per-tier yes/no with rationale

### Phased schedule (weekly)
- Week 1: {tiers, with deadlines}
- Week 2: …
- Week N: …

### Per-tier positioning variants
- Product Hunt: {60-word pitch}
- G2: {feature-anchored description}
- AlternativeTo: {comparison angle}
- AI-citation surfaces: {honest-comparison pattern}

### Product Hunt prep (if Tier 1)
- 3-week timeline checklist (as above)
- Asset list with status

### Reviews protocol (if Tier 3)
- 20-customer asks list
- Weekly cadence + ask template

### KPIs
- Launch-day target: top-N of day on PH
- 30-day target: 10 G2/Capterra reviews
- 90-day target: N AI-engine citations (via Brand Radar tracking)
```

---

## Integration with other skills

- **Upstream:** `/positioning` + `/product-messaging` provide the per-tier positioning variants; `/aeo-content` provides destination pages (comparison, "vs.", alternative); `/schema-markup` ensures structured-data eligibility for Tier 7.
- **Downstream:** Feeds `/product-launch` orchestration; reviews protocol feeds `/lifecycle-marketing` (the customer-reviewer relationship continues post-review).
- **Companion:** `/aeo-strategy` plans which citation surfaces to target; this skill executes against them.

---

## Anti-patterns

- ❌ Submit before destination pages exist.
- ❌ Same positioning copy across all 13 tiers.
- ❌ Product Hunt launch with no warm-up — typical result: <50 upvotes, lost launch window.
- ❌ Bulk-ask 20 customers for G2 reviews on the same day. Reads as a campaign; conversion tanks.
- ❌ Hidden / paid reviews. G2 and Capterra enforce. Manual-action territory.
- ❌ Submit to every tier on day 1 — exhaust attention budget; later tiers get half-prepped submissions.

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/directory-submissions/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/directory-submissions/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice and integrated with our existing launch chain.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

