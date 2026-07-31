---
name: gdrive-create
version: '1.0'
last_updated: 2026-02-11
author: genesys-growth
description: 'Creates branded Google Docs, Slides, and Sheets via GDrive MCP scripts, automatically routing documents to the
  correct client folder using the --client slug. Produces google-doc, google-slides, or google-sheet outputs with client branding
  (colors, fonts, logos via Clearbit). Triggers: "create a Google Doc", "push to Drive", "make slides", "create a sheet",
  "export to GDrive", "push this to Google Drive". Recommended upstream: brand-kit for visual branding. NOT for creating content
  — use content skills first, then this skill to export.'
goal: Creates branded Google Docs, Slides, and Sheets via GDrive MCP scripts, automatically routing documents to the correct
  client folder using the --client slug.
outcome: 'Creates branded Google Docs, Slides, and Sheets via GDrive MCP scripts, automatically routing documents to the correct
  client folder using the --client slug. Produces google-doc, google-slides, or google-sheet outputs with client branding
  (colors, fonts, logos via Clearbit). Triggers: "create a...'
primitive: meta
sub_primitive: infra
ontology_type: runbook
review_gate: 1
inputs:
  required: []
  recommended:
  - brand-kit
- type: google-doc
  feeds_into: []
- type: google-slides
  feeds_into: []
- type: google-sheet
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used:
- gdrive
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
paths:.claude/mcp/gdrive/**
---

# Google Drive document creation

Create branded Google Docs, Slides, and Sheets in the correct client folder. This skill is the single entry point for all Google Drive document creation across the entire system.

## When to use

- Any skill produces a deliverable (proposal, research, analysis, deck, tracker)
- User explicitly asks to "create a Google Doc", "push to Drive", "make a slide deck", "create a spreadsheet"
- After running `/client-proposals`, `/competitor-research`, `/product-messaging`, `/sales-enablement`, or any deliverable-producing skill

## Process

### Step 1: Determine document type

| User intent | Document type | Script |
|-------------|--------------|--------|
| Written deliverables (proposals, research, analysis) | Google Doc | `create-doc-unified.mjs` |
| Presentations, decks, pitch materials | Google Slides | `create-slides.mjs` |
| Data, trackers, comparisons, matrices | Google Sheets | `create-sheet.mjs` |

### Step 2: Identify client context

**Priority order:**
1. User explicitly names the client
2. Current working directory is inside `/project-consulting/{client-name}/`
3. File path contains a client identifier
4. Ask: "Which client is this for?"

**Valid client slugs** (from `gdrive-config.json`):
- `ClientCo` → PJ - ClientCo folder
- `ClientCo` → PJ - Proposals folder
- `gtm-e-school` → PJ - Proposals folder
- `genesys-growth` → PJ - Proposals folder
- `alphastream` → PJ - Alphastream folder
- `talli` → PJ - Talli.ai folder
- `archive` → PJ - Archive folder

### Step 3: Save deliverable as markdown

Before pushing to Google Drive, the deliverable must exist as a `.md` file. Save it following the naming convention: `MMYY-topic.md`

### Step 4: Run the appropriate script

#### Google Docs

```bash
cd dev-tools/mcp/gdrive && node create-doc-unified.mjs \
  "/full/path/to/file.md" \
  "Company Name" \
  --client {client-slug} \
  --title "Document Title"
```

**Parameters:**
- `file.md` — Path to the markdown file (required)
- `"Company Name"` — Full company name for the header (required)
- `--client` — Client slug from config (optional, routes to correct folder)
- `--title` — Custom document title, defaults to "Scope of work" (optional)
- `--folder` — Override folder ID (optional, overrides client config)

#### Google Slides

```bash
cd dev-tools/mcp/gdrive && node create-slides.mjs \
  "/full/path/to/file.md" \
  "Company Name" \
  --client {client-slug}
```

**Markdown format for slides:**
```markdown
# Presentation Title

## Slide 1 Title
- Bullet point
- Another point

## Slide 2 Title
### Section heading (bold)
- More content
```

- `#` = Presentation title (becomes title slide)
- `##` = New slide
- `###` = Bold subtitle within a slide
- `-` or `*` = Bullet points
- Indented bullets = nested bullets

**Branding:** Client logo from Clearbit API is placed top-right on every slide. Title uses client's primary brand color.

#### Google Sheets

```bash
cd dev-tools/mcp/gdrive && node create-sheet.mjs \
  "Sheet Title" \
  --client {client-slug} \
  --data "/path/to/data.csv"
```

**Parameters:**
- `"Sheet Title"` — Name of the spreadsheet (required)
- `--client` — Client slug (optional)
- `--data` — Path to CSV file to import (optional)

**Branding:** Header row gets client's primary color background with white bold text. Alternating row colors for readability. Frozen header row.

## Configuration

All client folder IDs and brand settings live in:

```
dev-tools/mcp/gdrive/gdrive-config.json
```

### Adding a new client

1. Get the Google Drive folder ID (run `node list-folders.mjs` or create a new folder)
2. Add to `gdrive-config.json`:
```json
{
  "new-client": {
    "name": "New Client",
    "domain": "newclient.com",
    "folderId": "FOLDER_ID",
    "brand": {
      "primaryColor": "#HEXCOLOR",
      "font": "Inter"
    }
  }
}
```
3. Optionally run `/brand-kit` on the client's website to extract exact colors

### Updating brand colors

If a client's brand changes or you want more accurate colors:
1. Run `/brand-kit https://client-website.com`
2. Update the `brand` object in `gdrive-config.json`

## Integration with other skills

When any skill finishes producing a deliverable, offer:

> "Want me to create this as a Google Doc in the {client} folder?"

If yes, follow the process above. This applies to all deliverable-producing skills including but not limited to:
- `/client-proposals`
- `/competitor-research`
- `/product-messaging`
- `/landing-page-copy`
- `/sales-enablement`
- `/icp-research`
- `/win-loss-analysis`
- `/transcript-analysis`

## Authentication

Scripts use OAuth 2.0 with tokens at `dev-tools/mcp/gdrive/credentials/token.json`.

If authentication fails:
1. Delete `credentials/token.json`
2. Run `cd dev-tools/mcp/gdrive && node auth.mjs`
3. Authorize in browser
4. Re-run the creation script

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Token expired" | Run `node auth.mjs` to refresh |
| Wrong folder | Check `gdrive-config.json` folder ID or use `--folder` override |
| No logo on slides | Verify client `domain` in config is correct (Clearbit needs valid domain) |
| "Scope insufficient" | Delete token.json and re-auth (scopes were updated to include Slides/Sheets) |
