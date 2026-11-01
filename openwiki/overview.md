---
type: overview
title: Repository Overview
description: What this repository is and how it is organized. A personal research repository on building agents with real expertise, which moved from LLM-friendly documentation to multi-agent orchestration and a master agent, laid out since 2026-11-02 as notes, sources, and experiments with a generated index and a decisions list.
tags: [overview, research-notes, agent-expertise, orchestration, openwiki]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:49:51.673Z
sources:
  - id: openwiki-source-f5a489e5822d87c0b8fc66ef
    resource: repo://.mcp.json
  - id: openwiki-source-b59005f0f903d10c3bb60923
    resource: repo://decisions.md
  - id: openwiki-source-9a99b7511a4d4f8356a83ea6
    resource: repo://JOURNEY.md
  - id: openwiki-source-733117321a85db437c83db32
    resource: repo://notes/09-repo-structure-and-pipeline.md
  - id: openwiki-source-c14bb42577beb1d920ff82a4
    resource: repo://notes/17-orchestration-news-2026-10.md
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
generated: { by: "claude-code", at: "2026-11-01T16:49:51.673Z" }
---

## What this repository is

This is not a software project. It is a research repository whose stated goal is building an agent with real domain expertise (`decisions.md` D06). The notes are written in Korean. It is also a test bed: the worker agents in `.claude/agents/` and the Hooks in `.claude/hooks/` apply the repository's own conclusions to itself.

## How the inquiry moved

| Period | Focus | Wiki section |
|---|---|---|
| 2026-08-30 to 08-31 | How to write documentation an LLM reads reliably, validated against Apache Amoro, Iceberg, and Paimon into the four elements of agent expertise. An incident where an agent asked for something it could look up | [Frameworks](frameworks/) |
| 09-02 | Narrowed the goal to an expert agent, demanded prior-art checks and an evaluation environment | [Self-Improvement Loop and Eval Harness](evaluation/self-improvement-loop.md) |
| 09-04 to 09-06 | Orchestration of several agents, rules enforced by Hooks, a general implementation schema | [Orchestrator Pattern](orchestration/orchestrator-pattern.md), [Hook Enforcement](orchestration/hook-enforcement.md), [Agent Implementation Schema](frameworks/agent-implementation-schema.md) |
| 09-21 | A layer that assembles vague requests into precise prompts | [Instruction Resolution Gate](frameworks/instruction-resolution-gate.md) |
| 09-25 to 09-30 | Department-style orchestration, KakaoPay as the baseline, research toward a master agent | [Orchestration Evidence](orchestration/orchestration-evidence.md), [KakaoPay Baseline](orchestration/kakaopay-baseline.md), [Master Orchestrator Research](orchestration/master-orchestrator.md) |
| 11-02 | Restructured the repository and its work pipeline | [Repository Structure and Work Pipeline](operations/repository-workflow.md) |
| 11-02 | First news sweep through the new pipeline: October 2026 orchestration news, 17 claims verified, recorded in `notes/17` | [Orchestration Evidence and Design Judgment](orchestration/orchestration-evidence.md) |

`JOURNEY.md` tells this story in date order, quoting the user's own words.

## Layout

| Location | Role |
|---|---|
| `index.md` | Start here. Its lower block is generated from note frontmatter by `scripts/build_index.py` |
| `notes/NN-slug.md` | All research and design notes. Numbers are permanent IDs |
| `sources/` | One note per external item (KakaoPay posts, master orchestrator surveys, superpowers history). Written once |
| `experiments/eval/` | The runnable evaluation harness |
| `decisions.md` | Open and settled direction-level decisions |
| `JOURNEY.md` | Dated narrative |
| `AGENTS.md` | Working rules and the work pipeline. Its top block is managed by OpenWiki |
| `.claude/` | Worker agents, Hooks, and the OpenWiki skill |
| `scripts/` | Index generator and repo lint |
| `openwiki/` | This wiki |

Before 2026-11-02 the notes lived in `agent-expertise-framework/`, split by the four elements. That tree no longer exists. `notes/09-repo-structure-and-pipeline.md` explains why it was replaced.

## How this wiki is produced

`.mcp.json` registers the `openwiki` MCP server, which an interactive Claude Code session uses to run OpenWiki's page-job lifecycle. The wiki is regenerated only that way, locally. There is no scheduled CI run and no model API key (`decisions.md` D16). Generated pages are protected by a Hook, described in [Hook Enforcement](orchestration/hook-enforcement.md).

The research also draws on folders outside this repository in the same workspace, such as the Amoro, Iceberg, and Paimon analyses under `data-lake/`. This wiki does not document their contents.

## Related pages

- [Quickstart](quickstart.md): where to start for each kind of question
- [Repository Structure and Work Pipeline](operations/repository-workflow.md)
- [Agent Implementation Schema](frameworks/agent-implementation-schema.md)
- [Master Orchestrator Research](orchestration/master-orchestrator.md): the current frontier
