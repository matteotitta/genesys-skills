<p align="center">
  <strong>genesys-skills</strong>
</p>

<p align="center">
  Production-grade Claude Code skills for B2B SaaS GTM.<br/>
  Shared weekly via the <a href="https://newsletter.genesysgrowth.com">GTM Engineer newsletter</a>.
</p>

<p align="center">
  <a href="https://newsletter.genesysgrowth.com"><img alt="Subscribe" src="https://img.shields.io/badge/Subscribe-Newsletter-6400D7?style=flat-square"></a>
  <a href="https://genesysgrowth.com"><img alt="Website" src="https://img.shields.io/badge/Website-genesysgrowth.com-181723?style=flat-square"></a>
  <a href="https://linkedin.com/in/matteotittarelli"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Matteo_Tittarelli-0A66C2?style=flat-square"></a>
</p>

---

## What are skills?

Skills are structured prompts for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's agentic coding tool. Think of them as reusable playbooks that turn Claude into a specialist operator for specific tasks.

Each skill includes:
- **SKILL.md** — the core prompt with process steps, quality gates, and output format
- **references/** — templates, schemas, examples, and search patterns the skill uses

Drop a skill into your `.claude/skills/` directory and invoke it with `/skill-name`.

## Skills

| Skill | Description | Added |
|-------|-------------|-------|
| [competitor-research](skills/competitor-research/) | Deep 13-dimension competitor analysis for B2B SaaS. Covers company, product, ICP, pricing, reviews, content, launches, SEO/AEO, technographics, hiring signals, GTM motion, social, and paid advertising. Includes templates, schemas, and real examples. | Mar 2026 |

## How to use

### 1. Clone or download a skill

```bash
# Clone the whole repo
git clone https://github.com/matteotitta/genesys-skills.git

# Or download a specific skill folder
```

### 2. Copy into your Claude Code project

```bash
# Copy the skill into your project's .claude/skills/ directory
cp -r genesys-skills/skills/competitor-research .claude/skills/
```

### 3. Use it

In Claude Code, the skill will auto-trigger when you mention competitor analysis, or you can invoke it directly:

```
/competitor-research
```

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (Anthropic's CLI)
- Some skills use MCP integrations (Apify, Firecrawl, Ahrefs) for richer data — these are optional. The skill will work without them, just with less coverage.

## About

These skills are built and battle-tested at [Genesys Growth](https://genesysgrowth.com) — a B2B SaaS GTM consultancy that helps Series A-B startups with positioning, messaging, content, and launches.

Each skill has been used across 45+ client engagements and refined through real feedback. They're the same skills we use daily with Claude Code to deliver client work.

New skills are shared weekly via the [GTM Engineer newsletter](https://newsletter.genesysgrowth.com). Subscribe to get them as they drop.

## License

MIT — use them however you want.
