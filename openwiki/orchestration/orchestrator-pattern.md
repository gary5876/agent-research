---
type: pattern
title: Orchestrator Pattern and Worker Agents
description: The five-stage decompose, dispatch, monitor, verify, reconcile pattern that notes/06 extracted from this repository's own delegated research, the failures that shaped it, and the four worker agents defined in .claude/agents with their real usage status.
tags: [orchestration, subagents, verification, claude-code, worker-agents]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:09:17.598Z
sources:
  - id: openwiki-source-532b557cbcfe2d098552cfdb
    resource: repo://.claude/agents/doc-writer.md
  - id: openwiki-source-91c2366dae09576bb6e2abc2
    resource: repo://.claude/agents/researcher.md
  - id: openwiki-source-24b09495dacc3b118d12e76f
    resource: repo://.claude/agents/supervisor.md
  - id: openwiki-source-5155c57fd5e2c59e1ed895a5
    resource: repo://.claude/agents/verifier.md
  - id: openwiki-source-78adcd79964049a8d458e647
    resource: repo://index.md
  - id: openwiki-source-ae2ec522901d6f17247acab5
    resource: repo://notes/06-orchestrator-pattern.md
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## Recorded before designed

`notes/06-orchestrator-pattern.md` does not design a manager agent from scratch. It records what the session coordinator had already done several times when delegating research to subagents, then checks that against external patterns.

Its central claim is that the core of a manager agent is not splitting work into parallel pieces, but refusing to accept returned results until they are verified. Of six delegated research tasks, three came back with a wrong conclusion or premise: a "no such library exists" result that `gh api` later disproved, a top recommendation for a project that turned out to be merging into another, and an inherited premise that a framework had already been adopted. Negative conclusions and uncritically inherited premises were the most frequent failure modes.

## The five stages

1. **Decompose.** Keep the user's original requirements in the subtask prompt without summarizing them away. Skipping this caused a delegation that dropped a side mention, now a Never rule in notes/04.
2. **Dispatch.** Run subagents in the background.
3. **Monitor.** Wait for completion notifications instead of polling.
4. **Verify.** The most important and most often skipped stage. Re-check negative and ranking conclusions with an independent tool before using them.
5. **Reconcile.** If verification disagrees, fix the document and extract the error into a rule so it does not recur.

Following the [Instruction Resolution Gate Design](../frameworks/instruction-resolution-gate.md), notes/06 argues that verification should be structural: a conclusion should reach a document only if an independent re-check is on record first.

## What had not been tested

notes/06 lists its own limits. True parallel dispatch had never been run, since every delegation was sequential. Retrying a crashed subagent had never happened. Subagents never communicated directly, so only a star topology through the coordinator was exercised.

## The four worker agents

To prepare for a real parallel test, the coordinator's roles were split into four subagent definitions in `.claude/agents/`, each with rules extracted from the failures above:

| Agent | Stage | Model | Tools | Key rule |
|---|---|---|---|---|
| `researcher` | Dispatch executor | inherit | WebSearch, WebFetch, Bash, Read | Try to disprove a "does not exist" conclusion with several queries. Check repo numbers with `gh api` |
| `verifier` | Verify | inherit | WebSearch, WebFetch, Bash, Read | Re-check through independent tool calls, never by reusing the researcher's reasoning. Answer CONFIRMED, REFUTED, or COULDN'T VERIFY |
| `doc-writer` | Reconcile | inherit | Read, Edit, Write, Grep, Glob | Write only already-verified findings. Since 2026-11-02 it writes frontmatter, runs `build_index.py` and `check.py`, and follows the banned-text rules |
| `supervisor` | Monitor (loop detection) | haiku | Read, Grep, Glob | Flag repeated failures and escalate instead of fixing. Its thresholds are guesses that have not been validated |

The supervisor uses a lightweight model because it judges process state, not code correctness.

## Usage status

When notes/06 was written, none of the four had been dispatched by name. The roles were played by the coordinator. The repository index now records that `researcher` was first used on 2026-11-02, for the prior-art survey behind the repository restructure, and that the other three remain definitions only. The planned experiment of dispatching several of them at once is still not done.

## Related pages

- [Hook Enforcement](hook-enforcement.md): the one fully automated control point at the time, and the origin of the supervisor role
- [Orchestration Evidence and Design Judgment](orchestration-evidence.md): later external evidence on the same questions
- [Repository Structure and Work Pipeline](../operations/repository-workflow.md): where research, verify, and write-up became pipeline steps
