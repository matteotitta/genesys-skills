---
name: linkedin-content-audit
version: '1.0'
last_updated: 2026-04-08
author: genesys-growth
description: 'Audits LinkedIn creator profiles by scraping recent posts via Apify and producing a structured analysis of hook
  patterns, post types, media formats, media content, CTAs, and engagement metrics. Over-fetches ~100 posts per profile and
  filters to top 25 by engagement for deep pattern analysis. Supports multi-profile benchmarking with cross-profile comparison
  matrix. Triggers: "LinkedIn content audit", "audit LinkedIn profiles", "analyze creator posts", "benchmark LinkedIn creators",
  "LinkedIn pattern analysis", "content audit for LinkedIn profiles". Feeds into linkedin-content-guide and content-strategy
  as competitive intelligence. NOT for writing posts — use linkedin-content. NOT for algo checking — use linkedin-algo-audit.'
goal: Audits LinkedIn creator profiles by scraping recent posts via Apify and producing a structured analysis of hook patterns,
  post types, media formats, media content, CTAs, and engagement metrics.
outcome: Audits LinkedIn creator profiles by scraping recent posts via Apify and producing a structured analysis of hook patterns,
  post types, media formats, media content, CTAs, and engagement metrics. Over-fetches ~100 posts per profile and filters
  to top 25 by engagement for deep pattern analysis....
primitive: social
sub_primitive: linkedin
ontology_type: content-audit
review_gate: 1
inputs:
  required: []
  recommended:
  - linkedin-content-guide
  - linkedin-algo-audit
- type: linkedin-content-audit-report
  feeds_into:
  - linkedin-content-guide
  - content-strategy
  - linkedin-hooks
depends_on: []
- content-strategy
- linkedin-content-guide
- linkedin-hooks
owned_by_agent: content
mcps_used:
- apify
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

# LinkedIn Content Audit

Audit LinkedIn creator profiles by scraping posts (Apify) and classifying them across 6 dimensions: hook patterns, post types, media types, media content, CTAs, engagement. Diagnostic only — does not write posts or check algo compliance. Over-fetches ~100 posts/profile (6-month window), deep-analyzes the top 25 by engagement.

## When to run

Run when: auditing a creator's LinkedIn, benchmarking 2+ profiles, extracting hook/CTA patterns, or sourcing competitive intel for content strategy. Skip when writing posts (`linkedin-content`), checking a single post's algo fit (`linkedin-algo-audit`), building an ICP guide (`linkedin-content-guide`), or running a multi-channel audit (`content-audit`). Full trigger/anti-trigger list → the premium reference.

## Inputs

**Required:** 1-10 LinkedIn profile URLs (`linkedin.com/in/...` format).

**Optional (defaults):** scrape depth `100`, time window `6months` (alt: month/3months/year), top-N for analysis `25`, include quote posts `true`, focus areas `all 6`, client context `none`. Validate URLs before scraping; confirm parameters with user. Full input table → the premium reference.

## Steps

1. **Validate inputs** — All URLs are `linkedin.com/in/...`; 1-10 profiles; confirm depth + window with user.
2. **Phase 1.1 — Apify scrape (single batch).** Call `mcp__apify__call-actor` with actor `harvestapi/linkedin-profile-posts`, input: `targetUrls: [all]`, `maxPosts: 100`, `postedLimit: "6months"`, `includeReposts: false`, `includeQuotePosts: true`, `scrapeReactions: false`, `scrapeComments: false`. One run = one start fee + per-post cost (cheaper than N runs). Reposts excluded so patterns reflect creator's own voice.
3. **Phase 1.2 — Retrieve + validate.** Use `mcp__apify__get-actor-output` with returned `datasetId`. Confirm 50-100 posts/profile, text + engagement + timestamps present. Flag profiles with <10 posts as "insufficient data." Fallback if Apify fails: ask user for manual posts (copy-paste, Shield/Taplio/AuthoredUp CSV, or screenshots).
4. **Phase 2.1 — Group by author** (URL or name).
5. **Phase 2.2-2.4 — Engagement filter.** Compute `total_engagement = likes + comments + shares` per post. Sort each profile descending. Take top 25 for deep analysis. Retain full dataset for volume/cadence metrics (total posts, posts/week, consistency stdev).
6. **Phase 3.1 — Hook classification.** Read first line / first sentence. Map to 14-category taxonomy in the premium reference. Output: count, %, avg engagement per hook type.
7. **Phase 3.2 — Post type (pillars).** Map to Educational / Personal / Promotional / Organizational / Engagement. Compare mix to 40/25/25/10 target. Definitions → the premium reference.
8. **Phase 3.3 — Media type.** Classify from Apify attachment data: text-only, carousel/document, single image, multi-image, video, poll, article/newsletter, external link. Output: format mix + avg engagement per format.
9. **Phase 3.4 — Media content.** For posts with visuals, classify what media depicts using post-text context only (screenshots, charts, selfies, memes, infographics, text-on-image, BTS, professional photo, AI-generated, undetermined). NEVER guess from URL.
10. **Phase 3.5 — CTA classification.** Analyze final 1-3 lines. Bucket into 8 types: comment prompt, DM invite, link/resource, follow/connect, save, repost, no CTA, multiple CTAs. Output: distribution + avg engagement per type. Pattern examples → the premium reference.
11. **Phase 3.6 — Engagement analysis.** Per-post likes/comments/shares; aggregated avg/median/max; top 5 with excerpts; cross-tabs (engagement × hook, × media, × pillar, × CTA); volume metrics from full dataset.
12. **Phase 3 checkpoint** — All 6 dimensions classified; percentages sum to 100% within each category; cross-tabs computed; volume metrics from full dataset.
13. **Phase 4 — Cross-profile comparison** (only if 2+ profiles). Build profile overview matrix; format mix table; hook style heat map; engagement benchmarks; CTA distribution; top patterns to emulate (evidence-cited); anti-patterns to avoid (evidence-cited). Detail → the premium reference.
14. **Self-evaluation.** Completeness (all phases + profiles + comparison if applicable); accuracy (3 random hook spot-checks, engagement avg sanity, format consistency vs attachments); honesty (zero invented numbers, no guessed media content, gaps marked). Full protocol → the premium reference.
15. **Write outputs.** Per-profile: `linkedin-audit-{username}.md`. Cross-profile: `linkedin-audit-comparison.md`. Templates → the premium reference.

## What good looks like

**Examples:** None on file — first run will seed `examples/`.

**Evaluations:** Quality gate passes when (a) data: every profile has 10+ posts, engagement + timestamps present; (b) analysis: all 6 dimensions classified, percentages sum to 100%, cross-tabs use consistent metrics; (c) output: per-profile reports stand alone, comparison includes actionable takeaways with evidence citations, all findings traceable to specific posts.

**Anti-hallucination (load-bearing):** Only analyze Apify-returned data. Never invent engagement counts, post text, or follower counts. Mark <10 posts as insufficient data. Source every finding `(Apify, harvestapi/linkedin-profile-posts, YYYY-MM-DD)`. When hook/CTA classification is ambiguous, mark as "ambiguous" and note the two closest matches. Use precise language ("23 of 25 posts (92%)" not "almost all"). Full guardrails → the premium reference.

