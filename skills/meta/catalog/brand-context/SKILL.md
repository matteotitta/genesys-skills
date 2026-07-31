---
name: brand-context-sync
version: '1.0'
last_updated: 2026-03-03
author: genesys-growth
description: 'Creates or updates the "Voice & Messaging" section in a client''s CLAUDE.md file, syncing voice patterns, vocabulary,
  messaging pillars, and competitor quick-reference into the project context. Produces a claude-md-section consumed by all
  content skills (linkedin-content, landing-page-copy, youtube-scripts, aeo-content, outreach-emails, storytelling, thought-leadership).
  Triggers: "sync brand context", "update client CLAUDE.md voice section", "brand context sync", "set up client voice". Run
  after completing tov-guidelines, brand-kit, or competitor-research. NOT for creating visual brand systems — use brand-kit
  instead.'
goal: Creates or updates the "Voice & Messaging" section in a client's CLAUDE.md file, syncing voice patterns, vocabulary,
  messaging pillars, and competitor quick-reference into the project context.
outcome: Creates or updates the "Voice & Messaging" section in a client's CLAUDE.md file, syncing voice patterns, vocabulary,
  messaging pillars, and competitor quick-reference into the project context. Produces a claude-md-section consumed by all
  content skills (linkedin-content, landing-page-copy,...
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 1
inputs:
  required: []
  recommended:
  - tov-guidelines
  - brand-kit
  - competitor-research
  - company-context
- type: claude-md-section
  feeds_into:
  - linkedin-weekly-content
  - website-copy
  - youtube-scripts
  - aeo-content
  - outreach-emails
  - storytelling
  - thought-leadership
depends_on: []
- aeo-content
- website-copy
- linkedin-weekly-content
- outreach-emails
- storytelling
- thought-leadership
- youtube-scripts
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
disable-model-invocation: true
---

# Brand Context Sync

Synthesise the "Voice & Messaging" section for a client's CLAUDE.md from existing upstream skill outputs. This is a meta-skill — it reads files already in the project folder, it does not perform new research.

The purpose: every content skill auto-loads the client CLAUDE.md. By adding a standardised "Voice & Messaging" section, content skills get instant access to voice rules, messaging anchors, and competitive context without re-asking the user.

For full 3-phase process + DESIGN.md awareness rules → the premium reference.

---

## Claude Code Triggers

**Invoke this skill when:**
- "sync brand context for [client]"
- "update voice section for [client]"
- "refresh client context"
- "add voice & messaging to CLAUDE.md"
- After completing `/tov-guidelines` for any client

**Do NOT invoke when:**
- User wants to run TOV analysis from scratch → use `/tov-guidelines`
- User wants full competitor research → use `/competitor-research`
- User wants to update project scope or file references in CLAUDE.md → edit manually

---

## Input Requirements

### Required
| Input | Description | Source |
|-------|-------------|--------|
| **Client project folder** | Must be inside `projects/consulting/{slug}/` | User context or explicit path |
| **Client CLAUDE.md** | The file to update | `projects/consulting/{slug}/CLAUDE.md` |

### Optional (improve quality)
| Input | How it helps |
|-------|--------------|
| TOV guidelines output | Voice rules (Use/Avoid lists) |
| Brand guidelines output | Visual identity, vocabulary |
| Competitor research aggregate | Competitive quick-ref |
| ICP research output | ICP description, key people |
| Product messaging output | Messaging anchors (value prop, differentiators, CTA) |
| Expert POV output | Author voice and positioning |

### Validation checklist
Before proceeding, verify:
- [ ] Client CLAUDE.md exists and is readable
- [ ] At least one upstream file exists (brand/, competitors/, icp/, messaging/)
- [ ] Template file exists at `VOICE-MESSAGING-TEMPLATE.md`

If no upstream files exist: tell the user "No brand files found. Run `/tov-guidelines` first to generate source material."

---

## Process at a glance

| Phase | Purpose | Output |
|-------|---------|--------|
| **1. Locate** | Scan project folder, determine CREATE vs UPDATE | File inventory + mode |
| **2. Extract** | Pull voice rules, vocabulary, messaging anchors, competitive quick-ref, key people | Section content (or MISSING markers) |
| **3. Write** | Format via template, insert/replace in client CLAUDE.md, verify | Updated CLAUDE.md |

For full per-phase steps, MISSING-marker conventions, and DESIGN.md awareness → the premium reference.

---

## Anti-Hallucination Guardrails

1. **Verbatim voice rules.** Copy Use/Avoid rules exactly from TOV. Don't paraphrase, generalise, or add rules not in source.
2. **No invented messaging.** If positioning/messaging output doesn't exist, mark as MISSING. Don't invent value props or differentiators.
3. **No invented competitors.** Only include competitors from competitor-research files. Don't add from general knowledge.
4. **Source tracing.** Every section must reference its source file.
5. **Mark unknowns explicitly.** Use `[MISSING — run /[skill-name] first]` for any section that can't be populated.

---

## Quality Checklist (pre-delivery)

### Content quality
- [ ] Voice rules are verbatim from source (not paraphrased)
- [ ] Max 12 Use + 12 Avoid rules (not more)
- [ ] Messaging anchors traced to positioning/messaging output
- [ ] Competitive quick-ref matches aggregate analysis
- [ ] MISSING sections clearly marked with the skill to run

### Format quality
- [ ] Section header is exactly `## Voice & Messaging (auto-loaded by content skills)`
- [ ] Subsection headers match template (Identity, Voice rules, Vocabulary, etc.)
- [ ] Arrows (→) used for differentiator lists
- [ ] Source file paths are relative to project root

### Completeness
- [ ] All 7 subsections present (even if some are MISSING)
- [ ] Sources subsection lists all files that were read
- [ ] No other CLAUDE.md sections modified

---

## Integration with Other Skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **tov-guidelines** | Primary upstream | Voice rules + vocabulary |
| **brand-kit** | Upstream | Visual identity context |
| **competitor-research** | Upstream | Competitive quick-ref |
| **icp-behavioural** | Upstream | ICP description |
| **product-messaging** | Upstream | Messaging anchors |
| **expert-pov** | Upstream | Author voice |
| **All content skills** | Downstream consumers | Auto-load the Voice & Messaging section from client CLAUDE.md |

---

