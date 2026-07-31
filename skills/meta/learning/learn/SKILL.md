---
name: learn
version: '1.0'
last_updated: 2026-04-26
author: genesys-growth
description: 'Process raw source material (transcripts, docs, articles, competitor pages, meeting notes) into structured context.
  Classifies input, extracts key insights, files to the correct location with MMYY naming, and cross-references existing context.
  The complement to /steal: /steal extracts patterns from external marketing; /learn absorbs knowledge from internal source
  material.'
goal: Process raw source material (transcripts, docs, articles, competitor pages, meeting notes) into structured context.
outcome: 'Process raw source material (transcripts, docs, articles, competitor pages, meeting notes) into structured context.
  Classifies input, extracts key insights, files to the correct location with MMYY naming, and cross-references existing context.
  The complement to /steal: /steal extracts patterns...'
primitive: meta
sub_primitive: learning
ontology_type: runbook
review_gate: 1
inputs:
  required: []
  recommended: []
- type: context-file
  feeds_into:
  - company-context
  - competitor-research
  - icp-research
  - positioning
  - product-messaging
depends_on: []
- company-context
- competitor-research
- icp-research
- positioning
- product-messaging
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
effort: max
---

# /learn — absorb source material into the knowledge base

Process raw material into structured context. Classify it, extract what matters, file it where it belongs, and connect it to what already exists.

`/steal` takes from the outside. `/learn` absorbs from the inside.

---

## Triggers

**Invoke when user says:**
- `/learn [file path or URL]`
- `/learn --queue` (drain mode — see below)
- "process this transcript"
- "add this to context"
- "learn from this [call / doc / article / page]"
- "I have a new [transcript / competitor page / doc] — file it"

**Do NOT invoke when:**
- User wants to extract marketing patterns from external work (use `/steal`)
- User wants to run a full structured research workflow (use `/company-context`, `/competitor-research`, `/icp-research`)
- User wants to save content they admire (use `/steal` → swipe file)
- User wants to analyze a transcript for specific deliverables (use `/transcript-analysis`)

---

## `--queue` mode (drain the slack-capture-bot queue)

When invoked as `/learn --queue` with no URL/file argument:

1. **Inventory the queue.** Read `.claude/queue/*.md`. Filter to files where frontmatter has `intent: learn` AND `status: unprocessed`. If none, say "queue is empty for /learn" and exit.

2. **Show the user the drain plan before starting.** Print a one-line summary per file:
   - `<filename>` — `<source>` — captured `<captured_at>` — reflex: `<reflex>`
   Ask: "Process all N? [y/N/select]" — `select` lets the user pick a subset by number.

3. **Process serially.** For each approved file:
   - Read the source URL/path from frontmatter
   - Run the standard /learn workflow against that source (classify → extract → file)
   - Use the reflex from the queue file as context for "why this was saved"
   - At the standard /learn review gate (Gate 1 — quick review), gate per-file
   - After completion, mark the queue file:
     - `status: processed`
     - `processed_at: <ISO timestamp>`
     - `processed_to: <path where /learn deposited the output>`

4. **Use the `queue.py` helper** at `projects/apps/slack-capture-bot/queue.py` to mark files done:
   ```bash
   python3 "projects/apps/slack-capture-bot/queue.py" done <slug> --output "<path-to-output>"
   ```

5. **Don't auto-skip on failure.** If a /learn run errors mid-queue, surface the error and ask whether to continue with the next file or stop.

6. **Summary at end.** Print: "Drained N files. M processed successfully, K errored. Run `queue trail` to see where outputs landed."

**When NOT to use `--queue`:** if the user passed a specific source on the command line, ignore queue mode and process that one source.

**When to use `/learn` vs. dedicated skills:**
- `/learn` = quick processing of ONE piece of source material into context
- `/company-context` = comprehensive company research using multiple sources + MCP tools
- `/competitor-research` = deep 11-dimension competitor analysis
- `/transcript-analysis` = structured extraction with quotes, themes, action items

Use `/learn` when you have a single document to absorb. Use dedicated skills when you need a complete, structured deliverable.

---

## Input requirements

| Input | Required? | Description |
|-------|-----------|-------------|
| Source material | Required | File path, URL, or pasted text |
| Client/project | Optional | Which client or project this belongs to (auto-detected from working directory if possible) |
| Focus area | Optional | "focus on competitive positioning" or "extract pricing insights" |

---

## Process

### Phase 1: Receive and classify

**Determine input type:**

| Type | Signals | Example |
|------|---------|---------|
| **Sales transcript** | Call recording, Gong/Granola export, Q&A format, buyer/seller dialogue | "Here's a discovery call with Acme Corp" |
| **Meeting notes** | Internal discussion, action items, decisions, no buyer present | "Notes from our positioning workshop" |
| **Competitor page** | URL to competitor website, pricing page, feature comparison | "Learn from sierra.ai/pricing" |
| **Article / report** | Industry content, analyst report, thought leadership | "Process this Forrester report" |
| **Internal doc** | Pitch deck, one-pager, brand guidelines, existing strategy doc | "Learn from our current messaging doc" |

