---
name: onboarding-video-script
version: '1.0'
last_updated: 2026-05-06
author: genesys-growth
description: Writes product onboarding video scripts that founders or PMs read aloud to record. Pulls from a product website
  URL plus a transcript (founder walkthrough, customer call, or PM screen-share) and produces a two-column talk-track plus
  click-path script that walks a brand-new user from first touch to a single aha moment with a habit-forming CTA. Triggers
  on "onboarding video script", "founder walkthrough script", "product onboarding video", "aha moment video", "first-run
  video script". Consumes locked positioning (anchor) and a transcript routed through transcript-analysis. NOT for marketing
  channel videos (use youtube-scripts), sales demos (use demo-script), in-product UI copy, or rendered onboarding MP4
  compositions (use onboarding-video for stills-driven onboarding renders, product-ui-frames for generic brand video).
goal: Write a founder/PM-recorded onboarding video script that lands a new user at one aha moment and a habit-forming CTA.
outcome: A two-column talk-track + click-path script with timing markers, production notes, and a single habit CTA. Founder
  records the video; the script unblocks recording without inventing features and matches positioning anchors.
primitive: product-marketing
sub_primitive: execution
ontology_type: onboarding-video-script
review_gate: 2
inputs:
  required:
  - transcript-analysis
  - positioning
  recommended:
  - company-context
  - product-messaging
  - icp-behavioural
  - tov-guidelines
- type: onboarding-video-script
  feeds_into: []
depends_on:
- transcript-analysis
- positioning
owned_by_agent: pmm
mcps_used:
- exa
- firecrawl
- notion
triggers:
  slash_commands:
  - /onboarding-video-script
  natural_language:
  - "onboarding video script"
  - "founder walkthrough script"
  - "product onboarding video"
  - "aha moment video"
  - "first-run video script"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# Onboarding Video Script

Writes the script a founder or PM reads aloud to record a product onboarding video. The video's job is to walk a brand-new user from first touch to **one** aha moment and end with a habit-forming CTA that attaches the product action to an existing daily trigger ("tomorrow morning, do X").

Output is a two-column markdown deliverable — talk track on the left, on-screen action / click path on the right, with timing markers and production notes. Modeled on the demo-script two-column pattern; differs by being founder-owned (not sales-owned), single-aha (not feature-tour), and habit-CTA-terminated (not "next steps").

The body of this file holds decision-grade context (when to invoke, inputs, duration tables, the single-aha and TTV rules, anti-hallucination guardrails, integration). Step-by-step process, two-column output template, the aha-moment framework, founder narration craft library, duration templates, quality gates, and the feedback loop live in the premium reference.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in onboarding-video-script |
|---|---|---|
| **R1** | Source placement (three layers) | Script is **internal-reference** (founder reads it aloud) BUT the video output is **end-customer-facing**. Talk-track column has no source attribution. Production-notes column carries internal cites for QA only. The video itself never carries a "Sources:" frame. |
| **R3** | Product-update tone | Founder narration frames as "we shipped X to fix Y" not "we are thrilled to introduce." Even on launch-day videos. Operator-direct founder voice. |
| **R6** | CTA hierarchy | The closing habit-CTA names the product-action tied to a daily trigger ("tomorrow morning, do X") — NOT a sign-up CTA (viewer already signed up to see the onboarding video). Per Step 6 warm-base = product-action rule. |
| **R9** | Action-oriented section names | "Hook / Land the aha / Habit-trigger close" — verb-led across script beats. |

---

## Claude Code triggers

**Invoke this skill when user says:**
- "Onboarding video script"
- "Founder walkthrough script"
- "Product onboarding video"
- "Aha moment video"
- "First-run video script"
- "Loom script for onboarding"
- "Activation video script"
- "Walkthrough script for [product]"

**Do NOT invoke when:**
- User wants marketing channel video → `/youtube-scripts`
- User wants sales demo → `/demo-script`
- User wants written onboarding doc → handle directly
- User wants in-product tooltip / modal copy → out of catalog (product UX)
- User wants emails around the video → `/email-nurture`
- User wants a rendered onboarding MP4 (animated UI pieces, motion graphics) → `/onboarding-video` (sibling — the render counterpart to this script skill)
- User wants a generic brand MP4 (not onboarding, no stills) → `/product-ui-frames`

---

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Product URL** | Live product website / pricing / feature pages | User-provided |
| **Transcript** | Founder walkthrough, customer call, or PM screen-share talk-through, processed through `transcript-analysis` | `transcript-analysis` upstream skill |
| **Locked positioning** | Primary anchor + differentiator the script must reflect | `positioning` skill output (status: locked) |
| **Target duration** | One of: 60s teaser / 3min onboarding (default) / 5min walkthrough / 10min full tour | User-specified |
| **Target persona** | One persona — multi-persona requires multi-script | User or `icp-behavioural` |

### Recommended (improve quality)

| Input | How it helps |
|-------|--------------|
| `product-messaging` | Aligns talk-track with locked messaging library |
| `icp-behavioural` | Persona-specific aha moment + pain points |
| `tov-guidelines` | Voice rules — conversational, founder-first-person |
| `company-context` | Firmographics + traction (used sparingly in talk-track) |

### Validation gate before proceeding

- [ ] Product URL is live and reachable
- [ ] Transcript exists (or `transcript-analysis` has run)
- [ ] Positioning is **locked** (not draft / review)
- [ ] Target duration chosen
- [ ] Target persona chosen (one)

If any required input is missing or positioning is not locked, ask before generating. Do NOT write a script against draft positioning — the script will be invalidated when positioning locks.

---

## Process at a glance

