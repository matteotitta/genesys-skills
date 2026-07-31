---
name: in-app-popups
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Designs in-product popups and overlays (exit-intent, scroll-trigger, time-delay, click-trigger) with timing hierarchy, value-first copy, easy-dismiss UX, segmentation rules, and mobile-specific patterns. References conversion benchmarks (exit-intent 3–10%, click-triggered 10%+, 2–5% email capture typical). Triggered by "popups", "modals", "overlays", "in-app prompts", "exit-intent popup", "newsletter signup popup". NOT for paywalls — separate skill at /paywalls (deferred — patterns folded into /pricing-strategy).
goal: Design in-product popups and overlays that capture conversions without harming UX.
outcome: Produces (1) popup type + trigger strategy, (2) targeting rules + segmentation, (3) copy structure + design specs, (4) A/B test hypotheses, (5) mobile-specific design patterns.
primitive: website
sub_primitive: execution
ontology_type: landing-page-copy
review_gate: 2
inputs:
  required: []
  recommended:
  - product-messaging
  - icp-behavioural
  - signup-onboarding-audit
- type: landing-page-copy
  feeds_into:
  - landing-page-copy
depends_on: []
- ab-testing
owned_by_agent: growth
mcps_used:
- exa
triggers:
  slash_commands:
  - /in-app-popups
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /in-app-popups — overlay design that respects users

Design popups, modals, and overlay elements that convert without burning UX trust. The wrong popup tanks NPS; the right popup is one of the cheapest conversion uplifts available.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`marketing-psychology.md`](../../../../../rules/marketing-psychology.md)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in in-app-popups |
|---|---|---|
| **R1** | Source placement | Popup copy is **end-customer-facing**. **No sources inline.** Design rationale lives in working doc only. |
| **R3** | Product-update tone | Popup framing — "[Feature] just shipped" not "we are thrilled to announce." Even on launch-driven popups. |
| **R6** | CTA hierarchy | Warm-base (in-product, post-login) → product-action CTA primary ("open [Feature]"). Cold-base (pre-login, marketing-site) → sign-up primary. Never both as primary. |
| **R9** | Action-oriented section names | Popup body verb-led — "Open Reporting" beats "Reporting available." |

---

## Step 1 — Timing hierarchy

Order triggers by quality (highest engagement signal first):

| Trigger | Typical conversion | Why it works |
|---|---|---|
| Exit-intent (mouse heads to close-tab on desktop) | 3–10% | Captures abandoning visitor; "last chance" frame |
| Click-triggered (user explicitly clicks "Get the guide" button) | 10%+ | Highest intent — user opted into the conversation |
| Scroll-based (fires at 25–50% scroll depth) | 2–5% | Engagement signal — they're reading |
| Time-based (after 30–60 sec) | 1–3% | Weakest — assumes any visitor wants the popup |

**Sharp rules:**
- Never fire on page load. The user hasn't seen anything yet.
- Avoid "Show after 5 seconds" — too soon. 30–60 sec minimum if time-based.
- Click-triggered should be the default for high-value offers (lead magnets, demo asks).

---

## Step 2 — Value-first design

The popup must justify the interruption. Test:

- **Headline benefit > headline ask.** "Get the cold-email template that books 12% reply rate" beats "Sign up for our newsletter".
- **Specific > vague.** "12% reply rate" beats "improve your reply rate".
- **One CTA** with optional polite decline ("No thanks — I'm not running outbound right now"). Never just an ❌.

---

## Step 3 — Respect-based UX

- **Easy dismissal.** Visible close button (top-right, ≥ 24px), ESC key, click-outside-to-close. All three.
- **Preference memory.** Once dismissed, don't show again for 30 days (longer for repeated dismissals).
- **Frequency cap.** Max 1 popup per session, 1 per page-type per 7 days.
- **Mobile-specific.** Never full-screen overlay on mobile. Use bottom slide-up (sticky bar 25% screen height) or full-width centered modal that respects viewport. Full-screen mobile popups trigger Google's intrusive-interstitial penalty.

---

## Step 4 — Segmentation strategy

Different popups for different visitor states:

| Segment | Popup |
|---|---|
| New visitor, first 30 sec | None (let them read) |
| New visitor, scroll 50%+ | Newsletter signup with value prop |
| Returning visitor, no signup | Lead magnet (demo, template, calculator) |
| Returning visitor, recent purchase | Upgrade / referral prompt |
| Exit-intent on pricing page | Discount or scheduling demo offer |
| Exit-intent on blog post | Newsletter signup matched to post topic |

**Sharp rule:** never show the same popup to a returning visitor who already dismissed. Reads as nag; tanks trust.

---

## Step 5 — Copy formula

```
Headline: Specific benefit (5-9 words)
Subhead: Proof or specificity (1 sentence)
Primary CTA: Action verb + outcome
Secondary: Polite decline matched to user state ("No thanks, I [user state]")

Example:
Headline: Get the cold-email template that books 12% replies
Subhead: 1-page template, 30 sec to skim, used by 200+ founders.
CTA: Send it to my inbox
Decline: No thanks, I'm not running outbound right now
```

---

## Step 6 — A/B hypotheses

Test in priority order:
1. Trigger type (exit-intent vs. scroll vs. click — which segment converts highest).
2. Headline (benefit specificity).
3. CTA copy.
4. Form length (email-only vs. email + 1 field).
5. Frequency cap (1/session vs. 1/visit).

Hand off formatted hypotheses to `/ab-testing`.

---

## Worked example — ClientCo in-product activation

**Current state:** Single time-delay popup ("Want a demo?") fires at 60 sec on every page for every user.

**Findings:**
- No segmentation — fires same popup to returning vs. new users.
- Time-based trigger — low intent.
- Vague headline — no value-prop.
- Mobile: full-screen overlay (intrusive-interstitial flag).

**Redesign:**
- New visitor on pricing page → exit-intent → "Get the ROI calculator before you leave".
- Returning visitor, ≥ 3 sessions → click-triggered "Book a demo with Baris" CTA on pricing.
- Mobile: bottom slide-up sticky bar with the same offer; full-screen overlays removed entirely.

---

## Anti-patterns

- ❌ Fire on page load. User hasn't engaged yet.
- ❌ Hidden close button.
- ❌ Full-screen mobile overlays (Google penalty risk).
- ❌ Same popup for every visitor state.
- ❌ Guilt-trip declines ("No thanks, I don't care about my business").
- ❌ Stack multiple popups (popup A closes → popup B opens).
- ❌ Re-show a dismissed popup within the same session.

---

## Integration with other skills

- **Upstream:** `/signup-onboarding-audit` may surface in-product friction that popups address; `/icp-behavioural` defines visitor states for segmentation.
- **Downstream:** `/ab-testing` runs the optimization tests; `/lifecycle-marketing` continues the conversation post-popup-conversion.

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/popups/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/popups/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice. Renamed to `in-app-popups` per user direction.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

