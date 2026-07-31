---
name: technographics-from-website
version: '1.0'
last_updated: 2026-05-18
author: genesys-growth
description: |
  Detects which vendor (CRM, platform, back-office system) a lead uses by analysing their public website — visual tells via screenshot vision extraction, plus optional HTTP probe verification against vendor portal subdomain patterns. Produces a per-lead technographic-signal output: detected vendor(s), confidence per vendor, verification status, visual evidence, and outbound-copy hook templates. Vendor-agnostic at the skill layer; per-vendor profiles (visual tells + optional HTTP verifiers) live in the premium reference Triggers: "find firms using ClientCo", "technographic qualification", "score these leads by CRM fit", "detect vendor usage from website", "which CRM does this lead use". Feeds into /lead-scoring (technographic dimension), /niche-signal-discovery (10th category), /outreach-emails (vendor-specific hooks), /abm-campaign (tier by CRM fit). NOT for company firmographics (use /company-context), NOT for tech-stack scraping of JS dependencies (use Apollo via /company-context), NOT for people discovery (use /clay-search).
goal: Detect vendor usage on lead websites via screenshot vision + optional HTTP verifier; produce per-lead technographic signals with verified outbound-copy hooks.
outcome: A per-lead technographic-signal output (detected vendor, confidence, verification status, evidence, outbound hooks) ready to feed lead-scoring as the technographic dimension or outreach-emails as personalization input.
primitive: outbound
sub_primitive: list-building
ontology_type: lead-assessment
review_gate: 2
inputs:
  required: []
  recommended:
  - icp-research
  - lead-scoring
- type: technographic-signal
  feeds_into:
  - lead-scoring
  - niche-signal-discovery
  - abm-campaign
  - outreach-emails
depends_on: []
- abm-campaign
- lead-scoring
- niche-signal-discovery
- outreach-emails
owned_by_agent: operator
mcps_used:
- chrome-devtools
- exa
- firecrawl
- gdrive
- notion
triggers:
  slash_commands:
  - /technographics-from-website
  natural_language:
  - "find firms using [vendor]"
  - "score these leads by CRM fit"
  - "technographic qualification"
  - "detect vendor usage from website"
  - "which CRM does this lead use"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: high
---

# /technographics-from-website — Detect vendor usage from a lead's website

Find out which back-office system, CRM, or platform a lead uses by analysing their public website. Visual extraction is the primary signal (screenshots fed to vision model identify login button labels, footer logos, embedded widget branding, "powered by" mentions). HTTP-probe verification is the optional confidence booster where the vendor has a discoverable portal subdomain pattern (e.g., `*.mypfp.co.uk` for ClientCo Personal Finance Portal).

Vendor-agnostic at the skill layer. Per-vendor profiles live in the premium reference and define the visual tells, optional HTTP verifier, and outbound-copy hook templates for each vendor universe.

**Research stack (Exa):** primary tools `web_fetch_exa`, `web_search_exa` for customer-list discovery. Chrome DevTools MCP for screenshot capture. Firecrawl as fallback. All per `.claude/rules/exa-protocol.md`.

**Imported via:** `/steal` analysis 2026-05-18 (`.claude/discovery/0526-ClientCo-pfp-fingerprint-steal-analysis.md`) — abstracted from the ClientCo PFP HTTP-probe technique into a vendor-agnostic visual + verifier skill.

---

## When to use this vs. other skills — voice-locked routing

| Skill | Question it answers |
|-------|--------------------|
| `/clay-search` or `/build-tam` | **Who** should we target? (People discovery) |
| `/deepline-enrich` | **How** do we reach them? (Emails, phones) |
| `/niche-signal-discovery` | **When** should we reach out? (Timing + intent) |
| `/lead-scoring` | **How ready** are they? (Qualification + prioritisation) |
| **`/technographics-from-website`** | **Which vendor do they use?** (Technographic signal) |
| `/company-context` | **Who are they?** (Firmographics + traction) |
| `/outreach-emails` | **What** do we say? (Personalised sequences) |

**Handoff pattern:** `/clay-search` or `/build-tam` (lead list) → `/technographics-from-website` (vendor signal overlay) → `/lead-scoring` (consume signal as technographic dimension) → `/outreach-emails` (use vendor-specific copy hook).

---

## Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Lead URLs** | List of company website URLs to analyse | `/clay-search`, `/build-tam`, FCA register, CRM export |
| **Vendor profile path** | Reference file defining the vendor universe to detect | the premium reference |
| **ICP context** *(recommended)* | For filtering thin matches | `/icp-research` upstream |

**Vendor profile shape** (see the premium reference for worked example):

- **Vendor name + brand spellings** — "ClientCo" / "Intelligent Office" / "IO"
- **Visual tells** — text strings, logo descriptions, button labels, footer mentions that the vision model looks for
- **Optional HTTP verifier** — URL pattern + expected response (e.g., `https://{slug}.mypfp.co.uk/` → HTTP 200 confirms ClientCo PFP tenant)
- **Outbound-copy hook template** — the "we integrate with X" snippet pre-filled

---

## 5-phase workflow

Full details in the premium reference. Summary:

