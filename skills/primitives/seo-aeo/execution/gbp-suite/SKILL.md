---
name: gbp-review-strategy
version: '1.0'
last_updated: 2026-03-16
author: genesys-growth
description: Analyzes review velocity, sentiment distribution, and competitor review patterns, then produces branded response
  templates for GBP review management. Delivers a review teardown report, response templates by sentiment tier (positive,
  neutral, negative), review solicitation strategy, and velocity benchmarks. Triggered by "review strategy", "review teardown",
  "review templates", "GBP reviews", or routed from /local-seo-audit orchestrator. Depends on company-context and gbp-category-audit.
  Feeds into gbp-content-engine. NOT for GBP post scheduling — use /gbp-content-engine instead.
goal: Analyzes review velocity, sentiment distribution, and competitor review patterns, then produces branded response templates
  for GBP review management.
outcome: Analyzes review velocity, sentiment distribution, and competitor review patterns, then produces branded response
  templates for GBP review management. Delivers a review teardown report, response templates by sentiment tier (positive,
  neutral, negative), review solicitation strategy, and velocity...
primitive: seo-aeo
sub_primitive: execution
ontology_type: content-audit
review_gate: 1
inputs:
  required: []
  recommended:
  - company-context
  - gbp-category-audit
- type: local-seo-audit
  feeds_into:
  - local-seo-audit
depends_on: []
- local-seo-audit
owned_by_agent: operator
mcps_used:
- exa
- firecrawl
- gdrive
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
slim_exemption: gbp-cluster-split-deferred-2026-04-30
---

## Research source (Exa)

**Default:** Exa, per `.claude/rules/exa-protocol.md` (auto-loaded for research, audit, competitor, ICP, AEO, content sourcing, sales prospecting work).

**Primary Exa tools for this skill:** `web_search_exa`.

**Use case:** competitor review pattern research.

**Tool surface during the migration window:**
- New plugin (preferred): `mcp__plugin_exa_exa__web_search_exa` (after `claude plugin i exa@claude-plugins-official`).
- Legacy MCP (still mounted): `mcp__exa__web_search_exa`.
- Both backends route to the same Exa API — they don't double-bill.

