---
name: analytics-tracking-plan
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Builds an analytics instrumentation plan. Defines the 5–10 critical events (Object-Action naming), standard properties (page/user/campaign/product), UTM strategy, and validation checklist. Tool-agnostic (GA4, PostHog, Mixpanel, Amplitude). Sits upstream of /ab-testing and /dashboard — neither can run on phantom metrics. Triggered by "analytics tracking plan", "event taxonomy", "GA4 setup", "PostHog events", "instrumentation plan", "what should we track". NOT for analysis or dashboarding — use /dashboard (post-hoc viz) or /experiment (hypothesis tracking).
goal: Define a deployable event tracking plan that connects business decisions to required data.
outcome: Produces (1) business-question-to-event mapping, (2) 5–10 critical events with Object-Action naming, (3) standard properties spec, (4) UTM strategy, (5) validation checklist (GTM Preview / Debug View, 48-hour stabilization).
primitive: website
sub_primitive: strategy
ontology_type: content-strategy
review_gate: 2
inputs:
  required: []
  recommended:
  - icp-research
  - funnel-strategy
  - product-messaging
- type: content-strategy
  feeds_into:
  - ab-testing
  - dashboard
depends_on: []
- ab-testing
- dashboard
- experiment
- signup-onboarding-audit
- revops
owned_by_agent: growth
mcps_used:
- exa
- gdrive
triggers:
  slash_commands:
  - /analytics-tracking-plan
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /analytics-tracking-plan — instrumentation before experiments

Build a deployable tracking plan before any experimentation or dashboarding work. Without this, every downstream measurement is phantom — /ab-testing has no events to count, /dashboard visualizes incomplete data, /signup-onboarding-audit can't measure drop-offs.

---

## Core principle — "track for decisions, not data"

Every tracked event must inform a decision someone is making. If no one would change behavior based on a metric, don't track it. **Quality > quantity: prioritize 5–10 critical events over 100 vanity metrics.**

Per source data (cite-verified, MIT): consistent naming conventions prevent ~40% of implementation bugs. Conversion data needs ~48 hours to stabilize before drawing inferences.

---

## Workflow

### Step 1 — Work backward from business questions

Don't start with "what events should we track?". Start with the questions:

| Business question | Required event |
|---|---|
| "Are people signing up?" | `signup_completed` |
| "Are they activating?" | `activation_milestone_hit` (per `/signup-onboarding-audit` definition) |
| "Are paid users using the product?" | `core_workflow_completed` |
| "Are referrals converting?" | `referral_clicked`, `referral_converted` (per `/referral-program`) |
| "Where is acquisition coming from?" | `traffic_source` property on every event |
| "Does marketing $X correlate with conversion?" | UTM + `signup_completed` join |

If a question doesn't have a clear required event, the question isn't decision-shaped — sharpen the question first.

### Step 2 — Define 5–10 critical events with Object-Action naming

Naming convention: `{object}_{action}` in past tense (action already happened when fired).

| Object | Action | Event name |
|---|---|---|
| signup | completed | `signup_completed` |
| account | created | `account_created` |
| trial | started | `trial_started` |
| trial | expired | `trial_expired` |
| subscription | upgraded | `subscription_upgraded` |
| subscription | cancelled | `subscription_cancelled` |
| feature_X | used | `feature_X_used` |
| referral | clicked | `referral_clicked` |
| pricing_page | viewed | `pricing_page_viewed` |
| demo | requested | `demo_requested` |

**Sharp rules:**
- Snake_case, past tense, no camelCase.
- Don't pre-empt every possible action — name 5–10 critical ones; add more later when business questions arrive.
- Avoid temporal events that mean different things to different consumers (`page_view` is fine; `user_engaged` is ambiguous).

### Step 3 — Standard properties on every event

Every event carries:

| Category | Properties |
|---|---|
| Page | `page_url`, `page_title`, `referrer_url` |
| User | `user_id` (anonymous + authenticated), `user_email_hash`, `user_company`, `user_role` |
| Campaign | `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` (capture first-touch + last-touch separately) |
| Product | `plan_tier`, `team_size`, `subscription_status` |
| Environment | `device_type`, `browser`, `os`, `app_version` |

Standard properties = consistency. Different events with different property names are a debugging nightmare.

### Step 4 — UTM strategy

Lock the UTM taxonomy up-front:

| Parameter | Allowed values | Example |
|---|---|---|
| `utm_source` | The platform: `linkedin`, `google`, `newsletter`, `direct`, `referral` | `utm_source=linkedin` |
| `utm_medium` | The channel type: `organic_social`, `paid_social`, `email`, `cpc`, `affiliate` | `utm_medium=organic_social` |
| `utm_campaign` | The campaign name (snake_case): `q2_launch_campaign` | `utm_campaign=q2_launch_campaign` |
| `utm_content` | Variant or asset: `hero_button_v2`, `carousel_post_3` | `utm_content=hero_button_v2` |
| `utm_term` | Paid keyword only | `utm_term=gtm_engineer` |

Document this taxonomy in a shared sheet; every marketer reads it before tagging URLs. Drift here destroys attribution.

### Step 5 — Implementation + validation

| Tool | Implementation home | Validation surface |
|---|---|---|
| GA4 | GTM container | GA4 DebugView |
| PostHog | Direct SDK or via GTM | PostHog Live Events |
| Mixpanel | Direct SDK or Segment | Mixpanel Live View |
| Amplitude | Direct SDK or Segment | Amplitude User Look-up |

Validation checklist (run before publishing to production):
- [ ] Each event fires with correct name + all standard properties.
- [ ] Test in tool's preview / debug mode before production deploy.
- [ ] Fire each event once per testing pass (don't loop in a test).
- [ ] Wait 48h after deploy before drawing inferences — conversion data stabilizes after ~48h.

---

## Worked example — ClientCo

**Business questions:**
1. "Are advisers signing up after our LinkedIn campaign?" → `signup_completed` + `utm_source=linkedin`.
2. "Are signed-up advisers activating (connecting their first client account)?" → `client_account_connected` (activation metric).
3. "Are connected advisers using the report generator?" → `report_generated`.
4. "Where do trial-to-paid conversions come from?" → `subscription_upgraded` + first-touch + last-touch UTMs.

**5 events:** `signup_completed`, `client_account_connected`, `report_generated`, `subscription_upgraded`, `subscription_cancelled`.

**Implementation:** GA4 via GTM; PostHog for product-side events. Standard properties enforced on all 5 events.

**Validation:** GTM Preview run; PostHog Live Events confirms; 48-hour wait before first cohort analysis.

---

## Anti-patterns

- ❌ Track 100 events because "we might need them". 90 become noise; the critical 10 get lost in the list.
- ❌ Inconsistent naming (`signupCompleted`, `signup-complete`, `signup_done`). Breaks downstream queries.
- ❌ Ship to production without preview-mode validation. Bugs are 10× more expensive after deploy.
- ❌ Make decisions inside the 48-hour stabilization window.
- ❌ No UTM taxonomy — every marketer invents their own. Attribution destroyed.

---

## Integration with other skills

- **Downstream:** `/ab-testing` consumes the events for sample-size math; `/dashboard` visualizes; `/signup-onboarding-audit` and `/revops` need event data to surface findings; `/referral-program` requires referral_clicked / referral_converted events.
- **Upstream:** `/icp-research` + `/funnel-strategy` define which business questions matter (which drives which events to track).

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/analytics/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/analytics/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice. Tool-agnostic across GA4 / PostHog / Mixpanel / Amplitude.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

