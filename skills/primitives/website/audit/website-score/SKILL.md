---
name: website-pm-score
version: '2.0'
last_updated: 2026-01-16
author: genesys-growth
description: Audits a B2B SaaS website for product marketing effectiveness and assigns a 0-100 PM score. Evaluates messaging
  clarity, social proof, CTA quality, competitive positioning, and visual hierarchy. Produces category-level scores with prioritized
  recommendations. Triggers on "website score", "PM audit", "website audit", "rate this website", or "how good is their marketing".
  Feeds into landing-page-copy for gap-driven rewrites and client-discovery for prospect qualification.
goal: Audits a B2B SaaS website for product marketing effectiveness and assigns a 0-100 PM score.
outcome: Audits a B2B SaaS website for product marketing effectiveness and assigns a 0-100 PM score. Evaluates messaging clarity,
  social proof, CTA quality, competitive positioning, and visual hierarchy. Produces category-level scores with prioritized
  recommendations. Triggers on "website score", "PM...
primitive: website
sub_primitive: audit
ontology_type: website-score
review_gate: 2
inputs:
  required: []
  recommended: []
- type: website-score
  feeds_into:
  - website-build
  - website-copy
depends_on: []
- website-build
- website-copy
owned_by_agent: operator
mcps_used:
- exa
- gdrive
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
effort: high
---

# Website PM Score

Evaluate B2B SaaS websites against first-principles product marketing criteria. Generate an actionable PM Score (0-100) that identifies specific gaps and provides prioritized, wireframed recommendations. Knowledge type: `website-score` per `.claude/rules/ontology.md`.

## Research substrate

Default substrate: **Exa** (per `.claude/rules/exa-protocol.md`, auto-loaded). Primary tool: `web_fetch_exa` for clean page extraction. Migration window: prefer plugin namespace `mcp__plugin_exa_exa__web_fetch_exa` once installed; legacy `mcp__exa__web_fetch_exa` still mounted as fallback. Citation: every Exa-derived claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]`. Quality gate: ≥3 sources per major claim, ≥50% `[VERIFIED]`, no fallback to `WebSearch` without flagging the data gap. Worked examples + tool catalog: `.claude/skills/meta-skills/exa/`.

## When to run

Invoke when the user says: `evaluate this website`, `score this website`, `website audit for [URL]`, `PM score for [company]`, `product marketing score`, `website assessment`, `homepage analysis`, `landing page audit`, `rate this website`, `what's wrong with this site`, `review [URL]`, `website teardown`, `messaging audit`. Do **NOT** invoke for: landing page copy writing (use `/landing-page-copy`), competitor research without scoring (use `/competitor-research`), positioning work (use `/product-messaging`), ICP research (use `/icp-behavioural`).

Two assessment modes — pick by depth needed:

- **Quick** — 5 categories scored, normalized to /100. Best for lead-magnet output, prospect triage, fast diagnostic.
- **Full** — 9 categories scored, raw /100. Best for active client engagements, comprehensive teardown, before/after planning.

Visual phase map → the premium reference. Full scoring rubric → the premium reference.

## Inputs

**Required:**

- `website URL` — primary site to evaluate (must be accessible/fetchable).
- `assessment mode` — `Quick` (5 categories) or `Full` (9 categories). User specifies or inferred.

**Recommended (improve quality):**

- `competitor URLs` — enables competitive teardown mode (element-by-element comparison).
- `vertical context` — adjusts expectations for industry.
- `specific focus areas` — weights certain categories higher.
- `known positioning` — helps evaluate differentiation accuracy.

If website URL missing, ask. If mode unclear, confirm Quick (lead magnet) vs. Full (comprehensive). If competitor URLs invalid, drop competitive context section without blocking.

## Steps