**Citation:** every Exa-derived claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` per `.claude/rules/ontology.md`.

**Quality gate (research outputs):** ≥3 sources per major claim, ≥50% `[VERIFIED]` confidence, date filter for any "recent / latest" claim, no fallback to `WebSearch` without flagging the data gap.

**Worked examples + tool catalog:** `.claude/skills/meta-skills/exa/`.

# GBP review strategy

Analyzes competitor review velocity, keyword mentions in reviews, neighborhood mentions, and recurring complaints. Then generates review response templates (5-star, 4-star, 3-star, 1-2 star) with 3 variations each that naturally incorporate service + location keywords. Covers article prompts #3 (competitor review teardown) and #4 (review response strategy) from the local SEO playbook.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in gbp-suite |
|---|---|---|
| **R1** | Source placement | Review response templates → **end-customer-facing** (posted publicly on GBP). No source tags. |
| **R2** | Single-doc-with-toggles | Multi-template pack ships as one doc with toggle per star tier. |
| **R3** | Product-update tone | Responses frame as "we appreciate / we hear / we ship X" — operator-direct, never "we are thrilled." |
| **R6** | CTA hierarchy | Response close → product-action (visit again, contact us) per customer-facing service business. |
| **R7** | FAQ titles + no sources block | Competitor-review teardown article uses FAQ title pattern ("What review patterns work for [vertical]?"). |
| **R8** | Entity-name headings | Section headings repeat business name where applicable. |
| **R9** | Action-oriented section names | Response template names verb-led. |

---

## Process Flowchart

```
┌──────────────────────────────────────────────────────────────┐
│ GBP REVIEW STRATEGY PROCESS │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ INPUT VALIDATION │
│ Required: │
│ □ Client GBP URL │
│ □ 2-3 competitor GBP URLs │
│ □ Target keywords (3+) │
│ □ Service areas (neighborhoods/cities) │
│ Optional: Current review count, response rate baseline │
│ → If missing: Ask for GBP URLs and target keywords │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 1: REVIEW DATA EXTRACTION │
│ □ Scrape last 50 reviews per listing (client + competitors) │
│ □ Extract: total count, avg rating, 30/60/90 day velocity │
│ □ Extract: mentioned services, neighborhoods, complaints │
│ ✓ Checkpoint: Review data captured for all listings │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 2: VELOCITY ANALYSIS │
│ □ Calculate reviews/month for each listing (30/60/90 day) │
│ □ Identify top competitor by velocity │
│ □ Calculate reviews/month needed to catch top competitor │
│ □ Estimate time-to-parity at target velocity │
│ ✓ Checkpoint: Velocity gap quantified with catch-up target │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 3: RESPONSE AUDIT │
│ □ Analyze owner responses: response rate, avg response time │
│ □ Check keyword usage in existing responses │
│ □ Evaluate tone and negative review handling │
│ □ Compare response quality across all listings │
│ ✓ Checkpoint: Response gaps identified vs. competitors │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 4: TEMPLATE GENERATION │
│ □ Create 5-star templates (3 variations) │
│ □ Create 4-star templates (3 variations) │
│ □ Create 3-star templates (3 variations) │
│ □ Create 1-2 star templates (3 variations) │
│ □ Each template includes service keywords + location mention │
│ ✓ Checkpoint: 12 templates ready, keywords naturally placed │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 5: STRATEGY DOCUMENT │
│ □ Set monthly review velocity target │
│ □ Identify where/when to ask for reviews │
│ □ Define what to ask customers to mention (service + area) │
│ □ Create 90-day review growth roadmap │
│ ✓ Checkpoint: Actionable strategy with measurable targets │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────┬─────────────────────────┐
│ REVIEW GATE: Level 1 (Quick) │ CHAIN SUGGESTIONS │
├────────────────────────────────────┼─────────────────────────┤
│ Present: Velocity analysis, │ → gbp-content-engine │
│ response audit, 12 templates, │ → gbp-listing-opt │
│ strategy doc │ → content-strategy │
│ Actions: [Approve] [Adjust] │ → Export to Google Docs │
│ [Add competitors] │ │
└────────────────────────────────────┴─────────────────────────┘
```

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Review strategy for [business]"
- "Review teardown"
- "Competitor review analysis"
- "Review response templates"
- "How do I get more reviews?"
- "Review velocity analysis"
- "Help me respond to reviews"
- "Google review strategy"
- "Review gap analysis"

**Do NOT invoke when:**
- User wants full local SEO audit (use `/local-seo-audit` orchestrator)
- User wants GBP category or attribute analysis (use `/gbp-category-audit`)
- User wants GBP posts or photo strategy (use `/gbp-content-engine`)
- User wants services section or description optimization (use `/gbp-listing-optimization`)

---

## Input Requirements

### Required Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Client GBP URL** | Google Maps/Business link for the client | User provides |
| **Competitor GBP URLs** | 2-3 top competitor listings | User provides or researched |
| **Target keywords** | 3+ service-related keywords to rank for | User provides |
| **Service areas** | Neighborhoods/cities served | User provides |

### Optional Inputs (improve quality)

| Input | How It Helps |
|-------|--------------|
| Current review count | Baseline for velocity calculations without scraping |
| Response rate baseline | Skip response audit if already known |
| Business owner name | Personalize response templates |
| Core services list | Ensure templates cover all service lines |
| Previous review solicitation methods | Build on what's already working |

### Input Validation Checklist

Before proceeding, verify:
- [ ] Client GBP URL is accessible and has reviews
- [ ] At least 2 competitor GBP URLs provided
- [ ] At least 3 target keywords specified
- [ ] Service areas defined (neighborhoods or cities)

**If inputs are missing:** Ask for client GBP URL first. Offer to research competitors via Exa/Firecrawl if user doesn't have competitor URLs.

---

## Process (Step-by-Step)

### Phase 1: Review data extraction

**Purpose:** Scrape and structure review data from client and competitor GBP listings.

**Steps:**

1. **Step 1.1: Scrape client reviews**
   - Pull last 50 reviews from client GBP URL
   - Extract: reviewer name, rating, date, review text, owner response (if any)
   - **Output:** Client review dataset

2. **Step 1.2: Scrape competitor reviews**
   - Pull last 50 reviews per competitor GBP URL (2-3 competitors)
   - Extract same fields as client
   - **Output:** Competitor review datasets

3. **Step 1.3: Parse review content**
   - For each listing, extract:
     - Total review count and average rating
     - Services mentioned (map to target keywords)
     - Neighborhoods/locations mentioned
     - Recurring complaints (grouped by theme)
     - Recurring praise (grouped by theme)
   - **Output:** Parsed review content analysis per listing

**Phase 1 Checkpoint:**
- [ ] Review data captured for client + all competitors
- [ ] Services, neighborhoods, and complaints extracted
- [ ] Data is sourced — no invented review counts or ratings

### Phase 2: Velocity analysis

**Purpose:** Quantify review generation speed and calculate the gap to close.

**Steps:**

1. **Step 2.1: Calculate review velocity per listing**
   - Count reviews in last 30, 60, and 90 days for each listing
   - Calculate reviews/month average for each window
   - **Output:** Velocity table (listing x time window)

2. **Step 2.2: Identify velocity gap**
   - Rank all listings by 90-day velocity
   - Calculate gap between client and top competitor
   - **Output:** Gap measurement (reviews/month behind)

3. **Step 2.3: Calculate catch-up projections**
   - Reviews/month needed to reach parity with top competitor in 6, 9, and 12 months
   - Factor in competitor's ongoing velocity (they don't stop)
   - **Output:** Time-to-parity projections at different velocity targets

**Phase 2 Checkpoint:**
- [ ] Velocity calculated for all listings across 30/60/90 day windows
- [ ] Gap quantified with specific catch-up numbers
- [ ] Projections account for competitor's ongoing velocity

### Phase 3: Response audit

**Purpose:** Evaluate how well each business responds to reviews and identify gaps.

**Steps:**

1. **Step 3.1: Calculate response metrics**
   - Response rate (% of reviews with owner reply)
   - Average response time (if timestamps available, otherwise note as [UNAVAILABLE])
   - **Output:** Response rate comparison table

2. **Step 3.2: Analyze response quality**
   - Check for target keyword usage in responses
   - Check for location/neighborhood mentions in responses
   - Evaluate tone: professional, personal, template-feeling, defensive
   - Assess negative review handling: apologetic, defensive, solution-oriented, ignored
   - **Output:** Response quality assessment per listing

3. **Step 3.3: Identify response patterns**
   - Does competitor use templates? (look for repeated phrases)
   - Do responses mention specific services or staff?
   - Do responses include calls-to-action (come back, try X)?
   - **Output:** Response pattern analysis

**Phase 3 Checkpoint:**
- [ ] Response rate and quality compared across all listings
- [ ] Keyword usage in responses quantified
- [ ] Best practices identified from top-performing competitor

### Phase 4: Template generation

**Purpose:** Create 12 review response templates (4 tiers x 3 variations) with embedded keywords.

**Steps:**

1. **Step 4.1: Define template structure**
   - Each template must naturally include:
     - At least 1 target service keyword
     - At least 1 location/neighborhood mention
     - Personal touch (reference specifics from review)
     - Forward-looking statement (invitation to return, try another service)
   - **Output:** Template structure guidelines

2. **Step 4.2: Create 5-star response templates (3 variations)**
   - Variation A: Service-focused (highlights the specific service praised)
   - Variation B: Team-focused (credits staff, builds personal connection)
   - Variation C: Community-focused (emphasizes neighborhood/local pride)
   - **Output:** 3 x 5-star templates

3. **Step 4.3: Create 4-star response templates (3 variations)**
   - Variation A: Grateful + improvement-curious (asks what would make it 5 stars)
   - Variation B: Service expansion (mentions related services they might enjoy)
   - Variation C: Loyalty-building (offers reason to return)
   - **Output:** 3 x 4-star templates

4. **Step 4.4: Create 3-star response templates (3 variations)**
   - Variation A: Empathetic + action-oriented (acknowledge gap, state fix)
   - Variation B: Dialogue-opening (invite offline conversation)
   - Variation C: Improvement commitment (specific steps being taken)
   - **Output:** 3 x 3-star templates

5. **Step 4.5: Create 1-2 star response templates (3 variations)**
   - Variation A: Empathetic + escalation (apologize, provide direct contact)
   - Variation B: Fact-based + resolution (address specific issue, state resolution)
   - Variation C: Service recovery (offer to make it right, specific next step)
   - Never: defensive, dismissive, or argumentative tone
   - **Output:** 3 x 1-2 star templates

**Phase 4 Checkpoint:**
- [ ] 12 templates total (4 tiers x 3 variations)
- [ ] Every template includes at least 1 service keyword naturally
- [ ] Every template includes at least 1 location mention naturally
- [ ] Negative review templates are empathetic, never defensive
- [ ] Templates have [BRACKET] placeholders for personalization

### Phase 5: Strategy document

**Purpose:** Create an actionable review growth plan with measurable targets.

**Steps:**

1. **Step 5.1: Set monthly velocity target**
   - Based on Phase 2 catch-up projections
   - Recommend realistic velocity (with reasoning)
   - **Output:** Monthly review target with justification

2. **Step 5.2: Map review solicitation touchpoints**
   - In-person: after service completion, at checkout
   - Digital: follow-up email/SMS, thank-you page, QR codes
   - Timing: optimal ask window (24-48 hours post-service)
   - **Output:** Touchpoint map with timing

3. **Step 5.3: Define review content guidance**
   - What to ask customers to mention: specific service, neighborhood, staff name
   - How to frame the ask (natural, not scripted)
   - Example scripts for staff to use when asking
   - **Output:** Content guidance with example ask scripts

4. **Step 5.4: Create 90-day roadmap**
   - Month 1: Set up systems (templates, ask scripts, QR codes)
   - Month 2: Launch review solicitation at all touchpoints
   - Month 3: Measure velocity, adjust approach, respond to all new reviews
   - **Output:** 90-day action plan

**Phase 5 Checkpoint:**
- [ ] Velocity target set with time-to-parity math
- [ ] Touchpoints identified with timing guidance
- [ ] Customer ask scripts provided
- [ ] 90-day roadmap with measurable milestones

---

# GBP Review Strategy: [Business Name]

**GBP URL:** [URL]
**Date assessed:** [Date]
**Competitors analyzed:** [Competitor 1], [Competitor 2], [Competitor 3]
**Assessor:** Genesys Growth

---

## Review Velocity Comparison

| Metric | [Client] | [Competitor 1] | [Competitor 2] | [Competitor 3] |
|--------|----------|-----------------|-----------------|-----------------|
| Total reviews | X | X | X | X |
| Average rating | X.X | X.X | X.X | X.X |
| Reviews (last 30 days) | X | X | X | X |
| Reviews (last 60 days) | X | X | X | X |
| Reviews (last 90 days) | X | X | X | X |
| Velocity (reviews/month) | X | X | X | X |

**Gap to #1:** [X] reviews/month behind [Competitor Name]
**Time to parity:** ~[X] months at [Y] reviews/month target

---

## Review Content Analysis

### Services mentioned in reviews

| Service keyword | [Client] | [Comp 1] | [Comp 2] | [Comp 3] |
|-----------------|----------|----------|----------|----------|
| [Keyword 1] | X mentions | X mentions | X mentions | X mentions |
| [Keyword 2] | X mentions | X mentions | X mentions | X mentions |
| [Keyword 3] | X mentions | X mentions | X mentions | X mentions |

### Neighborhoods mentioned in reviews

| Location | [Client] | [Comp 1] | [Comp 2] | [Comp 3] |
|----------|----------|----------|----------|----------|
| [Area 1] | X mentions | X mentions | X mentions | X mentions |
| [Area 2] | X mentions | X mentions | X mentions | X mentions |

### Recurring complaints (by theme)

| Complaint theme | [Client] | [Comp 1] | [Comp 2] | [Comp 3] |
|-----------------|----------|----------|----------|----------|
| [Theme 1] | X occurrences | X | X | X |
| [Theme 2] | X occurrences | X | X | X |

---

## Response Audit

| Metric | [Client] | [Comp 1] | [Comp 2] | [Comp 3] |
|--------|----------|----------|----------|----------|
| Response rate | X% | X% | X% | X% |
| Avg response time | [X days / UNAVAILABLE] | [X days] | [X days] | [X days] |
| Keyword usage in responses | [Yes/No] | [Yes/No] | [Yes/No] | [Yes/No] |
| Location mentions in responses | [Yes/No] | [Yes/No] | [Yes/No] | [Yes/No] |
| Negative review handling | [Approach] | [Approach] | [Approach] | [Approach] |

**Key gaps:**
- [Gap 1]
- [Gap 2]
- [Gap 3]

---

## Review Response Templates

### 5-star responses

**Variation A — Service-focused:**
> [Template with [SERVICE KEYWORD], [LOCATION], [REVIEWER NAME], [SPECIFIC DETAIL] placeholders]

**Variation B — Team-focused:**
> [Template]

**Variation C — Community-focused:**
> [Template]

---

### 4-star responses

**Variation A — Grateful + improvement-curious:**
> [Template]

**Variation B — Service expansion:**
> [Template]

**Variation C — Loyalty-building:**
> [Template]

---

### 3-star responses

**Variation A — Empathetic + action-oriented:**
> [Template]

**Variation B — Dialogue-opening:**
> [Template]

**Variation C — Improvement commitment:**
> [Template]

---

### 1-2 star responses

**Variation A — Empathetic + escalation:**
> [Template]

**Variation B — Fact-based + resolution:**
> [Template]

**Variation C — Service recovery:**
> [Template]

---

## Review Growth Strategy

### Monthly velocity target

- **Target:** [X] reviews/month
- **Current:** [X] reviews/month
- **Gap:** [X] reviews/month
- **Time to parity with [Competitor]:** ~[X] months

### Where to ask for reviews

| Touchpoint | When | Method | Expected yield |
|------------|------|--------|----------------|
| [Touchpoint 1] | [Timing] | [Method] | [Est. reviews/month] |
| [Touchpoint 2] | [Timing] | [Method] | [Est. reviews/month] |
| [Touchpoint 3] | [Timing] | [Method] | [Est. reviews/month] |

### What to ask customers to mention

- **Service:** [Specific service they received]
- **Location:** [Neighborhood or area name]
- **Experience:** [Specific aspect of service]

### Staff ask scripts

**Script 1 (in-person, post-service):**
> "[Natural ask script with specific service + location mention guidance]"

**Script 2 (follow-up text/email):**
> "[Natural digital follow-up script]"

### 90-day roadmap

| Month | Focus | Actions | Target |
|-------|-------|---------|--------|
| 1 | Setup | [Actions] | [Target] |
| 2 | Launch | [Actions] | [Target] |
| 3 | Optimize | [Actions] | [Target] |

---

## Iteration Prompts

1. "Want me to add more competitors to the velocity analysis?"
2. "Should I create review solicitation email/SMS sequences?"
3. "Want me to run the GBP content engine to complement this review strategy?"
4. "Should I export this to Google Docs for the client?"
```

