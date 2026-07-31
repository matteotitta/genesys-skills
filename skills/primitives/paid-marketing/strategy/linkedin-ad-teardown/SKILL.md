---
name: linkedin-ad-teardown
version: "1.0"
last_updated: 2026-07-14
author: genesys-growth
description: |
  Pull a competitor's live + recent ads from LinkedIn's public Ad Library and turn them into a strategy read — recurring themes, offers, ad formats, posting cadence, EU-disclosure targeting signals, and the gaps they're leaving open. Sources via our existing scrapers (Browser MCP free-first, then Firecrawl / Apify under the credit gates) — the Ad Library is public transparency data, never a login-gated member scrape. Bound to a competitor set; the first use is ClientCo vs its advice-tech rivals. Feeds /competitor-research with the paid-creative dimension it doesn't cover. Triggers: "LinkedIn ad teardown", "what ads is X running", "competitor ad library", "teardown [competitor] LinkedIn ads". NOT for our own account (use /paid-ads-audit) and NOT a full competitor profile (use /competitor-research).
goal: Produce a strategy read of a competitor's LinkedIn ads from the public Ad Library.
outcome: A per-competitor teardown — themes / offers / formats / cadence / targeting / gaps + the opening for the client — floored (no strategy from 2 ads), cited to Ad Library URLs, routed to the client's competitors/ folder, feeding /competitor-research.
primitive: paid-marketing
sub_primitive: strategy
ontology_type: competitor-intel
review_gate: 1
inputs:
  required: []
  recommended:
    - company-context
    - competitor-research
depends_on: []
owned_by_agent: paid
mcps_used:
  - firecrawl
  - apify
triggers:
  slash_commands:
    - /linkedin-ad-teardown
  natural_language:
    - "LinkedIn ad teardown"
    - "what ads is X running"
    - "competitor ad library"
    - "teardown their LinkedIn ads"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# LinkedIn Ad Teardown — competitor paid-creative strategy read

LinkedIn's Ad Library is public (it exists for ad transparency). This skill reads a competitor's ads from it and turns them into a strategy read: what themes and offers they're pushing, in what formats, how often, who they're targeting (from the EU "who's shown this" disclosure), and — the part that matters most — where the gaps are that the client can move into.

**Adapted from** `github.com/stan-default/liam`'s `liam-competitors` / `inspect_competitor_ads` (MIT), accessed 2026-07-14, via /steal — see [`.claude/discovery/0726-liam-steal-analysis.md`](../../../../discovery/0726-liam-steal-analysis.md). Concept port; the sourcing runs on our scraper stack, not Liam's Playwright engine.

---

## Doctrine inherited

- [`quantitative-evidence-floors.md`](../../../../rules/quantitative-evidence-floors.md) — no strategy read below the floor. State how many ads the read rests on.
- [`crawl-cost-discipline.md`](../../../../rules/crawl-cost-discipline.md) — free discovery first (the public Ad Library URLs), metered extraction only on the ads you keep.
- [`apify-credits.md`](../../../../rules/apify-credits.md) — if an Apify actor is used for bulk, gate it and estimate the cost first.
- [`storage-policy.md`](../../../../rules/storage-policy.md) + [`pii-redaction.md`](../../../../rules/pii-redaction.md) — the Ad Library is public transparency data (no member PII); route the teardown to `{client}/competitors/`, don't over-collect.

---

## Sourcing — public, gated, cheapest-first

The library lives at `https://www.linkedin.com/ad-library/` — searchable by advertiser, no login for the basic view. Source in this order:

1. **Browser MCP (free).** Navigate the public Ad Library, search the advertiser, read the results. The cheapest path — try it first.
2. **Firecrawl scrape (metered).** When the page is too JS-heavy to read cleanly via the browser.
3. **Apify LinkedIn Ad-Library actor (metered, gated).** Only for bulk across many competitors, and only after the `apify-credits.md` estimate + go-ahead.

Never scrape login-gated member data — the Ad Library only. It's transparency data, but stay polite (`crawl-cost-discipline.md`): respect rate limits, don't hammer.

---

## What to extract per competitor

- **Inventory** — how many active + recent ads (this is the count the whole read rests on — cite it).
- **Themes** — the recurring messages, value props, and pains they lead with.
- **Offers** — demos, trials, gated content, events, discounts; what the CTA asks for.
- **Formats** — single image / carousel / video / document / thought-leader ad.
- **Cadence** — from launch dates, the posting rhythm (steady drip vs burst).
- **Targeting signal** — from the EU disclosure ("who's shown this": roles, seniorities, countries) where present.
- **Gaps** — the formats, angles, and segments they're *not* running. This is the opening.

---

## The floor — voice-locked

**No strategy read below the floor.** Under ~5 ads, report the inventory only — not a "strategy." A competitor with 2 ads isn't a strategy you can reverse-engineer; it's two ads. State the count every time (`quantitative-evidence-floors.md`), and when the disclosure doesn't show targeting, mark it `[UNAVAILABLE]` — never infer who they're targeting from the creative alone.

---

## Anti-patterns

- ❌ Reading a strategy from 2 ads — inventory only below the floor.
- ❌ Scraping login-gated member data — Ad Library only.
- ❌ An ungated Apify bulk run — estimate + gate per `apify-credits.md`.
- ❌ Inferring targeting the EU disclosure didn't show — mark `[UNAVAILABLE]`.
- ❌ Design-cloning a competitor's creative — this is gap-finding + inspiration, not a copy job.

---

## Integration with other skills

- **Feeds `/competitor-research`** — the paid-creative dimension its 11-dimension profile doesn't cover.
- **Feeds `/paid-campaign-strategy` + `/linkedin-ads-copy`** — the gap becomes our angle.
- Pairs with [`a1-gallery-protocol.md`](../../../../rules/a1-gallery-protocol.md) when you want design references for the formats you spotted.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains + output template.

---

