<!-- 2026-11-02 verifier 에이전트 보고 원본. 대상은 research.md의 핵심 주장. -->

# Verification report (checked 2026-11-02)

All six papers have no journal-ref on arXiv. R3 is the only one whose comments field claims acceptance at a venue.

**R1. 2610.27655: CONFIRMED.** https://arxiv.org/abs/2610.27655, v1 20 Oct 2026, preprint (no comments or journal-ref). Abstract: "six models from three families, over about 7,950 simulated conversations", "pre-registered with a public change log", "worse in 12 of the 13 valid cells and tied in the thirteenth", "weighted mean -28 points, 95% CI [-44, -12]". Nuance: the mean is weighted, and the 13th cell is a tie. The abstract also says one validity bar was not met.

**R2. 2610.37700: CONFIRMED, with a wording nuance.** https://arxiv.org/abs/2610.37700, v1 25 Oct 2026, preprint (comments: 16 pages, no venue). Abstract: "2430 runs of six architectures with Claude Opus 5.5 and Haiku 5.5", "costs 3.22x as much as a single strong call", "takes 3.24x as long", "solves no more tasks", "an oracle choice between the two single calls solves 94.3% of runs at half the strong call's cost per solved task". Nuance: the oracle chooses between two single calls. It is not a general router. "Half the cost" means cost per solved task compared with the strong call. The tasks come from HumanEval and ClassEval (135 tasks).

**R3. 2610.29609: CONFIRMED (self-reported acceptance).** https://arxiv.org/abs/2610.29609, v1 21 Oct 2026. The comments field says it was accepted to the ICSE 2027 Research Track. I did not check this against the ICSE program, so treat it as the authors' own statement. Abstract: "Withholding it improves trace-only dangerous-misreport recall by 43.4 percentage points" (Qwen3.5-35B-A3B) and 13.3 points for DeepSeek-284B-A13B. Nuance: these are percentage points of trace-only recall, measured on GUI-agent completion judging.

**R4. 2610.22987: CONFIRMED.** https://arxiv.org/abs/2610.22987, v1 16 Oct 2026, preprint (comments: "Preprint"). Abstract: tested "including Claude Code and Codex CLI". Agents "successfully elicit the target allow-rules in 58% of experimental instances". After approval, the exploit achieved "silent goal completion in 47 of the 58 eligible instances (81.0%)". Nuance: 81.0% is 47 of 58 instances. It is conditional on approval, not on all runs.

**R5. 2610.15459: CONFIRMED.** https://arxiv.org/abs/2610.15459, v1 11 Oct 2026, preprint (no journal-ref). Abstract: "more than 29,000 executions across 100 tasks", "Flat maintains 53.0% task success under communication faults", "compared with 3.3% and 3.2% for Sequential and Hierarchical, respectively". The abstract calls these "workflow topologies".

**R6. 2610.31710: CONFIRMED.** https://arxiv.org/abs/2610.31710 (Compact-Bench), v1 22 Oct 2026, preprint (no comments or journal-ref shown). Abstract: "Across 14 summarizer backbones" and "LLM summaries retain at most 16.0% of recurring details, compared with 79.1% for mechanical extraction". Context: this measures context compaction for long-horizon coding agents.

**R7. Scale RLI leaderboard: CONFIRMED as of today.** https://labs.scale.com/leaderboard/rli lists "Opus 5.5: 21.25" (Automation Rate, %) in rank 1, ahead of GPT 6 Astra at 20.83. The page shows no last-updated date. This is a live leaderboard, not a peer-reviewed result, and the value may change.

Method: I fetched each arXiv abstract page and the leaderboard page fresh. Every number was in an abstract, so I did not need the HTML or PDF. A small model summarized each fetch. For R4 I re-fetched the page to check whether 58% means requested or approved. The abstract says "elicit", meaning the agent got the user to be asked for the rule, and approval is a separate later step.
