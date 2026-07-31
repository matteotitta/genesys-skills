---
name: quickstart-onboarding
version: '1.0'
last_updated: 2026-06-03
author: genesys-growth
description: 'Dynamically guides a person through cloning + setting up the claude-code-marketing-quickstart
  GitHub template (the 4-systems marketing OS: Context / Skills / Integrations / Orchestration), detecting
  where they are in the 15-minute tour and driving them to a first runnable "aha" — running a research skill
  and watching a real file land in the spine. Maximises immediate adoption. Flags: --mode beginner|internal.
  Triggers: "/quickstart", "onboard me to the marketing OS", "set up the quickstart repo", "get started with
  claude code marketing", "clone the quickstart". NOT for generic repo setup (this targets the canonical
  marketing-quickstart framework) and NOT for scoring a setup''s maturity (use /level).'
goal: Drive a person from git clone to a populated PMM spine + first research skill run on the marketing-quickstart framework, unblocking each step.
outcome: A fully set-up quickstart repo (Exa wired, 15-min tour done, first /competitor-research run, file landed) with the person oriented to their Week-1 entry point. Adoption tipping point hit, not just a README skimmed.
primitive: meta
sub_primitive: learning
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended:
  - level
- type: runbook
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands:
  - /quickstart
  natural_language:
  - onboard me to the marketing OS
  - set up the quickstart repo
  - get started with claude code marketing
  - clone the quickstart
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
disable-model-invocation: false
---

# /quickstart — onboard onto the marketing OS

**Situation.** Someone just got the link to the `claude-code-marketing-quickstart` repo — a fork-and-go marketing operating system built on the 4-systems framework (Context · Skills · Integrations · Orchestration), with a written 15-minute tour. **Complication.** A README is passive. People clone, skim, and stall *before* the first "aha" — the moment a real file lands in their spine from a skill they ran. That stall is where adoption dies. **Question.** How do we get a brand-new person from `git clone` to that first runnable win without them self-navigating a wall of text? **Answer.** This skill is the active wizard: it detects where they are, unblocks the exact next step, and drives them to run `/competitor-research` against a real target so they *feel* the framework in 15 minutes.

This onboards onto ONE canonical repo: `matteotitta/claude-code-marketing-quickstart`. The repo's [`README.md`](https://github.com/matteotitta/claude-code-marketing-quickstart) is the source of truth for the tour — this skill mirrors and drives it. The full beat-by-beat script + troubleshooting lives in the premium reference.

For an **async handoff** — distributing an MCP, plugin, or repo to a non-technical person you're *not* in a session with — use the one-paste install-prompt pattern in the premium reference. The pasted prompt carries the wizard when you can't.

```
Detect state → Exa key → Clone → Wire.env → Driven tour → THE AHA → Week-1 plan
     ↓ ↓ ↓ ↓ ↓ ↓ ↓
   Phase 0 Phase 1 Phase 2 Phase 3 Phase 4 Phase 5 Phase 6
```

---

## Modes

| Flag | Effect |
|------|--------|
| `--mode beginner` (default) | "Knowledgeable friend" voice. Explain *why* each step matters; define jargon inline. Celebrate the wins (especially the Phase 5 file landing). |
| `--mode internal` | Operator-terse. Skip the encouragement; just sequence the steps + flag blockers. For you/team spinning up a fresh fork. |

---

## Phase 0 — detect where they are (the dynamic part)

Don't restart someone who's halfway. Detect state, then resume at the right phase. Check, in order:

1. **In a cloned quickstart already?** Look in the cwd for the repo's fingerprints — `marketing/CLAUDE.md`, `.claude/skills/competitor-research/`, the `README.md` title "Claude Code Marketing Quickstart". If present → skip to the earliest *incomplete* phase below.
2. **`.env` set?** If the repo exists, check whether `.env` exists with a non-placeholder `EXA_API_KEY`. Missing → resume at Phase 3 (or Phase 1 if they have no key yet).
3. **Tour progress?** Has the PulseAnalytics example been replaced (any file in `marketing/competitors/` dated this month, or `marketing/icp/ICP.md` edited)? If yes, they're past the tour → jump to Phase 5/6.
4. **Nothing found?** Fresh start → Phase 1.

State the detected position back to the person in one line ("Looks like you've cloned it but haven't wired your Exa key — let's do that") so they know you adapted. See the premium reference for the exact checks.

---

## Phase 1 — Exa key (the one prerequisite)

The pre-seeded research skills use Exa for web search + page fetch. Free tier is plenty.

