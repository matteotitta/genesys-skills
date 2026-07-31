---
name: jobs-signal
version: '1.1'
last_updated: 2026-05-01
author: genesys-growth
description: 'Pulls LinkedIn job postings as hiring-intent signals for ABM and niche-signal workflows. Scrapes a target company''s
  active jobs (or a market-wide query) via Apify, extracts role + count + recency, and surfaces buying-intent triggers like
  "Company X is hiring 5 RevOps roles" or "30 of our 100 ABM accounts are hiring AI engineers right now". Two modes: cheap
  bulk scan via valig/linkedin-jobs-scraper ($0.32/1k jobs) and enriched mode via fantastic-jobs/advanced-linkedin-job-search-api
  with recruiter contact data + AI enrichments. Triggers: "find hiring signals at", "who is hiring [role]", "jobs at [company]",
  "hiring intent signals", "/jobs-signal", "scrape LinkedIn jobs". NOT for general job-board search (use a job aggregator),
  candidate sourcing (we''re a B2B SaaS GTM consultancy, not a recruiting firm), or general LinkedIn profile data (use /clay-search
  or /deepline-enrich).'
goal: Surface hiring-intent signals from LinkedIn job postings to power ABM targeting and niche-signal workflows.
outcome: A signal-enriched list of companies with active hiring activity matching role/recency filters, with per-company job
  count, role types, and posting timestamps. Feeds into /niche-signal-discovery for signal aggregation and /abm-campaign for
  account prioritisation.
primitive: outbound
sub_primitive: list-building
ontology_type: lead-assessment
review_gate: 1
inputs:
  required: []
  recommended:
  - icp-research
  - company-context
- type: signal-enriched-account-list
  feeds_into:
  - niche-signal-discovery
  - abm-campaign
  - lead-scoring
depends_on: []
- niche-signal-discovery
- abm-campaign
- lead-scoring
owned_by_agent: researcher
mcps_used:
- apify
- gdrive
- notion
triggers:
  slash_commands:
  - /jobs-signal
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: medium
---

# /jobs-signal — Hiring-intent signals from LinkedIn jobs

Companies that are hiring are companies that are spending. A target account hiring 5 RevOps roles signals revenue-tooling intent. A whole ABM list hiring AI engineers signals a market shift. This skill turns LinkedIn jobs data into structured signals for ABM and niche-signal workflows.

**Imported via:** `/steal` analysis 2026-05-01 (`.claude/discovery/0526-apify-linkedin-actors-steal-analysis.md`). Closed the only direct gap on the Apify-actor list — there was no existing capability for hiring-intent signals.

---

## When to use

### Run this skill when

- You have an ABM target list and want intent signals layered on
- You're researching a niche and want to know which companies are actively building in it
- A client wants competitive insight into who's hiring for [role] in [vertical]
- Pre-discovery prep wants "is this prospect hiring? for what?" as account context

### Do NOT use when

- You need candidate-side data (resumes, profiles for recruiting) — wrong tool
- You need general job-board aggregation (Indeed, Glassdoor) — different surface
- You need company firmographics — use `/company-context`
- You need contact data at companies — use `/clay-search` or `/deepline-enrich`

---

## Two modes — voice-locked

### Mode 1 — Bulk scan (default)

**Actor:** `valig/linkedin-jobs-scraper`
**Cost:** $0.32/1k jobs (DIAMOND tier) → $0.40/1k (FREE tier)
**Use when:** scanning many companies for hiring activity, or running market-wide role queries

The cheapest reliable jobs scraper at 99.7% success rate, 4.98★. Returns role title, location, posting date, company URL, job description.

### Mode 2 — Enriched (recruiter contact + AI enrichments)

**Actor:** `fantastic-jobs/advanced-linkedin-job-search-api`
**Cost:** $1.50/1k jobs (DIAMOND tier) → $5/1k (FREE tier) — **5–12× more expensive than Mode 1**
**Use when:** the client needs recruiter contact data alongside the jobs (to outreach the recruiter, not the company), or AI-enriched job classifications (seniority extraction, skill tagging, normalised role taxonomy)

Returns everything Mode 1 returns, plus: recruiter LinkedIn URL, recruiter email, AI-classified seniority, AI-extracted skills, normalised role family.

---

## Signal-strength matrix — voice-locked

| Indicator | Weight | What it means |
|-----------|--------|---------------|
| job_count | × 0.3 | More open roles = more spend, more activity |
| target_role_match_count | × 0.5 | Roles matching the *specific* intent we care about (e.g., RevOps for revenue-tooling intent) |
| recency | × 0.2 | Posted-in-last-7-days = strongest, 30+ days = decaying |

