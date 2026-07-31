---
name: sales-tracks
version: '1.0'
last_updated: 2026-05-01
author: genesys-growth
description: >-
  Creates persona-specific sales pitch tracks for live discovery and demo conversations.
  Each track combines a story arc that empathises with persona pain and JTBD, a
  capability/differentiator/benefit pitch sequence sourced from product-messaging,
  embedded objection handlers mined from win-loss-analysis transcripts, and a
  competitive anchor matrix that positions against each priority competitor for THAT
  specific persona. Consumes the full PMM foundational research stack: icp-research +
  icp-behavioural + positioning + product-messaging + competitor-research +
  win-loss-analysis + tov-guidelines + expert-pov + brand-kit. Outputs ship as
  per-persona markdown pages and optionally publish to Notion as a sales playbook
  the rep scans before a call. Triggered by "sales tracks", "pitch playbook",
  "talk track for [persona]", "sales playbook", "pitch deck for [persona]".
goal: Produce per-persona sales pitch tracks for live discovery + demo conversations.
outcome: A persona playbook (markdown + optional Notion) with one page per persona — story arc, capability pitch, objection handlers, competitor positioning matrix — locked for sales-team use and refreshed when upstream PMM artifacts change.
primitive: sales-enablement
sub_primitive: execution
ontology_type: sales-enablement-asset
review_gate: 3
inputs:
  required: []
  recommended:
    - icp-research
    - icp-behavioural
    - positioning
    - product-messaging
    - competitor-research
    - win-loss-analysis
    - tov-guidelines
    - expert-pov
    - brand-kit
depends_on: []
owned_by_agent: sales
mcps_used:
  - notion
  - granola
triggers:
  slash_commands:
    - sales-tracks
  natural_language:
    - "sales tracks"
    - "pitch playbook"
    - "talk track for"
    - "sales playbook"
    - "pitch deck for [persona]"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
slim_exemption: null
---

# Sales tracks

Persona-specific sales pitch tracks for live discovery and demo conversations. Each track is a single page the rep scans 60 seconds before a call: who they're talking to, the story arc to open with, the capability sequence to land, the objections they'll hear (with verbatim transcript quotes), the competitor moves to counter, and the discovery questions that confirm fit.

The body of this file holds decision-grade context (when to invoke, inputs, output structure, anti-Frankenstein guardrails, gotchas). Step-by-step process, output template, quality gates, and iteration prompts live in the premium reference.

This is the **persona-axis** sales artifact, complementing battlecards (competitor-axis), sales-deck (full pitch deck), and demo-script (product demo flow). A rep typically uses two together: sales-tracks for "who am I selling to," battlecards for "they brought up [competitor]."

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`doc-output-structure.md`](../../../../rules/doc-output-structure.md) — GDoc/Notion structural defaults (when published)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in sales-tracks |
|---|---|---|
| **R1** | Source placement (three layers) | Rep-facing working markdown stays internal-inline cited (auditability). Published Notion playbook is a **client-team surface** — sources move to a collapsed "Sources" toggle at the bottom of each persona track. No `[VERIFIED:...]` tags inline in the face doc. |
| **R3** | Product-update tone | §3 capability pitches default to "we shipped X to address Y" framing. Never "we're thrilled to announce." Even Tier 1 features get product-update tone. |
| **R6** | CTA hierarchy | §7 discovery questions end with the stage-appropriate next step — trial/sign-up for cold prospects, product-action for warm-base accounts already in motion. Never blog or PDF as primary CTA. |
| **R9** | Action-oriented section names | Section names already verb-led (Story arc, Capability pitch, Objection handlers, Discovery questions). Preserve — do not rename to status-oriented variants ("Overview," "Background"). |

---

## Claude Code triggers

**Invoke this skill when user says:**
- "Create sales tracks for [client]"
- "Pitch playbook for [persona / segment]"
- "Talk track for [persona]"
- "Sales playbook"
- "Pitch deck for [persona]" (when they mean the rep-facing playbook, not a slide deck)
- "How should the rep open with a [persona]"

**Do NOT invoke when:**
- User wants per-competitor intel → Use `/battlecards`
- User wants the customer-facing slide deck → Use `/sales-deck`
- User wants the live product demo flow → Use `/demo-script`
- User wants the deeper persona research itself → Use `/icp-research` or `/icp-behavioural`

---

