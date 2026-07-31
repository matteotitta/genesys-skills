---
name: revops-incident-response
version: '1.0'
last_updated: 2026-07-16
author: genesys-growth
description: 'Triage decision tree for revenue-funnel leaks — the paired triage half of /revops per audit-triage-pairing.md.
  Reads a /revops fix-list or a symptom report ("leads are stalling", "trials expire without converting"). Phase 0 gates
  on CRM data quality and can halt the run; Phase 1 detects named stalled leads per stage (not cohorts); Phase 2 traces
  root cause per lead across CRM stage history + call transcripts with quoted evidence; Phase 3 branches to a triage
  decision with a fix-time estimate and a Day-0/Day-1/Day-14 sequence; Phase 4 hands off. Evidence is per-lead; the verdict
  is systemic. Triggers: "revops incident", "why are leads stalling", "which leads leaked", "funnel triage", "trials are
  expiring", "fix the leak". Pairs with /revops — that audits the plumbing, this decides what to fix first. NOT for
  measurement (use /revops), NOT for prospective account routing (use /lead-scoring), NOT for closed-lost deal analysis
  (use /win-loss).'
goal: Decide which funnel leak to fix first, evidenced by per-lead root-cause traces rather than cohort statistics.
outcome: Triage report with a CRM data-quality verdict, named stalled leads carrying quoted per-lead root cause, the branch
  identified, a fix-time estimate, a Day-0/Day-1/Day-14 sequence, and a named hand-off target.
primitive: sales-enablement
sub_primitive: null
ontology_type: revops-incident-report
review_gate: 3
inputs:
  required: []
  recommended:
  - revops
  - funnel-strategy
  - icp-research
- type: revops-incident-report
  feeds_into:
  - email-nurture
  - funnel-strategy
depends_on: []
- email-nurture
- funnel-strategy
- lifecycle
owned_by_agent: sales
mcps_used:
- hubspot
- gdrive
triggers:
  slash_commands:
  - /revops-incident-response
  natural_language:
  - revops incident
  - why are leads stalling
  - which leads leaked
  - funnel triage
  - trials are expiring
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# /revops-incident-response — Decide which leak to fix first

`/revops` measures the plumbing and stops. This decides what to do about it, in what order, by when.

The unit rule, because it's easy to get wrong: **evidence is per-lead, the verdict is systemic.** A cohort stat ("483 companies died at intro→trial") names a leak but can't explain it — and an explanation invented from a cohort stat is exactly what gets invalidated on review. Tracing twenty named leads individually tells you *why*, which tells you what to fix. You ship a systemic decision backed by named leads, not a list of leads to chase.

---

## Workflow at a glance

| Phase | Purpose | Output |
|---|---|---|
| **0. Data-quality gate** | Is the CRM trustworthy enough to draw a conclusion from? | `PASS` / `PASS_WITH_CAVEATS` / **`HALT`** |
| **1. Detection** | Which named leads are stalled beyond SLA, per stage? | Named leads — never cohorts |
| **2. Investigation** | Why did each one stall? | Per-lead root cause, each citing a quote |
| **3. Triage** | Which leak first, how long, in what order? | Branch + fix-time + Day-0/1/14 |
| **4. Hand-off** | Who executes? | Named skill + a `history.md` entry |

**Phase 0 can end the run.** That is a feature, not a failure mode — see below.

---

## Phase 0 — The data-quality gate (runs first, can halt)

Never trust a leak number before you've checked whether the CRM can support one.

This exists because it already went wrong. ClientCo's [`0226-funnel-analysis.md`](../../../../../projects/consulting/active/ClientCo/sales/strategy/funnel/0226-funnel-analysis.md) shipped a confident H2-decline story attributed to a named rep's departure. Team review found she worked in **CS, not sales**, and her attributed deals were likely CRM reassignments. The same doc flags *"57% of deals have no assigned rep"* — then corrects itself: *"this is likely a CRM data quality issue (no automated self-serve deal creation exists), not evidence of self-serve dominance."* Its own priority action reads: *"Before requesting rep-level data, audit HubSpot deal lifecycle practices first."*

