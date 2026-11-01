<!-- 2026-11-02 verifier 에이전트 보고 원본. 대상은 vendors.md의 핵심 주장. -->

# Vendor claim verification (2026-11-02)

**V1. Anthropic Managed Agents dynamic workflows: CONFIRMED**
- https://platform.claude.com/docs/en/release-notes/overview, October 9, 2026 entry: "You can now let a Claude Managed Agents agent use dynamic workflows, in beta" and the setting is `{"type": "multiagent_20261001", "workflows": {"type": "enabled"}}`.
- https://platform.claude.com/docs/en/managed-agents/workflow-runs, limits table: "Threads working at once in one run | 64" (the page adds "The API doesn't guarantee this number"), "Agents a workflow starts over the run's whole life | 1,000", "Run lifetime | 24 hours by default, or the lifetime the agent sets". Also: "An agent working in a run's thread can't start a run of its own, so runs don't nest."
- https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration: "One level: The agent can delegate to only one level of agents."
- Wording note: `multiagent_20261001` is the value of the agent's `multiagent` field, not a beta header. The beta header is still `managed-agents-2026-04-01`. Also, a run can have more than 1,000 threads because failed agents may be retried.

**V2. Anthropic "fold subagents" article: CONFIRMED (the paraphrase is slightly loose)**
- https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop, dated "October 22, 2026".
- "a single agent with skills frequently outperformed both the one-prompt-for-everything design and the subagent design on quality", based on comparisons across several enterprise deployments.
- Org chart warning: "the agent architecture becoming a copy of their org chart" (the article ties this to Conway's law).
- "once you exceed 30-50 tool definitions in the system prompt, tool choice tends to degrade."
- Minor point: the fetched summary used "skills", not "progressively disclosed skills". I did not confirm that exact phrase.

**V3. Google Gemini at Work 2026: CONFIRMED**
- https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026, dated October 9, 2026. The exact title is "Welcome to Gemini at Work 2026: Introducing the Gemini agent", not "Gemini at Work 2026: Introducing Gemini agent".
- "dynamically create a roster of sub-agents, temporary, job-specific agents, each with their own identity".
- Coworker agent: "a persistent, defined role" and "dedicated identities including their own @agents.company.com emails". The Workspace section says it "receives its own Workspace account".

**V4. OpenAI Codex CLI 0.166.0 Guardian: CONFIRMED**
- `gh api repos/openai/codex/releases/tags/rust-v0.166.0`: published_at 2026-10-29T19:47:53Z. The body lists "#57451 Route state-changing multi-agent calls through Guardian review".
- https://learn.chatgpt.com/docs/changelog dates 0.166.0 as 2026-10-29 and lists the same entry.

**V5. Microsoft Copilot harness: PARTLY REFUTED (wording)**
- https://devblogs.microsoft.com/foundry/microsoft-copilot-harness-in-foundry/, title "Introducing the Microsoft Copilot harness in Foundry Agent Service", dated "October 28th, 2026", "in public preview". These parts are confirmed.
- The phrase "Subagents as a built-in tool" does not appear. The article says agents can "delegate bounded tasks to built-in subagents" under "Execution and delegation". The substance holds, but the claim should cite that wording rather than "built-in tool".
