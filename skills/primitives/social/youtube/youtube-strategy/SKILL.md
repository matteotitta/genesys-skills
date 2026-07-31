---
name: youtube-strategy
version: '1.0'
last_updated: 2026-04-21
author: genesys-growth
description: 'Builds a YouTube channel launch strategy for B2B SaaS operators. Outputs keyword demand analysis, competitor
  bucket segmentation, top-video gap analysis, 6 video ideas (with working titles + proven demand + the gap + your edge +
  format), case study / testimonial framework, and a Month-1 TOFU/BOFU mix. Input: company context + positioning (recommended)
  + past social engagement data (optional). Triggers: "YouTube strategy", "YouTube channel plan", "plan my YouTube", "video
  channel strategy", "what videos should I make on YouTube", "YouTube channel launch". NOT for individual scripts — feeds
  into youtube-scripts. NOT for LinkedIn/TikTok short-form — channel-specific.'
goal: Builds a YouTube channel launch strategy for B2B SaaS operators.
outcome: Builds a YouTube channel launch strategy for B2B SaaS operators. Outputs keyword demand analysis, competitor bucket
  segmentation, top-video gap analysis, 6 video ideas (with working titles + proven demand + the gap + your edge + format),
  case study / testimonial framework, and a Month-1...
primitive: social
sub_primitive: youtube
ontology_type: youtube-strategy
review_gate: 2
inputs:
  required:
  - positioning
  recommended: []
- type: youtube-strategy
  feeds_into:
  - youtube-scripts
depends_on:
- positioning
- youtube-scripts
owned_by_agent: content
mcps_used:
- ahrefs
- exa
- gdrive
- youtube-transcript
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

# YouTube Strategy

Generate a YouTube channel launch strategy for B2B SaaS operators. Output is a deck-style markdown document with keyword demand research, competitor segmentation, gap analysis, 6 video ideas, case-study / testimonial framework, and a Month-1 plan. Feeds into `youtube-scripts` for per-video production.

For full process, frameworks, and MCP integration → the premium reference.

---

## Research Substrate (Exa)

**Default:** Exa per `.claude/rules/exa-protocol.md`.

**Primary tools:** `web_search_exa` for competitor channel + keyword research.

**Tool surface during migration:** prefer `mcp__plugin_exa_exa__web_search_exa` (after `claude plugin i exa@claude-plugins-official`); legacy `mcp__exa__web_search_exa` still mounted.

**Citation:** every claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` per `.claude/rules/ontology.md`.

**Quality gate:** ≥3 sources per major claim, ≥50% `[VERIFIED]`, date filter for any "recent / latest" claim.

---

## Claude Code Triggers

**Invoke when user says:**
- "YouTube strategy for [company]"
- "Plan my YouTube channel"
- "What videos should I make on YouTube"
- "YouTube channel strategy / plan / launch plan"
- "Help me start a YouTube channel"
- "What's the opportunity on YouTube"
- "YouTube keyword research + video ideas"

**Do NOT invoke when:**
- User wants individual YouTube script → use `youtube-scripts`
- User wants LinkedIn video content → use `linkedin-content`
- User wants multi-channel content strategy → use `content-strategy`
- User wants content calendar / execution → use `content-operations`

---

## Input Requirements

### Client context (auto-loaded)
If working on a client project, client `CLAUDE.md` is auto-loaded. Pull positioning from `knowledge/positioning.md` and ICP from `knowledge/icp-definition.md`.

### Required
| Input | Description | Source |
|-------|-------------|--------|
| **Positioning statement** | 1-2 sentence who-you-are + what-you-do | `knowledge/positioning.md` or user |
| **ICP definition** | Who the channel targets | `knowledge/icp-definition.md` or user |

### Recommended (improves quality significantly)
| Input | How it helps |
|-------|--------------|
| Social engagement data | LinkedIn post reactions/comments per topic — fuels "proven demand" per idea |
| Client roster | Case-study candidate shortlist for BOFU videos |
| Content audit | Lets skill skip topics already covered |

### Optional
| Input | How it helps |
|-------|--------------|
| Niche hypothesis | Sharpens keyword seeding |
| Existing YouTube presence | Adjusts scope (launch vs relaunch vs refresh) |
| Competitor hypotheses | Seed list for channel scan |

### Validation checklist
Before proceeding:
- [ ] Positioning is 1-2 sentences with operator's specific angle (not generic)
- [ ] ICP is named (title + company type), not "small businesses" or "B2B"
- [ ] If LinkedIn data provided, it has post-level reactions/comments (not just topic themes)

If positioning or ICP is missing, ask before proceeding. Do not hallucinate.

---

## Anti-Hallucination Guardrails

1. **No invented keyword volumes** — always pull from Ahrefs MCP. If unavailable, mark `[UNAVAILABLE: Ahrefs pull failed]`.
2. **No invented engagement data** — "proven demand" per idea must cite real LinkedIn/Twitter/newsletter signal. If none, mark `[UNAVAILABLE]`.
3. **No invented case-study metrics** — pull from `knowledge/positioning.md` proof-points or user.
4. **No invented rankings** — for Phase 3 gap analysis, mark `[UNVERIFIED: manual check needed]` if YouTube SERP not run.
5. **Flag gap claims with source** — "nobody covers X" needs `[INFERRED: from competitor scan on {date}]`.
6. **Client roster dependency** — pull from client's `knowledge/profile.md` clients list or explicit user input.

---

## Process, Output, Quality, and Auto-Update

| Topic | Reference |
|-------|-----------|
| 5-phase process + frameworks + MCP integration | the premium reference |
| Output template + render targets + iteration prompts + handoff | the premium reference |
| Pre-delivery checklist + worked example + anti-examples + quality gate | the premium reference |
| 5-bucket competitor taxonomy with detection rules | the premium reference |
| 6-field video idea template with examples | the premium reference |
| Month-1 mix rules + funnel outcomes | the premium reference |
| Ahrefs MCP calls + competition scoring method | the premium reference |
| Worked example — Matteo's own YouTube strategy | `examples/0426-matteo-youtube-strategy.md` |

---

## Skill Relationships (per ontology.md)

```yaml
depends_on:
  - company-context # required — pulls positioning, clients, services
  - icp-profile # required — defines channel audience
  - positioning # recommended — sharpens "your edge" per idea
feeds_into:
  - youtube-scripts # per-video script production
  - content-operations # add Month-1 plan to weekly calendar
  - case-study # BOFU case-study production
enhances:
  - content-strategy # if multi-channel strategy exists, refines YouTube lane
```

Knowledge type produced: `youtube-strategy` (Level 1 — Strategy, review gate 2).

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

