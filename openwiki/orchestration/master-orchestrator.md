---
type: research-index
title: Master Orchestrator Research
description: Research toward a master ("Jarvis-style") agent that coordinates department agents. Covers the three original-source surveys and where they agree (notes/15, sources/master-orchestrator), the superpowers study and what to take from it (notes/16, sources/superpowers), and the open decisions that block the design.
tags: [master-agent, orchestration, superpowers, magentic-one, decisions]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:09:17.598Z
sources:
  - id: openwiki-source-b59005f0f903d10c3bb60923
    resource: repo://decisions.md
  - id: openwiki-source-cfa2d216c056682eaee147ff
    resource: repo://notes/15-master-orchestrator-research.md
  - id: openwiki-source-71fc76818520c29ee761d856
    resource: repo://notes/16-superpowers-study.md
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## Where this fits

After [Orchestration Evidence and Design Judgment](orchestration-evidence.md) and the [KakaoPay Baseline](kakaopay-baseline.md), the next layer up is the master agent that coordinates department agents. On 2026-09-28 the user asked for one, noting such agents are often called Jarvis. The research so far is surveys and one study. There is no design document yet.

## Three surveys (notes/15)

Each survey was written by an agent that appended to its file after finishing each source, and they live in `sources/master-orchestrator/`:

| File | Covers |
|---|---|
| `master-internals.md` | How masters work inside: Magentic-One's task and progress ledgers, Microsoft Agent Framework, Anthropic's lead agent and 2026 posts, Managed Agents coordinator, Devin, Cursor, OpenAI, LangChain, Google ADK, four research papers |
| `jarvis-named-systems.md` | Systems named Jarvis, from Microsoft JARVIS (HuggingGPT) to open-source repos and company cases |
| `oss-orchestrators.md` | 13 open-source orchestrators on top of Claude Code, with a comparison table and what to take and avoid |

Where all three agree:

1. The master does not do the work. It plans, delegates, checks, and reports, and open-source tools enforce this with permissions.
2. The strongest numeric evidence is for Magentic-One's task and progress ledgers. Removing them cost 31%, though that ablation removed planning, loop detection, and explicit instructions together.
3. Delegation uses a fixed form: goal, output format, tools, boundaries, success criteria.
4. Progress lives in files or event logs, not conversation memory. Completion is judged by artifacts and separate verification, not by the agent's report.
5. Retries and replans have numeric caps. Designs that said "never ask a human" or "retry without limit" were the ones with reported runaway loops.
6. Human approval points are explicit in role definitions and action tiers. A coordinator cannot substitute for human approval.
7. None of the surveys found independent measurement of department-style masters. Open-source performance numbers are almost all self-reported or unsupported.

## Study 1: superpowers (notes/16)

The first "study a well-known orchestrator first" note (`decisions.md` D14) read superpowers v6.3.0 from its installed files. Its development history (design docs, evaluations, release notes, issues) is in `sources/superpowers/design-history.md`.

The flow for one request is brainstorming, an isolated worktree, a written plan of 2 to 5 minute steps, subagent-driven development, and a finish step where a human chooses merge, PR, keep, or discard. In subagent-driven development the controller never implements or fixes anything itself. It keeps a per-plan ledger file, sends each task as a brief file plus a five-part instruction, accepts only short four-state reports, and judges completion from git diff and review, not from the implementer's claim.

notes/16 lists seven things to take into the master design: the ledger file, the five-part delegation with a single brief file, the report contract, reviewer rules (do not trust reports, do not pre-trim findings, do not use a cheap model for review), a five-round fix cap with stronger models from round four, a table-based contradiction check before starting, and mandatory model assignment per role.

## Open decisions blocking the design

These are rows D01 to D05 in `decisions.md`:

- **D01**: when new ambiguity appears mid-run, stop and ask, or decide and log. superpowers asks only for four kinds of risky actions and logs everything else, citing a nine-hour stall. This conflicts with the user's 2026-09-28 decision (D07) to keep asking until the plan is clear.
- **D02**: the final role and authority of the master.
- **D03**: whether the master is implemented in this repository or a separate one.
- **D04**: which single department task to build first.
- **D05**: where to get an evaluation set of 20 cases.

The overall shape is already decided (D12): the master makes judgments, and workflow code owns the execution flow.

## Related pages

- [Orchestration Evidence and Design Judgment](orchestration-evidence.md)
- [KakaoPay Baseline](kakaopay-baseline.md)
- [Repository Structure and Work Pipeline](../operations/repository-workflow.md): how decisions.md is maintained
