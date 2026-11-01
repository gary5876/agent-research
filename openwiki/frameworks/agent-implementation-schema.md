---
type: concept
title: Agent Implementation Schema
description: The domain-agnostic schema in notes/08 that places the four elements of agent expertise onto the agent anatomy (LLM, body, Tools, Context, Skills), why it was written, and how notes/09 instantiates it for this repository.
tags: [agent-expertise, schema, four-elements, repo-structure]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:09:17.598Z
sources:
  - id: openwiki-source-c4aef6faa9e5b156d753c9ff
    resource: repo://notes/08-agent-implementation-schema.md
  - id: openwiki-source-733117321a85db437c83db32
    resource: repo://notes/09-repo-structure-and-pipeline.md
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## Why it exists

By the time `notes/07` was written, the repo had two vocabularies for agent expertise: the four elements from `notes/01` (coherent data lake, narrow explicit interface, safe response filter, failure-derived prohibition rules) and the agent anatomy taken from the KakaoPay tech blog (a stateless LLM "head", an agent "body" running a ReAct loop, and three handles the body adjusts: Tools, Context, Skills).

`notes/08` records that while designing the repo's own document catalog, the same mistake was made three times because these two vocabularies were treated as separate problems:

1. A hand-written Layer table in `CATALOG.md` duplicated what each document's own tag already said.
2. A line-range sha256 verification system was added to detect drift between the two copies. A critique pass found it just repeated the duplication in a new form, so it was dropped.
3. A draft `write-docs` skill required exception ranges to be stated by heading number, which a real document (`06`) immediately violated.

Each time, a new concept was invented instead of consulting the principles the repo already had.

## The schema

The four elements sit on the anatomy's handles:

| Agent handle | Element | General definition |
|---|---|---|
| Context material | Coherent data lake | Every knowledge unit carries its own classification. No separate index remembers it on the unit's behalf. The lake's boundary is explicit |
| Skills | Narrow explicit interface | Access to the lake is a few fixed, named operations. At least the "put" and "find" directions share one definition of a knowledge unit |
| Skills' responses | Safe response filter | Responses distinguish originals from derived material, and originals win |
| What keeps the above correct | Failure-derived rules | Only the procedure is general: failure happens, diagnose in one line, add one Never rule |

The KakaoPay capability ladder (Tool, MCP, Skill, Plugin, Marketplace) is treated as a finer vocabulary for the Skills row, not a separate framework.

`notes/08` deliberately stops at the schema and defers filling it in for this repository to a separate document, because designing the schema and its instance in the same document is what caused the three failures.

## The instance: notes/09

`notes/09-repo-structure-and-pipeline.md` (2026-11-02) is that deferred document. It maps each row onto the restructured repo:

| Element | In this repo |
|---|---|
| Data lake | Every note in `notes/` carries `status`, `layer`, and `topic` in its own frontmatter. The lake boundary is `notes/`, `sources/`, and `experiments/` |
| Interface | Two operations. Put is the work pipeline plus `scripts/check.py`. Find is the generated `index.md` plus frontmatter grep. Allowed values live only in `scripts/build_index.py`, which `check.py` imports |
| Filter | `sources/` holds originals (layer 1), notes hold derived material, and designs are checked against originals before being cited |
| Failure rules | Failures found during the restructure (stale hand indexes, a path-dependent test bug) became `check.py` rules and a pre-commit Hook |

See [Repository Structure and Work Pipeline](../operations/repository-workflow.md) for the operational side.

## Related pages

- [Validating the Framework](framework-validation-research.md): where the four elements came from
- [Hook Enforcement](../orchestration/hook-enforcement.md): the source of the agent anatomy and the "Hook over prompt" principle
- [Repository Structure and Work Pipeline](../operations/repository-workflow.md)
