---
name: company-cfo
version: '1.0'
last_updated: 2026-07-08
author: genesys-growth
description: 'Monthly CFO close for Genesys Growth (single-director UK Ltd, GBP base) — pull cash + revenue from Xero (read-only) with Wise CSVs as historical cross-reference, categorize and reconcile, compute end-of-month cash via the transaction-sum method, update a forward scenario projector, and write the monthly snapshot leadership uses for runway, hiring, and director-drawing decisions. Modes: monthly (default close), weekly (thin cash pulse), scenario (ad-hoc forecast), pickup (resume prior run). Read-only against Xero; bound by financial-data.md (never fabricate figures) + pii-redaction.md. Triggers: monthly close, company finances, cash position, CFO report, financial scenario, cash runway, monthly financials, cash pulse, runway forecast, "run the CFO snapshot".'
goal: Produce the monthly company CFO snapshot — reconciled EOM cash, categorized cash flows, and a forward runway projection — from Xero and Wise source data.
outcome: A dated monthly snapshot in projects/genesys/goals/ — TL;DR status, cash in/out by category, reconciled EOM cash via transaction-sum, revenue metrics, and 1-3 forward scenarios — unblocking leadership runway, hiring, and director-drawing decisions and feeding next month's reconciliation.
primitive: ops
sub_primitive: execution
ontology_type: financial-report
review_gate: 3
inputs:
  required: []
  recommended: []
- type: financial-report
depends_on: []
owned_by_agent: operator
mcps_used:
- xero
- gdrive
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# company-cfo — monthly company CFO workflow

The standing analysis leadership (Matteo) uses to make runway / hiring / director-drawing / spend decisions. Primary cadence is **monthly** — run on the 1st for the closed prior month. Weekly, scenario, and pickup modes cover the in-between.