**Output bands:**
- **STRONG** (signal_strength ≥ 7): worth a Tier-1 ABM placement, immediate routing
- **MODERATE** (4–7): Tier-2 / nurture-track candidate
- **WEAK** (1–4): note in /niche-signal-discovery output but don't prioritise routing
- **NONE** (0): no relevant hiring activity in window

---

## Credit gate — voice-locked

`/jobs-signal` runs through `.claude/rules/apify-credits.md`'s gating rules. Before any actor call:

1. Estimate cost: `(expected_job_count × $/1k) / 1000 + actor_start_fee`
2. Show estimate to user
3. Wait for confirmation if estimate >$5

Cost cheat sheet + invocation patterns in the premium reference.

---

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **Company URLs** | Target firm LinkedIn URLs (ABM mode) | One of these is required |
| **Role + location query** | Market-wide scan | One of these is required |
| **Posted-after date** | ISO date filter (default: last 30 days) | Recommended |
| **ICP context** | For role-match scoring | Recommended |
| **Mode** | bulk \| enriched | Required (default: bulk) |

---

## Process

**Five-phase flow:** Input validation → Cost estimation + credit gate → Actor call (Mode 1 or 2) → Signal extraction (job_count, role_types, most_recent_posting, target_role_match_count, signal_strength) → Output. Step-by-step + actor invocation patterns + cost cheat sheet in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent jobs.** If the actor returns 12 jobs at Stripe, report 12, not "approximately 15."
2. **Don't infer hiring intent from job descriptions beyond literal text.** "Looking for someone with revenue-tooling experience" is signal. "Familiar with revenue tools" is not.
3. **Date validation.** If `most_recent_posting` is older than the date filter, flag — likely an actor bug, not a stale post.
4. **Empty result handling.** Zero jobs returned ≠ failure. It means no active hiring in the window. Report explicitly.
5. **Recruiter data (Mode 2).** If the actor returns a recruiter LinkedIn URL but no email, *do not* fabricate the email — pass to `/deepline-enrich` for waterfall lookup.

---

## Quality

Pre-delivery checks cover coverage (date filter set, empty-result reporting), quality (counts match actor exactly, recruiter emails marked `[UNAVAILABLE]` when not returned, signal-strength applied per matrix), and cost discipline (Apify gate, Mode 2 only when justified). Worked example (ClientCo 100-firm sweep at $1.60) + anti-examples (Mode 2 by default, all-jobs-ever, fabricated recruiter emails, soft-language inference) + quality gate in the premium reference.

---

## Chain Patterns

| Upstream | This skill | Downstream |
|----------|-----------|------------|
| ABM target list | **`/jobs-signal`** (bulk mode) | `/abm-campaign` for routing, `/niche-signal-discovery` for aggregation |
| Niche / vertical research | **`/jobs-signal`** (market-wide query) | `/niche-signal-discovery` |
| Discovery prep | **`/jobs-signal`** (single company) | `/client-discovery` as account context |
| Recruiter outreach use case | **`/jobs-signal`** (enriched mode) | `/deepline-enrich` for recruiter email validation → `/outreach-emails` |

In the engagement workflow: slots into the **AEO visibility loop** as an optional context-input (a sudden hiring spike on a target account is a signal that AEO content for that account's space is timely) and into the **sales pipeline** as a discovery-prep enrichment.

---

## Relationship to Other Skills

### Upstream (consumes)

| Skill | What it provides | Required? |
|-------|-----------------|-----------|
| `icp-research` | Target role definitions + ICP filters | Recommended |
| `company-context` | Company URL list (when running ABM-list mode) | Recommended |
| `abm-campaign` | The ABM list itself | Optional |

### Downstream (feeds into)

| Skill | How output is used |
|-------|-------------------|
| `niche-signal-discovery` | Hiring is one signal class — feeds the multi-signal aggregator |
| `abm-campaign` | Tier-1 routing for STRONG-signal accounts |
| `lead-scoring` | Hiring activity adds to fit + signal score |
| `outreach-emails` (Mode 2 only) | Recruiter contact for outreach |

---

## Credit and Tool Reference

| Tool | Purpose | Cost |
|------|---------|------|
| `valig/linkedin-jobs-scraper` (Apify MCP) | Bulk jobs scrape | $0.32–$0.40/1k jobs |
| `fantastic-jobs/advanced-linkedin-job-search-api` (Apify MCP) | Enriched jobs + recruiter data | $1.50–$5/1k jobs |
| `/deepline-enrich` (downstream, Mode 2 only) | Recruiter email validation | Deepline credits |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

