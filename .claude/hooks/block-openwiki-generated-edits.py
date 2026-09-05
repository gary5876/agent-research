#!/usr/bin/env python3
"""PreToolUse hook: block Edit/Write/NotebookEdit on OpenWiki-generated content.

Converts the prompt-only rule in agent-expertise-framework/04-purpose-and-
self-improvement-loop.md §5 ("Never hand-edit openwiki/*.md or
openwiki/.claims/*.json") into a deterministic Hook, per
agent-expertise-framework/07-harness-and-hook-enforcement.md.
"""
import json
import re
import sys

GENERATED_PATTERNS = [
    r"(^|/)openwiki/\.claims/",
    r"(^|/)openwiki/.*\.md$",
]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = data.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""

    if any(re.search(p, file_path) for p in GENERATED_PATTERNS):
        reason = (
            f"Blocked: '{file_path}' is OpenWiki-generated content. "
            "Never hand-edit openwiki/*.md or openwiki/.claims/*.json "
            "(agent-expertise-framework/04-purpose-and-self-improvement-loop.md §5). "
            "Edit the source doc in agent-expertise-framework/ instead and let OpenWiki regenerate."
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
