---
type: baseline-study
title: KakaoPay Baseline
description: The study of 24 KakaoPay tech blog posts read from original HTML (notes/13, sources/kakaopay), the principles that recur across them, and the area-by-area design in notes/14 that treats KakaoPay's practice as the floor and goes beyond it only where external evidence supports it.
tags: [kakaopay, baseline, orchestration, design, sources]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:09:17.598Z
sources:
  - id: openwiki-source-44b1ec50bc9b1fe792a12203
    resource: repo://notes/13-kakaopay-tech-blog-study.md
  - id: openwiki-source-472fb6349572fc3fd8434e69
    resource: repo://notes/14-kakaopay-baseline-and-target.md
  - id: openwiki-source-0312ea6e7bd18a03063bbb7c
    resource: repo://notes/diagrams/system-flow/render.sh
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## Why KakaoPay is the baseline

On 2026-09-27 the user set the target: build an agent system at least as developed as KakaoPay's, and go further where justified. `decisions.md` records this as D11.

## The study (notes/13)

The blog's full list of 164 posts was collected, and the 24 related to AI, LLMs, agents, and operations automation were read. WebFetch summaries were deliberately avoided. Each post was read from its original HTML, including body images, because an earlier WebFetch summary of the "AI Agent" post had dropped details and introduced content that was not in the original. That earlier summary is the source of the errors now flagged in notes/07 (see [Hook Enforcement](hook-enforcement.md)).

Each post has its own note in `sources/kakaopay/`, all using the same template, and notes/13 is the table of contents. The posts fall into four groups: agents and harness, LLM services and platform, 2025 hackathon projects, and operations automation.

## Principles that recur across posts

notes/13 keeps only principles that appear in several posts:

1. Prevent mistakes with structure, not prompts.
2. AI drafts and recommends, people approve and execute. This held without exception across the posts.
3. Use multiple agents only when conditions call for it. Only one project built a supervisor-style multi-agent system, and its author recorded it as slow and unstable. The voice chatbot chose a single agent on purpose because its flow was linear.
4. Split work small, one thing per call or per PR.
5. Code owns the flow. For example, the loan coach picks agents by status in code rather than with an LLM supervisor.
6. Keep one source of truth and cite it in answers.
7. Keep tools and permissions narrow.
8. Verify with external signals, such as a separate SQL validation call or a gate that requires zero critical findings.
9. Measure before and after. One retrospective regretted not collecting pre-change data, and the hackathon posts had no quantitative evaluation.

## The baseline design (notes/14)

notes/14 defines the floor carefully:

- **Baseline** is what KakaoPay actually runs in production (PR review, spec-driven development, deployment bot, resource recommendation, fraud detection, MCP toolkit).
- The "AI Agent" concept post is the baseline for harness ideas, though it has no measurements.
- Hackathon posts are reference only. They are two-day prototypes without quantitative evaluation, but they inform when to use multiple agents.
- **Beyond baseline** is only what KakaoPay's posts lack or do weakly and external evidence supports. Nothing is added without evidence.

It then sets a baseline and a beyond-baseline column for ten areas: planning and specification, production, review, supervision and monitoring, documents and knowledge, tools and permissions and security, human approval boundaries, operations automation, measurement, and multi-agent judgment. A one-screen flow diagram lives in `notes/diagrams/system-flow/`. Its HTML fixes the layout by hand because automatic Mermaid layout scrambled the order, and `render.sh` captures it to PNG with headless Chrome.

## What notes/14 replaces

Some KakaoPay content is replaced rather than adopted, with reasons drawn from [Orchestration Evidence](orchestration-evidence.md):

| KakaoPay content | Replacement | Reason |
|---|---|---|
| Persona split in the "AI Agent" post (strict architect, fast junior, harsh QA) | Roles defined by goal, output format, tools, boundaries, and permissions | Concept example without measurement. Personas showed no accuracy effect even on reasoning models. Splitting by kind of work loses context at each handoff |
| Five roles per department (the user's original idea) | Departments may be agents, but the five roles become process stages | Same reasons |
| Whole PR diff in one prompt | Review per file | Guardrail throttling on large diffs, and long inputs degrade performance |

## Still undecided

Whether tools and permissions really differ by department, which actions are irreversible, and which single task in which department to build first. The last one is `decisions.md` D04.

## Related pages

- [Orchestration Evidence and Design Judgment](orchestration-evidence.md)
- [Hook Enforcement](hook-enforcement.md)
- [Master Orchestrator Research](master-orchestrator.md)
