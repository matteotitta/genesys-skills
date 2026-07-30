---
name: marketing-team-tracker
version: "1.0"
last_updated: 2026-06-28
author: genesys-growth
description: |
  Maintains a curated roster of best-in-class marketing teams and harvests their most
  stealable plays on demand, each classified against five repeatable patterns
  (product-as-marketing, characters-and-series, community-as-distribution, weird-creative,
  pick-a-fight). Resolves each team's surfaces, scans for plays shipped since the last scan,
  ranks by engagement, and emits a dated marketing-plays brief plus an append-only swipe file
  and a living roster. Triggers: "track marketing teams", "marketing inspiration scan",
  "marketing swipe file", "what's X doing in marketing", "add X to the marketing tracker".
  Upstream: recommended signal-scan. Downstream: feeds content-strategy, marketing-ideas,
  thought-leadership, gtme-pulse, linkedin-weekly-content. NOT for competitor threat analysis
  (use /competitor-research), per-account buying signals (use /niche-signal), or one-off
  ideation from a brief (use /marketing-ideas).
goal: Track a roster of best-in-class marketing teams and surface their most stealable plays on demand, classified by pattern.
outcome: A dated marketing-plays brief, an append-only swipe file tagged by pattern with a steal-this line and a dated source, and a living roster carrying per-team last_scanned state — feeding content, ideation, and social work.
primitive: research
sub_primitive: null
ontology_type: temporal-signal-brief
review_gate: 1
inputs:
  required: []
  recommended:
  - signal-scan
outputs:
- type: temporal-signal-brief
  feeds_into:
  - content-strategy
  - marketing-ideas
  - thought-leadership
  - gtme-pulse
  - linkedin-weekly-content
depends_on: []
feeds_into:
- content-strategy
- marketing-ideas
- thought-leadership
- gtme-pulse
- linkedin-weekly-content
owned_by_agent: researcher
mcps_used:
- exa
- firecrawl
- apify
push_targets: []
triggers:
  slash_commands:
  - /marketing-team-tracker
  natural_language:
  - "track marketing teams"
  - "marketing inspiration scan"
  - "marketing swipe file"
  - "what's X doing in marketing"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# Marketing team tracker

Keep a living roster of the marketing teams worth stealing from, and harvest their best plays on demand. Each play is classified against five repeatable patterns, given a one-line "steal this", and filed in an append-only swipe file your content, ideation, and social skills can pull from. Knowledge type: `temporal-signal-brief` (per `.claude/rules/ontology.md`); maturity: emergent — each scan is fresh and time-bound, briefs are not locked.

Seeded from Tom Orbach's "Marketing Ideas" roundup (the 9 teams he follows + the five patterns they share), cite-only — same precedent as `.claude/rules/linkedin-cold-dm-doctrine.md`. The roster + swipe file are ours; the seed is attributed in `references/seed-data.md`.

Cousin to `/signal-scan` — that skill answers "what happened with one topic in N days." This one carries a *standing roster* of marketing teams, classifies what it finds against a *marketing-play taxonomy*, and *accumulates* a swipe file across runs. Distinct from `/marketing-ideas` (ideation from a brief — the tracker feeds it raw plays) and `/competitor-research` (a deep static dossier on a threat, not an inspiration source).

---

## When to run

Invoke for: `track marketing teams`, `marketing inspiration scan`, `marketing swipe file`, `what's {company} doing in marketing`, GTME Pulse sourcing, pre-content-calendar inspiration, `add {company} to the tracker`.

Do **NOT** invoke for:

- A deep competitor threat dossier → `/competitor-research` (static, 13-dimension, adversarial).
- Per-account buying signals / timing triggers → `/niche-signal` (outbound, "when to reach out").
- Ideation from a brief → `/marketing-ideas` (this skill *feeds* it real plays to riff on).
- One topic's last-N-days news → `/signal-scan` (topic-agnostic, no standing roster).

**Brain-first (mandatory):** before any external call, run the `.claude/rules/brain-first-lookup.md` ladder — `/recall {team}` + grep the swipe file. A play you logged last cycle may already answer the question. Annotate the brief if you went external after a miss.

---

## Modes + flags

