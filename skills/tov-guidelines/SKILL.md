---
name: tov-guidelines
version: "2.1"
author: genesys-growth
last_updated: 2026-01-21
description: >
  Analyzes existing client content (website, blog, social, docs) to extract
  voice patterns, vocabulary preferences, frequency scores, and do/don't
  usage rules. Produces a two-phase output: Phase 1 TOV analysis (patterns
  extracted from source material) and Phase 2 TOV guidelines (codified voice
  rules for content production). Upstream: recommended company-context.
  Downstream: feeds linkedin-content, landing-page-copy, product-messaging,
  outreach-emails, and all content skills. NOT for visual brand tokens
  (use /brand-kit).
---

# TOV guidelines

Extract actionable editorial tone of voice guidelines from a company's existing content. Two-phase workflow ensures guidelines are grounded in evidence, not assumptions.

---

## Process Flowchart

```text
┌──────────────────────────────────────────────────────────────┐
│                  TOV GUIDELINES PROCESS                       │
│              (Two-Phase Workflow with User Gate)              │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 1: ANALYSIS                                             │
│ Step 1.1: Discover site structure → page list                 │
│ Step 1.2: Scrape 15-20 pages by priority                      │
│ Step 1.3-1.6: Extract patterns (sentence, paragraph, word,    │
│               structural)                                     │
│ Step 1.7: Score frequency (High 80%+ / Med 40-79% / Low <40%)│
│ Step 1.8: Build content-type voice mapping                    │
│ Step 1.9: Generate voice-in-action examples                   │
│ Step 1.10: Identify inconsistencies                           │
│ Step 1.11: Document gaps                                      │
│ ✓ Output: tov-analysis.md                                     │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ REVIEW GATE: Level 2 (User Review Required)                   │
│ Present: Pattern findings, inconsistencies, gaps              │
│ User Actions: [Confirm] [Correct patterns] [Answer gap Qs]    │
│ → MUST have user review before proceeding to Phase 2          │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 2: GENERATION                                           │
│ Step 2.1: Incorporate user feedback                           │
│ Step 2.2: Generate guidelines (reader, tone, patterns,        │
│           vocabulary, structure, anti-patterns)               │
│ Step 2.3: Add source attribution to every guideline           │
│ ✓ Output: tov-guidelines.md                                   │
└──────────────────────────────────────────────────────────────┘
```

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Create TOV guidelines for [URL/company]"
- "Extract voice from website"
- "Build editorial guidelines"
- "Tone of voice document"
- "Brand voice guidelines"
- "Writing style guide for [company]"
- "What's [company]'s voice?"
- "Analyze voice from [URL]"

**Do NOT invoke when:**
- User wants brand identity guidelines (visual) → Use `brand-kit` skill
- User wants product messaging → Use `product-messaging` skill
- User wants to write content → Use appropriate content skill with TOV as input
- User just wants quick voice description → Answer directly

---

## Input Requirements

### Required Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Company URL** | Primary website URL | User provides |

### Optional Inputs (improve quality)

| Input | How It Helps |
|-------|--------------|
| Founder context | Interview transcript, founder notes, voice preferences |
| Existing guidelines | Current brand guidelines to incorporate or update |
| Target audience | Known audience details to validate against content |

---

## Process (Step-by-Step)

### Phase 1: Analysis

**Purpose:** Extract evidence-based voice findings from website content.

**Output:** `tov-analysis.md`

**Steps:**

