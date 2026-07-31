---
name: opportunity-scan
version: '1.0'
last_updated: 2026-05-25
author: genesys-growth
description: 'Scans skill-usage.jsonl + recall.db transcripts for opportunities to create new skills, deprecate unused ones, or formalize manual patterns into workflows. Detects three signal classes: repeated manual sequences not covered by existing skills, skills used <2× in 30 days (deprecation candidates), high-friction sessions (long single-tool chains). Outputs 1-3 weekly candidates to project-root OPPORTUNITIES.md. Triggers: "opportunity-scan", "scan for new skills", "find missing skills". The consumer side of skill-usage-logger.sh''s producer. NOT for external pattern discovery — use /steal.'
goal: Detect opportunities to create new skills, deprecate unused ones, or formalize manual patterns into workflows based on actual usage telemetry.
outcome: 1-3 candidates per week written to OPPORTUNITIES.md with rationale + skill spec + evidence (session IDs from recall.db).
primitive: meta
sub_primitive: learning
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended: []
- type: runbook
  feeds_into:
  - weekly-plan
  - skill-catalog
depends_on: []
- weekly-plan
- skill-catalog
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: medium
disable-model-invocation: true
---

# /opportunity-scan — detect skill + workflow opportunities from usage telemetry

Scan local telemetry (`skill-usage.jsonl` + `recall.db`) to surface 1-3 weekly opportunities for new skills, deprecations, or workflow formalizations. Internal self-improvement loop — paired with `/steal` (external pattern discovery) and `/system-health` (infrastructure health).

## Where it runs — local launchd cron, NOT a cloud Routine

