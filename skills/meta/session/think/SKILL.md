---
name: think
version: '1.0'
last_updated: 2026-05-23
author: genesys-growth
description: 'Temporal-trajectory-aware recall. Routes a question through a zero-LLM-cost intent classifier (temporal / knowledge_update / other). Temporal questions ("when did X last Y", "what changed since Z") get spliced answers from chronologically-sorted client history.md + goals/MMYY-NN-cycle.md + dated memory pages + extracted session decisions. Knowledge-update questions ("what is the latest on X", "any new on Y") filter the same sources to since-date or last-N. Other questions short-circuit to /recall. Triggers: "/think [question]", "when did", "when was the last", "what changed", "what is the latest", "any new on", "what happened with". NOT for live web research — use Exa per brain-first-lookup ladder Step 4. NOT for general session search — use /recall (this skill chains into it for non-temporal queries).'
goal: Route a question through an intent classifier and answer temporal / knowledge-update questions with a spliced chronological timeline from local sources.
outcome: Chronological timeline answering temporal or knowledge-update questions, spliced from client history.md, sprint cycles, memory pages, and extracted session decisions.
primitive: meta
sub_primitive: session
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
triggers:
  slash_commands:
  - /think
  natural_language:
  - "when did"
  - "when was the last"
  - "what changed since"
  - "what's the latest on"
  - "any new on"
  - "what happened with"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# /think — Temporal-trajectory queries against the brain

Answer "when did X last Y" / "what changed since Z" / "what's the latest on W" by splicing dated entries from client `history.md`, sprint `goals/MMYY-NN-cycle.md`, memory pages, and session decisions into a chronological timeline. Zero LLM cost on intent classification — regex routes the query, the splice does the work.

Stolen from `garrytan/gbrain` (v0.40.2.0) via /steal Phase 5–6 (2026-05-23). See [`.claude/discovery/0526-gbrain-steal-analysis.md`](../../../../discovery/0526-gbrain-steal-analysis.md) item G19.

---

## Triggers

**Invoke this skill when the user says:**

- `/think [question]`
- "When did Alan last push back on positioning?"
- "When was the last time we shipped a Pulse?"
- "What changed in ClientCo's pricing since the March doc?"
- "What's the latest on ClientCo's GTM stack build?"
- "Any new on ClientCo?"
- "What happened with the Notion shadow-pull thing?"

**Do NOT invoke when:**

- The question is rule-shaped or convention-shaped ("do we have a rule about X?") — use `/recall --memory`
- The question is decision-extraction shaped ("what did we decide about X?") — use `/recall --decisions`
- The question is research-shaped or external ("what's Salesloft launching this week?") — follow `.claude/rules/brain-first-lookup.md` then Exa per `exa-protocol.md`
- The question is in-session reasoning ("what should we do next?") — just answer

If unsure between `/think` and `/recall`: `/think` is for *when-shaped* and *what-changed-shaped* questions; `/recall` is for *what-was-decided* and *what-was-discussed* questions.

---

## Process

### Step 1 — Classify intent (regex, zero-LLM)

Apply the classifier to the input question. Three intents:

| Intent | Regex pattern (case-insensitive) | Routing |
|---|---|---|
| **temporal** | `\b(when|last time|first time|how long since|since when)\b` OR `\bwhen (did|was|were|had)\b` | Step 2 (timeline splice) |
| **knowledge_update** | `\b(latest|recent|new|updated|changed|current)\b.*\bon\b` OR `\bwhat (is|are) the (latest|current|new)\b` OR `\bany new\b` OR `\bsince (the|last)\b` | Step 3 (since-filter splice) |
| **other** | (no match) | Fast-path: short-circuit to `/recall <topic>` |

Implementation note: the classifier is deterministic — no model call. Wrong classification degrades gracefully (the source files still surface; the ordering is just less optimal). Default if ambiguous: `temporal`.

### Step 2 — Temporal splice (chronological timeline)

For temporal intent, build a unified chronological timeline by reading these sources:

1. **Client `history.md`** if a client name is in the query — `projects/consulting/active/{client}/history.md` (append-only ops record)
2. **Client sprint cycles** if a client name is in the query — `projects/consulting/active/{client}/goals/*-cycle.md` (dated cycle files)
3. **Memory pages** sorted by `indexed_at` from `memory_pages` table (G13) — filter by topic keyword
4. **Session decisions** sorted by `timestamp` from `decisions` table — filter by topic + optional `--client`

Splice + sort:

- Each entry gets a normalized `(date, source, claim)` triple
- Sort descending by date (most recent first)
- Limit to the top 20 entries or the last 90 days, whichever is smaller

Output format:

```
TIMELINE — "<query>"
────────────────────────────────────────
2026-05-23 [history] {history.md entry}
                        ↳ projects/consulting/active/{client}/history.md
2026-05-21 [decision] {decision text}
                        ↳ session {id_short}
2026-05-17 [memory] {memory page title}
                        ↳ memory/{slug}.md (tier {boost}x)
2026-05-15 [cycle] {cycle file headline}
                        ↳ goals/0526-02-cycle.md
...
```

For "when did X last Y" questions: find the most-recent entry matching X+Y, return it with full context. For "first time" questions: same logic, ascending sort.

### Step 3 — Knowledge-update splice (since-date filter)

For knowledge_update intent, parse the implicit time anchor and filter:

| Anchor | Filter |
|---|---|
| "latest" / "current" / "recent" | Last 30 days |
| "any new" / "new on" | Last 14 days |
| "since the March doc" / "since v3" | Find the named anchor; filter to entries after its date |
| "since last [week/month]" | Compute the date; filter accordingly |

