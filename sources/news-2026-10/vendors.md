<!-- 2026-11-02 researcher 에이전트 보고 원본. 조사 범위 2026-10-01 ~ 11-02. 검증 결과는 verify-vendors.md, 정리는 notes/17. -->

# Vendor agent and orchestration news, 2026-10-01 to 2026-11-02

Baseline: notes/11 (2026-09-25). "Changes §1?" means the section 1 verdict table.

## Anthropic

**2026-10-09, Managed Agents dynamic workflows (beta)**. Release notes https://platform.claude.com/docs/en/release-notes/overview, docs https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration and https://platform.claude.com/docs/en/managed-agents/workflow-runs
New `multiagent_20261001` type. The coordinator can write a program that runs many agents in phases as a server-side "workflow run", alongside subagents and an advisor. Agents can also define "inline agents" themselves. Limits per run: 64 threads at once, 1,000 agents per run, 24-hour default lifetime, 10 open runs per session. Subagent delegation stays "one level deep" with 25 child threads. "Runs don't nest": only the primary-thread agent can start a run. Cost is capped by a session budget that pauses runs.
[inference] The hosted API now offers code-as-orchestrator, matching notes/11 section 4. A master agent still cannot delegate to department agents that themselves delegate. Depth stays 1.
Changes §1? No. Strengthens section 4 point 1. The one-level limit is reconfirmed.

**2026-10-22, "Building agents: When to fold subagents into your main agent loop"** (Diane Sarkis). https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop
Applied AI team says a single agent with progressively disclosed skills often beat subagent designs in enterprise deployments. It names subagent sprawl that mirrors "a copy of their org chart". One customer saw about 2x faster runtime with a single loop. Tool choice "tends to degrade" past 30 to 50 tool definitions. Subagents remain right for context bloat, parallel fresh-context work, or conflicting instructions.
[inference] This is the most relevant item. It argues against department-shaped agents and recommends folding them in one at a time, with end-to-end evals.
Changes §1? Strengthens rows 1 and 3 ("start single", "do not split by role"). No reversal.

**2026-10-07, pricing and models**. Same release notes URL.
Haiku 5.5 launched (1M context). Sonnet 5.5 cache reads cut from $0.20 to $0.10 per MTok. Max, Ultra and Team plans gain monthly API credits.
[inference] Cheaper worker tiers lower fan-out cost, but notes/11 cites 3 to 10x token overhead, so the ratio is unchanged.
Changes §1? No.

**2026-10-21, Claude Duet research preview**. https://claude.com/resources/articles/claude-duet
A proactive single agent on its own cloud VM (Opus 5.5) with approval gates for messages, payments, signatures and deletions.
[inference] Another product shaped as one agent plus approval gates. Changes §1? No.

Agent teams in Claude Code are still "experimental and disabled by default", with "No nested teams" (doc undated, checked 2026-11-02).

## OpenAI

**2026-10-09 and 2026-10-16, Agents API sandbox changes**. https://developers.openai.com/changelog
Sandboxes can be pre-warmed, and sandbox compute is billed only during active turns. Oct 16 added document skills and an "ultrafast" service tier.
[inference] Idle department agents cost less to keep alive on OpenAI's hosted runtime.
Changes §1? No.

**2026-10-29, Codex CLI 0.166.0**. https://learn.chatgpt.com/docs/changelog (release tag rust-v0.166.0, gh api, 2026-10-29)
"State-changing multi-agent calls" now go through Guardian review. Failed subagents no longer flag tasks as needing attention.
[inference] A vendor is adding a review gate on writes between agents. This matches the "writes in one place" rule.
Changes §1? No.

Responses API multi-agent guide is still beta (GPT-5.6 and GPT-6.1 Sol), with "no fixed limit on tree depth" and `max_concurrent_subagents` default 3. No date shown, no change found.

## Google

**2026-10-09, "Gemini at Work 2026: Introducing Gemini agent"** (Thomas Kurian). https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026
One Gemini agent that creates temporary job-specific sub-agents, each with its own identity, for runs of hours or days. It can also act as a "coworker agent" with a "persistent, defined role" and its own @agents.company.com account. The event itself is reported as 2026-10-08 [secondary]. Availability and price are not stated in the post.
[inference] Persistent role agents are the closest vendor product to "department agents". This is a product claim, not evidence that role splits work.
Changes §1? No. It is in tension with row 3 and worth watching.

**2026-10-16 (commit) and 2026-10-23 (v2.13.0), ADK Python**. https://github.com/google/adk-python/releases/tag/v2.13.0
README now says SequentialAgent, ParallelAgent and LoopAgent "are deprecated" in favor of Workflow graphs. ADK 2.0 shipped 2026-05-19, so the deprecation itself may predate the window. v2.12.0 (2026-10-13) added `require_confirmation` on workflow nodes.
[inference] Google is also moving orchestration from agent classes to explicit graphs.
Changes §1? No. Supports section 4.

Also 2026-10-22: a supervisor-router reference architecture with simulated-workload figures only, https://developers.googleblog.com/architecting-governed-self-evolving-ai-agents-on-gemini-agent-platform/ (weak evidence).

## Microsoft

**2026-10-28, Microsoft Copilot harness in Foundry Agent Service (public preview)**. https://devblogs.microsoft.com/foundry/microsoft-copilot-harness-in-foundry/ and https://blogs.microsoft.com/blog/2026/10/28/introducing-the-microsoft-copilot-harness-unlocking-the-potential-of-truly-multi-model-agentic-work/ and docs (ms.date 2026-10-29) https://learn.microsoft.com/azure/foundry/agents/how-to/use-tools-skills-copilot-harness
A managed agent loop with five harness tools, one of which is "Subagents". The docs give no depth or concurrency limits. Runtime is free until 2026-12-01, then $0.0994 per vCPU-hour and $0.0118 per GiB-hour [the pricing figures come from search summaries of the devblog and were not re-read].
[inference] All four vendors now ship a hosted single-agent harness with subagents as a tool, not a team abstraction.
Changes §1? No.

Agent Framework had only incremental releases (python 1.20 to 1.24, dotnet 1.23 to 1.27, gh api).

## Protocols

**2026-10-01, "Introducing the A2A CLI"**. https://a2a-protocol.org/latest/blog/2026/10/01/introducing-a2a-cli/
A tooling release only. The latest A2A spec release is still v1.0.1 (2026-05-28, gh api). Bloomberg joined the TSC (commit dated 2026-10-20).
MCP: no new spec revision in the window. The latest is 2026-07-28. The only blog post was the Ruby SDK reaching Tier 1 (2026-09-29).
Changes §1? No.

## Outside the window (not known to notes/11)

- OpenAI Agents API public beta, 2026-09-10 [secondary date], https://openai.com/index/introducing-the-agents-api/
- OpenAI DevDay, 2026-09-29 (Dots always-on agents), https://openai.com/index/devday-2026-recap/
- MCP spec 2026-07-28 (stateless core), https://blog.modelcontextprotocol.io/posts/2026-07-28/
- Claude Opus 5.5 (2026-09-22) and Sonnet 5.5 (2026-09-28), same release notes URL
- Undated: Claude Code workflows doc now allows `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` up to 256 and an "ultracode" mode

## Searched for and not found

- An Anthropic engineering post on orchestration (the only October post is about source control, 2026-10-13)
- An OpenAI or Microsoft orchestration guide dated in the window
- Agent teams GA, or any lift of the one-level delegation limit
- Responses multi-agent GA or new limits
- A primary source for Copilot Studio's reported 2026-10-15 "agent accounts" release (secondary only)
- Community sentiment: not searched, out of scope for this pass
