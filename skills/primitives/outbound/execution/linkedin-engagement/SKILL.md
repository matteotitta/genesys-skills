---
name: linkedin-engagement-prospects
version: '1.1'
last_updated: 2026-05-01
author: genesys-growth
description: Converts LinkedIn post engagement (likes, comments, reshares) into a deduplicated, enriched prospect list. Uses
  the Apify LinkedIn actor MCP to pull engagers from a post URL, dedupes across multiple posts, enriches via /deepline-enrich,
  and outputs a CSV with engagement context. Triggered by "prospects from this LinkedIn post", "engagers on my post", "who
  liked my post", "turn this post into a prospect list", "LinkedIn engagement prospects", or "scrape engagers from this URL".
  NOT for content analysis ("what did they say about my post" is a different question), pipeline qualification (that's /lead-scoring),
  or contact-discovery from scratch (that's /build-tam).
goal: Converts LinkedIn post engagement (likes, comments, reshares) into a deduplicated, enriched prospect list.
outcome: Converts LinkedIn post engagement (likes, comments, reshares) into a deduplicated, enriched prospect list. Uses the
  Apify LinkedIn actor MCP to pull engagers from a post URL, dedupes across multiple posts, enriches via /deepline-enrich,
  and outputs a CSV with engagement context. Triggered by...
primitive: outbound
sub_primitive: execution
ontology_type: outreach-sequence
review_gate: 1
inputs:
  required: []
  recommended:
  - deepline-enrich
  - icp-research
  - lead-scoring
- type: signal-enriched-account-list
  feeds_into:
  - lead-scoring
  - outreach-emails
  - abm-campaign
  - niche-signal-discovery
depends_on: []
- abm-campaign
- lead-scoring
- niche-signal-discovery
- outreach-emails
owned_by_agent: content
mcps_used:
- apify
- deepline
- gdrive
- notion
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: medium
---

# LinkedIn engagement → prospects

Turn LinkedIn post engagement into an enriched prospect list. Input a post URL (or several), pull engagers via Apify, dedupe across posts, run `/deepline-enrich` for emails, and output a CSV with engagement context ready for outbound.

**Adopted from:** Extruct GTM skills (via `/steal` 2026-04-21). Real trigger: posts that go well attract the right ICP, and the engagement itself is a signal that the person is at least category-aware.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`outbound-research-hygiene.md`](../../../../../rules/outbound-research-hygiene.md) — dated signals (engagement date must be ≤90 days), no stale references
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in linkedin-engagement-prospects |
|---|---|---|
| **R1** | Source placement (three layers) | Engagement CSV is **internal-reference** (input to outbound). Inline metadata (post URL, engagement type, date) stays — the next skill (`/outreach-emails`) reads it. |
| **R3** | Product-update tone | When the downstream message references our content, frame as "I posted about X" not "we are thrilled to share." |
| **R6** | CTA hierarchy | DM follow-ups to engagers default to discovery-call or trial primary — never blog as primary. Engagement already showed they saw our content. |
| **R9** | Action-oriented section names | "Pull the engagers / Dedupe across posts / Enrich for email / Hand off to outbound" — verb-led. |

---

## Core philosophy — voice-locked

A like on your LinkedIn post is **not** the same as a marketing-qualified lead — but it is a signal that (a) the person saw your content, (b) engaged enough to click, and (c) self-selected into the topic. That beats cold sourcing for top-of-funnel heat.

This skill treats content engagement as a **first-touch signal**, not a qualification. Output still flows into `/lead-scoring` to decide if the signal is strong enough to act on, and `/deepline-enrich` to validate contact data before any outreach.

What this skill is NOT:
- It's not "engagement equals interest" — some engagement is politeness, networking, or bots
- It's not a qualification step — it feeds qualification, doesn't replace it
- It's not a one-click outbound tool — it produces a prospect list, which then needs `/lead-scoring` + `/outreach-emails`

---

## When to use

### Run this skill when

- A LinkedIn post on your own profile got 50+ engagements and you want to action them
- A client's founder has a post performing well and the client wants to capitalize
- Multiple related posts over a time window need to be dedupe-merged into one prospect list
- A competitor's post attracted the ICP (ethical competitive engagement play)
- You want to build a first-party prospect list without paid enrichment tools doing the discovery

### Do NOT use when

- The post has fewer than 20 engagements → manual review is faster
- The post is off-topic for your category → engagement quality will be low, signal is weak
- You want to scrape LinkedIn profiles more broadly → use `/build-tam`
- You want to understand *what people said in comments* semantically → that's analysis, not prospecting

---

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **LinkedIn post URL(s)** | One or more post URLs | Yes |
| **ICP context** | Client / engagement this list is for | Yes |
| **ICP doc path** | For automated filtering | Recommended |
| **Engagement type filter** | Likers / commenters / both (default: both) | Optional |
| **Time window** | Default: all available | Optional |

---

## Process

**Six-phase flow:** Input validation → Apify scrape → Dedupe (LinkedIn URL > name+company) → ICP filter (with reasons logged) → Handoff to `/deepline-enrich` → Output CSV with engagement context. Step-by-step + MCP integration in the premium reference.

---

## Modes — engagement, post-search, profile-feed, company-feed

The skill now supports four modes (added 2026-05-01 via `/steal`):

| Mode | Purpose | Default actor |
|------|---------|---------------|
| **Mode 1 — Engagement scraping** | Convert post engagement → prospect list (the original use case) | `apimaestro/linkedin-post-comments-replies-engagements-scraper-no-cookies` ($5/1k) |
| **Mode 2 — Topic search** | Find posts about a topic + their engagement | `harvestapi/linkedin-post-search` ($1.50/1k) |
| **Mode 3 — Profile feed** | Pull all posts from a target profile in date range | `harvestapi/linkedin-profile-posts` ($1.50/1k) |
| **Mode 4 — Company feed** | Pull all posts from a target company page in date range | `harvestapi/linkedin-company-posts` ($1.50/1k) |

Full actor matrix + budget alts + vendor-family risk note in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent engagers** — if Apify returns 40 engagers, report 40, not 50
2. **Don't invent companies** — if engager headline lacks company, mark as `[company not in headline]` and attempt `linkedin-url-lookup` rather than guessing
3. **Don't infer reaction sentiment beyond the literal reaction** — a "like" is a like, not a buying signal
4. **Flag private/deleted profiles** — if a profile 404s during enrichment, mark and skip rather than fabricating data
5. **Don't promise email coverage** — Deepline waterfall typically lands 40-70% emails; report actuals, not projections

---

## Quality

Pre-delivery checks cover coverage (all phases ran, filtered-engagers logged), quality (multi-post counts preserved, recency captured, no inflated reaction sentiment), and cost discipline (Apify + Deepline gates respected). Common-mistakes table (treating likes as MQLs, skipping ICP filter, vendor-family swap) + worked example (3-post AI compliance harvest, 287 unique → 158 ICP-fit → 102 valid emails) + anti-examples + quality gate (Apify success rate, dedupe accuracy, email find rate ≥40%) in the premium reference.

---

## Credit Gates — voice-locked

All Apify actor calls flow through `.claude/rules/apify-credits.md`. Deepline overlay uses `/deepline-enrich`'s gate per `.claude/rules/apollo-credits.md` for any Apollo-side enrichment.

| Action | Gate | Threshold |
|--------|------|-----------|
| Apify scrape | Estimate before run | >200 raw engagers OR >$5 estimated cost |
| Deepline enrichment | Confirm spend | >50 filtered prospects |
| Mode 2 zero-result query | Show user actual cost | $0.001 per zero result — surfaces if many queries miss |

---

## Chain Patterns

| Upstream | This skill | Downstream |
|----------|-----------|------------|
| LinkedIn content performance | **`/linkedin-engagement-prospects`** | `/deepline-enrich` → `/lead-scoring` → `/outreach-emails` |
| `/content-performance-loop` | **on top-performing posts** | `/lead-scoring` → `/abm-campaign` |
| Client's founder content | **engagement harvest** | Client-specific outbound sequence |

In the engagement workflow: slots into **content operations** as an optional post-publish task ("if a post goes viral, capture engagers within 7 days") and into the **sales pipeline** as an inbound-signal-capture step before discovery prep.

---

## Relationship to Other Skills

### Upstream (consumes)

| Skill | What it provides | Required? |
|-------|-----------------|-----------|
| `icp-research` | ICP filter criteria | Recommended |
| `linkedin-content` / `linkedin-expert-posts` | The posts generating engagement in the first place | Context only |

### Downstream (feeds into)

| Skill | How output is used |
|-------|-------------------|
| `deepline-enrich` | Receives filtered engager list for email waterfall |
| `lead-scoring` | Scores each engaged account on fit + signal strength |
| `outreach-emails` | Uses engagement as personalization hook |
| `abm-campaign` | Tier 1 ABM pool from highest-signal engagers |
| `niche-signal-discovery` | Engagement is one of the signal categories |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