| Mode | What it does |
|------|--------------|
| `/marketing-team-tracker` (default) | Scan the canonical roster for plays shipped since each team's `last_scanned`; emit a dated brief + append to the swipe file. |
| `--seed` | Bootstrap (or rebuild) the roster + swipe file from `references/seed-data.md`. Idempotent. |
| `--client {slug}` | Layer that client's overlay roster (`roster/client-{slug}-roster.md`) on the base; route the brief to `projects/consulting/active/{slug}/content/strategy/`. |
| `--team {name}` | Deep single-team scan (full surface sweep, ignores `last_scanned`). |
| `--add {company}` / `--remove {company}` | Roster management — resolve surfaces for a new team, or retire one. |

| Flag | Default | Effect |
|------|---------|--------|
| `--days N` | 30 | Lookback window per team. Marketing plays move slower than news — 30 is the floor, `--days 90` for a quarterly sweep. |
| `--emit=html` | markdown | Self-contained shareable HTML brief instead of markdown. |
| `--x` | off | Add X/Twitter via Apify actor (**credit-gated**). Many of these teams ship their best plays on X — opt in per run. |

---

## Inputs

The **roster is the input** — no required upstream skill. Recommended: `/signal-scan` (its resolved entities for a team transfer straight into the roster).

Read first, every run (brain-first):

- `projects/research/marketing-team-tracker/roster/canonical-roster.md` — the tracked teams + per-team surfaces + `last_scanned`.
- `projects/research/marketing-team-tracker/swipe-file/{team}.md` — what's already logged (so you don't re-surface it).
- `projects/research/marketing-team-tracker/marketing-team-strategy.md` — the cross-cycle scratchpad (decisions locked, things to stop doing, open questions). Per `.claude/rules/iterative-strategy-scratchpad.md`.

---

## The scan loop

Six steps. Schemas in `references/`. Surface→tool mapping in `references/monitoring-surfaces.md`.

1. **Read state (brain-first).** Load the roster, the per-team swipe files, and the scratchpad. Apply locked decisions; suppress named anti-patterns. Only scan for the gap since `last_scanned`.
2. **Resolve each team's surfaces.** From the roster: the named operator's LinkedIn + the company page + blog/changelog + X handle. Resolve before searching — this is the step that turns a brand-name keyword dump into actual plays (borrowed from `/signal-scan`). If a surface isn't in the roster, resolve it once and write it back.
3. **Scan since `last_scanned`.** Per team, sweep the resolved surfaces for marketing *moves* (campaigns, launches, stunts, positioning shifts, content series, community plays) shipped inside the `--days` window. Engagement-ranked, recency-decayed. Free discovery before metered extraction (`crawl-cost-discipline.md`); gate paid Apify (`apify-credits.md`).
4. **Extract → classify → steal-this.** For each new play: name it, classify it against the five patterns (`references/play-patterns.md`), write a one-line "steal this" takeaway, and tag confidence + source URL + access date. No quote, no metric you can't cite → mark `[Not available]`, never invent (per `evidence-bound-outputs.md`).
5. **Cross-team cluster.** Note where teams converge on the same pattern this cycle ("three teams ran a pick-a-fight play this month") — that convergence is the signal worth surfacing to Pulse.
6. **Emit + persist.** Write the dated brief; append new plays to each `swipe-file/{team}.md`; bump each team's `last_scanned`; update the scratchpad with anything that should carry forward. Apply the thin-input guard before you ship.

The refresh discipline mirrors `/competitor-research`: read the existing swipe file first, compare don't append-blind, date-stamp a "Recent changes" line, no-change = no entry.

---

## The five patterns

Every play classifies into one (occasionally two). Full rubric + worked examples in `references/play-patterns.md`.

