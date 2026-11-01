#!/usr/bin/env python3
"""Regenerate the generated block of index.md from the repo's own files.

Sources of truth (nothing here is typed by hand):
- notes/*.md frontmatter (status, layer, topic, summary)
- notes/*.md headings named "열린 질문" (open research questions)
- sources/<folder>/ file counts, and which notes link into each folder
- decisions.md rows whose status is "open"
- experiments/<folder>/README.md first heading

Usage (from anywhere inside the repo):
  python3 scripts/build_index.py          # rewrite index.md
  python3 scripts/build_index.py --check  # exit 1 if index.md is stale
"""
import os
import re
import subprocess
import sys

# Topic vocabulary. The only place topics are defined. Adding a topic means adding a line here.
TOPICS = {
    "expert-agent": "에이전트 하나의 전문성 (4요소와 구현 일반형)",
    "instruction": "사람의 말을 실행 지시로 바꾸는 층",
    "self-improvement": "평가와 자체개선 루프",
    "orchestration": "여러 에이전트 조율의 근거와 판단",
    "master": "마스터 에이전트 (자비스형)",
    "baseline": "카카오페이 바닥선",
    "repo-ops": "이 저장소 운영 (구조, 파이프라인)",
}
STATUSES = {"DRAFT", "ACTIVE", "PLANNED", "DEPRECATED"}
START, END = "<!-- index:start -->", "<!-- index:end -->"


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return subprocess.run(["git", "-C", here, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True, check=True).stdout.strip()


def parse_frontmatter(text):
    """Minimal YAML subset parser: key: value, key: [a, b], quoted strings."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    meta = {}
    for line in text[4:end].split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            meta[key.strip()] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
        else:
            meta[key.strip()] = val.strip('"')
    return meta


def load_notes(root):
    notes = []
    ndir = os.path.join(root, "notes")
    for name in sorted(os.listdir(ndir)):
        if not re.match(r"^\d{2}-.+\.md$", name):
            continue
        text = open(os.path.join(ndir, name), encoding="utf-8").read()
        notes.append({"file": name, "num": name[:2], "meta": parse_frontmatter(text) or {}, "text": text})
    return notes


def open_questions(text):
    """Count top-level bullets under a heading containing '열린 질문' or '열려 있는 질문'. Strikethrough bullets are done."""
    m = re.search(r"^(#{2,3}) [^\n]*(열린 질문|열려 있는 질문)[^\n]*$", text, re.M)
    if not m:
        return 0
    level = len(m.group(1))
    count = 0
    for line in text[m.end():].split("\n"):
        h = re.match(r"^(#{1,6}) ", line)
        if h and len(h.group(1)) <= level:
            break
        if line.startswith("- ") and not line.startswith("- ~~"):
            count += 1
    return count


def render(root):
    notes = load_notes(root)
    out = [START, "", "이 블록은 `python3 scripts/build_index.py`가 만든다. 손으로 고치지 않는다.", ""]

    out += ["## 주제별 문서", ""]
    for topic, desc in TOPICS.items():
        rows = [n for n in notes if topic in n["meta"].get("topic", [])]
        if not rows:
            continue
        out += [f"### {topic}: {desc}", "", "| 문서 | 상태 | 층 | 요약 |", "|---|---|---|---|"]
        for n in rows:
            m = n["meta"]
            out.append(f"| [{n['file']}](notes/{n['file']}) | {m.get('status', '?')} | {m.get('layer', '?')} | {m.get('summary', '')} |")
        out.append("")

    out += ["## 원문 자료 (sources/)", "", "고치지 않는 외부 자료 노트. 목차 문서는 그 폴더를 링크하는 notes 문서다.", "",
            "| 폴더 | 파일 수 | 목차 문서 |", "|---|---|---|"]
    sdir = os.path.join(root, "sources")
    for folder in sorted(os.listdir(sdir)):
        fpath = os.path.join(sdir, folder)
        if not os.path.isdir(fpath):
            continue
        count = len([f for f in os.listdir(fpath) if f.endswith(".md")])
        refs = [n for n in notes if f"../sources/{folder}/" in n["text"]]
        ref_links = ", ".join(f"[{n['num']}](notes/{n['file']})" for n in refs) or "없음"
        out.append(f"| [sources/{folder}/](sources/{folder}/) | {count} | {ref_links} |")
    out.append("")

    out += ["## 실험 (experiments/)", ""]
    edir = os.path.join(root, "experiments")
    for folder in sorted(os.listdir(edir)):
        readme = os.path.join(edir, folder, "README.md")
        if os.path.isfile(readme):
            title = next((l[2:].strip() for l in open(readme, encoding="utf-8") if l.startswith("# ")), folder)
            out.append(f"- [experiments/{folder}/](experiments/{folder}/): {title}")
    out.append("")

    open_rows = 0
    dpath = os.path.join(root, "decisions.md")
    if os.path.isfile(dpath):
        open_rows = sum(1 for l in open(dpath, encoding="utf-8") if re.match(r"^\| D\d+ \| open \|", l))
    out += ["## 다음에 할 일", "",
            f"- 열린 결정 {open_rows}개: [decisions.md](decisions.md)",
            "- 열린 질문이 남은 문서 (문서 안의 \"열린 질문\" 절, 숫자는 남은 항목 수):", ""]
    for n in notes:
        q = open_questions(n["text"])
        if q:
            out.append(f"  - [{n['file']}](notes/{n['file']}): {q}개")
    out += ["", END]
    return "\n".join(out)


def splice(current, block):
    if START not in current or END not in current:
        raise SystemExit(f"index.md is missing {START} / {END} markers")
    head = current.split(START)[0]
    tail = current.split(END, 1)[1]
    return head + block + tail


def main():
    root = repo_root()
    path = os.path.join(root, "index.md")
    current = open(path, encoding="utf-8").read()
    new = splice(current, render(root))
    if "--check" in sys.argv:
        if new != current:
            print("index.md is stale. Run: python3 scripts/build_index.py")
            return 1
        return 0
    if new != current:
        open(path, "w", encoding="utf-8").write(new)
        print("index.md updated")
    else:
        print("index.md already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
