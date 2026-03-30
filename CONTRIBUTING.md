# Contributing

## Repo structure

```
skills/
└── skill-name/
    ├── SKILL.md          ← Core skill prompt
    └── references/       ← Templates, schemas, examples
```

Each skill is a self-contained folder. Drop it into `.claude/skills/` and it works.

## Skill format

Skills use YAML frontmatter + markdown:

```yaml
---
name: skill-name
version: "1.0"
description: |
  When to use this skill.
---

# Skill title

Process steps, quality gates, and output format.
```

## New skills

New skills are added weekly via the [Genesys newsletter](https://newsletter.genesysgrowth.com). If you'd like to request a skill or suggest improvements, [open an issue](https://github.com/matteotitta/genesys-skills/issues).

## Bug reports

If a skill has issues (broken search patterns, outdated templates), please [open an issue](https://github.com/matteotitta/genesys-skills/issues) with:
- Which skill
- What went wrong
- Your Claude Code version
