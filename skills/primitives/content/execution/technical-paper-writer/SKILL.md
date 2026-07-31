---
name: technical-paper-writer
version: '1.0'
last_updated: 2026-07-17
author: Ben Moore (Discovered Labs / ClientCo), adapted by Genesys Growth
description: 'Renders existing first-party research — a whitepaper, survey, benchmark, or dataset — as an arXiv-style technical
  paper PDF via LaTeX/tectonic. A stats-heavy paper in preprint format gets cited: by journalists, by other content, and by
  LLMs, which prefer one authoritative source with defensible numbers over loose vendor claims. Becomes the citable centre
  of gravity for a data-led PR programme. Triggers: "write a technical paper", "arXiv-style paper", "turn this whitepaper/study
  into a paper", "research paper PDF", "format this as a preprint", "data-led PR", "get cited by LLMs or journalists", "make
  our study more credible or authoritative". NOT for writing the research itself — /thought-leadership writes the whitepaper,
  this skill renders it. NOT for marketing collateral, one-pagers, or content without real data: the format amplifies scrutiny,
  so it only works if the substance is research.'
goal: Render first-party research as an arXiv-style preprint PDF that journalists, content, and LLMs can cite.
outcome: A compiled arXiv-style paper PDF plus its LaTeX source, every statistic mapped to a bibliography entry, a mandatory
  Limitations section, and disclosed provenance. The citable anchor asset for a data-led PR programme.
primitive: content
sub_primitive: execution
ontology_type: technical-paper
review_gate: 3
inputs:
  required:
  - expert-pov
  recommended:
  - thought-leadership
  - icp-research
  - win-loss
  - product-pulse
- type: technical-paper
  feeds_into: []
depends_on:
- expert-pov
owned_by_agent: content
mcps_used:
- exa
triggers:
  slash_commands:
  - /technical-paper-writer
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Technical Paper Writer

Render first-party research as an arXiv-style technical paper. A stats-heavy paper in preprint format gets cited — by journalists, by other content, and by LLMs, which prefer a single authoritative source with defensible numbers over loose vendor claims. The paper becomes the citable centre of gravity for a data-led PR programme.

**Requires the tectonic LaTeX engine** (`brew install tectonic` on macOS; `cargo install tectonic` or the distro package elsewhere) and network access on the first run — it downloads its package bundle then. A slow or offline first run is that download, not a hang.

## Doctrine inherited

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`evidence-bound-outputs.md`](../../../../../rules/evidence-bound-outputs.md) — every claim carries its source, or its confidence drops
- [`quantitative-evidence-floors.md`](../../../../../rules/quantitative-evidence-floors.md) — state the volume floor, name the confounds and lag. A paper is the one format where this is load-bearing: the Methods and Limitations sections exist to carry it
- [`ontology.md`](../../../../../rules/ontology.md) — confidence levels + attribution
- [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md) — a paper in robot prose reads as generated, which is the opposite of the goal

**Boundary with `/thought-leadership`:** that skill *writes* the whitepaper — argument-led prose, contrarian angle, three human gates. This skill *renders* an existing study as a paper. They're sequential, not rival. "Write a whitepaper on X" → `/thought-leadership`. "Turn this study into a paper" → here.

## When to run

- A whitepaper, benchmark study, survey, or internal dataset exists and needs a citable, research-grade rendering
- Building the anchor asset for data-led PR / link earning
- NOT for marketing collateral, one-pagers, or content without real data — the format only works if the substance is research

## Steps

### 1. Intake

Collect: source material (findings, tables, method notes), author name(s) + affiliation + contact, whether this re-renders an earlier publication (if so: original date, sponsor, research partners), intended hosting URL (own domain under `/research/` works well).

### 2. Fact-gate (mandatory, before any LaTeX)

Every headline claim must trace to a named primary source. For any market-sizing claim ("X million...", "Y% of..."), run the **denominator test**: divide the claim by its total population. If the share implied is implausible for the stated definition, the claim is definitionally unsound even if a source exists.

