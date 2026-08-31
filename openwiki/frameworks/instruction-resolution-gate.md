---
type: design-proposal
title: Instruction Resolution Gate Design
description: A proposed natural-language-to-execution interpretation layer that classifies ambiguity as either lookup-resolvable or requiring user judgment, built from the instruction clarity incident, and the argument for why it must be a structural gate rather than something left to model judgment.
tags: [design, instruction-clarity, ambiguity, agent-architecture, gate]
verified:
  - by: openwiki/0.4.3
    at: 2026-08-30T15:41:00.038Z
sources:
  - id: openwiki-source-4c9b36f8ca0998a4d922aea5
    resource: repo://agent-expertise-framework/03-instruction-resolution-gate.md
generated: { by: "claude-code", at: "2026-08-30T15:41:00.038Z" }
---

## Origin

This design uses the failure recorded in [Instruction Clarity Incident](instruction-clarity-incident.md) as raw material. The user's conclusion, quoted directly: "To really use a specialized agent, you need a layer that analyzes and reassembles my natural language into a form an LLM can accept well." This page documents what that layer must do and why it cannot be left to the model's own judgment.

## Core statement

> The purpose of this layer is not "to eliminate questions," but to separate "ambiguity resolvable by lookup" from "ambiguity only the user can answer," so the former is never bounced back as a question.

## Two kinds of ambiguity

- **Lookup-resolvable ambiguity**: the answer already exists in the world and can be fixed using context the agent already holds (conversation memory, prior utterances) or tools it has access to (APIs, filesystem, web lookups). Example: "a repo starred on my GitHub" — account info plus `gh api` access is enough to resolve this by lookup.
- **Judgment-required ambiguity**: there are multiple candidates, or the answer is itself the user's preference/priority/judgment. Example: "which directory in this workspace should we clean up" — the answer is not out in the world; the user's intent is the answer.

The reason this layer needs to exist is to keep these two from being conflated. Treating lookup-resolvable ambiguity as judgment-required and bouncing it back to the user produces incidents like the one this design is built from. The reverse failure is just as real: treating judgment-required ambiguity as lookup-resolvable lets the agent arbitrarily settle it, executing work that diverges from the user's actual intent.

## Pipeline

```
User utterance
  → slot extraction (values needed to execute the request: target, scope, condition)
  → for each slot: does conversation context/memory already hold a value?
  → if not: can it be resolved via an available tool? attempt lookup
  → lookup resolves to exactly one value → execute with that value
  → lookup returns nothing or multiple candidates → generate a confirmation question grounded in those results
  → slot was never lookup-resolvable in the first place (a judgment call) → generate a confirmation question immediately
```

"Confirmation question generation" only ever happens after a lookup attempt, or for a slot that was never lookup-eligible to begin with (a judgment-required slot). There should be no structural path that reaches the question-generation step without having attempted a lookup first.

## Why this ordering cannot be left to model judgment

The initial assumption was that it would be enough to get the model to "think in this order" on its own. But revisiting the incident in [Instruction Clarity Incident](instruction-clarity-incident.md) shows that what actually happened was not "the model compared looking-up versus asking, and picked the wrong option" — it was that **the comparison itself never ran; an empty value went straight to "generate a question" reflexively**. What was skipped was not a choice between options, but the deliberation step itself.

This matters because: simply writing "follow this order this time" into the instructions for the same model does not prevent a recurrence. The step that was skipped in this incident was precisely the "thinking" step, so a design that expects the model to remember to re-check that step within its own reasoning process risks the same failure repeating.

Because of this, the layer must be built as a **structural gate, not a checklist**. For example: the action of "sending a question to the user" (a tool call) should only be executable if a record already exists showing a lookup was attempted for that slot — enforced outside the model's reasoning process. This forces the step even if the model would otherwise be inclined to skip it. That is the difference between "a layer that leaves it to judgment" and "a layer that enforces judgment."

## Applying the pipeline to the incident

- **Slot extraction**: a slot for "the repo to reference" is extracted in an unresolved state.
- **Context check**: the user's GitHub account (`gary5876`) is already in conversation memory → this slot is classified as a lookup candidate.
- **Lookup attempt**: run `gh api users/gary5876/starred`.
- **Result**: of 28 starred repos, exactly one — `langchain-ai/openwiki` — matches the "organizing documentation to be LLM-readable" description, so the slot resolves to a single value and execution proceeds. If multiple candidates had remained ambiguous instead, the pipeline would move to a confirmation question ("is it one of these?") grounded in those candidates — which is a legitimate question.

By contrast, "which directory should we clean up" is a judgment-required slot from the start, so it correctly goes straight to a confirmation question without a lookup attempt — and in the actual incident, it was handled that way. The problem was only that the two slot types were conflated, with the lookup-resolvable slot treated the same as the judgment-required one.

## Open questions (not yet answered by this design)

- How to catch a case where the lookup itself produces a wrong result (e.g., candidates narrow to one, but that one still diverges from the user's actual intent)? Over-trusting a successful lookup and proceeding without confirmation is a failure in the opposite direction.
- How to establish a general, upfront rule for classifying "is this slot lookup-resolvable" — currently this was classified after the fact based on this single incident, and no generalized rule exists yet.

## Related pages

- [Instruction Clarity Incident](instruction-clarity-incident.md) — the failure case this design is built from
- [LLM-Friendly Documentation Framework](llm-friendly-documentation.md) — the symmetric problem (writing documents explicitly for an LLM to read)
