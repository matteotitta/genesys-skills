---
name: contract-redline
version: "1.0"
last_updated: 2026-05-28
author: genesys-growth
description: |
  Applies tracked-changes redlines + margin comments to a supplier-hostile
  client contract (DOCX), producing a properly-marked review document for the
  counterparty's legal team. Translates an objection email into per-clause
  redlines with proposed counter-language and rationale comments authored as
  Matteo Tittarelli. Saves the redlined.docx to Downloads, uploads to the
  client's Drive folder, and drafts a Gmail reply. Used pre-signature in
  client engagements when the counterparty sends standard boilerplate that
  needs amendments before signing. Triggers: "redline this contract",
  "add comments to the contract as redlines", "redline the agreement and
  send back", "track-changes on the contract".
goal: Produce a properly-marked tracked-changes redline of a counterparty contract with margin comments per clause.
outcome: Redlined.docx in Downloads, Google Doc copy in the client's Drive folder, Gmail draft reply to the counterparty.

primitive: clients
sub_primitive: null
ontology_type: client-engagement
review_gate: 3

inputs:
  required: []
  recommended:
    - client-proposals

depends_on: []

owned_by_agent: b2b-consultant
mcps_used:
  - gmail
  - gdrive
triggers:
  slash_commands:
    - /contract-redline
  natural_language:
    - "redline this contract"
    - "add these comments as redlines"
    - "track changes on the contract"
    - "redline the agreement and send back"

status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 1

disable-model-invocation: false
---

# Contract redline

Translates an objection email into a properly-marked tracked-changes redline of a counterparty contract (DOCX), produces margin comments per clause authored as Matteo Tittarelli, and ships the result through three surfaces: local Downloads, Google Drive, and a Gmail draft reply.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Internal-reference legal skill. Applies [[feedback_execution_doctrine_refinements_step6]] R1 (margin comments cite clause sources inline — auditability), R3 (comment voice operator-direct), R9 (verb-led comment structure). Gmail draft reply inherits R6 (close → signed contract primary). R2/R5/R7/R8 not applicable.

Use this when the counterparty sends a standard supplier-hostile contract template (broad IP assignment to "Group Company", one-way uncapped indemnification, unilateral termination, perpetual confidentiality, sole-discretion offset, perpetual assignment) and the negotiation needs proposed counter-language tracked inline rather than buried in a 1,000-word objection email.

## When to use

- Counterparty (e.g., ClientCo, ClientCo, ClientCo, future ClientCo renewal) sends a contract draft with terms that need amendments.
- You already have an objection email or list of issues — this skill is for *executing* the redline, not for drafting the objections.
- Counterparty has explicitly asked for redlines ("could you put these in as tracked changes?"), or the negotiation is at the stage where redlines beat further email.

**Don't use this skill for:** the upstream proposal/scoping work (use `/client-proposals`), the discovery research (use `/client-discovery`), or post-signing onboarding (use `/client-onboarding`).

## Process — five phases

### Phase 1 — Map the issues to clauses

Read the user's objection email (or list of asks). For each issue, locate the exact paragraph in the contract's `document.xml` by extracting paragraphs and finding the run that contains the load-bearing phrase. Produce a 12-column table (or however many issues) mapping:

| # | Section | Original (deletion) | Proposed (insertion) | Comment rationale |

Most enterprise contracts have ~10–15 redlines. Some are surgical edits (one-word swap); some are wholesale clause rewrites; some are new clause insertions (e.g., a missing liability cap).

### Phase 2 — Unpack the DOCX

Use the `document-skills:docx` skill's redlining workflow. Setup steps:

1. Create a Python venv at `/tmp/contract-venv` and install `defusedxml` + `lxml`. The skill's library requires both.
2. Run `python ooxml/scripts/unpack.py <contract.docx> /tmp/contract-work/unpacked`. Note the suggested RSID — copy it for the `Document(...)` constructor.
3. Pre-patch any whitespace violations in the unpacked `document.xml` (most older legal templates have trailing `&#160;` non-breaking spaces missing `xml:space="preserve"`). Search for `<w:t>...&#160;</w:t>` and add the attribute, or the save step will fail validation.

### Phase 3 — Apply redlines in batches

Group redlines into batches of 3–10 per script. Two-batch shape works well for a 12-item contract:
- Batch 1: the dealbreakers (6 items)
- Batch 2: the material risks (6 items)

For each redline, choose the right pattern from `document-skills:docx`:

| Edit shape | Pattern |
|---|---|
| One-word swap | `replace_node(run, '<w:r>{rpr}<w:t>{before}</w:t></w:r><w:del>...</w:del><w:ins>...</w:ins><w:r>{rpr}<w:t>{after}</w:t></w:r>')` |
| Whole-clause rewrite | `replace_node(run, '<w:del>...</w:del><w:ins>...</w:ins>')` |
| Multi-run clause replacement | Replace first run with del+ins, then `suggest_deletion()` on the remaining runs |
| New clause insertion | `DocxXMLEditor.suggest_paragraph(...)` + `insert_after(anchor_paragraph, new_xml)` |
| Whole-paragraph deletion | `suggest_deletion(paragraph_node)` |