| Phase | Purpose | Output |
|-------|---------|--------|
| 1. Discover | Pull product context from URL + transcript; identify candidate ahas | Aha candidate list (3–5 options) |
| 2. Map aha | Pick **one** aha; map persona pain → TTV → activation metric → habit CTA | Aha + Hook-model decision (1 page) |
| 3. Script | Write hook → setup → aha walkthrough → reinforce → habit CTA in two-column format | Draft script |
| 4. Polish | Apply founder-narration craft rules; chunk for re-recordability; add B-roll cues | Polished script + production notes |

Full step-by-step (with checkpoints, flowchart, review gate) in the premium reference.

---

## Duration templates (decision-grade)

| Duration | Use case | Hook | Aha by | Total sections |
|----------|----------|------|--------|----------------|
| **60s teaser** | Public landing page video, ad pre-roll | 0:00–0:05 | 0:30 | Hook → Aha → CTA |
| **3min onboarding** *(default)* | First-run experience, post-signup welcome | 0:00–0:10 | 1:30 | Hook → Setup → Aha → Reinforce → Habit CTA |
| **5min walkthrough** | Mid-funnel conversion video, product page | 0:00–0:15 | 2:30 | Hook → Setup → Aha → 2nd use case → Reinforce → Habit CTA |
| **10min full tour** | Deep walkthrough for evaluators, sales-assist | 0:00–0:20 | 4:00 | Hook → Setup → Aha → 3 use cases → Reinforce → Habit CTA |

Full templates with section-by-section talk-track/click-path/timing in the premium reference.

---

## Aha moment framework (decision-grade)

The differentiator vs. generic video script generators. Six rules govern the script:

1. **One aha rule** — pick a single aha moment. Most onboarding videos try 4–5 features and miss all of them.
2. **TTV ceiling** — aha lands at or before 50% of total duration (40% for 10-min tour).
3. **Hook model** — every script must hit Eyal's four steps: trigger → action → variable reward → investment.
4. **Activation metric mapping** — the script drives one specific in-product action (the leading indicator of retention).
5. **Persona-specific aha** — same product, different aha per persona. Multi-persona = multi-script.
6. **Habit ladder CTA** — the CTA attaches the product action to an existing daily trigger ("tomorrow at standup, do X").

Full framework with worked decision tables in the premium reference.

---

## Founder narration rules (decision-grade)

Seven hard rules that distinguish founder-recorded onboarding videos from polished YouTube content:

1. **Conversational** — read-aloud test: "would I say this in a Zoom call?" No "leverage", no "synergize", no marketing-deck cadence.
2. **Re-recordable** — chunk script into 30–60s segments with clear cut points so founders can re-record sections without redoing the whole video.
3. **Screen-paced** — talk-track timing matches click-path. A 4-second click gets 4 seconds of talk track.
4. **Single-take feasibility** — minimize cuts. Founders aren't editors; script for one take per segment.
5. **First-person founder voice** — "I built this because…" not "Our platform offers…". Personal anchors trust faster than corporate.
6. **Length discipline** — if the script overruns, cut features, never the aha.
7. **One CTA** — single habit-forming action. Not three CTAs, not "and follow us on LinkedIn".

Full craft library with anti-examples in the premium reference.

---

## Anti-hallucination guardrails

1. **Don't invent features.** Only script features verifiable in the URL or transcript. Mark unconfirmed click paths with `[CONFIRM: click path]`.
2. **Don't invent metrics.** No "saves you 10 hours" claims in talk-track unless the founder gave you the number with a source.
3. **Don't fake testimonials.** No "users tell us…" without a real quote in the transcript.
4. **Persona-specific voice, not generic-buyer.** Adapt language to the actual persona; flag generic phrasing.
5. **Time-realistic.** Verify timing aloud — read the script with a stopwatch; if it overruns, trim before delivering.
6. **No invented aha.** If the transcript doesn't surface a clear aha, ask the founder before assuming one. Confirmation > confabulation.

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **positioning** | Provides input (required) | Anchor + differentiator the script reflects |
| **transcript-analysis** | Provides input (required) | Structured aha candidates, quotes, click-path hints |
| **product-messaging** | Provides input (recommended) | Talk-track aligns with locked messaging library |
| **icp-behavioural** | Provides input (recommended) | Persona pain → aha mapping |
| **tov-guidelines** | Provides input (recommended) | Voice rules (founder first-person) |
| **case-study** | Sibling | Different artifact: customer story vs. founder walkthrough |
| **storytelling** | Sibling | Narrative arc craft library — pull patterns when needed |
| **webinar** | Sibling | Different format: longer, multi-speaker |
| **demo-script** | Related | Sales walkthrough vs. user onboarding (different audience, different goal) |
| **email-nurture** | Downstream | Emails before/after the video — script feeds into the nurture sequence |
| **onboarding-video** | Sibling (script ↔ render pair) | Same flow, different artifact: this skill writes the founder-read script; `/onboarding-video` renders the animated UI variant. Often produced together — script first, then render. |
| **product-ui-frames** | Related | Generic brand-bound MP4 engine. `/onboarding-video` inherits from it; this script skill is a separate lane (script vs. render) |

---

## MCP data integration

**Level:** 2 — PM Execution

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Product URL (web)** | Pricing / feature / docs pages for grounding click paths | Exa `web_fetch_exa` per `.claude/rules/exa-protocol.md` | When transcript context is thin |
| **Product URL (clean extract)** | Full structured page content for dense pricing / feature tables | `mcp__firecrawl__firecrawl_scrape` | When Exa fetch returns insufficient detail |
| **Transcript** | Aha candidates, quotes, persona pain markers | `transcript-analysis` upstream skill | Always |

**Fallback (no MCP):** Founder-provided narration outline + manual product walkthrough notes.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