1. Send them to [exa.ai](https://exa.ai), sign up, generate an API key.
2. Tell them to keep it handy for Phase 3.

If they already have a key (or Exa wired globally), say so and skip ahead.

---

## Phase 2 — clone the template

```bash
gh repo create my-marketing-os --template matteotitta/claude-code-marketing-quickstart --private
cd my-marketing-os
```

The `--template` flag gives a clean fork with no inherited history. If they don't have the `gh` CLI, fall back to the GitHub UI "Use this template" button, then `git clone` + `cd`. Troubleshooting (no `gh`, auth, private-repo access) → the premium reference.

---

## Phase 3 — wire `.env`

```bash
cp.env.example.env
# paste the Exa key after EXA_API_KEY=
```

`.env` is gitignored — never commit it. Confirm the key is in place before continuing (a missing/placeholder key is the #1 cause of a failed Phase 5).

---

## Phase 4 — the driven 15-minute tour

Walk them through the reading order, *driving* it (read the file with them, point out the one thing that matters in each), not just linking. The beats, in order (full version in the premium reference):

1. Root `CLAUDE.md` — the lean index (under one page; pointers, not content).
2. `marketing/CLAUDE.md` — the workspace index: the PMM spine (icp / competitors / brand / positioning / messaging) + 5 execution workstreams.
3. `marketing/positioning/positioning.md` — the PulseAnalytics worked example. Point out: anchor + differentiators + value props, refresh cadence + named owner, no invented metrics.
4. `.claude/skills/competitor-research/SKILL.md` + `.claude/skills/icp-research/SKILL.md` — two of the 7 pre-seeded research skills; read how they read a URL and write a file to the spine.
5. `.claude/connections.md` + `integrations/CLAUDE.md` — what Claude has access to; why `.mcp.json` is committed; integrations play both input + output roles.

Keep momentum — this is 15 minutes, not a seminar.

---

## Phase 5 — THE AHA (don't skip this)

This is the adoption tipping point. Get them to run a real skill and watch a real file land:

```
/competitor-research [a competitor they actually care about] — [its URL]
```

The skill writes a dossier to `marketing/competitors/MMYY-{slug}.md`. **Point at the file landing in the spine** — that's the moment the framework stops being abstract. Celebrate it (beginner mode).

If they don't have a target ready, don't let the momentum die: offer to run it on a well-known company, or have them name their own company and run `/icp-research`. The goal is one file landing, today.

---

## Phase 5.5 — hand them the operating manual

They've just watched a file land. That's *what the system does*. This is *how to drive it* — the premium reference, which also ships at the root of the quickstart repo as `HOW-TO-OPERATE.md`.

Don't read all seven habits in the session — it's a 15-minute read of its own and the momentum from Phase 5 is worth more. Point at it, then walk **two** sections live, because these are the two walls they hit first:

- **§2 plan before it touches anything.** The next time they ask for something spanning several files, the difference between planning and not is an afternoon.
- **§7 let it write its own rules.** The compounding one. Show them the move: correct Claude, then add "update the context file so you don't repeat this." Have them do it once, now, on any correction from Phase 5.

Then name the triage table: *"When it goes weird — and it will — the table at the bottom tells you which of the seven you're missing."*

Frame it honestly: the four weeks build the system, this decides whether it still works in week eight. Same file our clients get when we build their workspace.

---

## Phase 6 — decide the Week-1 entry point

Two paths — help them pick:

- **Course-paced** — start the Claude Code for Marketers course at Week 1.1 (4 weeks, one shipped artifact per week). Best for marketers learning Claude Code from scratch.
- **Self-paced** — jump to Week 1.3 (populate their own PMM spine by running the 7 pre-seeded skills against their real company). Best for operators who just need the scaffold.

Lock in the **next concrete action** before ending ("By Friday, run `/competitor-research` on your top 3 competitors"). A named next step is what converts a clone into adoption.

If they haven't run `/level` yet, suggest it — it scores where they are and gives a roadmap beyond this repo.

---

## Adoption mechanics (woven through, not a phase)

- **Always resume, never restart** (Phase 0) — re-doing done steps reads as broken.
- **Drive to the file landing fast** (Phase 5) — the aha beats any amount of reading.
- **Real target over example** — running on a company they care about converts; running on PulseAnalytics doesn't.
- **End on a dated commitment** — "by Friday, X" not "explore when you can".

---

## Self-roast (run before delivering)

- Did I detect state in Phase 0, or did I blindly restart someone mid-setup?
- Did I drive the tour (point out the one thing per file), or just paste links?
- Did I get them to the Phase 5 file-landing aha, or stop at reading?
- Did I hand over the operating manual (Phase 5.5) and walk the two live sections, or just link it?
- Did I end on a single dated next action?
- Did I check the live repo README is still the source of truth (re-sync the tour-script if the repo's tour changed)?

---

