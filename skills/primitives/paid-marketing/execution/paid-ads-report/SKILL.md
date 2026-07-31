---
name: paid-ads-report
version: "1.0"
last_updated: 2026-07-01
author: genesys-growth
description: |
  Renders a brand-bound week-over-week LinkedIn Ads performance report from the linkedin-ads MCP: KPI cards (spend, impressions, CTR, CPC, CPM, frequency, engagements, conversions, conv rate, cost/conversion, audience penetration), campaign + creative tables, an audience-demographics breakdown (job function / seniority / industry / company size / country), a daily trend, an auto-insight narrative ("spend up 22%, CPL down 9% WoW"), and a day-of-week read. Rendered via /dashboard, bound to DESIGN.md tokens (no hardcoded colors). Reads the MCP's free analytics tools only — never a write tool. Triggers: "LinkedIn ads report", "paid report", "WoW ads report", "monthly LinkedIn Ads report", "how did the ads do this week". NOT for auditing existing campaigns (use /paid-ads-audit) or building strategy (use /paid-campaign-strategy).
goal: Render a brand-bound week-over-week LinkedIn Ads report from live MCP data, opening with an auto-insight narrative.
outcome: A single-page /dashboard-rendered report — KPI cards with WoW deltas, campaign + creative tables, demographics breakdown, daily trend, an auto-insight paragraph and weekday read — routed to the client's paid/execution/ folder, ready for /design-reviewer.
primitive: paid-marketing
sub_primitive: execution
ontology_type: dashboard
review_gate: 2
inputs:
  required: []
  recommended:
    - brand-kit
    - paid-campaign-strategy
depends_on: []
owned_by_agent: paid
mcps_used:
  - linkedin-ads
triggers:
  slash_commands:
    - /paid-ads-report
  natural_language:
    - "LinkedIn ads report"
    - "weekly paid ads report"
    - "monthly LinkedIn Ads report"
    - "how did the ads do this week"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Paid Ads Report — brand-bound WoW LinkedIn Ads report

Turn the `linkedin-ads` MCP's live analytics into a single-page, on-brand week-over-week report. Reads spend / CTR / CPL / demographics / trend via the MCP's free read tools, computes the WoW deltas, writes a three-sentence "what changed and why" opener, and renders the whole thing via `/dashboard` bound to the client's DESIGN.md tokens. The reader gets the story first, the tables second.

**Adapted from** `danielpopamd/linkedin-ads-mcp`'s `generate-dashboard.ts` + `compare_performance`/`get_daily_trends` (MIT) via 0726 /steal — see [`.claude/discovery/0726-linkedin-ads-mcp-steal-analysis.md`](../../../../discovery/0726-linkedin-ads-mcp-steal-analysis.md) (items M4 + M6). The upstream renders a stock HTML file; this renders a Genesys-branded report through `/dashboard`.

---

## Doctrine inherited

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets (the auto-insight opener IS the SQCA lead).
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — single-page report discipline (30–40 lines of narrative + the visual); length by reader.
- [`quantitative-evidence-floors.md`](../../../../rules/quantitative-evidence-floors.md) — a WoW delta is a verdict only above the volume floor. "Spend up 22%, CPL down 9%" on thin volume gets the "too early" caveat, not a crown.
- [`design-production.md`](../../../../rules/design-production.md) — DESIGN.md token contract + banned visual patterns (no gradient text, no generic drop shadows, ≤2 font weights, one accent).
- [`linkedin-ads-spend.md`](../../../../rules/linkedin-ads-spend.md) — **read tools only**. This skill never calls a write tool. If a write is ever needed, it's a separate gated action, not part of the report.
- [`storage-policy.md`](../../../../rules/storage-policy.md) + [`pii-redaction.md`](../../../../rules/pii-redaction.md) — ads data is client-confidential; route to the client folder, never commit raw exports or the rendered dashboard to git.

---

## When to use

- A client (or Genesys) wants a recurring — weekly or monthly — LinkedIn Ads performance report.
- You want the WoW story, not a raw metrics dump.

**When NOT to use:** auditing campaign health / structure → `/paid-ads-audit`. Planning budget/targeting → `/paid-campaign-strategy`. Writing ad copy → `/linkedin-ads-copy`. A one-off "what's my CTR" question → just call the MCP read tool directly.

---

## Inputs

| Input | Role |
|---|---|
| `linkedin-ads` MCP (authenticated) | Data source. Dormant until credentialed — see `.claude/mcp/linkedin-ads/README.md`. Until then, validate against the premium reference. |
| Account ID + reporting window | The account to report on; window defaults to the last complete week vs the prior week (WoW), with a 90-day daily trend. |
| DESIGN.md (brand-kit) | Token frontmatter (colors, typography). Recommended — falls back to the Genesys kit if the client has none. Cite tokens, never hardcode hex. |
| `--client {slug}` | Routes output to `projects/consulting/active/{slug}/paid/execution/` and triggers the client brand-kit lookup. |

