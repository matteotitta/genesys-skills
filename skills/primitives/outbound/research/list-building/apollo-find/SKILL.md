---
name: apollo-find-companies
version: '1.0'
last_updated: 2026-04-08
author: genesys-growth
description: Searches Apollo's 70M+ company database by industry, size, location, tech stack, funding, revenue, and hiring
  signals. Produces target account lists in markdown, CSV, or Clay-ready format. Free — does not consume Apollo credits. Feeds
  into company-context for deep research and build-tam for TAM expansion. Triggered by "find companies", "target account list",
  "companies using [tech]", "recently funded companies", "companies hiring for [role]", or "Apollo company search". NOT for
  researching a known company (use /company-context) or finding people (use /clay-search).
goal: Searches Apollo's 70M+ company database by industry, size, location, tech stack, funding, revenue, and hiring signals.
outcome: Searches Apollo's 70M+ company database by industry, size, location, tech stack, funding, revenue, and hiring signals.
  Produces target account lists in markdown, CSV, or Clay-ready format. Free — does not consume Apollo credits. Feeds into
  company-context for deep research and build-tam for TAM...
primitive: outbound
sub_primitive: list-building
ontology_type: lead-assessment
review_gate: 1
inputs:
  required: []
  recommended:
  - icp-research
- type: target-account-list
  feeds_into:
  - company-context
  - apollo-sequences
depends_on: []
- apollo-sequences
- company-context
owned_by_agent: operator
mcps_used:
- apollo-io
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

# /apollo-find-companies -- Target account discovery via Apollo

Search 70M+ companies by industry, size, funding, tech stack, revenue, and hiring activity. Always free — no Apollo credits consumed.

**Imported via:** `/steal` analysis of workflows.io Apollo x Claude Playbook (2026-04-08)

---

## When to use

- Building a target account list for a new campaign
- Finding companies in a specific industry or vertical
- Identifying companies using a competitor's tech stack (displacement plays)
- Finding recently funded companies (buying signal)
- Researching companies actively hiring for specific roles (intent signal)
- Expanding into a new market or vertical
- Building TAM lists from ICP criteria

## When NOT to use

- Researching a specific known company -> `/company-context`
- Finding people at companies -> `/clay-search` (with Apollo fallback)
- Enriching a company for full profile -> `/deepline-enrich` or Apollo MCP directly
- Building full prospect lists with people -> `/build-tam`

---

## Credit usage

**FREE.** Company search does not consume Apollo credits. Search freely.

Company **enrichment** is separate and costs credits. Use `/deepline-enrich` for that.

---

## Framework

### Step 1: Gather search criteria

Ask the user for their search parameters. At minimum, get one of:

| Parameter | Maps to | Example |
|-----------|---------|---------|
| **Company name** | `q_organization_name` | `Apollo` |
| **Domain(s)** | `q_organization_domains_list` | `['apollo.io', 'notion.so']` |
| **Industry keywords** | `q_organization_keyword_tags` | `['SaaS', 'fintech', 'AI']` |
| **HQ location** | `organization_locations` | `['San Francisco, CA', 'United States']` |
| **Exclude locations** | `organization_not_locations` | `['China', 'Russia']` |
| **Employee count** | `organization_num_employees_ranges` | `['50,200', '201,500']` |
| **Revenue range** | `revenue_range` | `{ min: 1000000, max: 50000000 }` |
| **Tech stack** | `currently_using_any_of_technology_uids` | `['salesforce', 'hubspot']` |
| **Total funding** | `total_funding_range` | `{ min: 5000000, max: 50000000 }` |
| **Latest funding amount** | `latest_funding_amount_range` | `{ min: 1000000, max: 10000000 }` |
| **Latest funding date** | `latest_funding_date_range` | `{ min: '2025-01-01', max: '2026-04-08' }` |
| **Hiring for roles** | `q_organization_job_titles` | `['SDR', 'Account Executive']` |
| **Hiring in locations** | `organization_job_locations` | `['London', 'remote']` |
| **Active job postings** | `organization_num_jobs_range` | `{ min: 5, max: 100 }` |
| **Number of results** | `per_page` | `25` (default) |

### Step 2: Ask output format

Before executing, ask:
> "How do you want the results? (1) Markdown table, (2) CSV-ready, or (3) Clay/Sheets-ready format?"

Default to markdown table if the user doesn't specify.

**Markdown table columns:** Company | Domain | Industry | Employees | Location | Has Phone
**CSV/Sheets columns:** company_name, domain, industry, employee_count, location, has_phone, apollo_org_id

### Step 3: Execute search

Use the `mcp__apollo-io__apollo_search_companies` tool with the gathered parameters.

**Tech stack note:** Replace spaces and periods with underscores in technology names:
- Google Analytics -> `google_analytics`
- WordPress.org -> `wordpress_org`

**No currency symbols** in funding/revenue fields. Just numbers: `5000000` not `$5,000,000`.

### Step 4: Present results

Format results based on user's output preference. Always include:
- Total results found
- Number shown on this page
- Whether more pages are available

### Step 5: Suggest next steps

After presenting results, suggest:
- "Want me to **research** any of these companies in depth?" -> `/company-context`
- "Want me to **find people** at these companies?" -> `/clay-search`
- "Want me to see **job postings** at any of these?" -> Apollo MCP `apollo_get_organization_job_postings`
- "Want to **narrow the search** with more filters?"
- "Want to see the **next page**?"

---

## Common search patterns

### Industry + Size + Location (most common)

Keywords: [INDUSTRY]
Employees: [RANGE]
Location: [LOCATION]

### Recently Funded (buying signal)

Keywords: [INDUSTRY]
Latest funding date: last 6 months
Latest funding amount: [MIN] to [MAX]
Location: [LOCATION]

### Actively Hiring (intent signal)

Keywords: [INDUSTRY]
Hiring for: [ROLE TITLES]
Number of jobs: min [N]

### Tech Stack / Competitor Displacement

Tech: [COMPETITOR TOOL]
Employees: [RANGE]
Location: [LOCATION]

---

## Pagination

- Default to 25 results per page. Max is 100.
- Apollo caps at 50,000 records (100 per page x 500 pages).
- If the user asks for more than 100 results, paginate automatically and combine.

## Tips

- Combine funding signals with industry and size for highest-quality account lists.
- Hiring signals tell you where a company is investing right now.
- Use `organization_not_locations` to exclude regions you can't serve.
- For lookalike discovery, find the industry keywords and tech stack of your best customers, then search for matches.
- The more filters you provide, the more targeted the results.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
