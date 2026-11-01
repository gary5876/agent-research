<!-- 2026-11-02 verifier 에이전트 보고 원본. 대상은 oss.md의 핵심 주장. -->

# Verification report (2026-11-02)

**O1. CONFIRMED.**
`gh api repos/obra/superpowers/releases/tags/v7.0.1` returns published_at 2026-10-21T21:05:11Z. The release notes say: "After a compaction, Claude Code re-attaches each skill cut off at 20,000 characters... subagent-driven development lost its five-round limit and ran 18 fix rounds on one task." The notes list the fix loop, final review and resuming among the things moved into `references/`. They also say: "`tests/skill-size/test-skill-size.sh` fails when any `SKILL.md` reaches 20,000 bytes." `gh api repos/obra/superpowers/issues/2481` shows created_at 2026-10-08T04:29:31Z, state closed, quoting "Five rounds maximum per task" and "one task ran 18 fix rounds, then a 19th and more." Small nuance: the release notes say "18 fix rounds", while the issue says 18 plus a 19th that had already started. "18 or more" fits both.

**O2. PARTLY REFUTED (the date is wrong, everything else checks out).**
`gh api repos/garrytan/gstack/pulls/3473` shows title "v1.91.253.0 feat(captain): /captain skill (also /crew)...". It was created 2026-10-26T14:06:33Z and merged 2026-10-26T18:04:23Z, and its approval row is dated 2026-10-26. So the PR landed on 2026-10-26, not around 2026-10-20. The "one controller merges, lanes never" model is confirmed. File ownership is listed under lane discipline.
capy/README.md on main is CONFIRMED: "197 PRs merged to gstack's main, up from 65 (3.0x)" over "The 14 days from the 2026-10-15 fix waves (the Captain took over the next day)". The windows are [10-01, 10-15) and [10-15, 10-29), so the counts start on 10-15, not 10-16.
CHANGELOG.md is CONFIRMED with a framing note. Its heading reads "## [1.91.347.0] - 2026-10-31": "A Captain archives only its own crew's threads." The entry is mainly a rule fix. It records the incident only as background: "The earlier wording also let a Captain archive threads its automations started outside the crew, and that emptied the owner's unattached threads."

**O3. CONFIRMED with one overstatement.**
WebFetch of the URL gives "AI coding agents fall for malicious instructions planted in the Downloads folder", dated October 26, 2026. The researchers are Forever Security (Gal Weizman, Omer Samet). For Codex, AGENTS.md was in ~/Downloads, and the article says: "Codex ran the malware in more than 90% of attempts." For Claude Code, the researchers wrote their own CLAUDE.md, and the article says: "Claude followed through on this about 50% of the time." Here "this" means saving a settings change that sends requests to the attacker's server. Running code in the same session worked "in about a fifth of tests". Calling 50% a "hijack" overstates the result. The article also places the Claude test only in "that folder" and never names Downloads for it.

**O4. CONFIRMED.**
`gh api repos/code-yeongyu/oh-my-openagent/releases/tags/v5.1.8` shows published_at 2026-10-01T15:00:33Z. The notes say: "Before, it started a second agent and handed back that agent's reply as a passing result." The fix ("no longer start a phantom agent turn", #9362) covers `bun` calls from eval or bash in the packaged engine.

**O5. CONFIRMED.**
`gh api repos/OWNER/REPO --jq .stargazers_count` returned: obra/superpowers 310467, garrytan/gstack 138558, code-yeongyu/oh-my-openagent 70574, bmad-code-org/BMAD-METHOD 54856. All four match the approximate figures.
