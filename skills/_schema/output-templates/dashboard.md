---
knowledge_type: dashboard
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Meta"
schema_version: 1
render_targets: []
canonical_render: app
---

# Dashboard — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Specification for a data-visualization application. **The artifact is an app**, not a Doc — `render_targets: []` (intentionally empty). The skill output is a SPEC that `/vibe-coding` consumes to build the actual React/Next app at `app_path`.

## Required frontmatter fields

```yaml
client: {slug}                       # or "genesys" for internal dashboards
skill: dashboard
version: 1
status: draft                        # draft | review | locked (when v1 built)
generated: {YYYY-MM-DD}
ontology_type: dashboard
dashboard_type: financial | competitive-landscape | content-performance | pipeline | custom
data_sources:                        # ≥1 entry
  - source: {CSV path | MCP query | skill-output ref}
    detail: {what data}
    refresh_method: manual | scheduled | live-query
metrics_displayed:                   # ≥1 entry, exactly one flagged primary
  - name: {metric name}
    source_mcp: {MCP that provides this data — e.g., GSC, Apollo, Xero}
    visualization: line | bar | sparkline | scorecard | table
    format: number | currency | percent | duration
    primary: false                   # flag exactly one as true
refresh_cadence: manual | daily | weekly | monthly
target_persona: {who reads this — e.g., "Genesys CEO", "Client CMO"}
framework_target: next | react | vibe-code   # which framework the vibe-coding build uses
app_path: {path}                     # projects/apps/{name}/ or projects/consulting/active/{client}/apps/{name}/
design_md_ref: {path}                # DESIGN.md per design-production.md
deploy_target: vercel | local | client-tenant
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

**Locking gate:** `status: locked` requires the app to exist at `app_path` with v1 built and approved.

## Required body sections (in order)

1. **Overview** — persona, use case, primary metric in 3 sentences
2. **Data sources** — table: source, detail, refresh method per source
3. **Metrics** — list with H3 per metric; identify primary metric explicitly
4. **Filters and interactions** — what user can filter / drill into / hover
5. **Architecture** — data flow diagram (sources → transform → presentation)
6. **Branding contract** — DESIGN.md tokens consumed; shadcn primitives used; recharts theming; forbidden patterns (no custom Button/Card; no hardcoded hex)
7. **Refresh runbook** — becomes the app's README on how to refresh data
8. **Acceptance checklist** — pre-locked checklist (data verified, primary metric prominent, refresh tested, mobile-readable, design tokens applied)

## Optional body sections

- **Future metrics** — v2/v3 additions
- **Comparison context** — when dashboard compares periods or cohorts
- **Alerts / thresholds** — when dashboard surfaces alerts (high churn, low conversion)

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Meta-tier requires ≥40% verified.

**Financial dashboards** inherit `financial-data.md` strict-non-fabrication rule — every number tagged with source (Xero MCP, Wise CSV path, etc.); no estimated financial data.

Sections requiring tags:
- Data sources (each source: existence + access path + refresh method verified)
- Metrics (each metric definition: where the number comes from, transform rules)

## Render rules per target

### gdrive (Doc) — N/A

Dashboard SPEC may be reviewed in a Doc, but the canonical artifact is the app. The Doc would just duplicate the spec markdown.

### gdrive (Slides) — N/A
### gdrive (Sheet) — N/A

### notion (Page render — optional thin pointer)

When stakeholders need a Notion link to the dashboard:
- Overview paragraph + screenshot of the live dashboard
- Refresh runbook in a toggle
- Link to `app_path` repo + `deployed_url`
- **Never duplicates the dashboard data** — Notion is just a pointer

### Special — dashboard renders as app

Push pipeline divergence: `push.dispatch({skill, schemaType: 'dashboard'})` short-circuits and:
1. Validates spec locally (frontmatter + sections + design_md_ref resolves)
2. Hands spec to `/vibe-coding` skill (build engine)
3. Vibe-coding produces app at `app_path`
4. If `deploy_target: vercel`, push.toVercel adapter handles deploy
5. Returns `{success, app_path, deployed_url}` instead of `{url, manifestLine}`

Manifest line points to deployed URL (not Drive doc URL).

## Validation rules

1. All required frontmatter fields present
2. `dashboard_type` enum check
3. `data_sources` ≥1 entry
4. `metrics_displayed` ≥1 entry; **exactly one flagged `primary: true`**
5. `framework_target` and `app_path` mandatory
6. `design_md_ref` resolves to existing DESIGN.md (else fails until `/brand-kit` runs)
7. **Financial dashboards:** every metric must cite Xero MCP or Wise CSV (no fabricated numbers per `financial-data.md`)
8. **`render_targets:` MUST be `[]`** — no Doc/Notion render
9. recharts mandatory for visualization (or documented alternative)
10. shadcn primitives only (no custom Button/Card/Tab — per `design-production.md`)
11. `refresh_cadence` mandatory

## Examples in the wild

- `.claude/skills/primitives/design/dashboard/SKILL.md` is the spec generator
- Phase 4 will produce conforming examples during rollout