For every redline, immediately add a `doc.add_comment(start=..., end=..., text=...)` with the rationale lifted verbatim from the user's objection email. Comments must be authored as Matteo Tittarelli (set in `Document(..., author="Matteo Tittarelli", initials="MT")`).

After each batch, `doc.save()` and verify via Python that the expected redline strings are present in `document.xml`.

### Phase 4 — Pack + verify

1. Run `python ooxml/scripts/pack.py /tmp/contract-work/unpacked <output.docx>` to produce the final DOCX.
2. Write the output to `~/Downloads/{original-name} - REDLINED MMYY.docx`.
3. Verify via Python:
   - Open the.docx as a zip
   - Confirm `word/comments.xml`, `word/commentsExtended.xml`, `word/people.xml` all present
   - Count `<w:ins>` / `<w:del>` / `<w:commentReference>` — should roughly match expected counts
   - Confirm all comment authors are "Matteo Tittarelli"
4. Extract "accept-mode" text for the key clauses to confirm the contract reads cleanly if the counterparty accepts all changes. Catches grammar issues from multi-run replacements.

### Phase 5 — Ship through three surfaces

1. **Local Downloads** — the.docx is already there from Phase 4. Done.
2. **Google Drive** — `node.claude/mcp/gdrive/upload-file.mjs <path> --client <slug>`. Use `upload-file.mjs` (preserves DOCX with tracked changes) **NOT** `create-doc-unified.mjs` (which flattens tracked changes during MD→GDoc conversion). The Google Doc preview will render tracked changes natively in Suggesting mode.
3. **Gmail draft** — search for the counterparty's thread via `mcp__gmail__search_threads`, then `mcp__gmail__create_draft` with `replyToMessageId` set to the latest counterparty message. Include the GDoc URL in the body so they can review either format. Note: Gmail MCP `create_draft` does not auto-attach the local.docx — the user attaches it manually before sending.

## Critical patterns

**Author + RSID setup:**
```python
doc = Document('/tmp/contract-work/unpacked',
               author="Matteo Tittarelli",
               initials="MT",
               rsid="<copy from unpack output>")
```

**Preserve run properties on every replacement:**
```python
rpr = tags[0].toxml() if (tags:= node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:del><w:r>{rpr}<w:delText xml:space="preserve">{old}</w:delText></w:r></w:del>...'
```

**Special-character entities for Word XML:**
- Curly apostrophe `’` → `&#8217;`
- Curly quotes `"` `"` → `&#8220;` `&#8221;`
- Em dash `—` → `&#8212;`
- Non-breaking space → `&#160;`

**Always use `xml:space="preserve"`** on `<w:t>` and `<w:delText>` with leading/trailing whitespace. The save validator will block on missing attribute.

**Comment ID auto-generation:** the Document library auto-generates `w:id` for new tracked changes and comments. Don't hard-code IDs.

## Anti-patterns

- ❌ Using `create-doc-unified.mjs` to push the redlined doc to Drive — that script converts markdown to a Google Doc and would lose all tracked changes. Use `upload-file.mjs` to preserve the DOCX intact.
- ❌ Modifying text inside another author's `<w:ins>` or `<w:del>` tags — use nested-deletion pattern per `document-skills:docx` ooxml.md guidance.
- ❌ Drafting wholesale-replacement clauses when surgical edits would suffice — the user's email tells you which edits are dealbreakers (full rewrite OK) vs. nuance tweaks (preserve as much original text as possible for review).
- ❌ Skipping the verification pass — extracting "accept-mode" text catches grammar errors from multi-run replacements that would otherwise reach the counterparty.
- ❌ Attaching the.docx to the Gmail draft via the MCP — `create_draft` doesn't reliably attach local files. Note in the response that the user attaches manually before sending.
- ❌ Auto-sending the Gmail reply — this is review_gate 3. The user reviews the redlines + the email body before send.

## Inputs required

- **Original contract.docx** — typically in `~/Downloads/` from the counterparty's email.
- **User's objection email or asks list** — typically inline in the conversation. Contains the per-clause rationale that becomes the comment text.
- **Client slug** in `gdrive-config.json` — controls the Drive folder routing. Add if missing (mirror an existing entry, set `name`, `code`, `domain`, `folderId`, `brand`).

## Quality gate (review_gate 3)

Before claiming done:

- [ ] All N redlines from the issues table appear in the verification grep
- [ ] All comments authored as "Matteo Tittarelli"
- [ ] Accept-mode text reads cleanly for the top 3-5 most-edited clauses (no broken grammar)
- [ ] Drive upload succeeded (URL printed)
- [ ] Gmail draft created in the correct thread (verify by thread ID match)
- [ ] User-facing summary clearly states: open Gmail, attach.docx, send

## Composition with other skills

- **Upstream:** `/client-proposals` (the deal that brought the contract to the table). The proposal's scope drives some of the redline content (e.g., the agreed Service Period length).
- **Downstream:** `/client-onboarding` (post-signature). Once the counterparty agrees, the signed contract becomes the canonical scope reference for the engagement.
- **Sibling:** `/client-discovery` (research before proposal). Pre-call research can flag known supplier-hostile patterns by counterparty so the redline pass starts faster.

## Final ship gate

Run `/premortem --output` before ship. See `.claude/skills/meta/orchestration/premortem/SKILL.md` for the 5 execution domains and output template.

