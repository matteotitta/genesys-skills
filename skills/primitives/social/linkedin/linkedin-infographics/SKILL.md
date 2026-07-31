---
name: linkedin-infographics
version: '1.2'
last_updated: 2026-04-21
author: genesys-growth
description: 'Creates LinkedIn infographics with accompanying text posts. Produces visual framework content, Canva canvas
  configurations, and carousel concepts ready for design handoff. Triggers: "infographic", "carousel", "visual framework",
  "LinkedIn graphic", "visualise this framework". Optionally consumes linkedin-content-guide for ICP alignment and tov-guidelines
  for brand consistency. Feeds into linkedin-weekly-content as visual brief component.'
goal: Creates LinkedIn infographics with accompanying text posts.
outcome: 'Creates LinkedIn infographics with accompanying text posts. Produces visual framework content, Canva canvas configurations,
  and carousel concepts ready for design handoff. Triggers: "infographic", "carousel", "visual framework", "LinkedIn graphic",
  "visualise this framework". Optionally...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 3
inputs:
  required: []
  recommended:
  - linkedin-weekly-content
  - tov-guidelines
  - brand-kit
  - genesys-design
- type: infographic-brief
  feeds_into:
  - linkedin-weekly-content
depends_on:
- genesys-design
- linkedin-weekly-content
owned_by_agent: content
mcps_used: []
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

# LinkedIn Infographics

Visual framework + accompanying text post. Infographic FIRST, text second — text exists to lift up the graphic. Source: Vince Pierri Cohort + Nick Broekema April 2026 coaching.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md), [`design-production.md`](../../../../../rules/design-production.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (infographic visual + caption is end-customer-facing — no source tags), R3 (caption + frame text capability-led), R6 (close = sign-up primary or DM, never engagement-farming), R9 (visual-frame headings verb-led).

## When to run

User says "infographic", "carousel", "visual framework", "LinkedIn graphic", or "visualise this framework". Has a real framework or concept (not invented). Don't run for text-only posts (use `linkedin-content`) or comments (use `linkedin-comment`).

## Inputs

Required: framework/concept to visualize, target ICP, goal (attract buyers / establish authority / drive saves). Optional: visual style, real proof points, contrarian angle, brand guidelines. Verify any metrics provided are real — never invent. If missing → ask for framework + audience + goal. Full validation checklist in the premium reference.

## Steps

1. **Read DESIGN.md** at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md`. Token frontmatter is source of truth for every visual element. If absent → pause and recommend `/brand-kit`. Authority: `.claude/rules/design-production.md`. **For Genesys personal-brand infographics**, the render substrate is the **genesys-design** skill (`.claude/skills/primitives/design/genesys-design/`) — start from its `ui_kits/infographic/index.html` template + `colors_and_type.css` tokens (the CSS binding of Genesys `brand/0626-brand-kit.md`) to output a real branded HTML artifact, not only a Canva brief.
2. **Phase 1 — Framework clarity.** Define core insight ("[Audience] thinks X, but actually Y"), blind spot ("Most [audience] believe [status quo]. This is wrong because [reason]"), outcome ("By doing X, [audience] achieves Y"). Templates in the premium reference.
3. **Phase 2 — Visual design (infographic FIRST).** Pick format from the premium reference (process flow, comparison, matrix, stack flow, nested circles, timeline, diagram, table). We're building **visual frameworks** that show INTERRELATIONSHIPS through shapes — not text in boxes. Shapes communicate without words: concentric circles = hierarchy, Venn = combination, spectrum = range.
4. **Apply Three S's threshold.** Substance (would they print it?) ≥3, Structure (do shapes communicate meaning?) ≥3, Style (will it signal traction?) ≥3. If any ≤2, reconsider. Full rubric in the premium reference.
5. **Apply Nick's April 2026 gates.** (a) Teach HOW not just WHAT — every element has micro-problem + tactical verb + DIY-this-week action. (b) Title leads with "How to…" or temporal transition (`from X to Y` allowed; proper-noun-only titles fail). (c) NO X-not-Y anywhere — sweep every card, band, strip; require 12/12+ rows pass. (d) Foundation strip = positive declarative principle. (e) Bottom strip = save + repost + pipeline CTA (no engagement Qs, no off-ecosystem links). (f) Named framework as watermark, not title.
6. **Build visual brief with token-cited spec.** Quote exact DESIGN.md token values for every color/type/shape (`colors.primary`, `typography.headline-md`, `rounded.lg`, `spacing.lg`). Include token-derived spec table for production tool. One primary color per visual. Two font weights max. Brand's `rounded.*` scale only.
7. **Write in-graphic copy.** Headline 5-8 words. Subhead explains what this teaches. Labels 1-3 words. Annotations brief. 2-3 font sizes max. High contrast. Test mobile readability at 50% zoom.
8. **Phase 3 — Text post (post supports graphic).** Hook structure: hook → misconception bullets → tease named framework → teach → optional CTA.
9. **Hook — use replacement opener (NOT legacy Great Switcheroo X-not-Y).** Pick one: (a) **Temporal transition** — "Most PMM research happens once. Then it sits in a Notion doc until the rebrand." (b) **Cost-of-inaction** — "Three things in your PMM stack are decaying right now: [X], [Y], [Z]." (c) **First-person proof** — "Last quarter I re-ran a client's full positioning, messaging, ICP, and competitor refresh in 4 hours." Reference: `0426-pmm-os-post.md`. Legacy Great Switcheroo formula in the premium reference (historical only).
10. **Misconception bullets (3-5).** "You might think it's about: → [assumption 1] → [assumption 2] → [assumption 3]. It's not." Each bullet 2-5 words. All plausible but wrong.
11. **Tease the named framework.** "The X Rule" / "The Art of X" / "The X Model" / "The X Spectrum". Makes it feel official, creates curiosity.
12. **Teach (3-5 short sentences).** Reference the visual ("See the graphic for the full breakdown"). Don't repeat — drive them to the graphic.
13. **CTA optional.** If used: engaging question, invite experience. Avoid "DM me", "Follow for more", "Like if you agree". Many high-performers have NO CTA.
14. **Self-evaluate.** Visual clear in 3s? Mobile-readable? Dense-to-save + scannable-to-assess? Hook uses approved opener? Named framework feels official? Text drives TO the graphic, doesn't repeat it? Full checklist in the premium reference.
15. **Present at Review Gate 3 (deep review).** Output: infographic brief (with token-cited spec table) + 3 hook options + complete text post. Anti-hallucination: never invent metrics, case studies, or frameworks — mark as `[PLACEHOLDER: need real data]`.

## What good looks like

- **References:**
- **Evaluations:** Three S's all ≥3 (one can be 5 to compensate for a 2). Nick's 6 gates all pass. X-not-Y sweep table 12/12+ rows pass. DESIGN.md token-cited spec table complete. Hook uses approved replacement opener. Visual + text pairing checklist all green.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
