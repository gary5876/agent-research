---
type: quickstart
title: Quickstart
description: Task-routing map for this repository — what it is, how the research notes are organized, and which wiki page answers which kind of question.
tags: [quickstart, research-notes, navigation]
verified:
  - by: openwiki/0.4.3
    at: 2026-08-30T15:41:00.038Z
sources:
  - id: openwiki-source-887cac2f19ff496dc6e7029e
    resource: repo://agent-expertise-framework/README.md
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-a2371d6362e5db4bc834ad03
    resource: repo://CLAUDE.md
generated: { by: "claude-code", at: "2026-08-30T15:41:00.038Z" }
---

## What this repository is

A personal research-notes repository, not a software project. There is no build, no runtime, and no API. Everything here is prose documenting one working session's line of inquiry, rooted in `agent-expertise-framework/`. See [Repository Overview](overview.md) for the full structure.

## Where to start depending on your question

| If you want to know... | Read this |
|---|---|
| How should I write documentation so an LLM/agent reads it without hallucinating? | [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md) |
| Was that documentation framework actually tested against real code, and what changed after testing it? | [Validating the Framework: Where Agent Expertise Comes From](frameworks/framework-validation-research.md) |
| What went wrong in a real case where an agent asked an unnecessary clarifying question? | [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md) |
| How should a system be designed so an agent doesn't repeat that kind of mistake? | [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md) |
| What's in this repo overall, and how does the OpenWiki tooling here work? | [Repository Overview](overview.md) |

## Suggested reading order

The source material in `agent-expertise-framework/` is numbered `00` through `03` and is meant to be read in that order — each page continues from the previous one:

1. [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md) — the starting methodology
2. [Validating the Framework: Where Agent Expertise Comes From](frameworks/framework-validation-research.md) — testing it against real projects, revising the hypothesis
3. [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md) — the reverse problem, told through a real failure
4. [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md) — a design response built from that failure

If you already know the framework and its validation, pages 3 and 4 stand on their own as a separate thread about instruction clarity rather than documentation clarity.

## Note on agent-facing files

`AGENTS.md` and `CLAUDE.md` at the repository root each contain only an OpenWiki-managed block. They point back to this generated wiki as optional context and state that generated OpenWiki pages should not be hand-edited — update the source notes in `agent-expertise-framework/` instead and let the wiki regenerate.

## Related pages

- [Repository Overview](overview.md)