That is this phase, written by the client's own analysis, in advance.

**Check five things** (detail + thresholds → the premium reference):

1. **Unassigned deals** — what share have no owner? Is that real self-serve or missing automation?
2. **Defunct stages** — is any stage still in the schema but dead in practice? (ClientCo: *"the MQL stage is effectively defunct since the HubSpot migration"*.)
3. **Stage-skipping** — deals jumping stages mean stage timestamps can't carry a stall calculation.
4. **Attribution integrity** — are owners assigned by role, or by reassignment artifact?
5. **Definition drift across systems** — the same word meaning different things in two tools. (ClientCo: *"'MQL' means different things across HubSpot and Triple Dart"*.)

**Verdicts.**

- **`PASS`** → proceed to Phase 1.
- **`PASS_WITH_CAVEATS`** → proceed, but every downstream verdict carries the named caveat inline. Not a footnote.
- **`HALT`** → **stop. Emit no leak verdict.** The finding *is* the data problem, and the deliverable is the fix-list for it. Hand back to `/revops`.

A HALT is a successful run. Shipping a confident leak verdict on untrustworthy data is the failure this skill exists to prevent — and it has already happened once on this client.

---

## Phase 1 — Detection (named leads, never cohorts)

Read the live CRM. Query stage-entry timestamps and find leads sitting past their stage SLA.

**Output shape:** a named lead, its stage, days stalled, owner, and deal context. Twenty named rows beat a percentage. If the answer comes back as "59.3% converted," you've reproduced the audit, not triaged it.

Live read via HubSpot MCP (`query_crm_data`, `search_crm_objects`, `get_crm_objects`). **Read-only — never write to a client CRM.** This is the first skill in the workspace declaring `mcps_used: [hubspot]`; access is viewer-level per [`ClientCo/goals/measurement.md`](../../../../../projects/consulting/active/ClientCo/goals/measurement.md).

Redact before you reason: end-client names, emails, phones, account numbers → `[CLIENT-n]` per [`pii-redaction.md`](../../../../rules/pii-redaction.md). ClientCo is FCA-regulated and their CRM carries end-client financial detail. Keep the roles, the company, the deal shape — mask the identity.

---

## Phase 2 — Investigation (root cause, quoted)

For each stalled lead, trace across systems and answer *why this one*.

