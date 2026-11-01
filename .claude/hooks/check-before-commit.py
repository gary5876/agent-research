#!/usr/bin/env python3
"""PreToolUse hook (Bash): run scripts/check.py before any `git commit` and block on failure.

Pipeline step 7 in notes/09-repo-structure-and-pipeline.md. Turns "run check.py
before committing" from a prompt rule into a structural gate, per
notes/07-harness-and-hook-enforcement.md.
"""
import json
import os
import re
import subprocess
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    command = (data.get("tool_input", {}) or {}).get("command", "") or ""
    if not re.search(r"\bgit\b(\s+-C\s+\S+)?(\s+-c\s+\S+)*\s+commit\b", command):
        return 0

    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result = subprocess.run([sys.executable, os.path.join(root, "scripts", "check.py")],
                            capture_output=True, text=True, cwd=root)
    if result.returncode == 0:
        return 0
    reason = ("Blocked: scripts/check.py failed, fix these before committing "
              "(notes/09-repo-structure-and-pipeline.md step 6):\n" + result.stdout + result.stderr)
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
