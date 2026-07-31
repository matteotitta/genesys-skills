---
name: signup-onboarding-audit
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Audits a product's signup form and post-signup onboarding flow against time-to-value primacy, field-friction mechanics, activation-metric definition, and 3–7 step checklist patterns. Produces priority-ranked recommendations and A/B test hypotheses. Merges Corey Haines's separate signup + onboarding skills into one audit pair. Triage half (signup-onboarding-incident-response) deferred per audit-triage-pairing.md. Triggered by "signup audit", "onboarding audit", "activation review", "why are users dropping off", "fix the signup flow".
goal: Surface signup and onboarding friction points with priority-ranked recommendations + A/B test hypotheses.
outcome: Produces (1) signup field-by-field audit, (2) onboarding step-by-step audit, (3) activation-metric definition, (4) priority-ranked recommendations sorted by impact × ease, (5) A/B hypotheses ready for `/ab-testing`.
primitive: website
sub_primitive: audit
ontology_type: content-audit
review_gate: 2
inputs:
  required: []
  recommended:
  - product-messaging
  - icp-behavioural
  - analytics-tracking-plan
- type: content-audit
  feeds_into:
  - ab-testing
depends_on: []
- ab-testing
- in-app-popups
owned_by_agent: growth
mcps_used:
- exa
- firecrawl
- gdrive
triggers:
  slash_commands:
  - /signup-onboarding-audit
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /signup-onboarding-audit — pre/intra-product friction audit

Audit the journey from "first click on Sign Up" through "first aha moment" with sharp heuristics on field friction, time-to-value, activation-metric definition, and checklist patterns.

This is the **measurement half** of the audit-triage pair. The triage counterpart `signup-onboarding-incident-response` is deferred per `.claude/rules/audit-triage-pairing.md` until a client triggers the build (likely ClientCo Q3 activation work).

---

## When to invoke

- Activation rate is below the team's gut threshold and the cause is unclear.
- A signup flow has visible drop-offs in analytics and prioritization is needed.
- An onboarding sequence (in-product checklist, email triggers, tooltips) hasn't been audited since launch.
- A client is preparing for a growth push and wants the activation engine inspected before scaling acquisition.

Do NOT invoke when:
- The product has no signup (sales-led only) — sales-process audit instead.
- The activation metric is undefined — define it first via the activation-metric definition step, then audit.

---

## Workflow

### Step 1 — Define the activation metric

The single specific action that correlates with retention. Examples:
- B2B SaaS: "User invited 1 teammate within 7 days" or "User completed 1 core workflow within 14 days".
- Vertical SaaS: "User connected their primary data source within 24 hours" (ClientCo: "connected first client account") or "User generated their first report".
- Marketplace: "User completed first transaction within 30 days".

If the client cannot name the activation metric, that's the first finding. No further audit until defined — measuring against an undefined target produces theatre, not signal.

### Step 2 — Signup field audit

Catalog every field on the signup form. For each, classify:

| Class | Examples | Rule |
|---|---|---|
| Essential | Email, password (or magic-link) | Keep |
| Deferrable | Company, role, phone | Move to post-signup or progressive profiling |
| Inferred from email | Company name, role guess | Don't ask — auto-fill |
| Vanity | "How did you hear about us", marketing consent | Cut from signup, ask later |

