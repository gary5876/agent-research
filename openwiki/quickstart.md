---
type: quickstart
title: Quickstart
description: Task-routing map for this repository. Where to start for each kind of question, using the notes, sources, and experiments layout, the generated index, the decisions list, and the wiki sections.
tags: [quickstart, navigation, routing]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:09:17.598Z
sources:
  - id: openwiki-source-8037e2358a2c4f9b2c722a11
    resource: repo://AGENTS.md
  - id: openwiki-source-a2371d6362e5db4bc834ad03
    resource: repo://CLAUDE.md
  - id: openwiki-source-78adcd79964049a8d458e647
    resource: repo://index.md
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## First stops

- **`index.md`** in the repository root is the starting point. Its generated block lists every note by topic with status, layer, and a one-line summary, the `sources/` folders, the experiments, and what is still open.
- **`decisions.md`** shows which direction-level decisions are open and which are settled.
- **`AGENTS.md`** gives the working rules and the nine-step pipeline. Its top block is managed by OpenWiki. `CLAUDE.md` only points to that block.

## Where to go for a question

| You want to know | Start with |
|---|---|
| What this repository is and how it got here | [Repository Overview](overview.md), then `JOURNEY.md` |
| How to add a note or where a file belongs | [Repository Structure and Work Pipeline](operations/repository-workflow.md) |
| How to write documents an LLM reads well | [LLM-Friendly Documentation Framework](frameworks/llm-friendly-documentation.md) |
| Where agent expertise comes from (the four elements) | [Validating the Framework](frameworks/framework-validation-research.md), then [Agent Implementation Schema](frameworks/agent-implementation-schema.md) |
| Why an agent asked instead of looking something up, and how to prevent it | [Instruction Clarity Incident](frameworks/instruction-clarity-incident.md), then [Instruction Resolution Gate Design](frameworks/instruction-resolution-gate.md) |
| How quality is measured, and how to run the eval harness | [Self-Improvement Loop and Eval Harness](evaluation/self-improvement-loop.md) |
| How subagents are delegated to and verified | [Orchestrator Pattern and Worker Agents](orchestration/orchestrator-pattern.md) |
| Why a rule is a Hook, or why an edit was blocked | [Hook Enforcement](orchestration/hook-enforcement.md) |
| What external evidence says about multi-agent systems | [Orchestration Evidence and Design Judgment](orchestration/orchestration-evidence.md) |
| What "at least as good as KakaoPay" means | [KakaoPay Baseline](orchestration/kakaopay-baseline.md) |
| The state of the master (Jarvis-style) agent design | [Master Orchestrator Research](orchestration/master-orchestrator.md) |

## Reading the notes

Notes are in Korean. Their YAML frontmatter tells you status (DRAFT, ACTIVE, PLANNED, DEPRECATED) and layer (1 original record, 2 design, 3 implementation, 4 generated). Before citing a layer 2 design, check the layer 1 material it was built from. Where notes/10 and notes/11 disagree on orchestration evidence, notes/11 is the current one.

## Related pages

- [Repository Overview](overview.md)
- [Repository Structure and Work Pipeline](operations/repository-workflow.md)
