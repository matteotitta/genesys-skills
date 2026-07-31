---
name: linkedin-sales-posts
version: '1.2'
last_updated: 2026-04-21
author: genesys-growth
description: 'Writes LinkedIn posts that sell through case study storytelling. Produces conversion-focused posts across 5
  archetypes: case study, problem diagnosis, origin story, quote hook, and objection-led. Triggers: "converting post", "sales
  post", "selling post", "offer post", "turn this result into a post". Depends on linkedin-content-guide output (ICP, pains-to-goals,
  ONE offer). NOT for personal stories — use linkedin-personal-posts. NOT for expert frameworks — use linkedin-expert-posts.'
goal: Writes LinkedIn posts that sell through case study storytelling.
outcome: 'Writes LinkedIn posts that sell through case study storytelling. Produces conversion-focused posts across 5 archetypes:
  case study, problem diagnosis, origin story, quote hook, and objection-led. Triggers: "converting post", "sales post", "selling
  post", "offer post", "turn this result into a...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 3
inputs:
  required:
  - linkedin-content-guide
  recommended:
  - tov-guidelines
  - linkedin-hooks
- type: linkedin-post
  feeds_into:
  - linkedin-comment
depends_on:
- linkedin-content-guide
- linkedin-comment
owned_by_agent: content
mcps_used: []
- notion
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# LinkedIn Sales Posts (Converting)

Generate converting LinkedIn posts that sell your offer through case study storytelling — without reading like an ad. Uses Nick Broekema's 12-section converting post template to weave proof, objection handling, qualification, and scarcity into a compelling narrative.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md), [`marketing-psychology.md`](../../../../../rules/marketing-psychology.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (no source tags in post body), R3 (proof framing capability-led, not "thrilled"), R6 (offer woven as soft CTA — DM / sign-up primary, never engagement-farming closer), R9 (12-section template verb-led).

**Produces:**
1. Case study extraction — before/transformation/after elements from a real client result
2. 12-section converting post — ready to copy/paste, offer woven in as "easter egg"
3. Visual element recommendation — what screenshot/image to pair with the post

**Differs from sibling skills:**
- `linkedin-content` — general founder content (educational, thought leadership, personal)
- `linkedin-content-guide` — builds ICP + offer foundation (upstream dependency)
- `linkedin-hooks` — hook formulas library (referenced for section 1)
- **linkedin-sales-posts** — specifically generates CONVERTING posts that sell through case study storytelling

**Source:** Nick Broekema (Content Design) — "Converting Post Breakdown" framework + 6-post pattern analysis.

---

## When to run

Invoke when user says:
- "Write a converting post about [client/result]" → Archetype 1 (case study)
- "Sales post for my offer" → Ask which archetype
- "Turn this case study into a LinkedIn post" → Archetype 1
- "Sell my [offer] on LinkedIn" → Ask which archetype
- "Write an offer post for [case study]" → Archetype 1
- "LinkedIn post to drive DMs" → Ask which archetype
- "Problem callout post" or "diagnose my ICP's problem" → Archetype 2 (problem diagnosis)
- "Origin story for my offer" or "how I created my offer" → Archetype 3 (origin story)
- "Post from a DM I received" or "quote hook post" → Archetype 4 (quote hook)
- "Handle objections in a post" or "niche proof post" → Archetype 5 (objection-led)

Do NOT invoke when:
- General LinkedIn content (educational, thought leadership) → `linkedin-content`
- Short offer post from SCART brief → `linkedin-content` with SCART offer type
- LinkedIn comments → `linkedin-comment`
- Build ICP/offer first → `linkedin-content-guide`
- Hook formulas → `linkedin-hooks`
- LinkedIn infographics → `linkedin-infographics`

## Five archetypes

Five distinct converting-post types. Each sells the same offer from a different angle — rotating prevents sales fatigue.

| # | Archetype | Hook style | Offer integration | Best for |
|---|-----------|------------|-------------------|----------|
| 1 | Case study | "How I helped [client] [result]" | Easter egg woven into story | Strong before/after metrics |
| 2 | Problem diagnosis | "[X]% of [ICP] [do this wrong]" | Solution to diagnosed problem | Awareness-stage buyers |
| 3 | Origin story | "I [did X] for [years] and [consequence]" | Conclusion of personal journey | New offer launches |
| 4 | Quote hook | "[Exact DM/quote from prospect]" | Answer to stated need | Mature audiences |
| 5 | Objection-led | "[Metric]" → "[skeptic quote]" | Proof against skepticism | Skeptical audiences |

