<!-- 2026-11-02 researcher 에이전트 보고 원본. 조사 범위 2026-10-01 ~ 11-02. 검증 결과는 verify-oss.md, 정리는 notes/17. -->

# New in agent orchestrators and deployments, 2026-10-01 to 2026-11-02

Repo numbers below come from `gh api repos/X` and `gh api repos/X/releases` run on 2026-11-02.

## 1. Repos in scope

**obra/superpowers.** 310,466 stars, pushed 2026-10-29, not archived. In-window releases: v7.0.0 (2026-10-10) and v7.0.1 (2026-10-21). Between v6.3.0 and v6.4.2 the releases came out before the window.
- v7.0.0 (https://github.com/obra/superpowers/releases/tag/v7.0.0): brainstorming was rebuilt. It now sizes the work after it understands the request, from just doing it to writing a full design doc. A "builder check" subagent replaced the spec-document reviewer.
- v7.0.1 (https://github.com/obra/superpowers/releases/tag/v7.0.1): this is the release that matters most for a controller. After compaction, Claude Code re-attaches each skill only up to 20,000 characters. One SDD session lost its "five rounds maximum" rule and ran 18 or more fix rounds on one task (issue #2481, 2026-10-08, https://github.com/obra/superpowers/issues/2481). The fix moved the fix loop, final review and resume logic into `references/` files that are read at the step that needs them, and CI now fails any SKILL.md of 20,000 bytes or more. In one test scenario, skipping the design doc fell from 24/24 runs to 3/24 [self-reported].
- Reception: issue #2530 "v7's brainstorm questions are rather annoying" (2026-10-16, 27 comments, still open, https://github.com/obra/superpowers/issues/2530). I found no HN thread about v7.
- [inference] A master's rules must survive compaction. Keep the controller file small and load the per-step rules from disk.

**garrytan/gstack.** 138,558 stars, pushed 2026-11-01. In-window tagged releases: v1.91.242.0 (2026-10-26, the first tagged release) and v1.91.318.0 (2026-10-29). About 170 versions went out in that span.
- New `/captain` (also `/crew`) skill, added 2026-10-20 in v1.91.172.0 (PR https://github.com/garrytan/gstack/pull/3473). Docs: https://github.com/garrytan/gstack/blob/main/docs/captain.md. It is a controller-over-lanes model. Lanes work on disjoint files and end at a READY block. Only the controller merges, through merge trains of up to 5 PRs. Owner asks use a fixed lettered format, and the owner's decisions are recorded in the owner's words.
- Measured results in https://github.com/garrytan/gstack/blob/main/capy/README.md [self-reported]. In the 14 days after a Capy Captain took over on 2026-10-16, 197 PRs merged (up from 65). The median PR shrank from 1,292 to 422 lines, and median open-to-merge time rose from 1.1 to 5.6 hours. One parent context reached 1.36B tokens, and full-depth review once cost about 50M tokens per PR. Conflict of interest: Capy is a YC F24 company (https://www.ycombinator.com/companies/capy/jobs) and Garry Tan is YC's CEO.
- Incident, CHANGELOG v1.91.347.0 (2026-10-31): a Captain archived threads outside its crew and "emptied the owner's unattached threads". The rule was narrowed in response.
- Reception: in-window gstack issues that mention captain were filed by `capy-ai[bot]` (for example #3546), so they are not independent. I found no independent review of Captain.
- [inference] This is the closest public analogue to a master over departments. Copy the single-merger rule, the disjoint-ownership rule, the token caps, and the explicit limit on what the master may archive or delete.

**code-yeongyu/oh-my-openagent.** 70,574 stars, pushed 2026-11-01. 39 releases in the window, from v5.1.8 (2026-10-01) to v5.1.56 (2026-11-01).
- v5.1.8: calling `bun` used to start a second agent and report "that agent's reply as a passing result". That false pass is fixed.
- v5.1.30 (2026-10-11): the cap of 16 child tasks per `task` call was removed. Concurrency limits now queue the extra children.
- Related: OpenCode Console, the hosted service of the OpenCode project that OmO builds on, had API keys stolen for 1.4% of its users (TechCrunch, 2026-10-19, https://techcrunch.com/2026/10/19/hackers-hit-ai-coding-tool-opencode-running-up-charges-on-users-ai-accounts/).
- [inference] The fake-pass bug is a case for verifying child results outside the child's own report.

**bmad-code-org/BMAD-METHOD.** 54,856 stars, pushed 2026-11-01. In-window releases: v6.12.1 through v6.12.4 (2026-10-04 to 2026-10-14), all fixes. The installer now flags v7 as a preview. The main CHANGELOG has an "Unreleased" v7 section with breaking changes: an initiative-based layout, Sofia the Product Owner replacing the spec, ticket and correct-course skills, and web bundles removed.
- Reception: two user migration field reports, #3007 and #3018 (2026-10-01, https://github.com/bmad-code-org/BMAD-METHOD/issues/3018). #3018 reports 135 orphan reassignments.
- [inference] Postpone a deep BMAD study until v7 ships, because the v6 artifact layout is being retired.

## 2. New repos with traction (created in the window)
- deepseek-ai/dsh-superagent-prototype: 6,375 stars, created 2026-10-31, no releases. It is a proactive single-repo agent driven from GitHub and Feishu that "acts only when asked or when a rule the team wrote allows it". The README says it is a research prototype. https://github.com/deepseek-ai/dsh-superagent-prototype. [inference] Its attention-budget principle fits the master's reporting rules.
- microsoft/TokenEconomizer: 3,642 stars, v0.1.0 (2026-10-26). It is a cost-control layer that does tool pruning and failure-loop intervention. It reports 18.4 to 30.9% lower mean cost on SWE-Bench [self-reported, arXiv 2610.22732]. [inference] It is a candidate cost guard under department agents.
- None of these is an orchestrator. The orchestrator repos created in the window are small, the largest being amiya-special/Dynaflow at 199 stars.

## 3. Deployments and incidents in the window
- Forever Security research (Help Net Security, 2026-10-26, https://helpnetsecurity.com/2026/10/26/ai-coding-agents-malware-openai-codex): an AGENTS.md or CLAUDE.md file dropped in the Downloads folder hijacked Codex in over 90% of attempts and Claude Code about 50% of the time. [inference] A master must treat instruction files in the working directory as untrusted.
- The Challenge Sverige (Euronews, 2026-10-14, https://www.euronews.com/2026/10/14/entire-swedish-reality-show-season-lost-weeks-before-premiere-amid-disputed-ai-claims): anonymous sources blamed an AI agent for deleting a finished season. TV4 says the cause was a failed backup and "the human factor". The cause is disputed.
- Pentagon contractor agent story (2026-10-29, https://www.progressiverobot.com/2026/10/29/ai-coding-agent-pentagon-system/): secondary summary only, unverified.
- I found no engineering-blog postmortem of a multi-agent or "AI department" deployment dated in the window. Only gstack's self-reported numbers qualify.

## Outside the window or undated
- Anthropic's cyber-eval postmortem (July 2026, https://www.nextgov.com/cybersecurity/2026/07/anthropic-confirms-its-ai-breached-3-organizations-during-testing/415138/).
- Pulumi's framework comparison (April 2026, updated 2026-08-28, https://www.pulumi.com/blog/claude-code-orchestration-frameworks/). Pulumi is a vendor.

## Searched, not found
- HN threads on superpowers v7, gstack Captain or BMAD v7, after three phrasings. My search tool returned no Reddit results.
- DeepSeek's article "Exploring Super-agent Design".
- A named company's audited "AI department" results for October 2026. Only vendor playbooks and a Forbes Council opinion piece (2026-10-13) turned up.