## Input requirements

### Required inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Client + persona dimensions** | Which personas to produce tracks for (stage, founder profile, industry — whichever axes the user wants) | User specifies |
| **At least one PMM foundation artifact** | Must have positioning OR messaging at minimum to write capability sequences | Client folder |

### Recommended inputs (the full chain — every consumer is named in the component map below)

| Input | Why it improves the track |
|-------|---------------------------|
| `icp-research` | Persona snapshot: segments, JTBD, pains, desired outcomes, anti-ICP |
| `icp-behavioural` | Persona snapshot: day-in-life, decision narratives, language patterns |
| `positioning` | Story arc: anchors and differentiators frame the resolution |
| `product-messaging` | Capability/diff/benefit pitch: per-product value props |
| `competitor-research` | Competitive anchor matrix: per-competitor intel |
| `win-loss-analysis` | Objection handlers + DIY/status-quo: verbatim quotes |
| `tov-guidelines` | Voice the rep should adopt — keeps the track on-brand |
| `expert-pov` | Empathy hook voice; founder narrative for the story arc |
| `brand-kit` | Visual identity for Notion publish (colors, type) |

### Input validation checklist

Before proceeding, verify:
- [ ] Client confirmed and persona dimensions defined (with the user)
- [ ] At least positioning or messaging exists in the client folder
- [ ] If competitor-positioning section is in scope: one file per priority competitor
- [ ] If objection-mining is in scope: win-loss-analysis OR raw transcripts available

**If recommended inputs are missing or stale (>90 days for messaging/positioning, >180 days for ICP/competitors):** the skill flags the gap and offers three options — run upstream skill first, proceed with stale + cite, or skip the affected section. Never fabricate to fill a gap.

---

## Process at a glance

| Phase | Purpose | Output |
|-------|---------|--------|
| 1. Persona scoping | Confirm persona axes with user; map to existing ICP segments | Confirmed persona list |
| 2. Narrative drafting | Story arc + capability pitch per persona | Draft sections 1-3 |
| 3. Objection + competitor enrichment | Mine win-loss for verbatim objections; build competitive anchor matrix | Draft sections 4-6 |
| 4. Validation + optional Notion publish | Quality gates; convert to Notion blocks if push enabled | Final tracks + Notion pages |

Full step-by-step (with checkpoints, persona-discovery flowchart, component-map consumption order, Granola fallback pattern, Notion publish commands) in the premium reference.

---

## Per-persona track structure (8 sections — no exceptions)

Every track contains these sections in this order:

1. **Persona snapshot** — who they are, JTBD, top 3 pains, top 3 desired outcomes
2. **Story arc** — empathy hook → tension → resolution. Three short paragraphs the rep can paraphrase
3. **Capability → differentiator → benefit pitch** — table mapping each capability the rep should land to its differentiator-versus-alternative and the benefit the persona feels
4. **Objection handlers** — verbatim transcript quote → recommended response → proof-point fallback. No invented objections
5. **Competitive anchor matrix** — rows = priority competitors + DIY/status-quo, columns = how they position to this persona / where they win / where we win for THIS persona / recommended response
6. **DIY / status-quo handling** — separate section because "we'll keep using Excel + the bank's portal" is a different objection class than competitor switching
7. **Discovery questions** — 3-5 fit-confirmation questions + 2-3 landmines that surface qualification signals
8. **Sources** — every quote, claim, competitor fact carries `[VERIFIED: source, date]` per [`ontology.md`](../../../../rules/ontology.md)

Full template with field-level guidance and a worked example in the premium reference.

---

## Component map — which input feeds which section

