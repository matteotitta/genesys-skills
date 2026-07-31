---
name: client-proposals
version: '2.0'
last_updated: 2026-01-21
author: genesys-growth
description: Creates client proposals with context formula, scope of work, pricing, and timeline after discovery calls. Produces
  a structured proposal document following the Genesys Growth engagement format, exported to Google Docs or Notion. Depends
  on client-discovery for qualification signals and scoping dimensions. Feeds into client-onboarding upon deal close and informs
  downstream skill chains (icp-behavioural, competitor-research, positioning). Gate 4 collaborative review required. Triggered
  by "write proposal", "scope of work", "SOW", "proposal for [client]", or "price this engagement".
goal: Creates client proposals with context formula, scope of work, pricing, and timeline after discovery calls.
outcome: Creates client proposals with context formula, scope of work, pricing, and timeline after discovery calls. Produces
  a structured proposal document following the Genesys Growth engagement format, exported to Google Docs or Notion. Depends
  on client-discovery for qualification signals and scoping...
primitive: clients
ontology_type: client-engagement
review_gate: 4
inputs:
  required:
  - client-discovery
  recommended:
  - company-context
- type: proposal
  feeds_into:
  - icp-behavioural
  - competitor-research
  - tov-guidelines
  - positioning
  - client-onboarding
depends_on:
- client-discovery
- competitor-research
- icp-behavioural
- positioning
- tov-guidelines
- client-onboarding
owned_by_agent: b2b-consultant
mcps_used:
- gdrive
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
effort: max
paths: projects/consulting/**, projects/prospects/**
---

# Client proposals

Generate scope-of-work proposals for B2B SaaS GTM consulting engagements. Map discovery insights to phased deliverables with defensible pricing. Gate 4 — pause for collaborative review before finalizing.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`doc-output-structure.md`](../../../../rules/doc-output-structure.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (proposal is client-team review surface — cleaned `[VERIFIED:...]` tags in appendix toggle, never inline in face doc), R2 (multi-phase proposal ships as one doc with toggles per phase), R3 (engagement framing operator-direct, never "thrilled to propose"), R5 (proposal opener mirrors discovery-call insight verbatim), R6 (close → signed proposal primary, kickoff scheduling as fallback), R9 (verb-led phase + deliverable names).

## When to run

Run when the user says: "create proposal for [company]", "scope of work for [company]", "create SOW", "GTM consulting proposal", "help me scope this project", or after a discovery call completes with notes available.

Don't run when the user wants discovery-call prep (`discovery`), pure company research (`company-context`), or post-signature ICP work (`icp-behavioural`).

## Inputs

Required:

- **Company identifier** — name or website. Verify it can be uniquely identified.
- **Discovery insights** — call notes, meeting transcript, or discovery doc covering pain points, goals, signals.

Recommended (sharpen scope and pricing):

- Budget signals (sets pricing band).
- Timeline constraints (affects phasing).
- Team resources — in-house designer, dev, content, etc. (affects scope).
- Specific deliverable requests.

If discovery insights are missing → ask for notes or run `discovery` first. Don't fabricate context.

## Steps

1. Pull upstream context — read `discovery` output and (if available) `company-context` output for the prospect. Pull Slack history (`slack_search_public`) and Granola meeting notes (`search_meetings`) for fresh context.
2. Map signals → deliverables — review pain points and goals; match against the six categories in the premium reference (foundational, website, content/distribution, launch support, sales enablement, customer marketing). Every line item must trace to a discovery signal.
3. Set pricing band — pick a scope type from the pricing table in the premium reference; adjust for stage, scope breadth, budget signals, complexity. Apply standard terms (3-month commitment, 30-day notice, auto-renewal).
4. Draft the context paragraph using the canonical formula: `[Company] is [1-sentence description]. The platform serves [ICP] who need to [primary use case]. [Value prop]. Fresh off [milestone/trigger], the team needs [deliverable] to [outcome].` Two to three paragraphs total — company overview, current situation, goals from discovery.
5. Phase the deliverables — Month 1 = foundation (research, audits); Month 2-3 = strategy + execution; Month 4+ = optional future scope. Foundation always precedes execution. Reflect client urgency (launch dates, board meetings, seasonal windows) in the timeline, not generic 4-week blocks.
6. Assemble the document using the markdown template in the premium reference — title, [Month Year] subtitle, Context, Deliverables (with the standard tentative-scope disclaimer), Terms, Collaboration. Use `- [ ]` for all deliverable items (Google Docs checklist conversion). Keep checklist items flat per workstream.
7. Run the self-evaluation in the premium reference — completeness, evidence quality, guardrails, self-roast. If anything fails, fix or flag before delivery.
8. Pause for Gate 4 collaborative review — multi-round co-creation. Review scope accuracy, pricing, phasing, terms with the user before finalizing.
9. After approval, offer the post-output options (adjust scope/pricing, push to Google Docs in `PJ - Proposals`, add/remove deliverables).

## What good looks like

**Examples (10 closed engagement proposals):**

**Evaluations (pre-delivery checklist):**

- Context paragraph shows specific understanding of the situation (not generic).
- Every deliverable maps to a documented discovery signal.
- Phasing is logical — foundation before execution.
- Pricing matches scope and budget signals.
- Terms section complete — commitment, notice, auto-renewal.
- Collaboration section includes start date, reporting line, team needs.
- `- [ ]` checkbox format used throughout deliverables.
- Standard tentative-scope disclaimer included.
- No invented company details, metrics, or testimonials.

Full self-evaluation protocol (completeness, evidence quality, guardrails, five self-roast questions, improvement suggestion format) → the premium reference.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
