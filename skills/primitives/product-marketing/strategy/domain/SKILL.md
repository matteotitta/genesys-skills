---
name: domain
version: '1.0'
last_updated: 2026-07-08
author: genesys-growth
description: 'Brainstorms and checks available.com domains for a new product, brand, or project — availability-first
  (work backwards from what is registrable, never fall in love with a name first). Runs on free RDAP + whois web lookups:
  budget → brainstorm combos → RDAP availability check → whois cross-check → aftermarket sweep → bucket → negotiate → then
  defer name research (USPTO trademark screen + social-handle checks) until after availability is confirmed. Triggers:
  find a domain, check domain availability, brainstorm domain names, is X.com available, what.com is available for X,
  domain hunt, name my product, aftermarket price on X.com, trademark check for a name. NOT for full brand identity (use
  brand-kit) or market positioning (use positioning).'
goal: Brainstorm and availability-check.com domain candidates for a new product or brand, working backwards from what is
  registrable and affordable rather than from a name already chosen.
outcome: 'A ranked domain shortlist: available-now candidates with registrar price, aftermarket-listed options under budget,
  and a top pick screened for trademark and social-handle conflicts — ready to register or negotiate.'
primitive: product-marketing
sub_primitive: strategy
ontology_type: domain-shortlist
review_gate: 1
inputs:
  required: []
  recommended: []
- type: domain-shortlist
depends_on: []
owned_by_agent: pmm
mcps_used:
- firecrawl
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# Domain shortlist — availability-first.com hunting

Brainstorm and check available `.com` domains for a new product, brand, or project. The whole method rests on one rule from Laura Roeder: **work backwards from what's actually available — don't fall in love with a name first.** A name you love with no registrable `.com` is a dead end; a name you find by checking availability first is a shortlist.

Defaults to `.com`. Only deviate (`.dev`, `.co`, `.io`, `.ai`) if the project is dev-tooling-only or the user asks.

## When to run

Invoke when the user says:
- "Find me a domain for [product]" / "What `.com` is available for [idea]?"
- "Is [name].com available?" / "Check domain availability for these"
- "Brainstorm domain names for [product]" / "Help me name my project"
- "What's the aftermarket price on [name].com?" / "Trademark check for [name]"

Do NOT invoke when:
- User wants a full brand identity (colours, logo, type) → `brand-kit`
- User wants market positioning or category → `positioning`
- User wants product/company naming strategy beyond the domain → treat naming as the deliverable, but the domain check is this skill

## The core principle — availability-first

The order is the deliverable. Most people pick a name, then discover the `.com` is gone or five figures, then compromise. This flow inverts that:

```
brainstorm → check what's registrable → filter to budget → THEN research the name
   (many) (RDAP, free) (drop the rest) (trademark + socials)
```

Trademark screening and social-handle checks are **deliberately deferred** until after availability and budget filtering. There's no point clearing a trademark on a name you can't register. See the premium reference for the full step-by-step.

## Genesys tooling — free web lookups

This skill is re-tooled onto free, web-native checks. No paid domain APIs and no registrar CLI are required.

| Job | Free tool (default) | Signal |
|---|---|---|
| Availability | RDAP over `curl` / WebFetch — `rdap.org/domain/{name}` | **404 = available · 200 = taken** |
| `.com` ground truth | RDAP authoritative registry — `rdap.verisign.com/com/v1/domain/{name}` | 404 = available · 200 = taken |
| Registrant + expiry | RDAP JSON `events`, or `whois` (CLI or WebFetch to a whois viewer) | dates, registrar, contact |
| Aftermarket sweep | Firecrawl scrape → click-through fallback | listed price / "make offer" |
| Trademark screen | Firecrawl scrape → USPTO click-through | Live exact-phrase match in class |
| Social handles | `curl` / WebFetch to `x.com/{h}`, `linkedin.com/company/{h}` | 404 = available |

