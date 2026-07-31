---
name: email-nurture
version: '1.0'
last_updated: 2026-01-17
author: genesys-growth
description: Creates post-download and post-demo nurture email sequences with timing, trigger logic, and progressive engagement
  toward conversion. Produces email copy, subject lines, send cadence, and exit criteria for marketing automation. Triggers
  on "nurture emails", "drip sequence", "follow-up emails", "post-download sequence", "post-demo nurture", or "lead nurture".
  NOT for onboarding, activation, or lifecycle emails — use lifecycle-marketing instead.
goal: Creates post-download and post-demo nurture email sequences with timing, trigger logic, and progressive engagement toward
  conversion.
outcome: Creates post-download and post-demo nurture email sequences with timing, trigger logic, and progressive engagement
  toward conversion. Produces email copy, subject lines, send cadence, and exit criteria for marketing automation. Triggers
  on "nurture emails", "drip sequence", "follow-up emails",...
primitive: lifecycle
ontology_type: lifecycle-campaign
review_gate: 2
inputs:
  required:
  - lifecycle-marketing
  recommended: []
- type: lifecycle-campaign
  feeds_into: []
depends_on:
- lifecycle-marketing
owned_by_agent: growth
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /email-nurture
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# Email Nurture

Create email nurture sequences that move prospects from content engagement to demo request, and from demo to closed deal. Focused on marketing automation sequences — not transactional or onboarding emails.

For full process, sequence templates, and email writing formulas → the premium reference.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`marketing-psychology.md`](../../../../rules/marketing-psychology.md) — 8 anchored heuristics (Rule of 7, loss aversion, JTBD)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in email-nurture |
|---|---|---|
| **R1** | Source placement (three layers) | Emails are **end-customer-facing**. **No sources block in body.** Internal QA cites live in working draft only; stripped before scheduling. |
| **R3** | Product-update tone | Any product/feature mention in nurture frames as "[Product] now does X" not "we're thrilled to announce." Even feature-launch nurture sequences. |
| **R5** | Blog as voice anchor | For content-follow-up sequences with an anchor blog/whitepaper, the email opener mirrors the blog's opening line verbatim. Channel-voice drift is the biggest tell of multi-author sequences. |
| **R6** | CTA hierarchy | Nurture targets prospects already in pipeline (warm-base). **Product-action CTA primary** (book a demo, start trial, open feature). Blog as fallback for not-ready-yet prospects. Never sign-up as primary (they're already signed up). |
| **R9** | Action-oriented section names | "How to upgrade" beats "Upgrade options." "Why [Product]" beats "About us." Verb-led across every email's subject + sections. |

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Email nurture sequence"
- "Post-download emails"
- "Demo follow-up emails"
- "Lead nurture sequence"
- "Content follow-up emails"
- "MQL nurture"
- "Email drip campaign"
- "Nurture sequence for [content]"
- "Follow-up sequence"
- "Re-engagement emails"

**Do NOT invoke when:**
- User wants onboarding emails → Use `lifecycle-marketing` skill
- User wants transactional emails → Different format
- User wants cold outreach → Use `outreach-emails` skill
- User wants one-off email → Write directly

---

## Input Requirements

### Required
| Input | Description | Source |
|-------|-------------|--------|
| **Trigger event** | What action starts the sequence | User specifies |
| **Sequence goal** | Desired outcome (demo, trial, meeting) | User specifies |
| **Audience context** | Who these people are | User or ICP research |

### Optional (improve quality)
| Input | How it helps |
|-------|--------------|
| Product messaging | Ensures alignment with positioning |
| Content asset | Specific asset they downloaded |
| Demo notes | Context from their demo |
| Persona details | Role, pain points, objections |
| Previous sequence performance | What's worked before |
| Send tool | Platform-specific constraints |

If trigger event, goal, or email count are missing, ask before generating.

---

## Core decisions

### Sequence cadence selector

| Trigger | Default emails | Spacing | Why |
|---------|---------------|---------|-----|
| Post-content download | 5 | Day 0, 2, 5, 8, 14 | Strike while interested |
| Post-demo | 5 | Day 0, 2, 4, 7, 14 | Maintain demo momentum |
| Re-engagement | 4 | Day 0, 7, 21, 45 | Longer gaps, fresh angles |

### Value escalation ladder

| Email | Commitment level | Subject pattern type |
|-------|-----------------|---------------------|
| 1 | Low | Reference trigger directly |
| 2 | Low-medium | Curiosity gap |
| 3 | Medium | Social proof |
| 4 | Medium-high | Direct ask |
| 5 | High | Final value + urgency or break-up |

### Constraints
- Subject lines: under 50 characters
- One CTA per email (no exceptions)
- Personalization tokens require fallbacks (`{{first_name|there}}`)

For full sequence templates, subject patterns, and copy frameworks → the premium reference.

---

## Anti-Hallucination Guardrails

1. **No invented case studies.** Only reference real customers if provided.
2. **No false urgency.** Don't claim deadlines that don't exist.
3. **Mark placeholders.** Use [COMPANY NAME] for unconfirmed references.
4. **Realistic metrics.** Don't promise specific outcomes unless verified.
5. **Platform-aware.** Note if formatting needs adjustment for specific ESP (HubSpot, Marketo, Customer.io).

---

## MCP Data Integration

**Level:** 2 — PM Execution (inherits upstream, no unique pulls)

**Inherits from:** product-messaging, lifecycle-marketing

**Pulls fresh:** NONE — messaging library provides all needed copy inputs.

**Fallback (no MCP):**
- Use product-messaging output directly
- If product-messaging hasn't run, trigger it first

---

## Integration with Other Skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **outreach-emails** | Related | Cold outreach vs. nurture |
| **lifecycle-marketing** | Related | Onboarding vs. pre-sale nurture |
| **case-study** | Provides input | Case studies for social proof emails |
| **product-messaging** | Provides input | Messaging for email copy |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

