---
name: local-seo-audit
version: '1.0'
last_updated: 2026-03-16
author: genesys-growth
description: 'Orchestrates local SEO audits by routing to four dedicated sub-skills: GBP category and attribute audit (/gbp-category-audit),
  review teardown and response strategy (/gbp-review-strategy), posts calendar and photo plan (/gbp-content-engine), and services
  and description optimization (/gbp-listing-optimization). Runs all four in sequence for full audit mode or routes individual
  requests to the correct sub-skill. Produces a comprehensive local visibility report. Triggered by "local SEO audit", "GBP
  audit", "Google Business Profile", "map pack optimization", or "local search". Feeds into landing-page-copy, content-strategy,
  and aeo-content.'
goal: 'Orchestrates local SEO audits by routing to four dedicated sub-skills: GBP category and attribute audit (/gbp-category-audit),
  review teardown and response strategy (/gbp-review-strategy), posts calen'
outcome: 'Orchestrates local SEO audits by routing to four dedicated sub-skills: GBP category and attribute audit (/gbp-category-audit),
  review teardown and response strategy (/gbp-review-strategy), posts calendar and photo plan (/gbp-content-engine), and services
  and description optimization...'
primitive: seo-aeo
sub_primitive: audit
ontology_type: content-audit
review_gate: 1
inputs:
  required: []
  recommended:
  - company-context
- type: local-seo-audit
  feeds_into:
  - website-copy
  - content-strategy
  - aeo-content
depends_on: []
- aeo-content
- content-strategy
- website-copy
owned_by_agent: operator
mcps_used:
- exa
- firecrawl
- gdrive
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

## Research substrate (Exa)

**Default:** Exa, per `.claude/rules/exa-protocol.md` (auto-loaded for research, audit, competitor, ICP, AEO, content sourcing, sales prospecting work).

**Primary Exa tools for this skill:** `web_search_exa`.

**Use case:** local pack + competitor research.

**Tool surface during the migration window:**
- New plugin (preferred): `mcp__plugin_exa_exa__web_search_exa` (after `claude plugin i exa@claude-plugins-official`).
- Legacy MCP (still mounted): `mcp__exa__web_search_exa`.
- Both backends route to the same Exa API — they don't double-bill.

