---
name: voice-reviewer
version: '1.4'
last_updated: 2026-05-17
author: genesys-growth
description: 'Reviews content output for voice quality and brand compliance across 8 dimensions (D8 is LinkedIn-only) including the 100 Posts Test.
  Produces a scored voice-review-report with pass/fail verdicts and rewrite suggestions. Triggers: "review voice", "check
  tone", "does this sound like [client]", "100 Posts Test", "voice check", "brand compliance review". Recommended upstream:
  tov-guidelines, brand-context for reference voice patterns. Run before shipping LinkedIn posts, landing page copy, emails,
  or articles. NOT for structural skill review — use skill-reviewer instead.'
goal: Reviews content output for voice quality and brand compliance across 8 dimensions (D8 is LinkedIn-only) including the 100 Posts Test.
outcome: 'Reviews content output for voice quality and brand compliance across 8 dimensions including the 100 Posts Test.
  Produces a scored voice-review-report with pass/fail verdicts and rewrite suggestions. Triggers: "review voice", "check
  tone", "does this sound like [client]", "100 Posts Test",...'
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended:
  - tov-guidelines
  - brand-context
- type: voice-review-report
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
context: fork
effort: medium
disable-model-invocation: true
---

# Voice Reviewer

Review any content output for voice quality, brand compliance, and authenticity. Checks 8 dimensions against both the global CLAUDE.md rules and client-specific voice guidelines (D8 is LinkedIn-specific and conditional). This is the standalone version of the quality checks the Stop hook runs automatically.

Use this when you want an explicit, detailed voice review — not just a pass/fail.

For the full 8-dimension rule set → the premium reference. For the 3-phase process + output format → the premium reference.

---

## Claude Code Triggers

**Invoke this skill when:**
- "voice check this"
- "does this sound right?"
- "run voice review"
- "100 posts test"
- "check this for brand compliance"
- "review the voice on this [post/copy/email]"

**Do NOT invoke when:**
- User wants to review a SKILL.md definition → use `/skill-reviewer` instead
- User wants to generate content → use the appropriate content skill
- User wants to edit existing content for a different reason (shortening, restructuring)

---

## Input Requirements

### Required
| Input | Description | Source |
|-------|-------------|--------|
| **Content to review** | Text output to check | User provides or last assistant message |

### Optional (improve quality)
| Input | How it helps |
|-------|--------------|
| Client name or project context | Activates client-specific voice rules from CLAUDE.md |
| Content type (LinkedIn, landing page, email, article) | Adjusts dimension weighting (D8 only fires for LinkedIn) |
| Author name | Checks if voice matches the attributed author |

If content is not a deliverable (code, plan, conversation), tell the user this skill is for content deliverables only.

---

## The 8 dimensions (summary)

| # | Dimension | Trigger |
|---|-----------|---------|
| 1 | **Corporate buzzwords** | Banned words from CLAUDE.md + client list |
| 2 | **Sentence structure** | Active voice, concrete claims, operator-first |
| 3 | **Em dash usage** | " — " with spaces, ≤ 2 per paragraph |
| 4 | **Title/header case** | Sentence case (not Title Case) |
| 5 | **Client-specific voice rules** | Conditional — only if client context loaded |
| 6 | **100 Posts Test** | Authentic across a feed of 100 from this author? |
| 7 | **Anti-AI-speak** | Structural patterns (false contrast, wrapped bow, AI transitions) + 45-row pattern→replacement table per the premium reference |
| 8 | **LinkedIn readability** | LinkedIn-only — mobile breaks, one story per post, ecosystem CTAs |

For full rules per dimension → the premium reference.

---

## Verdict logic

| Inputs | Verdict |
|--------|---------|
| All CLEAN/PASS | **Ship it** |
| Any WARN, no FAIL | **Minor fixes recommended** |
| Any FAIL | **Fix before shipping** |

---

## Anti-Hallucination Guardrails

1. **Quote the actual text.** When flagging an issue, always quote the exact text. Do not paraphrase.
2. **Don't flag style preferences as violations.** If something isn't in the banned list or client rules, it's not a violation.
3. **Don't over-flag intentional choices.** Quotes from customers, competitor names, technical terms may contain "banned" words — these are contextual, not violations.
4. **Be specific about fixes.** "Make it more active" is not a fix. "Change 'The platform was designed to...' → 'We designed the platform to...'" is a fix.

---

## Quality Checklist (pre-delivery)

### Content quality
- [ ] All 8 dimensions evaluated (D8 N/A for non-LinkedIn)
- [ ] Each finding has quoted evidence
- [ ] Fixes are specific enough to implement without guessing
- [ ] False positives filtered (quotes, proper nouns, technical terms)

### Format quality
- [ ] Score table formatted correctly
- [ ] Verdict matches scores
- [ ] Issues listed with quoted text + fix pairs

### Completeness
- [ ] Client context correctly identified (or noted as "global only")
- [ ] Summary mentions both strengths and issues

---

