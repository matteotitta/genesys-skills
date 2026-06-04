# The quiz — 8 questions → level + 4 pillars

The zero-setup front door. Ask all 8 in **one** `AskUserQuestion` call (it supports multiple questions, each rendered as clickable options). Keep the copy fun and fast. Each option carries a `(pillar, rung)` tag used for scoring.

Map each option's letter to the tag in the **Scoring map** at the bottom. Then run **Reconciliation**.

---

## The questions

**Q1 — Does Claude know who you are?** *(header: CLAUDE.md)*
- a) Nope — I just type prompts into the terminal
- b) I've got a CLAUDE.md with my basics in it
- c) My CLAUDE.md is detailed — preferences, project context, output rules
- d) My CLAUDE.md routes to memory files / rules / an ontology — it's an index, not a doc

**Q2 — Can Claude reach your real tools?** *(header: MCPs)*
- a) No — I copy-paste context in
- b) One or two MCPs wired (Drive, Slack, or similar)
- c) Three or more MCPs across data + comms + dev
- d) A deep MCP stack — incl. browser control + output routing to live destinations

**Q3 — Have you built reusable commands (skills)?** *(header: Skills)*
- a) No — I re-explain tasks each session
- b) A couple of simple skills
- c) Several skills I run regularly (`/research`, `/review`, etc.)
- d) Multi-phase skills + authored plugins; some skills call other skills

**Q4 — Do you have a knowledge system Claude draws from?** *(header: Memory)*
- a) Just whatever's in the chat
- b) A CLAUDE.md, nothing structured beyond it
- c) Structured memory / patterns / rules Claude reads
- d) Full context engine — memory tool, ontology, hooks-as-enforcement, recall

**Q5 — Do your skills work together / use subagents?** *(header: Orchestration)*
- a) Each task is one-shot, manual
- b) I use subagents now and then
- c) Skills chain (one feeds the next) + hooks gate quality
- d) Role-agents + worktrees + `/workflows` running parallel agents

**Q6 — Do you run Claude from scripts (not just the terminal)?** *(header: Headless)*
- a) Always interactive — I type, I wait
- b) I've tried `claude -p` once or twice
- c) I have scripts that call Claude headless + pipe JSON
- d) Claude is a component in my stack — Agent SDK, CI, data pipelines

**Q7 — Does Claude control a browser?** *(header: Browser)*
- a) No
- b) Tried it once
- c) I have a scrape / screenshot / PDF workflow
- d) Full research pipelines: crawl the web → synthesize → deliverable

**Q8 — Does Claude run without you sitting there?** *(header: Always-on)*
- a) No — it only runs when I open it
- b) I've scheduled a task once or twice
- c) Scheduled agents / background jobs run on a cadence
- d) Autonomous loops — agents spawning + managing other agents

---

## Scoring map — option → (pillar, rung cleared)

Each option clears the rung shown (and, cumulatively, all rungs below it for that signal). "—" means it clears nothing for that signal.

| Q | a | b | c | d | Pillar |
|---|---|---|---|---|--------|
| Q1 | rung 0 | rung 1 | rung 1 | rung 4 | Context |
| Q2 | rung 0 | rung 1 (partial) | rung 2 | rung 7 | Integrations |
| Q3 | rung 0 | rung 1 (partial) | rung 3 | rung 6 | Skills |
| Q4 | rung 0 | rung 1 | rung 4 | rung 4+ | Context |
| Q5 | rung 0 | rung 1 | rung 5 | rung 8 | Orchestration |
| Q6 | rung 0 | rung 1 | rung 6 | rung 6 | Skills/Integrations |
| Q7 | rung 0 | rung 1 | rung 7 | rung 7 | Integrations |
| Q8 | rung 0 | rung 1 | rung 9 | rung 10 | Orchestration |

Note: Q2-b is "rung 1 (partial)" — one or two MCPs does NOT clear rung 2 (Plugged needs 3+). Q3-b similarly partial.

---

## Reconciliation

1. **Per-pillar sub-score (0-4).** For each pillar, take the highest rung its answers clear, then map to the 0-4 rubric in [`levels.md`](levels.md):
   - Context: from Q1 + Q4. Skills: Q3 + Q6. Integrations: Q2 + Q6 + Q7. Orchestration: Q5 + Q8.
   - Convert the highest cleared rung for that pillar to its 0-4 band per the `levels.md` per-pillar rubric.

2. **Overall level (0-10).** The ladder is cumulative. Walk rungs 1→10; the person is at level **N** if they clear rung N's signal **and** every lower rung's signal. Stop at the first rung they fail — that's the gap; their level is one below it.
   - Rung-clear check uses the highest option per the relevant question(s): L1←Q1≥b, L2←Q2=c/d, L3←Q3=c/d, L4←Q4=c/d, L5←Q5=c/d, L6←Q6=c/d, L7←Q7=c/d, L8←Q5=d, L9←Q8=c/d, L10←Q8=d.
   - **One skipped pillar is allowed** — if a person clears L6 but not L4 (scripts but thin context), don't hard-stop at L3; score the overall at the gap but call the skipped pillar out in the dual lens (per `levels.md` detection notes). Use judgment: a genuine skip vs. a real gap.

3. **Present** the level + name + vibe + the 4 pillar bars, then continue to the roadmap (Phase 2) per the SKILL.md flow.

The quiz is a faster, slightly coarser read than the scan. If the person later has a real setup, suggest re-running with `--assess` for the precise version.
