---
name: linkedin-prospecting-loop
version: '1.0'
last_updated: 2026-06-29
author: genesys-growth
description: 'End-to-end LinkedIn prospecting loop that turns an ICP into a qualified, signal-prioritized, personalized, sequenced outbound run by orchestrating existing skills + MCPs (Apify find, Apollo enrich, lead-scoring, cold-DM doctrine, Extrovert voice) behind a human approval gate at every phase. Triggers: "LinkedIn prospecting loop", "run LinkedIn outbound for this ICP", "prospect on LinkedIn end to end", "find-qualify-message-sequence on LinkedIn". Requires icp-research; reuses linkedin-engagement-prospects, lead-scoring, linkedin-social-selling, abm-campaign. NOT for one-off warm DMs (use linkedin-social-selling), pure find (use linkedin-engagement-prospects), or content creation (use the linkedin-* content skills).'
goal: Turn an ICP into a qualified, personalized, sequenced LinkedIn outbound run by orchestrating existing skills + MCPs behind human approval gates.
outcome: 'A prospecting run — signal-prioritized qualified leads, per-prospect openers, a Day 0/4/9/30 sequence with signal-reset, and a LinkedIn-to-email channel plan — approved phase by phase, executed on Extrovert + Apify + Apollo. Unblocks repeatable cold LinkedIn outbound without manual skill-stitching.'
primitive: outbound
sub_primitive: execution
ontology_type: outreach-sequence
review_gate: 3
inputs:
  required:
  - icp-research
  recommended:
  - lead-scoring
  - company-context
  - linkedin-engagement-prospects
  - linkedin-social-selling
  - abm-campaign
- type: outreach-sequence
  feeds_into: []
depends_on:
- icp-research
owned_by_agent: growth
mcps_used:
- apify
- apollo-io
- extrovert
- exa
- gdrive
- notion
triggers:
  slash_commands:
  - /linkedin-prospecting-loop
  natural_language:
  - LinkedIn prospecting loop
  - run LinkedIn outbound for this ICP
  - prospect on LinkedIn end to end
  - find qualify message sequence on LinkedIn
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# LinkedIn prospecting loop

One approved motion that turns an ICP into a sequenced LinkedIn outbound run. It does not add a new capability — it chains the ones you already own (find, qualify, personalize, sequence, multi-channel) behind a human gate at every phase, so a run stops being five skills stitched by hand.

Built from the `/steal` of Gojiberry's "Connect Claude to LinkedIn via MCP" playbook. The playbook's execution layer was a paid vendor MCP; this skill runs the same motion on Extrovert + Apify + Apollo instead. See `.claude/discovery/0626-gojiberry-linkedin-mcp-steal-analysis.md`.

---

## Doctrine inherited

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, robot-tells ban
- [`outbound-research-hygiene.md`](../../../../../rules/outbound-research-hygiene.md) — dated signals (<12 months), current-company-only hooks, no invented stats
- [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md) — the 12 patterns DMs can't carry
- [`linkedin-cold-dm-doctrine.md`](../../../../../rules/linkedin-cold-dm-doctrine.md) — the cold-start motion: 9 tactics, connection/InMail envelope, "easy no" cadence
- [`marketing-psychology.md`](../../../../../rules/marketing-psychology.md) — Rule of 7 (touch count), loss aversion, jobs-to-be-done
- [`pii-redaction.md`](../../../../../rules/pii-redaction.md) — mask end-client PII before model/store/share (fires on ClientCo/FCA data)

---

## When to run

**Invoke when the user says:**
- "run a LinkedIn prospecting loop for [ICP/client]"
- "find, qualify, message and sequence [segment] on LinkedIn"
- "build me a cold LinkedIn outbound run end to end"

**Do NOT invoke when:**
- One-off warm DM off a single signal → `linkedin-social-selling`
- Pure prospect-find with no sequencing → `linkedin-engagement-prospects`
- Writing LinkedIn content → the `linkedin-*` content skills
- Email-only outreach → `outreach-emails`

---

## The loop

