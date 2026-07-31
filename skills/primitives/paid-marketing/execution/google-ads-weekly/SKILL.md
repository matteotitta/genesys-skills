---
name: google-ads-weekly
version: "1.1"
last_updated: 2026-07-30
author: genesys-growth
description: |
  Runs a weekly optimise-and-report cycle on a Google Ads search account. Pulls the account (via the read-only google-ads MCP, or a pasted CSV export when the API is not live), runs ten optimisation levers split by the data volume each needs, proposes a ranked change list, applies what the operator approves through the gated google-ads-write MCP, then drafts a Slack update and a cycle record. Levers: search-terms negatives, budget pacing, impression share, conversion health, structure drift (weekly); keyword performance, CPC discipline, RSA assets, Quality Score (28-day). Every write is gated by google-ads-spend.md. Triggers: "Google Ads weekly", "run the Google Ads optimisation", "weekly paid search update", "add negatives". NOT for LinkedIn (use /paid-ads-report), one-off account audits (/paid-ads-audit), or writing ad copy (/google-ads-copy).
goal: Run one weekly cycle that reads a Google Ads account, proposes ranked changes with their volume floors stated, applies the approved ones, and drafts the client update.
outcome: A ranked change list the operator approves, the approved mutations applied and read back, a Slack-ready weekly update, and a dated cycle record in the client's paid/execution/ folder.
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
  - google-ads
  - google-ads-write
triggers:
  slash_commands:
    - /google-ads-weekly
  natural_language:
    - "Google Ads weekly"
    - "run the Google Ads optimisation"
    - "weekly paid search update"
    - "add negative keywords"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Google Ads Weekly — optimise-and-report cycle

Reads a Google Ads search account, proposes a ranked change list, applies what is approved, and drafts the weekly client update. Optimise first, report second: the report describes what changed, not just what happened.

## Doctrine inherited

- **[`google-ads-spend.md`](../../../../rules/google-ads-spend.md)** gates every write. Preview before mutate, confirm before spend, deletes refused, 200-mutation batch cap, read back after writing. Non-negotiable.
- **[`pii-redaction.md`](../../../../rules/pii-redaction.md)** applies to search-terms data, which is free text people typed into a search box and routinely carries names, employers and phone numbers.
- **[`output-simplicity.md`](../../../../rules/output-simplicity.md)** caps the Slack update. It is a skim artifact for senior readers, so one screen, not a metrics dump.

## When to use

Use it for the weekly cycle on a live Google Ads search account where you hold at least read access.

Do not use it for:
- LinkedIn Ads → `/paid-ads-report`
- A one-off, deep, 45-check account audit → `/paid-ads-audit`
- Writing or refreshing ad copy → `/google-ads-copy`
- Shopping, Performance Max or Demand Gen accounts. The levers here assume search.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Client slug | yes | Resolves the workflow binding, e.g. `ClientCo` |
| Account data | yes | Either the `google-ads` MCP, or a pasted/CSV export. Both are first-class. |
| Client workflow file | recommended | `{client}/workflows/google-ads-weekly.md` carries the account's targets, structural guards and Slack format |
| Campaign strategy | recommended | The intended structure, so the cycle can detect drift |

**The export path is not a fallback.** When the API is not live, or access is read-only, or the token is still Test tier, the cycle runs identically off a pasted export and simply skips Phase 3.

## Process

### Phase 0 — Ground

Read the client workflow file, the paid strategy doc, and `goals/` for targets. Establish: the conversion action being optimised for, the monthly budget, the intended campaign structure, and the reporting bar. Never invent a target. If the target is an unfilled placeholder, say so in the output rather than substituting a benchmark.

### Phase 1 — Pull

Run the queries in the premium reference against the **read** server, or parse the pasted export. Persist the raw pull to the client's `paid/execution/` and keep only a summary in context, per `context-management.md`.

Redact PII from search terms before the data is stored or shared.

### Phase 2 — Propose

Run the ten levers in the premium reference. For each finding, produce: the lever, the evidence, the proposed change, the tier it falls in under `google-ads-spend.md`, and **the volume behind it**. Rank by expected impact on cost per conversion.

State the floor next to every verdict. A keyword with 4 clicks and no conversions is not a loser, it is unmeasured. Say that rather than proposing a pause.

Output the change list and stop. The operator approves before anything applies.

### Phase 3 — Apply

Only after approval, and only for approved items. Follow the gate: soft-tier items may share one approval after being itemised, hard-tier items are confirmed individually, deletes are refused. Cap at 200 mutations.

After the batch, re-read the affected resources through the **read** server and confirm each change landed. Report anything that did not.

Skip this phase entirely when running from an export, or when access is read-only.

### Phase 4 — Report

Produce two artifacts:

1. **The Slack update** in the client's format. One screen. What changed, what it means, what needs a decision.
2. **The cycle record** at `{client}/paid/execution/MMYY-NN-google-ads-cycle.md`: the pull summary, the full change list with approved/rejected status, what was applied and verified, and the hypothesis for next week.

Then append a `run` entry to the client's `history.md` and refresh `latest.md`.

**Nothing posts to a client channel unprompted.** The Slack update is a draft for review.

## Known limitations

State these rather than working around them:

- **Auction insights is not available in the Google Ads API.** Lever 4 (is a competitor bidding on our brand terms) cannot be automated. It is a manual check in the Google Ads UI, and the cycle flags it as a to-do rather than silently dropping it.
- **Quality Score is only meaningful on keywords with impressions.** Keywords below the impression threshold return null, not a low score. Do not report nulls as failures.
- **Search-terms data is sampled and lagged.** Recent days under-report. Never draw a conclusion from the most recent 2 days alone.
- **Conversion lag.** A conversion action with a long lookback will under-report the last week. Compare like windows, and say which window was used.

## Anti-patterns

- ❌ Proposing a pause on a keyword below the volume floor. That is optimising noise.
- ❌ Reporting a cost-per-conversion verdict for a single week on a small account without its floor stated.
- ❌ Applying a batch and reporting success from the write server's own response. Read it back.
- ❌ Bundling a budget increase into a soft-tier negatives approval.
- ❌ Adding a competitor's terms to another competitor's campaign because the data looked good.
- ❌ Posting the Slack update without the operator seeing it.
- ❌ Dumping the full search-terms table into the update. Synthesise, persist the rest.
- ❌ Substituting an industry benchmark when the client's own target is missing. Flag the gap.

## Final ship gate

Run `/premortem --output` before ship. See `.claude/skills/meta/orchestration/premortem/SKILL.md` for the 5 execution domains and output template.

For the Slack update specifically, also run the `output-simplicity.md` §10 pre-ship check: right length for a senior reader, no robot tells, sources placed correctly for a client-team artifact.

