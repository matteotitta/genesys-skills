---
name: positioning
version: '2.5'
last_updated: 2026-06-15
author: genesys-growth
description: Develops a positioning strategy with binary strategy selection, primary and secondary anchors, differentiators,
  and a positioning statement. Phase 3 presents the top strategic bets as fully-worked positioning options plus a comparison
  canvas (the scenarios / decisions-to-make step) before collapsing to one committed position; run standalone via --scenarios
  to emit just the options + canvas as a competitor-research deck closer. Produces hero recommendation and one-liners for homepage and campaign use. Triggers on "positioning",
  "category definition", "differentiation", "how do we position", or "strategic foundation for messaging". Requires icp-behavioural
  and competitor-research as upstream inputs. Feeds into product-messaging and landing-page-copy. NOT for messaging libraries
  or taglines — use product-messaging instead.
goal: Develops a positioning strategy with binary strategy selection, primary and secondary anchors, differentiators, and
  a positioning statement.
outcome: 'A positioning strategy: binary strategy, primary/secondary anchors, differentiators, positioning statement, and a hero
  recommendation. In scenarios mode, presents top-N options + a comparison canvas + a recommended pick (decisions to make)
  before collapsing to one committed position.'
primitive: product-marketing
sub_primitive: strategy
ontology_type: positioning
review_gate: 2
inputs:
  required: []
  recommended:
  - icp-behavioural
  - competitor-research
  - win-loss-analysis
- type: positioning-strategy
  feeds_into:
  - product-messaging
  - website-copy
  - sales-enablement
depends_on: []
- website-copy
- product-messaging
- sales-enablement
owned_by_agent: pmm
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /positioning
  - /positioning --scenarios
  natural_language:
  - positioning options
  - positioning scenarios
  - decisions to make on positioning
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: max
---

# B2B positioning strategy

Develop clear, defensible positioning for B2B SaaS products. Synthesizes ICP + competitor + brand context into a binary strategy choice (category vs problem), primary/secondary anchors, defensible differentiators, and a positioning statement that survives the 5-second clarity test.

## When to run

Invoke when the user says:
- "Help me position [product/company]" / "Positioning strategy for [company]"
- "What category should we be in?" / "How do I differentiate from [competitor]?"
- "Our homepage isn't converting" / "Our messaging is confusing"
- "Should we niche down or go broad?" / "How do I explain what we do?"
- "Multi-product positioning help"
- "Give me positioning options / scenarios" / "What are the decisions to make on positioning?" → scenarios mode (N fully-worked bets + canvas + recommended pick)

Do NOT invoke when:
- User wants landing page copy directly → `landing-page-copy`
- User wants full messaging library → `product-messaging` (run after positioning)
- User wants competitor research only → `competitor-research`
- User wants ICP research only → `icp-behavioural`

Workflow sequences:
- Greenfield: `positioning → product-messaging → landing-page-copy`
- Research-informed: `icp-behavioural → competitor-research → positioning → product-messaging`
- Audit fix: `website-pm-score → win-loss-analysis → positioning → landing-page-copy`
- Decisions to make: `competitor-research → positioning --scenarios → (client picks) → product-messaging`

## Inputs

**Required:**
- Company/product name and basic description
- Website URL (accessible, fetchable)

**Recommended (improve quality):**
- `icp-behavioural` output → sharpens persona + problem anchors
- `competitor-research` output → enables competitive alternative mapping
- `win-loss-analysis` output → real decision criteria, objections
- Sales feedback → what's working in conversations
- `website-pm-score` output → clarity gaps to fix

**If inputs missing:** Ask for website URL. Offer to run `website-pm-score` first to assess current clarity. Identify founder type early (customer-focused / technology-focused / competition-focused) — drives the approach sequence.

## Steps

**Mode:** Phase 3 presents the top-N anchor combinations as positioning options + a comparison canvas (the scenarios / decisions-to-make step), then collapses to the option the client picks and runs the validation steps on it. `--scenarios[=N]` emits just the options + canvas standalone (a competitor-research deck closer); default N=3. The single-committed-position outcome and the downstream contract are unchanged once a pick is made. → see the premium reference