```
ICP ─► [0] Health + load ─► [1] Find + signal ─► [2] Qualify ─► [3] Personalize ─► [4] Sequence ─► [5] Multi-channel
              │ │ GATE │ GATE │ GATE │ │ GATE
              └─ Extrovert └─ Apify/Apollo └─ lead-scoring └─ cold-DM + └─ Day 0/4/9/30 └─ abm-campaign
                 safety caps + 7 signals 0–10 route Extrovert voice + Rule of 7 + channel switch
```

Every gate is human approval. The loop **drafts and queues — it never auto-sends.** Sends route through Extrovert under its own LinkedIn safety caps.

### Phase 0 — Account health + ICP load
Read the locked ICP (`icp-research`). Verify LinkedIn account safety before any sends — reuse the SSI / pending-request / acceptance-rate caps in [`linkedin-social-selling`](../social-selling/SKILL.md)& Limits (2026)". Stop here if the account is over caps.

### Phase 1 — Find + signal scan → GATE
Pull prospects matching the ICP via `linkedin-engagement-prospects` (Apify modes), `apollo-io` enrichment, and the signal skills (`jobs-signal`, `niche-signal-discovery`). Score each prospect against the 7-signal taxonomy and flag the active-intent signals (see the premium reference). **Gate:** present the signal-ranked shortlist; user keeps the contact-now set.

### Phase 2 — Qualify → GATE
Run `lead-scoring` (0–10 on fit / intent / accessibility → route: contact now / nurture / discard) on the kept set. **Gate:** user confirms the contact-now routing.

### Phase 3 — Personalize → GATE
Draft per-prospect openers using [`linkedin-cold-dm-doctrine.md`](../../../../../rules/linkedin-cold-dm-doctrine.md) (notification-preview opener, feel-chosen, weightless ask, soft exit) and the warm plays in `linkedin-social-selling`. Voice via the Extrovert MCP. Every message passes the `ai-speak-anti-patterns.md` gate. **Gate:** user approves messages one by one (or in batches once the ICP is trusted).

### Phase 4 — Sequence
Build the Day 0 / 4 / 9 / 30 cadence with signal-reset (see the premium reference), respecting Rule of 7 touch counts. Queue, do not send.

### Phase 5 — Multi-channel → GATE
Apply the LinkedIn↔email channel-switch heuristic (in the premium reference) and hand non-responders to `abm-campaign` / `outreach-emails`. **Gate:** user approves the channel plan.

---

## Tool swap (Gojiberry → your stack)

| Playbook step | This loop uses |
|---|---|
| Find + read signals | `linkedin-engagement-prospects` (Apify) + `apollo-io` + `jobs-signal` / `niche-signal-discovery` + Exa |
| Qualify (0–10) | `lead-scoring` |
| Personalize | `linkedin-cold-dm-doctrine` + `linkedin-social-selling` plays; draft via Extrovert MCP |
| Sequence | the premium reference + Rule of 7 |
| Multi-channel | `abm-campaign` + `outreach-emails` |

No Gojiberry. Nothing here needs a new MCP — all four (Apify, Apollo, Extrovert, Exa) are already mounted.

---

## MCP credit gate

This loop calls credit-bearing MCPs. Per [`apify-credits.md`](../../../../../rules/apify-credits.md) and [`apollo-credits.md`](../../../../../rules/apollo-credits.md): estimate cost and confirm before any Apify actor run or Apollo enrichment. Search is free; enrichment + scraping cost credits. State the estimate at the Phase 1 gate.

---

## Anti-hallucination guardrails

1. Never invent signal data — only reference real, dated engagement (per `outbound-research-hygiene.md`).
2. No fabricated metrics or fake social proof — use `[X]` placeholders if unknown.
3. Verify ICP fit per prospect — a signal alone is not a qualification.
4. Never auto-send — every phase gate is human approval.
5. Redact end-client PII before model/store/share for regulated clients (`pii-redaction.md`).

---

## Integration with other skills

| Skill | Relationship |
|---|---|
| `icp-research` | Required upstream — supplies the ICP the loop runs on |
| `linkedin-engagement-prospects` | Called in Phase 1 (find + signal) |
| `lead-scoring` | Called in Phase 2 (qualify + route) |
| `linkedin-social-selling` | Called in Phase 3 (plays + account-safety caps) |
| `abm-campaign` / `outreach-emails` | Called in Phase 5 (multi-channel) |
| `extrovert-sync` | Keeps the Extrovert voice seed current for Phase 3 drafting |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

