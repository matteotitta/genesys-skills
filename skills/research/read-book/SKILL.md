---
name: read-book
version: '1.0'
last_updated: 2026-07-08
author: genesys-growth
description: 'Reads a book or long PDF and extracts structured, reusable notes — chunks
  by chapter (TOC) or 50-page block, pulls per-chapter TL;DR, key concepts, verbatim
  quotes with page refs, action items, and named frameworks, then writes a dated clip
  to the taste-library. Four modes: notes (default, chapter-by-chapter), summary (whole-book
  TL;DR + takeaways), quotes (pull-quotes only), study (notes + Q&A spaced-rep). Triggers:
  "read book", "book notes", "summarize PDF", "summarize this ebook", "extract frameworks
  from", "pull quotes from", "what''s in this book". Handles PDF, markdown,.txt, pasted
  text, and URL natively; EPUB/MOBI convert-to-PDF first. Upstream: none. Downstream:
  feeds content-strategy and thought-leadership.'
goal: Extract structured, reusable notes from a book or long PDF into a dated taste-library clip.
outcome: A source-notes clip carrying TL;DR, key takeaways, verbatim quotes with page
  refs, action items, and named frameworks — a grep-able knowledge asset content-strategy
  and thought-leadership pull from for evidence, angles, and proof points.
primitive: research
ontology_type: source-notes
review_gate: 1
inputs:
  required: []
  recommended: []
- type: source-notes
  feeds_into:
  - content-strategy
  - thought-leadership
depends_on: []
- content-strategy
- thought-leadership
owned_by_agent: researcher
mcps_used:
- firecrawl
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# Read book

Turn a book or long PDF into structured, grep-able notes. Same content-consumption pattern every time: ingest → chunk → extract → write a dated clip to the taste-library. The clip is the deliverable — a knowledge asset that `/content-strategy` and `/thought-leadership` pull from for evidence, angles, and named frameworks.

## Triggers

"read book", "read this book / PDF", "book notes", "extract notes from this PDF", "summarize this ebook", "what's in this book", "pull quotes from this", "extract frameworks from [book]".

## What it accepts

| Input | How it's read |
|---|---|
| **PDF** | The `Read` tool reads PDFs natively (~10 pages per call — chunk longer books). The `pdf` skill handles extraction edge cases. |
| **Markdown /.txt** | `Read` directly. No conversion. |
| **Pasted text** | Use what was pasted. Treat a short paste as one chunk. |
| **URL** (public-domain text) | `WebFetch` first (free). Firecrawl (`firecrawl_scrape`) only if the page is JS-heavy or blocked. Project Gutenberg / archive.org `.txt` URLs are cleanest. |
| **EPUB / MOBI** | Convert to PDF or markdown first (`ebook-convert`, calibre), then read as PDF. If no converter is installed, deferred — give the user the one-line install. |

Detect type from the file extension or URL. If ambiguous, ask.

## Modes

| Invocation | Mode | What you get |
|---|---|---|
| `read-book <input>` | **notes** (default) | Chapter-by-chapter: TL;DR + key concepts + quotes + action items + frameworks |
| `read-book <input> summary` | summary | Whole-book TL;DR (1 paragraph) + 3–5 takeaways + who-it's-for |
| `read-book <input> quotes` | quotes | Pull-quote highlights only, with chapter + page refs |
| `read-book <input> study` | study | Notes + 10–20 spaced-repetition Q&A cards |

Full per-mode templates: the premium reference. A long book (>200 pages) with no mode given defaults to notes — warn it'll take many read passes.

## Process

### Step 1 — Parse input and mode

Detect the format (table above) and the mode (default notes). Confirm the target book if the input is ambiguous.

### Step 2 — Get the text and plan the chunks

Per-source ingestion: the premium reference. Chunk in priority order:

1. **By chapter** when a TOC exists (PDF bookmarks, or converted EPUB chapter headers).
2. **By 50-page block** for PDFs with no TOC.
3. **By 30,000-char block** (~7,500 words) for markdown / text.

