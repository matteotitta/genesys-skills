---
name: linkedin-algo-audit
version: '1.0'
last_updated: 2026-03-17
author: genesys-growth
description: 'Checks LinkedIn posts or profiles against 2026 algorithm data for performance prediction. Produces a scored
  audit with actionable recommendations for reach optimisation. Triggers: "will this post perform?", "check this against the
  algo", "algo audit", "is my profile optimised for search?", "LinkedIn algorithm". Standalone quality gate — does not require
  voice, pillar, or ICP context. Runs after any LinkedIn post skill as optional review step.'
goal: Checks LinkedIn posts or profiles against 2026 algorithm data for performance prediction.
outcome: 'Checks LinkedIn posts or profiles against 2026 algorithm data for performance prediction. Produces a scored audit
  with actionable recommendations for reach optimisation. Triggers: "will this post perform?", "check this against the algo",
  "algo audit", "is my profile optimised for search?",...'
primitive: social
sub_primitive: linkedin
ontology_type: content-audit
review_gate: 0
inputs:
  required: []
  recommended:
  - linkedin-content-guide
  - linkedin-profile-optimization
- type: voice-review-report
  feeds_into:
  - linkedin-content-guide
depends_on: []
- linkedin-content-guide
owned_by_agent: content
mcps_used: []
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

# LinkedIn Algo Audit

Check LinkedIn posts and profile sections against 2026 algorithm data. Standalone quality gate — runs independently of voice, pillar, or client context. Returns a structured audit with pass/warn/fail scores and specific fixes.

**Data sources:** Shield Analytics (50K posts, Dec 2025), AuthoredUp (3M+ posts, Jan 2026), 360brew GPU-RAR framework, Propelgrowth blog, Scripe 2026 updates.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "check this against the algo"
- "will this post perform?"
- "algo audit"
- "is my profile 360brew optimized?"
- "LinkedIn algorithm check"
- "optimize for the algorithm"
- "why is my content not getting reach?"

**Do NOT invoke when:**
- User wants voice review → use `voice-reviewer`
- User wants to write a post → use the appropriate post skill
- User wants overall content strategy → use `linkedin-content-guide`

---

## Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Post text or profile section** | The content to audit | User provides or from last assistant message |
| **Audit type** | Post audit, Profile audit, or Full audit | User specifies or infer from content |

**Validation:**
- [ ] Content is provided (post text or profile section)
- [ ] Audit type is determinable

---

## Algorithm Foundation: GPU-RAR (2026)

Voice-locked framework — this is the spine of the audit logic. Stays in body.

LinkedIn replaced thousands of individual ranking models with a single AI model that reads content semantically — like a language model, not a keyword matcher.

**GPU-RAR Framework (360brew):**
- **G — Generate** embeddings from your profile text and post content
- **P — Profile** match between content topic and your stated expertise
- **U — User** interest matching (member embedding against topic clusters)
- **R — Relevance** scoring against the specific audience segment
- **A — Amplification** based on early engagement signals
- **R — Redistribution** to new segments if content holds up

**Key implications:**
- Your profile is the AI's prompt about you — misaligned profile = suppressed distribution
- Semantic matching, not keyword stuffing — hashtags are now largely irrelevant
- 90-day categorization window — posting consistently on 2-3 topics builds an audience cluster
- Evergreen redistribution — strong content resurfaces weeks later to new matching segments

---

## Algorithm Priority Signals (Ranked)

Voice-locked ranking — this is the load-bearing decision data. Stays in body.

1. **Saves** — highest weight; a post with 200 saves dramatically outperforms 1,000 likes
2. **Comment threads** — multi-party comments get 5.2× amplification
3. **Dwell time** — time spent reading correlates strongly with redistribution
4. **Profile-content alignment** — misalignment suppresses distribution for all posts
5. **Shares/reposts** — weighted 4× in TWE scoring
6. **Likes** — lowest weight of all engagement types

---

## Process

**Post audit (3 phases):** Content-audience fit → Post structure signals (hook dwell, save potential, comment thread, format performance, reach killers) → Scoring summary.

**Profile audit (3 phases):** Keyword-profile alignment → Content history alignment (if known) → Scoring summary.

Full step-by-step + scoring criteria + reach killers list in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Don't invent performance data.** All benchmarks must trace to Shield Analytics, AuthoredUp, or 360brew — sources cited in the premium reference.
2. **Don't predict exact impression counts.** Use the benchmark ranges as context, not guarantees.
3. **Don't flag content as "will fail".** Score as WARN/FAIL/PASS with specific fixes — never predict zero performance.

---

## Quality

Pre-delivery checks cover audit completeness (all sub-checks ran, fixes specific not generic), audit fairness (PASS = no blockers, not "great"), and benchmark currency. Algorithm benchmark tables (Shield, AuthoredUp, format performance, posting optimization) + anti-examples in the premium reference.

---

