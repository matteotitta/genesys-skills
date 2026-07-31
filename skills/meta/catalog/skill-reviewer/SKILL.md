---
name: skill-reviewer
version: '1.0'
last_updated: 2026-03-03
author: genesys-growth
description: 'Reviews SKILL.md files for structural quality across 8 dimensions (frontmatter, triggers, process, inputs, outputs,
  examples, edge cases, review gate). Produces a scored review report with pass/fail per dimension and actionable fix suggestions.
  Triggers: "review this skill", "check skill quality", "audit skill", "grade SKILL.md". Recommended upstream: skill-catalog
  for template reference. Run after creating or modifying any skill to catch gaps before shipping. NOT for reviewing content
  voice — use voice-reviewer instead.'
goal: Reviews SKILL.md files for structural quality across 8 dimensions (frontmatter, triggers, process, inputs, outputs,
  examples, edge cases, review gate).
outcome: 'Reviews SKILL.md files for structural quality across 8 dimensions (frontmatter, triggers, process, inputs, outputs,
  examples, edge cases, review gate). Produces a scored review report with pass/fail per dimension and actionable fix suggestions.
  Triggers: "review this skill", "check skill...'
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 0
inputs:
  required: []
  recommended:
  - skill-catalog
- type: skill-review-report
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
paths:.claude/skills/**
disable-model-invocation: true
---

# Skill Reviewer

Review a SKILL.md file for structural quality, completeness, and template compliance. Grades on 8 dimensions covering the canonical skill structure (see `.claude/skills/_schema/SKILL.template.md` + `.claude/skills/_schema/AUTHORING.md`). Used to catch drift before a skill ships.

This is a meta-skill — it reviews skill definitions, not skill outputs.

---

## Claude Code Triggers

**Invoke this skill when:**
- "review skill [name]"
- "audit [skill-name] skill"
- "is [skill] well-defined?"
- "check skill quality for [skill]"
- "grade this SKILL.md"

**Do NOT invoke when:**
- User wants to review content output quality → use `/voice-reviewer` instead
- User wants to check the skill catalog → use `/skill-catalog` instead
- User wants to build a new skill from scratch → use prompt-design instead

---

## Input Requirements

### Required inputs

| Input | Description | Source |
|-------|-------------|--------|
| **SKILL.md path** | Path to the SKILL.md file to review | User provides or inferred from context |

### Optional inputs (improve quality)

| Input | How it helps |
|-------|--------------|
| SKILL.template.md | Reference template for comparison — at `.claude/skills/_schema/SKILL.template.md` |
| skill-catalog SKILL.md | Cross-reference for catalog alignment check |

### Input validation checklist

Before proceeding, verify:
- [ ] SKILL.md file exists and is readable
- [ ] File contains YAML frontmatter (between `---` delimiters)

**If file doesn't exist:** Tell the user the path is invalid and ask for the correct one.

---

## Process (step-by-step)

### Phase 1: Read and parse

**Purpose:** Load the SKILL.md and extract structural elements.

**Steps:**

1. **Step 1.1: Read the file**
   - Load the full SKILL.md content
   - Parse YAML frontmatter into key-value pairs
   - Identify all H2 (`##`) and H3 (`###`) sections present
   - **Output:** Parsed frontmatter + section inventory

**Phase 1 checkpoint:**
- [ ] File successfully read
- [ ] Frontmatter parsed
- [ ] Section headers cataloged

### Phase 2: Grade each dimension

**Purpose:** Evaluate the skill against 8 quality dimensions.

**Steps:**

1. **Dimension 1: Frontmatter completeness**
   - Check for required fields: `name`, `version`, `author`, `last_updated`, `description`
   - Check for agentic fields: `dependencies`, `outputs`, `triggers`, `review_gate`
   - **PASS:** All required + agentic fields present with non-empty values
   - **WARN:** Required fields present but agentic fields missing
   - **FAIL:** Any required field missing

2. **Dimension 2: Trigger quality**
   - Check for `## Claude Code Triggers` section
   - Count "Invoke this skill when" trigger phrases
   - Check for "Do NOT invoke when" anti-triggers
   - **PASS:** 4+ trigger phrases AND 2+ anti-triggers
   - **WARN:** 2-3 trigger phrases OR only 1 anti-trigger
   - **FAIL:** Missing section OR fewer than 2 triggers OR no anti-triggers

3. **Dimension 3: Input definition**
   - Check for `## Input Requirements` section
   - Look for separation between Required and Optional inputs
   - Look for Input Validation Checklist
   - Look for "If inputs are missing" handling
   - **PASS:** All four elements present
   - **WARN:** Required/Optional separated but no validation checklist
   - **FAIL:** Missing section OR no input/output distinction

4. **Dimension 4: Process structure**
   - Check for `## Process` section with named phases
   - Each phase should have: Purpose, Steps, Checkpoint
   - Count phases (minimum 2 expected)
   - **PASS:** 2+ phases, each with purpose + steps + checkpoint
   - **WARN:** Phases present but missing checkpoints
   - **FAIL:** No process section OR only 1 phase OR no steps

5. **Dimension 5: Anti-hallucination guardrails**
   - Check for `## Anti-Hallucination Guardrails` section
   - Count guardrails listed
   - Check if guardrails are skill-specific (not generic copy-paste)
   - Look for placeholder format definition
   - **PASS:** 3+ skill-specific guardrails + placeholder format
   - **WARN:** 1-2 guardrails OR guardrails are generic
   - **FAIL:** Missing section OR zero guardrails

6. **Dimension 6: Output format**
   - Check for `## Output Format` section
   - Look for output structure definition (headers, formatting rules)
   - For copy skills: check for character count requirements
   - For analytical / data-verdict skills (audit, scoring, ranking, reporting): check for a report-format contract — a named output structure, a literal comparable template on recurring deliverables, and a bound significance floor (`quantitative-evidence-floors.md`: verdict states the volume behind it, synthesizes rather than dumping rows). WARN if the skill renders verdicts from counts but ships no floor or comparable format.
   - **PASS:** Clear output structure with formatting rules
   - **WARN:** Section exists but structure is vague
   - **FAIL:** Missing section

7. **Dimension 7: Quality checklist**
   - Check for `## Quality Checklist` section
   - Look for subsections: Content Quality, Format Quality, Completeness
   - Count checklist items
   - **PASS:** 3 subsections with 3+ items each
   - **WARN:** Checklist exists but fewer than 3 subsections
   - **FAIL:** Missing section OR fewer than 3 total items

8. **Dimension 8: Skill-catalog alignment**
   - Read `.claude/skills/meta/catalog/skill-catalog/SKILL.md`
   - Check if this skill name appears in the catalog
   - If listed: check review_gate in SKILL.md matches catalog entry
   - Check if dependencies listed match skill's Input Requirements
   - **PASS:** Skill registered in catalog with matching metadata
   - **WARN:** Skill registered but metadata doesn't match
   - **FAIL:** Skill not found in catalog

**Phase 2 checkpoint:**
- [ ] All 8 dimensions scored
- [ ] Each score has a specific finding (not just PASS/FAIL)
- [ ] Senior-engineer test: would a senior engineer say this skill is overcomplicated? If yes, flag for slim refactor regardless of dimension scores. <!-- Adapted from forrestchang/andrej-karpathy-skills (MIT) -->

### Phase 3: Generate report

**Purpose:** Compile the review into a structured report.

**Steps:**

1. **Step 3.1: Calculate overall score**
   - Count PASS, WARN, FAIL across all 8 dimensions
   - Overall verdict: ALL PASS = "Ready to ship", any FAIL = "Needs fixes", all WARN or better = "Acceptable with notes"
   - **Output:** Score summary

2. **Step 3.2: Write the report**
   - Follow the output format below
   - List critical issues (FAIL) first, then warnings
   - Include specific recommendations for each issue
   - **Output:** Complete review report

---

# Skill Review: [skill-name]

**Date:** YYYY-MM-DD
**File:** [path to SKILL.md]
**Verdict:** [Ready to ship | Acceptable with notes | Needs fixes]

## Score: X PASS / Y WARN / Z FAIL

| # | Dimension | Score | Finding |
|---|-----------|-------|---------|
| 1 | Frontmatter | PASS/WARN/FAIL | [one-line finding] |
| 2 | Triggers | PASS/WARN/FAIL | [one-line finding] |
| 3 | Inputs | PASS/WARN/FAIL | [one-line finding] |
| 4 | Process | PASS/WARN/FAIL | [one-line finding] |
| 5 | Guardrails | PASS/WARN/FAIL | [one-line finding] |
| 6 | Output format | PASS/WARN/FAIL | [one-line finding] |
| 7 | Quality checklist | PASS/WARN/FAIL | [one-line finding] |
| 8 | Catalog alignment | PASS/WARN/FAIL | [one-line finding] |

## Critical issues (FAIL)

[Details on each FAIL with specific line references and fix instructions]

## Warnings (WARN)

[Details on each WARN with improvement suggestions]

## Recommended updates

1. [Specific action to take]
2. [Specific action to take]
```

---

## Anti-Hallucination Guardrails

1. **Only report what's actually in the file:** Do not assume a section exists if you can't find the header. Grep for the exact header text.
2. **Count explicitly:** When reporting "4 trigger phrases found," list them. Don't approximate.
3. **Quote the file:** When flagging an issue, reference the specific line or section where the problem is.
4. **Don't invent recommendations from outside context:** Recommendations must be based on what the canonical template (`.claude/skills/_schema/SKILL.template.md`) + `AUTHORING.md` require, not general best practices.

---

## Quality Checklist (pre-delivery)

### Content quality
- [ ] All 8 dimensions actually evaluated (not skipped)
- [ ] Each finding references specific evidence from the file
- [ ] Recommendations are actionable (not vague "improve this")

### Format quality
- [ ] Score table formatted correctly
- [ ] FAIL items listed before WARN items
- [ ] Verdict matches score (no FAIL = "Ready to ship" is wrong if there are FAILs)

### Completeness
- [ ] Overall score calculated correctly
- [ ] All critical issues have fix instructions
- [ ] Report includes the file path reviewed

---

