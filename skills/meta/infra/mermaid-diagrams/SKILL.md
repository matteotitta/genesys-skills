---
name: mermaid-diagrams
version: '1.0'
last_updated: 2026-02-13
author: genesys-growth
description: 'Creates Mermaid diagrams for flowcharts, architecture maps, sequence diagrams, and process visualizations. Produces
  validated Mermaid syntax ready for rendering, with optional export to Figma or Google Slides embedding. Triggers: "diagram",
  "flowchart", "Mermaid", "process map", "architecture map", "visualize this process", "sequence diagram". NOT for interactive
  visual workflows — use workflow-playground instead. NOT for Google Slides presentations — use create-gdrive instead. NOT
  for infographics — use linkedin-infographics instead.'
goal: Creates Mermaid diagrams for flowcharts, architecture maps, sequence diagrams, and process visualizations.
outcome: 'Creates Mermaid diagrams for flowcharts, architecture maps, sequence diagrams, and process visualizations. Produces
  validated Mermaid syntax ready for rendering, with optional export to Figma or Google Slides embedding. Triggers: "diagram",
  "flowchart", "Mermaid", "process map", "architecture...'
primitive: meta
sub_primitive: infra
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
effort: low
---

# Mermaid diagrams

Create, validate, and export Mermaid diagrams for B2B SaaS workflows, architectures, and process visualizations.

---

## Triggers

**Invoke when user says:**
- "Create a diagram for [process]"
- "Flowchart for [workflow]"
- "Mermaid diagram of [system]"
- "Architecture map for [product]"
- "Process map for [workflow]"
- "Visualize [process/system]"
- "Export diagram to Figma"

**Do NOT invoke when:**
- User wants a text-only process description (just write it)
- User wants a Google Slides presentation (use `create-gdrive`)
- User wants an infographic (use `linkedin-infographics`)

---

## Supported diagram types

| Type | Mermaid syntax | Best for |
|------|---------------|----------|
| **Flowchart** | `graph TD` / `graph LR` | Processes, decision trees, user flows |
| **Sequence** | `sequenceDiagram` | API flows, user interactions, handoffs |
| **Class** | `classDiagram` | Data models, system architecture |
| **State** | `stateDiagram-v2` | Status workflows, lifecycle stages |
| **Gantt** | `gantt` | Timelines, project plans, launch schedules |
| **Mindmap** | `mindmap` | Brainstorming, topic clustering |
| **Quadrant** | `quadrantChart` | Positioning maps, priority matrices |

---

## Process

### Step 1: Identify diagram type

Match the user's need to the best Mermaid type:

- **"How does X flow?"** → Flowchart
- **"What happens between A and B?"** → Sequence diagram
- **"What are the states of X?"** → State diagram
- **"Show the timeline for X"** → Gantt chart
- **"Map out the concepts"** → Mindmap
- **"Plot X vs Y"** → Quadrant chart

### Step 2: Draft the diagram

Write valid Mermaid syntax. Follow these rules:
- Use descriptive node IDs (not single letters)
- Keep labels concise (under 40 characters)
- Use subgraphs to group related nodes
- Apply consistent direction (TD for vertical, LR for horizontal)
- Use appropriate link styles (solid for primary flow, dotted for optional)

### Step 3: Validate

Before delivery:
- [ ] Syntax renders without errors
- [ ] All nodes are connected (no orphans)
- [ ] Labels are readable at normal zoom
- [ ] Direction is logical (top-to-bottom or left-to-right)
- [ ] Subgraphs are labeled

### Step 4: Export (if requested)

See export workflow section below.

---

## Syntax templates

### Flowchart (process)

```
graph TD
    start[Start] --> step1[Step 1: Description]
    step1 --> decision{Decision?}
    decision -->|Yes| path_a[Path A]
    decision -->|No| path_b[Path B]
    path_a --> result[Result]
    path_b --> result

    subgraph Phase 1
        step1
        decision
    end
```

### Sequence diagram (interactions)

```
sequenceDiagram
    participant User
    participant App
    participant API
    participant DB

    User->>App: Action
    App->>API: Request
    API->>DB: Query
    DB-->>API: Response
    API-->>App: Data
    App-->>User: Display
```

### State diagram (lifecycle)

```
stateDiagram-v2
    [*] --> Draft
    Draft --> Review: Submit
    Review --> Approved: Approve
    Review --> Draft: Request changes
    Approved --> Published: Publish
    Published --> [*]
```

### Gantt chart (timeline)

```
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
        Research:a1, 2026-02-13, 7d
        Analysis:a2, after a1, 5d
    section Phase 2
        Design:b1, after a2, 10d
        Build:b2, after b1, 14d
```

### Quadrant chart (positioning)

```
quadrantChart
    title Positioning Map
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Do First
    quadrant-2 Schedule
    quadrant-3 Delegate
    quadrant-4 Eliminate
    Item A: [0.8, 0.9]
    Item B: [0.3, 0.7]
    Item C: [0.6, 0.2]
```

---

## Export workflow

### Option 1: SVG/PNG for Figma

1. Render the Mermaid diagram using the Mermaid CLI or an online renderer
2. Export as SVG (preferred for scalability) or PNG (for fixed-size use)
3. Import into Figma:
   - SVG: File > Place Image, or paste directly
   - PNG: File > Place Image
4. In Figma: ungroup the SVG to edit individual elements, apply brand colors

**Mermaid CLI command (if available):**
```bash
npx @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.svg -t dark
```

**Online renderers:**
- mermaid.live (official editor)
- Copy Mermaid code block → paste into any Mermaid renderer

### Option 2: Embed in Google Slides

1. Render diagram to SVG/PNG
2. Use `create-gdrive` skill to create a presentation
3. Insert the rendered image into the slide
4. Or: paste the Mermaid code block into a Google Doc for technical documentation

### Option 3: Inline in markdown

For markdown-native destinations (GitHub, Notion, CLAUDE.md):
- Wrap in triple backticks with `mermaid` language tag
- Most modern markdown renderers support Mermaid natively

---

## Style guidelines

### Colors (when using theme or classDef)

Apply client brand colors when available. Default to:
- Primary nodes: `fill:#1a1a2e,color:#fff`
- Secondary nodes: `fill:#16213e,color:#fff`
- Decision nodes: `fill:#0f3460,color:#fff`
- Highlight nodes: `fill:#e94560,color:#fff`

### Typography

- Keep node labels under 40 characters
- Use sentence case
- Avoid abbreviations unless universally understood

### Layout

- Vertical (TD) for sequential processes
- Horizontal (LR) for parallel or branching workflows
- Use subgraphs to reduce visual clutter
- Maximum 15-20 nodes per diagram (split larger ones)

---

## Integration with other skills

| Skill | How Mermaid helps |
|-------|-------------------|
| `workflow-design` | Visualize multi-step prompt chains |
| `create-gdrive` | Embed diagrams in Google Slides/Docs |
| `skill-catalog` | Dependency charts between skills |
| `icp-behavioural` | Buyer journey flowcharts |
| `product-launch` | Launch timeline Gantt charts |
| `content-strategy` | Content pipeline diagrams |

---