Same sources as Step 2 (history.md + cycles + memory + decisions). Same chronological output, but filtered to the since-window.

### Step 4 — Fast-path short-circuit (other intent)

If the intent classifier returns `other`, the question isn't temporal-shaped. Don't build a timeline — just hand off to `/recall <topic>` and return its result. This is the cheap default — most questions are not temporal, and routing them through the splice machinery would burn time for no gain.

---

## Worked examples

### Example 1 — "When did Alan last push back on positioning?"

- Intent: **temporal** (matches `\bwhen did\b`)
- Sources scanned: `projects/consulting/active/ClientCo/history.md` + memory pages with "alan" + session decisions filtered to `--client "ClientCo"`
- Output: most-recent entry surfaces (e.g., `2026-03-18 [decision] Alan pushed back on "MVP test" → compliance friction reclassification`)

### Example 2 — "What's the latest on ClientCo's GTM stack build?"

- Intent: **knowledge_update** (matches `\bwhat is the latest\b.*\bon\b`)
- Window: last 30 days
- Sources scanned: `projects/consulting/active/ClientCo/history.md` + sprint cycles + decisions
- Output: chronological timeline of the last 30 days of ClientCo activity, most-recent first

### Example 3 — "What did we decide about positioning?"

- Intent: **other** (no temporal regex match)
- Short-circuit: hand off to `/recall --decisions` filtered by topic "positioning"
- No timeline built — the question is decision-shaped, not when-shaped

### Example 4 — "Since the March doc, what changed on ClientCo pricing?"

- Intent: **knowledge_update** (matches `\bsince the\b`)
- Anchor: "March doc" → resolve to `projects/consulting/active/ClientCo/pricing/0326-*.md` mtime → filter to entries after
- Output: chronological timeline of pricing-related entries after the March doc

---

## Data sources (read paths)

| Source | Path | Date field |
|---|---|---|
| Client history.md | `projects/consulting/active/{client}/history.md` | date prefix on each line (e.g., `2026-05-21 —...`) |
| Client sprint cycles | `projects/consulting/active/{client}/goals/*-cycle.md` | filename `MMYY-NN-cycle.md` (NN = sprint #) |
| Memory pages | recall.db `memory_pages` table | `indexed_at` column |
| Session decisions | recall.db `decisions` table | `timestamp` column |

For client name extraction from the query, match against CLIENT_MAP from `session-indexer.py` (ClientCo, ClientCo, ClientCo, ClientCo, etc.).

---

## Anti-hallucination guardrails

1. **Never fabricate timeline entries.** Only return entries actually found in the source files. If a query matches nothing, say "no temporal entries found for {query}" — don't synthesize.
2. **Always cite the source path + date.** Every timeline row has a `↳ {path}` line. The user can verify.
3. **Don't paraphrase entries.** Quote the verbatim line from `history.md` or memory page; the verbatim phrasing IS the signal (per `.claude/rules/auto-memory.md`).
4. **Respect the brain-first-lookup ladder.** If the timeline is empty AND the question is research-shaped, escalate per `.claude/rules/brain-first-lookup.md` Step 4 — don't fill the gap with external data without explicit user approval.
5. **Cap output at top-20 or 90 days.** Longer timelines drown the reader; if more depth is needed, the user can ask `/think --since 6mo`.

---

## When to use this skill vs. its neighbors

| Question shape | Right tool |
|---|---|
| "When did X last Y?" | `/think` (temporal) |
| "What's the latest on X?" | `/think` (knowledge_update) |
| "What changed since [date/anchor]?" | `/think` (knowledge_update) |
| "Do we have a rule about X?" | `/recall --memory` (rule lookup) |
| "What did we decide about X?" | `/recall --decisions` (decision extraction) |
| "Find the session where we built X" | `/recall [topic]` (session content) |
| "What's happening today?" | `/today` (live productivity surface) |
| "Pick up where I left off" | `/recall` (default session search) |

The fast-path short-circuit means `/think` is safe to invoke broadly — non-temporal questions just route through to `/recall` without overhead.

---

## Composition with adjacent skills + rules

| Rule / Skill | Composition |
|---|---|
| `.claude/rules/brain-first-lookup.md` | `/think` is one of the Step-1 entry points when the question is temporal-shaped. Failed temporal lookup → escalate through Step 2-4 of the ladder |
| `.claude/rules/auto-memory.md` | Memory pages with `[[link]]`s surface in the timeline alongside their cluster — disciplined writes feed temporal recall |
| `/recall` | Short-circuit destination for non-temporal queries. Also the source of `decisions` table joined into Step 2 splice |
| `/session-wrap` | Writes the decisions + memory entries that this skill reads later |
| `/today` | Different time axis — today is forward-looking (what's on the calendar / inbox / Linear); think is backward-looking (what happened with X) |

---

## Anti-patterns

- ❌ Running `/think` on every question. The fast-path costs near-zero, but it adds a layer of indirection — only invoke when the question is temporal-shaped or you want the classifier to decide.
- ❌ Treating the classifier as infallible. Misclassification degrades gracefully; check the output and re-route manually if needed.
- ❌ Splicing too many sources. Top-20 / 90-day cap is the discipline; more drowns the signal.
- ❌ Paraphrasing source entries in the timeline. Quote verbatim with path + date.
- ❌ Filling temporal gaps with external research. If the brain has nothing, say so; don't invent a "latest on X" from training data.

---

