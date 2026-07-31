---
name: deepline-enrich
version: '2.2'
last_updated: 2026-05-05
author: genesys-growth
description: Enriches prospect lists with emails, phones, and company data via waterfall across 15+ providers. Validates email
  addresses before outbound campaigns using ZeroBounce and BetterContact. Runs pre-built enrichment plays (email waterfall,
  account mapping, CRM hygiene, etc.). Enforces credit gate before batch runs to prevent accidental spend. Produces enriched-prospect-list
  and validated-email-list outputs that feed into outreach-emails, abm-campaign, niche-signal-discovery, and linkedin-social-selling.
  Consumes CSV exports from clay-search, build-tam, or other discovery tools. Triggered by "enrich this list", "waterfall
  enrichment", "validate emails", "batch enrich", "run a play", or "Deepline". NOT for people discovery (use /clay-search
  or /build-tam), ICP scoring (use /icp-behavioural or /abm-campaign), or buying signals (use /niche-signal-discovery).
goal: Enriches prospect lists with emails, phones, and company data via waterfall across 15+ providers.
outcome: Enriches prospect lists with emails, phones, and company data via waterfall across 15+ providers. Validates email
  addresses before outbound campaigns using ZeroBounce and BetterContact. Runs pre-built enrichment plays (email waterfall,
  account mapping, CRM hygiene, etc.). Enforces credit gate...
primitive: outbound
sub_primitive: enrichment
ontology_type: company-context
review_gate: 1
inputs:
  required: []
  recommended:
  - clay-search
  - icp-research
  - company-context
- type: enriched-prospect-list
  feeds_into:
  - outreach-emails
  - abm-campaign
  - linkedin-social-selling
  - niche-signal-discovery
- type: validated-email-list
  feeds_into:
  - outreach-emails
depends_on: []
- abm-campaign
- linkedin-social-selling
- niche-signal-discovery
- outreach-emails
owned_by_agent: researcher
mcps_used:
- apollo-io
- clay
- deepline
- gdrive
- notion
triggers:
  slash_commands:
  - /deepline-enrich
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: max
---

# /deepline-enrich — Waterfall enrichment + email validation

Enrich prospect lists across 15+ data providers (Apollo, Hunter, PDL, Prospeo, Icypeas, ZeroBounce, BetterContact, etc.). Deepline runs a waterfall — first provider to return a valid result wins. Typically finds 20-40% more emails than any single provider.

**Imported via:** `/steal` analysis of https://code.deepline.com (2026-03-31). Phase F upgrade: Play patterns + credit gate (2026-04-04). Apify waterfall slot added 2026-05-01.

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in deepline-enrich |
|---|---|---|
| **R1** | Source placement (three layers) | Enrichment output is **internal-reference** (CSV feeding downstream outbound). Provider attribution stays inline per row (which provider returned the match) — auditability matters for source-quality forensics. |
| **R3** | Product-update tone | Skill-summary reports (cost per row, fill rate per provider) frame as "the run shipped X" not "we're thrilled to announce." Internal voice stays operator-direct. |
| **R9** | Action-oriented section names | "Run the waterfall / Validate the emails / Hand off to outbound" — verb-led. Preserve. |

Note: this skill is internal-reference only; R2/R5/R6/R7/R8 do not apply (no customer-facing surface).

---

## Prerequisites

- **Deepline CLI:** `curl -s "https://code.deepline.com/api/v2/cli/install" | bash`
- **Python 3.10+** required (macOS ships 3.9 — install via `brew install python@3.13`)
- **Node.js 20+** required (already met)
- **BYOK keys configured:** Run `deepline quickstart` to connect existing provider API keys

---

## Credit gate — voice-locked

ALWAYS run before any enrichment over 5 contacts. This is the load-bearing safety mechanism preventing accidental spend.

### Pre-execution checklist

```
1. ESTIMATE cost: deepline enrich --input file.csv --dry-run
2. CHECK balance: deepline billing --balance
3. CONFIRM with user: "This will cost ~$X for N contacts. Proceed?"
4. SET spending cap: deepline billing --set-monthly-limit [amount]
```

### Gate rules

| Batch size | Gate level | Action |
|------------|-----------|--------|
| 1-5 contacts | No gate | Run immediately, show cost after |
| 6-50 contacts | Soft gate | Show estimate, proceed unless user objects |
| 51-200 contacts | Hard gate | Show estimate, wait for explicit "yes" |
| 201+ contacts | Full gate | Show estimate + balance + monthly cap, wait for explicit approval |

### Cost reference

| Operation | Approx. cost per contact |
|-----------|------------------------|
| Email waterfall (BYOK) | Free (you pay providers directly) |
| Email waterfall (managed) | ~$0.10/credit |
| Phone enrichment | ~$0.15-0.25/credit |
| Company enrichment | ~$0.05-0.10/credit |
| Email validation | ~$0.03-0.05/credit |
| Full contact enrichment | ~$0.30-0.40/credit |

