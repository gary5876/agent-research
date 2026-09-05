---
type: overview
title: Repository Overview
description: What this repository is and how it is organized — a personal research-notes collection tracing one session's inquiry from "how to write LLM-friendly documentation" to "where does agent expertise come from," now organized as a folder tree rooted by a general implementation schema, plus the OpenWiki tooling wired into the repo.
tags: [overview, research-notes, agent-expertise, openwiki]
verified:
  - by: openwiki/0.4.3
    at: 2026-09-05T20:17:03.290Z
sources:
  - id: openwiki-source-f5a489e5822d87c0b8fc66ef
    resource: repo://.mcp.json
generated: { by: "claude-code", at: "2026-09-05T20:17:03.290Z" }
---

## What this repository is

This repository is not a software project. It holds research notes from a single working session, rooted in the `agent-expertise-framework/` directory, that trace a chain of inquiry starting from "how should documentation be written for an LLM to read well" and arriving at "where does an agent's domain expertise actually come from."

## Structure

### `agent-expertise-framework/` is a tree, not a flat list

The directory is described in its own [README](../agent-expertise-framework/README.md) as a physical implementation of its own conclusions: a root document, `08-agent-implementation-schema.md`, synthesizes the research into a domain-agnostic four-factor schema, and four subfolders each implement one factor:

| Folder | Factor | Notes | Wiki page |
|---|---|---|---|
| `00-data-lake/` | Coherent data lake | `00-llm-friendly-docs-framework.md` (the session's starting 12-principle framework) and `01-research-summary.md` (validating it against three cloned OSS projects, revising the hypothesis into the four-factor model) | [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md), [Validating the Framework](frameworks/framework-validation-research.md) |
| `01-narrow-interface/` | Narrow, explicit interface | `02-instruction-clarity-incident.md` (a recorded failure case) and `03-instruction-resolution-gate.md` (the interpretation-layer design built from it) | [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md), [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md) |
| `02-self-improvement-loop/` | Safe response filter | `04-purpose-and-self-improvement-loop.md`, `05-pipeline-options-and-plan.md`, and an `eval/` harness with a working grounding metric and PII filter | not yet a dedicated wiki page |
| `03-orchestration-and-enforcement/` | Failure-derived prohibition rules | `06-orchestrator-pattern.md` and `07-harness-and-hook-enforcement.md` (a Hook that structurally enforces a rule the prompt alone couldn't) | not yet a dedicated wiki page |

This wiki currently documents only the `00-data-lake/` and `01-narrow-interface/` material (four pages); `02-self-improvement-loop/`, `03-orchestration-and-enforcement/`, and the root schema document are not yet covered by dedicated pages.

The `agent-expertise-framework/README.md` also points to three sibling analysis directories one level up in the same workspace but **outside this repository** (`../../data-lake/amoro-analysis`, `../../data-lake/iceberg-analysis`, `../../data-lake/paimon-analysis`) that were cloned and analyzed as part of the same research pass. Those directories are referenced as external context throughout `00-data-lake/01-research-summary.md` but are not part of this repository, so this wiki does not document their internal content directly — see [Validating the Framework](frameworks/framework-validation-research.md) for what each contributed.

### Root-level files

- `CLAUDE.md` is an agent-facing instruction file containing only an OpenWiki-managed block pointing readers to this generated wiki as optional just-in-time context, and instructing that generated OpenWiki pages should not be hand-edited.
- `AGENTS.md` contains that same OpenWiki-managed block, plus a separate "문서 정리 컨벤션" (documentation convention) section: new research documents must carry `Status`/`Layer` header tags as their single source of truth for classification, get indexed in their folder's README, and local edits are treated as a separate request from `git push` (push only after the diff is shown and confirmed).
- `CATALOG.md` is a short, manually-maintained pointer file: for markdown research documents it says to check each document's own header tag directly (`grep`) rather than trusting a re-copied summary, and it lists the handful of non-markdown resources (`eval/`, `.claude/agents/`, `.claude/hooks/`, `openwiki/`, `README.md`) that cannot carry such a tag themselves.
- `.mcp.json` registers the `openwiki` MCP server (invoked as `openwiki mcp --host claude`), which is what an interactive Claude Code session uses to run the page-job lifecycle that produced this wiki.
- `.github/workflows/openwiki-update.yml` defines a scheduled GitHub Actions workflow (daily cron plus manual dispatch) that runs `openwiki code --update` in CI using an OpenAI-backed provider, and opens a pull request with any resulting changes to `openwiki/`, `AGENTS.md`, `CLAUDE.md`, and the workflow file itself.

## Why this repository has an OpenWiki setup

This is a research-notes repository rather than an application, so there is no runtime, build, or API surface to document in the traditional sense. The OpenWiki instance here instead documents the *content* of the research: the framework, its validation, the incident that prompted a design response, and that design itself.

## Related pages

- [Quickstart](quickstart.md) — where to start reading depending on what you want to know
- [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md)
- [Validating the Framework: Where Agent Expertise Comes From](frameworks/framework-validation-research.md)
- [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md)
- [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md)