> **Worked example.** "Two-thirds of households hold £100k+ in investable assets" — only true if "investable" quietly includes property and pensions. A source exists; the claim is still unsound. It gets replaced with a sourced one, or cut.

Unsourced or unsound claims get replaced or cut. Never rendered.

### 3. Structure

Follow the premium reference. Required elements, in order:

| Element | Rule |
|---|---|
| Title + subtitle | Findings-oriented, method in the subtitle |
| Author block | Name / affiliation / URL / email, one column per author |
| Date + `\thanks` footnote | Provenance: sponsor, research partners, and what changed if re-rendering an earlier publication |
| Abstract | Findings-led, numbers up front, one paragraph |
| Keywords | 4-6 |
| Introduction | Ends with a numbered **Contributions** list |
| Data and Methods | One subsection per method or data source |
| Results | One claim per subsection heading; booktabs tables |
| Discussion | What the findings mean; second-order observations |
| **Limitations and threats to validity** | Mandatory — this section IS the credibility mechanism. Include a "commissioned research" paragraph when true. |
| Conclusion | Restate findings with numbers |
| Acknowledgements + References | Every stat in the paper maps to a `\citep` entry |

**Worked example — finding to claim-heading:**

- Input (source material): "Survey: 62% of failed deployments traced back to configuration drift"
- Output (Results subsection): `\subsection{Configuration drift dominates deployment failures}` — the heading asserts the finding; the prose and table under it carry the number and the source.

### 4. Build

Copy the premium reference into a dedicated working folder as `main.tex` — **never edit the file in the premium reference** (it is the reusable template). Then `tectonic main.tex`.

Notes: the first-ever run downloads tectonic's package bundle over the network (slow, fails offline — not a hang); `\bibitem` optional args must keep the `Source(Year)` shape or natbib errors.

Fix every error **and every overfull hbox** (wide tables: `\footnotesize` + tighter `\tabcolsep`; long URLs: the template loads `xurl`). Then **read the compiled PDF** — page 1 and the references page — and confirm each stat cites the right source. An overfull table is invisible in the compile-log summary.

### 5. Integrity guards

- "Pending on arXiv" may only be claimed after an actual submission exists.
- Commissioned or sponsored research must say so, in the footnote and in Limitations.
- A re-rendering of earlier work must declare what changed and what didn't.

## What good looks like

**Evaluations** — Every statistic maps to a `\bibitem`. Every market-sizing claim passed the denominator test. Limitations section present and specific (not "further research is needed"). Provenance footnote names sponsor + partners where they exist. Sample sizes and confounds stated in Methods per `quantitative-evidence-floors.md`. The compiled PDF was read, not just compiled. No claim in the paper is softer or harder than its evidence.

## Common mistakes

- Rendering marketing claims in academic dress — the format amplifies scrutiny, not just credibility
- Skipping Limitations to "look stronger" — it works the other way: the Limitations section is what makes commissioned research citable
- Wide tables overflowing a two-column layout — check the compiled PDF visually, not just the compile exit code
- Citing one source for a sentence containing three claims — split the citations
- Claiming arXiv status before submitting

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/voice-reviewer` — the content ship gate: voice + brand quality (pm-loop.md).

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs.

A paper is the narrow case: **Authority** and **Credible** carry nearly all the load, and both are earned by the Limitations section and the bibliography, not by adjectives. **Concrete** applies to the Results headings — the heading asserts the finding, in numbers. Do not reach for Scarcity, Emotional, or Stories here; a preprint that reaches for them stops reading as research, which is the whole asset.

## Attribution

Contributed by Ben Moore (Discovered Labs / ClientCo), July 2026. The fact-gate (incl. the denominator test), paper structure table, template, and integrity guards are his. Adapted to Genesys frontmatter, doctrine, and gates.