This is the explicit consumption chain. Every section names its primary input (the artifact it can't be written without) plus enriching inputs. Auditable: a reviewer can ask "where did this paragraph come from?" and trace it back to a locked PMM artifact.

| Section | Primary input | Enriching inputs |
|---------|---------------|------------------|
| 1. Persona snapshot | `icp-research` | `icp-behavioural`, `win-loss-analysis` |
| 2. Story arc | `positioning` | `expert-pov`, `tov-guidelines` |
| 3. Capability pitch | `product-messaging` | `positioning`, `pricing-strategy` |
| 4. Objection handlers | `win-loss-analysis` | Granola transcripts (MCP), `competitor-research` |
| 5. Competitive matrix | `competitor-research` | `positioning`, `win-loss-analysis` |
| 6. DIY / status-quo | `win-loss-analysis` | `icp-behavioural`, `funnel-strategy` |
| 7. Discovery questions | `icp-research` | `icp-behavioural`, `win-loss-analysis` |
| 8. Sources | (all) | — |

---

## Anti-hallucination guardrails

**Critical for sales credibility — sales reps lose deals when they cite invented data:**

1. **Never invent objections.** Only verbatim quotes from win-loss-analysis or `_batches/` files. Mark gaps as `[OBJECTION GAP: no transcript evidence — gather in next batch]`.
2. **Never fabricate persona pains.** ICP-research is the canonical source. If a persona dimension isn't in icp-research yet, flag the gap.
3. **Never guess competitor pricing or features.** Use the competitor-research file or mark `[CONFIRM: pricing from competitor sales call]`.
4. **Never write a story arc without positioning anchors.** If positioning is missing, run `/positioning` first or flag the gap.
5. **Cite every claim.** `[VERIFIED: file-path, access-date]` on quotes, competitor facts, persona attributes.
6. **Be honest about persona uncertainty.** If a persona is hypothesised vs validated, mark it `[EMERGING: 1-3 data points]` per ontology maturity levels.
7. **Anti-Frankenstein:** never copy-paste full paragraphs from messaging/positioning into the track. Reframe in rep voice; cite the source.

---

## Gotchas

- **Generic "trust me" objection handlers** — "we have great support" instead of "here's the verbatim quote we got and the 2-sentence response that worked." Every handler must tie to a transcript moment.
- **Competitor matrix that's just feature parity** — readers' eyes glaze. Each row must end with the *persona-specific* "where ClientCo wins for THIS persona" — different per stage even with the same competitor.
- **Story arc that sounds like a pitch deck** — if you can drop it into a sales-deck without changes, it's too polished. The rep paraphrases; the doc primes them.
- **Discovery questions that are leading or product-y** — "would you benefit from consolidated cash views?" is bad; "how do you currently see your group cash position?" is good. Open, persona-fit-confirming, never product-pushing.
- **Stale inputs silently used** — if competitor file is 6 months old, the recommended response may be wrong. Quality gate checks input ages.
- **One-track-fits-all** — if 4 tracks read identically, you've over-generalised. The persona-specificity test: would a rep handed only this track know which persona they're talking to within the first paragraph?

---

## Integration with other skills

### Upstream skills (provide inputs)

| Skill | What it provides | Required? |
|-------|------------------|-----------|
| **icp-research** | Segments, JTBD, pains, anti-ICP, voice quotes | Recommended |
| **icp-behavioural** | Personas, day-in-life, decision narratives | Recommended |
| **positioning** | Anchors, differentiators, primary/secondary frames | Recommended |
| **product-messaging** | Per-product value props, taglines, proof points | Recommended |
| **competitor-research** | Per-competitor intel for matrix | Recommended |
| **win-loss-analysis** | Verbatim objections, lost-deal patterns | Recommended |
| **tov-guidelines** | Voice the rep adopts | Recommended |
| **expert-pov** | Founder narrative for story arc | Recommended |
| **brand-kit** | Visual identity (Notion publish) | Optional |

### Downstream skills (consume outputs)

| Skill | How it uses sales tracks |
|-------|-------------------------|
| **sales-deck** | Persona-tailored slide variants per stage |
| **demo-script** | Persona-specific demo flow (which features to lead with) |
| **outreach-emails** | Persona-specific email subject + opening |
| **abm-campaign** | Per-account playbook (sales track + battlecard combined) |

---

## MCP integration

**Level:** 2 — PM Execution (inherits upstream, plus 2 MCPs)

- **Notion** — `mcp__claude_ai_Notion__notion-create-pages` for publish (when `push_targets` includes notion). First iteration uses MCP directly; will migrate to `push.toNotion()` once Phase C adapter ships in [`.claude/mcp/push.mjs`](../../../../mcp/push.mjs).
- **Granola** — `query_granola_meetings({client, filter})` as fallback if win-loss-analysis doesn't surface enough verbatim objections for a persona. Read-only.

**Inherits from:** all 9 recommended PMM inputs above. No fresh competitor pulls — that's `/competitor-research`'s job.

**Fallback (no MCP):** Skip Notion publish step. Skip Granola fallback for objection mining. Skill still produces local markdown.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

