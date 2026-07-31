---
name: linkedin-hooks
version: '1.2'
last_updated: 2026-05-17
author: genesys-growth
description: 'Generates a batch of LinkedIn post hooks personalised to a specific ICP and offer. Produces a categorised hook
  library with optional enrichment from real buyer language in sales call transcripts. Triggers: "LinkedIn hooks", "hook library",
  "generate hooks", "hook ideas", "batch content ideation". Depends on linkedin-content-guide output (ICP + offer). Feeds
  into linkedin-expert-posts, linkedin-personal-posts, and linkedin-sales-posts as opening line inventory.'
goal: Generates a batch of LinkedIn post hooks personalised to a specific ICP and offer.
outcome: 'Generates a batch of LinkedIn post hooks personalised to a specific ICP and offer. Produces a categorised hook library
  with optional enrichment from real buyer language in sales call transcripts. Triggers: "LinkedIn hooks", "hook library",
  "generate hooks", "hook ideas", "batch content...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 2
inputs:
  required: []
  recommended:
  - linkedin-content-guide
  - transcript-analysis
  - icp-behavioural
  - tov-guidelines
- type: linkedin-hook-library
  feeds_into:
  - linkedin-weekly-content
depends_on: []
- linkedin-weekly-content
owned_by_agent: content
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /linkedin-hooks
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# LinkedIn Hooks

Generate a personalised library of LinkedIn post hooks using Nick Broekema's 42 hook templates (14 categories), enriched with ICP data, offer context, and real buyer language from sales calls.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md) (no X-not-Y hooks, no false-contrast structures per [[feedback_no_x_not_y_hooks]]). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (hook library is internal-reference), R3 (operator-direct framing in hooks), R9 (verb-led category names). Hook generation explicitly bans X-not-Y false-contrast structures.

**What this produces:**
1. **Category relevance scoring** — which of the 14 hook categories fit this ICP + offer
2. **20-36 personalised hooks** — across 8-12 relevant categories
3. **Top 5 strongest hooks** — ranked by specificity and curiosity gap
4. **Usage guide** — how to feed hooks into post-writing skills

**How it differs from the post-writing skills:** `linkedin-expert-posts` / `linkedin-personal-posts` / `linkedin-sales-posts` write full posts and generate 2-3 hooks as part of the process. This skill is a dedicated hook factory — it produces a reusable library of hooks in bulk, designed to be picked from over weeks of content creation.

**Source:** Nick Broekema (Content Design) — "42 Post Hook Templates" framework.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Generate LinkedIn hooks for [client/person]"
- "Create a hook library for [client]"
- "LinkedIn hook ideas for [topic/ICP]"
- "Batch hooks from my content guide"
- "Hook factory for [client]"
- "Generate hooks from sales calls"

**Do NOT invoke when:**
- User wants to write a full LinkedIn post → Use `linkedin-expert-posts` / `linkedin-personal-posts` / `linkedin-sales-posts`
- User wants to build an ICP + offer → Use `linkedin-content-guide`
- User wants to optimize their LinkedIn profile → Use `linkedin-profile`
- User wants a single hook for a specific post → Pick one from existing library

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **ICP context** | Who the content is targeting (pains, goals, language) | linkedin-content-guide output, user provides, or client CLAUDE.md |
| **Offer** | What the author does for their ICP | linkedin-content-guide output or user provides |
| **Author profile** | Who is posting (name, role, company) | User provides or from client context |

### Optional (significantly improve quality)

| Input | How It Helps |
|-------|--------------|
| **LinkedIn content guide output** | Full 14-question ICP + pains→goals table + SCART elements — richest possible input |
| **Granola sales call transcripts** | Real buyer language, objections, questions, vocabulary |
| **Transcript-analysis output** | Pre-extracted insights, verbatim quotes, pain themes |
| **Competitor names** | Enables "debunking" and "misconception" hooks that reference alternatives |
| **Voice profile / TOV guidelines** | Ensures hooks match the author's voice |
| **Content pillars** | Focus hook generation on specific pillar priorities |

**If inputs are missing:** Ask for minimum context — ICP description, core offer, and top 3-5 pains. Strongly recommend running `/linkedin-content-guide` first for best results.

---

## Process

4-phase flow: Context Gathering → Template Matching (14 categories scored HIGH/MEDIUM/LOW) → Hook Generation (2-3 per selected category) → Quality + Organisation (top 5 ranked). Full step-by-step in the premium reference.

---

## Hook Writing Principles

Five fundamentals to apply on every hook — regardless of template. These are voice-locked rules; they stay in body.

1. **Use specific numbers.** "Many people" → "7 out of 10 B2B SaaS VPs". Numbers create credibility and stop the scroll.
2. **Keep the hook line short.** 5–10 words max for the opening sentence. Long first lines lose people before the curiosity gap lands.
3. **Trigger one emotion.** Pick: curiosity, fear, desire, or surprise. Don't try to do all four — pick the sharpest one for this ICP.
4. **Lead with bold or contrarian.** Safe openers get scrolled past. A statement that challenges the status quo creates tension.
5. **Ask the question they're already asking.** Mirror the internal monologue of your ICP. "How do I generate pipeline without a big budget?" lands if they're already thinking it.
6. **Use ≥3 PLACE ingredients per hook.** Person, Location, Action, Cost, Era. Templates control hook shape; PLACE controls specificity. Below 3 ingredients, hooks slide into the generic-trap. See the premium reference.

### Inspiration accounts

Study these profiles for strong hook execution patterns:
- **Nick Broekema** — clarity, curiosity gaps, clean structure
- **Justin Welsh** — personal authority, contrarian takes, simplicity
- **Alex Hormozi** — specificity, numbers, bold claims
- **Lara Acosta** — TOFU growth posts, relatable stories, B2B personal brand

---

## Anti-Hallucination Guardrails

1. **Never invent metrics, quotes, or outcomes.** Only use proof points from the content guide, transcripts, or user-provided data. If none available, write hooks that don't require specific numbers.
2. **Don't fabricate client stories.** If using storytelling hooks, base them on real experiences from transcripts or user input. Mark as `[NEEDS REAL STORY]` if none available.
3. **Mark missing data.** If a hook template needs a specific metric or timeframe and none exists, adapt the template to work without it rather than inventing data.
4. **Use real buyer language.** When transcripts are available, use verbatim vocabulary. When not, use language from the ICP research — never generic industry terms.

---

## MCP Data Integration

**Level:** 2 — Execution (conditional pulls for enrichment)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Granola** | Sales/discovery call transcripts | `query_granola_meetings`, `get_meeting_transcript` | When user wants to enrich hooks with real buyer language |

### Fallback (no MCP)

- LinkedIn content guide output (pains→goals table)
- User-provided ICP description and pain points
- Client CLAUDE.md voice and messaging context

---

## Quality

Pre-delivery checklist covers hook quality (under 25 words, no emojis, curiosity gap), specificity quality (no placeholders, real ICP language), and voice quality (sounds like author, no buzzwords, passes 100 Posts Test). Worked example + anti-examples in the premium reference.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

