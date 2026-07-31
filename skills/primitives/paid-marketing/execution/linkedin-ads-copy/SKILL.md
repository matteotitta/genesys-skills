---
name: linkedin-ads-copy
version: '1.1'
last_updated: 2026-05-01
author: genesys-growth
description: 'Creates LinkedIn Ads copy across all ad formats — Sponsored Content, InMail, Video, Carousel, Document, and
  Thought Leader Ads — structured around full-funnel architecture: awareness, consideration, and conversion. Produces ad copy
  variants per format with headlines, intro text, CTAs, and character-count compliance. Depends on paid-campaign-strategy
  as required input. Feeds into ad-creative-brief for visual production. Triggered by "LinkedIn Ads copy", "sponsored content",
  "InMail ads", "LinkedIn campaign", "thought leader ads", "conversation ads", or "lead gen form ads". NOT for Google search
  ads — use /google-ads-copy instead. NOT for strategy — use /paid-campaign-strategy first.'
goal: 'Creates LinkedIn Ads copy across all ad formats — Sponsored Content, InMail, Video, Carousel, Document, and Thought
  Leader Ads — structured around full-funnel architecture: awareness, consideration, a'
outcome: 'Creates LinkedIn Ads copy across all ad formats — Sponsored Content, InMail, Video, Carousel, Document, and Thought
  Leader Ads — structured around full-funnel architecture: awareness, consideration, and conversion. Produces ad copy variants
  per format with headlines, intro text, CTAs, and...'
primitive: paid-marketing
sub_primitive: execution
ontology_type: linkedin-post
review_gate: 2
inputs:
  required:
  - paid-campaign-strategy
  recommended:
  - product-messaging
  - icp-behavioural
  - competitor-research
- type: linkedin-ads-copy
  feeds_into:
  - ad-creative-brief
depends_on:
- paid-campaign-strategy
- ad-creative-brief
owned_by_agent: content
mcps_used: []
- gdrive
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

# LinkedIn Ads Copy

Generate LinkedIn Ads copy for B2B SaaS campaigns across all ad formats. Structured around full-funnel campaign architecture (awareness > consideration > conversion). Enforces LinkedIn character limits per format. Outputs as structured markdown tables ready for LinkedIn Campaign Manager.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in linkedin-ads-copy |
|---|---|---|
| **R1** | Source placement | Ad copy is **end-customer-facing**. No source tags. |
| **R3** | Product-update tone | Intro text + headlines frame as "[Product] does X" not "thrilled to introduce." |
| **R5** | Blog as voice anchor | Anchor blog opener = intro text first line across funnel stages. |
| **R6** | CTA hierarchy | Awareness → blog/learn-more. Consideration → sign-up + blog as fallback. Conversion → trial primary. |
| **R9** | Action-oriented section names | Intro / Headline / Description verb-led, no "About us" copy patterns. |

---

## Triggers

Run this skill when:

- Paid-campaign-strategy is locked and the next step is generating ad-set copy
- A client wants TOFU/MOFU/BOFU LinkedIn coverage built out across formats
- Existing LinkedIn campaigns need refreshed copy (e.g., low CTR, format expansion)
- ABM targeting needs accompanying ad copy with variant breakdowns

Do NOT run when:

- Strategy isn't locked — run `/paid-campaign-strategy` first
- Target channel is Google search/display — use `/google-ads-copy`
- The ask is a single LinkedIn organic post — use `/linkedin-content` or `/linkedin-hooks`

---

## The Iron Law — voice-locked

**EVERY CHARACTER COUNT MUST BE VERIFIED.**

LinkedIn will truncate or reject copy that exceeds format limits. There is no "close enough." Count every character including spaces, punctuation, and emojis.

**No exceptions:**

