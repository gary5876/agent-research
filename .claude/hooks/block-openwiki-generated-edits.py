#!/usr/bin/env python3
"""PreToolUse hook: block Edit/Write/NotebookEdit on OpenWiki-generated content.

Converts the prompt-only rule in notes/04-purpose-and-self-improvement-loop.md §5 ("Never hand-edit openwiki/*.md or
openwiki/.claims/*.json") into a deterministic Hook, per
notes/07-harness-and-hook-enforcement.md.
"""
import json
import re
import sys

GENERATED_PATTERNS = [
    r"(^|/)openwiki/\.claims/",
    r"(^|/)openwiki/.*\.md$",
]


def is_assigned_page(file_path: str) -> bool:
    """Allow the one exception the rule intends: OpenWiki's own page loop.

    During a local OpenWiki run the host must write each assigned page itself.
    Allowed only when openwiki/.run.json is in the generating phase and the file
    is a planned page whose job is still pending. Claims sidecars, indexes, and
    any page outside the plan stay blocked.
    """
    match = re.search(r"(^|/)(openwiki/[^.][^/]*(?:/[^/]+)*\.md)$", file_path)
    if not match or "/.claims/" in file_path:
        return False
    try:
        with open("openwiki/.run.json", encoding="utf-8") as f:
            run = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False
    if run.get("phase") != "generating":
        return False
    wiki_path = "/" + match.group(2)
    return any(p.get("path") == wiki_path and p.get("status") == "pending"
               for p in (run.get("plan") or {}).get("pages", []))


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = data.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""

    if any(re.search(p, file_path) for p in GENERATED_PATTERNS) and not is_assigned_page(file_path):
        reason = (
            f"Blocked: '{file_path}' is OpenWiki-generated content. "
            "Never hand-edit openwiki/*.md or openwiki/.claims/*.json "
            "(notes/04-purpose-and-self-improvement-loop.md §5). "
            "Edit the source doc in notes/ instead and regenerate OpenWiki locally."
        )
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