1. **Validate inputs** — confirm URL is fetchable, mode is set, competitor URLs (if any) are valid.
2. **Fetch primary pages** — homepage required; Full mode also pulls pricing, features, customers, about. Capture hero section verbatim. Use `web_fetch_exa` for clean extraction.
3. **Apply 5-second test** — first viewport only. Check for tool anchor OR task anchor (one suffices). Frameworks → the premium reference ("The Amorphous Software Problem"). Output pass/fail with rationale.
4. **Competitor fetch** (if competitor URLs provided) — fetch homepages, apply same 5-second test, note comparative observations.
5. **Score Quick categories** (both modes) — Product clarity /12, Audience specificity /12, Problem articulation /15, Differentiation /15, Action clarity /10. Each score requires verbatim evidence from fetched pages.
6. **Score Full categories** (Full mode only) — Outcome clarity /15, Trust & proof /10, Risk reduction /6, Product visualization /5. Same evidence rule.
7. **Calculate total + interpretation** — Quick: sum to 64, normalize to /100. Full: raw /100. Apply score interpretation table (the premium reference): 85-100 Excellent / 70-84 Good / 55-69 Needs work / 40-54 Weak / 0-39 Critical.
8. **Per-ICP matrix** (if ≥2 personas provided) — score per persona × per category instead of single number. Per-persona evidence + recommendations + priority. Full protocol → the premium reference ("Per-ICP scoring mode").
9. **Prioritize recommendations by tier** — Fix this week (blocking copy-only), Fix this month (structural/new content), Fix this quarter (strategic/research-required). Tier criteria → the premium reference ("Recommendation tiers").
10. **Create before/after wireframes** — hero rewrites, key section additions, CTA improvements. Verbatim "before"; concrete copy in "after". Box-drawing format per template.
11. **Estimate impact** — apply benchmarks from the premium reference and the premium reference. Provide ranges, not precise numbers; cite basis.
12. **Add competitive context** (if competitor URLs provided) — element-by-element comparison matrix (hero anchor, status quo named, differentiator, gap assessment).
13. **Self-evaluate against guardrails** → the premium reference ("Anti-hallucination guardrails" + "Pre-delivery quality checklist"). Mark inferences explicitly. Note "Not quantified" for missing metrics.
14. **Write output** per template → the premium reference (full structure: score summary, 5-second test, category analysis, prioritized recommendations, competitive context, iteration prompts).
15. **Offer iteration prompts** post-delivery → the premium reference (refinement / expansion / quality offers + auto-update protocol).

## What good looks like

### Evaluations (binary pass/fail before declaring "done")

- All applicable categories scored (5 for Quick, 9 for Full).
- Every score has verbatim evidence quote from a fetched page.
- Scores sum correctly; interpretation matches range.
- 5-second test result includes pass/fail + grounding check (tool anchor / task anchor presence).
- ≥1 recommendation per tier (Fix this week / month / quarter).
- Before/after wireframes for hero changes use box-drawing characters and verbatim "before".
- No invented metrics — every claim quantified is on the site or marked "Not quantified".
- No assumed pages — only score what was fetched.
- Output title is `# Website PM Score: [Company Name]` exactly.
- Per-ICP matrix present if ≥2 personas were provided.

## Integration with other skills

| Direction | Skill | What flows |
|-----------|-------|-----------|
| **Feeds into** | `/landing-page-copy` | Gap recommendations → hero rewrite + section copy briefs |
| **Feeds into** | `/product-messaging` | Differentiation gaps → sharpens messaging anchors |
| **Receives from** | `/company-context` | Client context → deeper scoring grounding |
| **Receives from** | `/competitor-research` | Competitor profiles → competitive teardown mode |
| **Receives from** | `/icp-behavioural` | Personas → per-ICP scoring matrix |

**Recommended chains:**

- Prospect qualification: `company-context → website-score` (Quick mode for triage).
- Active client teardown: `competitor-research → website-score (Full) → landing-page-copy`.
- Multi-persona client: `icp-behavioural → website-score (per-ICP matrix) → product-messaging`.

## Pre-slim original

Pre-slim SKILL.md (777 lines, v2.0) archived at `.claude/skills/_archive/website-score/SKILL-pre-slim-20260429.md`. See the premium reference ("Changelog") for the v2.3 entry documenting the slim.

---

## Sourced patterns — technical SEO discipline

<!-- Sourced from coreyhaines31/marketingskills/seo-audit/SKILL.md (MIT) — accessed 2026-05-17. Imported via /steal I10. -->

Add these technical-SEO checks to the audit rubric. Each is a sharp threshold with a Google-enforced consequence:

- **Core Web Vitals thresholds (Google ranking signal).**
  - LCP (Largest Contentful Paint) < 2.5s
  - INP (Interaction to Next Paint) < 200ms
  - CLS (Cumulative Layout Shift) < 0.1
  Pages failing any of these are penalized in mobile + desktop ranking. Check via PageSpeed Insights.
- **Title tag: 50–60 characters with keyword near the beginning.** Above 60 truncates in SERP; below 50 underuses real estate.
- **Hreflang reciprocity rule.** Multi-language pages require self-referencing hreflang entries AND reciprocal links between languages. Missing either invalidates the cluster — Google ignores the entire setup.
- **E-E-A-T signals checklist.** Experience (author has used the product/service), Expertise (credentials visible), Authoritativeness (citations + inbound links), Trustworthiness (HTTPS, clear contact info, transparent ownership).
- **"Important pages within 3 clicks of homepage" rule.** Pages 4+ clicks deep are effectively invisible to most users + crawlers. (Paired with `/site-architecture` Step 1.)
- **One `<h1>` per page; logical hierarchy (no H1→H3 jumps).** Multiple H1s confuse content-importance signals.
- **JS-injected schema caveat.** `web_fetch` and similar tools cannot detect JavaScript-injected schema. For pages using client-side schema rendering, validate via Google's Rich Results Test (Google does execute the JS) — not via fetch tools. (Paired with `/schema-markup` Step 5.)

Priority hierarchy when auditing: Crawlability → Indexation → Speed → On-Page → Authority. Fix in that order; later-stage fixes don't matter if earlier stages are broken.
