#!/usr/bin/env python3
"""
Phase 4 frontmatter migration tool.

Transforms legacy SKILL.md frontmatter into the canonical Phase 4 shape per
.claude/skills/_schema/skill-frontmatter.schema.json.

Design:
- Strictly deterministic. No agent inference.
- Preserves SKILL.md body byte-for-byte.
- Reads + writes only the YAML frontmatter block (between leading --- markers).
- Drops fields not allowed by the schema (additionalProperties: false).

Usage:
    python migrate-frontmatter.py <SKILL.md path> [<SKILL.md path>...]
    python migrate-frontmatter.py --dry-run <path>     # show diff, no write
    python migrate-frontmatter.py --report <path>      # only print would-be changes

Exit codes:
    0 = all migrations succeeded
    1 = one or more migrations failed
    2 = script error
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

SCHEMA_PATH = Path(".claude/skills/_schema/skill-frontmatter.schema.json")
TEMPLATES_DIR = Path(".claude/skills/_schema/output-templates")
COMMANDS_DIR = Path(".claude/commands")

# Fields the schema accepts. Anything not in this set gets dropped.
ALLOWED_FIELDS = {
    "name", "version", "author", "last_updated", "description", "goal", "outcome",
    "primitive", "sub_primitive", "ontology_type", "review_gate",
    "inputs", "outputs", "depends_on", "feeds_into",
    "owned_by_agent", "mcps_used", "push_targets", "triggers",
    "status", "locked_by", "locked_date", "lock_version", "sources_count",
    "context", "effort", "paths", "disable-model-invocation",
}

# Legacy → canonical field renames
RENAMES = {
    "dependencies": "inputs",
    "export_destinations": "_export_destinations_legacy",   # consumed for push_targets inference, then dropped
    "mcp_integrations": "_mcp_integrations_legacy",         # consumed for mcps_used inference, then dropped
}

# Fields explicitly dropped (legacy concepts not in schema)
DROP_FIELDS = {"run_modes"}

# Role mapping: skill name fragment → owned_by_agent
ROLE_MAP = [
    # researcher
    (r"^company-context$|^competitor-research$|^icp-(research|behavioural)$|^tov-guidelines$|^brand-kit$|^transcript|^expert-pov$|^win-loss|^customer-interviews$|^funnel-strategy$|^deepline-enrich$", "researcher"),
    # pmm
    (r"^positioning$|^product-messaging$|^messaging$|^content-strategy$|^pricing-(strategy|research)$|^website-score$|^website-audit$", "pmm"),
    # growth
    (r"^landing-page-|^case-study$|^lifecycle|^email-nurture$|^product-launch$|^webinar(-brief)?$|^storytelling$|^website-grader$", "growth"),
    # content
    (r"^linkedin-|^youtube-|^aeo-content$|^thought-leadership$|^hype-man$|^newsletter$|^vibe-coding$|^content-cascade$|^one-pager$", "content"),
    # b2b-consultant
    (r"^client-(discovery|proposals|onboarding|context)$|^discovery$|^proposal$|^new-client$|^outreach-emails$|^outreach$", "b2b-consultant"),
    # sales
    (r"^battlecards$|^demo-script$|^sales-deck$|^abm(-campaign)?$|^clay-search$|^sales-enablement|^win-loss-analysis$", "sales"),
    # paid
    (r"^ad-creative-brief$|^google-ads-|^linkedin-ads-|^paid-", "paid"),
]
# default → operator (covers all meta + ungrouped)

# MCP detection patterns: regex → mcp slug
MCP_PATTERNS = [
    (r"mcp__exa__|mcp__plugin_exa_exa__|mcp_/exa/|exa_search|web_search_exa|company_research_exa|find_similar_links_exa|web_fetch_exa", "exa"),
    (r"mcp__apollo|mcp__claude_ai_Apollo_io__|apollo[_-]search_(people|companies)|apollo[_-]enrich|Apollo MCP", "apollo-io"),
    (r"mcp__firecrawl__|firecrawl_(scrape|crawl|search|extract|map)", "firecrawl"),
    (r"mcp__apify__|apify[--_](rag|web)", "apify"),
    (r"mcp__claude_ai_Notion__|mcp__notion-api__|Notion MCP", "notion"),
    (r"mcp__claude_ai_Linear__|Linear MCP", "linear"),
    (r"mcp__claude_ai_Slack__|Slack MCP", "slack"),
    (r"mcp__claude_ai_Gmail__|mcp__google-workspace__.*gmail|Gmail MCP", "gmail"),
    (r"mcp__google-workspace__.*calendar|mcp__claude_ai_Google_Calendar__", "google-calendar"),
    (r"mcp__claude_ai_Google_Drive__|mcp__google-workspace__.*drive|gdrive[/-]config|create-doc-unified|create-slides|create-sheet|create-pulse", "gdrive"),
    (r"mcp__claude_ai_Attio__|Attio MCP", "attio"),
    (r"mcp__xero__|Xero MCP", "xero"),
    (r"mcp__claude_ai_Clay__|Clay MCP", "clay"),
    (r"mcp__claude_ai_Figma__|Figma MCP", "figma"),
    (r"mcp__claude_ai_Ahrefs__|Ahrefs MCP|brand-radar|gsc-keyword|keywords-explorer|site-explorer", "ahrefs"),
    (r"mcp__gsc__|Google Search Console MCP|gsc_search_analytics|gsc_inspect_url", "google-search-console"),
    (r"mcp__claude_ai_Granola__|Granola MCP", "granola"),
    (r"mcp__claude_ai_Supabase__|Supabase MCP", "supabase"),
    (r"mcp__claude_ai_Vercel__|Vercel MCP", "vercel"),
    (r"mcp__trigger__|trigger\.dev|Trigger\.dev MCP", "trigger-dev"),
    (r"mcp__claude_ai_Canva__|Canva MCP", "canva"),
    (r"mcp__claude_ai_Gamma__|Gamma MCP", "gamma"),
    (r"mcp__claude_ai_Calendly__|Calendly MCP", "calendly"),
    (r"mcp__claude_ai_Zapier__|Zapier MCP", "zapier"),
    (r"mcp__youtube-transcript__|YouTube Transcript MCP", "youtube-transcript"),
    (r"deepline\b", "deepline"),
]

# canonical_render → push_targets default
PUSH_TARGETS_DEFAULTS = {
    "gdrive-doc": ["gdrive", "notion"],
    "gdrive-sheet": ["gdrive", "notion"],
    "gdrive-slides": ["gdrive"],
    "local": [],
    "app": [],
    None: ["gdrive", "notion"],
}


def load_template_render_map():
    """Map ontology_type → canonical_render from output-templates."""
    out = {}
    for f in sorted(TEMPLATES_DIR.glob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text()
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        kt = fm.get("knowledge_type", f.stem)
        out[kt] = fm.get("canonical_render")
    return out


SCHEMA_TOP_KEYS = {
    "name", "version", "author", "last_updated", "description", "goal", "outcome",
    "primitive", "sub_primitive", "ontology_type", "review_gate",
    "inputs", "outputs", "depends_on", "feeds_into",
    "owned_by_agent", "mcps_used", "push_targets", "triggers",
    "status", "locked_by", "locked_date", "lock_version", "sources_count",
    "context", "effort", "paths", "disable-model-invocation",
    # Legacy keys we want to heal so we can read + drop later
    "dependencies", "export_destinations", "mcp_integrations", "run_modes",
}


def heal_yaml_text(yaml_text):
    """Pre-clean common Phase 3 YAML corruption before parsing."""
    out_lines = []
    for line in yaml_text.splitlines():
        # Pattern 1: `^([\w-]+):\s+- ...` (top-level key with inline list)
        m = re.match(r"^([\w-]+):\s+(- .*)$", line)
        if m and m.group(1) in SCHEMA_TOP_KEYS:
            out_lines.append(f"{m.group(1)}:")
            out_lines.append(f"  {m.group(2)}")
            continue
        # Pattern 2: `^(key): (subkey): rest` (inline mapping under known top-level key)
        m = re.match(r"^([\w-]+):\s+([\w-]+):\s*(.*)$", line)
        if m and m.group(1) in SCHEMA_TOP_KEYS:
            key, subkey, rest = m.group(1), m.group(2), m.group(3)
            out_lines.append(f"{key}:")
            out_lines.append(f"  {subkey}: {rest}")
            continue
        out_lines.append(line)
    return "\n".join(out_lines)


def parse_frontmatter(text):
    """Return (frontmatter_dict, body_text). frontmatter_dict={} if missing.
    Tries plain parse first; on failure, heals known Phase 3 corruption and retries.
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text
    raw_yaml = m.group(1)
    body = text[m.end():]
    try:
        fm = yaml.safe_load(raw_yaml) or {}
        return fm, body
    except yaml.YAMLError:
        # Try once with healing
        healed = heal_yaml_text(raw_yaml)
        try:
            fm = yaml.safe_load(healed) or {}
            return fm, body
        except yaml.YAMLError as e2:
            raise ValueError(f"YAML parse error after healing: {e2}")