Genesys Growth is a single-director UK Ltd (Genesis Growth Ltd, #14363665), GBP base currency, lumpy consulting revenue collected on monthly invoices through Wise + bank. Same discipline as the source skill (transaction-sum EOM, categorization traps, scenario modeling) applied to Genesys books on Xero.

## Data-integrity contract (binding — read before any run)

This skill touches **real financial data**. Accuracy is non-negotiable. It obeys two rules verbatim:

- **`.claude/rules/financial-data.md`** — NEVER fabricate, estimate, or hallucinate any figure, client name, amount, or date. **Xero MCP is the primary source of truth; Wise CSV exports are the secondary/historical cross-reference — these are the ONLY sources.** If both are unavailable or context is lost, **STOP and ask** ("I don't have access to the source data — connect Xero or share the CSVs"). Never reconstruct from memory. Apply the verified client-name mappings (Granular Insights → Clarisights, Powerplay → Cello, Helium → SmartPricing, 13740668 Canada Inc./Xplenty → Integrate, Simplyk → ClientCo, Octave Technolog → Voiceflow, Raised Networks → Nimbus) when parsing Wise `Source name` / `Target name`. Watch the red flags: any client list built without reading the source, any "approximate" figure, any two clients merged, any client not in source data → STOP.
- **`.claude/rules/pii-redaction.md`** — before any report is stored or shared, redact PII (end-client contact names, emails, account/sort-code numbers, IBANs). Keep the signal (client company, category, amount, deal context); mask the identity. The report lands in `projects/genesys/goals/` and may be pushed to GDrive — redact before both.

**Xero access is READ-ONLY.** This skill only ever calls: `list-bank-transactions`, `list-payments`, `list-invoices`, `list-profit-and-loss`, `list-accounts`, and the read reports `list-report-balance-sheet`, `list-trial-balance`, `list-aged-receivables-by-contact`, `list-aged-payables-by-contact`, `list-organisation-details`. It NEVER calls any `create-*` or `update-*` Xero tool. Xero is not a paid-credit MCP — reads are free — but the read-only boundary is a hard rule regardless.

## When to run / when NOT

Run when: "run the CFO snapshot", "monthly close", "where's our cash", "what's runway", "model hiring a contractor", "cash pulse". Do NOT run for: an ad-hoc single-number lookup (query Xero directly); tax filing or accounting treatment (refer to the accountant — this is operational cadence, not statutory accounts); fundraising projections (different discipline).

## Step 0 — Load context + prior run

Before any work, read in order:

1. **`.claude/rules/financial-data.md`** — the data-integrity guardrails above. This governs HOW figures are sourced.
2. **The most recent CFO report** in `projects/genesys/goals/` (e.g. `MMYY-cfo-monthly.md`) — last month's snapshot: what was decided, what stayed open, the categories in use.
3. **`projects/genesys/goals/0226-fy-analysis.md`** + **`goals/0226-scope.md`** — FY targets, pacing, prior full-year actuals for trend context.
4. **`projects/genesys/latest.md`** + **`history.md`** — running narrative: known anomalies, current client roster, churn state.

Do NOT assume continuity from memory or training data — always read the prior report + Xero first.

## Step 1 — Parse mode

| Invocation | Mode | Cadence |
|---|---|---|
| `company-cfo monthly` (default) | **monthly** | Once per month on the 1st, for the closed prior month |
| `company-cfo weekly` | **weekly** | Thin cash pulse — current cash + next 2 weeks of expected flows |
| `company-cfo scenario <question>` | **scenario** | Ad-hoc modeling in the projector |
| `company-cfo pickup` | **pickup** | Resume where the prior run left off |

Sections below walk **monthly** in detail. Weekly, scenario, and pickup are summarized at the end.

---

## Monthly workflow

Confirm with the user: **which month are we reporting on?** (Default: prior calendar month.) Then walk the phases, pausing to confirm before each.

### Phase 1 — Pull source data (Xero read-only + Wise)

For the target month:

| Source category | Xero read-only pull | Cross-reference |
|---|---|---|
| **Cash / bank balances** | `list-accounts` (bank accounts) + `list-report-balance-sheet` (as-at date) for reconciled cash-at-bank | Wise CSV `Source/Target amount (after fees)` in GBP |
| **Cash movements** | `list-bank-transactions` per bank account for the period | Wise CSV rows, `Finished on` in month |
| **Revenue collected** | `list-payments` (received) + `list-invoices` (issued vs paid) | Wise inflows by `Source name` (apply client-name mappings) |
| **Category / P&L view** | `list-profit-and-loss` for the month | — |
| **Receivables ageing** | `list-aged-receivables-by-contact` (who owes, how old) | — |

Wise CSVs live at `projects/genesys/goals/0226-wise-source-data/FY-*.csv` (FY-25-26 = current). The export schema is a Wise Business transfers file: `ID, Status, Direction, Created on, Finished on, Source name, Source amount (after fees), Source currency, Target name, Target amount (after fees), Target currency,..., Category, Note`. Use **GBP base-currency** amounts for all cash analysis (see the currency-mismatch trap).

**If Xero is unreachable** (401 / expired token): do not proceed on Wise alone silently — flag it, refresh Xero per `reference_xero_mcp_refresh.md`, and note in the report which figures are Wise-only vs Xero-reconciled. If both are unavailable → STOP and ask.

### Phase 2 — Categorize and reconcile

Bucket all cash outflows into the locked Genesys category set (see the premium reference for the full set + fiscal-year lock discipline). The core categories:

`revenue` (client fees, net of fees/FX) · `director-remuneration` (PAYE salary + dividends) · `team` (contractors/VAs + any payroll) · `software` (SaaS subscriptions — the tool stack) · `professional-services` (accountant, legal) · `taxes` (Corporation Tax, VAT, PAYE/NIC) · `other`.

Run the universal traps every month (full list in the premium reference):

- **Currency mismatch** — Wise multi-currency: clients pay in USD/EUR/GBP. Always use the **base-currency (GBP)** amount, never the counterparty-currency amount. Xero revalues foreign balances to GBP at period end (unrealized FX) — the FX revaluation line is a known reconciliation item, not a real cash flow.
- **Cash-vs-credit double-count** — do not count both a card autopay outflow AND the individual card charges. Pick cash accounts as the source of truth; treat the card as a debt account.
- **Internal transfers** — GBP↔USD↔EUR moves between Genesys's own Wise balances net to zero. Exclude them.
- **Taxes held vs paid** — VAT collected sits in cash until the quarterly payment; Corporation Tax accrues but leaves cash ~9 months after year-end. Categorize by when cash actually moves, and note reserves separately so runway isn't overstated.
- **Director-drawing check** — verify the expected monthly salary + any planned dividend actually went out. If a draw was deferred to preserve cash, flag it (don't read the absence as a cost decrease).

Cross-checks before writing: payments received in Xero ≈ Wise + bank inflows (within collection timing); P&L category totals ≈ summed bank-transaction categories (within cash-vs-accrual lag).

### Phase 3 — Compute EOM cash (transaction-sum method)

**Non-negotiable.** Full recipe in the premium reference. The discipline: never trust a single balance number — compute EOM two independent ways and reconcile to the penny.

```
# 1. From opening balance at period start (Xero balance-sheet as-at the start date),
# sum all signed bank movements (list-bank-transactions + list-payments applied to
# bank) for each cash account through date T:
# balance_at_T = opening_balance + sum(movements where date <= T)
# 2. Sanity check: balance_at_T must equal Xero's reconciled cash-at-bank on the
# balance sheet as at T (list-report-balance-sheet, date=T) — Xero's ledger is the
# authoritative reconciled figure, the role the bank API's available_balance plays
# in the source method. They must agree to the penny (allowing the flagged FX
# revaluation line for multi-currency Wise balances).
# 3. Independent cross-reference: sum Wise CSV rows (Finished on <= T, base-currency
# amount) for the Wise-held accounts. Must reconcile within known timing lag.
# 4. Month-over-month: prior-month EOM + this month's net cash change == this-month EOM,
# to the pound.
```

If the two computations do not reconcile, **STOP — do not ship**. Investigate: an unreconciled bank line in Xero, a missing account, FX revaluation, a paging/timeout on the transaction pull, a Wise transfer not yet in Xero. A silent reconciliation gap propagates into every downstream chart and forecast. (A ~$42K walkback error once ran for weeks in a production CFO workflow before a month-over-month check caught it — hence this method.)

### Phase 4 — Update the scenario projector

Update the forward projector that projects EOM cash N months out under adjustable assumptions (revenue growth, contractor hire, spend changes). Structure + reference implementation in the premium reference: trailing 3 closed months (HISTORICAL) → TODAY (actual cash) → Mo 1 (current month, partial) → Mo 2–7 (scenario settings apply). Each month: `starting + revenue − expenses = profit → ending`.

Update each run: append the just-closed month to HISTORICAL (drop the oldest); set `startingCash` to today's actual reconciled balance; refresh category baselines to **actuals, not safe estimates**; set `baselineRevenue` net of Wise/processor fees; verify presets still hold.

### Phase 5 — Write the snapshot report

Write `projects/genesys/goals/MMYY-cfo-monthly.md` (MMYY = reported month) per the output format below. Include the plain-English "why" paragraph — what happened this month vs last, with continuity ("the [client] churn from last month finished hitting collections in June"). Redact PII per the contract before saving.

### Phase 6 — Update running context

If any of these shifted, update `projects/genesys/latest.md` + append to `history.md`: client roster / churn, MRR-equivalent recurring revenue, director-drawing or comp change, a new cash-floor constraint, a new recurring cost. Replace stale facts; don't append indefinitely. Log a `[COST]` line to `history.md` if the run used a sized agent fan-out (per `cost-budget-discipline.md`).

### Phase 7 — Review + route (no git for raw data)

- **Raw exports never get committed.** Wise CSVs already live in the repo (they're the curated source); any *new* raw Xero dump or intermediate pull is financial PII — keep it out of git per `.claude/rules/storage-policy.md`. The committed artifact is the **redacted report only**.
- Route the report to `projects/genesys/goals/` (Genesys-internal financial home, alongside the FY analysis + Wise source data).
- Push to GDoc for review per `.claude/rules/gdrive-protocol.md` (`--client genesys-growth`) only after PII redaction.

---

## Weekly cash pulse mode

Thin — fits a 15-minute check.

1. Pull current reconciled cash (`list-report-balance-sheet` / `list-accounts`).
2. Pull last 7 days of movements + next 7–14 days of known outflows (salary, VAT/tax due, contractor invoices) and expected inflows (`list-aged-receivables-by-contact`).
3. Compute: current cash, next outflow (date + amount), next expected collection (date + amount).
4. Flag if cash < next 2 weeks of outflows (cash-floor watch — the floor applies to the intramonth LOW, not the EOM high).
5. One-line: `Cash £X | Next out £Y on <date> | Next in £Z on <date> | Floor: OK|WATCH|BREACH`.

Save to `projects/genesys/goals/MMYY-cfo-weekly-WW.md`. Pair with `/schedule` for a Monday-morning run.

## Scenario mode

Ad-hoc — "what if I bring on a £4K/mo contractor in September" or "what if a £6.5K client churns". Open the projector, adjust the knobs, capture the resulting cash curve. Save to `projects/genesys/goals/MMYY-cfo-scenario-{slug}.md`.

## Pickup mode

Resume the prior run. Surface: most recent monthly report + weekly pulse, the reported month's open items (), current-narrative from `latest.md`. Re-read the source before continuing — never assume continuity.

## Reconciliation self-roast (run before the report ships)

- [ ] Every figure traces to Xero or a Wise CSV — zero invented / "approximate" numbers.
- [ ] EOM computed two independent ways (transaction-sum vs Xero balance sheet) and they reconcile to the penny (FX revaluation line flagged, not silently absorbed).
- [ ] Month-over-month: prior EOM + net change == this EOM, to the pound.
- [ ] Client-name mappings applied to all Wise `Source/Target name` fields.
- [ ] Categories match last month's exactly (fiscal-year lock) — any change documented in the "why" paragraph.
- [ ] Currency: all amounts in GBP base; no counterparty-currency amounts leaked in.
- [ ] Tax reserves (VAT held, Corp Tax accruing) noted separately — runway not overstated.
- [ ] PII redacted before save + push.
- [ ] Any unreconciled gap → STOPPED and investigated, not shipped.

If any check fails, fix or STOP before the report ships. These data-integrity gates are the review gate for this skill.

# Genesys CFO snapshot — {Month YYYY}

## TL;DR
| Metric | This month | Prior | Δ |
|---|---|---|---|
| Net cash change | £… | £… | … |
| Ending cash (reconciled) | £… | £… | … |
| Recurring revenue | £… | £… | … |
| Runway (months at current burn) | … | … | … |
| Recommendation | {one line} | | |

## Cash in — by source
## Cash out — by category (director-remuneration / team / software / professional-services / taxes / other)
## Revenue metrics — active clients, recurring revenue Δ, recent churn (client + £)
## Tax + reserves — VAT held, Corp Tax accruing, PAYE
## Forward projection — 1-3 scenarios from the projector
## Recommended actions — concrete decisions for leadership
## Open items — to resolve next month
## Why — plain-English narrative of what moved and why
```

## Notes on quality

- **Never invent methodology or figures.** Trust Xero + Wise; if undocumented, ask — don't guess (`financial-data.md`).
- **Transaction-sum is non-negotiable.** Walkback from one balance snapshot has burned CFO workflows repeatedly. Compute two ways, reconcile, STOP on a gap.
- **Categorization discipline > precision.** Same categories every month = trend-readable. Lock for the fiscal year (Sep–Aug).
- **Baseline to actuals, not safe estimates.** A software line modeled at £600 when actuals run £900 makes optimistic projections that break.
- **Revenue is net of Wise/processor fees + FX**, not gross.
- **Cash floor applies to the intramonth LOW**, not the EOM high — consulting collections are lumpy; cash dips between invoice runs.
- **When numbers don't reconcile, stop.** Don't ship a report with an unexplained gap.

## Attribution

Adapts the transaction-sum EOM-cash method + scenario projector from [`coreyhaines31/makerskills/company-cfo`](https://github.com/coreyhaines31/makerskills) (MIT, © 2026 Corey Haines), accessed 2026-07-08. Re-tooled onto Xero MCP (read-only) + Wise CSVs; bound by financial-data.md + pii-redaction.md.

