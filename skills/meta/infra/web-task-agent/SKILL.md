---
name: web-task-agent
version: "1.0"
last_updated: 2026-06-08
author: genesys-growth
description: |
  Runs a plain-language web task as a multi-step browser loop on MCPs already mounted (Chrome DevTools + Firecrawl). Two v1 modes — monitor (watch a page for changes, report a grounded diff) and QA (walk a site, check CTAs/links/schema, screenshot mismatches). Carries browser-use's loop discipline as prompt patterns: pre-done verification, soft loop nudges, action chaining, ground-every-claim-in-observed-content. Client-agnostic tool for any engagement or Genesys-internal motion. Triggers: /web-task, "monitor this page for changes", "QA the CTAs on this site", "watch this competitor page", "check what changed on [url]". NOT for: building or cloning sites (use /website-build, /website-clone), one-shot scraping (use Firecrawl directly), pre-built LinkedIn scraping (use Apify skills), or form-filling / login-walled automation (deferred to v2).
goal: Run a plain-language web task as a multi-step loop on existing MCPs, grounded entirely in observed page content.
outcome: A grounded web-task report — a monitor diff or a QA findings list — sourced only from observed content, ready to feed competitor or website work.
primitive: meta
sub_primitive: infra
ontology_type: runbook
review_gate: 2
inputs:
  required: []
  recommended:
  - competitor-research
- type: web-task-report
  feeds_into:
  - competitor-research
depends_on: []
- competitor-research
owned_by_agent: operator
mcps_used:
- chrome-devtools
- firecrawl
triggers:
  slash_commands:
  - /web-task
  natural_language:
  - monitor this page for changes
  - watch this competitor page
  - QA the CTAs on this site
  - check what changed on
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# /web-task-agent — plain-language web task → multi-step loop

Run a web task as a multi-step browser loop on MCPs you already pay for. No new runtime, no API double-billing, no new always-on MCP. Two v1 modes: **monitor** (watch a page, report a grounded diff) and **QA** (walk a site, check CTAs/links/schema, flag mismatches).

## Provenance

Adapted from browser-use (github.com/browser-use/browser-use, MIT, © 2024 Gregor Zunic) per `/steal` analysis (2026-06-08) — see [`.claude/discovery/0626-browser-use-steal-analysis.md`](../../../../discovery/0626-browser-use-steal-analysis.md). We lift the **loop discipline** (pre-done verification, soft loop nudges, action chaining, ground-every-claim) as prompt patterns. We do **not** import the library — the loop runs on Chrome DevTools + Firecrawl MCPs already mounted. That call is the verdict's central KILL: the library duplicates our stack and adds a second Chromium + paid LLM keys.

## What this is / is not

A thin orchestration skill: it wraps existing MCPs with a disciplined loop. Client-agnostic — invoke for any engagement or Genesys-internal motion.

| Use this when | Use something else when |
|---|---|
| Watch a page and report what changed | Build/clone a site → `/website-build`, `/website-clone` |
| Walk a site checking CTAs / links / schema | One-shot scrape of one URL → Firecrawl directly |
| A repeatable multi-step web task on existing MCPs | LinkedIn engager/profile/job scraping → Apify skills |
| | Open-web research → Exa per exa-protocol.md |
| | Form-filling / login-walled automation → deferred to v2 |

---

## Triggers

**Invoke when the user says:**
- `/web-task <url> <what to do>`
- "monitor this page for changes" / "watch this competitor page"
- "QA the CTAs on this site" / "check every link on [url]"
- "check what changed on [url] since last time"

**Do NOT invoke when:**
- The job is building or cloning a site (`/website-build`, `/website-clone`)
- A single `firecrawl_scrape` answers the question (no loop needed)
- The data lives behind a login or needs form submission (v2 — refuse for now, name the reason)
- A pre-built Apify actor already covers the source (LinkedIn, job boards)

---

## Ethics guardrails (read FIRST)

This skill drives a browser against live sites. Treat as a Gate-2 check — confirm intent before any run that touches a third party, and log the answer.

**Legitimate uses:** monitoring publicly-visible competitor pages; QA on a site the user owns or is engaged to work on; reading public content the site's robots policy permits.

**Refuse if:** the task targets login-walled or paywalled content without authorization; it scrapes a source whose ToS prohibits automated access; it impersonates a user; or it would submit forms / create accounts on a third party. When in doubt, ask before proceeding.