def heal_pipe_string(value):
    """Strip a leading `|` artifact from a literal-block-leak description.
    Phase 3 sloppily produced `description: |\n  |\n    Real text` which loads
    as the literal string `|\n    Real text`. We detect and unwrap.
    """
    if not isinstance(value, str):
        return value
    s = value.strip()
    if s.startswith("|"):
        # Drop the leading | line, dedent the rest
        lines = s.split("\n")
        rest = lines[1:] if len(lines) > 1 else [s.lstrip("|").strip()]
        # Dedent
        dedented = []
        for ln in rest:
            dedented.append(ln.strip())
        cleaned = " ".join(x for x in dedented if x)
        return cleaned.strip() or value
    return value


def reparse_nested_yaml(value, fallback):
    """When a field comes through as a string of YAML (Phase 3 leak), re-parse it.
    Return parsed value or fallback if parsing fails or yields unexpected shape.
    """
    if not isinstance(value, str):
        return value
    s = value
    if s.lstrip().startswith("|"):
        s = s.lstrip().lstrip("|")
    lines = [ln for ln in s.splitlines() if ln.strip()]
    if not lines:
        return fallback
    indents = [len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()]
    min_indent = min(indents) if indents else 0
    dedented = "\n".join(ln[min_indent:] if len(ln) >= min_indent else ln for ln in s.splitlines())
    try:
        parsed = yaml.safe_load(dedented)
        if parsed is None:
            return fallback
        return parsed
    except yaml.YAMLError:
        return fallback


