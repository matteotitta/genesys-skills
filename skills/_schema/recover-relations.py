#!/usr/bin/env python3
"""Recover dependencies + outputs[].feeds_into from pre-Phase-4 git history.

After Phase 4 migration, depends_on / feeds_into / inputs.recommended turned
out empty for ~50 skills because the legacy YAML literal-blocks had inconsistent
indentation that defeated yaml.safe_load. This script:

1. For each active SKILL.md, fetch the pre-Phase-4 version from git (HEAD~3)
2. Run the regex extractors on the legacy `dependencies` and `outputs` fields
3. Patch the CURRENT migrated file's inputs.recommended, depends_on, feeds_into,
   and outputs[].feeds_into with the recovered data

Idempotent. No-op if the current file already has populated relations.
"""
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml", file=sys.stderr); sys.exit(2)

# Re-implement the regex extractors here for self-containedness
def regex_extract_outputs(value):
    if not isinstance(value, str):
        return None
    out = []
    blocks = re.split(r"(?=^\s*-\s*type:)", value, flags=re.MULTILINE)
    for block in blocks:
        type_m = re.search(r"-\s*type:\s*([\w-]+)", block)
        if not type_m:
            continue
        type_val = type_m.group(1)
        feeds = re.findall(r"^\s*-\s*([\w-]+)\s*$", block, flags=re.MULTILINE)
        feeds = [f for f in feeds if f != type_val]
        out.append({"type": type_val, "feeds_into": feeds})
    return out if out else None


def regex_extract_dependencies(value):
    if not isinstance(value, str):
        return None
    result = {"required": [], "recommended": []}
    for key in ("required", "recommended"):
        m = re.search(rf"{key}:\s*\[([^\]]*)\]", value)
        if m:
            items = [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]
            result[key] = items
            continue
        m = re.search(rf"{key}:\s*$", value, flags=re.MULTILINE)
        if m:
            tail = value[m.end():]
            items = []
            for ln in tail.splitlines():
                bm = re.match(r"^\s*-\s*([\w-]+)\s*$", ln)
                if bm:
                    items.append(bm.group(1))
                elif ln.strip() and not ln.strip().startswith("-"):
                    break
            result[key] = items
    return result


def parse_legacy_fm(text):
    """Parse a legacy SKILL.md frontmatter into a {key: raw_string} map.
    Doesn't try to YAML-parse — just splits on top-level keys.
    """
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    raw = m.group(1)
    fields = {}
    # Find every top-level `^key:` and capture content until next top-level key
    pattern = re.compile(r"^([\w-]+):\s*(.*?)(?=\n[\w-]+:|\Z)", re.MULTILINE | re.DOTALL)
    for match in pattern.finditer(raw):
        key = match.group(1)
        val = match.group(2).strip()
        fields[key] = val
    return fields


def parse_current_fm(text):
    """Parse current well-formed YAML frontmatter."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}, "", ""
    return yaml.safe_load(m.group(1)) or {}, m.group(1), text[m.end():]


def get_legacy(path, ref="HEAD~3"):
    """Fetch the pre-Phase-4 version of a file from git."""
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return r.stdout


def serialize_fm(fm):
    order = [
        "name", "version", "last_updated", "author",
        "description", "goal", "outcome",
        "primitive", "sub_primitive", "ontology_type", "review_gate",
        "inputs", "outputs", "depends_on", "feeds_into",
        "owned_by_agent", "mcps_used", "push_targets", "triggers",
        "status", "locked_by", "locked_date", "lock_version", "sources_count",
        "context", "effort", "paths", "disable-model-invocation",
    ]
    ordered = {k: fm[k] for k in order if k in fm}
    for k in fm:
        if k not in ordered:
            ordered[k] = fm[k]
    return yaml.safe_dump(ordered, sort_keys=False, default_flow_style=False,
                         allow_unicode=True, width=120)


def recover_one(path):
    p = Path(path)
    legacy = get_legacy(path)
    if not legacy:
        return f"NO_LEGACY {path}"
    legacy_fields = parse_legacy_fm(legacy)
    current_text = p.read_text(encoding="utf-8")
    current_fm, _, body = parse_current_fm(current_text)
    if not current_fm:
        return f"NO_CURRENT {path}"

    changes = []

    # Recover dependencies
    dep_raw = legacy_fields.get("dependencies")
    if dep_raw:
        deps = regex_extract_dependencies(dep_raw)
        if deps:
            req = deps.get("required") or []
            rec = deps.get("recommended") or []
            cur_inputs = current_fm.get("inputs") or {"required": [], "recommended": []}
            if req and not cur_inputs.get("required"):
                cur_inputs["required"] = req
                current_fm["depends_on"] = list(req)
                changes.append(f"+inputs.required={req}")
            if rec and not cur_inputs.get("recommended"):
                cur_inputs["recommended"] = rec
                changes.append(f"+inputs.recommended={rec}")
            current_fm["inputs"] = cur_inputs

    # Recover outputs feeds_into
    out_raw = legacy_fields.get("outputs")
    if out_raw:
        outputs = regex_extract_outputs(out_raw)
        if outputs:
            # Merge feeds_into into current outputs (matched by type, or by index)
            cur_outputs = current_fm.get("outputs") or []
            # Build feeds_into union per type
            feeds_by_type = {o["type"]: o["feeds_into"] for o in outputs}
            merged_feeds = set()
            for o in outputs:
                merged_feeds.update(o.get("feeds_into", []))
            # Replace current outputs with recovered ones (preserves type variety)
            if outputs and not any(co.get("feeds_into") for co in cur_outputs):
                current_fm["outputs"] = outputs
                changes.append(f"+outputs={len(outputs)} types, {len(merged_feeds)} downstream feeds")
            # Update top-level feeds_into mirror
            if merged_feeds:
                merged_list = sorted(merged_feeds)
                if current_fm.get("feeds_into") != merged_list:
                    current_fm["feeds_into"] = merged_list
                    changes.append(f"+feeds_into={len(merged_list)}")

    if not changes:
        return f"NOOP {path}"

    new_yaml = serialize_fm(current_fm)
    new_text = f"---\n{new_yaml}---\n\n{body.lstrip(chr(10))}" if body else f"---\n{new_yaml}---\n"
    p.write_text(new_text, encoding="utf-8")
    return f"OK   {path}  {' '.join(changes)}"


def main():
    paths = sys.argv[1:]
    if not paths:
        # Default: all active skills
        EXCL = {"_archive", "_flagged", "_schema", "_evals", "_scripts"}
        paths = []
        for p in sorted(Path(".claude/skills").rglob("SKILL.md")):
            if any(x in EXCL for x in p.parts):
                continue
            paths.append(str(p))

    n_ok = n_noop = n_miss = 0
    for path in paths:
        result = recover_one(path)
        print(result)
        if result.startswith("OK"):
            n_ok += 1
        elif result.startswith("NOOP"):
            n_noop += 1
        else:
            n_miss += 1
    print(f"\n=== Recovered: {n_ok}, NoOp: {n_noop}, Missing: {n_miss} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
