---
name: prompt-design
version: '1.0'
last_updated: 2026-02-13
author: genesys-growth
description: 'Creates reusable AI prompts using a 7-section architecture (role, context, task, format, constraints, examples,
  quality criteria) for Clay, AirOps, or automation tools. Produces production-ready prompt templates with variable placeholders
  and validation rules. Split from workflow-prompt-design v2.0 (Mode A — individual prompts). Triggers: "write a prompt",
  "prompt design", "prompt template", "create a Clay prompt", "AirOps prompt". NOT for designing multi-step workflow chains
  — use workflow-design (Mode B) instead.'
goal: Creates reusable AI prompts using a 7-section architecture (role, context, task, format, constraints, examples, quality
  criteria) for Clay, AirOps, or automation tools.
outcome: Creates reusable AI prompts using a 7-section architecture (role, context, task, format, constraints, examples, quality
  criteria) for Clay, AirOps, or automation tools. Produces production-ready prompt templates with variable placeholders and
  validation rules. Split from workflow-prompt-design...
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
effort: medium
---

# Prompt Design

Generate reusable prompts using the 7-section architecture for B2B SaaS marketing deliverables.

For full process flowchart and step-by-step → the premium reference.

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Create a prompt for [deliverable]"
- "Build a prompt template"
- "Generate a prompt for [task]"
- "Prompt template for [use case]"
- "Make me a prompt"
- "Write a prompt for [deliverable]"

**Do NOT invoke when:**
- User wants a workflow → Use `workflow-design` skill
- User wants to execute a prompt → Just run it directly
- User wants a specific skill output → Use the relevant skill

---

## Input Requirements

### Required
| Input | Description | Source |
|-------|-------------|--------|
| **Deliverable type** | What output the prompt should produce | User specifies |

### Optional (improve quality)
| Input | How it helps |
|-------|--------------|
| Target audience | Tailors prompt language |
| Quality criteria | Defines success metrics |
| Existing prompts | Builds on proven patterns |
| Tool context | Adapts for specific AI (Claude, GPT, etc.) |

If deliverable type is missing, ask the user before generating.

---

## Core Framework: 7-Section Prompt Architecture

Every prompt follows this structure:

| Section | Purpose | Content |
|---------|---------|---------|
| **ROLE** | Sets expertise and context | "You are a [expert type] with [experience]..." |
| **GOAL** | System-level objective | "Your goal is to [outcome]..." |
| **INPUTS** | All `{{variables}}` user provides | List each variable with description |
| **TASK** | Step-by-step instructions | Numbered steps with clear actions |
| **OUTPUT FORMAT** | Structure, length, constraints | Format specification, character limits |
| **CONTEXT** | Reminder to pull from memory/knowledge | "Use any brand context, previous research..." |
| **EXAMPLE** | Placeholder for user's example | "Reference this example: {{example}}" |

### Prompt template

```markdown
## ROLE
You are a [EXPERT TYPE] with deep expertise in [DOMAIN]. You have [SPECIFIC EXPERIENCE].

## GOAL
Your goal is to [PRIMARY OBJECTIVE] that [QUALITY CRITERIA].

## INPUTS
The user will provide:
- `{{variable_1}}`: [Description]
- `{{variable_2}}`: [Description]

## TASK
Follow these steps:
1. [First action with specific instruction]
2. [Second action with specific instruction]
3. [Third action with specific instruction]

## OUTPUT FORMAT
Deliver the output as:
- Format: [Markdown/JSON/etc.]
- Length: [Specification]
- Structure: [Description]

Include:
- [Required element 1]
- [Required element 2]

## CONTEXT
Pull from any available context:
- Brand guidelines and voice
- Previous research or deliverables
- Known audience information

## EXAMPLE
Reference this example for quality: {{example}}
```

### Category matching

Match the user's request to the appropriate reference file:

| Category | Use cases | Reference file |
|----------|-----------|----------------|
| Research | Competitor, persona, win/loss | the premium reference |
| Social | LinkedIn, X, carousels | the premium reference |
| Long-form | Blog, articles | the premium reference |
| Landing pages | Homepage, persona, use case | the premium reference |
| Launch | Product announcements | the premium reference |
| Sales | Decks, battlecards | the premium reference |
| Positioning | Frameworks, canvases | the premium reference |
| Founder content | Thought leadership | the premium reference |
| AEO | Comparison, definition, how-to | the premium reference |
| Distribution | Channel distribution | the premium reference |

---

## Anti-Hallucination Guardrails

1. **Use exact 7-section structure.** Don't invent new sections.
2. **Mark all variables.** Every user input must be `{{marked}}`.
3. **Include quality gates.** Every prompt needs verification criteria.
4. **Reference existing patterns.** Check reference files before creating new.
5. **Test variable completeness.** Ensure all needed inputs are captured.

---

## Integration with Other Skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **workflow-design** | Complementary | For multi-step workflows with chained prompts |
| **All content skills** | Uses output | Prompts feed into skill execution |
| **vibe-coding** | Related | For building tools that use prompts |

---