def regex_extract_outputs(value):
    """Last-resort: extract outputs from a corrupted YAML literal-block string.
    Returns [{type, feeds_into}, ...] or None if no extractions found.
    """
    if not isinstance(value, str):
        return None
    out = []
    # Find each `- type: X` block, then look for following `feeds_into:` and bullet entries
    # Split on `- type:` boundaries
    blocks = re.split(r"(?=^\s*-\s*type:)", value, flags=re.MULTILINE)
    for block in blocks:
        type_m = re.search(r"-\s*type:\s*([\w-]+)", block)
        if not type_m:
            continue
        type_val = type_m.group(1)
        # Find feeds_into list — bullet entries between this block's start and the next type
        feeds = re.findall(r"^\s*-\s*([\w-]+)\s*$", block, flags=re.MULTILINE)
        # Filter out the type names themselves
        feeds = [f for f in feeds if f != type_val]
        out.append({"type": type_val, "feeds_into": feeds})
    return out if out else None


def regex_extract_dependencies(value):
    """Extract `required:` and `recommended:` lists from a corrupted dependencies string."""
    if not isinstance(value, str):
        return None
    result = {"required": [], "recommended": []}
    # Find `required:` followed by either inline `[a, b]` or bullet list
    for key in ("required", "recommended"):
        # Try inline list first
        m = re.search(rf"{key}:\s*\[([^\]]*)\]", value)
        if m:
            items = [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]
            result[key] = items
            continue
        # Try block list — find `key:` line, then collect following `- item` lines
        m = re.search(rf"{key}:\s*$", value, flags=re.MULTILINE)
        if m:
            # Lines after this match
            tail = value[m.end():]
            # Collect leading `- item` lines (until a non-list line)
            items = []
            for ln in tail.splitlines():
                bm = re.match(r"^\s*-\s*([\w-]+)\s*$", ln)
                if bm:
                    items.append(bm.group(1))
                elif ln.strip() and not ln.strip().startswith("-"):
                    break
            result[key] = items
    return result


