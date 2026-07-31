---
name: linkedin-content-guide-founders
version: '1.0'
last_updated: 2026-03-17
author: genesys-growth
description: 'Builds a full founder-led or executive LinkedIn program for a client. Produces posting strategy, content pillars,
  SME content playbook, and engagement cadence. Triggers: "build a LinkedIn engine for [client]", "founder LinkedIn strategy",
  "SME content program", "LinkedIn content engine", "executive content program". Depends on linkedin-content-guide for the
  strategy layer. NOT for Matteo''s own LinkedIn posting — use linkedin-content-guide instead.'
goal: Builds a full founder-led or executive LinkedIn program for a client.
outcome: 'Builds a full founder-led or executive LinkedIn program for a client. Produces posting strategy, content pillars,
  SME content playbook, and engagement cadence. Triggers: "build a LinkedIn engine for [client]", "founder LinkedIn strategy",
  "SME content program", "LinkedIn content engine",...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 3
inputs:
  required:
  - linkedin-content-guide
  recommended:
  - linkedin-social-selling
  - linkedin-profile-optimization
  - linkedin-algo-audit
  - tov-guidelines
- type: runbook
  feeds_into: []
depends_on:
- linkedin-content-guide
owned_by_agent: content
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
effort: high
---

# LinkedIn Content Guide — Founders

Design and execute founder-led LinkedIn programs that turn LinkedIn into a pipeline channel for B2B SaaS companies. This skill orchestrates the full journey — from account health through scaled team content — for client founders and executives. For Matteo's own posting strategy, use `linkedin-content-guide` instead.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (program guide is client-team review surface — cleaned tags in appendix), R3 (founder-voice framing capability-led, not "thrilled"), R5 (founder long-form anchor cascades to short-form), R9 (verb-led headings).

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "build a LinkedIn engine for [client]"
- "founder LinkedIn strategy"
- "SME content program"
- "executive LinkedIn program"
- "thought leadership program for [client]"
- "scale [client]'s LinkedIn"
- "founder content playbook"
- "LinkedIn content engine"

**Do NOT invoke when:**
- User wants a single post for a founder → use `linkedin-content-guide` + client voice context
- User wants Matteo's own posting strategy → use `linkedin-content-guide`
- User wants LinkedIn Ads only → answer directly
- User wants social selling without content → use `linkedin-social-selling`

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Client/company** | Who we're building this for | User provides |
| **Primary SME** | Founder or executive leading the program | User provides |
| **ICP** | Ideal Customer Profile | User provides or from client CLAUDE.md |
| **Current state** | Existing LinkedIn presence, metrics, SSI | User provides |

### Optional (improve quality)

| Input | How it helps |
|-------|--------------|
| Business goals | Pipeline targets, awareness goals |
| Content history | What's worked/failed before |
| Tool stack | Existing marketing/sales tools |
| Budget | For ads, tools, production |
| Timeline | Program duration expectations |

**Validation:**
- [ ] Primary SME is identified and committed to the program
- [ ] ICP is clear enough to define content pillars
- [ ] Client has realistic timeline expectations (6+ months for full program)
- [ ] Account health check has been or will be run (Phase 0)

---

## Program Overview

| Phase | Timing | Focus |
|-------|--------|-------|
| **Phase 0: Account health** | Pre-program | SSI check, connection request audit, warmup protocol |
| **Phase 1: Foundation** | Month 1, Week 1 | Technical setup, SME selection, content pillars, profile optimization |
| **Phase 2: Content engine** | Month 1, Weeks 2-4 | Video production, graphics, engagement routine |
| **Phase 3: Optimization** | Month 2+ | Analytics, TWE scoring, LinkedIn Ads |
| **Phase 4: Scale** | Month 3+ | Multi-channel cascade, team scaling, social selling integration |

Phase 1-4 detail in the premium reference. Phase 0 (load-bearing operational constants) lives in body below.

---

## Phase 0: Account Health & Safety (Pre-Program)

**Before starting any program, verify account health.** These are voice-locked operational constants that affect every founder program.

| Metric | Target | Risk if below |
|--------|--------|---------------|
| Social Selling Index (SSI) | Above 70 | Flagged faster by LinkedIn |
| Pending connection requests | Under 700 | #1 spam signal |
| Connection acceptance rate | Above 30% | Auto-restriction |

**Connection limits (2026):**
- Weekly: 100-150 standard; 200-250 high-SSI Sales Nav
- Daily safe limit: 25 connections, 5 days/week
- Monthly capacity: 800-1000 outreach messages per account

**Account warmup (new or dormant accounts):**
- 6-8 week warmup before scaling
- Start: 5-10 manual connection requests daily
- Never scale automation before warmup complete
- Withdraw unaccepted requests every 2-4 weeks

**2026 InMail changes (CRITICAL):**
- Open InMail cap reduced ~87% (from ~800/month to under 100)
- Sales Navigator Core no longer sufficient for serious outbound
- Sales Navigator Advanced/Corporate now required
- Credits returned on responses — prioritize warm signals before cold lists

**Check SSI:** [linkedin.com/sales/ssi](https://www.linkedin.com/sales/ssi)

---

## Process

Phases 1-4 (Foundation → Content Engine → Optimization → Scale) cover the full 6+ month engagement. Each phase has its own checklists, cadences, and integration points with downstream skills (`linkedin-expert-posts`, `linkedin-personal-posts`, `linkedin-sales-posts`, `linkedin-comment`, `linkedin-social-selling`). Full step-by-step in the premium reference.

---

## Anti-Hallucination Guardrails

1. **Never invent metrics or results.** Use `[PLACEHOLDER]` for missing data.
2. **No fabricated case studies.** Only reference real client examples.
3. **Budget estimates must be marked.** Use "[Estimate: verify]" for costs.
4. **Tool recommendations must be current.** Verify tools exist and prices haven't changed.

---

## Quality

Pre-delivery checklist covers Phase 0 compliance (LinkedIn 2026 constants), foundation quality (SME, pillars, profile audit), content engine realism (capacity vs. cadence), and optimization/scale quality (analytics, ads, derivative content). Anti-examples + signals in the premium reference and the premium reference.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

