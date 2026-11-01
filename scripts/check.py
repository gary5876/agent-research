#!/usr/bin/env python3
"""Repo lint. Run before every commit (the Claude Code commit Hook runs it for you).

Checks:
1. notes/*.md frontmatter: required fields and allowed values, unique numbers.
2. Relative markdown links resolve (all .md outside openwiki/ and virtualenvs).
3. index.md is up to date with scripts/build_index.py.
4. Lines added since HEAD (staged if anything is staged, else working tree) in .md files:
   no middle dots, no semicolons outside code, no banned words. Code fences and
   inline code are exempt. Untouched old lines are not checked.

Exit 0 when clean, 1 with a list of problems otherwise.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_index  # noqa: E402

MIDDOTS = [chr(c) for c in (0xB7, 0x318D, 0x2022, 0x2219, 0x30FB)]
WORDS_FILE = os.path.expanduser("~/.claude/CLAUDE.md")
SKIP_DIRS = ("openwiki/", ".git/", ".venv/", ".pytest_cache/", "node_modules/")
BT = chr(96)


def banned_words():
    """Read the banned-word list from the user's global CLAUDE.md ('- 단어: X' lines)."""
    if not os.path.isfile(WORDS_FILE):
        return []
    return re.findall(r"^- 단어: (\S+)\s*$", open(WORDS_FILE, encoding="utf-8").read(), re.M)


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True).stdout


def check_frontmatter(root, problems):
    seen = {}
    for n in build_index.load_notes(root):
        f, m = n["file"], n["meta"]
        if not m:
            problems.append(f"notes/{f}: missing YAML frontmatter")
            continue
        if n["num"] in seen:
            problems.append(f"notes/{f}: number {n['num']} already used by {seen[n['num']]}")
        seen[n["num"]] = f
        if m.get("status") not in build_index.STATUSES:
            problems.append(f"notes/{f}: status must be one of {sorted(build_index.STATUSES)}")
        if m.get("layer") not in {"1", "2", "3", "4"}:
            problems.append(f"notes/{f}: layer must be 1, 2, 3, or 4")
        topics = m.get("topic")
        if not isinstance(topics, list) or not topics:
            problems.append(f"notes/{f}: topic must be a non-empty list like [orchestration]")
        else:
            for t in topics:
                if t not in build_index.TOPICS:
                    problems.append(f"notes/{f}: unknown topic '{t}' (add it to TOPICS in scripts/build_index.py first)")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", m.get("date", "")):
            problems.append(f"notes/{f}: date must be YYYY-MM-DD")
        if not m.get("summary"):
            problems.append(f"notes/{f}: summary is empty")


LINK = re.compile(r"\]\(([^)\s]+)\)")


def check_links(root, problems):
    for dp, _, files in os.walk(root):
        rel_dp = os.path.relpath(dp, root) + "/"
        if any(s in rel_dp for s in SKIP_DIRS):
            continue
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dp, name)
            in_fence = False
            for i, line in enumerate(open(path, encoding="utf-8"), 1):
                if line.lstrip().startswith(BT * 3):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                for target in LINK.findall(re.sub(BT + "[^" + BT + "]*" + BT, "", line)):
                    if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                        continue
                    tpath = target.split("#")[0]
                    if not os.path.exists(os.path.normpath(os.path.join(dp, tpath))):
                        problems.append(f"{os.path.relpath(path, root)}:{i}: broken link {target}")


def check_index(root, problems):
    current = open(os.path.join(root, "index.md"), encoding="utf-8").read()
    if build_index.splice(current, build_index.render(root)) != current:
        problems.append("index.md is stale. Run: python3 scripts/build_index.py")


def added_lines(root):
    """Yield (path, line_no) for lines added vs HEAD in .md files. Staged diff if anything is staged."""
    staged = bool(git(root, "diff", "--cached", "--name-only").strip())
    diff = git(root, "diff", "--cached" if staged else "HEAD", "-U0", "--", "*.md")
    path = None
    for line in diff.split("\n"):
        if line.startswith("+++ "):
            p = line[4:]
            path = p[2:] if p.startswith("b/") else None
            if path and path.startswith(SKIP_DIRS):
                path = None
        elif line.startswith("@@") and path:
            m = re.search(r"\+(\d+)(?:,(\d+))?", line)
            start, count = int(m.group(1)), int(m.group(2) or 1)
            for n in range(start, start + count):
                yield path, n, staged


def check_added_text(root, problems):
    words = banned_words()
    cache = {}
    for path, n, staged in added_lines(root):
        if path not in cache:
            text = git(root, "show", f":{path}") if staged else open(os.path.join(root, path), encoding="utf-8").read()
            lines = text.split("\n")
            fence, flags = False, []
            for l in lines:
                if l.lstrip().startswith(BT * 3):
                    fence = not fence
                    flags.append(True)
                else:
                    flags.append(fence)
            cache[path] = (lines, flags)
        lines, flags = cache[path]
        if n - 1 >= len(lines) or flags[n - 1]:
            continue
        line = re.sub(BT + "[^" + BT + "]*" + BT, "", lines[n - 1])
        if any(c in line for c in MIDDOTS):
            problems.append(f"{path}:{n}: middle dot")
        if ";" in re.sub(r"&#?\w+;", "", line):
            problems.append(f"{path}:{n}: semicolon")
        for w in words:
            if w in line:
                problems.append(f"{path}:{n}: banned word '{w}'")


def main():
    root = build_index.repo_root()
    problems = []
    check_frontmatter(root, problems)
    check_links(root, problems)
    check_index(root, problems)
    check_added_text(root, problems)
    if problems:
        print("check.py found problems:")
        for p in problems:
            print("  " + p)
        return 1
    print("check.py: all clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