**Key:** Deepline charges only on successful matches. Failed lookups don't consume credits.

### Pilot mode — ALWAYS test first

Before any batch, test on 2 rows:

```bash
deepline enrich --input prospects.csv --output test.csv \
  --with email=person_search_to_email_waterfall:{"title":"{{title}}","company":"{{company}}"} \
  --rows 0:1
```

Review output. If results look right, run the full batch.

Apollo-side credit gate also applies per `.claude/rules/apollo-credits.md`. Apify-slot calls flow through `.claude/rules/apify-credits.md`.

---

## When to use which enrichment tool — voice-locked

| Tool | Use when | Strengths |
|------|----------|-----------|
| **Deepline CLI** | Waterfall enrichment across providers, email validation, batch CSV | Multi-provider fallback, cost visibility, 20-40% better coverage |
| **Apollo MCP** (`mcp__apollo-io__*`) | Quick single-contact lookup, company / people search | Integrated in conversation, no CLI needed |
| **Clay MCP** (`mcp__claude_ai_Clay__*`) | Company enrichment at known companies, Claygent research | Integrated in conversation, AI research via Claygent |

**Rule of thumb:** Deepline = MAXIMUM EMAIL COVERAGE across a list. Apollo MCP = quick lookups. Clay MCP = company-level enrichment + AI research.

**Handoff pattern:** `/clay-search` (discover) → `/deepline-enrich` (enrich + validate) → `/outreach-emails` (write sequences)

---

## Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Prospect CSV** | Rows with name + title + company + domain | `/clay-search`, `/build-tam`, manual |
| **CRM export** | Existing contact list (CRM hygiene plays) | HubSpot / Salesforce / Attio |
| **LinkedIn URL list** | URL-only inputs (Apify slot fallback) | Sales Nav exports, Phantombuster scrapes |
| **Email addresses** | For validation or reverse-enrichment | Existing list |

---

## Process

**Standard waterfall flow:** dry-run → pilot (2 rows) → full batch → email validation → filter to `valid`. Multi-stakeholder play (~30% win rate vs ~5% single-threaded) and quarterly CRM hygiene play (30% job-change rate per year) follow the same gate discipline. Full commands + workflows + provider configuration in the premium reference.

**Apify waterfall slot** for LinkedIn-URL-only inputs (`dev_fusion/Linkedin-Profile-Scraper` $10/1k or `apimaestro/.../no-cookies` $5/1k) also documented in the premium reference.

---

## Plays

22 pre-built enrichment plays organized by input type: Email Finding (6), People Finding (6), Validation & Scoring (3), CRM Hygiene & Job Changes (4), Outbound Integration (3). Decision tree + per-play input/output/cost in the premium reference.

---

## Quality

Pre-execution checks cover cost discipline (dry-run + cap + user confirmation), pilot discipline (2-row test before full batch), input quality (column normalization, dedupe), and output quality (validation step ran, valid/catch-all/invalid segmented). Common-mistakes table (no dry-run, skipped validation, using Deepline for discovery) + worked example (250-row $38 estimate) + anti-examples + quality gate (≥75% find rate, ≥80% valid, ≤$0.20/validated, ≤2% bounce) in the premium reference.

**Hit-rate gate (proceed/stop) — added 2026-05-05 via /steal from Andytoizer/agentoperator-outbound-engine:**
- **`valid` + `catch_all` together = hit.** Most deliverable catch-all domains accept real emails even when the provider can't verify the exact mailbox. Treating catch_all as a miss undercounts deliverable coverage by ~15-25% in B2B SaaS lists.
- **80% combined hit rate is the proceed/stop gate.** If `(valid + catch_all) / total < 0.80`, stop before proceeding to research/drafting. Below 80% means upstream is broken: domains malformed, LinkedIn URLs stale, or waterfall providers misconfigured. Don't waste research and drafting time on contacts you can't email.
- **If you need stricter (valid only), override explicitly** in the play config — but document why in `goals/MMYY-NN-cycle.md` so the next operator knows the gate was tightened.

---

## Handoff Patterns

| From | To | What passes |
|------|----|-------------|
| `/clay-search` | `/deepline-enrich` | Raw prospect CSV |
| `/build-tam` | `/deepline-enrich` | TAM list with account + contact data |
| `/deepline-enrich` | `/niche-signal-discovery` | Enriched list for signal overlay |
| `/deepline-enrich` | `/outreach-emails` | Validated email list |
| `/deepline-enrich` | `/abm-campaign` | Scored + enriched account list |
| `/deepline-enrich` | Sequencers | Push to Instantly / Lemlist / HeyReach / Smartlead |

---

## Integration with the engagement workflow

Assigned to the **Researcher** role-agent. Slots into:
- **Sales pipeline:** "discovery prep" — auto-enrich prospects before discovery calls
- **New-client onboarding:** No direct role (research phase uses company-context, not contact enrichment)
- **Outbound:** Core enrichment step after target list build

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

