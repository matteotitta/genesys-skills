---
name: expert-pov
version: '1.0'
last_updated: 2026-01-25
author: genesys-growth
description: 'Extracts contrarian beliefs, market perspectives, and philosophical stances from founder interviews or questionnaire
  responses. Produces structured POV themes, founder interview question sets, and One Big Idea (OBI) candidates for authority
  positioning. Triggers: "expert POV", "founder POV", "one big idea", "OBI", "authority positioning", "contrarian beliefs",
  or "thought leadership foundation". Upstream: recommended company-context, icp-behavioural, competitor-research. Downstream:
  feeds thought-leadership, linkedin-content, content-strategy, positioning, and storytelling. NOT for content production
  (use /linkedin-content or /thought-leadership) or general brand voice (use /tov-guidelines).'
goal: Extracts contrarian beliefs, market perspectives, and philosophical stances from founder interviews or questionnaire
  responses.
outcome: 'Extracts contrarian beliefs, market perspectives, and philosophical stances from founder interviews or questionnaire
  responses. Produces structured POV themes, founder interview question sets, and One Big Idea (OBI) candidates for authority
  positioning. Triggers: "expert POV", "founder POV",...'
primitive: research
ontology_type: expert-pov
review_gate: 2
inputs:
  required: []
  recommended:
  - company-context
  - icp-behavioural
  - competitor-research
outputs:
- type: expert-pov
  feeds_into:
  - positioning
  - product-messaging
  - linkedin-weekly-content
  - storytelling
  - website-copy
depends_on: []
feeds_into:
- website-copy
- linkedin-weekly-content
- positioning
- product-messaging
- storytelling
owned_by_agent: researcher
mcps_used:
- exa
push_targets:
- gdrive
- notion
triggers:
  slash_commands:
  - /expert-pov
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# Expert POV

Extract and synthesize a founder's unique point of view on their market, craft, and philosophy. Produces the raw material for authority-led positioning — beliefs, stances, and perspectives that differentiate the founder.

**Core philosophy:** Authority comes from having a distinct perspective, not just expertise. Surface what the founder *actually believes* (including contrarian views) and synthesize into OBI candidates.

## When to use

**Invoke when user says:**
- "expert POV / founder POV for [founder/company]"
- "one big idea / OBI for [founder]"
- "authority positioning / thought leadership foundation"
- "contrarian beliefs / what makes [founder] different"
- "founder interview questions"

**Do NOT invoke when:**
- User wants product messaging without founder POV → `product-messaging`
- User wants competitor analysis → `competitor-research`
- User wants ICP research → `icp-behavioural`
- User wants content strategy without POV foundation → run this first

## Inputs

**Required:** Company/founder name; industry/category (for question customization).

**Optional (improves quality):** company context, existing content (LinkedIn posts, podcasts, interviews), competitor positioning, founder background.

**Validation before proceeding:** founder name provided; industry known or discoverable; collection method agreed (async vs live vs content mining). If missing, ask the user; offer to run `company-context` first if needed.

## Process

```
Phase 1 — Question generation     (25-30 questions across 6 POV dimensions)
       ↓
Phase 2 — Founder input           (async / live / content mining)
       ↓
Phase 3 — POV extraction          (beliefs, hot takes, origin stories, taste)
       ↓
Phase 4 — OBI synthesis           (cluster → candidates → score → develop top OBI)
       ↓
Review Gate 2 (Deeper Review)     [Approve] [Iterate OBI] [Expand themes]
```

**Phase walkthroughs (with checkpoints + outputs):**
- Phase 1 → `references/steps/phase-1-question-generation.md`
- Phase 2 → `references/steps/phase-2-founder-input.md`
- Phase 3 → `references/steps/phase-3-pov-extraction.md`
- Phase 4 → `references/steps/phase-4-obi-synthesis.md`

**Phase 4 explicitly checks the 100 Posts Test — could the founder genuinely write 100 authentic posts about this OBI?**