---

## Process

1. **Resolve account + window.** `list_ad_accounts` → pick the account. Window = last complete week (period B) vs prior week (period A) for WoW; 90-day range for the trend.
2. **Pull data (read tools only).** In parallel: `get_campaign_performance` + `get_creative_performance` (period B), `get_campaign_groups`, `get_audience_demographics` across the 5 pivots (job function / seniority / industry / company size / country), `get_daily_trends` (DAILY, 90d), `compare_performance` (TIME_PERIOD, week B vs week A). Never a write tool.
3. **Compute derived metrics.** CTR, CPC, CPM, frequency, engagement rate, conversion rate, cost-per-conversion, audience penetration. Prefer the MCP's native fields; compute only what's missing. Never invent a figure (`financial-data.md`).
4. **Write the auto-insight opener (M6).** For each headline metric, if `|WoW Δ| > 10%`, emit one sentence ("Spend up 22%, CPL down 9%, CTR flat"). Name the top 2–3 movers by campaign. Add the day-of-week read (best/worst weekday by CTR from the trend). This paragraph leads the report — 3 sentences, no jargon.
5. **Render via `/dashboard`.** Bind to DESIGN.md tokens. Single page: insight paragraph → KPI row (with WoW arrows) → daily trend → campaign table → creative table → demographics. Respect the design budgets (one accent, ≤2 weights, no banned patterns).
6. **Route + protect.** Save the report + rendered artifact to `{client}/paid/execution/MMYY-linkedin-ads-report.md`. Ads data is client-confidential — don't commit the raw dashboard/exports to git (the clone already gitignores `dashboard.html`).

---

## Report structure

| Section | Shows |
|---|---|
| **Headline** (opener) | 3-sentence auto-insight: top movers + WoW direction + the day-of-week read |
| **KPIs** | Spend, Impressions, CTR, CPC, CPM, Frequency, Engagements, Eng rate, Conversions, Conv rate, Cost/Conv, Audience penetration — each with the WoW arrow + % |
| **Trend** | 90-day daily line (impressions / clicks / spend / conversions) |
| **Campaigns** | Per-campaign table, sorted by spend, with the full KPI set |
| **Creatives** | Per-creative table (headline, format, CTR, conv, video completion) |
| **Demographics** | Top job functions / seniorities / industries / company sizes / countries by engagement |

---

## Auto-insight thresholds (M6)

- **Movement sentence:** metric enters the opener only if `|WoW Δ| ≥ 10%`. Below that, "flat".
- **Direction language:** spend/CPC/CPM/CPL up = worded as cost; CTR/conv-rate/engagement up = worded as gain.
- **Top movers:** name the 2–3 campaigns with the largest absolute spend Δ or CPL Δ.
- **Weekday read:** best + worst weekday by CTR across the trend window (from `get_daily_trends` weekday averages).
- **Below the volume floor:** if a metric's denominator is under the floor (`quantitative-evidence-floors.md` — e.g. <~1,000 impressions, <3 conversions, before a full attribution window), the mover sentence carries a "too early" caveat instead of a verdict, even when the % delta is large. A 40% CPL swing on 5 conversions is noise, not a win.

---

## Design cycle (post-authoring phases)

After the happy-path render, walk these before ship. Each references the shared design-quality library at `../../../meta/catalog/design-reviewer/the premium reference. Run `/design-reviewer` as the final ship-ready gate.

- **Layout** — one accent, clear KPI hierarchy, tables scannable (`layout-*`).
- **Distill** — cut every metric the reader doesn't act on; the opener carries the story (`distill-*`).
- **Typeset** — ≤2 font weights, tabular numerals for the metric columns (`typeset-*`).
- **Cognitive load** — ≤7±2 KPI cards visible at once; group the rest (`cognitive-load-*`).
- **Polish** — WoW arrows read green/red by direction-of-good, not raw sign (`polish-*`).
- **Final review** — run `/design-reviewer` (5 dimensions × 0–4, P0–P3 severity).

---

## Anti-patterns

- ❌ Calling any write tool. This skill reads only; writes are a separate gated action per `linkedin-ads-spend.md`.
- ❌ Hardcoded hex / fonts — bind to DESIGN.md tokens.
- ❌ A wall of tables with no story — the auto-insight opener leads.
- ❌ Inventing a figure the MCP didn't return — mark `[UNAVAILABLE]`, never guess.
- ❌ Committing the rendered dashboard or a raw export to git — client-confidential, client folder only.
- ❌ Reporting a raw metric dump for an exec reader — length by reader per `output-simplicity.md`.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template. Then run `/design-reviewer` as the final visual gate — review-gate 2 is the floor for a client-facing report.
