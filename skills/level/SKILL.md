---
name: level
version: '1.2'
last_updated: 2026-06-04
author: genesys-growth
description: 'Assesses a Claude Code environment''s maturity on a fun 0-10 ladder calibrated to the 4-systems
  pillars (Context / Skills / Integrations / Orchestration), via an interactive quiz OR a silent file scan,
  then produces a single-next-level roadmap + a branded, shareable HTML dashboard. Level 10 is benchmarked
  against the most advanced documented setup plus the latest Anthropic-native features. Flags: --mode beginner|internal,
  --quiz, --assess, --build. Triggers: "/level", "what''s my claude code level", "claude code level quiz",
  "assess my claude code setup", "claude code maturity". NOT for assessing a client''s GTM maturity (use the
  GTM audit skills) and NOT for diagnosing a slow session (use /why-slow).'
goal: Score a Claude Code environment 0-10 (with a 4-pillar breakdown) and hand back a focused next-level roadmap + shareable dashboard.
outcome: A scored assessment (quiz or scan) + per-pillar sub-scores + single-next-level roadmap + a re-runnable, screenshot-shareable HTML dashboard. Level 10 is anchored to the documented ceiling, so the score is honest, not inflated.
primitive: meta
sub_primitive: learning
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended: []
outputs:
- type: runbook
  feeds_into:
  - quickstart-onboarding
depends_on: []
feeds_into:
- quickstart-onboarding
owned_by_agent: operator
mcps_used: []
push_targets: []
triggers:
  slash_commands:
  - /level
  natural_language:
  - what's my claude code level
  - claude code level quiz
  - assess my claude code setup
  - claude code maturity
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
disable-model-invocation: false
---

# /level — the 10 levels of Claude Code

**Situation.** Most people using Claude Code have no idea how much of it they're actually using — they type prompts into a terminal and stop there, or they've built a deep system and can't see the gaps. **Complication.** There's no honest, repeatable way to answer "how good is my setup, really, and what's the single next thing to build?" Generic "10 levels of AI" lists don't measure Claude Code specifically, and self-assessment drifts. **Question.** Where are you on the Claude Code mastery curve, and what's the one move that levels you up? **Answer.** This skill scores you 0-10 on a ladder calibrated to the 4 systems pillars, benchmarked against the most advanced documented setup + the latest Anthropic features, then hands you a focused roadmap and a shareable dashboard.

This is NOT the generic "10 levels of Claude" (browser, desktop, projects). It's specifically Claude Code mastery. Level 0 is "just installed it." Level 10 is genuinely rare — it's the documented ceiling in [`references/benchmark.md`](references/benchmark.md).

```
Pick a front door → Score it → Show the roadmap → Render dashboard → Build first step
       ↓                ↓             ↓                ↓                  ↓
   quiz or scan    0-10 + 4 pillars  next level only  HTML (shareable)  optional
```

Designed to be re-run. Every time you level up, the score updates.

---

## Modes and flags

Parse the user's input for flags. Defaults shown.

| Flag | Effect |
|------|--------|
| `--mode beginner` (default) | "Knowledgeable friend" voice (see tone rules below). Default brand = GTM Engineer School (or template defaults). Default front door = **quiz**. |
| `--mode internal` | Operator-terse voice for self/team audits. Default brand = Genesys Growth kit. Default front door = **scan**. |
| `--brand-kit <path>` | Brand the HTML dashboard from a specific brand kit (a DESIGN.md with token frontmatter). Overrides the mode's default brand. `--brand-kit none` forces the plain dark defaults. |
| `--format html` (default) `\| ascii \| both` | Output shape. `html` = the branded dashboard. `ascii` = a fixed-width, paste-anywhere result card (best for sharing — Slack / LinkedIn / a code block). `both` = render each. |
| `--quiz` | Force the interactive quiz front door (works with zero setup; shareable). |
| `--assess` | Force the silent file scan, then stop after the assessment (no roadmap/build). |
| `--build` | Skip assessment; jump straight to building the next step (asks current level first). |

If no flag: use `--mode beginner` and offer both front doors ("Want the quick **quiz**, or should I **scan** your setup?"). When you have a brand kit (via `--brand-kit` or the mode default), offer to apply it: "Brand the dashboard with your {brand} kit, or keep the plain dark theme?"

---

## Phase 1 — pick a front door, then score