- "It's only 1 character over" → LinkedIn truncates it. Trim it.
- "The visible limit is 150 but max is 600" → Users see 150. Write for 150. Use 600 only when expanding is worth it.
- "Carousel headline limit is 70 chars" → It's 45 with a link. Know which format you're writing for.
- "We can just shorten the CTA" → Conversation Ad CTAs are ≤20 chars. Spotlight CTAs are ≤18 chars. Different formats, different limits.

---

## Funnel-stage discipline — voice-locked

| Stage | Voice | What's allowed | What's banned |
|-------|-------|----------------|---------------|
| TOFU | Educational, not sales-y | Insight hooks, soft CTAs, thought leader format | Product names in intro, hard sell, demo CTAs |
| MOFU | Product education | Feature spotlights, before/after, named proof | Generic awareness copy, missing CTA |
| BOFU | Conversion drivers | Single direct CTA, de-risking language, social proof | Multiple CTAs, soft hooks, vague offer |
| Retargeting | Closing language | Urgency, social proof, direct CTA | New-to-brand intros (audience already engaged) |

Hooks must be genuinely distinct across the three variants — *different angles* (stat / contrarian / question / proof / before-after), not synonym swaps.

---

## Targeting invariants — voice-locked

- **Skills-only > title+skills > title-AND-skills.** Title AND skill in separate facet groups shrinks the audience 60-80% silently. Default to skills + seniority + function in the same group for ABM.
- **Audience-size bands match funnel stage.** TOFU 30-150K, MOFU 10-50K, BOFU 5-30K. If your numbers are off-band, the layering is wrong.
- **Competitive displacement is MOFU/BOFU only.** Listing competitor products as skill targets at TOFU reads as aggressive and tanks engagement.
- **Insight Tag required for retargeting.** No tag = no retargeting audience. Confirm before recommending it.

---

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **paid-campaign-strategy** | Campaign architecture, audiences, objectives | Required |
| **product-messaging** | Value props, differentiators, proof points | Recommended |
| **icp-behavioural** | Customer language, pain points, persona detail | Recommended |
| **competitor-research** | For competitive displacement campaigns | Optional |
| **brand-kit + tov-guidelines** | Voice + visual constraints | Recommended |

---

## Process

**Four-phase flow:** Funnel-stage selection → Copy generation (3 variants per ad, character verification) → Targeting + budget mapping → Verification + structured output. Full flowchart, ad-format spec table, hook patterns per stage, targeting AND/OR logic, and competitive displacement playbook in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent metrics or customer names.** If proof isn't in product-messaging or messaging library, mark `[NOT AVAILABLE]` and omit.
2. **Don't approximate character counts.** Count every variant before output.
3. **Don't recommend bid strategies the client can't run.** Manual bidding requires Campaign Manager access; flag if unavailable.
4. **Don't fabricate skill IDs for competitive displacement.** If you don't have the verified LinkedIn skill ID, name the skill in plain text and flag for the client to verify in Campaign Manager.
5. **Audience-size estimates are estimates.** Always note "approximate" — LinkedIn forecasts shift based on time of day and recent activity.

---

## Quality

Self-evaluation checklist (character compliance, variant distinctiveness, funnel logic, voice rules), anti-examples (close-enough char counts, paraphrase variants, TOFU with hard CTA, title-AND-skill targeting), failure-mode triage (low CTR / CPC spikes / under-performing carousels) in the premium reference.

---

## Integration with Other Skills

### Upstream (consumes)

| Skill | What it provides | Required? |
|-------|-----------------|-----------|
| `paid-campaign-strategy` | Campaign architecture + objectives | Required |
| `product-messaging` | Value props + proof points | Recommended |
| `icp-behavioural` | Customer language + persona depth | Recommended |
| `competitor-research` | Competitive displacement angles | Optional |

### Downstream (feeds into)

| Skill | How output is used |
|-------|-------------------|
| `ad-creative-brief` | Visual direction per format (image/video/carousel) |
| `paid-ads-audit` | Baseline copy reference for performance review |
| `landing-page-copy` | Headline alignment for ad → page consistency |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