**Sources:** CRM stage history (what moved, when, and what didn't) + call transcripts. Parse transcripts with the existing adapter spec at `research/win-loss/the premium reference — WebVTT / SRT / **Gong** / Fireflies / Otter / Grain / generic JSON / plaintext. Don't rebuild it. (Granola arrives via MCP as a delivery source, not a sniffed format.)

**Every root cause cites a verbatim quote + speaker**, per [`evidence-bound-outputs.md`](../../../../rules/evidence-bound-outputs.md). No quote → mark `[INFERRED: from X + Y]` or drop the claim. Never invent the reason a deal stalled.

```
[CLIENT-7] · Intro → Trial · stalled 34d · owner: [REP]
Root cause: pricing, not fit — "we'd need sign-off above 20k and I can't get that this quarter"
            (buyer, [11:04]). Trial never provisioned.
```

**Do not screenshot the journey.** Zapier's system reconstructed lead journeys via browser automation because *their security team blocked MCP connectors*. That was their constraint; HubSpot is a live connector here. MCP reads beat screenshots — importing their workaround would import their handicap.

---

## Phase 3 — Triage (branch → fix-time → Day-0/1/14)

Aggregate the per-lead causes, then decide. Five branches — full trees, thresholds, and fix-time estimates → the premium reference:

| Branch | Fires when the per-lead causes cluster on… | First action |
|---|---|---|
| **1. Qualification leak** | Wrong-fit leads reaching a stage they can't clear (pricing shock, size mismatch) | Add the qualification gate one stage earlier |
| **2. No-nurture leak** | Right-fit leads going quiet with no follow-up mechanism | Ship the missing sequence for the largest cohort |
| **3. Handoff leak** | Stalls at an owner change or an SLA with no tracking | Instrument the SLA before changing it |
| **4. Product/proof leak** | A recurring objection engineering or marketing must answer | Route the objection, don't re-sell it |
| **5. Phantom leak** | The "leak" is a reporting artifact | Back to `/revops` — this isn't a funnel problem |

**State the volume floor.** Per [`quantitative-evidence-floors.md`](../../../../rules/quantitative-evidence-floors.md): no "biggest leak" verdict below the floor. Under it, give a directional read and say so. Name the confounds — seasonality, attribution window, conversion lag — before crediting a cause.

**Multi-branch:** when causes split across branches, rank by recoverable volume × inverse fix-time, and say what you're not doing.

---

## Phase 4 — Reporting + hand-off

Compose, don't build. Recurrence via `/schedule`; the weekly roll-up via [`/dashboard`](../../../primitives/design/dashboard/SKILL.md), which ships a pipeline-visualization template. No new cron infrastructure — that layer exists.

Hand off by branch: nurture gap → `/email-nurture` or `/lifecycle` · qualification gap → `/funnel-strategy` · plumbing/reporting → back to `/revops`. Append a `[REVOPS]` line to the client's `history.md`.

---

## Anti-Hallucination Guardrails

1. **Never fabricate a leak number.** Live CRM read or nothing. If the MCP is unavailable, say so and stop — per the `financial-data.md` posture, do not reconstruct pipeline data from memory or from a stale doc.
2. **Never invent a root cause.** Quote or lower the confidence.
3. **Never skip Phase 0.** The gate exists because the failure already happened on this client.
4. **Never write to the CRM.** Read-only, always.
5. **Never crown a leak below the volume floor.** Directional read + caveat instead.
6. **Never ship an unredacted end-client name.** FCA-bound data.

---

## Integration with other skills

| Skill | Relationship |
|---|---|
| [`/revops`](../revops/SKILL.md) | **The audit half.** It measures the plumbing; this decides. A HALT hands straight back to it. |
| [`/win-loss`](../../../research/win-loss/SKILL.md) | Explains **closed-lost deals with transcripts**. This explains **silently-stalled leads**. Different populations; its transcript adapters are reused here. |
| [`/lead-scoring`](../../../primitives/outbound/strategy/lead-scoring/SKILL.md) | **Prospective** — should we pursue this account? This is **retrospective** — why did this one die? |
| [`/funnel-strategy`](../../../research/funnel-strategy/SKILL.md) | Defines the stages and SLAs this measures stalls against. Hand-off target for Branch 1. |
| [`/email-nurture`](../../../primitives/lifecycle/email-nurture/SKILL.md) · [`/lifecycle`](../../../primitives/lifecycle/lifecycle/SKILL.md) | Hand-off targets for Branch 2. |

---

## Quality checks (pre-output)

Full gate → the premium reference. The load-bearing five:

- [ ] Phase 0 emitted an explicit verdict **before** any leak claim. A HALT emitted no leak verdict at all.
- [ ] Detection names actual leads. If the output is a percentage, it's an audit — start over.
- [ ] Every root cause carries a verbatim quote + speaker, or is marked `[INFERRED]` / dropped.
- [ ] The volume floor is stated; confounds and lag are named.
- [ ] End-client PII masked. Nothing written to the CRM.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains and output template.

Then run `/scope-guardian-reviewer` — the client-deliverable ship gate: scope-creep check on proposals/SOWs (pm-loop.md). Live-CRM findings invite scope sprawl; this is the gate that catches "while we're in here…".

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Attribution

The Detection → Investigation → Reporting shape, and specifically the **per-lead granularity + recurrence** that our cohort-level audit thinking wouldn't have produced, is adapted from Zapier's internal lead-leakage agent system as described in ["Zapier's no lead left behind agent"](https://demandcollective.substack.com/p/zapiers-no-lead-left-behind-agent), Demand Collective, accessed 2026-07-16. Cite-only — concept port, zero code. Their browser-automation implementation is deliberately **not** ported (see Phase 2). See [`.claude/discovery/0726-zapier-lead-leakage-steal-analysis.md`](../../../../discovery/0726-zapier-lead-leakage-steal-analysis.md).

---