**Sharp rules:**
- 3 or fewer fields → single-step form OK.
- 4+ fields → multi-step with progress indicator.
- Password requirements visible upfront (don't ambush at submit).
- Mobile: large touch targets, autofill-friendly field types (`type="email"`, `autocomplete="email"`).
- "Takes 30 seconds" messaging sets expectations and reduces abandonment.

### Step 3 — Onboarding flow audit

Map the path from signup confirmation to activation-metric hit. For each step, score:

- Time-to-value contribution: does this step move the user closer to the aha moment or away?
- Friction: how many decisions / inputs / waits does it impose?
- Necessity: would removing this step lose anything?

**Sharp rules:**
- Checklist length: 3–7 items. Fewer feels trivial; more overwhelms.
- Order by impact: highest-leverage step first, not easiest.
- "Do, don't show" — interactive completion beats tutorial videos.
- Tour length: 3–5 steps maximum before exhaustion.
- Celebrate completions visibly (progress bars, confetti, badges).

### Step 4 — Multi-channel coordination

Onboarding ≠ in-product only. Audit the email triggers, in-app prompts, and `/in-app-popups` overlays in coordination:

- Day 0 email (immediately post-signup): pointer to the next critical step.
- Day 1 trigger (if no activation): friction-removal nudge specific to the stuck step.
- Day 3, 7 triggers: per-state, not per-time.

Misalignment (email says "do X" while in-product says "do Y") is a common finding.

### Step 5 — Priority-ranked recommendations

Score each recommendation on Impact × Ease (5 × 5 = 25 max):

| Finding | Recommendation | Impact (0-5) | Ease (0-5) | Score | Priority |
|---|---|---|---|---|---|
| 8-field signup form, 47% drop-off at "company size" | Cut "company size" + "industry" from signup; add to first onboarding step | 5 | 5 | 25 | P0 |
| No activation metric defined | Define metric via 1-hour team workshop | 5 | 4 | 20 | P0 |
| Day-3 email fires regardless of state | Convert to state-based trigger | 4 | 3 | 12 | P1 |
| Tour is 9 steps long | Cut to 5 steps; defer 4 to contextual hover | 3 | 4 | 12 | P1 |

Top 3 land in the action queue; below that goes to a backlog.

### Step 6 — A/B hypotheses for `/ab-testing`

Each high-priority recommendation becomes an A/B hypothesis in the format from `/ab-testing`:

> "Because [observation], we believe [change] will cause [outcome] measured by [metric] within [timeframe]."

Example:
> "Because 47% of users drop off at the company-size field, we believe removing the field will increase signup completion by 25% measured by signup-completion-rate within 2 weeks."

Hand off the formatted hypotheses to `/ab-testing` for sample-size calculation and test design.

---

## {Product / Client} signup + onboarding audit

### Activation metric
- Defined: ✅ {metric statement} / ❌ {first finding: define this}

### Signup field audit
| Field | Class | Recommendation |
|---|---|---|
| email | Essential | Keep |
| company | Deferrable | Move to post-signup |
|...

### Onboarding flow audit
- Step 1: {description} — {time-to-value contribution: high/med/low} — {friction: high/med/low} — {keep/cut/reorder}
-...

### Multi-channel coordination findings
- Email Day 0:...
- In-product trigger Day 1:...
- Coordination misalignment: {if any}

### Priority-ranked recommendations
- P0: {top 3 recs with Impact × Ease scores}
- P1: {next 3-5 recs}
- Backlog: {rest}

### A/B hypotheses (formatted for /ab-testing)
- H1: Because..., we believe..., measured by..., within...
- H2:...
```

---

## Integration with other skills

- **Upstream:** `/analytics-tracking-plan` provides the event taxonomy needed to measure drop-offs; `/product-messaging` defines the value-prop the signup form sells against.
- **Downstream:** Hypotheses feed `/ab-testing` (test design + sample-size math); in-product overlay redesigns feed `/in-app-popups`.
- **Triage half (deferred):** `signup-onboarding-incident-response` per `.claude/rules/audit-triage-pairing.md`. Backlog noted; build when a client triggers an incident-mode use case.

---

## Anti-patterns

- ❌ Audit without an activation metric. You're measuring noise.
- ❌ Recommend "redesign the signup page" without per-field reasoning. Friction is field-level.
- ❌ Prioritize by ease alone (easy wins) instead of impact × ease.
- ❌ Audit signup or onboarding alone, not both. The handoff is where most friction lives.
- ❌ Tutorial-heavy onboarding when "do, don't show" applies.

---

## Attribution

This skill merges and adapts patterns from [`coreyhaines31/marketingskills/signup/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/signup/SKILL.md) and [`coreyhaines31/marketingskills/onboarding/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/onboarding/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice; merged into one audit skill per user direction. Triage half deferred per audit-triage-pairing rule.

---

