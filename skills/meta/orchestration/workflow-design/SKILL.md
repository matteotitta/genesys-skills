---
name: workflow-design
version: '1.0'
last_updated: 2026-02-13
author: genesys-growth
description: 'Designs multi-step AI workflows with chained prompts for Clay, AirOps, n8n, or other automation tools. Produces
  a complete workflow specification with stage-by-stage prompt definitions, input/output mappings, and implementation guide.
  Split from workflow-prompt-design v2.0 (Mode B — workflow architecture). Triggers: "design a workflow", "prompt chain",
  "workflow automation", "build an automation", "chain these steps". NOT for writing individual prompts — use prompt-design
  (Mode A) instead. NOT for visualizing workflows — use workflow-playground instead.'
goal: Designs multi-step AI workflows with chained prompts for Clay, AirOps, n8n, or other automation tools.
outcome: Designs multi-step AI workflows with chained prompts for Clay, AirOps, n8n, or other automation tools. Produces a
  complete workflow specification with stage-by-stage prompt definitions, input/output mappings, and implementation guide.
  Split from workflow-prompt-design v2.0 (Mode B — workflow...
primitive: meta
sub_primitive: orchestration
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
effort: high
---

# Workflow Design

Design multi-step AI workflows with chained prompts for B2B SaaS marketing deliverables.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Design a workflow"
- "Create a process for [task]"
- "Build a prompt chain"
- "Sequence prompts for [goal]"
- "Create an AI workflow"
- "Multi-step process for [task]"
- "Chain prompts together"

**Do NOT invoke when:**
- User wants a single prompt → Use `prompt-design` skill
- User wants to execute a prompt → Just run it directly
- User wants code/app built → Use `vibe-coding` skill

---

## Input Requirements

### Required Inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Task description** | What the workflow should accomplish | User specifies |
| **Desired outcome** | What the final output should be | User specifies |

### Optional Inputs (improve quality)

| Input | How It Helps |
|-------|--------------|
| Existing prompts | Builds on proven patterns |
| Integration needs | Determines variable chaining |
| Tool context | Adapts for specific AI (Claude, GPT, etc.) |
| Quality criteria | Defines success metrics per stage |

### Input Validation Checklist

Before proceeding, verify:
- [ ] Task description is clear
- [ ] Desired outcome is defined
- [ ] Stages can be identified

**If inputs are missing:** Ask for task description and desired outcome.

---

## Core Frameworks (voice-locked invariants)

### Workflow Patterns

| Pattern | Structure | Use When |
|---------|-----------|----------|
| **Linear** | Stage 1 → 2 → 3 → 4 | Research → Strategy → Execution |
| **Parallel + Merge** | [A + B + C] → Merge → D | Independent research streams |
| **Iterative Loop** | Stage → Check → Refine → Check | Quality-critical outputs |
| **Fork** | Stage 1 → [A or B] based on condition | Different paths for different inputs |

### Variable Chaining Rules

| Rule | Description |
|------|-------------|
| **Explicit naming** | `{{stage1_output}}` not just `{{output}}` |
| **Format matching** | Output format of N must match input format of N+1 |
| **Validation** | Check variables exist before using |
| **Fallback** | Define behavior if variable is empty |

---

## Process pointer

Step-by-step phases, flowchart, and pre-built workflow chains live in the premium reference.

Summary: validate inputs → map workflow → generate stage prompts (each using 7-section architecture) → create variable registry → write execution guide → compile single markdown document.

---

## Anti-Hallucination Guardrails

1. **Use exact 7-section structure for each stage.** Don't invent new sections.
2. **Mark all variables.** Every user input and stage output must be `{{marked}}`.
3. **Include quality gates.** Every stage needs verification criteria.
4. **Test variable chains.** Ensure outputs match expected inputs.
5. **Reference existing patterns.** Check reference files before creating new workflow stages.

---

## Quality

Pre-delivery checklist, worked example (Transcript-to-LinkedIn workflow), and anti-examples live in the premium reference.

Minimum bar: diagram complete, variable registry covers every variable, all stages carry a 7-section prompt, quality gates defined between stages, execution guide present.

---

## Skill Auto-Update Protocol

Feedback signal detection, pattern triggers, and self-update format live in the premium reference.

---

## Integration with Other Skills

Each stage uses the 7-section prompt architecture from the `prompt-design` skill. For individual prompt creation, use `prompt-design`.

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **prompt-design** | Foundation | Each workflow stage uses 7-section prompt architecture |
| **All content skills** | Uses output | Workflows feed into skill execution |
| **vibe-coding** | Related | For building tools that use workflows |
| **transcript-analysis** | Provides input | Interview workflows |

---