**Determine destination:**

1. Check current working directory — if inside a client folder (`projects/consulting/active/{client}/`), route there
2. If user specifies a client, route to that client's folder
3. If no client context, route to `projects/research/` or ask

### Phase 2: Extract

Based on input type, extract different things:

**From sales transcripts:**
- Key buyer quotes (verbatim with timestamps if available)
- Objections raised and how they were handled
- Pain points mentioned
- Competitors referenced
- Decision criteria mentioned
- Deal stage signals (early exploration, active evaluation, negotiation)

**From competitor pages:**
- Positioning claims and key messages
- Pricing model and tiers (if visible)
- Feature emphasis and differentiation claims
- Target audience signals
- Social proof (customer logos, testimonials, metrics)

*Optional — counterfactual rewrite:* If the page is weak/generic (i.e., the user is learning from it as a *negative* example), add a "Rewrite" section with a one-paragraph version that would actually work. The diff between the original and the rewrite IS the lesson. Skip if the page is strong or the user didn't flag it as weak.

**From articles / reports:**
- Core thesis and key arguments
- Data points and statistics (with source attribution)
- Frameworks or models introduced
- Implications for our clients or work

**From internal docs:**
- Current positioning and messaging (for comparison with newer versions)
- Key decisions and their rationale
- Gaps or questions flagged in the doc
- Assumptions stated or implied

**From meeting notes:**
- Decisions made (with rationale)
- Action items (with owners if mentioned)
- Open questions
- Strategic direction changes

### Optional: bet-before-metrics calibration

If the source has measurable outcome data attached (post engagement, page conversion, deal value, view count, reply rate), pause **before reading the outcome** and record a one-word prediction in the output file:

```
**Prediction:** WIN | LOSE | UNSURE
**Why I bet that way:** [one line — what signal drove the gut call]
**Actual outcome:** [filled in after reading]
**Calibration note:** [if WIN/LOSE prediction was wrong, one line on what should have tipped me the other way]
```

Skip this step if no outcome data exists, or if the user has already revealed it. Losses teach more than wins — the calibration note is the highest-leverage line in the file.

This loop trains taste over time: the same prediction format across 50+ `/learn` runs becomes a personal calibration record. No automation needed — the file IS the record.

### Phase 2.5 — Atomic claim extraction + reweave check (optional)

Insert between Phase 2 (Extract) and Phase 3 (Structure and file). Full protocol in the premium reference.

**Skip when:** source is purely informational (skim-read for context, not absorbed into client knowledge); user says "just file this, don't reweave"; client folder has no `latest.md` / `history.md` yet (first /learn run — nothing to reweave against).

**Run when:** source contradicts or refines a locked-down strategic output (positioning, messaging, pricing); source is from a sales call; source is from a competitor (these three categories produce the most reweave signal per dollar of effort).

1. **Split** each Phase 2 insight bullet into atomic claims — one assertion per claim. See the premium reference for the "atomic" definition + worked examples.
2. **Number** each claim `[CLIENT]-[YYYYMMDD]-[NN]` (e.g., `ADV-20260517-03`). Append-only across all `/learn` runs for that client.
3. **Tag** each claim with confidence (`[VERIFIED]` / `[INFERRED]` / `[ESTIMATED]` / `[UNAVAILABLE]` per `.claude/rules/ontology.md`) and maturity (`[EMERGENT]` / `[VALIDATED]` / `[CANONICAL]`). New claims default to `[EMERGENT]`.
4. **Reweave scan** — for each claim, grep the client's `latest.md` + `history.md` for the subject. Classify the relationship: `[NEW]` / `[CONFIRMS: claim-id]` (promotes EMERGENT → VALIDATED) / `[EXTENDS: claim-id]` / `[CONTRADICTS: claim-id]`.
5. **Stop on contradiction** — if any claim has `[CONTRADICTS:...]`, halt the run and surface to user. The system never auto-resolves; user picks new-wins, old-wins, or both-with-conditional. Log the resolution in `history.md` under `[REWEAVE]`.

The reweave verdict block (count of new / confirmed / extended / contradicted) goes into the Phase 3 output file as a new section between "Key insights" and "Evidence."

### Phase 2.5 — Atomic claim extraction + reweave check (optional)

Insert between Phase 2 (Extract) and Phase 3 (Structure and file). Full protocol in the premium reference.

**Skip when:** source is purely informational (skim-read for context, not absorbed into client knowledge); user says "just file this, don't reweave"; client folder has no `latest.md` / `history.md` yet (first /learn run — nothing to reweave against).

**Run when:** source contradicts or refines a locked-down strategic output (positioning, messaging, pricing); source is from a sales call; source is from a competitor (these three categories produce the most reweave signal per dollar of effort).

