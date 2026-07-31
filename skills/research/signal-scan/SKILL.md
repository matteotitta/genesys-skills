---
name: signal-scan
version: "1.0"
last_updated: 2026-06-08
author: genesys-growth
description: |
  Produces a topic-agnostic "what happened in the last N days" signal brief for any
  person, company, product, technology, or market term — ranked by engagement (upvotes,
  likes, views, stars, market odds) rather than SEO. Resolves entities before searching,
  expands to peer communities, clusters the same story across surfaces, and fans out across
  Reddit, Hacker News, news/funding, GitHub, G2/Trustpilot/Product Hunt, and YouTube (with
  X/TikTok/Instagram/Polymarket behind credit-gated flags). Triggers: "what happened with X
  in the last 30 days", "recent activity on", "what's new with", "signal scan on", "last 30
  days". Upstream: recommended company-context. Downstream: feeds competitor-research,
  gtme-pulse, content-strategy, client-discovery. NOT for internal decision history (use /think),
  session recall (use /recall), a deep static competitor dossier (use /competitor-research),
  or a curated newsletter from pre-collected links (use /gtme-pulse).
goal: Produce a dated, cited, engagement-ranked brief of what happened on any topic in the last N days across community, news, code, and market surfaces.
outcome: A markdown or HTML brief — releases, news/funding, community sentiment, notable signals — with inline citations and access dates, ranked by engagement. Feeds competitor monitoring, newsletter prep, content strategy, and discovery prep without manual search chains.
primitive: research
ontology_type: temporal-signal-brief
review_gate: 1
inputs:
  required: []
  recommended:
  - company-context
- type: temporal-signal-brief
  feeds_into:
  - competitor-research
  - gtme-pulse
  - content-strategy
  - client-discovery
depends_on: []
- competitor-research
- gtme-pulse
- content-strategy
- client-discovery
owned_by_agent: researcher
mcps_used:
- exa
- firecrawl
- github
- youtube-transcript
- apify
triggers:
  slash_commands:
  - /signal-scan
  natural_language:
  - "what happened with X in the last 30 days"
  - "recent activity on"
  - "what's new with"
  - "signal scan on"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# Signal scan

Answer "what happened with **{topic}** in the last **N** days?" for any person, company, product, technology, or market term. The brief is ranked by what people actually engaged with — upvotes, likes, views, GitHub stars, prediction-market odds — not by SEO. Knowledge type: `temporal-signal-brief` (per `.claude/rules/ontology.md`); maturity: emergent (each run is fresh, time-bound — briefs are not locked).

