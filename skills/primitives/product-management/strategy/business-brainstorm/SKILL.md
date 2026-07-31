---
name: business-brainstorm
version: '1.0'
last_updated: 2026-07-08
author: genesys-growth
description: 'Pressure-tests a potential new business, product, or side project against a 9-dimension serial-founder filter (problem, audience, wedge, monetization, moat, portfolio fit, distribution, energy fit, opportunity cost), rating each strong/OK/weak/needs-research, and outputs a dated viability brief with a build / sleep-on-it / pass verdict plus a first-100-customers sketch and a domain read. Routes unknowns to /deep-research + Exa; checks.com availability via the sibling /domain skill (RDAP/WHOIS fallback). Archives every brief to the premium reference so past calls stay searchable. Triggers: "business brainstorm", "should I build X", "pressure-test this idea", "validate this idea", "is X a good business", "new business idea", "what about a [type] for [audience]". Recommended upstream: company-context, icp-research. Downstream: promote to /strategy-doc when the verdict is build. NOT for marketing ideas for a product you already run (use /content-strategy) and NOT for a strategy doc on an already-committed build (use /strategy-doc).'
goal: Pressure-test a business or product idea across nine founder-filter dimensions and return a build / sleep-on-it / pass verdict.
outcome: A dated viability brief scoring the idea on 9 dimensions with a build / sleep-on-it / pass verdict, a first-100-customers sketch, a domain read, and open questions — archived and searchable, ready to promote to /strategy-doc if it's a build.
primitive: product-management
sub_primitive: strategy
ontology_type: idea-validation
review_gate: 2
inputs:
  required: []
  recommended:
  - company-context
  - icp-research
- type: idea-validation
  feeds_into:
  - strategy-doc
depends_on: []
- strategy-doc
owned_by_agent: product-manager
mcps_used:
- exa
- gdrive
- notion
triggers:
  slash_commands:
  - /business-brainstorm
  natural_language:
  - "business brainstorm"
  - "should I build X"
  - "pressure-test this idea"
  - "validate this idea"
  - "is X a good business"
  - "new business idea"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# Business brainstorm — pressure-test an idea against the founder filter

Takes a vague idea, runs it through a 9-dimension founder filter, and returns a structured viability brief with a hard verdict: build, sleep on it, or pass. Composes with `/deep-research` (for market validation) and the sibling `/domain` skill (for naming and.com availability).

This is the upstream question — *should this thing exist, and can you win it?* It's not marketing ideas for a product you already run (that's `/content-strategy`), and it's not a strategy doc for an already-greenlit build (that's `/strategy-doc`). Run this first; promote the winners to `/strategy-doc`.

## When to run

Invoke when you say:

- "Pressure-test this idea" / "is X a good business" / "should I build X"
- "New business idea — [1-line]" / "what about a [type] for [audience]"
- "Validate this side project before I sink a weekend into it"

Do NOT run when:

- You want marketing angles for an existing product → `/content-strategy`
- The build is already committed and you need the strategy → `/strategy-doc`
- You want ICP or competitor depth on its own → `/icp-research`, `/competitor-research`

## Inputs

**Required:**

- The idea in 1–2 sentences (the *what*)
- The reason it's on your mind now (the *why now*)

**Recommended (improve the score):**

- `company-context` — if the idea sits near a known market or client
- `icp-research` — sharpens the audience + wedge dimensions
- Any starting context — a chat where this came up, a post that sparked it, a problem you hit

**If the idea is too vague to score:** ask 1–2 clarifying questions and stop. Don't pad the brief with assumptions.

## The 9 dimensions

Full rubric with per-dimension ✅/🟡/❌ criteria and the scoring-to-verdict gates: the premium reference. In summary:

1. **Problem** — real, frequent, acute?
2. **Audience** — who has it, can you reach them?
3. **Wedge** — how do you get the first 100 customers?
4. **Monetization** — who pays, how much, how often?
5. **Moat** — why is it hard to copy?
6. **Portfolio fit** — complements or cannibalizes your existing properties?
7. **Distribution** — which audience asset launches it?
8. **Energy fit** — do you want to run it for 2+ years?
9. **Opportunity cost** — what do you *not* do if you do this?

Rate each ✅ strong / 🟡 OK / ❌ weak / ❓ needs-research. Problem, Audience, Distribution, and Energy are the four non-negotiables — a ❌ on any caps the verdict.

## Steps

### 1 — Capture the idea

Get the *what* and the *why now*. If you point at a past chat or doc, load it first. Check memory `project_*.md` before assuming the idea is brand-new — it may already be an in-flight build.

### 2 — Load the framework + portfolio overlay

Read the premium reference and apply each dimension in order.

Load your portfolio context before scoring the fit dimensions, so you don't have to name each property by hand. Check:

- `MEMORY.md` — active client roster
- memory `project_*.md` — in-flight builds
- `projects/genesys/CLAUDE.md` — the Genesys businesses (Genesys Growth, GTM Engineer School, the newsletters, the LinkedIn audience)
- `projects/apps/` — the app portfolio