def serialize_frontmatter(fm):
    """Dump YAML frontmatter with deterministic key order + readable lists."""
    # Order keys per the SKILL.template.md grouping
    order = [
        # Identity
        "name", "version", "last_updated", "author",
        # Trigger surface
        "description", "goal", "outcome",
        # Taxonomy
        "primitive", "sub_primitive", "ontology_type", "review_gate",
        # Graph edges
        "inputs", "outputs", "depends_on", "feeds_into",
        # Operations
        "owned_by_agent", "mcps_used", "push_targets", "triggers",
        # Lifecycle
        "status", "locked_by", "locked_date", "lock_version", "sources_count",
        # Legacy permitted
        "context", "effort", "paths", "disable-model-invocation",
    ]
    ordered = {}
    for k in order:
        if k in fm:
            ordered[k] = fm[k]
    # Catch any allowed keys not in our order (defensive)
    for k in fm:
        if k not in ordered and k in ALLOWED_FIELDS:
            ordered[k] = fm[k]
    return yaml.safe_dump(
        ordered,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=120,
    )


def infer_owned_by_agent(name):
    """Pick owned_by_agent from skill name. Default operator for unmatched."""
    if not name:
        return "operator"
    for pattern, role in ROLE_MAP:
        if re.search(pattern, name):
            return role
    return "operator"


def infer_mcps_used(body_text):
    """Scan body for MCP usage patterns; return sorted unique list."""
    found = set()
    for pattern, slug in MCP_PATTERNS:
        if re.search(pattern, body_text, re.IGNORECASE):
            found.add(slug)
    return sorted(found)


def infer_push_targets(ontology_type, render_map, legacy_export=None):
    """Pick push_targets array. Use legacy export_destinations as hint if present."""
    # Preserve explicit legacy intent if it mentions framer/vercel
    if legacy_export is not None:
        legacy_str = json.dumps(legacy_export).lower() if not isinstance(legacy_export, str) else legacy_export.lower()
        targets = []
        if "gdrive" in legacy_str or "google_doc" in legacy_str or "google doc" in legacy_str or "google_drive" in legacy_str:
            targets.append("gdrive")
        if "notion" in legacy_str:
            targets.append("notion")
        if "framer" in legacy_str:
            targets.append("framer")
        if "github" in legacy_str:
            targets.append("github")
        if "vercel" in legacy_str:
            targets.append("vercel")
        if targets:
            return targets
    # Fall back to template default
    canon = render_map.get(ontology_type)
    return PUSH_TARGETS_DEFAULTS.get(canon, ["gdrive", "notion"])


def normalize_inputs(value):
    """Ensure inputs is {required: [], recommended: []}."""
    if value is None:
        return {"required": [], "recommended": []}
    if isinstance(value, dict):
        return {
            "required": value.get("required") or [],
            "recommended": value.get("recommended") or [],
        }
    # Legacy: list form (treat as required)
    if isinstance(value, list):
        return {"required": list(value), "recommended": []}
    return {"required": [], "recommended": []}


def normalize_outputs(value, ontology_type):
    """Ensure outputs is [{type: ..., feeds_into: [...]}]."""
    if value is None:
        return [{"type": ontology_type or "runbook", "feeds_into": []}]
    if isinstance(value, list):
        out = []
        for item in value:
            if isinstance(item, dict):
                out.append({
                    "type": item.get("type") or ontology_type or "runbook",
                    "feeds_into": item.get("feeds_into") or [],
                })
            elif isinstance(item, str):
                out.append({"type": item, "feeds_into": []})
        return out or [{"type": ontology_type or "runbook", "feeds_into": []}]
    if isinstance(value, str):
        return [{"type": value, "feeds_into": []}]
    return [{"type": ontology_type or "runbook", "feeds_into": []}]


