---
name: product-pulse
version: '1.0'
last_updated: 2026-05-05
author: genesys-growth
description: 'Produces a single-page (30-40 lines) daily or weekly product pulse report — Headlines / Usage / System Performance / Followups — that measures progress against the locked product strategy. Pulls metrics from connected MCP data sources (PostHog, Mixpanel, Amplitude, Datadog, Sentry, Stripe, GSC, etc.) and pairs quantitative with at least one qualitative user signal. Triggers: "product pulse", "daily metrics", "pulse report", "how is X performing". Required upstream: strategy-doc (defines the metrics to measure). Feeds ship-learnings + strategy-doc refresh. NOT for marketing dashboards (use /dashboard) or analytics deep-dives (use data:analyze).'
goal: Produce a single-page disciplined pulse report that measures the locked strategy's metrics and surfaces drift early.
outcome: Produces a 30-40-line pulse report with Headlines / Usage / System Performance / Followups sections, citing at least one user conversation per cycle (K3 quant+qual rule), and feeding both strategy-doc refreshes and ship-learnings.
primitive: product-management
sub_primitive: audit
ontology_type: product-pulse
review_gate: 1
inputs:
  required:
  - strategy-doc
  recommended: []
- type: product-pulse
  feeds_into:
  - ship-learnings
  - strategy-doc
depends_on:
- strategy-doc
- ship-learnings
- strategy-doc
owned_by_agent: product-manager
mcps_used:
- gsc
- posthog
- mixpanel
- amplitude
- stripe
- datadog
- sentry
- gdrive
- notion
triggers:
  slash_commands:
  - /product-pulse
  natural_language:
  - "product pulse"
  - "daily metrics"
  - "pulse report"
  - "how is X performing"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: medium
---

# Product pulse — single-page metrics report

Produce a daily or weekly pulse report that measures the locked product strategy's metrics. Adapted from `/ce-product-pulse` in [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT).

The pulse closes the strategy↔pulse↔ship loop: strategy declares metrics, pulse measures them, learnings flow back to strategy refreshes.

## When to run

Invoke when the user says:
- "Run product pulse for [product]"
- "Daily pulse"
- "Weekly pulse"
- "How's [product] doing?"
- Cron-scheduled (default: 8am daily — via the `/schedule` skill or Trigger.dev cron)

Do NOT invoke when:
- User wants a marketing dashboard → `/dashboard`
- User wants a deep analytics investigation → `data:analyze`
- User wants a competitive analysis → `/competitor-research`
- No locked `strategy-doc` exists for the product → run `/strategy-doc` first; pulse is meaningless without locked metrics

## Inputs

**Required:**
- Locked `strategy-doc` (defines the metrics this pulse measures)
- Product name / ship slug

**Optional but valuable:**
- MCP connections: PostHog / Mixpanel / Amplitude (usage), Datadog / Sentry / Logfire / Honeycomb (system perf), Stripe / Paddle (revenue), GSC (search), custom DB read replicas
- Latest user conversation / interview note (for the K3 qualitative pairing)
- Previous pulse for delta comparison

**If MCP connection missing for a metric:** flag the data gap explicitly; don't fabricate a number. Per `.claude/rules/financial-data.md` — never invent metrics.

## Steps

1. **Phase 1 — Load locked strategy.** Read `strategy-doc` (the upstream dependency). Extract the metrics section. These are what we measure.
2. **Phase 2 — Pull metrics.** Query each MCP for the named metrics. Compare to previous period (default 7 days). Flag anomalies (>20% delta or threshold cross).
3. **Phase 3 — Pull system signals.** Query infra MCPs (Datadog / Sentry / etc.) for errors, latency, regressions.
4. **Phase 4 — Pull qualitative.** Find at least one user conversation, support ticket, or interview note from the period. If none: flag as a data gap and suggest a user call.
5. **Phase 5 — Compose pulse.** Apply 4-section structure. Apply 30-40 line discipline. Cut anything that doesn't move strategy thinking.
6. **Phase 6 — Self-roast.** Run checks below.
7. **Phase 7 — Push.** GDoc / Notion + Slack notification (if cron-scheduled).

## MCP credit gate

This skill calls free / read-only operations on PostHog / Mixpanel / Amplitude / GSC / Datadog / Sentry / Stripe MCPs. None spend credits. Confirm with the user only if connecting a new MCP for the first time.

## Self-roast (run before push)

- [ ] All 4 sections present (Headlines / Usage / System Performance / Followups)
- [ ] Total line count 30-40 (cut if longer; anything over 40 is dilution)
- [ ] Every metric in pulse traces to a metric in the locked `strategy-doc`
- [ ] Anti-vanity-metrics rule applied (K2): no page views / impressions / MAU without conversion
- [ ] At least one qualitative signal present (K3): quoted user / ticket / interview
- [ ] Anomalies flagged (>20% delta) — with a 1-line interpretation, not just "X went up"
- [ ] Each followup has an owner + suggested next step (not just "look into this")
- [ ] No fabricated numbers — data gaps flagged explicitly per `financial-data.md`

# {Product} pulse — {YYYY-MM-DD}

**Period:** {start} → {end} · **Strategy ref:** {strategy-doc path/version}

## Headlines
- {metric}: {value} ({±%} vs {prev}) — {1-line interpretation}
-...

## Usage
- {metric_1}: {value} ({±%}) — {note}
-...

## System Performance
- {error rate / latency / uptime} — {note}
-...

## Followups
- **{problem}** (owner: {name}) — {next step}. *User signal: "{quote}" — {source}*
-...
```

## Composition rule reference

Pulse is the measurement node in the **PM closed loop** (P3). See [.claude/rules/pm-loop.md](../../../../../rules/pm-loop.md). Cron pattern (P8): schedule via the `/schedule` skill or Trigger.dev cron.

## Attribution

Adapted from [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) v3.5.0 (MIT). Source pattern: `/ce-product-pulse`. Single-page discipline: P4 from /steal Phase 4.

