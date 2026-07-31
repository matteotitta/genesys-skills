---
name: youtube-scripts
version: '2.0'
last_updated: 2026-01-16
author: genesys-growth
description: 'Writes retention-optimized YouTube video scripts with hooks, pattern interrupts, pacing markers, and timing
  cues. Produces full scripts with title options, thumbnail concepts, descriptions, and chapter timestamps. Depends on transcript-analysis
  or thought-leadership for source material. Triggers: "YouTube video", "video script", "video content", "write a script for",
  "repurpose this into video". NOT for short-form social video — use linkedin-content for LinkedIn video posts.'
goal: Writes retention-optimized YouTube video scripts with hooks, pattern interrupts, pacing markers, and timing cues.
outcome: Writes retention-optimized YouTube video scripts with hooks, pattern interrupts, pacing markers, and timing cues.
  Produces full scripts with title options, thumbnail concepts, descriptions, and chapter timestamps. Depends on transcript-analysis
  or thought-leadership for source material....
primitive: social
sub_primitive: youtube
ontology_type: youtube-script
review_gate: 2
inputs:
  required:
  - youtube-strategy
  recommended: []
- type: youtube-script
  feeds_into: []
depends_on:
- youtube-strategy
owned_by_agent: content
mcps_used:
- exa
triggers:
  slash_commands:
  - /youtube-scripts
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# YouTube Scripts

Generate retention-optimized YouTube scripts that treat video content as a lifecycle system, not a one-time event. Every script ships with hook options, timing markers, body framework, retention hooks every 2-3 minutes, single-CTA outro, and supporting assets (3 titles under 60 chars, 2-3 thumbnail concepts, SEO description with timestamps, pinned comment). Research source is Exa per `.claude/rules/exa-protocol.md` — primary tool `web_search_exa` for fact-checking and B-roll references; cite per ontology with `[VERIFIED: exa_search, {url}, accessed YYYY-MM-DD]`; ≥3 sources per major claim, ≥50% verified, no fallback to `WebSearch` without flagging the data gap.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (script body has no inline source tags — researcher-facing notes only; rendered video has no source frames), R3 (script voice operator-direct, never "thrilled to bring you"), R6 (single-CTA outro → sign-up primary for cold, product-action for warm), R9 (verb-led hook + retention beat names).

## When to run

Invoke when the user says: "Write a YouTube script", "Create video script for [topic]", "YouTube video outline", "Script for YouTube about [topic]", "Video content script", "Help me script a video", "YouTube hooks for [topic]", "Video intro script".

Do NOT invoke for:
- LinkedIn video content → `linkedin-content`
- Podcast scripts → handle directly
- Written articles → `aeo-content`
- Presentation slides → `sales-enablement`

## Inputs

**Required:** topic, angle/perspective, target viewer, key message (one sentence).
**Optional (improve quality):** brand voice, existing content, SEO keywords, competitor videos, desired length, proof points (specific results / case studies / data).

**Validation gate before proceeding:**
- [ ] Topic is specific (not just "marketing")
- [ ] Angle provides clear perspective
- [ ] Target viewer is defined
- [ ] Key message is one sentence

If missing, ask for the four required fields before writing anything.

**Client context:** if working on a client project, the client CLAUDE.md auto-loads. Apply voice rules, vocabulary, and messaging anchors from its "Voice & Messaging" section automatically — don't ask the user to re-specify what's already documented.

## Steps

1. **Analyze topic + angle.** Determine content type (educational, case study, contrarian, tutorial). Output: content type identified.
2. **Select hook type.** Choose from the premium reference (contrarian / curiosity-gap / pattern-interrupt / proof-first / problem-agitation / story). Full library: the premium reference.
3. **Select body framework.** Choose from frameworks table (problem-solution-proof / chronological / myth-busting / case-study / framework-reveal / before-after). Full library: the premium reference.
4. **Estimate duration.** Account for hook (8s) + intro (45s) + outro (60s); add body sections sized to depth. Output: target duration.
5. **Generate 2-3 hook options.** Each under 8 seconds read aloud, no filler, creates curiosity gap or pattern interrupt. Label each with hook type + timing estimate. Present for user selection.
6. **Write intro (under 45s).** Authority + Promise + Stakes per the premium reference. Numbered promise creates expectation.
7. **Write body sections.** Apply selected framework. One point per section. Lead with insight, then explain. Prove every claim (data, example, analogy). Signal transitions ("Now that we've covered X, let's talk about Y"). Insert retention hook every 2-3 minutes per the premium reference ("But here's where it gets interesting...", "Here's where most people go wrong...").
8. **Write outro.** Summary under 30s + single clear CTA + specific engagement prompt + open loop teasing next video. CTA patterns: the premium reference.
9. **Add production notes.** Key visuals needed, B-roll suggestions, on-screen text callouts.
10. **Generate 3 title options.** Under 60 characters each, keyword included naturally. Patterns: the premium reference.
11. **Generate 2-3 thumbnail concepts.** Visual description + text overlay + emotion/expression guidance.
12. **Write description.** SEO-optimized opening, timestamp chapters, CTA + links, tags.
13. **Create pinned comment.** Engagement prompt or resource link.
14. **Self-evaluate.** Hook <8s, intro <45s, every claim has proof, no invented stats/testimonials (mark as "Example:" if illustrative or `[PLACEHOLDER]` if missing). Anti-hallucination + signal detection: the premium reference.
15. **Format + present.** Use the premium reference exactly. Review gate 2 (spot check) — actions: [Approve] [Different hook] [Expand].

## What good looks like

### Evaluations

Pre-delivery checklist (full version in the premium reference):

**Script quality** — all sections have timing markers; hook <8s; intro <45s; each body section has one point; every claim has proof; retention hooks every 2-3 minutes.

**Supporting assets** — 3 title options ≤60 chars; 2-3 thumbnail concepts with text overlay; description has timestamps; pinned comment ready.

**Format** — markdown valid; timing markers consistent; production notes included.

**Hook check** — creates curiosity gap or pattern interrupt; ≤8s read aloud; no filler; viewer knows what's at stake.

**Body check** — one point per section; transitions signal movement; no section exceeds 4 minutes without engagement break.

**Outro check** — summary ≤30s; single clear CTA; comment prompt is specific and answerable; open loop creates anticipation.

**Iteration prompts** to offer after delivery (refine / expand / quality) live in the premium reference.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/voice-reviewer` — the content ship gate: voice + brand quality (pm-loop.md).

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