Keep a short chunking plan (source, title, author, type, total pages, strategy, chunk list) in the scratchpad — not in the repo.

### Step 3 — Read each chunk and extract

Loop: read chunk N → extract per the chosen mode (the premium reference) → append the partial to the scratchpad. For PDFs, read chunks individually — never the whole book in one call (the PDF Read cap is ~10 pages). If a chunk is front-matter or diagrams with nothing to extract, log the skip and continue.

### Step 4 — Aggregate into the full notes

Combine the chunk partials into the mode's full-book shape: TL;DR, key takeaways (3–7 — the ones that survive forgetting), who-it's-for, verdict, chapter notes, and cross-reference suggestions.

### Step 5 — Write the taste-library clip

The clip is the deliverable. Write to:

```
projects/research/taste-library/resources/{MMYY}-{slug}.md
```

`{MMYY}` = current month+year (0726 = July 2026). `{slug}` = author + short-title in kebab-case (`0726-hormozi-100m-offers.md`). Frontmatter matches the taste-library clip convention (below). Confirm the `tags` against the blessed vocabulary in `projects/research/taste-library/CLAUDE.md`, and write a real `why` — a clip without a `why` is a bookmark, not a taste signal.

### Step 6 — Report

In chat: one-line headline (`<title> · <author> · <pages or words> · <mode> · <chunks>`), the clip path, the TL;DR, and the top 3 takeaways (top 3 quotes for quotes mode).

## Evidence discipline

Bound by [`.claude/rules/evidence-bound-outputs.md`](../../../rules/evidence-bound-outputs.md). Quotes are the highest-value output and the easiest to corrupt:

- **Quote verbatim.** Copy the exact words. Never paraphrase into quotation marks.
- **Cite the locator.** Page number (`p. 84`) when available; chapter + paragraph (`Ch 3, ¶12`) for EPUB-converted books with no stable pages.
- **Attribute.** When the author quotes someone else, name them after the quote. When it's the author, no attribution is needed.
- **Never invent.** If the book doesn't say it, it doesn't go in the notes. Flag a gap rather than fill it.

## Quality notes

- **Don't flatten.** A 30-page chapter earns 8–15 lines, not 3. Compression is good; flattening loses the specifics that make the clip worth keeping.
- **Preserve specifics.** Names, numbers, dates, examples — keep them. The point is that later you can grep "what did X say about Y" and find it.
- **Action items are explicit.** When the book makes you think "I should do X," flag it. These are the highest-leverage lines for GTM work.
- **Name the frameworks.** When the author names a framework, call it out by name — a framework you remember outperforms ten ideas you forget.
- **Push back.** In notes and study mode, surface disagreements. Reading critically beats reading reverently.

## Error handling

| Failure | Response |
|---|---|
| EPUB/MOBI, no converter | `brew install calibre` (`ebook-convert`) or `brew install pandoc`, then convert to PDF/markdown first. |
| Scanned PDF (no text layer) | OCR first: `brew install ocrmypdf && ocrmypdf <in.pdf> <out.pdf>`. |
| PDF has no TOC | Fall back to 50-page chunks; note it in the clip. |
| Book >500 pages | Warn on time and read passes; offer summary mode instead of full notes. |
| Chunk extracts nothing | Skip, log, continue — don't fail the whole run. |

## Composes with

- **`/content-strategy`** — book takeaways and frameworks feed cluster planning and content angles.
- **`/thought-leadership`** — quotes, frameworks, and pushback become evidence and counterpoints in long-form.
- **`/deep-research`** — when a research question surfaces a book, this is the next step; notes feed back into the brief.
- **`/storytelling`** and **`/gtme-pulse`** — book stories and stats become narrative and newsletter material.

## Attribution

Adapts [`coreyhaines31/makerskills/read-book`](https://github.com/coreyhaines31/makerskills) (MIT, © 2026 Corey Haines), accessed 2026-07-08. Re-pointed at our taste-library as the notes sink.
