---
type: "Reference"
title: "Framework validation research"
description: Validating the LLM-friendly documentation framework against three cloned open-source projects, revising the hypothesis into a four-factor model of agent expertise.
tags: [research, validation, agent-expertise, four-factor-model]
verified:
  - by: openwiki/0.4.3
    at: 2026-09-05T20:17:03.290Z
sources:
  - id: openwiki-source-f974e1c8ce579ae676932d80
    resource: repo://agent-expertise-framework/00-data-lake/01-research-summary.md
generated: { by: "claude-code", at: "2026-09-05T20:17:03.290Z" }
---

## Starting point

This note picks up where [LLM-Friendly Documentation Framework](llm-friendly-documentation.md) leaves off. That framework proposes principles for writing documentation an LLM can read without having to "reconstruct by inference." This page documents the next step: testing that framework against real open-source repositories rather than leaving it as untested theory.

## Progression of the research

1. **Starting question**: how should LLM-friendly documentation be written to reduce hallucination?
2. **Hypothesis**: agent expertise comes from the data lake being structured in a way that is easy for the agent itself to consume.
3. **First validation target**: Apache Amoro — chosen because it is both a lakehouse management system and ships `amoro-mcp-server`, an agent-facing interface module, making it possible to test the hypothesis directly against a real agent interface.
4. **Hypothesis revision**: a well-structured data lake alone was found insufficient (see below).
5. **Extended validation**: comparison widened to two of the three table formats Amoro manages — Iceberg and Paimon (Hudi excluded, see caveat below) — to compare both the design philosophy differences between table formats and how differently each project's own `AGENTS.md` is written.

## Revised hypothesis (final)

> Agent expertise comes not from "a well-built data lake" alone, but from the combination of: a coherent data lake + a narrow, explicit query interface + a safe response filter + a documented set of failure-derived prohibition rules.

Each of the four factors and its supporting basis, as recorded in the source note:

| Factor | Basis |
|---|---|
| Coherent data lake | Amoro's self-optimizing behavior and unified catalog |
| Narrow, explicit interface | Amoro's MCP server exposes only 11 GET-style tools and explicitly states it has no general-purpose action executor |
| Safe response filter | Dual filtering — a blacklist (regex) plus a whitelist (field allowlist) |
| Failure-derived prohibition rules | Iceberg's `AGENTS.md` was reverse-derived from 58,000+ PR review comments, distinguishing `Never` rules from `Ask first` rules |

The fourth factor was not part of the original hypothesis; it emerged while comparing the density of `AGENTS.md` files across Amoro, Iceberg, and Paimon.

This four-factor model was later synthesized with an Agent anatomy (LLM/body, Tools/Context/Skills) drawn from external research into a domain-agnostic implementation schema, recorded in `agent-expertise-framework/08-agent-implementation-schema.md` in the repository (not yet covered by a dedicated wiki page).

## What each external analysis contributed

The research draws on three sibling analysis directories outside this repository (`../../data-lake/amoro-analysis`, `../../data-lake/iceberg-analysis`, `../../data-lake/paimon-analysis`, referenced from [agent-expertise-framework/00-data-lake/01-research-summary.md](../../agent-expertise-framework/00-data-lake/01-research-summary.md)):

- **amoro-analysis** is the core case study: the lakehouse management structure plus a deep analysis of the MCP-based agent interface. Most of the evidence for the revised hypothesis comes from here.
- **iceberg-analysis** covers a "spec-first, implementation-later" project's module-boundary design, and the review-comment-derived `AGENTS.md` case study.
- **paimon-analysis** is a contrast case: a fundamentally different storage structure (LSM-tree) from Iceberg, paired with a thin `AGENTS.md` that documents build commands only.

## Method note

All three repositories were shallow-cloned (`--depth 1`) locally so the actual code and spec documents could be read and verified directly, rather than relying on summaries. Apache Hudi was not cloned — its packed size (2.9GB) is more than 20x the other two — so any Hudi-related statements in the source material are explicitly marked as unverified rather than asserted as fact. This itself is presented as an example of following framework principle 3 (separating current/verified state from unconfirmed state) within the research note itself.

## Open questions noted in the source

- Framework principle 12 (a verification loop: task → cross-check docs against code → report on mismatch instead of guessing) was applied only to the static production of documentation in this research pass. It was not yet tested inside an actual agent code-editing loop.
- Cloning and analyzing Hudi directly would complete the three-way comparison into a four-way one.
