---
name: thought-leadership
version: '1.0'
last_updated: 2026-01-16
author: Genesys Growth
description: 'Creates long-form thought leadership articles and whitepapers through a 3-phase human-in-the-loop process (outline,
  draft, polish). Produces publication-ready articles with contrarian angles, evidence-backed arguments, and TOV-matched prose.
  Depends on expert-pov and transcript-analysis for source material. Triggers: "thought leadership article", "long-form content",
  "write a whitepaper", "write an article about X", "expand this insight into a piece". Feeds into newsletter editions and
  linkedin-expert-posts as anchor content. NOT for short-form social posts — use linkedin-content instead. NOT for rendering
  an existing whitepaper or study as an arXiv-style paper PDF — this skill writes the whitepaper, /technical-paper-writer
  renders it.'
goal: Creates long-form thought leadership articles and whitepapers through a 3-phase human-in-the-loop process (outline,
  draft, polish).
outcome: Creates long-form thought leadership articles and whitepapers through a 3-phase human-in-the-loop process (outline,
  draft, polish). Produces publication-ready articles with contrarian angles, evidence-backed arguments, and TOV-matched prose.
  Depends on expert-pov and transcript-analysis for...
primitive: content
sub_primitive: execution
ontology_type: thought-leadership
review_gate: 2
inputs:
  required:
  - expert-pov
  - content-strategy
  recommended: []
- type: thought-leadership
  feeds_into: []
depends_on:
- expert-pov
- content-strategy
- technical-paper-writer
owned_by_agent: content
mcps_used:
- exa
- gdrive
- notion
triggers:
  slash_commands:
  - /thought-leadership
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Thought Leadership

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets (Storytelling/SQCA is Tenet 7)
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md) — the 12 patterns thought-leadership hooks can't carry
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in thought-leadership |
|---|---|---|
| **R1** | Source placement (three layers) | Published essay is **end-customer-facing**. **No `[VERIFIED:...]` tags inline.** Citations convert to inline links inside the prose at publish time (e.g., "Tan's [post on Series A spread](url)"). Working draft carries internal `[VERIFIED:...]` for the phase-1 → phase-2 review gate, stripped before phase 3 polish. |
| **R3** | Product-update tone | When the essay references the author's product, frame as "we ship X" not "we are thrilled to announce." The contrarian angle does the work — adjectives don't. |
| **R5** | Blog as voice anchor | Long-form essay IS the voice anchor. Downstream LinkedIn / newsletter / podcast assets paraphrase forward from the essay's opening line — that's where R5 originates upstream. |
| **R9** | Action-oriented section names | Section headers state the claim (not "Background / Conclusion"). "Why the spread game is broken" beats "The Series A problem." Claim-led, not category-led. |

## When to run

Long-form articles, essays, whitepapers, or guest posts where the user has a contrarian or non-obvious angle they want to publish. Three human-approval gates (Phase 1 pyramid, Phase 2 prose, Phase 3 polish). Skip for LinkedIn posts (`linkedin-content`), newsletter copy, or website copy. Triggers, anti-triggers, and pre-flight checklist → the premium reference.

## Inputs

| Input | Status | Source |
|-------|--------|--------|
| Topic / core insight | Required | User — must be specific and contrarian |
| Target audience | Required | ICP research or user-specified |
| Core argument | Required | User or collaboratively developed |
| ICP research | Recommended | `clients/[client]/icp-behavioural.md` |
| Product messaging | Recommended | `clients/[client]/product-messaging.md` |
| Content strategy | Recommended | Pillars + roadmap |
| Competitor positions | Recommended | Identifies white space |
| Source material, word count, publication context | Optional | LinkedIn 800-1500 / blog 1500-2500 / guest 2000-3500 |

Client CLAUDE.md is auto-loaded — apply its voice/messaging anchors. Full input matrix and pre-flight checklist in the premium reference.

## Steps

1. **Validate inputs** — topic specific, audience known, contrarian angle present, user has time for 3 review cycles.
2. **Phase 1.1 — Clarify core insight.** Ask: "What's the one thing you want the reader to believe after reading this that they didn't believe before?"
3. **Phase 1.2 — Identify audience starting point.** Current belief, gap to governing thought, anticipated objections.
4. **Phase 1.3 — Build the pyramid.** Governing Thought → 2-4 Key Line Arguments → Supporting Evidence per key line. Use the template in the premium reference. Pyramid theory + MECE deep-dive in the premium reference.
5. **Phase 1.4 — Test structure.** MECE check (no overlap, fully supports governing thought) + "so what?" test on every level.
6. **Phase 1 deliverable + STOP.** Wrap in the Phase 1 checkpoint format. Wait for explicit "Approved — proceed to Phase 2" before continuing.
7. **Phase 2.1 — Map pyramid to prose sections.** Governing thought → opening, key lines → sections, objections → inline or dedicated, "so what?" → closing.
8. **Phase 2.2 — Write opening.** Hook → Context → Thesis → optional Roadmap. **Phase 2.3 — Expand each section:** Headline → Lead → Evidence → Transition. **Phase 2.4 — Write closing:** Restate → Synthesize → Implications → CTA.
9. **Phase 2 deliverable + STOP.** Three title options + full prose outline. Wrap in Phase 2 checkpoint format. Wait for "Approved — proceed to Phase 3".
10. **Phase 3.1 — Apply TOV.** Operator authority, prescriptive confidence, framework-driven clarity, candid partnership, specificity over superlatives, conversational warmth. Em dashes with spaces, sentence case headlines, numerals, banned-word check. Quick checklist → the premium reference.
11. **Phase 3.2 — ICP guardrails.** Would target ICP care? Right sophistication? Would they share this with their team?
12. **Phase 3.3 — Anti-hallucination guardrails.** No invented client names/metrics/quotes. Mark missing data as `[Data point needed]`. Verify proof points or flag as `[Example — verify before publishing]`.
13. **Phase 3.4 — 100 Posts Test.** "If I published 100 posts like this, would the aggregate feel authentic to my voice and brand?" Plus final read-aloud check.
14. **Phase 3 deliverable + final STOP.** Wrap as `THOUGHT LEADERSHIP FINAL — PHASE 3` with quality report and items-for-review. Wait for "Approved — ready to publish".
15. **Push to chains.** After approval, offer LinkedIn teaser, standalone quote pulls, email intro, or newsletter summary. Suggest `/linkedin-content`, `/email-nurture`, or update `/content-strategy` plan.

Format guidelines per platform → the premium reference. Phase output wrappers, checkpoint dialogues, MECE details, Exa research substrate, and full auto-update protocol → the premium reference.

## What good looks like

**Examples** — `examples/worked-example-gtm-engineer.md` (full 3-phase walkthrough), `examples/top-performing-examples.md` (validated patterns).

**Evaluations** — Governing thought is contrarian and specific (not commodity wisdom). Key lines are MECE. Every claim has verified source or `[Example — verify]` flag. No banned words: solutions, leverage, synergy, scalable, best-in-class, game-changer, innovative, cutting-edge, very, really, basically, just. Three checkpoints honoured (no skipping ahead). Passes 100 Posts Test. Cites `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` for any external claim per `.claude/rules/ontology.md` and `.claude/rules/exa-protocol.md`.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/voice-reviewer` — the content ship gate: voice + brand quality (pm-loop.md).

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