Both doors converge on the same result: a level (0-10) + a 0-4 sub-score per pillar. Read [`references/levels.md`](references/levels.md) for the ladder, the 4-pillar mapping, and the scoring rules ("highest level meeting ALL criteria"). It is the source of truth for both doors.

### Phase 1a — Quiz (default in beginner mode)

Read [`references/quiz.md`](references/quiz.md) for the question bank + the answer→(level band + pillar) scoring map.

1. Ask the ~8 questions using `AskUserQuestion` (one tool call, multiple questions, clean clickable options). Keep it fast and fun.
2. Map each answer to its pillar + level band per the scoring map.
3. Reconcile to a single level + 4 pillar sub-scores per the rule in `quiz.md` (a pillar's sub-score is gated by the highest rung that pillar's answers clear; the overall level is the highest rung where ALL its required pillars clear).
4. The quiz needs nothing on disk — it works for a total beginner or a prospect.

### Phase 1b — Scan (default in internal mode)

Silently inspect the environment — do NOT ask permission per check, just read what's available. Use the scan checklist in [`references/levels.md`](references/levels.md). Cover: CLAUDE.md (all locations + depth), `.claude/skills` + `.claude/commands` (count + complexity), MCP config (`.mcp.json` + user config + plugins — count + categories), memory/rules/ontology depth, hooks + agents (quality-gate + orchestration signals), headless/SDK + plugin signals, browser MCPs, worktrees + `/workflows`, scheduled/background agents.

Then ask the 3 context questions:
1. What do you mainly use Claude Code for?
2. What's your biggest friction right now?
3. If you could automate one repeated thing, what would it be?

Determine the level via the calibrated scoring table in `levels.md`. **Quantity ≠ level** — 50 trivial skills is still Level 3; integration + complexity is what moves the rungs.

### Converge — present the assessment

Anchor the ceiling using [`references/benchmark.md`](references/benchmark.md): Level 10 = the documented most-advanced setup + every current Anthropic-native feature. Present, in the mode's voice:

- The level number + its fun name + one-line vibe.
- The dual lens: a quick per-pillar read (which of Context / Skills / Integrations / Orchestration is strong, which is the gap).
- Walk the rungs they've cleared bottom-to-top, naming the specific thing found for each, then name the first rung that stops them and **why it matters** (plain language, not jargon).
- "Where that puts you" — most land 1-4; 5 is strong; 7+ is rare.

**Tone rules (beginner mode):** talk like a knowledgeable friend, not a grading rubric. Explain *why* each thing matters, not just that it was found. Say so genuinely when something's impressive; say it constructively when something's messy. Define jargon inline ("headless mode — running Claude from a script instead of typing into the terminal"). Use "you/your".

**Tone rules (internal mode):** operator-terse. Lead with the weakest pillar and the single highest-leverage fix. Skip the encouragement.

If `--assess`, stop here. Otherwise continue.

---

## Phase 2 — the roadmap (next level only)

Show ONLY the next-level transition — focus is everything, don't dump all 10. Read the matching section in [`references/roadmaps.md`](references/roadmaps.md) for the assessed level and present its 3-4 steps with time estimates, recalibrated to current Anthropic-native features (plugins, `/workflows`, subagents, hooks, scheduled agents, the Agent SDK, output styles, worktrees, the memory tool).

---

## Generate the dashboard

Always produce output after Phase 1 (+ Phase 2 unless `--assess`). Pick the shape from `--format` (default `html`). For the quiz / lead-gen path, offer the ASCII card — it's the paste-anywhere artifact (Slack, LinkedIn, a code block).

### HTML dashboard (`--format html`, default — or `both`)

1. Read [`references/dashboard-template.html`](references/dashboard-template.html).
2. **Resolve the brand.** Pick the brand kit (a DESIGN.md with token frontmatter):
   - `--brand-kit <path>` given → read that file. `--brand-kit none` → skip to the template's dark defaults.
   - else `--mode internal` → `projects/genesys/brand/0626-brand-kit.md` (the latest `*-brand-kit.md` under `projects/genesys/brand/`).
   - else `--mode beginner` → a GTM Engineer School kit if one exists, else the template's dark defaults.
   - For a client run, prefer `projects/consulting/active/{client}/brand/*-brand-kit.md`.
