---
type: design-proposal
title: Instruction Resolution Gate Design
description: A proposed interpretation layer that classifies ambiguity as lookup-resolvable or requiring user judgment, assembles a precise prompt through a loop where search and questions feed each other, uses per-domain slot schemas, and confirms the finished prompt before execution. Built from the instruction clarity incident and revised on 2026-09-21.
tags: [design, instruction-clarity, ambiguity, agent-architecture, gate]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:49:51.673Z
sources:
  - id: openwiki-source-b59005f0f903d10c3bb60923
    resource: repo://decisions.md
  - id: openwiki-source-c77851ae36e5d23e15577e7e
    resource: repo://notes/03-instruction-resolution-gate.md
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## Purpose

`notes/03-instruction-resolution-gate.md` designs the layer between a user's natural language and a specialized agent, using the [Instruction Clarity Incident](instruction-clarity-incident.md) as its material. Its one-line goal is not to eliminate questions, but to separate ambiguity that a lookup can resolve from ambiguity only the user can resolve, and to stop the first kind from being thrown back at the user as a question.

## Two kinds of ambiguity

- **Lookup-resolvable**: the answer already exists and can be settled from conversation context, memory, or tools. Example: "a repo on my GitHub", which the account plus `gh api` resolves.
- **Judgment-required**: there are several candidates, or the user's preference is the answer. Example: which directory to reorganize.

Treating a lookup-type gap as a judgment call produces the original incident. Treating a judgment call as a lookup lets the agent silently decide something the user should have.

## The assembly loop (2026-09-21 revision)

The first version was a straight line: try a lookup, ask if it fails. The revision turned it into a loop:

1. Identify the request's domain and load that domain's slot schema.
2. While empty slots remain, pick one. Fill it from context if possible. For a lookup-type slot, search the source the schema names, fill it if the result is unique, otherwise ask with the search results attached as options. For a judgment-type slot, ask with options built from already-filled slots and search results.
3. If a newly filled value is a clue for another slot, send that slot back to search.
4. Show the assembled prompt once for confirmation, then execute.

Search and questions feed each other. A search turns an open question ("which repo?") into a choice among found candidates, which people answer more accurately. An answer can trigger the next search, such as reading the chosen repo's README to fill the "reorganization criteria" slot. The invariant stays the same: for a lookup-type slot, a question can only come after a search attempt.

## Per-domain slot schemas

Letting the model invent slots on the fly makes two things unstable: which slots exist, and whether each slot is lookup or judgment. The incident failed on the second. So slots are written down ahead of time per domain, each with a type (lookup or judgment), a source (where to search, or where to get options), and dependencies on other slots. The doc argues that knowing which slots a request in a domain needs, for example a code review versus a cover letter, is what domain expertise means.

## Why it must be a structural gate

Revisiting the incident, the failure was not a wrong choice between looking up and asking. The comparison never ran: an empty slot went straight to question generation. Since the skipped step was the deliberation itself, telling the model to deliberate does not prevent recurrence. The layer therefore has to be enforced outside the model's reasoning, for example by allowing a question tool call only when a lookup record exists for that slot. The slot schema makes this checkable: a lookup-type slot requires a search record, a judgment-type slot passes.

## Confirmation and question cap

After the loop, the assembled prompt is shown once with the source of each slot value (memory, search, user answer, default). This catches searches that narrowed to a single wrong candidate, and costs the user one review instead of one question per slot. The doc also proposes a question cap, with defaults for judgment slots beyond it, shown openly on the confirmation screen.

The question cap conflicts with a later decision. On 2026-09-28 the user decided that planning should continue asking until a clarity standard is met rather than stop at a fixed number of questions (`decisions.md` D07). notes/03 §5 has not been updated to reflect that.

## Applied to the incident

In the incident, the GitHub account was already in conversation memory, so the reference-repo slot was lookup-type. `gh api users/gary5876/starred` returned 28 repos and narrowed to one match, `langchain-ai/openwiki`, so no question was needed. "Which directory" was judgment-type from the start, and asking it was correct. In the loop version, filling the repo slot would then trigger reading its README for the criteria slot, and the confirmation step would show the full prompt before running.

## Open questions

- The two original open questions (catching a wrong unique lookup, and classifying slots) now have design answers (confirmation step, schema types), but neither is implemented or tested.
- Who writes slot schemas and from what evidence. The only example is a post-hoc classification of one incident.
- How to detect that the domain-identification step loaded the wrong schema.
- The question cap number and which judgment slots get defaults first (see the D07 conflict above).

## Related pages

- [Instruction Clarity Incident](instruction-clarity-incident.md): the failure this design is built from
- [Hook Enforcement](../orchestration/hook-enforcement.md): the same "structure over prompt" principle applied with Claude Code Hooks
