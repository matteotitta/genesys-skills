---
name: plugin-scaffold
version: '1.0'
last_updated: 2026-04-19
author: genesys-growth
description: 'Scaffolds a Claude Code / Cowork plugin bundle from a short YAML spec or from an existing agent definition''s
  skills list. Produces the canonical bundle layout (.claude-plugin/plugin.json, settings.json with default agent, agents/,
  commands/, skills/ as symlinks to canonical sources in.claude/skills/, README, examples/). Use when creating a new personal
  plugin bundle in projects/apps/genesys-plugins/ or promoting an existing agent into a distributable plugin. Triggers: "scaffold
  a plugin", "create a bundle", "package [agent-name] as a plugin", "new plugin bundle". NOT for editing canonical skills
  — that stays in.claude/skills/. NOT for publishing to a marketplace — use a separate publish step.'
goal: Scaffolds a Claude Code / Cowork plugin bundle from a short YAML spec or from an existing agent definition's skills
  list.
outcome: Scaffolds a Claude Code / Cowork plugin bundle from a short YAML spec or from an existing agent definition's skills
  list. Produces the canonical bundle layout (.claude-plugin/plugin.json, settings.json with default agent, agents/, commands/,
  skills/ as symlinks to canonical sources in...
primitive: meta
sub_primitive: infra
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended: []
- type: runbook
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: low
---

# /plugin-scaffold — Scaffold a plugin bundle

Generates a fresh plugin bundle under `projects/apps/genesys-plugins/bundles/{bundle-name}/` following the canonical Claude Code plugin format. Symlinks skills from `.claude/skills/` so the bundle stays in sync with canonical sources.

---

## Claude Code triggers

**Invoke when user says:**
- "scaffold a plugin for [agent/workflow]"
- "create a new bundle"
- "package [agent-name] as a plugin"
- "bundle these skills together:..."
- "new plugin bundle: [name]"

**Do NOT invoke when:**
- User wants to edit a skill (canonical sources stay in `.claude/skills/` — edit there)
- User wants to publish a bundle to a public marketplace (that's a separate publish step)
- User is asking about the Claude Code plugin *format* in general (answer from context, don't scaffold)

---

## Inputs

The skill accepts a bundle spec in one of two forms:

### Form 1 — Inline spec

```yaml
bundle: linkedin-engine
description: "Personal LinkedIn content engine. Voice memo or thought → drafted post on brand in 60s."
agent: social-marketer # defaults to bundle name if omitted
author: genesys-growth
version: "0.1.0"
skills:
  - content-skills/linkedin-skills/linkedin-hooks
  - content-skills/linkedin-skills/linkedin-expert-posts
  - content-skills/linkedin-skills/linkedin-personal-posts
  # … add more paths relative to.claude/skills/
commands:
  - name: draft-from-thought
    description: "Turn a raw thought into a voice-checked LinkedIn post."
  - name: weekly-batch
    description: "Run the weekly content batch."
cowork_ready: true # false if any skill or MCP is local-only
resale_candidate: true # leave true so a future voice-scrub fork stays on the table
```

### Form 2 — From an existing agent

If the user says "package the social-marketer agent as a plugin", read `.claude/agents/{agent-name}.md`. The frontmatter already has a `skills:` list — use it. Prompt the user for bundle name + description only.

---

## Process

1. **Validate inputs** — bundle name kebab-case, all listed skill paths exist under `.claude/skills/`, target folder doesn't already exist (else ask to overwrite).
2. **Create folder structure**:
   ```
   projects/apps/genesys-plugins/bundles/{bundle}/
   ├──.claude-plugin/plugin.json
   ├── settings.json
   ├── README.md
   ├── agents/{agent}.md (copy + adapt from.claude/agents/{agent}.md)
   ├── commands/{each}.md
   ├── skills/ (symlinks to.claude/skills/...)
   └── examples/ (empty placeholder + README)
   ```
3. **Render `plugin.json`** from the premium reference using the spec.
4. **Render `settings.json`** with `"agent": "{agent}"` as the default.
5. **Copy + adapt the agent definition** from `.claude/agents/{agent}.md`. Keep the body. Strip the `skills:` frontmatter (Cowork doesn't read it the same way). Add a short "Bundle context" section referencing the plugin name.
6. **Create symlinks** for each skill: `ln -s {absolute-path-to-.claude-skill} skills/{skill-name}`. Use absolute paths so symlinks survive bundle moves.
7. **Stub each command** under `commands/` with a frontmatter + description. Leave the body as a TODO marker for the user to fill with the opinionated chain.
8. **Render `README.md`** from the premium reference with the bundle name, description, skill list, and install command.
9. **Update the top-level `projects/apps/genesys-plugins/marketplace.json`** to include the new bundle.
10. **Report** the created paths and a 1-line install command the user can run to test the bundle locally.

---

## Verification

- `plugin.json` parses as valid JSON (run `python3 -c "import json; json.load(open('path/to/plugin.json'))"`).
- All symlinks resolve (`ls -la bundles/{bundle}/skills/` shows no broken links).
- `marketplace.json` includes the new bundle entry.
- `README.md` renders correctly (no unresolved template variables like `{{bundle}}`).

---

## After completing work

Suggest the user:
1. Fill in the body of each stubbed command under `commands/`.
2. Seed `examples/` with 2-3 real outputs for in-context reference.
3. Test locally: `/plugin install file:///Users/matteotittarelli/Desktop/CORE/WORK/CLAUDE\ CODE/projects/apps/genesys-plugins {bundle-name}`.

