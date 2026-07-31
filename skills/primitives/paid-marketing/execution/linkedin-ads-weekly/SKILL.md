---
name: linkedin-ads-weekly
version: "1.0"
last_updated: 2026-07-30
author: genesys-growth
description: |
  Runs a weekly optimise-and-report cycle on a LinkedIn Ads account. Pulls the account (via the read tools of the linkedin-ads MCP, or a pasted export when the API is not authenticated), runs ten optimisation levers split by the data volume each needs, proposes a ranked change list, and — once LinkedIn Ads writes are enabled — applies what the operator approves through the gated linkedin-ads MCP; until then it emits an operator-applies-manually change list. Reporting reuses /paid-ads-report (the WoW dashboard) and /paid-ads-experiment-log (the change journal) rather than re-implementing them. Levers: audience drift, budget pacing, creative fatigue, cost discipline, lead-form health, structure drift (weekly); creative performance, audience saturation, angle refresh, objective/bid fit (28-day). Every write is gated by linkedin-ads-spend.md. Triggers: "LinkedIn Ads weekly", "run the LinkedIn optimisation", "weekly paid social update", "pause underperforming LinkedIn ads". NOT for Google (use /google-ads-weekly), one-off account audits (/paid-ads-audit), the read-only report (/paid-ads-report), or writing ad copy (/linkedin-ads-copy).
goal: Run one weekly cycle that reads a LinkedIn Ads account, proposes ranked changes with their volume floors stated, applies the approved ones (when writes are live), and drafts the client update.
outcome: A ranked change list the operator approves, the approved mutations applied and read back (or a manual-apply list while writes are blocked), a Slack-ready weekly update, and a dated cycle record in the client's paid/execution/ folder.
primitive: paid-marketing
sub_primitive: execution
ontology_type: experiment-log
review_gate: 2
inputs:
  required: []
  recommended:
    - paid-campaign-strategy
    - brand-kit
depends_on: []
owned_by_agent: paid
mcps_used:
  - linkedin-ads
triggers:
  slash_commands:
    - /linkedin-ads-weekly
  natural_language:
    - "LinkedIn Ads weekly"
    - "run the LinkedIn optimisation"
    - "weekly paid social update"
    - "pause underperforming LinkedIn ads"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# LinkedIn Ads Weekly — optimise-and-report cycle

Reads a LinkedIn Ads account, proposes a ranked change list, applies what is approved, and drafts the weekly client update. The Google sibling is [`/google-ads-weekly`](../google-ads-weekly/SKILL.md); this is the same optimise-first-report-second discipline for LinkedIn. The report describes what changed, not just what happened.

## Doctrine inherited

- **`linkedin-ads-spend.md`** gates every write. Preview before mutate, confirm before spend or delete, never auto-confirm in batch, default to DRAFT/PAUSE. Where LinkedIn Ads writes are not yet enabled (pending Advertising-API / Developer-Portal approval), Phase 3 emits an operator-applies-manually change list and the gate activates once writes land. Non-negotiable when they do.
- **`pii-redaction.md`** applies to lead-gen form data, which carries names, work emails and job titles people submitted directly.
- **`output-simplicity.md`** caps the Slack update. One screen for a senior reader, not a metrics dump.

## When to use

Use it for the weekly cycle on a live LinkedIn Ads account where you hold at least read access.

Do not use it for:
- Google Ads → [`/google-ads-weekly`](../google-ads-weekly/SKILL.md)
- A one-off, deep account audit → `/paid-ads-audit`
- The read-only week-over-week report on its own → [`/paid-ads-report`](../paid-ads-report/SKILL.md) (this skill *invokes* it in Phase 4)
- The standalone change journal → [`/paid-ads-experiment-log`](../paid-ads-experiment-log/SKILL.md) (also invoked in Phase 4)
- Writing or refreshing ad copy → `/linkedin-ads-copy`

## Inputs

| Input | Required | Notes |
|---|---|---|
| Client slug | yes | Resolves the workflow binding, e.g. `ClientCo` |
| Account data | yes | Either the `linkedin-ads` MCP read tools, or a pasted/CSV export. Both are first-class. |
| Client workflow file | recommended | `{client}/workflows/linkedin-ads-weekly.md` carries the account's targets, campaign split and Slack format |
| Campaign strategy | recommended | The intended structure, so the cycle can detect drift, plus the persona + awareness tiers the angle matrix reads |

**The export path is not a fallback.** While the API is not authenticated, or access is read-only, or writes are not yet enabled, the cycle runs identically off a pasted export and simply produces a manual-apply change list in Phase 3.

