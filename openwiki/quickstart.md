---
type: quickstart
title: Quickstart
description: Task-routing map for this repository — what it is, how the research notes are organized as a folder tree, and which wiki page answers which kind of question.
tags: [quickstart, research-notes, navigation]
verified:
  - by: openwiki/0.4.3
    at: 2026-09-05T20:17:03.290Z
sources:
  - id: openwiki-source-887cac2f19ff496dc6e7029e
    resource: repo://agent-expertise-framework/README.md
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-a2371d6362e5db4bc834ad03
    resource: repo://CLAUDE.md
generated: { by: "claude-code", at: "2026-09-05T20:17:03.290Z" }
---

## What this repository is

A personal research-notes repository, not a software project. There is no build, no runtime, and no API. Everything here is prose documenting one working session's line of inquiry, rooted in `agent-expertise-framework/`, which is organized as a tree (four subfolders, one per research factor, under a root synthesis document). See [Repository Overview](overview.md) for the full structure.

## Where to start depending on your question

| If you want to know... | Read this |
|---|---|
| How should I write documentation so an LLM/agent reads it without hallucinating? | [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md) |
| Was that documentation framework actually tested against real code, and what changed after testing it? | [Validating the Framework: Where Agent Expertise Comes From](frameworks/framework-validation-research.md) |
| What went wrong in a real case where an agent asked an unnecessary clarifying question? | [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md) |
| How should a system be designed so an agent doesn't repeat that kind of mistake? | [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md) |
| How does a self-improvement loop, a multi-agent orchestrator pattern, or Hook-based enforcement fit in? | Not yet a dedicated wiki page — read `agent-expertise-framework/02-self-improvement-loop/` and `agent-expertise-framework/03-orchestration-and-enforcement/` directly in the repository |
| What's the general, domain-agnostic version of "what makes an agent expert"? | Not yet a dedicated wiki page — read `agent-expertise-framework/08-agent-implementation-schema.md` directly in the repository |
| What's in this repo overall, and how does the OpenWiki tooling here work? | [Repository Overview](overview.md) |

## Suggested reading order

The material in `agent-expertise-framework/` is organized into four numbered subfolders, each covering one factor of the four-factor model, plus a root document synthesizing all of them. This wiki currently documents only the first two subfolders' material:

1. [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md) — the starting methodology (`00-data-lake/`)
2. [Validating the Framework: Where Agent Expertise Comes From](frameworks/framework-validation-research.md) — testing it against real projects, revising the hypothesis (`00-data-lake/`)
3. [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md) — the reverse problem, told through a real failure (`01-narrow-interface/`)
4. [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md) — a design response built from that failure (`01-narrow-interface/`)

If you already know the framework and its validation, pages 3 and 4 stand on their own as a separate thread about instruction clarity rather than documentation clarity. Beyond this wiki, `02-self-improvement-loop/`, `03-orchestration-and-enforcement/`, and the root `08-agent-implementation-schema.md` continue the same inquiry but are not yet summarized as wiki pages — read them directly in the repository.

## Note on agent-facing files

`CLAUDE.md` at the repository root contains only an OpenWiki-managed block pointing back to this generated wiki as optional context and stating that generated OpenWiki pages should not be hand-edited. `AGENTS.md` contains that same block plus a documentation convention section: new research documents must carry `Status`/`Layer` header tags as their single source of truth, get indexed in their folder's README, and treat local edits as a request separate from `git push`.

## Related pages

- [Repository Overview](overview.md)