def normalize_triggers(value, name):
    """Restructure triggers to {slash_commands, natural_language}."""
    out = {"slash_commands": [], "natural_language": []}
    # Add slash command if a matching command file exists
    if name:
        cmd_path = COMMANDS_DIR / f"{name}.md"
        if cmd_path.exists():
            out["slash_commands"] = [f"/{name}"]
    if value is None:
        return out
    if isinstance(value, dict):
        # Already canonical?
        if "slash_commands" in value or "natural_language" in value:
            sc = value.get("slash_commands") or out["slash_commands"]
            nl = value.get("natural_language") or []
            return {"slash_commands": list(sc), "natural_language": list(nl)}
        # Legacy keys
        nl = []
        for legacy_key in ("auto_suggest_when", "triggers", "examples"):
            v = value.get(legacy_key)
            if isinstance(v, list):
                nl.extend([str(x) for x in v if x])
        out["natural_language"] = nl
        return out
    if isinstance(value, list):
        out["natural_language"] = [str(x) for x in value if x]
    return out


def derive_goal(description):
    """One-sentence imperative ≤200 chars."""
    if not description:
        return "Produce canonical output per this skill's ontology type."
    desc = re.sub(r"\s+", " ", str(description)).strip()
    # Take first sentence
    m = re.match(r"^(.{20,200}?[.!?])(\s|$)", desc)
    if m:
        return m.group(1).strip()
    return desc[:200].rstrip()


def derive_outcome(description):
    """≤300 chars, what the locked artifact unblocks. Break at word boundary."""
    if not description:
        return "Locked artifact ready for downstream consumption."
    desc = re.sub(r"\s+", " ", str(description)).strip()
    if len(desc) <= 300:
        return desc
    # Break at last word boundary, leave room for trailing "..."
    cut = desc[:296].rsplit(" ", 1)[0].rstrip()
    result = cut + "..."
    return result if len(result) <= 300 else result[:300]


def derive_primitive_from_path(path):
    """Infer primitive from folder structure."""
    parts = Path(path).parts
    if "research" in parts:
        return "research"
    if "primitives" in parts:
        idx = parts.index("primitives")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    if "meta" in parts or "meta-skills" in parts:
        return "meta"
    if "client-skills" in parts:
        return "clients"
    if "content-skills" in parts:
        return "content"
    if "pmm-skills" in parts or "product-marketing-skills" in parts:
        return "product-marketing"
    if "sales-skills" in parts:
        return "sales-enablement"
    if "paid-marketing-skills" in parts or "paid-skills" in parts:
        return "paid-marketing"
    if "lifecycle-skills" in parts:
        return "lifecycle"
    if "growth-marketing-skills" in parts:
        return "website"
    return "meta"


