---
type: evidence-and-judgment
title: Orchestration Evidence and Design Judgment
description: External evidence on multi-agent orchestration from mostly 2023 to 2025 sources (notes/10), its re-verification against 2026 models and guides (notes/11, which wins on conflict), and the judgment notes/12 draws for the user's department-style agent organization idea.
tags: [orchestration, multi-agent, evidence, evaluation, design]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:48:28.899Z
sources:
  - id: openwiki-source-b59005f0f903d10c3bb60923
    resource: repo://decisions.md
  - id: openwiki-source-cd31a54318f348be831f2373
    resource: repo://notes/10-orchestration-evidence-2023-2025.md
  - id: openwiki-source-fd81adca3997e2dad0f5307e
    resource: repo://notes/11-orchestration-current-2026.md
  - id: openwiki-source-d62f0766d3a66d0a636a5646
    resource: repo://notes/12-orchestration-application.md
  - id: openwiki-source-c14bb42577beb1d920ff82a4
    resource: repo://notes/17-orchestration-news-2026-10.md
generated: { by: "claude-code", at: "2026-11-01T16:48:28.899Z" }
---

## Three documents, one rule

- `notes/10-orchestration-evidence-2023-2025.md` collects sources on design patterns and official guides, company-style multi-agent systems, failure modes and judge reliability, and the Claude Code execution environment. Every source carries its year and an evidence grade (peer-reviewed paper, preprint, vendor, practitioner, forum, official docs). Most pages were read through WebFetch, so quotes may differ slightly from the original, and much of the research used GPT-4 era models.
- `notes/11-orchestration-current-2026.md` re-checks each of those conclusions against 2026 guides, operating cases, and newer models. Items the main session re-read from the original carry `[재확인]` (re-verified), and items seen only through search summaries carry `[미검증]` (unverified).
- `notes/12-orchestration-application.md` applies both to the user's idea. When 10 and 11 disagree, 11 wins (`decisions.md` D10).

## What held up in 2026 (notes/11 §1)

| 2023 to 2025 conclusion | 2026 verdict |
|---|---|
| Start with a single agent | Kept. Anthropic, OpenAI, Microsoft, and LangChain all still say this |
| Multi-agent suits research and read tasks only | Updated. Coding (write) work now gets orchestrators and parallel workers, if writes are isolated by file, worktree, or VM |
| Splitting by job role is risky | Strengthened. Anthropic named splitting by kind of work as a problem in January 2026 |
| Self-correction without external signal hurts | Weakened. Some reasoning models no longer degrade |
| LLM judges favor themselves and share mistakes | Kept, with bias that differs by model |
| Expert personas do not raise accuracy | Kept, including reasoning models |
| At equal cost multi-agent does not beat single | Mostly kept, except on human-designed decomposable tasks |
| Handoffs between agents leak information | Kept on 2026 models |
| Lost in the middle of long inputs | Weakened for simple retrieval |

notes/11 §7 also lists figures that circulate but must not be cited because their sources could not be traced.

## October 2026 refresh (notes/11 section 9, notes/17)

A sweep of 2026-10-01 to 11-02, with 17 design-relevant claims re-checked against primary sources, reversed none of the verdicts above. Three got stronger and one row was added:

| Verdict | October evidence | Result |
|---|---|---|
| Start with a single agent | Anthropic, 2026-10-22: a single agent with skills often beat subagent designs in enterprise deployments | Strengthened |
| Splitting by job role is risky | The same article warns against architectures that copy the org chart. A planner, coder, reviewer pipeline cost 3.22x and solved no more (arXiv 2610.37700) | Strengthened |
| Single beats multi at equal cost | Pre-registered tau2-bench study: multi-agent worse in 12 of 13 valid cells (arXiv 2610.27655) | Strengthened |
| Handoffs leak information | LLM summaries kept at most 16.0% of recurring details, mechanical extraction 79.1% (arXiv 2610.31710) | Kept |
| Same-model supervisors oversee poorly | Hiding the worker's success report from the verifier raised recall of dangerous misreports by 13.3 to 43.4 points (arXiv 2610.29609) | Kept, with a remedy: give the verifier traces, not claims |
| New: agents can route around human approval | Planted repository context got agents to propose overly broad allow-rules in 58% of cases, and 81.0% of approved cases completed silently (arXiv 2610.22987) | Approval points must sit outside the agent's reach |
| Delegation is one level deep | Managed Agents dynamic workflows (2026-10-09) keep one-level delegation and do not nest runs | Kept |

notes/17 lists the corrections the verifiers made and the items that were not verified. The raw reports are in `sources/news-2026-10/`.

## Applied to the department idea (notes/12)

The user's starting idea was three departments (marketing, development, operations), each with five agents (planning, monitoring, production, review, documentation), under one orchestrator: about 19 LLM roles in three tiers.

notes/12 (status DRAFT) concludes:

- **The five roles are process stages, not specialties.** Planning belongs to the orchestrator and is written to a fixed form, and to code when the flow is fixed. Production stays with one agent that holds the context. Review runs mechanical checks first and gives an LLM reviewer only the spec and the output. Monitoring is rules (iteration caps, token caps, repeated-call detection) enforced by Hooks or code. Documentation is a shared store and templates, passing paths instead of summaries.
- **Splitting by department is conditionally justified**, when departments really use different tools and permissions. Adding a team-lead tier inside a department is a last resort.
- **Do not trust LLM reviewers alone.** Give them executable checks, consider a different model family, and have a person sample final quality.
- **Define roles by specification** (goal, output format, tools, boundaries) rather than titles.
- **Put more human approval in marketing and operations**, especially for publishing, pricing, discounts, budget, and hiring.

Its recommended path starts with one task in one department built as one agent with tools, measured on about 20 real requests against a same-budget single-agent baseline, and expands only when the numbers improve. Re-measure which structure can be removed whenever the model changes.

Its open questions (which task first, where the 20 evaluation cases come from) are now `decisions.md` D04 and D05.

## Related pages

- [KakaoPay Baseline](kakaopay-baseline.md): applies notes/11 and notes/12 against KakaoPay's practice
- [Master Orchestrator Research](master-orchestrator.md): the layer above
- [Orchestrator Pattern and Worker Agents](orchestrator-pattern.md): this repo's own earlier pattern
