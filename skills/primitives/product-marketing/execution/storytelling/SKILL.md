---
name: storytelling
version: '2.0'
last_updated: 2026-01-16
author: genesys-growth
description: Builds narrative-driven campaigns with emotional arcs and founder stories. Produces story frameworks, campaign
  concepts, and channel-adapted narratives for multi-touchpoint execution. Triggers on "storytelling", "narrative", "brand
  story", "founder story", "emotional campaign", or "story arc". Consumes transcript-analysis and expert-pov as upstream inputs
  for authentic source material. NOT for individual LinkedIn posts — use linkedin-content instead.
goal: Builds narrative-driven campaigns with emotional arcs and founder stories.
outcome: Builds narrative-driven campaigns with emotional arcs and founder stories. Produces story frameworks, campaign concepts,
  and channel-adapted narratives for multi-touchpoint execution. Triggers on "storytelling", "narrative", "brand story", "founder
  story", "emotional campaign", or "story arc"....
primitive: product-marketing
sub_primitive: execution
ontology_type: thought-leadership
review_gate: 2
inputs:
  required:
  - expert-pov
  recommended: []
- type: thought-leadership
  feeds_into:
  - thought-leadership
depends_on:
- expert-pov
- thought-leadership
owned_by_agent: growth
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /storytelling
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# Storytelling

Architect narrative-driven B2B campaigns that create emotional resonance, sustained engagement, and pipeline through systematic story development across anchor, derivative, and distribution layers.

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets (Storytelling/SQCA is Tenet 7)
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`marketing-psychology.md`](../../../../../rules/marketing-psychology.md) — JTBD framing
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in storytelling |
|---|---|---|
| **R1** | Source placement (three layers) | Narrative frameworks ship as **client-team review surfaces**. Cleaned `[VERIFIED:...]` tags in a collapsed appendix. No tags in the narrative body. Source dataset (ICP research, win-loss themes, customer quotes that anchor the metaphor) lives in working doc only. |
| **R3** | Product-update tone | Anchor narratives frame as "[Customer] ships X" not "we are thrilled to launch the [grand metaphor]." Even keynote-level brand campaigns stay even-keeled. The story carries the weight, not the adjectives. |
| **R5** | Blog as voice anchor | When the storytelling campaign has an anchor blog or whitepaper, the blog's opening line becomes the canonical voice anchor across every derivative asset. Cross-channel voice consistency is what makes the campaign read as one story. |
| **R9** | Action-oriented section names | "Set the situation / Name the tension / Land the resolution / Stage the next chapter" — verb-led narrative beats, not status-led ("Background / Problem / Solution / Conclusion"). |

## When to run

Invoke when the user asks for: storytelling/narrative/brand campaign, story arc for [product/launch], hero's journey campaign, brand narrative, campaign metaphor, content campaign, thought leadership campaign, anchor content campaign, multi-week campaign, keynote/executive narrative, customer transformation story.

**Do NOT invoke for:** single blog post (use `aeo-content`), landing page copy (use `landing-page-copy`), email sequences without narrative arc (use `email-nurture`), social posts without campaign strategy (use `linkedin-content`).

## Inputs

**Required:**
| Input | Description | Source |
|-------|-------------|--------|
| Product/messaging context | 3+ capabilities, 3+ differentiators | `messaging` skill output |
| ICP research | Champion persona with pain points | `icp-behavioural` output |
| TOV guidelines | Voice attributes defined | `tov-guidelines` or client docs |

**Optional (improves quality):** competitor research (narrative gap), campaign objectives (focus arc), timeline constraints (calendar calibration), budget context (asset scope).

**Validation gate:** if any required input missing, ask user to provide or offer to run upstream skill first.

**Client context:** if working on a client project, the client CLAUDE.md is auto-loaded — apply Voice & Messaging rules automatically; don't re-ask.

## Steps

### Phase 1 — Insight mining

1. **Extract narrative tension.** Use the four-question framework in the premium reference (status quo, urgency, why current fails, transformation promise) → Output: narrative tension framework.
2. **Map emotional payload.** Pain point → underlying emotion → story beat (table in the premium reference) → Output: emotional journey map.
3. **Identify competitive narrative gaps.** Competitor / their story / what they miss / your angle → Output: competitive narrative positioning.
4. **Compile narrative foundation brief.** Use template in the premium reference → Output: brief covering core tension, emotional journey, transformation promise, competitive angle, voice alignment.

**Checkpoint:** narrative tension identified, emotional journey mapped, competitive angle defined, foundation brief complete.

### Phase 2 — Narrative development

5. **Select story arc.** Match campaign goal → arc → duration using table in the premium reference (6 primary literary arcs + 4 B2B-specific). Document rationale.
6. **Map arc stages to content beats.** For Hero's Journey use the 12-stage table in the premium reference. For other arcs, build equivalent stage→beat→focus mapping.
7. **Create before/after archetypes.** Use template in the premium reference (visual metaphor, behaviors, tools, frustrations/feelings, beliefs, outcome). Names must be evocative nouns.
8. **Build metaphor system.** Select pop culture references for target demographic, map to story beats. Validate per the premium reference selection rule (age/role/geography fit).
9. **Define narrative altitude (executive audiences only).** Use 4-altitude table in the premium reference (30k/15k/5k/ground). Produce altitude-specific narrative versions for multi-stakeholder buying committees.

**Checkpoint:** arc selected and mapped, archetypes documented, metaphors validated, altitude defined if applicable.

### Phase 3 — Content orchestration

10. **Build campaign timeline.** Use the premium reference 6-week Hero's Journey template (or proportional version for other arcs). Map weekly anchor + support assets.
11. **Generate anchor content briefs.** Use brief template in the premium reference (title, thesis, story beat, key messages, proof points, CTA) — one per anchor.
12. **Generate derivative content briefs.** Social posts, email sequences, memes — formats per the premium reference.
13. **Define distribution plan.** Channel × content type × frequency × goal matrix per the premium reference.
14. **Define pipeline metrics.** Awareness → engagement → conversion → pipeline. Targets from client inputs only or marked "Suggested: X" — never invent.

**Checkpoint:** timeline complete, all briefs generated, distribution and metrics defined.

### Self-evaluation + review gate

15. **Run self-evaluation and quality checks per the premium reference** (anti-hallucination guardrails, narrative/content/completeness checklists). Mark unconfirmed details with `[PLACEHOLDER: description]`. Present full campaign at **Gate 2 (standard review)** — actions: approve, adjust arc, expand scope.

## What good looks like

**Examples:**
- `examples/octave-prompt-swamp-campaign.md` — Hero's Journey full campaign for Octave (prompt swamp narrative)

**Evaluations (golden output traits):**
- Transformation stated as archetype shift (not generic outcome)
- Emotional journey specific, not generic
- Competitive angle positions against category or status quo, not against named competitor
- Tension is quantified (e.g., "60% of time")
- Archetype names are evocative nouns; visual metaphors are concrete and visible
- Behaviors observable, beliefs in first-person quotes, outcome concrete
- Metaphors verified against demographic
- All metrics either client-sourced or marked "Suggested:"

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
