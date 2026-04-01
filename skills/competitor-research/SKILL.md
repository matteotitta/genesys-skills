---
name: competitor-research
version: "2.6"
author: genesys-growth
last_updated: 2026-03-19
description: >
  Deep 13-dimension competitor analysis for B2B SaaS. Use when client
  needs competitive context for positioning, sales-enablement, or
  product-messaging. Covers company, product, ICP, pricing, reviews,
  content, launches, SEO/AEO, technographics, hiring signals, GTM
  motion, social presence, and paid advertising.
---

# Competitor research

Run deep competitor analysis across 13 research dimensions for B2B SaaS companies. Produces structured insights with explicit confidence levels, source citations, and actionable data gaps.

**Knowledge type:** `competitor-intel` (see `.claude/rules/ontology.md`)
**Maturity on first run:** emergent → validated after client review

## Attribution standard

**Inline attribution (simplified):**

Use concise inline source references for key data points. Do NOT use the verbose `[VERIFIED: url, date]` block syntax inline — it clutters the output.

- `(Source: Crunchbase)` — direct named source
- `(Source: Vendr)` — Vendr contract data (pricing fallback)
- `(Source: competitor website)` — direct competitor page
- `(Source: Reddit, r/[subreddit])` — community signal, treat as Low confidence unless corroborated
- `(Source: G2)` — review platform data
- `(Source: Apify, [actor name])` — scraped data via Apify MCP
- Omit attribution only for facts that are self-evidently sourced (e.g., a feature listed on the competitor's features page)

**End-of-document audit trail:**

Every output ends with a **Sources & data quality** section (see output template). This table consolidates:
- All URLs with access dates
- Confidence level per dimension
- Data gaps with unverified claims and follow-up actions

**Quality threshold:** minimum 50% verified claims, maximum 20% estimated.

---

## Process Flowchart

```text
┌──────────────────────────────────────────────────────────────┐
│                 COMPETITOR RESEARCH PROCESS                   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 1: INPUT VALIDATION                                     │
│ □ Required: Competitor name, Website URL                      │
│ □ Optional: Market category, client context, specific Qs      │
│ → If ambiguous name: Confirm competitor identity with user    │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 2: DIMENSION RESEARCH (13 dimensions)                   │
│ Step 2.1: Company → funding, team, revenue                    │
│ Step 2.2: Product → features, differentiators                 │
│ Step 2.3: ICP → segments, personas, customers                 │
│ Step 2.4: Pricing → plans, model, value metric                │
│ Step 2.5: Reviews → G2, Capterra, sentiment                   │
│ Step 2.6: Content → blog, formats, lead magnets, events       │
│ Step 2.7: Launches → recent announcements                     │
│ Step 2.8: SEO/AEO → SERP positions (use Ahrefs MCP if avail)  │
│ Step 2.9: Technographics → integrations (limited)             │
│ Step 2.10: Openings → hiring signals                          │
│ Step 2.11: GTM → sales motion, outbound signals, messaging    │
│ Step 2.12: LinkedIn/Social → organic strategy, founder        │
│ Step 2.13: Paid advertising → LinkedIn/Meta/Google ads        │
│ ✓ Checkpoint: All dimensions researched, sources documented   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 3: SYNTHESIS & GAPS                                     │
│ Step 3.1: Assign confidence levels (High/Med/Low)             │
│ Step 3.2: Write executive summary                             │
│ Step 3.3: Document data gaps with follow-up actions           │
│ Step 3.4: Run quality verification                            │
│ ✓ Checkpoint: No unsourced claims, gaps documented            │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 4: AGGREGATE ANALYSIS (Multi-Competitor)                │
│ Trigger: 2+ competitors researched for same client            │
│ Step 4.1: Identify cross-competitor patterns                  │
│ Step 4.2: Build threat matrix                                 │
│ Step 4.3: Analyze market positioning dynamics                 │
│ Step 4.4: Feature parity analysis                             │
│ Step 4.5: Credibility signal audit                            │
│ Step 4.6: Extract strategic recommendations                   │
│ ✓ Checkpoint: Aggregate insights documented                   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ SELF-EVALUATION                                               │
│ □ Completeness: All 13 dimensions addressed?                  │
│ □ Evidence: Every data point has source or "Not available"?   │
│ □ Guardrails: No invented data? No unsourced claims?          │
│ → If issues found: Flag low-confidence areas                  │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ REVIEW GATE: Level 1 (Quick Review)                           │
│ Present: Executive summary, confidence breakdown              │
│ Actions: [Approve] [Dig deeper on X] [Research more]          │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ CHAIN SUGGESTIONS                                             │
│ → "Want me to research additional competitors?"               │
│ → "Ready to run positioning with this competitive context?"   │
│ → "Should I generate battlecard content from this?"           │
│ → "Ready for aggregate analysis across all competitors?"      │
│ → Save as reference example if positive feedback              │
└──────────────────────────────────────────────────────────────┘
```

---

## The Iron Law

**NO DATA POINT WITHOUT SOURCE.**

Every claim has a URL + access date. Every metric cites its origin. "Not available" is always better than invented data.

**No exceptions:**

- "This is widely known" → Still needs a source. Cite it.
- "I read this somewhere" → Find the URL or mark "Not available".
- "I can estimate this" → Estimates need explicit confidence levels and reasoning.
- "The user needs this fast" → Fast + wrong = useless. Take the time.

---

## Red Flags (Stop and Verify)

🚩 About to write revenue/funding without source → STOP. Cite Crunchbase, PitchBook, or mark "[Data needed]".

🚩 About to state competitor feature without verifying → STOP. Check their website/docs first.

🚩 About to invent customer logos → STOP. Only include logos you found on their site.

🚩 About to guess pricing → STOP. Research their pricing page or mark "Pricing not public".

🚩 About to claim market position without evidence → STOP. Cite G2, analyst report, or mark confidence level.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Research this competitor: [name/URL]"
- "Competitor analysis for [company]"
- "Competitive intelligence on [company]"
- "Analyze [company] as a competitor"
- "Battlecard research for [competitor]"
- "Competitive landscape for [market]"
- "Compare [competitor 1] vs [competitor 2]"
- "What's [competitor] doing?"

**Do NOT invoke when:**
- User wants company qualification/traction → Use `company-context` skill
- User wants product messaging only → Use `product-messaging` skill
- User wants to research own company → Use `company-context` or `product-messaging`
- Quick question about one feature → Answer directly without full 11-dimension framework

---

## Input Requirements

### Required Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Competitor name** | Exact company/product name | User provides |
| **Website URL** | Competitor's website | User provides or confirm |

### Optional Inputs (improve quality)

| Input | How It Helps |
|-------|--------------|
| Market category | Helps with disambiguation and keyword selection |
| Client context | Current positioning helps sharpen analysis |
| Specific questions | Focus research on areas of interest |
| Research depth | Deep (default) or comparison matrix |

### Input Validation Checklist

Before proceeding, verify:
- [ ] Competitor name is unambiguous (if not, confirm with user)
- [ ] Website URL is correct and accessible
- [ ] Research mode confirmed (single deep dive or comparison matrix)

**If inputs are missing:** Ask for website URL. If name is ambiguous (e.g., "Bolt" could be multiple companies), confirm which competitor.

---

## Process (Step-by-Step)

### Phase 1: Confirmation & Setup

**Purpose:** Verify competitor identity and establish research scope.

**Steps:**

1. **Step 1.1: Confirm competitor identity**
   - Verify exact company/product name
   - Confirm website URL is correct
   - Check for name disambiguation issues
   - **Output:** Confirmed competitor details

2. **Step 1.2: Determine research mode**
   - Default: Single competitor deep dive (11 dimensions)
   - Alternative: Comparison matrix (3-6 competitors, core dimensions)
   - **Output:** Research mode confirmed

**Phase 1 Checkpoint:**
- [ ] Competitor name unambiguous
- [ ] Website URL verified
- [ ] Research mode selected

### Phase 2: Dimension Research

**Purpose:** Systematically research all 11 dimensions.

**Steps:**

1. **Step 2.1: Company research (Dimension 1)**
   - Search funding: `"[competitor]" crunchbase funding`
   - Search valuation: `"[competitor]" series raised valuation`
   - Fetch about page
   - Extract: Founded, HQ, team size, funding, revenue
   - **Output:** Company profile with sources

2. **Step 2.2: Product research (Dimension 2)**
   - Fetch homepage and features page
   - Fetch documentation if available
   - Extract: Core description, key features, differentiators, platform
   - **Output:** Product profile with sources

3. **Step 2.3: ICP research (Dimension 3)**
   - Fetch customers/case studies page
   - Fetch solutions/industries page
   - Search: `site:reddit.com "[competitor]" use case who uses` — validate segments and uncover niche use cases not on their website
   - Extract: Company size, industries, personas, geos, named customers
   - **Output:** ICP profile with sources

4. **Step 2.4: Pricing research (Dimension 4)**
   - **Step 1:** Fetch `/pricing` page directly
   - **Step 2 (if hidden/gated):** Search `site:g2.com "[competitor]" pricing` — extract plan names, price ranges from review snippets
   - **Step 3 (if still missing):** Search `site:vendr.com "[competitor]"` — Vendr publishes negotiated SaaS contract data; mark findings as `(Source: Vendr)`
   - **Step 4 (if still missing):** Search `site:reddit.com "[competitor]" pricing cost per seat` — extract user-reported pricing, negotiation outcomes, plan details; mark as `(Source: Reddit)`, Low confidence
   - **Step 5 (if all fail):** Mark "Pricing not public — pricing page, G2, Vendr, and Reddit checked"
   - Extract: Model, plans, free tier, enterprise availability, value metric
   - **Output:** Pricing profile with sources

5. **Step 2.5: Reviews research (Dimension 5)**
   - Search: `site:g2.com "[competitor]" reviews`
   - Search: `site:capterra.com "[competitor]" reviews`
   - Search: `site:reddit.com "[competitor]" review` — unfiltered sentiment, bugs, feature complaints
   - Search: `site:reddit.com "[competitor]" problems issues` — surfaces pain points not visible on review platforms
   - Extract: Ratings, review count, sentiment themes, pros/cons, Reddit community signals
   - Note: Reddit findings = Low confidence unless corroborated by G2/Capterra patterns
   - **Output:** Reviews profile with sources

6. **Step 2.6: Content research (Dimension 6)**
   - Fetch blog and resources page
   - Extract: Topics, formats, frequency, lead magnets
   - **Output:** Content profile with sources

7. **Step 2.7: Launches research (Dimension 7)**
   - Search: `"[competitor]" launch announcement [current year]`
   - Search: `site:producthunt.com "[competitor]"`
   - Extract: Product launches, feature announcements (last 3 months)
   - **Output:** Launches profile with sources

8. **Step 2.8: SEO/AEO research (Dimension 8)**
   - **If Ahrefs MCP available (preferred):**
     - `ahrefs.domain_overview({ target: "[competitor.com]" })` → DR, traffic estimate
     - `ahrefs.organic_keywords({ target: "[competitor.com]", limit: 20 })` → top keywords
     - `ahrefs.backlinks({ target: "[competitor.com]", limit: 10 })` → referring domains
     - Confidence: High
   - **If Ahrefs NOT available — use Serper.dev (free fallback):**
     - Requires `SERPER_API_KEY` env var (sign up at serper.dev — 2500 free searches/month)
     - Run 5-10 SERP checks for key category keywords using `WebFetch` or `mcp__exa__web_search_exa`
     - Query patterns: `"[category keyword]"`, `"[competitor name] vs [category]"`, `"best [category] tool"`
     - Extract: competitor ranking position, featured snippet ownership, title/meta copy
     - Use `site:[competitor.com]` search to estimate indexed page count
     - Confidence: Medium (SERP positions accurate; traffic estimates and DR not available without Ahrefs)
   - **If no tools available:** Manual SERP checks for 3-5 key category keywords only
     - Confidence: Low
   - Extract: Domain rating (if Ahrefs), organic traffic estimate, top keywords, SERP positions, indexed pages
   - **Output:** SEO profile with confidence level based on data source

9. **Step 2.9: Technographics research (Dimension 9)**
   - Fetch integrations page
   - Check job postings for tech stack hints
   - Note: Full data requires BuiltWith access
   - Extract: Integrations, visible tech signals
   - **Output:** Technographics profile (limited without premium tools)

10. **Step 2.10: Openings research (Dimension 10)**
    - Fetch careers page
    - Search: `site:linkedin.com/jobs "[competitor]"`
    - Extract: Open roles, hiring departments, seniority, locations
    - **Output:** Openings profile with sources

11. **Step 2.11: GTM research (Dimension 11)**
    - Analyze website messaging and CTAs
    - Check founder LinkedIn activity
    - Search job postings for SDR/BDR/outbound roles — mention of sequencing tools (Outreach, Salesloft, Apollo) signals active outbound
    - Search: `site:reddit.com "[competitor]" sales demo cold email` — surfaces buyer-reported sales experience, outbound aggressiveness, SDR quality
    - Extract: Sales motion (PLG/sales-led/hybrid), primary CTA, channel mix (inbound vs. outbound vs. paid vs. organic), outbound signals, messaging themes
    - **Output:** GTM profile with sources

12. **Step 2.12: LinkedIn / Social research (Dimension 12)**
    - Fetch linkedin.com/company/[competitor] — capture followers, about, recent posts
    - Search: `"[competitor]" site:linkedin.com/posts` for recent post titles and topics
    - Check founder/CMO LinkedIn profiles for post cadence and themes
    - Extract: Follower count + YoY growth, post frequency, content types (product/thought leadership/customer/events), founder activity
    - Note: Impression and reach data require LinkedIn Analytics access — mark [UNAVAILABLE]
    - **Output:** LinkedIn/Social profile with sources

13. **Step 2.13: Paid advertising research (Dimension 13)**

    **IMPORTANT:** All three ad libraries are JS-rendered — raw HTML fetches will fail or return empty. Use Apify actors (preferred) or Firecrawl browser mode.

    **Google Ads Transparency Center (highest priority for B2B SaaS):**
    - **Option A — Apify (preferred):**
      1. `mcp__apify__search-actors` with query `"Google Ads Transparency"` — select highest-rated actor
      2. Fetch actor input schema with `mcp__apify__fetch-actor-details`
      3. Call actor with `{ "advertiserDomain": "[competitor.com]" }` or equivalent input
      4. Extract: active campaign count, ad copy themes, CTA patterns, geographic targeting
    - **Option B — Firecrawl browser:**
      1. `mcp__firecrawl__firecrawl_browser_create` — launch browser session
      2. Navigate to `https://adstransparency.google.com/?region=anywhere`
      3. Search for competitor domain in the search input
      4. `mcp__firecrawl__firecrawl_browser_execute` — extract ad cards from results
    - **If both fail:** Mark "Google Ads data unavailable — JS wall. Manual check at adstransparency.google.com required" in data gaps table
    - Note: Google paid search is HIGH probability for B2B SaaS at scale — always attempt this check

    **LinkedIn Ads Library:**
    - **Option A — Apify (preferred):**
      1. `mcp__apify__search-actors` with query `"LinkedIn Ads Library scraper"`
      2. Call actor with `{ "companyHandle": "[competitor-linkedin-handle]" }` or `{ "companyUrl": "linkedin.com/company/[handle]" }`
      3. Extract: ad types (sponsored content, message ads, lead gen forms), creative themes, CTA patterns, running dates
    - **Option B — Firecrawl:**
      1. Direct scrape: `https://www.linkedin.com/ad-library/search?companyIds=[handle]`
      2. If JS-blocked: use `mcp__firecrawl__firecrawl_browser_create` + execute
    - **If no ads found:** Mark as verified absence — "No active LinkedIn Ads found (verified YYYY-MM-DD)" — absence is a high-confidence signal that this competitor is sales-led or organic-first

    **Meta Ads Library:**
    - Fetch: `https://www.facebook.com/ads/library/?q=[competitor name]&search_type=keyword_unordered&active_status=active`
    - Extract: active ad count, creative formats, copy themes, CTA patterns
    - For B2B enterprise: low probability of Meta activity — mark "No Meta ads found" if not found (not a data gap)

    - "No active ads found" is a high-confidence data point — treat as verified GTM signal, not a data gap
    - **Output:** Paid advertising profile per platform with confidence levels

**Phase 2 Checkpoint:**
- [ ] All 13 dimensions researched
- [ ] Sources documented for each finding
- [ ] "Not available" noted for missing data

### Phase 3: Synthesis & Gaps

**Purpose:** Compile findings and document limitations.

**Steps:**

1. **Step 3.1: Assign confidence levels**
   - High: Primary source, recent, verifiable
   - Medium: Secondary source, analyst estimate
   - Low: Inferred, single unverified source
   - **Output:** Confidence levels assigned

2. **Step 3.2: Compile executive summary**
   - 2-3 paragraphs summarizing key findings
   - Highlight competitive strengths and weaknesses
   - **Output:** Executive summary

3. **Step 3.3: Document data gaps**
   - What couldn't be found
   - What requires premium tools
   - Suggested follow-up actions
   - **Output:** Data gaps section

4. **Step 3.4: Quality verification**
   - Run quality checklist
   - Verify no unsourced claims
   - Confirm surprising claims corroborated
   - **Output:** Verified output

**Phase 3 Checkpoint:**
- [ ] Confidence levels assigned
- [ ] Executive summary written
- [ ] Data gaps documented
- [ ] No unsourced claims

### Phase 4: Aggregate Analysis (Multi-Competitor)

**Purpose:** Synthesize cross-competitor patterns into strategic intelligence after completing 2+ individual deep dives for the same client.

**Trigger conditions:**
- 2+ competitors researched for the same client project
- User explicitly requests aggregate analysis or cross-competitor insights
- Chain suggestion accepted after completing 2nd+ competitor deep dive

**Steps:**

1. **Step 4.1: Pattern identification**
   - Read all competitor deep dives in the client's competitors folder
   - Extract recurring themes across dimensions (funding patterns, feature convergence, market consolidation, pricing models)
   - Identify market dynamics (who's consolidating, who's struggling, what's commoditized)
   - **Output:** Cross-competitor patterns summary

2. **Step 4.2: Threat matrix construction**
   - Rank competitors by threat level: PRIMARY / ENTERPRISE TIER / DIRECT ICP / STEALTH WATCH / LOW / DEFUNCT
   - Justify each ranking with evidence from individual deep dives
   - Identify exploitable vulnerabilities per competitor
   - **Output:** Threat matrix table

3. **Step 4.3: Market positioning dynamics**
   - Map competitors on relevant spectrums (SMB↔Enterprise, Organic↔VC/PR, Feature depth, etc.)
   - Track ranking trends over time (AdviserSoftware.com, G2, etc.)
   - Identify white space and crowded zones
   - **Output:** Positioning maps with narrative analysis

4. **Step 4.4: Feature parity analysis**
   - Build capability comparison table (all competitors × key features)
   - Classify each feature by market maturity: Commoditized / Differentiator / Emerging
   - Identify battleground features where positioning is contested
   - **Output:** Feature parity matrix with maturity classification

5. **Step 4.5: Credibility signal audit**
   - Compare funding, awards, press, enterprise logos, founder visibility, content strategy across all competitors
   - Identify where the client is ahead and behind on credibility signals
   - **Output:** Credibility comparison table with gap analysis

6. **Step 4.6: Strategic recommendations**
   - Extract 3-5 actionable recommendations from pattern analysis
   - Each recommendation includes: rationale, evidence, suggested actions, effort/impact scoring
   - Link recommendations to specific competitive vulnerabilities
   - Surface follow-up questions that only the client can answer (product capabilities, customer permissions, etc.)
   - **Output:** Strategic recommendations with evidence

**Phase 4 Checkpoint:**
- [ ] All individual deep dives referenced and cross-checked
- [ ] Threat rankings justified with evidence (not opinion)
- [ ] Feature parity table uses "Unknown" where client capabilities are unverified
- [ ] Strategic recommendations are actionable (not generic "be better")
- [ ] Data gaps section identifies what only the client can answer
- [ ] Sources aggregated from all deep dives

**Phase 4 Output:** Save as `MMYY-aggregate-insights.md` in the client's competitors folder.

---

## Core Frameworks

### 13 Research Dimensions

| # | Dimension | What to Find | Primary Sources |
|---|-----------|--------------|-----------------|
| 1 | **Company** | Revenue, funding, team size, HQ | Crunchbase, Tracxn, LinkedIn |
| 2 | **Product** | Features, capabilities, differentiators | Website, docs, G2 |
| 3 | **ICP** | Segments, geos, company sizes | Case studies, solutions pages |
| 4 | **Pricing** | Plans, amounts, value metrics | Pricing page, G2 |
| 5 | **Reviews** | Ratings, sentiment, themes | G2, Capterra, TrustRadius |
| 6 | **Content** | Topics, formats, cadence, owned events | Blog, resources, LinkedIn, event pages |
| 7 | **Launches** | Recent product/feature announcements | LinkedIn, Product Hunt, press releases |
| 8 | **SEO/AEO** | Rankings, traffic, gaps | SERP analysis (limited) |
| 9 | **Technographics** | Tech stack, integrations | Integrations page (limited) |
| 10 | **Openings** | Job postings, hiring signals | Careers, LinkedIn Jobs |
| 11 | **GTM** | Sales motion, inbound/outbound mix, outbound signals, messaging | Website, job descriptions, LinkedIn |
| 12 | **LinkedIn / Social** | Organic posting strategy, content types, frequency, founder activity, follower count | LinkedIn company page, founder profiles |
| 13 | **Paid advertising** | Active ad campaigns, creative themes, ICP signals in copy, CTAs, spend signals | LinkedIn Ads Library, Meta Ads Library, Google Ads Transparency Center |

### Confidence Scoring

| Level | Definition | Example |
|-------|------------|---------|
| **High** | Primary source, recent, verifiable | Company blog, press release, official pricing page |
| **Medium** | Secondary source, analyst estimate | Sacra estimates, TechCrunch reporting, Tracxn data |
| **Low** | Inferred, single unverified source | Forum posts, old articles, indirect mentions |

### Competitor Disambiguation

Many company names are ambiguous. Common issues:

| Ambiguous Name | Possible Meanings |
|----------------|-------------------|
| Bolt | Ride-sharing, Fintech, Bolt.new (AI coding) |
| Cursor | AI code editor, Design tool |
| Base | Database, Base44 (AI app builder) |
| Linear | Issue tracking, Other |

**Resolution approach:**
1. Use domain-qualified searches: "bolt.new" not "bolt"
2. Include category context: "Cursor AI coding" not "Cursor"
3. Check for parent companies: Bolt.new is part of StackBlitz
4. When in doubt, confirm with user before starting

### Research Modes

**Single competitor mode (default):**
- Full 11 dimensions
- Maximum depth
- Executive summary + detailed findings
- Data gaps with follow-up actions

**Comparison matrix mode:**
- 3-6 competitors
- Core dimensions only: Company, Product, Pricing, ICP, Reviews
- Tabular output
- Key differentiators summary

---

## Output Format

### Standard Output Structure (Single Competitor)

**IMPORTANT**: All competitor files must follow this exact structure. Do not invent alternative header formats like "competitive intelligence analysis", "competitive analysis", or "Competitive Intelligence Report". The title is always `# Competitor research: [Name]`.

```markdown
# Competitor research: [Competitor Name]

**Website**: [URL]
**Category**: [Market category]
**Research date**: [YYYY-MM-DD]

---

## Executive summary

[2-3 paragraphs summarizing key findings, competitive strengths, weaknesses, and strategic implications]

---

## Confidence summary

| Confidence level | Data points |
|------------------|-------------|
| Verified         | [N]         |
| Inferred         | [N]         |
| Estimated        | [N]         |
| Unavailable      | [N]         |

---

## 1. Company

| Metric | Finding | Source |
|--------|---------|--------|
| Founded | [Year] | (Source: Crunchbase) |
| HQ | [Location] | (Source: LinkedIn) |
| Team size | [Count] | (Source: LinkedIn) |
| Total funding | [Amount] | (Source: Crunchbase) |
| Latest round | [Stage, amount, date] | (Source: TechCrunch) |
| Revenue estimate | [Amount/range] | (Source: Sacra) |

---

## 2. Product

**Core description:** [1-2 sentences]

**Key features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Stated differentiators:**
- [Differentiator 1]
- [Differentiator 2]

**Platform:** [Web/Desktop/Mobile/API]

**Source**: [competitor website]

---

## 3. ICP

| Dimension | Finding | Source |
|-----------|---------|--------|
| Company size | [Startup/SMB/Enterprise] | (Source: case studies page) |
| Industries | [List] | (Source: solutions page) |
| Personas | [Roles] | (Source: competitor website) |
| Geographic focus | [Regions] | (Source: careers page) |

**Named customers:** [List of public logos] (Source: competitor website)

---

## 4. Pricing

| Plan | Price | Includes |
|------|-------|----------|
| [Plan 1] | [Price] | [Key features] |
| [Plan 2] | [Price] | [Key features] |
| Enterprise | [Contact/Custom] | [Key features] |

**Pricing model:** [Per seat/Usage/Flat/Hybrid]
**Free tier:** [Yes/No, details]
**Value metric:** [What they charge for]
**Source**: [pricing page / G2 / Vendr / Reddit — note which was used]

---

## 5. Reviews

| Platform | Rating | Review Count |
|----------|--------|--------------|
| G2 | [X/5] | [N] |
| Capterra | [X/5] | [N] |
| TrustRadius | [X/10] | [N] |

**Top praised:**
- [Theme 1]
- [Theme 2]

**Top criticized:**
- [Theme 1]
- [Theme 2]

**Recent sentiment (last 3 months):** [Summary]

**Reddit signals:** [Community-reported issues, pain points, or praise — marked Low confidence unless corroborated]

---

## 6. Content

**Blog frequency:** [Posts per week/month]
**Top topics:**
- [Topic 1]
- [Topic 2]

**Content formats:** [Blog/Podcast/Video/Guides]
**Lead magnets:** [List]
**Newsletter:** [Yes/No]

**Source**: [competitor blog URL]

---

## 7. Launches

| Date | Announcement | Type | Source |
|------|--------------|------|--------|
| [Date] | [Launch] | Product/Feature/Partnership | [URL] |

**If none:** No major launches in last 3 months.

---

## 8. SEO/AEO

### If Ahrefs MCP Available:

| Metric | Value | Source |
|--------|-------|--------|
| **Domain Rating (DR)** | [Score]/100 | Ahrefs |
| **Organic traffic (est.)** | [Number]/mo | Ahrefs |
| **Referring domains** | [Number] | Ahrefs |
| **Organic keywords** | [Number] | Ahrefs |

**Top organic keywords:**

| Keyword | Volume | Position | Traffic % |
|---------|--------|----------|-----------|
| [Keyword 1] | [Vol] | [Pos] | [%] |
| [Keyword 2] | [Vol] | [Pos] | [%] |
| [Keyword 3] | [Vol] | [Pos] | [%] |

**Confidence:** High (Ahrefs data)

### If Ahrefs MCP NOT Available:

**Note:** Full SEO data requires Ahrefs MCP. Findings below are based on manual analysis.

**SERP positions for key terms:**

| Keyword | Position | Notes |
|---------|----------|-------|
| [Keyword 1] | [Position] | [Context] |
| [Keyword 2] | [Position] | [Context] |

**Estimated indexed pages:** [Rough count from site: search]
**Content volume:** [Blog post count estimate]

**Confidence:** Low (manual analysis only)

---

## 9. Technographics

**Note:** Full technographics require BuiltWith access. Findings below are from public sources.

**Integrations:** [List from integrations page]
**Tech stack signals:** [From job postings]

**Limitations:** Full stack data requires BuiltWith — marked "Not available."

---

## 10. Openings

| Department | Open Roles | Seniority | Location |
|------------|------------|-----------|----------|
| Engineering | [N] | [Junior/Senior] | [Remote/Location] |
| Sales | [N] | [Junior/Senior] | [Remote/Location] |
| Marketing | [N] | [Junior/Senior] | [Remote/Location] |

**Hiring signals:** [Growth, new function, replacement]

**Source**: [careers page URL]

---

## 11. GTM

**Sales motion:** [PLG/Sales-led/Hybrid]
**Primary CTA:** [Free trial/Demo/Contact]
**Channel mix:** [Inbound/Outbound/Paid/Organic weighting — estimated]

**Outbound signals:**
- SDR/BDR hiring: [Yes/No — from careers page]
- Outbound tools visible in JDs: [Outreach/Salesloft/Apollo/other]
- Cold email footprint: [Signals from review sites or prospects]
- Buyer-reported experience: [Reddit signals about sales motion — Low confidence]

**Messaging themes:**
- [Theme 1]
- [Theme 2]

**Positioning statement:** [If identifiable]

**Source**: [competitor website, job descriptions]

---

## 12. LinkedIn / Social

**Company page:** [URL] | **Followers:** [count] | **YoY growth:** [%]

**Post frequency:** [X/week or /month]
**Content mix (estimated):**
- Product/feature: [%]
- Thought leadership: [%]
- Customer stories: [%]
- Events/webinars: [%]
- Other: [%]

**Top content themes:**
- [Theme 1]
- [Theme 2]

**Founder/exec LinkedIn activity:**
- [Name, role]: [Frequency, themes]

**Note:** Impression and reach data require LinkedIn Analytics access — not available via public sources

**Source**: [LinkedIn company page URL]

---

## 13. Paid advertising

### Google Ads Transparency Center
**Active campaigns:** [Yes/No — verified YYYY-MM-DD]
**Ad types:** [Search / Display / Video]
**Ad copy themes:**
- [Theme 1]
**Keywords visible in headlines:** [List]
**Primary CTA:** [Demo / Trial / Contact / Download]
**Data method:** [Apify actor / Firecrawl browser / manual check]

### LinkedIn Ads Library
**Active campaigns:** [Yes/No — verified YYYY-MM-DD]
**Ad types:** [Sponsored content / Message ads / Lead gen forms / Dynamic ads]
**Creative themes:**
- [Theme 1]
**Visible ICP signals in ad copy:** [Notes]
**Primary CTA:** [Book demo / Free trial / Download / etc.]
**Data method:** [Apify actor / Firecrawl browser / manual check]

### Meta Ads Library
**Active campaigns:** [Yes/No — verified YYYY-MM-DD]
**Ad count:** [N active ads or "No active ads found"]
**Creative themes:**
- [Theme 1]
**Targeting signals:** [Inferred from copy: persona, pain point, offer]

---

## Sources & data quality

| Dimension | Source | URL | Access date | Confidence |
|-----------|--------|-----|-------------|------------|
| Company | Crunchbase | [URL] | [YYYY-MM-DD] | Verified |
| Company | LinkedIn | [URL] | [YYYY-MM-DD] | Verified |
| Product | Competitor website | [URL] | [YYYY-MM-DD] | Verified |
| Pricing | [Pricing page / G2 / Vendr / Reddit] | [URL] | [YYYY-MM-DD] | [Verified/Inferred/Estimated] |
| Reviews | G2 | [URL] | [YYYY-MM-DD] | Verified |
| Reviews | Reddit | [URL] | [YYYY-MM-DD] | Estimated |
| SEO | [Ahrefs / Serper.dev / Manual] | — | [YYYY-MM-DD] | [Verified/Inferred/Estimated] |
| Ads | [Apify / Firecrawl / Manual] | — | [YYYY-MM-DD] | [Verified/Estimated] |
| [Add rows as needed] | | | | |

### Data gaps & unverified claims

| Dimension | Claim or gap | Why unverified | Follow-up action |
|-----------|--------------|----------------|------------------|
| Revenue | [Estimate if used] | Secondary source only | Check for recent press/Sacra |
| Ads | [Platform if failed] | JS wall / scrape failed | Manual browser check |
| [Dimension] | [Missing data] | [Not available/Requires premium] | [Suggestion] |

---

## Iteration Prompts

After reviewing this research, consider:
1. "Should I research additional competitors?"
2. "Want me to create a comparison matrix?"
3. "Should I generate battlecard content from this?"

---

## Skill Improvement Notes

**What worked well:**
- [Auto-captured]

**Potential improvements:**
- [Auto-captured]
```

### Comparison Matrix Output

```markdown
# Competitor comparison matrix

**Competitors analyzed:** [N]
**Research date**: [YYYY-MM-DD]

---

## Company overview

| Competitor | Founded | Funding | Team Size | Revenue Est. |
|------------|---------|---------|-----------|--------------|
| [Comp 1] | [Year] | [Amount] | [Count] | [Range] |
| [Comp 2] | [Year] | [Amount] | [Count] | [Range] |

---

## Product Comparison

| Competitor | Core Value Prop | Key Differentiator |
|------------|-----------------|-------------------|
| [Comp 1] | [1 sentence] | [1 differentiator] |
| [Comp 2] | [1 sentence] | [1 differentiator] |

---

## Pricing Comparison

| Competitor | Model | Entry Price | Enterprise |
|------------|-------|-------------|------------|
| [Comp 1] | [Type] | [Price] | [Yes/No/Contact] |
| [Comp 2] | [Type] | [Price] | [Yes/No/Contact] |

---

## ICP Comparison

| Competitor | Company Size | Primary Persona |
|------------|--------------|-----------------|
| [Comp 1] | [Size] | [Role] |
| [Comp 2] | [Size] | [Role] |

---

## Reviews Comparison

| Competitor | G2 Rating | Review Count | Top Praise | Top Criticism |
|------------|-----------|--------------|------------|---------------|
| [Comp 1] | [X/5] | [N] | [Theme] | [Theme] |
| [Comp 2] | [X/5] | [N] | [Theme] | [Theme] |

---

## Key Differentiators Summary

[2-3 paragraphs analyzing competitive positioning, white space, and strategic implications]

---

## Data Gaps

| Competitor | Missing Data | Follow-up |
|------------|--------------|-----------|
| [Comp 1] | [What] | [Suggestion] |
| [Comp 2] | [What] | [Suggestion] |
```

---

## What Good Looks Like

### Example 1: Linear (Issue Tracking, Single Competitor)

**Input context:**
```
Competitor: Linear
Website: linear.app
Goal: Deep dive for client in project management space
```

**Expected output excerpt:**
```markdown
## Executive Summary

Linear is a $1.25B+ issue tracking platform that has captured significant market share by focusing on speed, design quality, and developer experience. Founded in 2019, they've raised $52M and built a team of 50-100 employees.

Their competitive positioning centers on being "the issue tracker built for software teams" with an emphasis on keyboard shortcuts, sub-200ms performance, and opinionated workflows. They've successfully differentiated from Jira by targeting modern engineering teams who value speed over configurability.

Key competitive threats: Their pricing ($8/user/month) and PLG motion make them accessible to startups but they're increasingly pushing into enterprise. Recent launches include AI-powered triage and advanced roadmapping features, signaling expansion beyond core issue tracking.

---

## 1. Company

| Metric | Finding | Confidence | Source |
|--------|---------|------------|--------|
| Founded | 2019 | High | Crunchbase |
| HQ | San Francisco | High | LinkedIn |
| Team size | 50-100 | Medium | LinkedIn estimate |
| Total funding | $52M | High | Crunchbase |
| Latest round | Series B, $35M, Jan 2022 | High | TechCrunch |
| Revenue estimate | $30-50M ARR | Medium | Sacra estimate |
```

**Why this is good:**
- Executive summary provides strategic context
- Every data point has confidence level and source
- Acknowledges estimate uncertainty
- Actionable competitive intelligence

### Anti-Examples (What to Avoid)

| Bad Pattern | Why It's Bad | Better Approach |
|-------------|--------------|-----------------|
| "Revenue: $25M" (no qualifier) | Appears as fact when likely estimate | "Revenue estimate: $25M ARR (Medium confidence, Sacra)" |
| "Their tech stack uses React" (guessed) | Invented data | "Tech stack: Not available (requires BuiltWith)" |
| Missing dimensions | Incomplete analysis | Include all 11, mark "Not available" if no data |
| No data gaps section | Missing actionable follow-up | Always include gaps with suggested actions |
| "They seem to be struggling" | Unsourced interpretation | Cite specific signals or mark as inference |

---

## Anti-Hallucination Guardrails

1. **Never invent data.** Mark "Not available" or "Unknown" if not found
2. **Always cite sources inline.** Use `(Source: name)` for key data points — no verbose `[VERIFIED: url, date]` blocks inline
3. **Consolidate sources at the end.** Full URLs, access dates, and confidence levels go in the "Sources & data quality" table
4. **Acknowledge premium tool limits.** SEO and technographics need paid tools — state which tool was used (Ahrefs / Serper.dev / manual)
5. **Verify surprising claims.** If data seems unusual, search for corroboration
6. **Explicit gaps over false data.** "Not available" is always better than guessing
7. **Reddit is Low confidence by default.** Corroborate with G2/Capterra before upgrading to Medium
8. **Vendr pricing = Medium confidence.** User-negotiated data may differ from list price — always note this
9. **Ads "no data found" ≠ data gap.** If scraping returns no ads, mark as "no active ads verified" — it's a high-confidence GTM signal

### Missing Data Labels

Use these explicit labels when data cannot be found:

| Label | When to Use |
|-------|-------------|
| "Not available" | Data doesn't exist publicly |
| "Unknown" | Data may exist but not found |
| "Requires premium tool" | Data exists but needs paid access (Ahrefs, BuiltWith) |
| "Conflicting sources" | Multiple sources disagree |
| "Ads data unavailable — JS wall" | Scraping failed, manual browser check needed |

---

## Quality Checklist (Pre-Delivery)

### Data Quality
- [ ] Every data point has source URL or explicit "Not available"
- [ ] Confidence levels assigned to key metrics
- [ ] No invented or estimated numbers without clear labeling
- [ ] Disambiguation confirmed for ambiguous names
- [ ] Surprising claims corroborated with second source

### Coverage Quality
- [ ] All 13 dimensions addressed (single competitor mode)
- [ ] Core 5 dimensions addressed (comparison matrix mode)
- [ ] Executive summary provides strategic insight
- [ ] Data gaps section completed with follow-up actions

### Format Quality
- [ ] Output header with date and font specification
- [ ] Tables properly formatted
- [ ] Confidence summary included
- [ ] Freshness noted for time-sensitive data

---

## Self-Evaluation Protocol

After generating competitor research output, automatically run these checks:

### Completeness Check

- [ ] All 13 dimensions addressed (single competitor mode)?
- [ ] Core 5 dimensions addressed (comparison matrix mode)?
- [ ] Executive summary provides strategic insight?
- [ ] Data gaps section complete with follow-up actions?
- [ ] Any placeholders remaining?

### Evidence Quality Check

- [ ] Every data point has source URL or explicit "Not available"?
- [ ] Confidence levels assigned to all key metrics?
- [ ] Ratio of High vs Medium vs Low confidence acceptable?
- [ ] No invented or estimated numbers without clear labeling?

### Guardrail Check

- [ ] No invented data? Every claim sourced?
- [ ] Disambiguation confirmed for ambiguous names?
- [ ] Surprising claims corroborated with second source?
- [ ] Premium tool limitations explicitly noted?

### Self-Roast Questions

Ask internally:

1. "If the user cross-checked this research, would any claims fail verification?"
2. "Am I being honest about data gaps, or hiding them in vague language?"
3. "Does the executive summary provide real strategic insight or just summarize facts?"
4. "Would a competitive intelligence analyst consider this thorough?"
5. "Are my confidence levels accurate, or am I being overconfident?"

### Improvement Suggestions

Based on evaluation, surface to user:

> "This research could be stronger if [specific improvement]. Want me to [action]?"

Example prompts:

- "The revenue estimate has low confidence — want me to search for additional sources?"
- "The ICP section is thin — want me to dig deeper into their case studies?"
- "Missing recent launch data — want me to check Product Hunt and LinkedIn announcements?"

---

## Post-Output: Iteration Prompts

After delivering output, proactively offer:

### Refinement Prompts
1. "Should I dig deeper on any dimension?"
2. "Want me to verify any low-confidence data?"
3. "Should I expand the executive summary analysis?"

### Expansion Prompts
1. "Ready to research additional competitors?"
2. "Should I create a comparison matrix?"
3. "Want me to generate battlecard content from this?"

### Quality Prompts
1. "Any findings that seem inconsistent?"
2. "Should I search additional sources for gaps?"
3. "Want me to corroborate any surprising claims?"

---

## Skill Auto-Update Protocol

### Feedback Signal Detection

| User Signal | Interpretation | Action |
|-------------|----------------|--------|
| "Great research" / "This is thorough" | High quality match | Log as positive pattern, offer to save as reference |
| "This data is outdated" | Source freshness issue | Log for source update |
| "Missing [X] dimension" | Coverage gap | Log new dimension to consider |
| "Source was wrong" | Source reliability issue | Flag source, find alternatives |
| "Good find on [X]" | Effective search pattern | Capture as reusable pattern |
| "Need more depth on [dimension]" | Depth preference | Log user preference |
| Quick approval (<5 min) | Output was strong | Reinforce patterns used |

### Output as Reference Example

When user approves output (explicit "great research" or quick approval):

1. **Ask:** "This competitor research met your expectations. Want me to save it as a reference example for this skill?"

2. **If approved:**
   - Extract the full competitor research output
   - Anonymize client-specific context if needed (or keep with permission)
   - Save to `/claude skills/context-skills/competitor-research/references/examples/[date]-[competitor-slug].md`
   - Update "What Good Looks Like" section with link to new example
   - Add to reference files table

**Reference Example Format:**

```markdown
<!--
REFERENCE EXAMPLE
Skill: competitor-research
Generated: YYYY-MM-DD
Competitor: [competitor name]
Quality Rating: Approved by user
-->

# Example: [Brief description of what makes this research effective]

## Context

- **Competitor type:** [Category, funding stage, market position]
- **Research mode:** [Single competitor / Comparison matrix]
- **Why this worked:** [Key success factors]

## Research Summary

- **Dimensions covered:** [X]/11
- **Confidence breakdown:** High: X | Medium: Y | Low: Z
- **Key insight:** [Most valuable finding]

## Full Output

[Complete competitor research output as delivered]

---

## Learning Notes

- [Search pattern that worked well]
- [Source that provided high-quality data]
- [Any caveats or competitor-specific factors]
```

### Improvement Tracking

After each skill use, note:
1. **Dimension coverage:** Which dimensions had full vs. partial data?
2. **Source quality:** Mix of High/Medium/Low confidence?
3. **Premium tool gaps:** What couldn't be found without paid tools?
4. **New patterns:** Any new search strategies that worked?

### Pattern Detection Rules

When same feedback received 3+ times for this skill:

1. **Surface pattern:** "I've noticed [pattern] in competitor research feedback. Should I update the skill to [proposed change]?"

2. **If approved:** Propose specific SKILL.md edit with:
   - Current behavior
   - Proposed change
   - Affected sections

3. **Log in changelog** with feedback reference

**Common patterns to watch for:**

- Users frequently requesting deeper research on specific dimensions → Enhance that dimension's search patterns
- Sources frequently returning "Not available" → Find alternative sources
- Confidence levels often disputed → Calibrate confidence scoring
- Users requesting additional dimensions → Consider adding to framework

### Suggested Skill Update Format

```markdown
## Proposed Skill Update

**Skill:** competitor-research
**Triggered by:** [feedback pattern]
**Frequency:** [X occurrences]

**Current behavior:**
[What the skill does now]

**Proposed change:**
[Specific modification]

**Implementation:**
[Exact lines to change in SKILL.md]

**Approve this update?** [Yes/No]
```

---

## Reference Files

| File | Purpose | Status |
|------|---------|--------|
| `references/output-template.md` | Single competitor output structure | ✓ Core |
| `references/matrix-template.md` | Multi-competitor comparison tables | ✓ Core |
| `references/search-patterns.md` | Detailed search queries per dimension | ✓ Core |
| `references/source-urls.md` | Common data source URL patterns | ✓ Core |
| `references/example-linear.md` | Worked example: Linear | ✓ Example |
| `references/example-lovable.md` | Worked example: Lovable | ✓ Example |
| `references/examples/` | User-approved competitor research outputs | ✓ Examples |

---

## Integration with Other Skills

### Competitor-research feeds INTO these skills

| Skill | What It Receives | How It Uses It |
|-------|------------------|----------------|
| **positioning** | Competitive alternatives, market context | Alternative mapping, differentiation angles |
| **product-messaging** | Competitor weaknesses, positioning gaps | Sharpens client messaging, contrast points |
| **sales-enablement** | Full competitor profiles, weaknesses | Battlecard content, objection handling |

### Competitor-research receives FROM these skills

| Skill | What It Provides | How Competitor-research Uses It |
|-------|------------------|--------------------------------|
| **company-context** | Client context, market position | Provides comparison baseline |

### Recommended workflow sequences

**Sequence 1: Comprehensive competitive analysis**
```text
company-context → competitor-research → positioning
```

**Sequence 2: Battlecard creation**
```text
competitor-research → sales-enablement
```

**Sequence 3: Full PMM stack**
```text
icp-behavioural + competitor-research → positioning → product-messaging → sales-enablement
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.4 | 2026-03-17 | Expanded from 11 → 13 dimensions. Added D12 (LinkedIn/Social): organic posting strategy, content types, founder activity, follower count. Added D13 (Paid advertising): LinkedIn Ads Library, Meta Ads Library, Google Ads Transparency Center — includes "no ads" as verified data point. Expanded D11 (GTM) with outbound signals: SDR/BDR hiring, tool stack detection from JDs, channel mix estimation. Added process steps 2.12 and 2.13. Added Apify RAG browser and ads library URL patterns to MCP integrations. Updated all quality checklists and self-evaluation sections from 11 → 13. |
| 2.3 | 2026-02-06 | Phase 4: Aggregate Analysis — new cross-competitor synthesis phase triggered after 2+ deep dives for same client. Includes threat matrix, feature parity, credibility signals, market positioning dynamics, and strategic recommendations. New `aggregate-insights` output type. |
| 2.1 | 2026-01-21 | Agentic enhancements: YAML frontmatter with dependencies/outputs/triggers, visual flowchart, self-evaluation protocol, enhanced auto-update with reference example capture, upstream/downstream integration map |
| 2.0 | 2026-01-16 | Refactored to v2.0 template: structured phases, confidence scoring, iteration prompts, auto-update rules |
| 1.0 | Original | Initial skill creation with 11 dimensions |

---

## MCP data integration

**Level:** 0 — Context (heavy pulls)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Exa** | Company profile per competitor | `company_research_exa` | Per competitor |
| **Firecrawl** | Full competitor site crawl + map | `firecrawl_crawl`, `firecrawl_map` | Per competitor |
| **Apify** | G2/Capterra reviews | `call-actor` (g2-scraper) | Per competitor |
| **YouTube** | Competitor video content/presence | `get_transcript` | If YouTube channel exists |
| **GTM** | Competitor tracking patterns | `list_tags` | If container accessible |
| **Slack** | Internal competitive intel threads | `slack_search_public` | Always |
| **Granola** | Client call mentions of competitors | `search_meetings` | Always |
| **Apify RAG browser** | LinkedIn Ads Library, Meta Ads Library, Google Ads Transparency Center | `apify-slash-rag-web-browser` | D13 per competitor |
| **Firecrawl** | Full site crawl + ads library pages (when credits available) | `firecrawl_scrape` | Per competitor; fallback to Apify if credits exhausted |

**D13 URL patterns:**

| Platform | URL pattern | Priority |
|----------|------------|----------|
| LinkedIn Ads Library | `linkedin.com/ad-library/search?companyIds=[handle]` | High (B2B standard) |
| Google Ads Transparency | `adstransparency.google.com` (search by domain) | High (search ads common) |
| Meta Ads Library | `facebook.com/ads/library/?q=[competitor name]` | Low (B2B enterprise unlikely) |

### Fallback (no MCP)

- WebSearch + WebFetch for competitor sites and profiles
- Manual G2/Capterra review search
- Manual competitive intel gathering
