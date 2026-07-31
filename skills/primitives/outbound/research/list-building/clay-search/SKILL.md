---
name: clay-search
version: '1.3'
last_updated: 2026-05-01
author: genesys-growth
description: Searches for people by domain, title, seniority, industry, location, and other LinkedIn filters via Clay (primary)
  and Apollo (secondary). Produces prospect lists exported to CSV, JSON, or SQLite for downstream outreach and enrichment.
  Feeds into outreach-emails and linkedin-social-selling. Triggered by "find contacts at", "search for people", "build outreach
  list", "Clay people search", "prospect discovery", "expand keyword search", or "Apollo people search". Consumes icp-research
  for targeting criteria. NOT for company enrichment or contact enrichment at known companies (use Clay MCP directly for that).
  NOT for company discovery (use /apollo-find-companies).
goal: Searches for people by domain, title, seniority, industry, location, and other LinkedIn filters via Clay (primary) and
  Apollo (secondary).
outcome: Searches for people by domain, title, seniority, industry, location, and other LinkedIn filters via Clay (primary)
  and Apollo (secondary). Produces prospect lists exported to CSV, JSON, or SQLite for downstream outreach and enrichment.
  Feeds into outreach-emails and linkedin-social-selling....
primitive: outbound
sub_primitive: list-building
ontology_type: lead-assessment
review_gate: 1
inputs:
  required: []
  recommended:
  - icp-research
  - company-context
- type: prospect-list
  feeds_into:
  - outreach-emails
  - linkedin-social-selling
depends_on: []
- linkedin-social-selling
- outreach-emails
owned_by_agent: sales
mcps_used:
- apollo-io
- clay
- deepline
- gdrive
- notion
triggers:
  slash_commands:
  - /clay-search
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# /clay-search — Bulk people discovery via Clay

Search for professionals using 50+ LinkedIn filters. Exports to CSV, JSON, or SQLite with automatic deduplication.

---

## When to use which Clay tool — voice-locked

| Tool | Use when | Strengths |
|------|----------|-----------|
| **Clay MCP** (`mcp__claude_ai_Clay__*`) | Company enrichment, contact enrichment at known companies, running subroutines, tracking events | Integrated in conversation, real-time enrichment |
| **autoclay CLI** (`clay people search`) | Broad people search across domains/industries, bulk discovery with 50+ filters, keyword expansion | Richer filtering, bulk output, deduplication |

**Rule of thumb:** Use Clay MCP when you know WHO or WHAT COMPANY. Use autoclay when you have CRITERIA and need to DISCOVER people.

### Clay MCP advanced tools (2026)

| Tool | What it does | GTM use case |
|------|-------------|--------------|
| `list_subroutines` | Discover all custom automations in your Clay workspace | Audit available automations |
| `run_subroutine_direct` | Execute custom functions directly with specific values (no search needed) | ICP fit scoring, personalization, signal detection |
| `run_subroutine` | Execute custom functions on search results | Chain enrichment → custom scoring → export |
| `run_subroutine_no_mapping` | Execute functions with automatic field mapping | Quick automation when field names match |
| `ask-question-about-accounts` | NL queries on Salesforce accounts (requires sync) | "Which accounts in EMEA have >500 employees and no open opp?" |
| `track-event` | Log analytics events for workflow optimization | Track which workflows produce best results |

**Claygent (via MCP):** Clay's AI research agent invoked through `run_subroutine_direct` for natural-language research (competitive research, ICP validation, personalization at scale). Powerful chaining: Clay enrichment → Firecrawl scraping → messaging tools.

**Deepline handoff:** After exporting from Clay, run `/deepline-enrich` for waterfall email enrichment across 15+ providers (20-40% more emails than Apollo alone). Flow: `/clay-search` (discover) → `/deepline-enrich` (waterfall + validate) → `/outreach-emails` (write).

---

## Filter guidance — voice-locked operational wisdom

These lessons come from real Clay API behaviour:

1. **Function filters are unreliable.** Clay's taxonomy frequently returns zero results despite matching records. Start with `--title-keywords` instead of `--functions`.
2. **Title keywords > inferred taxonomies.** `--title-keywords "VP Marketing,Head of Marketing"` is more reliable than `--seniority VP --functions Marketing`.
3. **Start broad, then filter.** Run a preview with minimal filters first. Add constraints only after you see what's available.
4. **Preview before committing.** Always run `--mode preview` before `--mode full`. Preview is free and shows you the result quality.
5. **Use keyword expansion.** `clay keywords expand "growth marketing"` reveals Clay's related terms — helps you cast a wider net.
6. **Combine title keywords with seniority for precision.** When you need specific levels: `--title-keywords "Marketing" --seniority "VP,Director"` works better than title keywords alone.

---

## CLI quick start

```
/Users/matteotittarelli/Library/Python/3.9/bin/clay
```

Session-based auth (23-hour cookie at `~/.autoclay/session.json`). No API key — uses Clay email/password. First run: `clay setup` or `clay auth login`. Full command reference + workflows in the premium reference.

---

## Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Filter criteria** | Domains, titles, seniority, country, company size, industry | User-provided / `/icp-research` upstream |
| **ICP context** | For filter calibration | `icp-research` recommended |
| **Output format** | CSV / JSON / SQLite | User specifies |

---

## Process

**Standard flow:** keyword expansion (free) → preview-mode search (free, max 50) → refine filters → full-mode export (credits) → handoff to `/deepline-enrich` for emails. Apollo runs as secondary when Clay results are thin. Apify slots A (bulk employees >10k rows) and B (name-disambiguation) for cost-optimization edge cases. Full commands + Apify slots + Apollo equivalents + workflows in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent results.** Report Clay/Apollo's actual return count.
2. **Don't fabricate LinkedIn URLs.** Apollo doesn't return them — mark as `[no LinkedIn URL]` and offer Slot B (name-disambiguation) if user wants resolution.
3. **Don't over-promise tech stack data.** Apollo has stronger tech stack filtering than Clay; surface that in output schema if used.
4. **Tag source per row.** `[Clay]` / `[Apollo]` for every merged row.
5. **Cost transparency.** Show preview-mode result before committing credits.

---

## Quality

Pre-delivery checks cover filter discipline (preview-first, title-keywords-over-functions), coverage (broad-then-narrow, Apollo for thin results, Apify for >10k seeds), and cost discipline (Apify + Apollo gates respected). Worked example (DACH PMM search) + anti-examples (full-mode without preview, function filters, over-filtering, Clay for bulk-employee runs) + quality gate (preview-first 100%, title-relevant ≥80%) in the premium reference.

---

## Credit Gates — voice-locked

| Action | Gate | Source |
|--------|------|--------|
| Clay full-mode search | Always preview first | `--mode preview` is free |
| Apollo enrichment overlay | Per-credit gate | `.claude/rules/apollo-credits.md` |
| Apify slot A (>10k bulk employees) | Estimate before run | `.claude/rules/apify-credits.md` |
| Apify slot B (name-disambiguation, >1k rows) | Estimate before run | `.claude/rules/apify-credits.md` |
| Deepline waterfall handoff | Use `/deepline-enrich` gate | Per that skill's matrix |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

