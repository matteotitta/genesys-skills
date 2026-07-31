---
name: sales-enablement
version: '3.0'
last_updated: 2026-02-06
author: genesys-growth
description: 'Orchestrates sales enablement asset creation by routing to dedicated sub-skills: /sales-deck for presentation
  decks, /battlecards for competitive battlecards, and /demo-script for demo talk tracks. Handles remaining asset types directly
  including ROI calculators, objection handlers, discovery guides, competitive one-pagers, deal qualification checklists,
  and pricing guides. Consumes competitor-research, product-messaging, icp-behavioural, and win-loss-analysis as upstream
  context. Triggered by "sales enablement", "sales assets", "sales collateral", or requests for any sales-facing materials.'
goal: 'Orchestrates sales enablement asset creation by routing to dedicated sub-skills: /sales-deck for presentation decks,
  /battlecards for competitive battlecards, and /demo-script for demo talk tracks.'
outcome: 'Orchestrates sales enablement asset creation by routing to dedicated sub-skills: /sales-deck for presentation decks,
  /battlecards for competitive battlecards, and /demo-script for demo talk tracks. Handles remaining asset types directly
  including ROI calculators, objection handlers, discovery...'
primitive: sales-enablement
ontology_type: sales-enablement-asset
review_gate: 2
inputs:
  required: []
  recommended:
  - competitor-research
  - product-messaging
  - icp-behavioural
  - win-loss-analysis
- type: sales-asset
  feeds_into:
  - product-launch
  - outreach-emails
depends_on: []
- outreach-emails
- product-launch
owned_by_agent: sales
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
effort: high
---

# Sales enablement

Orchestrator for sales enablement assets. Routes to dedicated sub-skills for decks, battlecards, demo scripts, and CX/chatbot demos. Handles ROI calculators, objection handlers, discovery guides, competitive one-pagers, deal qualification checklists, and pricing guides directly.

## When to run

- User asks for sales-facing material: ROI calc, objection handler, discovery guide, competitive one-pager, qualification checklist, pricing guide
- User says "sales enablement", "sales assets", "sales collateral" with no specific asset type → ask which type, route accordingly
- competitor-research or product-messaging just completed → offer to derive battlecards / sales deck / demo script
- User wants a live sales demo for a prospect → route to `/cx-assessment` or `/chatbot-assessment`
- Do **not** run for: standalone competitor research, standalone messaging, win-loss analysis, landing-page copy. Route to those skills directly

## Inputs

Required (at least one):
- URL for research
- Attachment: existing messaging, ICP docs, sales notes
- Skill reference: output from `competitor-research`, `product-messaging`, `icp-behavioural`, `win-loss-analysis`

Plus: confirmed **asset type** (battlecard, ROI calc, sales deck, objections, discovery guide, one-pager, qualification, pricing). If missing, ask before proceeding. Minimum-context-by-asset matrix in the premium reference ("Minimum context by asset type").

## Steps

1. **Route or own.** If user asked for sales deck / battlecard / demo script / CX / chatbot → invoke the dedicated sub-skill (see Sub-skills table below) and stop. Otherwise continue here for the 6 asset types this skill owns.
2. **Validate inputs.** Confirm asset type, target (competitor or persona), and at least one context source. Surface gaps explicitly.
3. **Phase 1 — context gathering.** Inventory attachments + URLs + referenced skill outputs. Map to asset requirements. Offer to run upstream skills (`/competitor-research`, `/product-messaging`, `/icp-behavioural`, `/win-loss-analysis`) for any gap. Checkpoint: minimum context for selected asset is available.
4. **Phase 2 — asset generation.** Select template per asset (objection-handler / discovery-guide frameworks inlined in playbook; full templates in the premium reference). Generate content; source every claim with confidence (High / Medium / Low / [UNVERIFIED]); mark gaps explicitly. Checkpoint: all claims sourced or marked.
5. **Phase 3 — delivery.** Format per asset: Markdown (handlers, guides, qualification, pricing), interactive HTML (ROI calculator), Markdown/PDF (one-pager). Run quality checklist.
6. **Self-evaluation.** Run completeness + evidence + guardrail + actionability checks (full protocol in the premium reference). Roast: would a sales rep actually use this in a call, or is it too generic?
7. **Review gate 2.** User reads + approves; reviews claim accuracy, competitive intel, actionability.
8. **Chain suggestions.** If asset approved → suggest companion assets (battlecard → sales deck; discovery guide → demo script; ROI calc → pricing guide). Offer export to Google Docs / Notion.

## What good looks like

### Sub-skills (dedicated — route, don't reimplement)

| Skill | Path | Invoke | Use when |
|-------|------|--------|----------|
| Sales deck | `sales-deck/SKILL.md` | `/sales-deck` | Prospect presentations (PPTX, Google Slides, Google Docs) |
| Battlecards | `battlecards/SKILL.md` | `/battlecards` | Competitive intelligence for sales calls |
| Demo script | `demo-script/SKILL.md` | `/demo-script` | Product demo talk tracks and click paths |
| CX assessment | `../client-skills/ClientCo-cx/cx-assessment/SKILL.md` | `/cx-assessment [Company]` | Live sales demo — branded CX dashboard from prospect's public data |
| Chatbot assessment | `../client-skills/ClientCo-cx/chatbot-assessment/SKILL.md` | `/chatbot-assessment [Company]` | Live sales demo — Bot Intelligence Score 0-100 with live testing |

**Routing rule:** never handle deck / battlecard / demo / CX / chatbot directly — invoke the sub-skill. CX + chatbot live in `client-skills/ClientCo-cx/` (originally ClientCo); reusable as-is on any prospect. CTA override: `--cta <url>` switches the lead-capture CTA from `ClientCo.ai/contact` to your brand. Detail: the premium reference.

### Asset types this skill owns

| Asset | Format | Primary sources | Template |
|-------|--------|-----------------|----------|
| ROI calculator | Interactive HTML | product-messaging + icp-behavioural | the premium reference |
| Objection handler | Markdown | win-loss-analysis + competitor-research | the premium reference |
| Discovery guide | Markdown | icp-behavioural + product-messaging | the premium reference |
| Competitive one-pager | Markdown / PDF | competitor-research | the premium reference |
| Deal qualification | Markdown | icp-behavioural + win-loss-analysis | the premium reference |
| Pricing guide | Markdown | competitor-research + win-loss-analysis | the premium reference |

### Anti-hallucination guardrails (sales credibility is everything)

- Never invent competitor claims — verified data with sources only
- Never fabricate customer quotes — verbatim or `[PLACEHOLDER: need customer quote]`
- Never estimate ROI numbers without methodology label
- Confidence levels (High/Medium/Low) on all competitive intel
- Cite sources for all factual claims
- Acknowledge gaps rather than fill with plausible content

### Evaluations

- All claims sourced or marked [UNVERIFIED]
- Confidence levels (High / Medium / Low) on every competitive claim
- No invented data points or quotes
- Output header includes asset type, target, generated date, context sources used
- Format matches asset type (MD / PPTX / HTML / PDF)
- Sales rep can use immediately without translation
- Upstream skills (competitor-research, product-messaging, icp-behavioural, win-loss-analysis) referenced where used
- Review gate 2 passed before delivery

