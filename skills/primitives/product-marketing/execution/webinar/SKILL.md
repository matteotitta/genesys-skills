---
name: webinar-brief
version: '1.0'
last_updated: 2026-01-17
author: genesys-growth
description: Plans webinars with logistics, content outline, speaker prep, promotion strategy, and post-event follow-up. Produces
  run-of-show, promotion calendar, registration page copy, and nurture sequences. Triggers on "webinar", "webinar brief",
  "online event", "webinar planning", or "speaker prep". Consumes product-messaging or content-strategy as upstream input
  for topic and audience alignment.
goal: Plans webinars with logistics, content outline, speaker prep, promotion strategy, and post-event follow-up.
outcome: Plans webinars with logistics, content outline, speaker prep, promotion strategy, and post-event follow-up. Produces
  run-of-show, promotion calendar, registration page copy, and nurture sequences. Triggers on "webinar", "webinar brief",
  "online event", "webinar planning", or "speaker prep"....
primitive: product-marketing
sub_primitive: execution
ontology_type: launch-plan
review_gate: 2
inputs:
  required:
  - expert-pov
  - product-messaging
  recommended: []
- type: launch-plan
  feeds_into: []
depends_on:
- expert-pov
- product-messaging
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
effort: medium
---

# Webinar Brief

Comprehensive webinar briefs covering the lifecycle: positioning, content, run-of-show, promotion, follow-up, repurposing.

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`doc-output-structure.md`](../../../../../rules/doc-output-structure.md) — GDoc/Notion structural defaults
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in webinar-brief |
|---|---|---|
| **R1** | Source placement (three layers) | Brief is **client-team review surface**. Cleaned `[VERIFIED:...]` tags live in a collapsed appendix toggle. Registration page + promotion copy (end-customer surfaces) carry NO source tags. |
| **R2** | Single-doc-with-toggles | Multi-asset webinar pack (registration page + promo email + reminder email + run-of-show + follow-up + repurpose plan) ships as **one Notion doc with one toggle per asset** — not 6 separate files. Tessa's Step 6 pattern. |
| **R3** | Product-update tone | When the webinar features a product capability, frame as "we ship X" not "we are thrilled to announce." Promo copy stays even-keeled. |
| **R5** | Blog as voice anchor | When paired with an anchor blog post, the blog's opening line becomes the canonical voice anchor across registration page + promo email + run-of-show opener. Cross-channel voice consistency. |
| **R6** | CTA hierarchy | Promo copy → register-for-webinar primary, blog as fallback. Post-webinar follow-up → trial / demo CTA per Step 6 hierarchy (depends on attendee stage). |
| **R9** | Action-oriented section names | "How to register / What [Webinar] covers / Why attend [Webinar]" — verb-led + entity-named. |

## When to run

Trigger on "plan a webinar", "webinar brief / strategy / promotion plan", "run-of-show", "virtual event brief", "co-marketing webinar", "partner webinar". Skip if the user only needs slides (use presentation tools), demo script (`demo-script`), email sequence (`email-nurture`), or registration page copy (`landing-page-copy`). Full triggers and inputs in the premium reference.

## Inputs

Required: webinar topic, target audience, date/time, speakers. Optional but improve quality: product messaging (alignment), co-marketing partner, past webinar data (benchmarks), bonus content assets, demo environment, promotion budget. If required inputs are missing, ask for topic + date + speakers and confirm whether a live demo is included. Full input table in the premium reference.

## Steps

1. **Validate inputs** — topic, date, speakers, audience, format (live/recorded, demo/no demo). Mark unconfirmed logistics with `[CONFIRM: detail]`.
2. **Define positioning** — topic angle, promise, why now, differentiator. One-sentence positioning statement.
3. **Set goals + metrics** — registrations, attendance rate, engagement, pipeline. Mark targets `[TARGET]` if not benchmarked.
4. **Pick format** — solo / panel / interview / demo+Q&A / workshop. Match duration to format. See the premium reference.
5. **Build content outline** — fit time-realistic sections (default 45-min: 5 intro / 10 context / 20 core / 5 application / 5 Q&A). Templates in the premium reference.
6. **Write speaker prep** — talking points per section, transitions, Q&A anticipation.
7. **Create run-of-show** — T-30 tech check, T-15 speakers online, T-5 green room, 0:00 go live, section timings, close + stop recording. Owners on every row.
8. **Plan engagement moments** — polls, Q&A prompts, resource drops, live reactions, with timing.
9. **Build promotion calendar** — T-3 weeks → T-1 hour. Channels: email (3-4), LinkedIn, Twitter, partner. Owner on every row.
10. **Write promotional copy** — registration page (headline <70ch, sub <120ch, 3-5 bullets, speaker bios, form fields), 3-4 email invites, social posts, partner kit if co-marketing.
11. **Design follow-up sequences** — attendee (Day 0 recording, Day 2 takeaway, Day 5 demo offer) + no-show (Day 0 recording + FOMO).
12. **Plan repurposing** — blog post (Wk1), quote cards (Wk1-2), short clips (Wk1), podcast extract (Wk2).
13. **Define metrics review template** — registrations vs target, attendance rate, watch time, Q&A volume, demo requests, pipeline.
14. **Self-evaluate** — positioning differentiated? content time-realistic? all copy written? no invented speakers/metrics? Fix or flag.
15. **Present at Gate 2** — full brief, run-of-show, promotion calendar, follow-up. Suggest chains: `demo-script`, `email-nurture`, `landing-page-copy`.

Detailed phase-by-phase substeps and checkpoints in the premium reference.

## What good looks like

**Examples**

**Evaluations** — self-eval gate before delivery: positioning clear+differentiated, content fits time, all copy written, no invented speakers/metrics, run-of-show complete with owners, promotion calendar covers full timeline, follow-up sequences both attendee + no-show, repurposing plan defined. Failures → fix or flag with `[CONFIRM]` / `[TARGET]`.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
