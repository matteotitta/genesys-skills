---
name: linkedin-profile-optimization
version: '1.0'
last_updated: 2026-03-16
author: genesys-growth
description: 'Audits and optimises LinkedIn profiles — headline, about section, banner copy, and experience entries. Produces
  a full profile rewrite aligned with founder-led content program positioning. Triggers: "LinkedIn profile", "profile audit",
  "optimise profile", "headline rewrite", "about section". Optionally consumes tov-guidelines, icp-behavioural, and company-context
  for alignment. Feeds into linkedin-content and linkedin-infographics as profile foundation.'
goal: Audits and optimises LinkedIn profiles — headline, about section, banner copy, and experience entries.
outcome: 'Audits and optimises LinkedIn profiles — headline, about section, banner copy, and experience entries. Produces
  a full profile rewrite aligned with founder-led content program positioning. Triggers: "LinkedIn profile", "profile audit",
  "optimise profile", "headline rewrite", "about section"....'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 3
inputs:
  required: []
  recommended:
  - tov-guidelines
  - icp-behavioural
  - company-context
- type: linkedin-profile-audit
  feeds_into:
  - linkedin-weekly-content
  - linkedin-infographics
depends_on: []
- linkedin-weekly-content
- linkedin-infographics
owned_by_agent: content
mcps_used:
- firecrawl
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# LinkedIn Profile Optimization

Audit a client's LinkedIn profile and generate optimized copy for every section — headline, about, banner, experience, featured, recommendations. Combines Apify scraping for structured profile data with user-provided screenshots for visual assessment, then applies proven profile optimization frameworks.

**Why this matters:** LinkedIn's algorithm reads your entire profile as text context to decide content distribution. A misaligned profile suppresses reach regardless of content quality. This skill ensures profile-content alignment before any content program begins.

**Source:** Nick Broekema (Content Design) — profile optimization methodology.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (profile copy is end-customer-facing — no source tags), R3 (headline + about capability-led, never "thrilled to be"), R6 (featured / CTAs → DM or sign-up primary), R9 (verb-led section headings — "What I do / How I help / Who I work with").

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Optimize [client name]'s LinkedIn profile"
- "LinkedIn profile audit for [person]"
- "Rewrite [person]'s LinkedIn headline/about/bio"
- "Profile optimization for [client]"
- "Help [name] improve their LinkedIn profile"
- "[Client] needs a better LinkedIn presence"

**Do NOT invoke when:**
- User wants to write a LinkedIn post → Use `linkedin-expert-posts` / `linkedin-personal-posts` / `linkedin-sales-posts`
- User wants LinkedIn comments → Use `linkedin-comment`
- User wants a LinkedIn infographic/carousel → Use `linkedin-infographics` / `linkedin-carousels`

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **LinkedIn profile** | URL or full name + company | User provides |
| **ICP description** | Who is this profile trying to attract? | User provides or from icp-behavioural |

### Optional (improve quality)

| Input | How It Helps |
|-------|--------------|
| TOV guidelines | Voice patterns to match in copy generation |
| Company context | Positioning, value props, proof points to reference |
| ICP profile | Detailed pain points and buyer language |
| Screenshots | Visual assessment of banner and profile picture |
| Current positioning | Messaging anchors and differentiators |
| Proof points | Specific metrics, results, client names for banner/about |

**If inputs are missing:** Ask for LinkedIn URL and ICP description at minimum. Request screenshots for banner/profile pic assessment.

---

## Audit scoring table (8 sections)

This table is the load-bearing decision surface for the audit phase. Every audit fills it in.

| Section | Max Score | Key Criteria |
|---------|-----------|-------------|
| **Profile picture** | /10 | Color (not b/w), smile, eye contact, zoom, branded background, contrast |
| **Banner** | /15 | Branded whitespace, clear category, proof points, ICP resonance |
| **Headline** | /15 | Formula fit, ICP clarity, desire/outcome, buyer language |
| **About** | /20 | PAIS structure, hook strength, CTA, specificity, proof |
| **Featured** | /10 | Links (not posts), CTA quality, friction level (3 max) |
| **Experience** | /15 | Current role depth, story, ideal client described, results |
| **Recommendations** | /10 | Problem-solution-outcome structure, relevance, recency |
| **Bio-link** | /5 | Presence, CTA coverage, number of links |
| **TOTAL** | **/100** | |

