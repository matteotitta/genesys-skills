# The Level 10 benchmark — the documented ceiling

This is what "most advanced" actually looks like, so the score stays honest instead of flattering. Level 10 = a reference environment that maxes all four pillars **AND** uses the current Anthropic-native feature set. Score against THIS, not a vague community ideal.

**Last verified: 2026-06-03.** Refresh this file whenever Anthropic ships major Claude Code features, or the reference environment changes materially. One file to update — don't scatter "latest features" through the skill body.

---

## Part 1 — the reference environment (all four pillars, maxed)

A real, documented Genesys Growth setup. Use it as the concrete picture of each pillar at 4/4.

| Pillar | What the ceiling looks like |
|--------|------------------------------|
| **Context (4/4)** | 35+ auto-loaded rule files; a per-client folder ontology; memory tool + a session-recall index (SQLite FTS5, 17K+ messages); ambient sync-pull from Drive + Notion; CLAUDE.md as a lean index that routes to everything; hooks enforcing context rules (pre-commit, session-start, stale-context warnings). |
| **Skills (4/4)** | 150+ governed skills across 11 GTM primitives + research + meta; a JSON-schema'd frontmatter spec; auto-validation + auto-catalog regeneration on commit; skill-reviewer + voice-reviewer + design-reviewer quality gates; 60+ slash commands. |
| **Integrations (4/4)** | ~25+ MCPs (data, comms, dev, browser, research, finance) across user-scope + project-scope + plugins; credit-gated paid MCPs; committed project-scoped MCP config; MCPs on both the input (research) and output (publish) sides. |
| **Orchestration (4/4)** | 38 agents + 3 composite personas; 8 role-agents wired to a Paperclip control plane; Trigger.dev wave-batch orchestration; git worktrees for parallel agents; `/workflows` multi-agent fan-out; scheduled/cron jobs (launchd sync-pull); the 4 named orchestration patterns (sequential / fan-out / supervisor / consensus). |

If an environment matches this picture across all four columns, it's a 10.

---

## Part 2 — the current Anthropic-native feature ceiling

The features a top-tier setup uses today. Each maps to one or more pillars. Presence of the *advanced* features (worktrees, `/workflows`, scheduled agents, the Agent SDK, plugins) is what separates 8-10 from 5-7.

| Feature | Pillar | What it unlocks |
|---------|--------|-----------------|
| **CLAUDE.md** (multi-location, lean-index) | Context | Persistent identity + routing |
| **Memory tool** | Context | Cross-session persistent facts |
| **Hooks** (PreToolUse / PostToolUse / SessionStart / pre-commit / pre-compact) | Context + Orchestration | Quality gates + context refresh |
| **Skills** (`SKILL.md` + `references/`) | Skills | Reusable, governed producers |
| **Output styles** | Skills | Voice/format shaping per session |
| **MCPs** (plugins + `.mcp.json`, user + project scope) | Integrations | Real-tool access, in + out |
| **Plugins** (deferred-tool bundles) | Integrations + Skills | Zero-startup-cost distribution |
| **Subagents** (Agent tool; fresh vs fork) | Orchestration | Parallel specialist work |
| **Git worktrees** (incl. ephemeral agent worktrees) | Orchestration | Isolated parallel agents |
| **`/workflows`** (deterministic multi-agent fan-out) | Orchestration | Pipeline / fan-out / consensus harnesses |
| **Headless mode** (`claude -p`, JSON output) | Skills + Integrations | Scripted, pipeable Claude |
| **Agent SDK** | Skills + Integrations | Claude as an app component |
| **Scheduled agents** (`/schedule`, CronCreate, launchd/cron) | Orchestration | Runs on a cadence, unattended |
| **Background tasks** | Orchestration | Long-running unattended work |
| **Prompt caching + 1M context** | Context | Cheap, large stable context |

---

## How to use this file

- When presenting an assessment, anchor the top of the ladder here: "Level 10 isn't aspirational hand-waving — it's this documented setup running every current Anthropic-native feature."
- When someone is high (8-9), name which Part-2 features they're still missing vs. the ceiling.
- Never inflate a score because the person has *many* of something. The ceiling is about composition + the advanced features, not counts.