No credential automation in v1. The skill never logs in, never submits forms, never stores cookies.

---

## Inputs

**Required:**
- `target_url` — the page or site to act on (publicly accessible)
- `task` — plain-language description of what to do ("watch the pricing page", "check every CTA goes somewhere live")

**Recommended:**
- `mode` — `monitor` | `qa` (inferred from the task if omitted)
- `baseline` — for monitor mode, the prior captured state to diff against (a previous run's report)
- `competitor-research` output — for monitor mode, to know which pages matter

---

## MCP credit gate

This skill calls **Firecrawl** and **Chrome DevTools**. Per `.claude/rules/apify-credits.md` (and the firecrawl analogue), state spend before running:

| Operation | Cost | Gate |
|---|---|---|
| `firecrawl_scrape` (capture one page) | low (~$0.01) | none — run, report cost |
| `firecrawl_monitor_create` (persistent watch) | per-check + storage | soft — confirm before creating a persistent monitor |
| Chrome DevTools navigate / snapshot / screenshot | no credit cost | none |
| Multi-page QA sweep (>10 pages) | scales with page count | hard — show page count + estimate, wait for yes |

Never create a persistent `firecrawl_monitor` or run a >10-page sweep without confirming first. Probe one page before any fan-out (per `goal-driven-loops.md`).

---

## Modes (v1)

### Monitor mode — watch a page, report a grounded diff

1. Capture current observable state (`firecrawl_scrape` markdown, or Chrome DevTools snapshot for JS-heavy pages).
2. Diff against the baseline (prior run's captured state). If no baseline, this run *is* the baseline — capture and stop.
3. Reason about what changed and why it matters ("CTA moved from 'Get started' to 'Book a demo'; a fourth pricing tier appeared at $X").
4. Report only changes grounded in the two captures. No speculation about intent beyond what the text shows.

### QA mode — walk a site, flag mismatches

1. Get the page set (sitemap, or the URLs the user named).
2. For each page: navigate (Chrome DevTools), check the named targets — CTA destinations resolve, links are live, schema/meta present.
3. Screenshot any mismatch.
4. Report findings as a list: page → check → pass/fail → evidence.

### Deferred to v2 (do not attempt in v1)

Gated-directory harvesting, form-filling, login-walled extraction. These carry the highest flake + legal risk. Refuse with a one-line reason and point to the v2 note.

---

## The loop discipline (the stolen core)

Every mode runs the same disciplined loop. Full protocol → the premium reference. The four load-bearing rules:

1. **Pre-done verification.** Before declaring done: re-read the task, list every requirement, check each against what you actually observed, and confirm with evidence. Any unmet requirement → not done.
2. **Ground every claim in observed content.** Each statement in the report traces to a specific capture (a scrape, a snapshot, a screenshot). No claim the page didn't show.
3. **Soft loop nudges.** If the same action repeats with no new information ~3 times, or the page state is unchanged across steps, stop and change approach — don't grind.
4. **Action chaining.** Page-changing actions (navigate, click) go last in a step; safe reads (scrape, snapshot, extract) chain freely.

---

## Anti-hallucination guardrails

1. **No claim the capture didn't show.** If it's not in the scrape/snapshot/screenshot, it doesn't go in the report.
2. **No invented diffs.** A "change" requires two captures showing it. Without a baseline, report current state only — never a fabricated delta.
3. **No assumed intent.** Report what changed, not why the competitor "must be" doing it, unless the page states it.
4. **No silent page drops.** If a QA sweep skips pages (timeout, block), name them in the report — don't imply full coverage.

---

## Composition with other skills

| Stage | Skill | Why |
|---|---|---|
| Before monitor | `/competitor-research` | Names which competitor pages are worth watching |
| After monitor | `/competitor-research` | A flagged change feeds the next competitor refresh |
| After QA | `/website-audit` | QA findings feed the broader site audit |
| Different job | `/website-clone`, `/website-build` | Build/clone, not watch/check |

---

## Completion report

When done, output:
- Mode run (monitor / QA) + target
- For monitor: baseline date, current date, the grounded diff (or "no change")
- For QA: page count checked, pass/fail per check, screenshots of mismatches
- Pages skipped + why (if any)
- MCP spend incurred

---