Status flags: ✓ Good (>70%) | ⚠ Needs work (40-70%) | ✗ Critical (<40%)

---

## Process

3-phase flow: Profile Data Gathering → Profile Audit (using the 8-section scoring table above) → Optimized Copy Generation. Full step-by-step in the premium reference.

---

## Endorsement Strategy

Skill endorsements signal ICP relevance to LinkedIn's search algorithm and 360brew's semantic map. Include this as a quick-win recommendation in all profile audits.

**Approach:**
- Endorse 10–15 relevant contacts proactively. Most reciprocate within 1-2 weeks.
- Focus on contacts who are ICP-adjacent (peers, past colleagues, complementary service providers).
- Prioritise skills that match ICP search terms: GTM, B2B SaaS, positioning, go-to-market, product marketing, content strategy, pipeline generation.
- Remove irrelevant skills (e.g. "Microsoft Excel", "Photoshop") that dilute semantic topic signal.
- Keep the top 3 pinned skills directly aligned to the ONE offer (see `linkedin-content-guide` offer statement).

**Why it matters:** LinkedIn's member embedding system weighs skill endorsements as signals of expertise in specific topic clusters. Endorsements from relevant contacts reinforce your semantic profile faster than self-selected skills alone.

---

## Profile Clarity Tenets (Coach Feedback, March 2026)

Voice-locked rules — these stay in body. Source: Nick Broekema / Content Design, March 2026.

- [ ] **Headline = one sentence** — Who you help + what they get + how fast. Not a laundry list of capabilities.
- [ ] **Banner = single static message** — Not a carousel of rotating promises. One clear line.
- [ ] **About section: mobile readability** — Shorter lines, breathing room, dynamics. No big blocks of text on mobile.
- [ ] **About section: less is more** — Keep ICP language but cut without losing meaning. Wordy = weaker.
- [ ] **Profile-recommendation alignment** — Does the profile reflect what clients consistently say? If all recs say "fast, high quality," the profile should lead with speed + quality.
- [ ] **ICP specificity** — Does the profile name the actual ICP role + company stage? Don't be everything to everyone.

---

## Anti-Hallucination Guardrails

1. **Never invent client metrics, results, or proof points.** Only use data provided or mark as `[PLACEHOLDER: need real metric]`
2. **Don't fabricate recommendations or testimonials.** If none exist, note the gap and provide the request template
3. **No invented company descriptions.** Use scraped data or ask for clarification
4. **Mark assumptions clearly.** Use "Example:" prefix for illustrative scenarios
5. **Verify proof points are real.** Ask user to confirm before including specific numbers in banner/about

---

## MCP Data Integration

**Level:** 0 — Context (heavy data gathering)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Apify** | LinkedIn profile data (headline, about, experience, skills, recommendations) | `search-actors` → `fetch-actor-details` → `call-actor` | Always |
| **Firecrawl** | Company website (for messaging alignment) | `firecrawl_scrape` | If company-context not available |

### Apify workflow

1. Search for LinkedIn profile scraper: `search-actors` with query "LinkedIn profile scraper"
2. Get actor details: `fetch-actor-details` for the selected actor
3. Run actor: `call-actor` with the LinkedIn profile URL as input
4. Get results: `get-actor-output` for structured profile data

### Fallback (no Apify/scraping)

If scraping fails or is unavailable:
- Ask user to copy-paste each profile section manually
- Request screenshots for visual elements
- Proceed with manual data — all frameworks still apply

---

## Quality

Pre-delivery checklist covers audit quality (verbatim evidence, score sums correct), copy quality (formula adherence, PAIS completeness, proof points real), voice quality (matches `tov-guidelines`), and the Profile Clarity Tenets restated for review. Worked example + anti-examples in the premium reference.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