| Pattern | The move |
|---------|----------|
| **Product-as-marketing** | The product itself is the campaign — a playable demo, a free tool, a feature that markets (Decart's Oasis, Ahrefs' free tools, Anthropic's import button). |
| **Characters-and-series** | Recurring characters and series, not one-off ads (Ramp's Brian, Torq's TorqTV, tl;dv's sketches). |
| **Community-as-distribution** | Turn the community into the distribution channel (Clay's certifications + Slack, Lovable's clippers, Cluely's creator army). |
| **Weird-creative** | Creative so weird people share it for you (Cluely's blank billboards, Ramp's wrecking ball, Anthropic's coffee shop). |
| **Pick-a-fight** | Pick a fight on purpose — a category, a competitor, a norm (Cluely's whole brand, Torq's "SOAR is Dead", tl;dv vs "bot-free"). |

---

## Output contract

Three artifacts per run, all filled from the canonical `references/brief-template.md`. Field schemas: `references/roster-schema.md`, `references/swipe-file-schema.md`.

**1. The dated brief** — `MMYY-marketing-plays-brief.md` (or the client folder under `--client`). Sections:

- **Headline** — the single most stealable play across the roster this cycle.
- **Fresh plays** — new plays since last scan, ranked, grouped by team. Each: the play · pattern · steal-this · source + access date.
- **Pattern watch** — which of the five patterns is trending across the roster this cycle (the cross-team cluster).
- **Roster status** — per team: scanned date · plays added · "thin / dry" if nothing new.
- **Coverage footer** — which surfaces ran, were thin, or were skipped. No silent truncation.

**2. The swipe file** — append new plays to `swipe-file/{team}.md`, each entry carrying the `references/swipe-file-schema.md` frontmatter (team · pattern · steal-this · source · date). A play without a steal-this is a bookmark, not a swipe — drop it or write the why (`taste-library` rule).

**3. The roster** — bump `last_scanned` per scanned team; write back any newly resolved surface.

Voice + structure follow `output-tenets.md`, `output-simplicity.md`, `doc-output-structure.md`, `ai-speak-anti-patterns.md`. Source placement per `output-simplicity.md` § three-layer (internal-input brief keeps citations inline).

---

## Thin-input guard

If a scan surfaces fewer than **3 fresh plays** worth stealing across the whole roster, say so — ship a short "thin cycle" note naming what was checked, rather than padding the brief with weak plays. Marketing teams don't ship a stealable move every 30 days; an honest dry note beats a manufactured one (pattern from `/niche-signal`'s thin-input rule).

---

## Credit gate

Default surfaces — Exa news + Firecrawl blog/LinkedIn-page/changelog — incur no Apify spend. `--x` runs through an Apify actor and is **off by default**: when on, follow `.claude/rules/apify-credits.md` — `fetch-actor-details` (free) first, estimate cost, gate before `call-actor` (soft <$5, hard ≥$5). Probe one team before fanning out across the roster (`goal-driven-loops.md`).

---

## Quality gate (binary, before declaring done)

- Brain-first ladder run before any external call; brief annotated if it went external after a miss.
- Each team's surfaces resolved (operator + company page + blog + X handle named in the roster, or "none found").
- Every play carries pattern + steal-this + source URL + access date; no invented engagement numbers (mark `[Not available]`).
- Date window respected — nothing older than `--days N` as a fresh play (older context flagged as background).
- Thin-input guard applied — < 3 fresh plays ships an honest dry note, not padding.
- Cross-team pattern watch present when 2+ teams converge.
- Scratchpad + `last_scanned` updated; new surfaces written back to the roster.
- `--x` / paid calls: cost estimated + gated.

---

## Composition

| Rule | Role |
|------|------|
| `brain-first-lookup.md` | Step 1 — check the swipe file + recall before external. |
| `iterative-strategy-scratchpad.md` | The cross-cycle memory file that makes corrections compound. |
| `exa-protocol.md` | Tool selection + citation standard for default surfaces. |
| `crawl-cost-discipline.md` | Free discovery before metered extraction. |
| `apify-credits.md` | Gate `--x` and any paid Apify call. |
| `goal-driven-loops.md` | Probe one team before fanning out across the roster. |
| `evidence-bound-outputs.md` | Cite the play or lower confidence — never invent the move or the metric. |
| `output-tenets.md` · `output-simplicity.md` · `doc-output-structure.md` · `ai-speak-anti-patterns.md` | Brief voice + structure. |

---

## References

- `references/play-patterns.md` — the five-pattern rubric + classification rules + worked examples.
- `references/roster-schema.md` — the roster file + per-team dimension schema.
- `references/swipe-file-schema.md` — the swipe entry frontmatter + worked example.
- `references/brief-template.md` — the canonical output skeleton (brief + swipe entry + roster row + thin-cycle variant) every run fills.
- `references/monitoring-surfaces.md` — per-team surfaces, the entity-resolution checklist, default-on/off, credit gates.
- `references/seed-data.md` — the seed teams + operator additions (~50 documented plays) + sources + steal-this lines (cite-only, Tom Orbach attribution).

---