Stolen MCP-native from [`mvanhorn/last30days-skill`](https://github.com/mvanhorn/last30days-skill) (MIT). The method is the steal — entity-resolution-before-search, peer expansion, story clustering, engagement ranking. The 1,036-line Python engine is **not**: every surface maps to an MCP we already run (Exa, Firecrawl, GitHub, youtube-transcript, Apify). Provenance + verdict table: `.claude/discovery/0626-last30days-skill-steal-analysis.md`.

## When to run

Invoke for: `what happened with {topic} in the last 30 days`, `recent activity on {company}`, `what's new with {technology}`, `signal scan on {market}`, pre-call prospect prep, weekly newsletter sourcing, competitor recency checks.

Do **NOT** invoke for:

- Internal decision history / "what did we decide" → `/think` (searches our own decision logs).
- "What did we discuss in past sessions" → `/recall` (session DB).
- A deep, static, 13-dimension competitor dossier → `/competitor-research`. (This skill is shallow + recent + topic-agnostic; it feeds that skill's "Recent changes" header.)
- A curated newsletter from links you already collected → `/gtme-pulse` (this skill *sources* the raw signal that feeds it).

**Brain-first (mandatory):** before any external call, run the `.claude/rules/brain-first-lookup.md` ladder — `/recall {topic}` + grep client folders. A locked client doc may already hold what a scan would rediscover. Annotate the brief if you went external after a brain miss.

## Inputs + flags

**Required:** `topic` — the thing to scan (person / company / product / technology / market term). If ambiguous (e.g. "Pivot", "Base", "Bolt"), confirm the disambiguator before running.

**Flags:**

| Flag | Default | Effect |
|------|---------|--------|
| `--days N` | 30 | Lookback window. `--days 14` for fast-moving, `--days 90` for slower markets. |
| `--compare "A vs B"` | off | Per-entity parallel pipelines, merged into a head-to-head brief. |
| `--emit=html` | markdown | Self-contained shareable HTML file instead of markdown. |
| `--x` | off | Add X/Twitter via Apify actor (**credit-gated**). |
| `--tiktok` | off | Add TikTok via Apify actor (**credit-gated**; thin for most B2B topics). |
| `--instagram` | off | Add Instagram via Apify actor (**credit-gated**; thin for most B2B topics). |
| `--markets` | off | Add Polymarket / Kalshi odds via Firecrawl (free; relevant only for forward-looking topics). |

## The pipeline

Seven steps. Full detail → the premium reference. Surface→tool mapping → the premium reference.

1. **Brain-first check.** `/recall {topic}` + grep client folders (per `brain-first-lookup.md`). Use what's already known; only go external for the gap.
2. **Resolve entities before searching.** Find the topic's X/LinkedIn handle, GitHub user/org/repo, the subreddits where its category is discussed, and its domain — *before* any keyword search. This is the step that turns a keyword dump into signal. Kills collisions (searching "42" → Jackie Robinson jerseys; "Pivot" → gymnastics).
3. **Expand to peer communities.** If the topic is a product in a known category, add the cross-product communities where practitioners actually compare tools (not just the brand's own mentions). Annotate the brief with the peer set used.
4. **Generate a query plan.** *You* (the model) write the plan — intent / freshness mode / cluster mode / 1–4 subqueries with per-surface weights. Schema → the premium reference. No engine plans this; Claude does.
5. **Parallel fan-out, date-filtered.** Run the resolved surfaces concurrently, each bounded to the `--days` window. Probe one surface before fanning out (per `goal-driven-loops.md`). Free discovery before metered extraction (per `crawl-cost-discipline.md`). Gate every paid Apify call (per `apify-credits.md`).
6. **Cluster + rank.** Merge the same story across surfaces into one item (HN + Reddit + newsletter on the same launch = one clustered signal, not three). Rank by engagement (upvotes / likes / views / stars / odds) with recency decay.
7. **Synthesize a cited brief.** Narrative prose, inline citations with access dates, per the premium reference. Default-on surfaces: Reddit, HN, news/funding, GitHub, G2/Trustpilot/Product Hunt, YouTube. Flag-gated: X/TikTok/IG/markets.

## Credit gate

X / TikTok / Instagram run through Apify actors and are **off by default**. When a flag turns one on, follow `.claude/rules/apify-credits.md`: `fetch-actor-details` (free) first, estimate cost, gate before `call-actor` (soft <$5, hard ≥$5). Deep-Reddit via Apify is also credit-gated; the default Reddit surface uses free Exa site-filtered search. `--markets` (Firecrawl) and all default-on surfaces incur no Apify spend. Probe one item before any batch fan-out.

## Quality gate (binary, before declaring done)

- Brain-first ladder run before any external call; brief annotated if it went external after a miss.
- Entities resolved before searching (handle / repo / subreddits named in the brief, or explicitly "none found").
- Peer set named when the topic is a product in a known category.
- Every claim has an inline citation + access date; no invented engagement numbers (mark `[Not available]`).
- Date window respected — nothing older than `--days N` in the brief (or flagged as background context).
- Story-level dedup applied — no single story appearing 3× from 3 surfaces.
- Coverage footer lists which surfaces ran, were thin, or were skipped — no silent truncation.
- Apify flags: cost estimated + gated before any paid call.

## Composition

| Rule | Role |
|------|------|
| `brain-first-lookup.md` | Step 1 — check the brain before external. |
| `exa-protocol.md` | Tool selection + citation standard for the default surfaces. |
| `crawl-cost-discipline.md` | Free discovery (spider_links / sitemap) before metered extraction. |
| `apify-credits.md` | Gate every paid Apify call (X/TikTok/IG/deep-Reddit). |
| `goal-driven-loops.md` | Probe-one-before-fan-out on the parallel surfaces. |
| `outbound-research-hygiene.md` | When a signal feeds outbound copy — dated, ≤12mo, current-company-only. |
| `output-tenets.md` · `output-simplicity.md` · `doc-output-structure.md` · `ai-speak-anti-patterns.md` | Brief voice + structure + source placement. |