3. **Map brand-kit tokens → dashboard tokens** (per the template's brand-token comment):

   | Dashboard | DESIGN.md source | Notes |
   |-----------|------------------|-------|
   | `{{ACCENT}}` | `colors.accent` | primary (number, current dot, bars, links) |
   | `{{DONE}}` | `colors.tertiary` or `colors.success` | cleared dots/rows |
   | `{{BG}}` / `{{SURFACE}}` / `{{SURFACE_2}}` | `colors.background` / `surface` / `surface-elevated` | |
   | `{{BORDER}}` | `colors.border` | |
   | `{{TEXT}}` / `{{TEXT_MUTED}}` / `{{TEXT_SUBTLE}}` | `colors.on-background` / `-muted` / `-subtle` | |
   | `{{FONT}}` + `{{FONT_LINK}}` | `typography.*.fontFamily` | add the font's web `<link>` (e.g. Fontshare for General Sans); else `""` |
   | `{{BRAND_NAME}}` / `{{BRAND_URL}}` | `name` / domain | |

   If the kit is a light theme, keep text/background readable (the template assumes a dark canvas — for light brands, swap `{{BG}}`→light, `{{TEXT}}`→dark and sanity-check contrast). Honor `design-production.md` token-cite discipline: use the kit's exact hex, never approximate.
4. Replace every `{{TOKEN}}` with real assessment data — per-pillar bars + the shareable result card (level + name + vibe, sized to screenshot).
5. Write to `~/Desktop/claude-code-level.html`.
6. Open it platform-aware (`open` on macOS, `xdg-open` on Linux, `start` on Windows/WSL).
7. Tell the user it's open + print the path + name the brand applied.

### ASCII card (`--format ascii` — or `both`)

A fixed-width, monochrome, copy-paste card — the most shareable shape. Build a JSON payload and pipe it to the generator (it asserts every line is identical width, so the box never misaligns):

```bash
echo '{"level":N,"name":"<level name>","vibe":"<vibe line>",
"pillars":{"Context":c,"Skills":s,"Integrations":i,"Orchestration":o},
"takeaway":["short line 1 (≤48 chars)","line 2","line 3"],
"brand_name":"<from brand kit name>","brand_url":"<from brand kit domain>"}' \
  | python3 references/ascii-card.py
```

It prints the card and saves `~/Desktop/claude-code-level.txt`. Then **also paste the card inline in a fenced code block** so the user can copy it straight from chat. `brand_name`/`brand_url` come from the resolved brand kit's `name` + domain (ASCII is monochrome — brand presence is the wordmark, not colour). Keep `takeaway` to 2-3 lines ≤48 chars each.

---

## Phase 3 — build it now (optional)

Ask: "Want me to build the first step of your roadmap right now?" If yes, execute the matching build step in [`references/build-steps.md`](references/build-steps.md) for the assessed level (create the CLAUDE.md, wire the first MCP, write the first skill, scaffold memory, upgrade a skill to multi-phase, write the first headless script, etc.). Adapt to the person — don't paste templates verbatim. If no, end on the roadmap summary.

If the person scores 0-2 and wants a guided ramp, point them at `/quickstart` — it onboards them onto the marketing-quickstart framework and gets them to Level 2-3 fast.

---

## Self-roast (run before delivering)

- Is the level honest, or inflated? Quantity ≠ maturity — did I check integration + complexity, not just file counts?
- Did I anchor Level 10 to `benchmark.md`, so the ceiling is real and not flattering?
- Beginner mode: did I explain *why* each gap matters and define jargon, or did I just list findings?
- Did I show only the NEXT level's roadmap, not all 10?
- Did the dashboard actually render + open, with the per-pillar bars and a shareable card?

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-03 | Initial. Adapted from the community "Level Up" skill (thegenaicircle.com); recalibrated to the Genesys 4-systems pillars, Level 10 = the documented Genesys ceiling + latest Anthropic features, added the interactive quiz front door + dual-lens per-pillar scoring + dual-mode branding. |
| 1.1 | 2026-06-04 | Added `--brand-kit <path>` flag + full DESIGN.md→dashboard token mapping (accent/done/bg/surface/text/font/name/url). Template fully tokenized (was accent-only). Internal mode defaults to the Genesys brand kit; offers to brand on every run. |
| 1.2 | 2026-06-04 | Added `--format html\|ascii\|both`. New `references/ascii-card.py` — a fixed-width, alignment-asserted, paste-anywhere result card (best for sharing). HTML output section generalized to "Generate the output" with per-format branches. |