## Frameworks and references

| Topic | File | Contents |
|-------|------|----------|
| 6 POV dimensions | `references/pov-dimensions.md` | Belief, Craft, Market, Story, Taste, Vision — with 5 core questions per dimension |
| Full question bank | `references/question-bank-full.md` | Prioritized questions by dimension with follow-ups |
| OBI frameworks | `references/obi-frameworks.md` | What makes a good OBI, formula patterns, 100 Posts Test, Andy Raskin Strategic Narrative |
| Output template | `references/output-template.md` | Canonical 10-section deliverable structure (Exec summary → Belief map → Hot takes → Stories → Taste → Theme clusters → OBI candidates → Recommended OBI → Raw material → Gaps) |
| Worked walkthroughs | `references/examples/belief-and-obi-walkthroughs.md` | Belief extraction + OBI candidate examples + anti-examples |
| Full worked example | `examples/example-matteo-titta.md` | End-to-end "Taste + Systems" run for Matteo Tittarelli / Genesys Growth |
| Quality + guardrails | `references/quality-and-guardrails.md` | Anti-hallucination rules, pre-delivery checklist, iteration prompts, skill integration map, MCP data integration |

**Scoring matrix (Phase 4.3):** Authenticity 30% · Differentiation 25% · Memorability 20% · Scalability 15% · Business fit 10%. Score 1-5; weighted total. Full criterion definitions in `references/steps/phase-4-obi-synthesis.md`.

## Research substrate (Exa)

Default research substrate per `.claude/rules/exa-protocol.md` (auto-loaded for research, audit, competitor, ICP, AEO, content sourcing work).

**Primary tools for this skill:** `web_search_exa` and the plugin `/search` slash command for parallel-subagent dispatch on founder content mining + POV expansion.

**Tool surface during migration:** prefer plugin namespace `mcp__plugin_exa_exa__web_search_exa` (after `claude plugin i exa@claude-plugins-official`); legacy `mcp__exa__web_search_exa` still mounted; both backends route to the same Exa API.

**Citation:** every Exa-derived claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` per `.claude/rules/ontology.md`.

**Quality gate:** ≥3 sources per major claim, ≥50% `[VERIFIED]` confidence, date filter for any "recent / latest" claim, no `WebSearch` fallback without flagging the data gap.

Worked examples + tool catalog: `.claude/skills/meta-skills/exa/`.

## Output

Produces an Expert POV deliverable saved as `expert-pov/MMYY-{founder}.md` in the client folder. The deliverable carries 10 sections per the canonical structure in `references/output-template.md`:

1. Executive summary (with core philosophy + OBI recommendation)
2. Belief map (core beliefs + implicit assumptions + push-back)
3. Contrarian positions (hot takes table)
4. Origin stories (2-3, with moment / realization / shape)
5. Taste profile (admires + rejects + quality signals)
6. Theme clusters (3-5)
7. OBI candidates (3-5, scored)
8. Recommended OBI (philosophy + activation plan + proof points)
9. Raw material bank (quotes, story assets, 20+ content angles)
10. Data gaps

**Anti-hallucination guardrails (must apply):** quote verbatim; mark inferences explicitly; never invent stories; trace every OBI to stated beliefs; mark unknowns as gaps; assign High/Medium/Low to contrarian level. **Thin-input guard:** if founder input yields fewer than 3 beliefs + 1 origin story + 1 contrarian position, **do not proceed to OBI synthesis** — report thin input back and request follow-ups. (Adopted from Gooseworks `industry-scanner` via `/steal` 2026-04-21.)

Pre-delivery checklist (content / OBI / evidence / completeness), iteration prompts, integration map with downstream skills (positioning, product-messaging, linkedin-content, storytelling, landing-page-copy), and MCP data integration (Exa / Granola / YouTube) → `references/quality-and-guardrails.md`.
