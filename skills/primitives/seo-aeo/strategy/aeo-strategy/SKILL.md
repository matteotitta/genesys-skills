---
name: aeo-strategy
version: '1.2'
last_updated: 2026-04-16
author: genesys-growth
description: Develops a research-backed content strategy for search and AI visibility. Produces cluster taxonomy, keyword
  gap analysis, competitor content audit, prioritized article queue with target keywords, and a 90-day publishing timeline.
  Depends on content-strategy and competitor-research for upstream context. Feeds into aeo-content for article production
  and programmatic-seo for scaled execution. Triggered by "AEO strategy", "content roadmap", "keyword gap analysis", "what
  should we publish", or "SEO content plan". NOT for writing individual articles — use /aeo-content instead.
goal: Develops a research-backed content strategy for search and AI visibility.
outcome: Develops a research-backed content strategy for search and AI visibility. Produces cluster taxonomy, keyword gap
  analysis, competitor content audit, prioritized article queue with target keywords, and a 90-day publishing timeline. Depends
  on content-strategy and competitor-research for upstream...
primitive: seo-aeo
sub_primitive: strategy
ontology_type: content-strategy
review_gate: 2
inputs:
  required: []
  recommended:
  - competitor-research
  - content-strategy
  - company-context
  - icp-behavioural
  - win-loss-analysis
  - transcript-analysis
- type: content-strategy
  feeds_into:
  - aeo-content
depends_on: []
- aeo-content
owned_by_agent: operator
mcps_used:
- exa
- gdrive
- gdrive
triggers:
  slash_commands:
  - /aeo-strategy
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# AEO Strategy

Produce a research-backed content strategy for search + AI visibility. Output: cluster taxonomy, keyword gap analysis, competitor content audit, prioritised article queue with target keywords, and a 90-day publishing timeline. Level 1 strategy skill — produces **what to write**; the Level 2 `aeo-content` skill produces **the actual content** from this queue.

## When to run

User says "AEO strategy", "content roadmap", "keyword gap analysis", "what should [company] publish", "90-day content plan for search", "article queue for [company]", or "what content will get us cited by AI?". Skip if they want a single article (`/aeo-content`), channel-agnostic plan (`/content-strategy`), or pure SEO audit (web search). Full trigger list: the premium reference.

## Inputs

**Required:** company context (product, features) · 3-5 competitors with URLs · GSC exports (Queries CSV, Pages CSV, Coverage) · GA4 exports (Traffic acquisition, Landing pages). Without GSC/GA4, all keyword data must be marked `[ESTIMATED]` and strategy confidence flagged in the executive summary.

**Recommended:** ICP research · existing content audit · positioning/messaging · competitor-research · content-strategy · win-loss-analysis · transcript-analysis (last two enable Phase 2.5 query seeding).

**Optional:** prior keyword research · monthly content target (override default 20) · AirOps brand kit.

Full export instructions (exact GSC/GA4 click paths, columns, used-in-phase mapping) + validation checklist: the premium reference.

## Steps

Eight phases. Each phase has sub-steps, output templates, and checkpoints in the premium reference — read it before producing the output.

1. **Phase 1 — Input validation.** Load company context · confirm 3-5 competitors with geography tags · set parameters (default: 20/month, 90 days, 50/20/30 BOFU/MOFU/TOFU split; adjust by maturity).
2. **Phase 2 — Cluster taxonomy.** Build 5-8 product-mapped pillars (not generic categories), each with 5-10 sub-clusters from product docs + ICP pains + competitor content.
3. **Phase 2.5 — Transcript query seeding** *(only if win-loss/transcript outputs exist).* Mine buyer questions, convert to natural-language queries, tag by cluster + source, merge into `aeo/query-index.md` (or seed it).
4. **Phase 3 — SEO keyword gap analysis.** Pull client baseline (GSC) + competitor keywords (DataForSEO → Apify → Exa fallback) · identify gaps · group by cluster · separate by geography · pull AirOps AI-citation baseline · write 1-paragraph competitor keyword strategy summaries.
5. **Phase 4 — Competitor content analysis.** Enumerate each competitor's pages free with `mcp__spider__spider_links` (per `.claude/rules/crawl-cost-discipline.md`), triage to in-scope pages, then Firecrawl only the kept set · LLM-classify pages by funnel stage (TOFU/MOFU/BOFU) AND cluster · build funnel-stage and cluster comparison tables · identify zero-coverage clusters and underweight stages.
6. **Phase 5 — Competitor best performing content.** Exa + Firecrawl + DataForSEO traffic estimates → pick top 5 per competitor · tag each with funnel stage + cluster · write 1-paragraph strategy analysis per competitor.
7. **Phase 6 — Content type strategy.** Define types per stage (BOFU: comparisons, branded, integrations, pricing, demo · MOFU: how-to, "Best X for Y", deep-dives, use cases, compliance · TOFU: definitions, industry guides, regulatory, thought leadership) · set % allocation grounded in Phase 4 gaps · write rationale per type.
8. **Phase 7 — Article queue.** Generate specific titles per type with target keywords. BOFU: 1 comparison per competitor + branded pages. MOFU: how-tos mapped to features + "Best for [year]" listicles, flag UPDATE vs CREATE. TOFU: definitions targeting highest-volume gap keywords + industry/regulatory guides.
9. **Phase 8 — 90-day timeline.** Assign articles to months (M1: comparisons + high-volume TOFU + initial MOFU · M2: BOFU deep-dives + continue MOFU/TOFU · M3: remaining BOFU + integrations + TOFU depth) · build period × stage summary table.

**Anti-hallucination guardrails (must apply during execution):** keyword volumes sourced or marked `[ESTIMATED: based on SERP analysis]` · page counts from crawl data only · no invented competitor content (verify via Exa/Firecrawl) · article titles flagged as suggestions · explicitly note approximated research. Full guardrails + per-phase checkpoint lists: the premium reference and the premium reference.

## What good looks like

**Output structure** (the premium reference for full template): `# [X]-day content roadmap for [Company]` → Executive summary (2-3 sentences + content-type table) → Research (A. clusters · B. keyword gaps · C. competitor content · D. competitor best performing) → Strategy and content examples (rationale + article tables) → Timeline (monthly + summary) → Iteration prompts.

**Design principles:** executive summary table first (10-second scan) · research before strategy · clean tables over prose walls · specific ready-to-brief titles with target keywords (not categories) · simple monthly timeline.

**Pre-delivery quality gates** (full checklists in the premium reference):
- *Research:* 5-8 clusters mapped to product features · keyword gaps with volumes · competitor crawl page counts · pages classified by stage AND cluster · top 5 per competitor.
- *Strategy:* allocation sums to 100% · monthly counts realistic · rationale grounded in Phases 3-5 (not generic) · types appropriate for client maturity.
- *Execution:* specific titles (not categories) · target keywords per article · UPDATE vs CREATE flags · monthly priorities actionable immediately · summary totals mathematically correct.

**Evaluations:** allocation percentages add to 100 · article-count totals match Phase 6 allocation across Phases 7 and 8 · every keyword volume tagged `[VERIFIED]` or `[ESTIMATED]` · every competitor page count traceable to Firecrawl crawl or marked `[ESTIMATED]` · ≥3 sources per major Exa-derived claim with `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` per `.claude/rules/exa-protocol.md`.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
