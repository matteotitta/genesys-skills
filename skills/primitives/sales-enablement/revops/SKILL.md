---
name: revops
version: '1.0'
last_updated: 2026-05-17
author: genesys-growth
description: Audits a client's revenue operations layer — CRM hygiene, MQL→SQL routing, lead scoring, sales-cycle stage definitions, funnel reporting — and produces a prioritized fix-list. Distinct from /lifecycle-marketing (which runs campaigns) and /sales-enablement (which equips reps with assets) — this skill addresses the plumbing between the two. Triggered by "revops audit", "HubSpot cleanup", "MQL SQL routing", "lead scoring fix", "CRM hygiene", "funnel reporting broken". Paired triage half /revops-incident-response is built — that skill decides which leak to fix first; this one measures.
goal: Surface and prioritize RevOps plumbing fixes that unblock pipeline conversion.
outcome: Produces (1) CRM hygiene audit, (2) MQL→SQL routing audit with shared definitions, (3) lead-scoring model audit, (4) sales-cycle stage audit, (5) funnel-reporting audit, (6) prioritized fix-list with effort estimates.
primitive: sales-enablement
sub_primitive: null
ontology_type: content-audit
review_gate: 2
inputs:
  required: []
  recommended:
  - icp-research
  - funnel-strategy
  - analytics-tracking-plan
- type: content-audit
  feeds_into:
  - funnel-strategy
depends_on: []
- funnel-strategy
- sales-enablement
owned_by_agent: sales
mcps_used:
- exa
- gdrive
triggers:
  slash_commands:
  - /revops
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
---

# /revops — revenue operations audit

Audit the plumbing between marketing and sales. RevOps lives in the gaps: CRM data quality, MQL→SQL handoff, lead scoring, stage definitions, funnel reporting. When this layer is broken, marketing spend leaks at the handoff and sales blames marketing for "bad leads".

This is the **measurement half** of an audit-triage pair. [`/revops-incident-response`](../revops-incident-response/SKILL.md) is the triage half, built 2026-07-16 per `.claude/rules/audit-triage-pairing.md` — it decides which leak to fix first, estimates fix-time, and sequences Day-0/1/14. Measure here; decide there.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in revops |
|---|---|---|
| **R1** | Source placement | Audit output is **internal-reference** (rep/marketing team). Inline `[VERIFIED:...]` tags stay for QA auditability. |
| **R3** | Product-update tone | Audit findings frame as "X is broken / Y is leaking" — operator-direct, never "we are thrilled to report." |
| **R9** | Action-oriented section names | "Audit the funnel / Find the leak / Hand off to triage" — verb-led. |

Note: this skill is internal-reference; R2/R5/R6/R7/R8 do not apply (no customer-facing surface).

---

## When to invoke

- MQL→SQL conversion rate has dropped or never been measured.
- Sales says "marketing leads are bad"; marketing says "sales doesn't follow up".
- CRM is leaking duplicate records / dead opportunities / unrouted leads.
- Lead scoring model exists but no one trusts the score.
- Funnel reporting shows different numbers depending on who's asking.

Do NOT invoke when:
- The product hasn't found PMF — fix product before fixing RevOps.
- Marketing isn't running any campaigns — there's no funnel to audit yet.

---

## Workflow

### Step 1 — CRM hygiene audit

Check the data foundation:

| Check | Question | Healthy threshold |
|---|---|---|
| Duplicate records | What % of contacts have a duplicate? | < 5% |
| Stale records | What % haven't been touched in 12+ months? | < 30% (or actively archived) |
| Field completeness on key fields (title, company, segment) | What % have all 3? | > 80% |
| Closed-lost re-entry process | Documented and followed? | Yes |
| Source attribution on every contact | Tagged with traffic source / campaign? | > 95% |

Output: count + % per check. Anything below the threshold is a P1 fix.

### Step 2 — MQL→SQL routing audit

The handoff is where most RevOps pain lives. Audit:

- **Shared definition.** Is MQL defined? Is SQL defined? Are both signed off by marketing AND sales? If no shared doc exists, that's finding #1.
- **Routing mechanic.** When an MQL converts, where does it go? (Round-robin? Territory? Specific AE?) Documented?
- **SLA.** How fast must sales touch a new SQL? (Best-practice: <5 min for inbound demo; <24h for content-driven.) Tracked?
- **Disposition tracking.** When sales rejects an SQL, is the reason captured back to marketing? (No-reject-feedback loops are blind.)

