---
name: linkedin-content-guide
version: '1.0'
last_updated: 2026-03-16
author: genesys-growth
description: 'Builds a focused LinkedIn ICP and offer proposition using a 14-question experiential framework combined with
  website scraping. Produces an ideal client profile and one distilled LinkedIn offer statement. Triggers: "LinkedIn ICP",
  "LinkedIn offer", "who do I serve on LinkedIn", "optimize my offer", "ICP for LinkedIn", "content guide from ICP". Requires
  website URL as primary input. Feeds into all LinkedIn post skills (expert, personal, sales), linkedin-hooks, linkedin-profile-optimization,
  and outreach-emails. NOT for full founder-led programs for clients — use linkedin-content-guide-founders instead.'
goal: Builds a focused LinkedIn ICP and offer proposition using a 14-question experiential framework combined with website
  scraping.
outcome: 'Builds a focused LinkedIn ICP and offer proposition using a 14-question experiential framework combined with website
  scraping. Produces an ideal client profile and one distilled LinkedIn offer statement. Triggers: "LinkedIn ICP", "LinkedIn
  offer", "who do I serve on LinkedIn", "optimize my...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 2
inputs:
  required: []
  recommended:
  - company-context
outputs:
- type: linkedin-content-guide
  feeds_into:
  - linkedin-weekly-content
  - linkedin-profile-optimization
  - outreach-emails
  - positioning
depends_on: []
feeds_into:
- linkedin-weekly-content
- linkedin-profile-optimization
- outreach-emails
- positioning
owned_by_agent: content
mcps_used: []
push_targets:
- gdrive
- notion
triggers:
  slash_commands:
  - /linkedin-content-guide
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# LinkedIn Content Guide

Builds a practitioner-first LinkedIn ICP and distills it to ONE focused offer — using Nick Broekema's framework adapted for AI-assisted research. Produces a 14-question ICP, a Pains→Goals content guide, an offer statement, and a SCART brief with 9 post ideas.

How it differs from `/icp-research`: that skill does market-level ICP analysis for B2B SaaS products. This skill builds a *personal* ICP for LinkedIn positioning — starting from your best collaborations and practitioner experience, supplemented by website research.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (guide doc is internal-reference for other LinkedIn skills — inline cites stay), R3 (offer + post-idea framing operator-direct), R5 (long-form essay anchor becomes voice anchor across the 9 post ideas), R9 (verb-led section headings).

## When to run

- "Build my LinkedIn ICP" or "LinkedIn ICP and offer for [company/person]"
- "Who should I target on LinkedIn?" / "Create my LinkedIn offer proposition"
- "Optimize my offer for LinkedIn" / "Help me define my ideal client for LinkedIn content"
- "ICP + offer for [URL]"

Do NOT run when: user wants market-level ICP (`/icp-research`), behavioural buyer simulation (`/icp-behavioural`), to write a single post (`/linkedin-content`), profile optimization (`/linkedin-profile-optimization`), or competitive research (`/competitor-research`).

See `references/skill-integration.md` for full upstream/downstream wiring.

## Inputs

**Required**

| Input | Description | Source |
|-------|-------------|--------|
| Website URL | Company or personal website to research | User provides |

**Optional (significantly improves quality)**

| Input | How it helps |
|-------|--------------|
| Personal experience notes | Direct answers to experiential questions (Q5, Q6, Q10, Q13, Q14) |
| Sales call notes / transcripts | Real language, objections, questions from buyers |
| Existing ICP docs | Validate or expand current understanding |
| Target LinkedIn audience | Who specifically they want to attract |
| Best client example | Description of their ideal collaboration |
| company-context output | Pre-existing company research from upstream skill |

If inputs are missing: ask for website URL at minimum. Strongly encourage personal experience notes — the more experiential input, the better the ICP quality.

## Steps