## Process

### Phase 0 — Ground

Read the client workflow file, the paid strategy doc, and `goals/` for targets. Establish: the conversion action being optimised for (lead-gen form completion vs website conversion), the monthly budget, the intended campaign structure (a small set of campaigns spanning use-case, awareness, case-study and retargeting), and the reporting bar. Never invent a target. If it is an unfilled placeholder, say so in the output rather than substituting a benchmark.

### Phase 1 — Pull

Run the read tools in the premium reference against the `linkedin-ads` MCP, or parse the pasted export. Persist the raw pull to the client's `paid/execution/` and keep only a summary in context, per `context-management.md`.

Redact PII from lead-gen form data before it is stored or shared.

### Phase 2 — Propose

Run the ten levers in the premium reference. For each finding, produce: the lever, the evidence, the proposed change, the tier it falls in under `linkedin-ads-spend.md`, and **the volume behind it**. Rank by expected impact on cost per result.

State the floor next to every verdict. A creative with 300 impressions and no conversion is not a loser, it is unmeasured. Say that rather than proposing a pause.

Output the change list and stop. The operator approves before anything applies.

### Phase 3 — Apply

Only after approval, and only for approved items.

- **While writes are not yet enabled:** emit the approved changes as an operator-applies-manually list — the exact Campaign-Manager steps to take — and log each to the change journal via `/paid-ads-experiment-log`. Nothing is written through the API.
- **When writes land:** follow the gate — spend-reducing items (pause a fatigued creative, lower a bid or budget) may share one approval after being itemised; spend-increasing items (raise a budget, activate a campaign) are confirmed individually; deletes are refused. Create as DRAFT/PAUSED. After the batch, re-read the affected resources through the read tools and confirm each change landed. Report anything that did not.

Skip this phase entirely when running from an export.

### Phase 4 — Report

Reuse, do not re-implement:

1. **The WoW dashboard** — invoke [`/paid-ads-report`](../paid-ads-report/SKILL.md) for the client's week-over-week LinkedIn Ads report (it owns the dashboard render + auto-insight opener). This cycle supplies the window; the report skill owns the rest.
2. **The change journal** — log each applied (or manually-applied) change via [`/paid-ads-experiment-log`](../paid-ads-experiment-log/SKILL.md) with its hypothesis + expected metric, so next cycle can read the lift.
3. **The Slack update** — in the client's format. One screen. What changed, what it means, what needs a decision.
4. **The cycle record** — at `{client}/paid/execution/MMYY-NN-linkedin-ads-cycle.md`: the pull summary, the full change list with approved/rejected status, what was applied (or listed for manual apply) and verified, and the hypothesis for next week.

Then append a `run` entry to the client's `history.md` and refresh `latest.md`.

**Nothing posts to a client channel unprompted.** The Slack update is a draft for review.

## Known limitations

State these rather than working around them:

- **Writes may not be enabled** until a LinkedIn Developer App is approved for the Advertising API. Reads work; Phase 3 is manual-apply until then.
- **Competitor share is not in the API.** LinkedIn has no auction-insights equivalent. The competitor read is a separate [`/linkedin-ad-teardown`](../../strategy/linkedin-ad-teardown/SKILL.md) run against the public Ad Library, and it feeds lever 9, not a query here.
- **High CPMs, thin volume.** At £1,500/mo a week is a handful of leads. Most kill decisions sit below the floor weekly — that is the whole reason for the split.
- **Reporting lag + sampling.** Recent days under-report; demographic breakdowns are sampled. Never conclude from the last 2 days, and compare like windows.
- **Frequency is derived.** LinkedIn does not expose frequency directly — compute it as `impressions ÷ approximateUniqueImpressions`.

## Anti-patterns

- ❌ Proposing a creative pause below the impression floor. That is optimising noise.
- ❌ Reporting a cost-per-lead verdict for a single week on a small account without its floor stated.
- ❌ Re-implementing the WoW dashboard or the change journal inline. Invoke `/paid-ads-report` and `/paid-ads-experiment-log`.
- ❌ Bundling a budget increase into a soft-tier creative-pause approval.
- ❌ Treating a blocked write as a data problem. It is an auth state; run manual-apply and log it.
- ❌ Reallocating an entire budget off one week of demographic data.
- ❌ Posting the Slack update without the operator seeing it.
- ❌ Substituting an industry benchmark when the client's own target is missing. Flag the gap.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains and output template.

For the Slack update specifically, also run the `output-simplicity.md` §10 pre-ship check: right length for a senior reader, no robot tells, sources placed correctly for a client-team artifact.

