---
type: design-and-harness
title: Self-Improvement Loop and Eval Harness
description: The evaluate, diagnose, improve loop designed in notes/04, the pipeline options and staged plan in notes/05, and the runnable harness in experiments/eval that implements two pieces of it (a grounding metric over OpenWiki Claims and swappable response filters).
tags: [evaluation, self-improvement, deepeval, presidio, grounding]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:09:17.598Z
sources:
  - id: openwiki-source-20d2f486b822d1f970e69b57
    resource: repo://experiments/eval/compare_filters.py
  - id: openwiki-source-afd2e5743eb3912d02624555
    resource: repo://experiments/eval/filters/base.py
  - id: openwiki-source-4cc6ce5f988d7bbd5992e213
    resource: repo://experiments/eval/grounding_metric.py
  - id: openwiki-source-5a4a6690f3c21048806a3e0e
    resource: repo://experiments/eval/test_grounding.py
  - id: openwiki-source-93b351e0fe7cd05dd0058da9
    resource: repo://notes/04-purpose-and-self-improvement-loop.md
  - id: openwiki-source-afcfb207b2b2de69330360e2
    resource: repo://notes/05-pipeline-options-and-plan.md
  - id: openwiki-source-733117321a85db437c83db32
    resource: repo://notes/09-repo-structure-and-pipeline.md
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## What this covers

`notes/04-purpose-and-self-improvement-loop.md` adds the parts of the 12-principle documentation framework that turned out weak or missing (status separation, glossary, constraints, ADRs, verification) on top of the four-element model of agent expertise. Its central design is a self-improvement loop. `notes/05-pipeline-options-and-plan.md` compares four ways to wire that loop and stages the work. `experiments/eval/` is the only part that actually runs.

## The loop (notes/04 §7)

The loop has six steps: generate a response, score it per purpose with DeepEval custom metrics, gate releases with Promptfoo regression tests, monitor production traces, attribute any failure to a cause, then rescore after the fix.

The attribution step is the core of the design. A failure must be routed to exactly one of five fixed categories before the loop can continue:

| Category | Fix |
|---|---|
| Grounding failure | Strengthen the source docs and regenerate |
| Interface over-exposure | Shrink the exposed tools |
| Sensitive data exposure | Add a filter rule |
| Repeated mistake | Add a Never or Ask-first constraint |
| None of the above | Record as a candidate fifth element |

The doc contrasts this with Reflexion-style self-critique: criticism comes from an external scorer and the result is forced into fixed categories, rather than the same model reflecting freely.

## Failure-derived constraints (notes/04 §5)

Seven Never and Ask-first rules were extracted from incidents in the original session, for example never paraphrasing away side mentions when delegating a user request, never hand-editing OpenWiki output, and never writing a subagent's negative conclusion ("no such library exists") into a doc without re-verifying it. The doc itself flags that seven rules from one session is a small sample.

## Pipeline options (notes/05)

| Option | Shape |
|---|---|
| A | CI gate: DeepEval and Promptfoo on every PR |
| B | Gateway: all responses pass one gateway with built-in guardrails |
| C | Observability first: no pre-release gate, trace production |
| D | Full combination: the whole notes/04 loop |

Option A was chosen as the first stage, with D as the direction to grow into. C conflicts with the project's principle of blocking bad judgment structurally before it ships, and B depends on a gateway whose maintenance signals were the weakest surveyed. Of the eight staged steps, only step 1 (grounding metric and filter comparison harness) is marked done. Step 3 assumed a GitHub Actions workflow, and this repo no longer has one (see [Repository Structure and Work Pipeline](../operations/repository-workflow.md)).

## The harness (experiments/eval)

**Grounding metric.** `grounding_metric.py` is a deterministic DeepEval metric with no LLM call. It parses a Claim evidence resource of the form `repo://path#Lstart-Lend` and fails if the file no longer exists or the line range is out of bounds. It does not compare content hashes, so a line that changed in place still passes. `test_grounding.py` turns every evidence entry in `openwiki/.claims/**/*.json` into a pytest case. Both files locate the repo root as two directories up from their own location, which only holds while the harness lives at `experiments/eval/`. An earlier move to a deeper folder silently broke this.

**Swappable filters.** `filters/base.py` defines a `ResponseFilter` interface with a single `scan` method. A regex baseline and a Presidio backend (with custom PEM key, AWS key, and email recognizers) implement it, and `compare_filters.py` runs every backend in its `BACKENDS` list over a labeled five-case corpus. Adding a backend means implementing `ResponseFilter` and appending it to that list.

## Recorded results

On 2026-11-02, after the venv was rebuilt at the new location:

- The filter comparison matched the earlier record: regex baseline recall 0.75 (missed the AWS key), Presidio 1.00, no false positives for either.
- The grounding test failed 21 of 24 cases. Every failure was a Claim whose evidence pointed at the pre-restructure path `agent-expertise-framework/...`. This is the failure the metric exists to catch, and regenerating the wiki is what resolves it. The "30 passed" figure in notes/04 and the harness README predates the September folder move.

## Related pages

- [Validating the Framework](../frameworks/framework-validation-research.md): the four elements the loop routes failures to
- [Hook Enforcement](../orchestration/hook-enforcement.md): one of the notes/04 Never rules turned into a Hook