1. **Step 1.1: Discover site structure**
   - Fetch homepage and extract all internal links
   - Filter: same domain only (no third-party links)
   - Prioritize: /about, /manifesto, /values, /blog/*, /case-studies/*, /pricing, /faq
   - **Output:** Page list for analysis

2. **Step 1.2: Scrape comprehensively**
   - Fetch pages in priority order (stop at ~15-20 pages)
   - Priority 1: Homepage (core positioning, primary CTA style)
   - Priority 2: About/Manifesto/Values (origin story, beliefs, personality)
   - Priority 3: Blog posts (3-5) (long-form voice, educational tone)
   - Priority 4: Case studies (2-3) (proof presentation, client voice)
   - Priority 5: Pricing/Services (commercial tone, specificity)
   - Priority 6: FAQ (objection handling, conversational tone)
   - Priority 7: Landing pages (persuasion patterns)
   - **Output:** Page content collected

3. **Step 1.3: Extract sentence-level patterns**
   - Average sentence length
   - First-person vs. third-person usage
   - Question frequency
   - Command/imperative usage
   - **Output:** Sentence-level analysis

4. **Step 1.4: Extract paragraph-level patterns**
   - Average paragraph length
   - Opening patterns
   - Transition patterns
   - Evidence placement
   - **Output:** Paragraph-level analysis

5. **Step 1.5: Extract word-level patterns**
   - Recurring terms (company vocabulary)
   - Industry terms (customer vocabulary)
   - Banned/avoided words
   - Modifier frequency (very, really, extremely)
   - **Output:** Word-level analysis

6. **Step 1.6: Extract structural patterns**
   - Header style (sentence case vs. title case)
   - CTA placement and phrasing
   - Proof stacking patterns
   - Section organization
   - **Output:** Structural analysis

7. **Step 1.7: Score frequency**
   - High (80%+): Pattern across most page types
   - Medium (40-79%): Pattern on some pages
   - Low (<40%): Pattern appears rarely
   - Conflict: Contradictory patterns found
   - **Output:** Frequency scores per finding

8. **Step 1.8: Build content-type mapping**
   - Document how voice varies by content type
   - Note person, formality, CTA style per type
   - **Output:** Voice variation table

9. **Step 1.9: Generate voice-in-action examples**
   - Create before/after pairs (generic → on-brand)
   - **Output:** Transformation examples

10. **Step 1.10: Identify inconsistencies**
    - Flag conflicts (e.g., homepage uses "I", pricing uses "we")
    - Note as issues to resolve in Phase 2
    - **Output:** Inconsistency list

11. **Step 1.11: Document gaps**
    - What couldn't be determined from scraping
    - Suggested founder interview questions
    - **Output:** Gap inventory

**Phase 1 Checkpoint:**
- [ ] 15+ pages analyzed
- [ ] All pattern categories extracted
- [ ] Frequency scores assigned
- [ ] Inconsistencies flagged
- [ ] Gaps documented

**User Review Point:** Present Phase 1 analysis to user for review before Phase 2.

### Phase 2: Generation

**Purpose:** Create actionable guidelines from validated findings.

**Output:** `tov-guidelines.md`

**Steps:**

1. **Step 2.1: Incorporate feedback**
   - User reviews Phase 1 analysis
   - Apply corrections to misidentified patterns
   - Resolve inconsistencies
   - Fill gaps with founder answers
   - **Output:** Validated findings

2. **Step 2.2: Generate guidelines document**
   - Primary reader definition
   - Tone attributes with examples
   - Pattern library with LLM guidance
   - Vocabulary lists
   - Structure templates
   - Anti-patterns
   - **Output:** Complete guidelines

3. **Step 2.3: Add source attribution**
   - Every guideline traces to source URL
   - Frequency scores carried forward
   - Unresolved gaps marked "TBD - requires founder input"
   - **Output:** Sourced guidelines

**Phase 2 Checkpoint:**
- [ ] All guidelines have source attribution
- [ ] Inconsistencies resolved
- [ ] Gaps marked or filled
- [ ] Document follows template

---

## Core Frameworks

### Six Critical Questions

Every TOV guidelines document answers:

| # | Question | What It Contains |
|---|----------|------------------|
| 1 | **Who's actually reading?** | Primary reader definition with job title, challenges, goals |
| 2 | **What does tone sound like?** | Demonstrable before/after examples, not adjectives |
| 3 | **What patterns repeat vs. vary?** | Pattern library with LLM-specific guidance |
| 4 | **What words actually used?** | Vocabulary with company terms, customer terms, banned words |
| 5 | **What structure fits?** | Opening patterns, body structure, CTA style |
| 6 | **What to refuse?** | Anti-patterns with specific phrases, claims, tones to avoid |

### Frequency Scoring

| Score | Criteria | Example |
|-------|----------|---------|
| **High (80%+)** | Pattern appears across most page types | "First-person 'I' used on 5 of 6 pages (83%)" |
| **Medium (40-79%)** | Pattern appears on some pages | "'I' used on homepage and about, but not blog posts (40%)" |
| **Low (<40%)** | Pattern appears rarely | "'We' found once on pricing page (17%)" |
| **Conflict** | Contradictory patterns found | "Homepage uses 'I', pricing uses 'we'" |

### Pattern Categories

| Category | What to Extract |
|----------|-----------------|
| **Sentence-level** | Length, person, questions, imperatives |
| **Paragraph-level** | Length, openings, transitions, evidence |
| **Word-level** | Company vocabulary, customer vocabulary, banned words |
| **Structural** | Headers, CTAs, proof stacking, sections |
| **Content-type** | Voice variations by page type |
| **Emotional register** | Tone by content moment |

---

## Output Format

### Phase 1 Output (Analysis)

```markdown
# TOV Analysis: [Company Name]

**Website:** [URL]
**Pages analyzed:** [Count]
**Analysis date:** [Date]

---

## Pages Scraped

| Page | URL | Voice Facets Revealed |
|------|-----|----------------------|
| Homepage | [URL] | Core positioning, primary CTA |
| About | [URL] | Origin story, beliefs |

---

## Pattern Findings

### Sentence-Level Patterns

| Pattern | Finding | Frequency | Source Pages |
|---------|---------|-----------|--------------|
| Average sentence length | [X words] | High/Med/Low | [Pages] |
| Person usage | [First/Third] | High/Med/Low | [Pages] |
| Question frequency | [X per page] | High/Med/Low | [Pages] |

### Word-Level Patterns

**Company vocabulary:**
- [Term 1] — [Frequency] — [Source pages]

**Banned/avoided words:**
- [Word] — [Evidence it's avoided]

---

## Content-Type Voice Mapping

| Content Type | Person | Formality | CTA Style |
|--------------|--------|-----------|-----------|
| Homepage | [I/We/Brand] | [Conversational/Professional] | [Style] |
| Blog posts | [I/We/Brand] | [Conversational/Professional] | [Style] |

---

## Voice-in-Action Examples

| Generic | On-Brand | Principle |
|---------|----------|-----------|
| "[Generic phrasing]" | "[Actual phrasing from site]" | [What makes it distinctive] |

---

## Inconsistencies Found

### [Inconsistency 1]
- **Page A:** "[Finding]" ([URL])
- **Page B:** "[Conflicting finding]" ([URL])
- **Recommendation:** [How to resolve]

---

## Gaps Identified

| Gap | Why It Matters | How to Fill |
|-----|----------------|-------------|
| [Gap] | [Impact] | [Method] |
```

### Phase 2 Output (Guidelines)

```markdown
# TOV Guidelines: [Company Name]

**Based on analysis of:** [URL]
**Pages analyzed:** [Count]
**Generated:** [Date]

---

## 1. Primary Reader

**Job title:** [Title]
**Challenges:** [Key challenges]
**Goals:** [What they want to achieve]
**How they read:** [Skimming? Deep reading? Mobile?]

---

## 2. Tone Attributes

### [Attribute 1]

**What it means:** [Description]

**Before (generic):**
> "[Generic example]"

**After (on-brand):**
> "[On-brand example from site]"

**Source:** [URL where this pattern appears]

---

## 3. Pattern Library

### Sentence Patterns

| Pattern | Guideline | Source |
|---------|-----------|--------|
| Person | Use "[I/We/Brand]" consistently | [Frequency: X%] |
| Length | Target [X] words average | [Analysis finding] |

### LLM-Specific Guidance

When using this TOV in AI prompts:
- [Specific instruction 1]
- [Specific instruction 2]

---

## 4. Vocabulary

### Always Use

| Term | Context | Source |
|------|---------|--------|
| [Term] | [When to use] | [URL] |

### Never Use

| Term | Say Instead | Source |
|------|-------------|--------|
| [Term] | [Alternative] | [Evidence] |

---

## 5. Structure Templates

### Opening Patterns

**For [content type]:**
[Template structure]
**Source:** [URL]

---

## 6. Anti-Patterns

### Phrases to Avoid

| Don't Say | Why | Say Instead |
|-----------|-----|-------------|
| "[Phrase]" | [Reason] | "[Alternative]" |

### AI-Speak Structural Patterns to Flag

| Pattern | Example | Guideline |
|---------|---------|-----------|
| **False contrast reframe ("X isn't Y. It's Z.")** | "The problem isn't effort. It's coverage." | THE number one AI-speak tell. Rewrite to just state the point directly. |
| **Wrapped bow ending** | "That's the real competitive advantage." | End on questions, open thoughts, or mid-thought instead. |
| **AI transition phrases** | "Here's the thing:" / "Here's why:" | Verbal tics of LLMs. Cut entirely. |
| **Uniform paragraph rhythm** | Every paragraph is 2-3 sentences | Mix lengths wildly. One-word paragraphs. Long ones. |
```

---

## What Good Looks Like

### Example: Genesys Growth TOV Analysis

**Input context:**
```
URL: https://genesysgrowth.com
Type: B2B SaaS GTM consulting
```

**Expected output excerpt:**
```markdown
### Sentence-Level Patterns

| Pattern | Finding | Frequency | Source Pages |
|---------|---------|-----------|--------------|
| Average sentence length | 12 words | High (87%) | All pages |
| Person usage | First-person "I" | High (83%) | Homepage, About, Services |
| Question frequency | 2-3 per page | Medium (60%) | Homepage, Services |
| Imperative usage | Moderate (CTAs only) | High (90%) | All pages |

### Voice-in-Action Examples

| Generic | On-Brand | Principle |
|---------|----------|-----------|
| "We help companies improve their GTM" | "I help B2B SaaS teams accelerate their GTM without the bloat" | Operator authority + specificity |
| "Contact us to learn more" | "Book a call with Matteo" | Personal name > generic CTA |
| "Our solutions leverage AI" | "I use Clay, Claude, and n8n to build systems" | Name specific tools > buzzwords |
```

**Why this is good:**
- Every finding has frequency score
- Source pages cited
- Before/after examples are real, not invented
- Principles extracted from evidence

---

## Anti-Hallucination Guardrails

1. **Every finding needs source.** Include page URL where pattern was found.
2. **Frequency scores based on counts.** "5 of 6 pages (83%)" not "usually"
3. **Examples from actual content.** Never invent illustrative examples.
4. **Flag inconsistencies.** Don't paper over contradictory patterns.
5. **Document gaps explicitly.** Don't fill gaps with assumptions.

---

## Quality Checklist (Pre-Delivery)

### Phase 1 Quality
- [ ] 15+ pages scraped and analyzed
- [ ] All pattern categories have findings
- [ ] Frequency scores calculated (not estimated)
- [ ] Inconsistencies explicitly flagged
- [ ] Gaps documented with founder questions

### Phase 2 Quality
- [ ] All guidelines trace to Phase 1 findings
- [ ] Inconsistencies resolved (or marked pending)
- [ ] Examples are from actual scraped content
- [ ] Source URLs included for verification

---

## MCP Data Integration

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Firecrawl** | Content pages (blog, about, docs) for voice analysis | `firecrawl_scrape` | Always |
| **YouTube** | Founder video transcripts for spoken voice | `get_transcript` | If founder videos exist |
| **Exa** | Brand content across external channels | `web_search_exa` | Always |

### Fallback (no MCP)

- WebFetch for content page samples
- Manual transcript analysis
- WebSearch for external brand content

---

## Reference Files

| File | Purpose | Status |
|------|---------|--------|
| `references/content-analysis-guide.md` | Pattern extraction framework | Core |
| `references/analysis-template.md` | Phase 1 output structure | Core |
| `references/tov-template.md` | Phase 2 output structure | Core |
| `references/founder-interview-questions.md` | Questions to fill gaps | Core |
| `references/quality-checklist.md` | Pre-delivery quality checks | Core |
| `examples/genesys-growth-analysis-example.md` | Complete Phase 1 example | Example |
| `examples/genesys-growth-guidelines-example.md` | Complete Phase 2 example | Example |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.1 | 2026-01-21 | Agentic enhancements: visual flowchart, self-evaluation protocol, upstream/downstream integration map |
| 2.0 | 2026-01-16 | Refactored to v2.0 template: Claude Code triggers, iteration prompts, auto-update rules. Two-phase workflow preserved. |
| 1.0 | Previous | Initial skill creation with two-phase workflow |