---

## Anti-Hallucination Guardrails

1. **Only report what was scraped.** If review data can't be extracted for a listing, mark as "[UNAVAILABLE: could not scrape reviews for [listing]]" — don't estimate.
2. **No invented review counts or ratings.** Every number in velocity tables must come from scraped data or user-provided data.
3. **Velocity math must be shown.** Show the calculation behind reviews/month and time-to-parity projections so user can verify.
4. **Response templates are templates, not real responses.** Clearly mark all placeholders with [BRACKETS] and never include real customer names or review content in templates.
5. **Complaint themes must come from actual reviews.** Don't invent complaint categories — only report themes that appear in scraped review text.
6. **Review data is point-in-time.** Note the scrape date on all data tables — review counts change daily.
7. **Time-to-parity is an estimate.** Tag all projections with [ESTIMATED: based on current velocity trends] — competitors can change their velocity too.

---

## Quality Checklist (Pre-Delivery)

### Data quality
- [ ] Review data scraped for client + all competitors (or marked [UNAVAILABLE])
- [ ] Velocity calculated from actual review dates, not estimated
- [ ] All numbers traceable to scraped data
- [ ] Scrape date noted on all data tables

### Analysis quality
- [ ] Velocity comparison table complete (30/60/90 day)
- [ ] Service keyword mentions extracted and compared
- [ ] Neighborhood mentions extracted and compared
- [ ] Recurring complaints grouped by theme with counts
- [ ] Response audit covers rate, time, keywords, tone