1. **Phase 1 — Discovery & current state.** Fetch website (homepage, pricing, about, product). Apply 5-second clarity test on H1+H2. Identify founder type. Extract current category / differentiation / ICP / problem claimed. → see the premium reference
2. **Phase 2 — Anchor & alternative mapping.** Map 6 anchor types (Activity, Product Category, Use Case, Problem, Persona, Competitive Alternative). Map 5 alternative types (Manual/DIY, Legacy incumbent, Direct competitor, Adjacent tool, Status quo). Run Esner Decision Tree (Framework 13) to get a starting hypothesis. Score top combinations on Clarity / Differentiation / Relevance. Classify market maturity (emerging vs mature). → see the premium reference
3. **Phase 3 — Present scenarios, decide, commit.** Take the top-N scored anchor combinations from Step 2.4 (default 3) and expand each into a fully-worked positioning option: concrete hero H1/H2, primary + secondary anchors with type labels, value triad (category / problem / differentiation), secondary angle archetype (Framework 14: Niche / Low-Cost / Premium / Unique Attribute / Lite — max 2), thesis, and risks. Each option must shift its primary anchor or binary strategy — no two options that are the same bet reworded. Assemble the comparison canvas (one column per option; confidence dot per cell mapped to VERIFIED/INFERRED/ESTIMATED/UNAVAILABLE). Mark a recommended pick and name the trade-off each option forces. Present as decisions to make → client picks one. Then collapse to the chosen option: lock its binary strategy (category vs problem), anchors, and 2-3 defensible differentiators (delivery / guarantee / focus / proprietary); determine market focus with TAM math; pick the primary competitive alternative. → see the premium reference + the premium reference
4. **Run clarity ladder.** (On the committed option once a scenario is picked.) Compress positioning to 1 word, 1 phrase, 1 sentence, 1 paragraph. If any level fails, revisit anchor or differentiator selection.
5. **Run guarantee test.** For each differentiator: would you guarantee with money on the line? Verdict Pass / Fail / Partial. Cross-reference proof type per anchor (Framework 15: Activity → Before/After, Use Case → Workflow + Outcome, Category → Comparative, Competitive Alt → Switch/Upgrade).
6. **Map strategic implications.** Document what each decision implies for messaging direction, ICP sharpening, competitive counter-positions. If competitor-research available, include voice calibration. These feed product-messaging, icp-behavioural, tov-guidelines.
7. **Compose output.** Use template at the premium reference (scenarios mode / `--scenarios`: use the premium reference). Anchor-specific positioning statement template:
   - Activity: "We help [persona] [do activity] — replacing [manual process] with [product mechanism]."
   - Use Case: "We help [persona] [accomplish use case] without [key friction] — by [differentiated approach]."
   - Product Category: "We are a [category] that [key differentiator] — unlike [competitive alternative] which [weakness]."
   - Competitive Alternative: "We're a [leader]-alternative that [key upgrade] — for [persona] who [unmet need]."
8. **Channel emphasis guidance.** Same positioning, different facet leads per channel: homepage → primary anchor; thought leadership → Activity/Use Case; comparison pages → Competitive Alternative; sales discovery → Use Case/Activity; case studies → proof type matching primary anchor.
9. **Self-evaluation.** Run completeness, evidence, guardrail checks. Surface improvements. → see the premium reference
10. **Review gate (Level 2).** Present full strategy + decisions. Approve or iterate.
11. **Suggest chain.** If approved: "Want me to run `product-messaging` next?" Tight coupling.

Frameworks reference (15 total): all detailed in the premium reference. Anti-patterns + gotchas: the premium reference. Changelog + MCP integration: the premium reference.

## What good looks like

### Evaluations

- 5-second clarity test passes (H1+H2 answer "which tools" or "which tasks")
- Decision tree hypothesis recorded AND validated against scoring matrix
- Secondary angle archetype selected from Framework 14 (max 2)
- Clarity ladder passes at all 4 levels (word / phrase / sentence / paragraph)
- All differentiators have guarantee test verdicts (Pass / Fail / Partial)
- Proof types align to primary anchor per Framework 15
- No "platform for X" alone, no invented categories, no "AI-powered" as primary differentiator
- ≤3 differentiators (focus discipline)
- Activity anchor used only when no software category exists
- TAM math is realistic (ACV × customers needed) — not hopeful thinking
- Strategic implications mapped for messaging, ICP, competitive (and voice if competitor data available)
- Scenarios mode: exactly N options (default 3, range 2-4), each with a distinct primary anchor or binary strategy (no bet reworded)
- Scenarios mode: every option has a concrete hero H1+H2 (not a placeholder), a thesis, and a risks list
- Scenarios mode: canvas present, one column per option, a confidence dot on every cell mapped to VERIFIED/INFERRED/ESTIMATED/UNAVAILABLE (no all-green canvas)
- Scenarios mode: recommendation framed as decisions to make with the trade-off per option named — not a forced single answer

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
