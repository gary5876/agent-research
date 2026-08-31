---
type: overview
title: Repository Overview
description: What this repository is and how it is organized — a personal research-notes collection tracing one session's inquiry from "how to write LLM-friendly documentation" to "where does agent expertise come from," plus the OpenWiki tooling wired into the repo.
tags: [overview, research-notes, agent-expertise, openwiki]
verified:
  - by: openwiki/0.4.3
    at: 2026-08-30T15:41:00.038Z
sources:
  - id: openwiki-source-6d4b4e707b8d60b6ccfa3425
    resource: repo://.github/workflows/openwiki-update.yml
  - id: openwiki-source-f5a489e5822d87c0b8fc66ef
    resource: repo://.mcp.json
  - id: openwiki-source-887cac2f19ff496dc6e7029e
    resource: repo://agent-expertise-framework/README.md
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-a2371d6362e5db4bc834ad03
    resource: repo://CLAUDE.md
generated: { by: "claude-code", at: "2026-08-30T15:41:00.038Z" }
---

## What this repository is

This repository is not a software project. It holds research notes from a single working session, rooted in the `agent-expertise-framework/` directory, that trace a chain of inquiry starting from "how should documentation be written for an LLM to read well" and arriving at "where does an agent's domain expertise actually come from."

## Structure

### `agent-expertise-framework/`

The root directory for the session's material, described in its own [README](../agent-expertise-framework/README.md) as "the root directory for the entire topic covered in this session." It contains four numbered notes meant to be read roughly in order, plus a README that indexes them:

| File | Content | Wiki page |
|---|---|---|
| `00-llm-friendly-docs-framework.md` | The session's starting point: a 12-principle framework for writing LLM-friendly documentation (explicitness, glossary, Constraints, ADRs, verification loop, etc.) | [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md) |
| `01-research-summary.md` | The result of validating that framework against three cloned open-source projects (Apache Amoro, Iceberg, Paimon), revising the hypothesis into a four-factor model of agent expertise | [Validating the Framework: Where Agent Expertise Comes From](frameworks/framework-validation-research.md) |
| `02-instruction-clarity-incident.md` | The opposite direction: a real recorded failure case where the agent misjudged a lookup-resolvable fact as a user decision | [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md) |
| `03-instruction-resolution-gate.md` | A requirement-interpretation gate designed from the incident in `02`, distinguishing lookup-resolvable from judgment-required ambiguity | [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md) |

The `agent-expertise-framework/README.md` also points to three sibling analysis directories one level up in the same workspace but **outside this repository** (`../../data-lake/amoro-analysis`, `../../data-lake/iceberg-analysis`, `../../data-lake/paimon-analysis`) that were cloned and analyzed as part of the same research pass. Those directories are referenced as external context throughout `01-research-summary.md` but are not part of this repository, so this wiki does not document their internal content directly — see [Validating the Framework](frameworks/framework-validation-research.md) for what each contributed.

### Root-level files

- `AGENTS.md` and `CLAUDE.md` are agent-facing instruction files. Both currently contain only an OpenWiki-managed block pointing readers to this generated wiki as optional just-in-time context, and instructing that generated OpenWiki pages should not be hand-edited — source docs should be updated instead and the wiki regenerated.
- `.mcp.json` registers the `openwiki` MCP server (invoked as `openwiki mcp --host claude`), which is what an interactive Claude Code session uses to run the page-job lifecycle that produced this wiki.
- `.github/workflows/openwiki-update.yml` defines a scheduled GitHub Actions workflow (daily cron plus manual dispatch) that runs `openwiki code --update` in CI using an OpenAI-backed provider, and opens a pull request with any resulting changes to `openwiki/`, `AGENTS.md`, `CLAUDE.md`, and the workflow file itself.

## Why this repository has an OpenWiki setup

This is a research-notes repository rather than an application, so there is no runtime, build, or API surface to document in the traditional sense. The OpenWiki instance here instead documents the *content* of the research: the framework, its validation, the incident that prompted a design response, and that design itself — the same four artifacts listed in the table above.

## Related pages

- [Quickstart](quickstart.md) — where to start reading depending on what you want to know
- [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md)
- [Validating the Framework: Where Agent Expertise Comes From](frameworks/framework-validation-research.md)
- [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md)
- [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md)