Critical architecture note: this skill consumes `.claude/sessions/skill-usage.jsonl` and `.claude/sessions/recall.db`, both of which are **gitignored** (they're per-session telemetry, not committed). A cloud Routine running from a fresh git checkout would have no access to them.

Solution: a local `launchd` cron job at `.claude/automation/opportunity-scan/com.genesys.opportunity-scan.plist` fires the scan every Sunday at 17:00 JST. The job invokes `claude --print` against the project so the full local toolchain is available (Slack MCP for the DM, local file access for telemetry).

Install:
```bash
cp.claude/automation/opportunity-scan/com.genesys.opportunity-scan.plist \
   ~/Library/LaunchAgents/com.genesys.opportunity-scan.plist
launchctl unload ~/Library/LaunchAgents/com.genesys.opportunity-scan.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.genesys.opportunity-scan.plist
```

Verify:
```bash
launchctl list | grep opportunity-scan
tail -f /tmp/genesys-opportunity-scan.log
```

If your machine is asleep at 17:00 Sunday, launchd fires the job on next wake — never strictly missed, just delayed.

Sibling skills + boundary: see `.claude/rules/orchestration-patterns.md` and the plan file `~/.claude/plans/<plan>.md` §10.

## Detection signal classes

### Class 1 — Repeated manual sequences not covered by existing skills

Same multi-tool sequence appears in 3+ sessions where no Skill followed.

**Detection:**
- Query `recall.db` for tool sequences of length 4+
- Cross-reference `skill-usage.jsonl` to confirm no skill invocation accompanied the sequence
- Cluster by shape (sequence of tool names ignoring args)
- Surface clusters with frequency ≥3

**CYCLE-1 LEARNING:** Ignore `Bash×4` 4-grams as noise (1192 occurrences in 7 days — Bash is the universal escape hatch). Look for **mixed-tool** 4-grams (e.g., `Read → Grep → Bash → Edit`).

### Class 2 — Skills used <2× in 30 days (deprecation candidates)

Catalog skills rarely invoked. Surfaced for KILL verdict.

**Detection:**
- Glob `.claude/skills/**/SKILL.md` for the catalog
- Per skill: count invocations in `skill-usage.jsonl` over last 30 days, summing both `source: "skill-tool"` (PostToolUse Skill capture) AND `source: "slash"` (UserPromptSubmit capture)
- Surface skills with count < 2 AND catalog age > 30 days (grace period — never flag a skill less than 30 days old)

**CYCLE-1 LEARNING:** Depends on `skill-usage.jsonl` capturing slash-command invocations. This was DARK in cycle 1 (only `Skill` tool captured). Now resolved via `.claude/hooks/slash-command-logger.sh` (UserPromptSubmit). Source field disambiguates the two capture paths.

### Class 3 — High-friction sessions (long single-tool chains)

Sessions with consecutive same-tool invocations indicating a friction point that could be a skill.

**Detection:**
- Query `recall.db` for sessions where the same tool fires N+ consecutive times
- Threshold: **8** for MCP tools (credit-gated, slower), **15** for built-in tools (cheaper, faster)
- Flag the session ID + tool name + chain length

**CYCLE-1 LEARNING:** The Apify cycle-1 finding (29× `mcp__apify__fetch-actor-details` in one session) was a class-3 hit at threshold 8. The 29× was visible because the chain happened in a single session — no need for cross-session detection.

## Process — 7 phases

### Phase 1 — Load

Read in parallel:
- `.claude/automation/opportunity-scan/state.json` — `last_run_at`, runs counter, window config
- `.claude/automation/opportunity-scan/opportunity-scan-strategy.md` — scratchpad (decisions locked / things to stop doing / definitions refined)
- `.claude/sessions/skill-usage.jsonl` — filter to last 7 days (per `--window 7d` default)
- `.claude/sessions/recall.db` — query sessions in same window
- `OPPORTUNITIES.md` — read existing entries to dedupe (match on suggested skill name)

### Phase 2 — Detect (3 classes in parallel)

Run the three signal-class detectors against the loaded telemetry. Each emits raw candidates with evidence.

### Phase 3 — Rank

Per candidate, score on 3 dimensions (each 0-3):
- **Frequency** — how often does this pattern fire? (3 = ≥5 occurrences/week, 2 = 3-4, 1 = 2, 0 = 1)
- **Friction** — how costly is the unautomated path? (3 = credit-gated MCP or 15+ tool calls, 2 = noticeable but cheap, 1 = trivial, 0 = no friction)
- **Coverage gap** — is there NO existing skill that covers it? (3 = no skill, 2 = adjacent skill exists but doesn't fit, 1 = partial coverage, 0 = covered)

Total = /9. **Surface candidates with ≥5/9. Cap at 3 per run.**

### Phase 4 — Spec

For each surfaced candidate, generate:
- `Name:` kebab-case (`/<name>`)
- `Purpose:` one line
- `Primitive / sub_primitive:` best guess (see `.claude/rules/ontology.md`)
- `Build estimate:` S (<1 day), M (1-3 days), L (4+ days)

### Phase 5 — Write

Append entries to repo-root `OPPORTUNITIES.md` matching the template at lines 12-24. **Skip duplicates** — if an entry with the same suggested skill name already exists, don't re-surface (the entry might be DEFERred or KILLed by Matteo).

### Phase 6 — Scratchpad

Update `.claude/automation/opportunity-scan/opportunity-scan-strategy.md` per the `.claude/rules/iterative-strategy-scratchpad.md` discipline:
- New "decisions locked" entries (only if Matteo's feedback this cycle warrants)
- New "things to stop doing" entries (suppress patterns that surfaced wrong)
- "Open questions for next cycle" — what to investigate next time
- Cycle-N findings — counts + key observations from this run

### Phase 7 — State writeback

Update `.claude/automation/opportunity-scan/state.json`:
- `last_run_at` — ISO timestamp
- `runs` += 1
- `candidates_surfaced_this_run` — count this cycle
- `candidates_surfaced_lifetime` += count this cycle
- `consecutive_zero_correction_runs` — for approval-loop discipline (see Constraints)

## Subcommands

### `/opportunity-scan` (default)
Run the full 7-phase scan against the default 7-day window. The cloud Routine fires this on Sunday cron.

### `/opportunity-scan review`
Inline-review mode. Read `OPPORTUNITIES.md`, find pending entries (those with `Verdict (Matteo to set):` placeholder unchanged), and walk Matteo through verdicting one by one:

```
Candidate N/M — /<name> (<signal-class>, <score>/9)

Pattern: <one-line>
Suggested build: <S/M/L>. Primitive: <primitive>/<sub_primitive>.
Evidence: session <id> + N others.

Verdict? [B]uild [D]efer [K]ill [S]kip
```

On `B` / `D` / `K`: edit OPPORTUNITIES.md in place — replace `Verdict (Matteo to set): BUILD / DEFER / KILL` with `Verdict: BUILD` (or DEFER/KILL). Optionally prompt for one-line rationale.

On `S`: leave the entry untouched (still pending for next cycle).

Precedent: `/discover status`, `/discover dismiss <name>`, `/discover built <name> <path>` — same subcommand pattern.

## Constraints

- **Read-only on telemetry.** Never modify `skill-usage.jsonl` or `recall.db`.
- **Cap 3 candidates per run.** Past 3, save the rest for next cycle (better signal-to-noise per OPPORTUNITIES.md review).
- **Respect the scratchpad's locked decisions.** Per `.claude/rules/iterative-strategy-scratchpad.md`: cycle 2+ reads "things to stop doing" first and suppresses matching patterns.
- **Approval-loop discipline.** Per `.claude/rules/approval-loop-pattern.md`: if 3 consecutive weeks pass with zero BUILD verdicts (all DEFER or KILL), the routine flags itself in the scratchpad and recommends retuning detection thresholds.
- **Never use the word "substrate"** — per `.claude/rules/auto-memory.md`.

## Integration with other skills

- **Producers:** `.claude/hooks/skill-usage-logger.sh` (PostToolUse + Skill captures), `.claude/hooks/slash-command-logger.sh` (UserPromptSubmit captures), `.claude/hooks/session-indexer.py` (writes recall.db).
- **Consumers:** Matteo (Sunday review), `/weekly-plan` (reads OPPORTUNITIES.md alongside Linear when building the week).
- **Sibling routines:** `/steal weekly` (external pattern discovery — different signal source), `/system-health` (infrastructure health — different signal source). Boundary documented in the plan §10.

## Anti-patterns

- ❌ Don't run /opportunity-scan as the user's first action of the week to "see what came up" — it's a scheduled cloud Routine; opening OPPORTUNITIES.md is faster.
- ❌ Don't auto-build BUILD-verdicted candidates. Build them deliberately in a separate session via `/skill-creator`.
- ❌ Don't surface candidates from the with-space project dir if those sessions are stale (the cleanup of 2026-05-18 emptied that dir).
- ❌ Don't conflate "skill not invoked" with "skill not useful" — newly-built skills need a 30-day grace before deprecation flag fires.