**Selection guide, archetype-specific section modifications, full reference posts** → the premium reference and the premium reference.

## Inputs

**Required:**
- LinkedIn content guide output (ICP, pains→goals table, ONE offer, SCART brief)
- Case study / proof points — real client transformation with before/after metrics

**Optional (improve quality significantly):**
- Tone-of-voice guidelines (calibrates voice to author)
- Hook preference (specific formula or style)
- Offer details (bonuses, deliverables, pricing tier)
- Scarcity details (real spot limits, waitlist numbers, deadlines)
- Visual / screenshot (results image to pair with the post)
- Client permission (use real name or anonymize)

**Validation checklist before proceeding:**
- [ ] Content guide output available (ICP, pains→goals, offer)
- [ ] Case study has SPECIFIC before-state metrics (not vague)
- [ ] Case study has SPECIFIC after-state metrics
- [ ] Transformation details are clear (what was done)
- [ ] Client permission obtained (or will anonymize)

If inputs missing:
- No content guide → Ask user to run `linkedin-content-guide` first, or provide ICP + offer manually
- Vague case study → **STOP.** Ask: "I need specific numbers for the before and after state. What were the exact metrics?"
- No scarcity data → Proceed without section 12 (omit)

**Critical:** Never proceed with vague metrics. "They got more followers" is not enough — "grew from 2k to 14,381 followers" is.

## Steps

### Phase 1: Case study extraction
1.1 Load content guide context (ICP, pains→goals, offer deliverables)
1.2 Extract "before" state with specific numbers + map to ICP pains
1.3 Extract transformation (deliverables + trigger event) → maps to section 4 arrow bullets
1.4 Extract "after" state with specific numbers + map to ICP goals
1.5 Extract objection handles (1-2 "yeah buts" + reframes)
1.6 Extract scarcity elements — real ONLY, or mark "OMIT SECTION 12"

### Phase 2: Post construction (12-section template)
2.1 Generate 2-3 hook options for section 1 (formulas in the premium reference)
2.2 Present hooks for user selection
2.3 Write all 12 sections following the premium reference
   - Sections 1-3: Hook → extension → ICP pain
   - Section 4: "Easter egg" — full offer in case study story (→ bullets for deliverables)
   - Sections 5-6: Stack value + show results
   - Sections 7-9: Qualify + handle objections + premium positioning
   - Sections 10-12: CTA + pricing signal + REAL scarcity
   - Format as clean code block, no framework labels in output
2.4 Map each section to content guide elements (mapping table)

### Phase 3: Quality & voice check
3.1 100 Posts Test — would this be specific to your ICP across 100 posts?
3.2 Anti-AI detection — no corporate language, no AI-obvious phrasing
3.2b Nick's X-not-Y sweep (April 2026) — scan for `"X isn't Y — it's Z"`, `"Stop X. Start Y."`, two-sentence parallel-inverse structures. Build sweep table with verdicts. Sales posts particularly prone in Section 3 reframes and case study results
3.3 Easter egg check — section 4 reads as story, not pitch
3.4 Scarcity integrity — all real, or section 12 omitted
3.5 Character count target 1,200-1,500 (acceptable 1,000-2,000)

**Full step-by-step walkthrough, flowchart, checkpoints, anti-hallucination guardrails** → the premium reference.

## What good looks like

- Reads as a story, not an advertisement — the offer is discovered through narrative
- Hook pulled from strongest line in the body (not predictable case-study opener)
- One transformation arc, cleanly told (one case study per post)
- Specific-enough that target buyers see themselves in section 3
- All metrics verbatim from user input — none invented
- All scarcity 100% real or section 12 omitted entirely
- CTA drives DMs (trigger word) — not website visits or call bookings
- Premium positioning present without arrogance
- 1,000-2,000 chars; first 3 lines hook before the LinkedIn cut
- Voice: operator-first, first-person, founder's actual voice (not template language)

**Pre-output 5-dim refine rubric** (score 1-10 each before delivery; iterate any ≤6): hook strength, clarity, engagement potential, platform fit, authenticity. **Coach's quality gates, full self-evaluation protocol, output format spec, iteration prompts, downstream chain integration** → the premium reference.

**Anti-hallucination guardrails** (full list in the premium reference): never invent metrics, never fabricate scarcity, never invent client names or stories, never generate testimonial quotes, never inflate results.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
