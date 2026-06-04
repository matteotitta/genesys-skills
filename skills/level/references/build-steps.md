# Build it now — Phase 3 actions per level

If the person says yes to "build the first step now," execute the action matching their assessed level. Adapt to the person — never paste a template verbatim. Build the actual file/config in their environment.

---

## At Level 0 → build a CLAUDE.md

Create a CLAUDE.md in the project root using their 3 context-question answers. Sections: About (role + main work + key tools detected), Communication Style, Project Context, Output Rules (address their stated friction), What I Want to Automate (their Q3 answer as a checklist). Make it specific to them, not generic.

## At Level 1 → wire the first MCP

From their main-work answer, recommend + set up their first MCP. Prefer a **plugin** (deferred, zero startup cost) over raw config. If config: create/update `.mcp.json` (project-scope). Walk authentication. Test with a real query. Then nudge toward 3+ to reach Plugged.

## At Level 2 → write the first skill

From their Q3 (what they'd automate): create `.claude/skills/{name}/SKILL.md` (or `.claude/commands/{name}.md`) for that exact use case. Frontmatter + steps + output format + rules. Run it once. Suggest 2-3 more skills to build next.

## At Level 3-4 → scaffold the memory architecture

Set up the memory tool and/or a `memory/` tree (company / customers / patterns / examples). Seed with their top patterns + 1-2 reference outputs. Update CLAUDE.md to route to it (navigation table + "before starting work" rule). Show the feedback loop (extract patterns post-project).

## At Level 4-5 → upgrade a skill to multi-phase + add a hook

Take their most-used skill; rewrite it with phases + approval gates + a subagent call. Reference their memory/patterns for consistency. Then add one quality-gate hook (e.g. a PreToolUse hook blocking writes to `.env`, or a PostToolUse auto-lint). Optionally set an output style.

## At Level 5-6 → write the first automation script

Create a shell script that calls `claude -p` for a routine task, with `--allowedTools` scoped. Test end-to-end. Show how to schedule it (cron / `/schedule`) or run on demand. (Remember: headless takes plain-text prompts, not slash commands.)

## At Level 6+ → an advanced optimization pass

Pick the highest-leverage one:
1. **Context-budget audit** — how much context is consumed at startup? Trim unused MCPs (prefer deferred plugins).
2. **Skill-architecture review** — which skills could chain? Build the connections.
3. **Memory health check** — stale files / outdated patterns? Prune.
4. **MCP health check** — does every configured MCP still work? Test each.
5. **Pipeline review** — where could headless / `/workflows` replace interactive sessions?
6. **Orchestration upgrade** — introduce worktrees, role-agents, or a `/workflows` fan-out for parallel work; or a scheduled agent for a recurring task.
