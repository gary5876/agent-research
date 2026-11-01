---
type: enforcement-mechanism
title: Hook Enforcement
description: Why this project moves rules from prompts into Claude Code Hooks (notes/07), the two Hooks in the repo (the OpenWiki generated-edit block and the pre-commit check), how each is registered, the bugs found in them, and the corrections later made to notes/07's KakaoPay quotations.
tags: [hooks, enforcement, claude-code, openwiki, harness]
verified:
  - by: openwiki/0.4.3
    at: 2026-11-01T16:09:17.598Z
sources:
  - id: openwiki-source-a598baea2819500ba641fd63
    resource: repo://.claude/hooks/block-openwiki-generated-edits.py
  - id: openwiki-source-6a5607f50da1378ae0048107
    resource: repo://.claude/hooks/check-before-commit.py
  - id: openwiki-source-1fe463fcf07912e5cdbb5a91
    resource: repo://.claude/settings.json
  - id: openwiki-source-cbafbc7b849d7f2808b2ba28
    resource: repo://notes/07-harness-and-hook-enforcement.md
generated: { by: "claude-code", at: "2026-11-01T16:09:17.598Z" }
---

## The principle

`notes/07-harness-and-hook-enforcement.md` takes its thesis from the KakaoPay tech blog post on AI agents: a rule that must hold should be enforced by a Hook, which runs whenever its condition matches, rather than by a prompt, which the model may or may not follow. The project's own phrasing is "a Hook is certain, a prompt is probable." This is the same conclusion the [Instruction Resolution Gate Design](../frameworks/instruction-resolution-gate.md) reached independently: a step that depends on the model remembering to do it will eventually be skipped.

## Correction notice on notes/07

On 2026-09-27 the KakaoPay post was re-read from its original HTML (see [KakaoPay Baseline](kakaopay-baseline.md)). That pass found errors in notes/07 §1 to §4, which had been written from a WebFetch summary: the article title was wrong, the "5-stage maturity path" does not exist in the original, and the quoted "Hook execution is guaranteed, prompts are probabilistic" is not an actual sentence from it. notes/07 now opens with a correction notice and says to cite the per-post source note `sources/kakaopay/ai-agent-1.md` instead. The Hook work from §5 onward is the project's own and remains valid.

## Hook 1: block hand-edits of generated wiki content

`.claude/hooks/block-openwiki-generated-edits.py` turns the notes/04 Never rule "do not hand-edit OpenWiki output" into a structural block. It runs on every Edit, Write, and NotebookEdit call and denies any target under `openwiki/.claims/` or any `openwiki/**/*.md`.

It is registered in the committed `.claude/settings.json`, not the personal `settings.local.json`. It was first placed in the personal file and moved once it was clear the rule should bind anyone working in the repo.

Two bugs have been found and fixed:

- **cwd dependence (2026-09-05).** The registered command used a relative script path, so it broke whenever the shell's working directory had drifted from the repo root. The command now starts with `cd "$(git rev-parse --show-toplevel)"`. notes/07 §7-2 records this as evidence that a Hook's guarantee only holds if the Hook's own invocation is environment-independent.
- **No exception for OpenWiki itself (2026-11-02).** During a local OpenWiki run the host has to write each assigned page, and the Hook blocked that too. The 2026-09-06 regeneration ended with status `interrupted`, and this is a plausible reason. The Hook now allows a write only when `openwiki/.run.json` is in the `generating` phase and the target is a planned page whose job is still `pending`. Claims sidecars, generated indexes, and pages outside the plan stay blocked.

## Hook 2: run the repo lint before commits

`.claude/hooks/check-before-commit.py` matches Bash calls whose command contains `git commit`, runs `scripts/check.py`, and denies the call with the problem list if the check fails. It turns pipeline step 6 in [Repository Structure and Work Pipeline](../operations/repository-workflow.md) into a gate.

As of 2026-11-02 the script exists, but `.claude/settings.json` registers only Hook 1. Adding the Bash entry was blocked by a separate user-level hook that protects settings files until the user explicitly approves the change.

## Related pages

- [Orchestrator Pattern and Worker Agents](orchestrator-pattern.md): the supervisor role notes/07 added
- [Repository Structure and Work Pipeline](../operations/repository-workflow.md)
- [KakaoPay Baseline](kakaopay-baseline.md): where the notes/07 quotation errors were found