1. **Phase 1 — Research & data gathering.** Scrape website (Firecrawl), search external signals (Exa), load upstream context. → `references/steps/phase-1-research.md`
2. **Phase 2 — 14-question ICP.** Answer all 14 questions to the quality standard, apply confidence markers, flag experiential questions for user validation. → `references/steps/phase-2-icp-questions.md` and `references/14-question-framework.md`
3. **Phase 3 — Pains → Goals content guide.** Extract 10-20 pain points from the 14 answers, mirror to goals, format as the canonical Guide table. → `references/steps/phase-3-pains-goals.md`
4. **Phase 4 — Offer distillation.** List all services, identify the ONE offer (ROI × impact × fulfilment), produce two-part "What I do / What I market" statement. → `references/steps/phase-4-offer-distillation.md`
5. **Phase 5 — SCART content brief.** Populate the 5 SCART elements, generate 9 post ideas (3 story + 3 expertise + 3 offer), recommend posting frequency and format mix. → `references/steps/phase-5-scart-brief.md` and `references/scart-framework.md`
6. **Phase 6 — Ongoing ideation engine (optional).** Layer Growth/Authority/Sales pillar split, 22-question ideation bank, posting schedule, repurposing cycle. → `references/steps/phase-6-ongoing-ideation.md`
7. **Self-evaluation + review gate (Level 2).** Run completeness, depth, honesty checks. → `references/quality-guardrails.md`
8. **Assemble final output** in canonical format. → `references/output-format.md`
9. **Suggest chains:** `linkedin-profile-optimization` → `linkedin-content` → `outreach-emails` → `positioning`. → `references/skill-integration.md`

Visual flowchart of the full process: `references/process-flowchart.md`. MCP tools and Exa research substrate: `references/mcp-integration.md`.

## What good looks like

### References

- `references/14-question-framework.md` — the 14 questions classified (research-answerable vs. experiential), quality standard per answer
- `references/scart-framework.md` — Statement / Context / Action / Results / Trigger, mapped per post type
- `references/writing-tenets.md` — Nick Broekema coach feedback (brevity, hooks, CTAs, formatting, profile)
- `references/output-format.md` — canonical output template
- `references/quality-guardrails.md` — anti-hallucination rules, pre-delivery checklist, self-evaluation, gotchas, iteration prompts
- `references/mcp-integration.md` — Exa protocol, Firecrawl, Apify, fallback path
- `references/skill-integration.md` — upstream/downstream skill wiring, triggers, workflow sequences
- `references/process-flowchart.md` — visual flow of the full skill
- `references/steps/phase-1-research.md` through `phase-6-ongoing-ideation.md` — per-phase walkthroughs

### Examples

- `references/examples/gold-standard-genesys-growth.md` — Matteo Tittarelli's full output as the quality benchmark
- `references/examples/icp-answer-q1-role.md` — depth bar for a research-answerable question
- `references/examples/icp-answer-q2-pain.md` — depth bar for a pain question (must be quotable)
- `references/examples/pain-goal-pairs.md` — the Pains → Goals table at the right specificity
- `references/examples/offer-statement.md` — two-part "What I do / What I market" with the Louis Vuitton principle
- `references/examples/archetype-story-post.md` — Story post archetype (makes you human)
- `references/examples/archetype-expertise-post.md` — Expertise post archetype (makes you credible)
- `references/examples/archetype-offer-post.md` — Offer post archetype (makes you a business)

### Evaluations

The output passes when: all 14 ICP questions have 4-8 bullets or a rich paragraph; experiential questions Q5/Q6/Q10/Q13/Q14 carry `[REQUIRES USER VALIDATION]`; the Pains→Goals table has 10-20 specific pairs (not generic); ONE offer is identified with explicit ROI×impact×fulfilment rationale; all 5 SCART elements are populated; 9 post ideas exist (3 each for story/expertise/offer) tied to specific pain→goal pairs; no invented metrics, quotes, or testimonials; confidence markers applied consistently. Full checklist: `references/quality-guardrails.md`.

## Push

Push to client engagement folder under `linkedin/` and to Notion client database. Filename: `MMYY-linkedin-content-guide.md` per CLAUDE.md naming convention. Review gate Level 2 (Standard) — user reviews ICP depth, validates experiential answers, confirms ONE offer choice, and signs off on the SCART brief before downstream skills run. After approval, run `/brand-context-sync` if voice patterns surfaced.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/voice-reviewer` — the content ship gate: voice + brand quality (pm-loop.md § lens-reviewer).

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