Use these for **portfolio fit**, **distribution**, and **opportunity cost**. When brainstorming for a client instead of Genesys, swap in the client's product lines and channels as the portfolio.

### 3 — Score each dimension

For each of the 9, write a 1-line take plus a verdict (✅ / 🟡 / ❌ / ❓). Don't fake the unknowns — mark them ❓ and route to research in Step 4.

### 4 — Route unknowns to research (when needed)

If 2+ dimensions are ❓, offer: *"Want me to run /deep-research on [topic] before scoring?"*

- Deep multi-source read → `Skill({skill: "deep-research", args: "<topic>"})`
- Quick market/competitor scan → `mcp__exa__web_search_exa` with a date filter, per [`.claude/rules/exa-protocol.md`](../../../../../rules/exa-protocol.md)

Useful targets: market size + who-pays signal; the competitive landscape ("alternatives to X" pages); ICP signal on the forums/Reddit/X where the audience gathers; pricing benchmarks off competitor pricing pages. Fold the findings into the score and re-rate the ❓ rows.

### 5 — Check the.com

Run the sibling `/domain` skill on the working name(s) for availability + pricing. If naming is wide open, run 5–10 candidate names through it and report which are free.

If `/domain` isn't available yet, fall back to a free RDAP/WHOIS lookup via `WebFetch` on `https://rdap.org/domain/<name>.com` — a 404 means likely available, a 200 means registered. A strong idea on a $50k domain is worse than a B+ idea on a free.com.

### 6 — Write the brief

Use the output format below.

### 7 — Archive

Write the brief to the premium reference<YYYY-MM-DD>-<slug>.md`. Append one line to the premium reference (create it on first run):

```markdown
- 2026-07-08 — [<idea>](./<filename>.md) — **<verdict>** — <one-line rationale>
```

Archive every brief, even the passes — killed ideas resurface, and the archived rationale stops you re-litigating them.

### 8 — Surface + offer next step

Show the brief in chat and name the archive path. Then offer, by verdict:

- **Build** → "Promote to `/strategy-doc` and scaffold a repo / landing page?"
- **Sleep on it** → "Set a 30-day revisit via `/schedule`?"
- **Pass / steal-an-angle** → nothing to scaffold; the "angle to steal" section is the payoff
- Any verdict → "Push to Notion as a positioning canvas?" per [`.claude/rules/notion-protocol.md`](../../../../../rules/notion-protocol.md)

# Business brainstorm: <name or idea slug>

**Date:** <YYYY-MM-DD> · **Idea:** <1–2 sentences> · **Why now:** <1 sentence>

## Verdict
**Build** / **Sleep on it** / **Pass** / **Steal an angle for [existing property]**

<2–3 sentence rationale>

## Score
| Dimension | Take | Verdict |
|---|---|---|
| 1. Problem | … | ✅ |
| 2. Audience | … | 🟡 |
| 3. Wedge | … | ❓ |
| 4. Monetization | … | ✅ |
| 5. Moat | … | ❌ |
| 6. Portfolio fit | … | ✅ |
| 7. Distribution | … | ✅ |
| 8. Energy fit | … | 🟡 |
| 9. Opportunity cost | … | ❌ |

## Domain
- <name>.com — available / taken / aftermarket $<price>

## Research applied
- <link to the /deep-research brief, if one was run>

## Open questions
- <what would change the verdict>

## If you build it (sketch)
- **First 100 customers:** <how> · **Wedge offer:** <what> · **Price:** <range> · **MVP scope:** <1–3 features>

## If you don't build it
- **Angle to steal for an existing property:**
  - <property>: <angle>
```

## Self-roast (run before you surface the brief)

- [ ] All 9 dimensions scored — no "figure it out later" cop-outs
- [ ] Verdict is one of build / sleep-on-it / pass / steal-an-angle — never "maybe"
- [ ] The four non-negotiables (Problem, Audience, Distribution, Energy) checked against the ❌-caps-the-verdict rule
- [ ] Portfolio overlap grepped (`MEMORY.md` + `project_*.md`) — if the idea is 80% an existing property, the verdict is steal-an-angle, not build
- [ ] ❓ rows either researched or explicitly flagged as open questions
- [ ] Domain checked; the brief is archived with an INDEX line
- [ ] "Angle to steal" filled even on a pass — it's the highest-leverage output of a kill

## Composition

- `/deep-research` + Exa — market, competitor, and ICP validation for ❓ dimensions
- `/domain` (sibling) —.com availability and naming; RDAP/WHOIS `WebFetch` fallback
- `/strategy-doc` — the promotion target when the verdict is build
- Memory (`project_*.md`, `MEMORY.md`) — portfolio context, so you don't pitch an idea you already run

## Attribution

Adapts the serial-founder-filter framework from [`coreyhaines31/makerskills/business-brainstorm`](https://github.com/coreyhaines31/makerskills) (MIT, © 2026 Corey Haines), accessed 2026-07-08. Adapted to Genesys operator voice + our /deep-research + Exa tooling.