### Template quality
- [ ] 12 templates total (4 tiers x 3 variations)
- [ ] Every template includes at least 1 service keyword naturally
- [ ] Every template includes at least 1 location mention naturally
- [ ] Negative review templates are empathetic, never defensive
- [ ] All placeholders clearly marked with [BRACKETS]
- [ ] Templates sound human, not robotic or over-optimized

### Strategy quality
- [ ] Monthly velocity target set with catch-up math
- [ ] Touchpoints identified with timing and method
- [ ] Customer ask scripts provided (in-person + digital)
- [ ] 90-day roadmap with measurable milestones
- [ ] Strategy is realistic for business size and type

---

## Post-Output: Iteration Prompts

After delivering output, proactively offer these iteration options:

### Refinement prompts
1. "Want me to adjust the velocity target based on your capacity?"
2. "Should I customize the templates for a specific service line?"
3. "Want me to add more competitors to the analysis?"

### Expansion prompts
1. "Want me to create review solicitation email/SMS sequences?"
2. "Should I run /gbp-content-engine to build a posts strategy that reinforces review themes?"
3. "Want me to create a review monitoring dashboard spec?"

### Quality prompts
1. "Want me to test the response templates against your actual recent reviews?"
2. "Should I analyze seasonal patterns in your review velocity?"
3. "Want me to identify which competitor response patterns correlate with higher ratings?"

---

## MCP Data Integration

**Level:** 0 — Context (heavy data gathering, competitive analysis)

### Primary tools

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Apify** | Structured Google Maps review data | `call-actor` (Google Maps Reviews actor) | Primary extraction method |
| **Firecrawl** | GBP listing pages (fallback) | `firecrawl_scrape` | When Apify unavailable or for supplementary data |
| **Exa** | Competitor discovery if URLs not provided | `web_search_exa` | When user doesn't have competitor GBP URLs |

### Apify integration

```javascript
// Google Maps Reviews actor — extract last 50 reviews per listing
call-actor({
  actorId: "compass/google-maps-reviews-scraper",
  input: {
    startUrls: ["[GBP_URL]"],
    maxReviews: 50,
    reviewsSort: "newest"
  }
})
```

**What Apify provides:**
- Review text, rating, date, reviewer name
- Owner response text and timestamp
- Total review count and average rating
- Structured data ready for analysis

### Fallback (no MCP)

- `WebFetch` for manual GBP page fetching (limited review data)
- User provides review data export (Google Takeout or third-party tool)
- Manual review counting from GBP screenshots
- User provides competitor review counts directly

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

