---
name: client-discovery
version: '1.2'
last_updated: 2026-04-16
author: genesys-growth
description: Prepares discovery call materials including company research, opening playbook, tailored call agendas, qualification
  questions, and listening cues. Produces a call prep doc with personal connection hooks, preparation references, signals
  mapped to proposal scoping dimensions, and chain into sales-call-playbook for during-call guidance. Consumes company-context
  as upstream input for prospect intelligence. Feeds into sales-call-playbook (during-call guide) and client-proposals (post-call
  scoping). Triggered by "discovery call", "call prep", "qualification", "prepare for call with [company]", or "discovery
  questions for [prospect]".
goal: Prepares discovery call materials including company research, opening playbook, tailored call agendas, qualification
  questions, and listening cues.
outcome: Prepares discovery call materials including company research, opening playbook, tailored call agendas, qualification
  questions, and listening cues. Produces a call prep doc with personal connection hooks, preparation references, signals
  mapped to proposal scoping dimensions, and chain into...
primitive: clients
ontology_type: client-engagement
review_gate: 2
inputs:
  required: []
  recommended: []
- type: client-engagement
  feeds_into:
  - client-proposals
  - client-onboarding
depends_on: []
- client-proposals
- client-onboarding
owned_by_agent: b2b-consultant
mcps_used:
- apollo-io
- exa
- firecrawl
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
paths: projects/consulting/**, projects/prospects/**
---

## Research source (Exa)

**Default:** Exa, per `.claude/rules/exa-protocol.md` (auto-loaded for research, audit, competitor, ICP, AEO, content sourcing, sales prospecting work).

**Primary Exa tools for this skill:** `company_research_exa, web_search_exa`.

**Use case:** pre-call account intel for prospect-prep.

**Tool surface during the migration window:**
- New plugin (preferred): `mcp__plugin_exa_exa__company_research_exa` (after `claude plugin i exa@claude-plugins-official`).
- Legacy MCP (still mounted): `mcp__exa__company_research_exa`.
- Both backends route to the same Exa API — they don't double-bill.

**Citation:** every Exa-derived claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` per `.claude/rules/ontology.md`.

**Quality gate (research outputs):** ≥3 sources per major claim, ≥50% `[VERIFIED]` confidence, date filter for any "recent / latest" claim, no fallback to `WebSearch` without flagging the data gap.

**Worked examples + tool catalog:** `.claude/skills/meta-skills/exa/`.

---

# Client discovery

Generate tailored discovery call scripts based on prospect context. Maps research to targeted questions and listening cues for qualification.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`outbound-research-hygiene.md`](../../../../rules/outbound-research-hygiene.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (discovery script is internal rep-facing — inline cites stay for QA), R3 (question framing operator-direct), R9 (verb-led script section names).

---

## Process at a glance

```
INPUT VALIDATION → RESEARCH PROSPECT → GENERATE QUESTIONS → ADD CUES → REVIEW & CHAIN
```

Three steps:
1. Research prospect website + LinkedIn + sent materials, build opening playbook
2. Generate tailored questions across 8 categories
3. Add listening cues + qualification criteria

Full flowchart, step-by-step runbook, and self-evaluation gate live in the premium reference.

---

## Claude Code triggers

**Invoke this skill when user says:**
- "Discovery call for [company]"
- "Discovery questions for [prospect]"
- "Prepare for discovery with [company]"
- "Qualify this prospect"
- "Discovery prep"

**Do NOT invoke when:**
- User wants company research only → Use `company-context` skill
- User wants to create a proposal → Use `client-proposals` skill
- User wants ICP research for a client → Use `icp-behavioural` skill

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Company identifier** | Website URL, name, or any context | User provides |

### Optional (improve quality)

| Input | How it helps |
|-------|--------------|
| company-context output | Pre-researched traction and qualification |
| Funding stage | Sets expectations for budget and scope |
| Known pain points | Focuses discovery questions |
| Meeting context | Any prior conversations or emails |

**If inputs are missing:** Ask for company URL or name.

---

## Discovery question categories (8 total)

| Category | Purpose | Anchor question | Time |
|----------|---------|-----------------|------|
| **Company/product** | Stage, GTM motion, marketing function | "How is your marketing function structured today?" | 5-7 min |
| **Goals and priorities** | Triggers, success metrics, past failures | "What triggered this conversation now?" | 5-7 min |
| **ICP and competitive** | Buyer personas, competitors | "Who are your top 3 competitors?" | 5-7 min |
| **Messaging and positioning** | Current frameworks, customer voice | "How would your best customers describe you?" | 5-7 min |
| **Website and conversion** | Satisfaction, scope, resources | "What's your conversion rate today?" | 3-5 min |
| **Content and distribution** | Founder time, LinkedIn priority | "How much time can founders dedicate to content?" | 3-5 min |
| **Resources and constraints** | Budget, team, decision-makers | "What's the budget range you're working with?" | 3-5 min |
| **Timeline and next steps** | Urgency, process | "When do you need to see results?" | 3-5 min |

Full question bank by category in the premium reference.

---

## Anti-hallucination guardrails

1. **Base context on research.** Use actual website content, not assumptions.
2. **Tailor questions to findings.** Reference specific things you observed.
3. **Mark assumptions.** If inferring from limited data, note explicitly.
4. **No invented details.** If you can't find funding info, don't make it up.

---

## Integration with other skills

| Skill | Relationship |
|-------|--------------|
| **company-context** | Pre-research prospect before discovery |
| **sales-call-playbook** | Generate during-call guide (run immediately after discovery) |
| **client-proposals** | Create proposal after discovery call |

---

## MCP data integration

**Level:** 0 — Context (heavy pulls)

**Inherits from:** company-context (if already ran for this company — skip Exa/Firecrawl/Apollo)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Exa** | Prospect company profile | `company_research_exa` | Always |
| **Firecrawl** | Prospect website scrape | `firecrawl_scrape` | Always |
| **Apollo** | Org + key people enrichment | `apollo_search_companies`, `apollo_search_people` | Always |
| **YouTube** | Prospect YouTube presence/content | `get_transcript` | If YouTube channel exists |
| **Slack** | Prior conversations with prospect | `slack_search_public` | Always |
| **Granola** | Previous meetings with prospect | `search_meetings` | Always |

### Fallback (no MCP)

- WebSearch + WebFetch for prospect research
- Manual LinkedIn research for contacts
- Manual conversation history review

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

