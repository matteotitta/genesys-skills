<p align="center">
  <strong>genesys-skills</strong>
</p>

<p align="center">
  Production-grade Claude Code skills for B2B SaaS GTM.<br/>
  Shared weekly via the <a href="https://newsletter.genesysgrowth.com">Genesys newsletter</a>.
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
| [icp-research](skills/icp-research/) | 12-section ideal customer profile research for B2B SaaS. Produces TAM analysis, firmographic segments, champion and economic buyer persona deep-dives, negative ICP, intent signals, voice of customer synthesis, and segment-level recommendations. Includes dimension schemas, output templates, search patterns, and a worked Strapi example. | Apr 2026 |
| [tov-guidelines](skills/tov-guidelines/) | Two-phase tone of voice extraction for B2B SaaS. Phase 1 scrapes 15-20 pages to extract sentence, paragraph, word, and structural patterns with frequency scores. Phase 2 generates codified voice rules with source attribution. Includes analysis template, guidelines template, founder interview questions, and Genesys Growth examples. | Apr 2026 |
| [brand-kit](skills/brand-kit/) | Screenshot-first visual identity extraction for B2B SaaS. Produces an 8-section brand system file: visual identity description, colors, typography, components, data viz, logo usage, spacing, and signature elements. Confidence-scored tokens (0-5). Includes brand kit template and worked examples (Genesys Growth, Cursor). | Apr 2026 |
| [case-study](skills/case-study/) | Customer success story builder for B2B SaaS. Produces a structured narrative with hook, problem context, solution detail, quantified results, customer quotes, and distribution-ready excerpts (LinkedIn version, newsletter blurb, sales pull-quote). Forces metric specificity and marks unverifiable claims as `[UNAVAILABLE]` rather than inventing them. Pulls voice from your locked TOV. | May 2026 |
| [battlecards](skills/battlecards/) | Sales-floor competitive battlecard generator for B2B SaaS. Produces 1-page references per competitor: positioning, threat tier, where they win, where you win, top 3-5 objections with handlers, comparison angles, and quick-frame elevator pitches. Designed for AE consumption mid-deal — scannable in 60 seconds. Supports refresh-from-call-transcript mode for keeping battlecards current as deals evolve. | May 2026 |
| [level](skills/level/) | Claude Code maturity scorecard. Scores any Claude Code environment 0-10 across 4 systems (Context / Skills / Integrations / Orchestration), each 0-4. Two front doors: an 8-question quiz for beginners, a silent file scan for advanced users. Hands back a single-next-level roadmap calibrated to current Anthropic features (plugins, /workflows, subagents, hooks, scheduled agents, the Agent SDK, output styles, worktrees, the memory tool) plus a branded, shareable HTML dashboard or paste-anywhere ASCII card. Level 10 is anchored to the documented ceiling, so the score is honest, not inflated. | Jun 2026 |
| [win-loss](skills/win-loss/) | Win/loss analysis for B2B SaaS. Analyzes sales call transcripts across 6 dimensions (product, messaging, GTM/sales, pricing, competition, customer context) to extract why deals are won, lost, retained, or churned. Produces aggregate patterns with frequency counts, confidence levels, and strategic recommendations. Forces every finding to cite a verbatim quote and labels single-call patterns as unconfirmed rather than inventing trends. Includes the 3-phase process, output template, quality checklist, extraction patterns, and a worked 5-transcript example. | Jun 2026 |

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

These skills are built and battle-tested at [Genesys Growth](https://genesysgrowth.com) — a B2B SaaS GTM consultancy that helps Series A-C startups with positioning, messaging, content, and launches.

Each skill has been used across 50+ client engagements and refined through real feedback. They're the same skills we use daily with Claude Code to deliver client work.

New skills are shared weekly via the [Genesys newsletter](https://newsletter.genesysgrowth.com). Subscribe to get them as they drop.

## License

MIT — use them however you want.