**Paid tools are deferred, not required.** Domainr API (aggregated marketplace status), Namecheap API (year-1 promo pricing), and the Vercel CLI (`.com` check + buy) are optional cross-checks — use them only if the user already has the keys or CLI configured. The free RDAP + Firecrawl + click-through path covers every base without them.

**On the anti-bot pages:** HugeDomains, Afternic, Sedo, Dan, and USPTO's search SPA all sit behind Cloudflare / AWS WAF and reliably 403 raw `curl` and `WebFetch`. Firecrawl's unblocker is the one assisted attempt; a composed click-through URL is the reliable fallback the user clicks in ~30 seconds. Don't fight the scrapers with headless-browser workarounds.

## The flow

Nine steps, availability-first. Full commands and the anti-bot tool ladders live in the premium reference; the seed-word brainstorming method and budget buckets live in the premium reference.

1. **Budget** — ask what they'd pay; anchor to the budget buckets; filter all candidates under-budget before checking.
2. **Brainstorm** — 20–40 candidates via the seed-word method (two-word mashups preferred; prefix/suffix grid when a bare word is taken). Surface the numbered list before checking.
3. **Availability (free RDAP)** — loop `rdap.org` (404 = available, 200 = taken), pacing for its rate limit.
4. **Cross-check** — authoritative `.com` RDAP (`rdap.verisign.com`) for ground truth; RDAP JSON / whois for registrant + expiry.
5. **Aftermarket sweep** — for taken-but-wanted candidates, Firecrawl scrape → click-through to HugeDomains / Afternic / Sedo / Dan.
6. **Bucket** — available-now / aftermarket-under-budget / drop.
7. **Negotiate** — lowball 30–50% below ask; use "make an offer"; direct owner outreach for parked domains.
8. **Name research (NOW, not before)** — USPTO trademark screen + X / LinkedIn / Instagram handle checks on the top 3–5 survivors.
9. **Buy** — register the winner at a mainstream registrar, or buy through the marketplace escrow. **Confirm before spending — real money.**

# Domain shortlist — {project}, {date}

Budget: {$ range}

## Available now (~$10–$30/yr)
| Domain | RDAP status | Notes |
|---|---|---|
| trycove.com | AVAILABLE (404) | two-word mashup, easy spell |

## Aftermarket — under budget
| Domain | Asking | Marketplace | Link |
|---|---|---|---|
| cove.com | $1,795 | HugeDomains | {url} |

## Dropped (over budget / no listing / weak)
- clubhouse.com — five-figure, ungoogleable

## Recommended pick — {domain}
- Availability: AVAILABLE / listed at {price}
- Trademark screen: {no blocking Live exact-phrase match in class N | flag}
- Social handles: x.com ☑ · linkedin ☑ · instagram (verify)
- Say-it-out-loud test: spellable on a phone call ☑
- Caveat: screening, not legal clearance — run serious names past an IP lawyer
```

Route the file to the relevant project or client folder as `MMYY-domain-shortlist.md` per the CLAUDE.md naming convention.

## Guardrails

- **Brainstorm-first, action-last.** RDAP and social checks are free and safe; a purchase is not. Never trigger a buy until the user says "buy it."
- **Budget filter is non-negotiable.** "But I love it" is the exact trap the method catches.
- **USPTO screening ≠ legal clearance.** Gut-check filtering only; serious names go to an IP lawyer or a full clearance service.
- **No invented availability.** Report the RDAP status code you actually got. If a check is rate-limited or unclear, say so — don't guess a domain is free.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains and output template. For a domain shortlist the sharpest failure modes are: a top pick that trademark-collides in its own class, a name unspellable on a phone call, or one that ages badly as the company grows past the founding idea.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for a quick single-domain availability check.

## Attribution

Adapts the availability-first domain method from [`coreyhaines31/makerskills/domain`](https://github.com/coreyhaines31/makerskills) (MIT, © 2026 Corey Haines; itself crediting Laura Roeder's method), accessed 2026-07-08. Re-tooled onto free RDAP/whois + WebFetch; paid aggregators deferred.
