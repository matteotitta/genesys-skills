---
name: lifecycle-marketing
version: '1.0'
last_updated: '2026-04-30'
description: Designs multi-channel lifecycle campaigns for onboarding, activation, retention, and churn prevention. Produces
  email sequences with trigger logic, timing, and channel orchestration across email, push, SMS, in-app, and paid social.
  Triggers on "lifecycle marketing", "onboarding sequence", "activation emails", "retention campaign", "churn prevention",
  or "customer lifecycle". Requires product-messaging as upstream input. NOT for lead nurture or drip sequences — use email-nurture
  instead.
goal: Designs multi-channel lifecycle campaigns for onboarding, activation, retention, and churn prevention.
outcome: Designs multi-channel lifecycle campaigns for onboarding, activation, retention, and churn prevention. Produces email
  sequences with trigger logic, timing, and channel orchestration across email, push, SMS, in-app, and paid social. Triggers
  on "lifecycle marketing", "onboarding sequence",...
primitive: lifecycle
ontology_type: lifecycle-campaign
review_gate: 2
inputs:
  required:
  - icp-behavioural
  - product-messaging
  recommended: []
- type: lifecycle-campaign
  feeds_into:
  - email-nurture
depends_on:
- icp-behavioural
- product-messaging
- email-nurture
owned_by_agent: growth
mcps_used:
- exa
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

# Lifecycle Marketing

Generate production-ready lifecycle marketing campaigns for B2B SaaS products across email, push, SMS, in-app messaging, and paid social.

For full process, lifecycle stages, campaign templates, and emotional cue framework → the premium reference.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`marketing-psychology.md`](../../../../rules/marketing-psychology.md) — 8 anchored heuristics
- [`doc-output-structure.md`](../../../../rules/doc-output-structure.md) — GDoc/Notion structural defaults (campaign planning docs)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in lifecycle-marketing |
|---|---|---|
| **R1** | Source placement (three layers) | Customer-facing surfaces (email, push, SMS, in-app, paid social) → **no sources block.** Campaign planning doc (client-team review) → cleaned `[VERIFIED:...]` tags in a collapsed appendix toggle. |
| **R2** | Single-doc-with-toggles | Cross-channel campaigns ship as **one campaign doc with one toggle per channel/asset** — not 5 separate files for email + push + SMS + in-app + paid. Index up top. |
| **R3** | Product-update tone | Even feature-driven campaigns frame as "[Product] now does X" not "we're thrilled to announce." |
| **R5** | Blog as voice anchor | Cross-channel campaigns with an anchor blog post mirror the blog's opening line across every channel verbatim. Voice drift across channels is the loudest tell of multi-author lifecycle campaigns. |
| **R6** | CTA hierarchy | Warm-base lifecycle → product-action CTA primary (open feature, complete onboarding, upgrade). Trial/sign-up only when re-engaging churned or upgrading free → paid. Blog as fallback. |
| **R9** | Action-oriented section names | "How to activate [Product]" beats "Activation playbook." Verb-led across campaign brief sections + asset titles. |

---

## Research source (Exa)

**Default:** Exa per `.claude/rules/exa-protocol.md`.

**Primary tools:** `web_search_exa` for competitor lifecycle / nurture flow research.

**Tool surface:** prefer `mcp__plugin_exa_exa__web_search_exa`; legacy `mcp__exa__web_search_exa` still mounted.

**Citation:** every claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]`.

**Quality gate:** ≥3 sources per major claim, ≥50% `[VERIFIED]`, date filter for any "recent / latest" claim.

---

## Campaign philosophy

Effective lifecycle marketing isn't about sending more messages — it's about sending the right message at the right moment through the right channel. Every campaign should:

- Map to specific user behaviors and lifecycle stages (not arbitrary time delays)
- Drive measurable outcomes (activation, adoption, retention, expansion)
- Respect channel-appropriate copy lengths and formats
- Test emotional angles systematically (urgency, exclusivity, curiosity, etc.)
- Include clear CTAs that align with the user's current journey stage

---

## Three-phase workflow

| Phase | Purpose | Deliverable |
|-------|---------|-------------|
| **1. Discovery** | Gather context, goals, segments, channels | Campaign brief |
| **2. Strategy** | Map lifecycle stages, triggers, messaging hierarchy | Strategy doc |
| **3. Generation** | Produce channel-specific copy with variants | Production-ready copy files |

For full discovery questions, lifecycle stage mapping, campaign templates, and per-channel specs → the premium reference.

---

## Required inputs

| Input | Required | Purpose |
|-------|----------|---------|
| **Campaign goal** | Yes | What behavior/outcome are we driving? |
| **Company name** | Yes | Personalization + UTM parameters |
| **Product description** | Yes | What does the product do? Key value props |
| **Lifecycle stage** | Yes | Where are users in their journey? |
| **Target audience** | Yes | Who are we messaging? (role, seniority, segment) |
| **Channels needed** | Yes | Email / push / SMS / in-app / paid social |
| **Number of messages** | Recommended | How many touchpoints in the sequence? |
| **Sender/From name** | Recommended | Personal name vs. company name |
| **Existing brand context** | Optional | TOV guidelines, messaging frameworks, previous campaigns |

---

## Anti-Hallucination Guardrails

1. **Ground claims in context.** All product benefits must come from provided context.
2. **No invented metrics.** Use provided proof points or mark as `[PLACEHOLDER: metric]`.
3. **No invented testimonials.** Only use provided quotes.
4. **Mark missing context.** Use `[PLACEHOLDER: description]` for unconfirmed details.
5. **Respect channel constraints.** Stay within word count limits.
6. **No fake urgency.** Only use urgency cues when there's real time pressure.

---

## Integration with Other Skills

| Skill | Integration point |
|-------|-------------------|
| **product-messaging** | Value props, capabilities, benefits for copy |
| **icp-behavioural** | Persona pain points, motivations, language |
| **tov-guidelines** | Brand voice, editorial patterns, word choices |
| **landing-page-copy** | Consistent messaging with landing pages |
| **email-nurture** | Downstream — pre-conversion drip sequences |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