### Step 3 — Lead scoring audit

If a lead scoring model exists:
- What inputs feed it? (Firmographic, behavioral, intent, fit.)
- When was it last calibrated? (Models > 12 months old are usually wrong.)
- What's the correlation between score and actual close? (If close rate at score 80 isn't 2× score 40, the model is noise.)
- Is the score visible / actionable to sales? (Hidden scores = unused scores.)

If no model exists, propose a starter (firmographic fit × behavioral intent × time-decay), not a perfect one.

### Step 4 — Sales-cycle stage definitions

Every stage needs:
- Exit criteria (what must be true to advance).
- Owner (who advances).
- Standard duration (so stale deals get flagged).

Common gaps:
- "Discovery" → "Proposal" with no exit criteria → reps advance prematurely.
- "Negotiation" with no standard duration → deals park here for quarters.
- "Closed Won" with no source-attribution capture → no feedback loop to marketing.

### Step 5 — Funnel reporting audit

The single most-asked question in RevOps: "what's our funnel?". Audit:
- Is there ONE source of truth? (HubSpot? Salesforce? A spreadsheet?)
- Do marketing + sales + finance see the same numbers?
- Are conversion rates between stages calculated consistently (cohort-based, not snapshot)?
- Is the reporting cadence regular? (Monthly minimum for B2B; weekly for high-velocity.)

### Step 6 — Prioritized fix-list

Score each finding on Impact × Ease (1–5 each):

| Finding | Recommendation | Impact | Ease | Score | Priority |
|---|---|---|---|---|---|
| No shared MQL/SQL definition | Workshop with marketing + sales + RevOps; sign off in 1 page | 5 | 4 | 20 | P0 |
| 32% of contacts have duplicates | HubSpot dedupe + ongoing dedupe rule | 4 | 3 | 12 | P1 |
| Lead scoring model 24 months old | Refresh inputs + recalibrate against last 6mo closed deals | 4 | 2 | 8 | P2 |
|... |

Top 3 land in the action queue.

---

## Worked example — ClientCo HubSpot cleanup

**Findings:**
- No shared MQL/SQL definition (P0).
- 18% duplicate contacts in HubSpot (P0).
- Lead routing: round-robin within an SDR team that's been restructured 3 months ago — routing rules never updated (P0).
- No SLA on inbound demo requests — measured at 4-hour median response (P1).
- Lead scoring model exists, score correlation with close = 0.1 (statistical noise) — P2 because requires more work than the 3 P0s.

**Top 3 action queue:**
1. Define MQL/SQL in 60-min workshop next week; sign off in 1-pager.
2. HubSpot dedupe pass (manual review of top 200 duplicates; automated rule for future).
3. Update routing rules to match current SDR team structure.

---

## Anti-patterns

- ❌ Audit without sales in the room. Marketing-only RevOps audits miss the handoff layer.
- ❌ Propose a perfect lead-scoring model on day 1. Calibration takes 90+ days; ship the rough model and iterate.
- ❌ Skip the funnel-reporting audit because "the dashboard exists". One dashboard ≠ one source of truth.
- ❌ Fix downstream (stage definitions) before fixing upstream (MQL/SQL definition). Cascade.
- ❌ Stay in the `/lifecycle-marketing` lane (campaigns) when the problem is plumbing.

---

## Integration with other skills

- **Upstream:** `/icp-research` defines the fit criteria for lead scoring; `/funnel-strategy` defines the stage model.
- **Downstream:** Findings feed `/sales-enablement` (battlecards, training); priorities feed `/analytics-tracking-plan` (instrumentation fixes).
- **Triage half (built):** [`/revops-incident-response`](../revops-incident-response/SKILL.md) per `.claude/rules/audit-triage-pairing.md`. Hand the prioritized fix-list to it, or send it a symptom report directly.

---

## Attribution

This skill adapts patterns from [`coreyhaines31/marketingskills/revops/SKILL.md`](https://github.com/coreyhaines31/marketingskills/blob/main/skills/revops/SKILL.md) (MIT license, © Corey Haines / Conversion Factory). Adapted to Genesys operator voice; integrated with funnel-strategy + analytics-tracking-plan.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/scope-guardian-reviewer` — the client-deliverable ship gate: scope-creep check on proposals/SOWs (pm-loop.md). A RevOps audit surfaces every broken thing in the CRM at once; this is the gate that keeps a scoped fix-list from becoming an unscoped cleanup project.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

