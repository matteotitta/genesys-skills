---
name: linkedin-social-selling
version: '1.3'
last_updated: 2026-06-16
author: genesys-growth
description: 'Connects LinkedIn content to outbound pipeline via signal-based warm outreach. Produces 12 tactical outreach
  plays, TWE scoring frameworks, and content-to-engagement-to-outreach flywheel architecture. Triggers: "social selling",
  "signal-based outreach", "warm outreach", "LinkedIn automation", "HeyReach", "Scripe", "AuthoredUp", "TWE scoring". Consumes
  engagement signals from linkedin-comment. Feeds into outreach-emails for DM-to-email bridge.'
goal: Connects LinkedIn content to outbound pipeline via signal-based warm outreach.
outcome: 'Connects LinkedIn content to outbound pipeline via signal-based warm outreach. Produces 12 tactical outreach plays,
  TWE scoring frameworks, and content-to-engagement-to-outreach flywheel architecture. Triggers: "social selling", "signal-based
  outreach", "warm outreach", "LinkedIn automation",...'
primitive: social
sub_primitive: linkedin
ontology_type: outreach-sequence
review_gate: 2
inputs:
  required:
  - linkedin-content-guide
  recommended: []
- type: outreach-sequence
  feeds_into: []
depends_on:
- linkedin-content-guide
owned_by_agent: content
mcps_used:
- apollo-io
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

# LinkedIn Social Selling

Signal-based LinkedIn outreach that turns content engagement into pipeline. 12 tactical plays leveraging intent signals to maximize response rates. Apollo + Exa for prospect research; per-prospect Apollo enrichment gated per `.claude/rules/apollo-credits.md`.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`outbound-research-hygiene.md`](../../../../../rules/outbound-research-hygiene.md) — dated signals, current-company-only hooks, no invented stats
- [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md) — the 12 patterns DMs and comments can't carry
- [`linkedin-cold-dm-doctrine.md`](../../../../../rules/linkedin-cold-dm-doctrine.md) — the cold-start motion: 9 tactics, connection/InMail envelope, "easy no" cadence (powers the cold-start plays)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in linkedin-social-selling |
|---|---|---|
| **R1** | Source placement (three layers) | DMs and comments are **end-customer-facing**. **No source tags inline.** Internal play-tracking + research evidence lives in working notes only; never surfaces in the DM body. |
| **R3** | Product-update tone | When a play references our product, frame as "I shipped X" or "we ship X" — never "we are thrilled to announce." Reads as ad copy, not as a human reaching out. |
| **R6** | CTA hierarchy | DM closes name the next step appropriate to the signal — discovery-call for cold signal (profile view), trial sign-up for content engagement, demo for high-intent (pricing-page visit). Blog as fallback when the prospect isn't yet sign-up-ready. |
| **R9** | Action-oriented section names | "Spot the signal / Open the DM / Land the value / Close on next step" — verb-led across every play. |

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "social selling playbook"
- "LinkedIn outreach strategy"
- "signal-based outreach"
- "turn engagement into pipeline"
- "outreach plays"
- "LinkedIn DM strategy"
- "convert profile viewers"
- "reach out to post engagers"
- "website visitor outreach"
- "InMail strategy"
- "cold DM" / "cold LinkedIn outreach"
- "cold-start plays"
- "connection request strategy"

**Do NOT invoke when:**
- User wants to create LinkedIn content → Use appropriate `linkedin-*` skill
- User wants to write comments → Use `linkedin-comment` skill
- User wants to build a full founder LinkedIn program → Use `linkedin-content-guide-founders` skill
- User wants email outreach → Use `outreach-emails` skill

---

