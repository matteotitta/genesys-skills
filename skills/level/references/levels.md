# The 10 levels — calibrated to the 4 systems pillars

Source of truth for both front doors (quiz + scan). The single 0-10 score is the headline; the 4-pillar breakdown is the dual lens. Level 10 is the documented ceiling in [`benchmark.md`](benchmark.md).

The 4 pillars (from the marketing-quickstart 4-systems framework):

- **Context** — the data Claude reads: CLAUDE.md, memory, rules, ontology, hooks-as-enforcement.
- **Skills** — the producers: reusable skills/commands that do the work.
- **Integrations** — the connectors: MCPs (plugins + `.mcp.json`) wiring Claude to real tools.
- **Orchestration** — the coordinators: subagents, chains, agents, worktrees, schedules.

Early rungs build one pillar; later rungs compose them; Level 10 maxes all four.

---

## The ladder

| Lvl | Name | Vibe | Dominant pillar(s) | What it means (plain English) |
|-----|------|------|--------------------|-------------------------------|
| 0 | **Tourist** | just passing through | — | Just installed it. Typing prompts like it's ChatGPT in a terminal. No setup, no config. Everyone starts here. |
| 1 | **Marked** | planted your flag | Context | You wrote a CLAUDE.md, so Claude actually knows who you are and what you want. You know the core commands. This alone is a huge jump. |
| 2 | **Plugged** | wired to your tools | Integrations | Claude reads your real tools — Slack, Drive, Notion, Gmail — through 3+ MCPs. No more copy-pasting context. |
| 3 | **Skilled** | has a toolkit | Skills | You've built reusable skills you run regularly. Instead of re-explaining a task every session, you type `/research` and it runs. |
| 4 | **Architect** | designs the system | Context (deep) | A structured knowledge system: memory, patterns, rules, ontology, client profiles. Output improves over time because Claude draws from everything you've taught it. |
| 5 | **Conductor** | runs the orchestra | Orchestration | Skills chain into each other. Subagents do parallel work. Hooks gate quality. Output styles shape voice. Claude feels like a team, not a tool. |
| 6 | **Machinist** | builds the assembly line | Skills + Integrations | You call Claude from scripts — headless mode, JSON output, the Agent SDK, authored plugins. Claude is a component in your stack, not just a chat window. |
| 7 | **Hunter** | sends Claude into the wild | Integrations | Claude controls a browser — scrapes, screenshots, generates PDFs/decks, runs research pipelines that crawl the web and turn findings into deliverables. |
| 8 | **Ringleader** | commands a team of agents | Orchestration | Multiple Claude instances + role-agents working in parallel via worktrees and `/workflows`. You coordinate them like a tech lead. |
| 9 | **Nightshift** | works while you sleep | Orchestration + Integrations | Claude runs on a schedule whether you're at your desk or not — scheduled agents, background tasks, monitoring. It's infrastructure now. |
| 10 | **Swarm** | the apex | all four, maxed | Agents that manage agents, autonomous loops, the full orchestration stack. The documented ceiling (see `benchmark.md`). Genuinely rare. |

Most people land 1-4. Level 5 is strong. Level 7+ is rare.

---

## Per-pillar 0-4 sub-score rubric (the dual lens)

Each pillar is scored 0-4 independently. The dashboard renders these as bars so the gap is obvious.

| Score | Context | Skills | Integrations | Orchestration |
|-------|---------|--------|--------------|---------------|
| 0 | No CLAUDE.md | No custom skills | No MCPs | Everything manual, one-shot |
| 1 | CLAUDE.md exists | 1-2 skills | 1-2 MCPs | Uses subagents occasionally |
| 2 | + rules / memory referenced | 3+ skills used regularly | 3+ MCPs across categories | Skills chain; hooks as gates |
| 3 | Structured memory + ontology + hooks; CLAUDE.md routes to them | Multi-phase skills; skills call skills; plugins authored | Browser MCPs + output routing; committed `.mcp.json` | Role-agents + worktrees + `/workflows`; parallel agents |
| 4 | Full context engine (memory tool, recall, sync, the lot) | Large governed catalog with validation + auto-sync | Deep MCP stack both input + output, credit-gated | Scheduled/background agents; agents managing agents |

A pillar's sub-score = the highest row it fully clears.

---

## Scoring rule (overall level)

The overall level is the **highest rung where the environment meets ALL of that rung's required signals** (below). You can't be Level 6 with no Level 4 context — the ladder is cumulative, with the one allowed exception that a person may skip a pillar they genuinely don't need (note it, don't punish it twice).

### Scan checklist — signals per level

```
L1 Marked        CLAUDE.md exists in any location (CLAUDE.md, .claude/CLAUDE.md,
                 CLAUDE.local.md, ~/.claude/CLAUDE.md). Knows core slash commands.
L2 Plugged       3+ working MCP servers across .mcp.json + user config + plugins.
                 Pulling real data into sessions (data / comms / dev / browser categories).
L3 Skilled       3+ custom skills in .claude/skills/ or .claude/commands/, used regularly.
L4 Architect     Structured memory (memory tool OR memory/ dir with patterns/examples),
                 rules, and/or ontology that CLAUDE.md references + routes to.
                 Context architecture, not just a config file.
L5 Conductor     Multi-phase skills (chains: output of one feeds another). Subagent usage
                 OR agent defs in .claude/agents/. Hook configs as quality gates.
                 Output styles in use.
L6 Machinist     Shell scripts / automation calling `claude -p`; JSON output piping;
                 Agent SDK; authored plugins. Programmatic, not just interactive.
L7 Hunter        Browser MCP (Chrome DevTools / Playwright / Puppeteer). Screenshot /
                 PDF / scrape → deliverable pipelines.
L8 Ringleader    Parallel CC instances OR git worktrees for agents; role-agents with
                 distinct roles; /workflows orchestration.
L9 Nightshift    Scheduled tasks running CC (cron / launchd / /schedule). Background
                 agents (pm2 / systemd / background tasks). Persistent infra.
L10 Swarm        Autonomous loops; multi-agent orchestration framework; agents spawning
                 + managing agents; safety boundaries + rollback. = benchmark.md.
```

### Detection notes

- **Quantity ≠ level.** 50 one-line skills is still Level 3. Complexity + integration between components is what moves rungs. A skill that orchestrates subagents is worth more than ten that don't.
- **CLAUDE.md depth bands:** <10 lines = minimal, 10-50 = basic, 50-150 = solid, 150+ = advanced (+ references memory/patterns/workflows, navigation tables, progressive disclosure).
- **Hooks are quality gates, not infrastructure** — they count toward L5 (Orchestration), not L9.
- When a person clears a high pillar but skips a lower one (e.g. headless scripts but thin context), score the overall level at the gap and call out the skipped pillar in the dual lens. Don't silently round up.
