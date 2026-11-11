# Contributing

## Repo structure

```
skills/
└── skill-name/
    └── SKILL.md          ← the whole skill
```

Each skill is one folder with one file. Drop the folder into `.claude/skills/` and it works.

## Skill format

Skills use YAML frontmatter plus markdown:

```yaml
---
name: skill-name
description: What the skill does and when to use it.
---

# Skill title

When to run, inputs, steps, and what good looks like.
```

## Requests and bugs

To suggest a skill or report a problem, [open an issue](https://github.com/matteotitta/genesys-skills/issues) with:
- Which skill
- What went wrong
- Your Claude Code version