## Core Framework: Content → Engagement → Outreach Flywheel

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. POST CONTENT 2. TRACK SIGNALS 3. OUTREACH │
│ Content attracts ───► Who engages? ───► Reach out │
│ ICP attention Profile views with context │
│ Post likes/comments │
│ Website visits │
│ │
│ 4. CONVERT TO PIPELINE │
│ DM → Call → Deal │
└─────────────────────────────────────────────────────────────────┘
```

**Why this works:**
- LinkedIn outreach gets 5-7× better response rates than cold email
- Warm signals (engagement) = 3-4× higher response than cold lists
- Context from their engagement makes messages hyper-relevant
- Content builds trust before the conversation starts

---

## Account Safety & Limits (2026) — voice-locked

Verify account health before any plays. These constants drive every send-or-skip decision.

| Metric | Target | Risk if below |
|--------|--------|---------------|
| Social Selling Index (SSI) | Above 70 | Flagged faster |
| Pending connection requests | Under 700 | #1 spam signal |
| Connection acceptance rate | Above 30% | Auto-restriction |

**Connection limits:**
- Weekly: 100-150 (standard), 200-250 (high-SSI Sales Nav)
- Daily safe limit: 25 connections, 5 days/week
- Monthly capacity: 800-1000 outreach messages per account

**2026 InMail changes (CRITICAL):**
- Open InMail cap reduced ~87% (from ~800/month to under 100)
- Sales Navigator Advanced/Corporate now essential
- Recruiter plans have highest limits
- Credits returned on responses — quality > quantity
- Prioritize warm signals before cold lists

**Automation safety:**
- Avoid cheap browser-based automation tools (<$50/mo)
- Run automation during prospect's local business hours
- Don't run multiple automation tools on one account
- Disable Grammarly and ad-blockers while automating

---

## Signal Priority Order — voice-locked

Reach out in this order for best results. Higher-priority signals deserve faster turnaround and the warmest channel first.

| Priority | Signal | Response rate | Temperature |
|----------|--------|---------------|-------------|
| 1 | Website pricing page | Highest | Hot |
| 2 | Website visitor (any) | Very high | Hot |
| 3 | Profile viewer | High | Warm |
| 4 | Post commenter | High | Warm |
| 5 | Post liker | Medium-high | Warm |
| 6 | Company page follower | Medium | Lukewarm |
| 7 | New job starter (<90 days) | Medium-high | Lukewarm |
| 8 | Competitor post engager | Medium | Cool |
| 9 | Keyword post author | Medium | Cool |
| 10 | Influencer follower | Low-medium | Cold |
| 11 | Event attendee | Low-medium | Cold |
| 12 | Open profile (cold list) | Lowest | Cold |

---

## TWE Pre-Qualification — voice-locked

Before loading prospects into automation, score the upstream content strategy. Content with TWE < 4 only generates vanity engagement; loading those signals into automation wastes capacity.

| Dimension | Weight | Question |
|-----------|--------|----------|
| **Thought (T)** | 1 point | Does content share a genuine POV or insight? |
| **Work proof (W)** | 2 points | Does content reference real work, clients, or results? |
| **Engagement hook (E)** | 4 points | Does content trigger a reply, DM, or comment from ICP? |

Minimum TWE total: 4 (out of 7) before automating.

---

## Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Intent signal** | Profile view, post engagement, website visit, etc. | RB2B / Sales Nav / Valley / manual |
| **Prospect details** | Name, company, role, LinkedIn URL | Sales Nav / Apollo / user-provided |
| **ICP context** | Whether prospect fits target segment | `icp-research` upstream |

---

## Process

**Five-phase flow:** Account health check → Signal identification & prioritization → Play selection & message crafting → Self-evaluation → Review gate. Full step-by-step + tool stack details + MCP integration in the premium reference.

**12 warm plays + 4 cold-start plays (with Phase 0 connection protocol) + voice notes + no-brainer offer + technographic + multi-channel amplification** in the premium reference. Cold-start plays consume [`linkedin-cold-dm-doctrine.md`](../../../../../rules/linkedin-cold-dm-doctrine.md).

---

## Anti-Hallucination Guardrails

1. **Never invent signal data.** Only reference real engagement (verified by Valley / Sales Nav / RB2B / manual).
2. **Don't fabricate metrics.** Use `[X%]` placeholder if unknown.
3. **No fake social proof.** Only cite real client names with permission.
4. **Verify ICP fit.** Signal alone doesn't mean qualified.
5. **Check contact history.** Don't re-contact recent outreach (>90 days since last touch).

---

## Quality

Pre-outreach checks cover message quality (under 75 words, signal reference, no pitch), account safety (limits, single automation tool), targeting (ICP fit verified separately), and TWE pre-qualification. Worked example (picking play for pricing-page signal) + anti-examples (generic cold-DM, pitch in first message, multi-tool stacking, ignoring 2026 InMail caps) + post-launch failure-mode triage in the premium reference.

---

## Integration with Other Skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **linkedin-personal-posts / sales-posts / expert-posts** | Upstream | Content generates signals for outreach |
| **linkedin-comment** | Upstream | Comments warm up prospects before DM |
| **linkedin-content-guide-founders** | Parent program | Social selling is Phase 4 of the founder program |
| **outreach-emails** | Downstream | Add engaged prospects to email sequences |
| **company-context** | Research | Prospect's company before outreach |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

