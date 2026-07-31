---
name: company-context
version: '2.3'
last_updated: 2026-04-08
author: genesys-growth
description: 'Gathers firmographics, traction signals, funding history, team composition, tech stack, hiring activity, and
  key decision-makers for a target company via Exa, Apollo, Firecrawl, and Apify MCP. Produces a structured company-context
  document with qualification score, ICP fit assessment, red flag analysis, and optional account brief (job postings, key
  people, outreach angles). Triggers: "company research", "company background", "qualify this prospect", "discovery call prep",
  "account brief", or any company URL provided for research. Upstream: none (root context skill). Downstream: feeds competitor-research,
  icp-research, client-discovery, positioning, client-proposals, and apollo-sequences. NOT for competitor analysis (use /competitor-research)
  or ICP personas (use /icp-research).'
goal: Gathers firmographics, traction signals, funding history, team composition, tech stack, hiring activity, and key decision-makers
  for a target company via Exa, Apollo, Firecrawl, and Apify MCP.
outcome: Gathers firmographics, traction signals, funding history, team composition, tech stack, hiring activity, and key
  decision-makers for a target company via Exa, Apollo, Firecrawl, and Apify MCP. Produces a structured company-context document
  with qualification score, ICP fit assessment, red flag...
primitive: research
ontology_type: company-context
review_gate: 1
inputs:
  required: []
  recommended: []
- type: company-context
  feeds_into:
  - client-discovery
  - competitor-research
  - client-proposals
depends_on: []
- client-discovery
- client-proposals
- competitor-research
owned_by_agent: researcher
mcps_used:
- apollo-io
- exa
- gdrive
- gdrive
- notion
triggers:
  slash_commands:
  - /company-context
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: max
paths: projects/consulting/**, projects/prospects/**
---

# Company context

Extract firmographics, traction signals, funding, team composition, tech stack, hiring activity, and decision-makers for a target company. Produces a markdown artifact with qualification score (0-25), ICP fit assessment, red flag analysis, and optional Apollo account brief. Output drops into any client or prospect folder and feeds discovery prep, competitor research, positioning, and proposal scoping.

## When to run

Invoke for "company research", "company background", "qualify this prospect", "discovery call prep", "account brief", or whenever the user provides a company URL for research.

Do NOT invoke for competitor analysis (`/competitor-research`), product messaging extraction (`/messaging`), ICP personas (`/icp-behavioural`), or casual website checks.

Skill chain: this is a root/gateway skill. Common downstream chains in the premium reference.

## Inputs

**Required:** Company identifier — website URL, LinkedIn URL, or company name. If name is ambiguous (e.g., "Atlas", "Beam"), confirm with user before proceeding.

**Optional (improve quality):**
- LinkedIn company URL — sharper team size + org structure
- Specific questions — focus research on areas of interest
- Discovery call date — adds urgency context

**Substrate:** Exa-first per `.claude/rules/exa-protocol.md`. Primary tools `company_research_exa` and `web_search_exa`. MCP fallback chain in the premium reference. Cite per ontology: `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]`.

## Apify bulk-mode fallback (added 2026-05-01)

**Imported via:** `/steal` analysis 2026-05-01 (`.claude/discovery/0526-apify-linkedin-actors-steal-analysis.md`).

For ABM-scale company-context sweeps (>50 accounts in one run), Apollo's per-credit cost compounds — and Apollo doesn't index every company in the long tail. Bulk fallback:

| Tool | Use case | Cost |
|------|----------|------|
| `dev_fusion/Linkedin-Company-Scraper` | Bulk LinkedIn company URL → firmographics (name, industry, size, website, employee count, description, specialties) | $8/1k flat |

**MCP invocation pattern:**
```
mcp__apify__call-actor
  actor: "dev_fusion/Linkedin-Company-Scraper"
  input: {
    "company_urls": ["https://www.linkedin.com/company/...",...]
  }
```

**Threshold rule:** Use Apollo `apollo_enrich_company` + Exa `company_research_exa` for <50 companies (richer data, qualification scoring depth). Use this Apify slot for >50 companies in one ABM-scale sweep where the per-account depth needed is firmographic-only.

**Concrete win:** ClientCo's planned 100-firm account brief sweep (May 2026) — dev_fusion at $8/1k = $0.80 vs Apollo at ~$50 in credits.

**Cost gate:** All Apify-slot calls flow through `.claude/rules/apify-credits.md`. Show estimate before running on >50 companies (>$0.40 estimated cost).

## Steps

1. **Validate input.** Confirm company is identifiable. If name ambiguous, ask user for URL or clarification.
2. **Fetch website.** Pull homepage (positioning, customer signals), about page (story, team), careers page (hiring signals).
3. **Search funding.** Crunchbase, Tracxn, PitchBook, CB Insights, TechCrunch, Forbes, company press. Query patterns in the premium reference.
4. **Search revenue / team.** GetLatka, Growjo, LeadIQ, Owler, LinkedIn company page. Use revenue-from-team-size heuristics in the premium reference when sources are sparse.
5. **Extract customer signals.** Logo walls, case studies, "trusted by X" claims, G2/Capterra review counts.
6. **Assign confidence levels.** High = official source; Medium = reputable third-party; Low = aggregator/estimate. Map to `[VERIFIED] / [INFERRED] / [ESTIMATED]` per ontology. Detail in the premium reference.
7. **Identify conflicting data + document gaps.** Flag sources that disagree. Mark missing data as `[UNAVAILABLE: searched X, Y, Z]`. Suggest discovery questions to fill gaps.
8. **Calculate qualification score (0-25).** Five criteria × 0-5: stage fit, revenue fit, industry fit, marketing leader present, ICP signals. Rubric in the premium reference.
9. **Assess ICP fit signals.** Team signals, marketing gaps (opportunities), positioning complexity, intent signals — checklist in the premium reference.
10. **Check red flags.** Layoffs, funding drought, exec departures, pivots, hidden pricing, missing logos, high burn — checklist in the premium reference.
11. **Generate 3-5 key observations.** Discovery-call-ready insights and talking points.
12. **Optional — account brief mode.** If user requests, gate on Apollo credits, then run `apollo_get_organization_job_postings` (1 credit) + `apollo_search_people` (free, filtered to director+). Output hiring activity, key people, outreach angles. Spec in the premium reference.
13. **Self-evaluate.** Run completeness, evidence, and guardrail checks per the premium reference. Flag low-confidence areas before review gate.
14. **Render output.** Use the standard template in the premium reference (traction signals, funding details, team breakdown, qualification score, ICP fit, red flags, key observations, data gaps + optional account brief).
15. **Review gate (Level 1, quick review).** Present qualification score + traction signals. Then surface chain suggestions: competitors? discovery questions? client-discovery? Apollo sequence? Save as reference example if positive feedback.

## What good looks like

### Evaluations

- All 4 target questions answered (revenue, customers, funding, team) or marked `[UNAVAILABLE: searched X]`
- Every data point carries source + confidence level
- Qualification score calculated 0-25 with notes per criterion
- ICP fit + red flags checklists completed
- Data gaps section with discovery questions
- ≥3 sources per major claim, ≥50% `[VERIFIED]` per `.claude/rules/exa-protocol.md`
- No invented funding/revenue/team numbers — `[UNAVAILABLE]` notation when missing
- Confidence levels match the ontology mapping (High → verified, Medium → inferred, Low → estimated)