1. **Capture** — for each lead URL, screenshot the homepage + `/clients` or `/login` sub-pages via `mcp__chrome-devtools__take_screenshot`. Firecrawl as fallback when Chrome DevTools fails.
2. **Extract** — feed screenshot to Claude vision; ask "which of these visual tells appear?" against the vendor profile. Return per-vendor confidence (high/medium/low/none) + cited evidence (verbatim text or visual description).
3. **Verify** *(optional, per vendor profile)* — if vision identifies a candidate vendor AND the vendor profile defines an HTTP verifier, follow the public link pattern (e.g., visit the lead's `/clients` page, find their "Client login" link, HTTP-probe the destination subdomain). HTTP 200 = confirmed; non-200 = unconfirmed (visual signal stands).
4. **Score** — combine visual confidence + verifier outcome into a single per-vendor confidence. Verified = HIGH; visual-only + medium-vision = MODERATE; visual-only + low-vision = WEAK. No tells found = NO_SIGNAL.
5. **Output** — produce structured per-lead record (see Output schema below).

---

## Composition with `/lead-scoring` — dimension contract

The technographic-signal output feeds `/lead-scoring` as input to its Phase 1 fit assessment (the "technographic" dimension already exists in the premium reference of `/lead-scoring`) AND as a Phase 2 signal category.

Mapping documented in the premium reference. Short version:

| Technographic-signal field | Maps to `/lead-scoring` field |
|---|---|
| `confidence: HIGH (verified)` | technographic-fit: STRONG (evidence: verified vendor signal) |
| `confidence: MODERATE (vision-only)` | technographic-fit: MODERATE |
| `confidence: WEAK` | technographic-fit: WEAK |
| `NO_SIGNAL` | technographic-fit: [UNAVAILABLE] |
| Verified vendor matches client's integration list | Signal: "technographic-fit-match" (STRONG recency, drives SALES routing) |

---

## Anti-hallucination guardrails

1. **Never invent visual tells.** Quote verbatim text from the screenshot or describe the visual element specifically. Mark `[UNAVAILABLE]` when the vision model can't see a tell rather than guessing.
2. **Never claim verification without an HTTP response.** If the HTTP probe wasn't run, mark `result: NOT_ATTEMPTED` — don't conflate visual signal with verified signal.
3. **Cite the screenshot.** Every claim needs the screenshot reference (`screenshot_001_homepage.png` + sub-region) so a reviewer can audit.
4. **Respect vendor-profile boundaries.** The skill only detects vendors defined in the loaded vendor profile. "I see a CRM but don't know which one" = `vendor: unknown` not a fabricated guess.
5. **Don't escalate weak signals to SEND_VENDOR_SPECIFIC.** WEAK confidence routes to SEND_GENERIC outbound; vendor-specific hooks fire only on MODERATE+ with verification preferred.

---

## Credit gates

This skill calls Chrome DevTools (local browser, no per-call cost), Exa (per `.claude/rules/exa-protocol.md`, uncapped), and optionally Firecrawl (per Firecrawl usage limits — soft gate at >100 URLs/run).

| Batch size | Gate level | Action |
|---|---|---|
| 1-10 leads | No gate | Run immediately |
| 11-50 leads | Soft gate | Show estimate (~10 sec/lead screenshot + vision), proceed unless user objects |
| 51-200 leads | Hard gate | Show estimate (~10-30 min total), wait for explicit approval |
| 200+ leads | Full gate | Suggest Trigger.dev wave-batch per `orchestration-patterns.md`→ Wave-batch |

Vision calls use the standard Claude model — no Anthropic API spend (uses the user's Claude Code plan). Per `.claude/rules/approval-loop-pattern.md`, prompt-tuning rounds always use Agent tool, not paid API.

---

## Quality checks (pre-delivery)

- [ ] Every lead has at least one screenshot captured (or `[UNAVAILABLE: capture failed, reason X]`)
- [ ] Every detected vendor has visual evidence quoted or specifically described
- [ ] Every verified vendor has HTTP response status cited
- [ ] No detected vendor was added beyond those in the loaded vendor profile
- [ ] `recommended_action` aligns with confidence + signal_quality (no SEND_VENDOR_SPECIFIC on WEAK)
- [ ] Output routes correctly per `Push` section below
- [ ] If batch >50: cost estimate shown and user approved

---

## Anti-patterns

- ❌ Running this skill without a vendor profile — no detection target = noise output. Always load a profile first.
- ❌ Using this skill for generic tech-stack detection (JS libraries, analytics tools) — Apollo + BuiltWith cover that lane via `/company-context`.
- ❌ Treating WEAK confidence as actionable. WEAK = mention vendor only in nurture; never pre-arm a cold email with it.
- ❌ Skipping the verifier step when the vendor profile defines one. Visual-only is cheaper but verifier-confirmed signals justify aggressive outbound; skipping the verifier downgrades the signal you could have had.

---

## Integration with the engagement workflow

Assigned to the **Operator** role-agent (specialist: gtm-engineer for the actual run). Slots into:
- **Context refresh:** Quarterly technographic refresh on active target accounts
- **Outbound:** Technographic overlay step between list-building and signal-discovery
- **Sales pipeline:** Pre-call technographic confirmation for warm prospects

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