def migrate_one(path, render_map, dry_run=False):
    """Migrate one SKILL.md. Returns (status, change_log)."""
    p = Path(path)
    if not p.exists():
        return "missing", []
    text = p.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as e:
        return f"parse_error: {e}", []
    if not fm:
        return "no_frontmatter", []

    changes = []
    new_fm = dict(fm)

    # 0. HEAL Phase 3 YAML corruption
    # 0a. description: strip leading `|` literal-block leak
    if isinstance(new_fm.get("description"), str):
        healed = heal_pipe_string(new_fm["description"])
        if healed != new_fm["description"]:
            new_fm["description"] = healed
            changes.append("healed: description (stripped pipe leak)")
    # 0b. outputs: re-parse if it came through as string
    if isinstance(new_fm.get("outputs"), str):
        raw = new_fm["outputs"]
        reparsed = reparse_nested_yaml(raw, None)
        if isinstance(reparsed, list) and reparsed:
            new_fm["outputs"] = reparsed
            changes.append("healed: outputs (yaml re-parse)")
        else:
            # Last resort: regex extraction
            extracted = regex_extract_outputs(raw)
            if extracted:
                new_fm["outputs"] = extracted
                changes.append(f"healed: outputs (regex extract, {len(extracted)} items)")
            else:
                new_fm["outputs"] = None
    # 0c. dependencies: re-parse if string
    if isinstance(new_fm.get("dependencies"), str):
        raw = new_fm["dependencies"]
        reparsed = reparse_nested_yaml(raw, None)
        if isinstance(reparsed, dict) and (reparsed.get("required") or reparsed.get("recommended")):
            new_fm["dependencies"] = reparsed
            changes.append("healed: dependencies (yaml re-parse)")
        else:
            extracted = regex_extract_dependencies(raw)
            if extracted and (extracted["required"] or extracted["recommended"]):
                new_fm["dependencies"] = extracted
                changes.append(f"healed: dependencies (regex extract, req={len(extracted['required'])} rec={len(extracted['recommended'])})")
            else:
                new_fm["dependencies"] = None
    # 0d. triggers: re-parse if string
    if isinstance(new_fm.get("triggers"), str):
        reparsed = reparse_nested_yaml(new_fm["triggers"], None)
        if isinstance(reparsed, dict):
            new_fm["triggers"] = reparsed
            changes.append("healed: triggers (re-parsed from string)")
        else:
            new_fm["triggers"] = None
    # 0e. mcp_integrations: re-parse if string
    if isinstance(new_fm.get("mcp_integrations"), str):
        reparsed = reparse_nested_yaml(new_fm["mcp_integrations"], None)
        if isinstance(reparsed, dict):
            new_fm["mcp_integrations"] = reparsed
            changes.append("healed: mcp_integrations (re-parsed from string)")
        else:
            new_fm["mcp_integrations"] = None
    # 0f. export_destinations: re-parse if string
    if isinstance(new_fm.get("export_destinations"), str):
        reparsed = reparse_nested_yaml(new_fm["export_destinations"], None)
        if reparsed is not None:
            new_fm["export_destinations"] = reparsed
            changes.append("healed: export_destinations (re-parsed from string)")

    # 1. Capture legacy fields before renames
    legacy_export = new_fm.pop("export_destinations", None)
    legacy_mcp_integrations = new_fm.pop("mcp_integrations", None)
    if "run_modes" in new_fm:
        new_fm.pop("run_modes")
        changes.append("dropped: run_modes")
    if legacy_export is not None:
        changes.append("consumed: export_destinations → push_targets")
    if legacy_mcp_integrations is not None:
        changes.append("consumed: mcp_integrations → mcps_used")

    # 2. dependencies → inputs
    if "dependencies" in new_fm:
        deps = new_fm.pop("dependencies")
        new_fm["inputs"] = normalize_inputs(deps)
        changes.append("renamed: dependencies → inputs")
    elif "inputs" not in new_fm:
        new_fm["inputs"] = {"required": [], "recommended": []}
        changes.append("added: inputs")
    else:
        new_fm["inputs"] = normalize_inputs(new_fm["inputs"])

    # 3. ontology_type — keep if present (backfill agent handles missing)
    ontology_type = new_fm.get("ontology_type")

    # 4. Normalize outputs
    new_fm["outputs"] = normalize_outputs(new_fm.get("outputs"), ontology_type)

    # 5. Re-derive depends_on / feeds_into from inputs / outputs
    inputs_required = new_fm["inputs"]["required"]
    if new_fm.get("depends_on") != inputs_required:
        new_fm["depends_on"] = list(inputs_required)
        changes.append("repopulated: depends_on")
    feeds_set = set()
    for o in new_fm["outputs"]:
        for f in o.get("feeds_into", []) or []:
            feeds_set.add(f)
    feeds_list = sorted(feeds_set)
    if new_fm.get("feeds_into") != feeds_list:
        new_fm["feeds_into"] = feeds_list
        changes.append("repopulated: feeds_into")

    # 6. primitive — fix if missing
    if not new_fm.get("primitive"):
        new_fm["primitive"] = derive_primitive_from_path(path)
        changes.append(f"added: primitive={new_fm['primitive']}")

    # 7. owned_by_agent
    if not new_fm.get("owned_by_agent"):
        name = new_fm.get("name") or p.parent.name
        new_fm["owned_by_agent"] = infer_owned_by_agent(name)
        changes.append(f"added: owned_by_agent={new_fm['owned_by_agent']}")

    # 8. mcps_used — scan body
    body_mcps = infer_mcps_used(body)
    # Merge in legacy mcp_integrations keys if present
    if isinstance(legacy_mcp_integrations, dict):
        for k in legacy_mcp_integrations.keys():
            body_mcps.append(k.replace("_", "-"))
    body_mcps = sorted(set(body_mcps))
    if new_fm.get("mcps_used") != body_mcps:
        new_fm["mcps_used"] = body_mcps
        changes.append(f"set: mcps_used={body_mcps}")

    # 9. push_targets
    pt = infer_push_targets(ontology_type, render_map, legacy_export)
    if new_fm.get("push_targets") != pt:
        new_fm["push_targets"] = pt
        changes.append(f"set: push_targets={pt}")

    # 10. triggers
    new_fm["triggers"] = normalize_triggers(new_fm.get("triggers"), new_fm.get("name") or p.parent.name)

    # 11. goal / outcome
    if not new_fm.get("goal"):
        new_fm["goal"] = derive_goal(new_fm.get("description"))
        changes.append("added: goal")
    if not new_fm.get("outcome"):
        new_fm["outcome"] = derive_outcome(new_fm.get("description"))
        changes.append("added: outcome")

    # 12. Lifecycle
    for k, default in [("status", "draft"), ("locked_by", None),
                       ("locked_date", None), ("lock_version", None),
                       ("sources_count", 0)]:
        if k not in new_fm:
            new_fm[k] = default
            changes.append(f"added: {k}")

    # 13. Defaults for required fields
    if "version" not in new_fm:
        new_fm["version"] = "1.0"
        changes.append("added: version")
    elif isinstance(new_fm["version"], (int, float)):
        new_fm["version"] = str(new_fm["version"])
    if "last_updated" not in new_fm:
        new_fm["last_updated"] = "2026-04-30"
        changes.append("added: last_updated")
    if "name" not in new_fm:
        new_fm["name"] = p.parent.name
        changes.append(f"added: name={p.parent.name}")
    if "description" not in new_fm or len(str(new_fm.get("description", ""))) < 80:
        # Keep existing if present even if short; bumping to >=80 chars without context risks fabrication
        if "description" not in new_fm:
            new_fm["description"] = f"Skill {new_fm['name']} produces {ontology_type or 'output'} artifacts. See SKILL.md body for full triggers, inputs, and process."
            changes.append("added: description (placeholder)")

    # 14. Drop any field not in ALLOWED_FIELDS
    dropped = []
    for k in list(new_fm.keys()):
        if k not in ALLOWED_FIELDS:
            dropped.append(k)
            new_fm.pop(k)
    if dropped:
        changes.append(f"dropped: {dropped}")

    # 15. Serialize and write
    new_yaml = serialize_frontmatter(new_fm)
    new_text = f"---\n{new_yaml}---\n\n{body.lstrip(chr(10))}" if body else f"---\n{new_yaml}---\n"
    if not dry_run and new_text != text:
        p.write_text(new_text, encoding="utf-8")
    return ("ok" if changes else "no-op"), changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="SKILL.md paths to migrate")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--report", action="store_true", help="Print full change log per file")
    args = parser.parse_args()

    if not SCHEMA_PATH.exists():
        print(f"ERROR: schema not found at {SCHEMA_PATH}", file=sys.stderr)
        return 2

    render_map = load_template_render_map()

    n_ok, n_noop, n_err = 0, 0, 0
    for path in args.paths:
        status, changes = migrate_one(path, render_map, dry_run=args.dry_run)
        if status == "ok":
            n_ok += 1
            if args.report:
                print(f"\n=== {path} ===")
                for c in changes:
                    print(f"  - {c}")
            else:
                print(f"OK   {path}  ({len(changes)} changes)")
        elif status == "no-op":
            n_noop += 1
            print(f"NOOP {path}")
        else:
            n_err += 1
            print(f"FAIL {path}  status={status}")

    print(f"\n=== Summary: {n_ok} migrated, {n_noop} no-op, {n_err} failed ===")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
