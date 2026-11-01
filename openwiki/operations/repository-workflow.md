---
type: workflow
title: Repository Structure and Work Pipeline
description: How research is added to and found in this repository since the 2026-11-02 restructure. Covers folder rules, note frontmatter, the generated index, decisions.md, scripts/check.py, the nine-step work pipeline, and local-only OpenWiki regeneration.
tags: [workflow, repo-structure, index, lint, decisions, openwiki]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:49:51.673Z
sources:
  - id: openwiki-source-b59005f0f903d10c3bb60923
    resource: repo://decisions.md
  - id: openwiki-source-733117321a85db437c83db32
    resource: repo://notes/09-repo-structure-and-pipeline.md
  - id: openwiki-source-b761b69ee5bd60548cd67eff
    resource: repo://scripts/build_index.py
  - id: openwiki-source-998f86849be36c8415518127
    resource: repo://scripts/check.py
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## Why the layout looks like this

Until 2026-11-02 the notes lived in `agent-expertise-framework/`, split into folders by the four elements of agent expertise. Once the research question moved to multi-agent orchestration and a master agent, new work no longer fit those folders. Folder numbers and document numbers collided in paths, four hand-maintained indexes drifted, and open decisions were scattered across documents. `notes/09-repo-structure-and-pipeline.md` records the diagnosis, the prior art consulted, and the choice. The core rule: folders split only by kind of material, while topic and status live in each document's own frontmatter, and indexes are generated from that frontmatter.

## Folders

| Location | Holds | Rule |
|---|---|---|
| `notes/NN-slug.md` | Everything the project writes: studies, research summaries, designs | Next number is the highest + 1. Numbers are permanent IDs and never renumbered, because notes cite each other as "(10 A-2)" |
| `sources/<topic>/` | One note per external item (KakaoPay posts, master orchestrator surveys, superpowers history) | Written once, not edited afterwards. A note in `notes/` acts as the table of contents |
| `experiments/<name>/` | Runnable code, currently the eval harness | README per folder |
| `notes/diagrams/<name>/` | Diagram HTML source, rendered PNG, `render.sh` | |
| `openwiki/` | This wiki | Generated only |

Only two lists are maintained by hand: `decisions.md` for direction-level decisions and `JOURNEY.md` for the dated narrative. Everything else that lists documents is generated.

## Note frontmatter

Every `notes/` document starts with YAML frontmatter: `status` (DRAFT, ACTIVE, PLANNED, DEPRECATED), `layer` (1 original, 2 design, 3 implementation, 4 generated), optional `layer_note`, `topic` (a list), `date`, and a one-line `summary`. The allowed topics and statuses are defined in exactly one place, `TOPICS` and `STATUSES` in `scripts/build_index.py`. Adding a topic means adding a line there.

## Generated index

`scripts/build_index.py` rewrites only the block between `<!-- index:start -->` and `<!-- index:end -->` in `index.md`. It produces:

- a table per topic from note frontmatter (a note with two topics appears under both)
- a table of `sources/` folders with file counts and the notes that link into each folder
- the `experiments/` folders with their README titles
- a "next steps" list: the number of `open` rows in `decisions.md`, plus every note that has an "open questions" heading, with a count of its remaining bullets (struck-through bullets count as done)

Run with `--check` to exit non-zero when the index is stale.

## decisions.md

One table each for open and decided items, with columns ID, status, question, decision, date, and source. IDs are never reused. A decided row keeps its place and changes status. A reversed decision becomes `superseded` and gets a new row. Research questions that belong to one document stay in that document's "open questions" section and reach the index automatically.

## scripts/check.py

The repo lint, meant to run before every commit:

1. Frontmatter: required fields, allowed values, unique numbers.
2. Relative links resolve, for every Markdown file outside `openwiki/` and virtualenvs. Links inside code are skipped.
3. `index.md` matches what `build_index.py` would generate.
4. For lines added since HEAD (the staged diff when anything is staged), no middle dots, no semicolons outside code, and none of the banned words listed in the user's global `~/.claude/CLAUDE.md`. Code fences and inline code are exempt. Older untouched lines are not checked, so existing text does not block unrelated commits.

`.claude/hooks/check-before-commit.py` runs `check.py` when a Bash command contains `git commit` and denies the call with the problem list if it fails. As of the restructure it is not yet registered in `.claude/settings.json`, because a user-level hook blocks edits to settings files without the user's explicit go-ahead. Until then `check.py` is run by hand. See [Hook Enforcement](../orchestration/hook-enforcement.md).

## The work pipeline

1. **Register the question.** A direction-level decision gets an `open` row in `decisions.md`. A question inside one document goes in that document's open questions section.
2. **Research.** The researcher agent. Per-item source notes go to `sources/<topic>/`.
3. **Verify.** Claims headed for a document, especially "does not exist" conclusions, top picks, and numbers, are re-checked by the verifier agent.
4. **Write up.** `notes/NN-slug.md` with frontmatter.
5. **Close out.** Update the `decisions.md` row. Append to JOURNEY when a large stage ends.
6. **Index and check.** `build_index.py`, then `check.py`.
7. **Commit locally.**
8. **Regenerate the wiki** when needed, in a local Claude session through the OpenWiki skill. There is no CI schedule and no model API key (`decisions.md` D16). The scheduled workflow installed with OpenWiki in August failed on every run for lack of a key and was removed.
9. **Push** only after separate confirmation.

## Related pages

- [Agent Implementation Schema](../frameworks/agent-implementation-schema.md): the schema this layout instantiates
- [Hook Enforcement](../orchestration/hook-enforcement.md): the generated-edit block and the pre-commit check
- [Repository Overview](../overview.md)