1. **Split** each Phase 2 insight bullet into atomic claims — one assertion per claim. See the premium reference for the "atomic" definition + worked examples.
2. **Number** each claim `[CLIENT]-[YYYYMMDD]-[NN]` (e.g., `ADV-20260517-03`). Append-only across all `/learn` runs for that client.
3. **Tag** each claim with confidence (`[VERIFIED]` / `[INFERRED]` / `[ESTIMATED]` / `[UNAVAILABLE]` per `.claude/rules/ontology.md`) and maturity (`[EMERGENT]` / `[VALIDATED]` / `[CANONICAL]`). New claims default to `[EMERGENT]`.
4. **Reweave scan** — for each claim, grep the client's `latest.md` + `history.md` for the subject. Classify the relationship: `[NEW]` / `[CONFIRMS: claim-id]` (promotes EMERGENT → VALIDATED) / `[EXTENDS: claim-id]` / `[CONTRADICTS: claim-id]`.
5. **Stop on contradiction** — if any claim has `[CONTRADICTS:...]`, halt the run and surface to user. The system never auto-resolves; user picks new-wins, old-wins, or both-with-conditional. Log the resolution in `history.md` under `[REWEAVE]`.

The reweave verdict block (count of new / confirmed / extended / contradicted) goes into the Phase 3 output file as a new section between "Key insights" and "Evidence."

### Phase 3: Structure and file

**Create the output file:**

```markdown
# [Descriptive title]

**Source:** [file path, URL, or "pasted text"]
**Type:** [transcript | competitor-page | article | internal-doc | meeting-notes]
**Processed:** [today's date]
**Client:** [client name if applicable]

---

## Key insights

[3-7 bullet points — the most important things this material tells us]

## Evidence

[Verbatim quotes, data points, or specific observations with source attribution]
[Format: "[VERIFIED: source_type, reference]" per ontology standards]

## Implications

[What this means for strategy, positioning, messaging, or next steps]
[Be specific: "This suggests Acme's pricing objection is about perceived value, not budget"]

---

## Related context

**Built from:**
- [Source file/URL]

**Connects to:**
- [Existing context files this relates to — check the client folder]

**Feeds into:**
- [Skills that could benefit: "Run /competitor-research for a full structured profile"]
- [Or: "Update positioning — this contradicts our current differentiation claim"]
```

**File naming:** `MMYY-[type]-[subject].md`
- Sales transcript: `0426-transcript-acme-discovery.md`
- Competitor page: `0426-competitor-sierra-pricing.md`
- Article: `0426-article-forrester-ccaas-wave.md`
- Meeting notes: `0426-notes-positioning-workshop.md`

**File routing:**

| Context | Destination |
|---------|-------------|
| Active client work | `projects/consulting/active/{client}/{topic-folder}/` |
| Prospect research | `projects/prospects/{prospect}/` |
| Genesys internal | `projects/genesys/` |
| General research | `projects/research/` |

### Phase 4: Connect

After filing:

1. **Check for related context** — scan the destination folder for files that this new material connects to. Add cross-references in both directions if appropriate.

2. **Flag contradictions** — if the new material contradicts existing context (e.g., competitor changed pricing, buyer objection conflicts with ICP assumption), flag it explicitly:
   > "This contradicts `0326-positioning.md` which claims [X]. The new evidence suggests [Y]. Consider refreshing positioning."

3. **Suggest next steps** — based on what was extracted:
   - New competitor data → "Run `/competitor-research` for a full structured profile"
   - Buyer insights → "This could inform `/icp-research` or `/icp-behavioural`"
   - Pricing intelligence → "Feed into `/pricing-strategy` or `/pricing-research`"
   - Voice/messaging data → "Relevant for `/tov-guidelines` or `/product-messaging`"
   - Reusable pattern spotted (a hook structure, framework, or methodology that could become a skill or rule) → "Run `/steal` to evaluate this for the skill system"

---

## Quality checks

Before saving:
- [ ] Input correctly classified (transcript vs competitor page vs article vs internal doc vs notes)
- [ ] Key insights are specific, not generic ("Acme's VP Eng cited integration complexity as #1 objection" not "buyer had concerns")
- [ ] Evidence includes verbatim quotes or specific data points where available
- [ ] File routed to correct destination folder
- [ ] MMYY naming convention followed
- [ ] Related context section populated (checked existing files in destination)
- [ ] Contradictions flagged if any found
- [ ] At least one downstream skill suggested

---

## Anti-patterns

| Mistake | Fix |
|---------|-----|
| Summarizing instead of extracting | Pull specific quotes, data points, and claims — not paraphrases |
| Filing without checking what exists | Always scan the destination folder first |
| Generic implications | "This is interesting" → "This means our Sierra battlecard needs updating because..." |
| Missing attribution | Every data point needs `[VERIFIED: source]` or `[INFERRED: from X]` |
| Over-processing | Don't turn a 2-page doc into a 10-page analysis. Extract what matters, file it, move on |
