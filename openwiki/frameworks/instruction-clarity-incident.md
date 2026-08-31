---
type: incident-case-study
title: "Instruction Clarity Incident: Misreading a Lookup as a Decision"
description: A recorded failure case where an agent mistook a fact it could have looked up (a starred GitHub repo, resolvable from known account plus tool access) for a decision only the user could make, asked unnecessary clarifying questions, and the instruction-writing guidance derived from it.
tags: [incident, instruction-clarity, ambiguity, agent-behavior, case-study]
verified:
  - by: openwiki/0.4.3
    at: 2026-08-30T15:41:00.038Z
sources:
  - id: openwiki-source-a9dd2f18c8a2725c73b4c52e
    resource: repo://agent-expertise-framework/02-instruction-clarity-incident.md
generated: { by: "claude-code", at: "2026-08-30T15:41:00.038Z" }
---

## Direction

Where [LLM-Friendly Documentation Framework](llm-friendly-documentation.md) addresses "how should a document be written so an LLM can read it," this page addresses the reverse direction: "how should an instruction be given so an LLM does not misjudge it," using a real recorded failure as evidence.

## The incident

The user made this request (Korean, translated): "There's an open-source repo I starred on my GitHub for organizing documentation to be LLM-readable — I'd like to reorganize the docs by referencing that."

The agent already had the user's GitHub account (`gary5876`) in memory and had a tool available (`gh api`) that could list starred repositories in a single call. Instead of running that lookup, the agent asked the user "what's the repo name?" twice — once as a structured question that failed schema validation, once as plain text. Only after the user pointed out "did you even read what I said?" did the agent run `gh api`, which succeeded on the first attempt. What blocked the agent from the start was not missing information or a missing tool — it was a misjudgment.

## Root-cause analysis

### 1. The sentence's grammatical hierarchy split "execution instruction" from "background explanation"

The request has two clauses:

- A subordinate clause (ending in the Korean connective `-는데`): "there's a repo I starred on my GitHub" — conventionally used in Korean to set up background/premise.
- A main clause (closing the sentence): "I'd like to reorganize the docs by referencing that" — the actual request.

The agent has a parsing habit of weighting the main clause heavily and treating the subordinate clause as situational background rather than something to act on. This habit is usually correct — `-는데` clauses are often genuine background. But here, the referent of the main clause's demonstrative ("that") existed only inside the subordinate clause. Once the subordinate clause was filed away as background, the reference needed to execute the main clause was buried along with it.

### 2. Without an imperative verb, the sentence was not recognized as a lookup instruction

The sentence contained no explicit lookup verb (e.g., "look it up," "check it"). From the user's perspective, saying "it's on my GitHub" already supplied the location, and since the agent already had the account info and the tool, a lookup was the obvious next step. But the agent tends to treat only clauses with an imperative verb as "executable instructions," so it failed to connect the lookup cue embedded in a descriptive sentence to an action.

### 3. A tool failure was not used as a trigger to reconsider the approach

When constructing the first question (asking for the repo name), the agent forced what should have been a free-text question into a single-option structured-question format. The tool rejected it as a schema violation. Instead of reconsidering whether the approach itself (asking the user back) was wrong, the agent discarded only that malformed question and repeated the same mistake — asking again — as plain text. A failure signal was received but did not trigger a change in strategy.

## Instruction-writing guidance derived from this incident

### 1. Put the referent of a demonstrative in the instruction clause, not the background clause

Rather than "reference that and organize it," specify how the "that" is to be resolved directly inside the instruction clause — e.g., "look it up from my starred GitHub repos and reference it." This promotes the information from the background clause into the instruction clause, so even if the agent's background/execution parsing habit stays the same, the lookup instruction is not missed.

### 2. Use distinct verbs for "look it up yourself" versus "you decide"

"Look it up / check it / verify it" means the agent should fill in the answer itself using its own tools. "Pick one / tell me" means only the user knows the answer. Making this verb distinction explicit prevents the agent from bouncing a lookup-resolvable fact back as a question.

### 3. Don't rely on the sentence to implicitly justify not repeating known information

Saying "it's on my GitHub" without naming the repo is natural between people, but an agent can easily treat "no name given" as "insufficient information." The more an execution condition matters (target identifier, location, scope), the more it should be attached directly to the command clause rather than left to flow through in a descriptive clause — e.g., "look through gary5876's GitHub stars for a documentation-format-related repo and use that" folds even the lookup starting point (the account) into the instruction clause, reducing room for misjudgment.

### 4. When multiple requests are bundled in one sentence, verify each request's completeness separately

This incident actually contained two requests: "reference the repo" (a lookup-type request) and "reorganize the docs" (a task-type request). When bundled into one sentence, the agent can easily miss one of them — especially the one buried in a subordinate clause. Splitting them into separate sentences or a numbered list raises the odds that each request is handled independently.

## Summary of causes

1. **Information misclassification**: a fact resolvable by lookup (the repo name) was misclassified as a decision requiring user judgment.
2. **Failure to use context already held**: the user account info already present in conversation memory was not connected to the lookup instruction.
3. **An unhandled exception in the Korean clause-hierarchy parsing heuristic**: the main-clause/subordinate-clause (`-는데`) parsing habit did not account for the case where the main clause's demonstrative depends on the subordinate clause.
4. **No strategy reconsideration after failure**: when the tool rejected the question, the approach itself was not reconsidered, and the same mistake (asking the user back) was repeated.

## Related pages

- [Instruction Resolution Gate Design](instruction-resolution-gate.md) — the interpretation-layer design built directly from this incident
- [LLM-Friendly Documentation Framework](llm-friendly-documentation.md) — the symmetric problem (writing documents explicitly for an LLM to read)
