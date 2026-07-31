---
name: dashboard
version: '1.0'
last_updated: 2026-03-09
author: genesys-growth
description: 'Generates self-contained React dashboard applications from structured data, with pre-built templates for financial,
  competitive landscape, content performance, and pipeline visualizations. Produces a deployable React app with charts, filters,
  and data refresh capability. Chains with /vibe-coding as build engine and Xero MCP for financial data. Triggers: "/dashboard
  [type]", "build me a dashboard", "visualize this data", "create a reporting dashboard", "I need a dashboard showing". NOT
  for simple charts — use a spreadsheet. NOT for Google Sheets — use create-gdrive. NOT for static reports — use a document
  skill.'
goal: Generates self-contained React dashboard applications from structured data, with pre-built templates for financial,
  competitive landscape, content performance, and pipeline visualizations.
outcome: Generates self-contained React dashboard applications from structured data, with pre-built templates for financial,
  competitive landscape, content performance, and pipeline visualizations. Produces a deployable React app with charts, filters,
  and data refresh capability. Chains with...
primitive: design
ontology_type: dashboard
review_gate: 2
inputs:
  required: []
  recommended: []
- type: dashboard
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used:
- gdrive
- xero
triggers:
  slash_commands:
  - /dashboard
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# /dashboard — Build persistent data dashboards