**Citation:** every Exa-derived claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` per `.claude/rules/ontology.md`.

**Quality gate (research outputs):** ≥3 sources per major claim, ≥50% `[VERIFIED]` confidence, date filter for any "recent / latest" claim, no fallback to `WebSearch` without flagging the data gap.

**Worked examples + tool catalog:** `.claude/skills/meta-skills/exa/`.

# Local SEO audit

Orchestrator for local SEO audits of Google Business Profile listings. Routes to 4 dedicated sub-skills covering categories, reviews, content, and listing optimization. Based on the 8-prompt local SEO playbook adapted for Claude Code's MCP stack.

---

## Sub-skills (dedicated)

| Skill | Path | Invoke | Use when |
|-------|------|--------|----------|
| GBP category audit | `gbp-category-audit/SKILL.md` | `/gbp-category-audit` | Category + attribute gap analysis vs. competitors |
| GBP review strategy | `gbp-review-strategy/SKILL.md` | `/gbp-review-strategy` | Review teardown + response template system |
| GBP content engine | `gbp-content-engine/SKILL.md` | `/gbp-content-engine` | Posts calendar + photo upload plan |
| GBP listing optimization | `gbp-listing-optimization/SKILL.md` | `/gbp-listing-optimization` | Services section + description optimization |

**Routing rule:** If user requests a specific audit type, route to the dedicated sub-skill. Do NOT handle these directly — invoke the sub-skill instead.

---

## Full audit mode

When user requests a "full local SEO audit" or "complete GBP audit", run all 4 sub-skills in this order (matches the recommended 4-week execution cadence):

```
Week 1: /gbp-category-audit → Fix foundation (categories + attributes)
Week 2: /gbp-listing-optimization → Optimize listing text (services + description)
Week 3: /gbp-review-strategy → Build review system (teardown + templates)
Week 4: /gbp-content-engine → Launch content engine (posts + photos)
```

After each sub-skill completes, present results and ask if user wants to continue to next phase.

---

## Process Flowchart

Input validation → routing decision → (single sub-skill OR sequential 4-skill run) → scoring (full audit only) → Gate 1 review → chain suggestions. Full ASCII flowchart in the premium reference.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Local SEO audit for [business]"
- "GBP audit"
- "Google Business Profile audit"
- "Audit my Google listing"
- "Local search optimization"
- "Map pack analysis"
- "How do I rank locally?"
- "Local SEO score"
- "Compare my GBP to competitors"

**Route to sub-skills instead:**
- "Category audit" / "GBP categories" / "Attributes audit" → Use `/gbp-category-audit`
- "Review strategy" / "Review teardown" / "Review templates" → Use `/gbp-review-strategy`
- "GBP posts" / "Content calendar" / "Photo audit" → Use `/gbp-content-engine`
- "Services optimization" / "Description optimization" → Use `/gbp-listing-optimization`

**Do NOT invoke when:**
- User wants website PM score (B2B SaaS) → Use `/website-pm-score`
- User wants AEO content → Use `/aeo-content`
- User wants programmatic SEO → Use `/programmatic-seo`

---

## Input Requirements

### Required Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Business name** | Legal business name | User provides |
| **Business GBP URL** | Google Maps/Business link | User provides |
| **Competitor GBP URLs** | 2-3 top competitor listings | User provides or researched |
| **Target keywords** | 3+ search terms to rank for | User provides |
| **Service areas** | Neighborhoods/cities served | User provides |

### Optional Inputs (improve quality)

| Input | How It Helps |
|-------|--------------|
| Website URL | Cross-references services, enables listing-website alignment check |
| Core services list | Ensures services section covers all offerings |
| Current review count | Baseline for velocity calculations |
| Business address | NAP consistency checks |

### Input Validation Checklist

Before proceeding, verify:
- [ ] GBP URL is accessible
- [ ] At least 2 competitor GBP URLs provided
- [ ] At least 3 target keywords specified
- [ ] Service areas defined

**If inputs are missing:** Ask for GBP URL first. Offer to research competitors via Exa/Firecrawl if user doesn't have competitor URLs.

---

## Iteration Prompts

1. "Want me to run a specific sub-audit in more depth?"
2. "Should I create a 90-day execution roadmap from these findings?"
3. "Want me to export this to Google Docs for the client?"
```

---

## Anti-Hallucination Guardrails

1. **Only score what was scraped.** If a GBP page didn't load, mark that audit as "incomplete" — don't infer.
2. **No invented review counts.** If review data can't be extracted, note "[UNAVAILABLE: could not scrape reviews]".
3. **Competitor data must be sourced.** Every competitor comparison needs the scraped data behind it.
4. **Impact estimates as ranges.** "Adding missing categories typically improves visibility by 10-30%" with [ESTIMATED] tag.
5. **GBP data is point-in-time.** Note the scrape date — listings change frequently.

---

## Quality Checklist (Pre-Delivery)

- [ ] All 4 sub-audits completed (full mode) or selected audit completed
- [ ] Scoring rubric applied with evidence per category
- [ ] Top 5 actions identified with impact/effort ratings
- [ ] Executive summary written
- [ ] No invented data — all comparisons from scraped sources
- [ ] Export-ready markdown format

---

## MCP Data Integration

Primary tools: Firecrawl (GBP page scraping, default), Exa (SERP map-pack analysis), Apify (structured Google Maps data, credit-gated). Fallback: WebFetch + WebSearch + user-provided screenshots. Full integration table in the premium reference.

---

## Integration with Other Skills

### Upstream Skills (Provide Inputs)

| Skill | What It Provides | Required? |
|-------|------------------|-----------|
| **company-context** | Business details, service areas | Recommended |

### Downstream Skills (Consume Outputs)

| Skill | How It Uses Local SEO Audit |
|-------|----------------------------|
| **landing-page-copy** | Website improvements based on listing-site alignment |
| **aeo-content** | Local content optimized for AI search |
| **content-strategy** | Ongoing local content plan |

---