Turn raw data into a reusable React dashboard. Instead of throwaway analysis, produce persistent visualization tools that can be refreshed with new data. Pre-built templates for common GTM use cases.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`design-production.md`](../../../../rules/design-production.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (dashboard is client-team review surface — DESIGN.md cites inline for build QA; rendered dashboard has no source frames), R3 (KPI labels capability-led), R6 (CTAs from dashboard nav → product-action for in-product variants, sign-up for market-facing), R9 (verb-led section + KPI names).

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "/dashboard [type]"
- "Build me a dashboard for..."
- "Visualize this data"
- "Create a reporting dashboard"
- "I need a dashboard showing..."

**Do NOT invoke when:**
- User wants a simple chart (just describe it or use a spreadsheet)
- User wants a Google Sheet (use `create-sheet.mjs`)
- User wants a static report (use a document skill)

---

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| Data source | Yes | File path (CSV/JSON), MCP query, or skill output reference |
| Dashboard type | No | `financial` / `competitive-landscape` / `content-performance` / `pipeline` / `custom` |
| Brand hub | No | Client brand hub file for branded colors, fonts, and data viz rules |
| Deploy target | No | `local` (default) / `lovable` / `vercel` |

---

## Dashboard Templates

### 1. Financial (`financial`)

**Data source:** Xero MCP (`list-profit-and-loss`, `list-invoices`, `list-payments`) or Wise CSVs
**Visualizations:**
- Revenue by client (bar chart, stacked monthly)
- MRR/ARR trend line
- P&L summary (income vs. expenses)
- Payment timeline (when invoices are paid)
- Client concentration risk (pie chart)

**Process:**
1. Pull data from Xero MCP or read Wise CSVs
2. Transform into dashboard-friendly JSON
3. Build React app with Recharts/Chart.js
4. Include date range filters and client toggles

### 2. Competitive Landscape (`competitive-landscape`)

**Data source:** Output from `/competitor-research` skill (comparison matrices, threat levels)
**Visualizations:**
- Feature comparison matrix (interactive table with color coding)
- Positioning map (2D scatter: price vs. capability)
- Threat level radar chart
- Market coverage heatmap
- Competitor timeline (funding, launches, pivots)

**Process:**
1. Read competitor research output files
2. Extract structured data (dimensions, scores, features)
3. Build React app with D3/Recharts
4. Include competitor toggle filters

### 3. Content Performance (`content-performance`)

**Data source:** Output from `/content-audit` skill or CSV export from analytics
**Visualizations:**
- Content inventory by type and status
- Topic coverage heatmap (topics vs. funnel stages)
- Publication frequency timeline
- Performance metrics (views, engagement, conversions)
- Gap analysis visualization

**Process:**
1. Read content audit output or analytics CSV
2. Categorize by topic, type, funnel stage
3. Build React app with interactive filters
4. Include search and sort capabilities

### 4. Pipeline (`pipeline`)

**Data source:** Funnel strategy output, CRM CSV, or manual data
**Visualizations:**
- Funnel visualization (stage counts and conversion rates)
- Stage duration distribution
- Win/loss rate by source
- Pipeline velocity trends
- Revenue forecast projection

### 5. Custom (`custom`)

**Data source:** Any structured data (CSV, JSON)
**Process:**
1. Analyze the data shape (columns, types, relationships)
2. Suggest appropriate visualizations
3. Ask user to confirm/adjust
4. Build the dashboard

---

## Design integration — DESIGN.md + shadcn + recharts

**Upstream contract:** This skill consumes the client's DESIGN.md file at `projects/consulting/{client}/brand/{MMYY}-brand-kit.md`. The dashboard renders in the client's brand: shadcn primitives for UI chrome (`<Card>`, `<Tabs>`, `<Button>`), recharts for data viz styled with brand colors.

**What this skill reads:**
- `colors.*` — chart palette: primary for the main series, secondary/tertiary for additional series, neutral for axes/gridlines, error for negative deltas
- `typography.*` — title/headline tokens for dashboard headers, label-sm for axis labels and legends
- `rounded.*` — card and chart container radii
- `spacing.*` — gap between metric cards, dashboard section margins, chart inner padding

**Web rendering pipeline (same as `/vibe-coding`):**

```
DESIGN.md tokens → app/globals.css (CSS vars) → tailwind.config.ts (utilities)
                                                                  ↓
                                          shadcn primitives + recharts theming
                                                                  ↓
                                                    Branded React dashboard
```

**Recharts theming:**
- Pass token-derived hex values to recharts `<Line stroke>`, `<Bar fill>`, `<Pie cell>`, `<Area fill>` props
- Reference colors via CSS variables in styled components: `var(--primary)`, `var(--secondary)`
- Axis labels and tooltips inherit `var(--font-sans)` and `var(--on-surface)`
- Chart containers wrap in shadcn `<Card>` for consistent surface styling

**Forbidden:**
- Default recharts colors (cyan/orange/green palette) — always brand-derived
- Hardcoded chart colors in component code — always CSS vars or token-derived constants
- Custom card/tab/button equivalents — use shadcn primitives

**Required:**
- Cite DESIGN.md path in the dashboard project README
- Apply the brand's "Do's and Don'ts" — one primary color per dashboard surface (use it for the most important metric only)

**Authority:** Full integration contract in `.claude/rules/design-production.md` (auto-loaded). When in doubt, that file wins.

**If no DESIGN.md exists:** pause and recommend running `/brand-kit` first. Do not invent tokens.

---

## Build Process

### Step 1: Data preparation

Read and validate the data source:
- CSV → Parse headers, detect types, handle missing values
- JSON → Validate structure, identify nested objects
- MCP → Execute queries, transform responses
- Skill output → Read markdown tables or structured sections

### Step 2: Architecture

Generate a React app structure:
```
dashboard/
├── src/
│ ├── App.tsx # Main app with routing
│ ├── data/ # Transformed data as JSON
│ ├── components/ # Chart components
│ ├── hooks/ # Data loading and filtering
│ └── styles/ # Tailwind or styled-components
├── package.json
├── vite.config.ts
└── README.md # Data refresh instructions
```

### Step 3: Component selection

Based on data shape and dashboard type, select chart components:
- Bar charts → Comparisons across categories
- Line charts → Trends over time
- Pie/donut → Composition/proportion
- Scatter → Correlation between two variables
- Tables → Detailed data with sorting/filtering
- Heatmaps → Two-dimensional density
- Radar → Multi-variable comparison

### Step 4: Build via /vibe-coding

Hand off to the `/vibe-coding` skill with a detailed specification:

```
Build a React dashboard app with these requirements:
- Framework: Vite + React + TypeScript
- Charts: Recharts (or Chart.js)
- Styling: Tailwind CSS
- Data: {inline JSON or file path}
- Components: {list of chart components needed}
- Filters: {date range, category toggles, search}
- Branding: {colors from gdrive-config.json if client specified}
```

### Step 5: Data refresh instructions

Generate a README explaining how to refresh the data:
- For Xero: which MCP commands to run and how to export
- For CSVs: where to get the updated file
- For skill output: which skill to re-run

---

## Client Branding

When `--client` is specified, pull brand colors from `.claude/mcp/gdrive/gdrive-config.json`:

```javascript
// Example: ClientCo branding
{
  "primaryColor": "#1a1a2e",
  "secondaryColor": "#16213e",
  "accentColor": "#0f3460",
  "font": "Inter"
}
```

Apply to: chart colors, header background, accent elements, font family.

---

## Design cycle (post-authoring phases)

Dashboards are data-dense by definition — Cognitive load is **always-on** for this skill (not conditional). Run the full phase walk before ship. Each phase references `../../meta/catalog/design-reviewer/the premium reference.

- **Layout** — `layout-tenets.md` (rhythm, density budget; dashboards push 8–15 components per viewport)
- **Distill** — `distill-principles.md` (every chart earns its place)
- **Typeset** — `typeset-principles.md` (tabular nums for numeric data)
- **Polish** — `polish-principles.md` (interaction states for filters, sortable columns)
- **Harden** — `harden-checklist.md` (empty states, loading skeletons matching chart shape, error states for failed data fetches)
- **Cognitive load** — `cognitive-load-tenets.md` *(always-on for dashboards: ≤7±2 visible options per decision, progressive disclosure, recognition over recall)*
- **Delight** — `delight-patterns.md` (custom empty states; restraint matches B2B SaaS context)
- **Onboarding** — `onboarding-patterns.md` (empty-state-with-tutorial as first-run experience)
- **Final review** — run `/design-reviewer`

## Notes

- Start with the simplest visualization that answers the question — don't over-engineer
- Financial dashboards MUST use real data from Xero MCP or Wise CSVs (never fabricated)
- Competitive landscape dashboards work best after running `/competitor-research` first
- The `/vibe-coding` skill handles the actual app creation — this skill focuses on data transformation and specification
- For quick one-off visualizations, consider a Google Sheet instead (faster, no build step)

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
