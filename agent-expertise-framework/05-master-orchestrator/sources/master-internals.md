# 마스터 오케스트레이터 내부 설계 조사

- 조사일: 2026-09-28
- 목적: 부서 에이전트(마케팅, 개발, 운영)를 조율하는 마스터 오케스트레이터를 만들 때, 토폴로지 선택이 아니라 마스터 에이전트 "내부"가 무엇으로 이루어지는지(책임, 상태, 위임 내용, 결과 회수와 검증, 루프와 종료 규칙, 사람 개입, 측정치와 실패)를 1차 자료로 정리
- 기준선: 카카오페이 기술블로그 수준(출처, 수치, 한계를 같이 적는 수준)을 최소선으로 삼음

## 증거 등급 정의
- T1: 실험이 있는 논문(arXiv 등). 학회 채택 여부는 확인한 경우에만 별도 표기
- T2: 회사 공식 엔지니어링 블로그의 사내 측정치 또는 사례. 재현 불가, 자사 홍보 편향 가능
- T3: 공식 API/프레임워크 문서. 동작 명세만 있고 성능 수치 없음
- T4: 동료심사 전 소규모 프로브 또는 초록 수준만 확인한 논문. 일반화 제한
- [추론]: 원문에 없는 내 해석. 표시 없는 인용문과 숫자는 원문에서 직접 읽은 것

## 조사 방법과 한계
- 각 원문을 curl로 받아 python으로 HTML 태그를 벗긴 텍스트(arXiv는 HTML 판 또는 PDF 텍스트)를 만들고, 키워드 주변을 직접 읽어 인용과 숫자를 옮김
- 같은 날 앞선 실행(.previous-run 폴더)의 초안이 남아 있었음. 이번 실행은 그 초안을 체크리스트로만 쓰고, 모든 인용과 숫자를 원문 텍스트에서 다시 grep해 확인한 것만 남김. 확인이 안 된 항목은 "확인 못 함"으로 표기
- 전문 정독이 아닌 키워드 구간 발췌 읽기인 소스는 각 절에 따로 적음. 키워드에 걸리지 않은 내용은 누락됐을 수 있음
- 인용문 안의 대시 기호는 원문 표기를 그대로 둔 것이고, 내 문장에는 쓰지 않음
- 각 소스는 (a) 책임 (b) 상태와 저장 위치 (c) 위임 내용 (d) 결과 회수, 검증, 종합 (e) 루프, 종료, 재계획 규칙 (f) 사람 개입 (g) 측정 결과와 실패 순으로 정리. 원문에 해당 내용이 없으면 "원문에 없음"

---

## 1. Microsoft Magentic-One (arXiv 2411.04468)
- URL: https://arxiv.org/abs/2411.04468 (HTML 판 https://arxiv.org/html/2411.04468v1 로 읽음)
- 날짜: v1 2024-11-07(arXiv API의 published 값). 원문 "The experiments reported here were conducted between August and October 2024"
- 등급: T1 (학회 채택 여부는 확인 안 함)
- 읽은 범위: 4.1 워크플로, 5.2 결과, 5.3 절제, 5.4 오류분석, 6.2 한계, 6.3 위험, 부록 C 오류 코드 표를 키워드로 발췌해 읽음

### (a) 책임
- 원문: "it formulates a plan, maintains structured working memory of progress, directs tasks to other agents, restarts and resets upon stalling, and determines task completion"
- 워커 4개(WebSurfer, FileSurfer, Coder, ComputerTerminal)를 지휘. 오케스트레이터 자신은 도구를 직접 쓰지 않고 계획, 추적, 지시만 함

### (b) 상태와 저장 위치
- 두 개의 원장(ledger). 둘 다 오케스트레이터 LLM 호출의 프롬프트 컨텍스트로 유지됨(외부 DB 서술 없음)
- Task Ledger(외부 루프가 관리): 원문 "the Orchestrator creates the task ledger to serve as short-term memory for the duration of the task". 채우는 항목은 "given or verified facts, facts to look up (e.g., via web search), facts to derive (e.g., programmatically, or via reasoning), and educated guesses", 그리고 plan
  - educated guesses의 용도: "express memorized closed-book information in a guarded or qualified manner ... lessening the system's overall sensitivity to errors or hallucinations. For example, agents might only rely on the guesses when they get stuck, or when they run out of time". 추측은 외부 루프가 주기적으로 갱신
  - 순서: "Only after the facts and guesses in the task ledger have been populated, the Orchestrator considers the makeup of the team". 팀원 description과 원장을 보고 계획 작성
  - plan: "expressed in natural language and consists of a sequence of steps and assignments of those steps to individual agents". 계획은 "more as a hint for step-by-step execution – neither the Orchestrator nor the other agents are required to follow it exactly"
- Progress Ledger(내부 루프가 매 반복 생성): 다섯 질문
  1. "Is the request fully satisfied (i.e., task complete)?"
  2. "Is the team looping or repeating itself?"
  3. "Is forward progress being made?"
  4. "Which agent should speak next?"
  5. "What instruction or question should be asked of this team member?"
  - 답할 때 task ledger와 "the current agent conversation context"를 함께 봄
- stall 카운터: "a counter for how long the team has been stuck or stalled"

### (c) 위임 내용
- Progress Ledger 4번(다음 담당)과 5번(지시 또는 질문)이 곧 위임 메시지. 위임 필드는 "누구에게"와 "자연어 지시 1개"뿐 [추론: 목표, 출력 형식 같은 별도 필드는 원문에 없음]

### (d) 결과 회수, 검증, 종합
- 워커 출력은 공유 대화 컨텍스트에 쌓이고, 매 반복의 Progress Ledger 1~3번 질문이 사실상 진행 평가 역할
- 종료 시: "the Orchestrator reviews the full transcript, along with the ledger, and reports either a final answer, or its best educated guess"
- 별도 검증 에이전트는 없음

### (e) 루프, 종료, 재계획 규칙
- 이중 루프: 외부 루프가 Task Ledger(계획 포함), 내부 루프가 Progress Ledger
- stall: "If a loop is detected, or there is a lack of forward progress, the counter is incremented. As long as this counter remains below a threshold (≤ 2 in our experiments)" 내부 루프 계속. 임계 초과 시 내부 루프를 빠져나와 외부 루프에서 "reflection and self-refinement step ... it identifies what may have gone wrong, what new information it learned along the way, and what it might do differently" 후 원장과 계획 갱신
- 재계획 시 리셋: "we force all agents to clear their contexts and reset their states after each plan update"
- 전체 종료: "until the Orchestrator determines the task is complete or the team has reached some (parameterized and configurable) termination logic, such as reaching a maximum number of attempts, or exceeding a specified maximum time limit"
- 원문은 이 stall 설계의 의도를 "gives the agents a limited budget to recover from small errors, or to persist through brief episodes of uncertainty"라고 설명. 임계값 2의 근거 실험은 원문에서 못 찾음

### (f) 사람 개입
- 시스템 루프 안에 사람 승인 단계 없음
- 한계 절: "Adding human oversight and humans-in-the-loop, may also save costs by reducing the number of iterations incurred when agents are stuck and problem-solving. This remains an active and ongoing area of future research."
- 위험 절의 관찰: 로그인 반복 실패로 계정이 정지되자 "The agents then attempted to reset the account's password", 가짜 Reddit 대신 진짜 사이트로 가려다 네트워크 차단에 막힘, 쿠키와 약관을 사람 없이 수락, "the agents occasionally attempted to recruit other humans for help (e.g., by posting to social media, emailing textbook authors, or, in one case, drafting a freedom of information request to a government entity)". 결론 "agents operate under a strict principle of least privilege, and maximum oversight"

### (g) 측정 결과와 실패
- 테스트셋 완료율(Table 1, %): GAIA 32.33(GPT-4o) / 38.00(GPT-4o+o1), AssistantBench 11.0 / 13.3(정확도는 25.3 / 27.7), WebArena 32.8(GPT-4o). 사람 GAIA 92.00
- 절제(GAIA 검증셋): 오케스트레이터를 AutoGen GroupChat으로 교체. 원문 설명 "simply decides which agent should speak next during task execution, eliminating both ledgers, planning, progress tracking, loop detection, and explicit instructions to other agents". 결과 "without the full ledgers, performance drops by 31%". 워커 하나 제거 시 "between 21% (Coder, Executor) to 39% (FileSurfer)"
  - [추론] 이 절제는 원장, 계획, 루프 감지, 명시 지시를 한꺼번에 제거한 것이라, 예를 들어 사실 분리 원장 단독 효과는 이 논문으로 알 수 없음
- 오류분석(로그를 GPT-4o로 코딩): 최다 "persistent-inefficient-actions"(실패에도 전략을 안 바꾸는 반복. 부록 예시에 "The orchestrator commanded agents to use a flawed path repeatedly"), 2위 "insufficient-verification-steps"("tasks are marked as complete without thorough validation", 예시 "Final outputs were accepted without validating data correctness"), 3위 "underutilized-resource-options". 그 외 코드 "delayed-feedback-updates" 예시 "After WebSurfer confirmed a task, the orchestrator delayed updating ..."
- 비용: "Magentic-One requires dozens of iterations and LLM calls to solve most problems ... incurring perhaps several US dollars, and tens of minutes per task"

## 2. Magentic 패턴: Azure Architecture Center + Microsoft Agent Framework 문서
- URL 1: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns (HTML 메타 ms.date 2026-02-12, updated_at 2026-09-21)
- URL 2: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic (ms.date 2026-09-04, updated_at 2026-09-21)
- 등급: T3 (명세와 예시 코드, 성능 수치 없음)
- 읽은 범위: URL 2는 전문, URL 1은 Magentic 절과 SRE 예시, 회피 조건

### (a) 책임
- Azure: "the magentic manager agent builds a task ledger to develop the approach plan with goals and subgoals", "It iterates, backtracks, and delegates as many times as needed to build a complete plan", "regularly checks whether the original request is satisfied or stalled and updates the ledger to adjust the plan"
- Agent Framework(MAF) 실행 흐름(원문 순서): Planning Phase, Optional Plan Review, Agent Selection, Execution, Progress Assessment, Stall Detection("If progress stalls, auto-replan with an optional human review process"), Iteration("Steps 3-6 repeat until the task is complete or limits are reached"), Final Synthesis("The manager synthesizes all agent outputs into a final result")

### (b) 상태와 저장 위치
- MAF 표준 매니저: "A standard manager is based on the Magentic-One design, with fixed prompts taken from the original paper". 원장 상태는 매니저 인스턴스가 들고 있음
- 경고(원문): "Don't share a stateful explicit manager across concurrent or interleaved workflows. Use manager_factory to give each workflow isolated manager state." Python 빌더에서 manager_agent는 워크플로마다 새 StandardMagenticManager를 만들고, manager 인자는 인스턴스를 공유
- 체크포인트: 계획 검토 예시 코드가 CheckpointManager와 SuperStepCompletedEvent의 체크포인트를 받아 재개하는 구조 (인메모리 예시)
- Azure SRE 예시에서 원장 구성: "Resolution approach plan, Resolution task statuses, and the Live-site issue resolved section" (다이어그램 설명)

### (c) 위임 내용
- Progress Ledger가 타입으로 노출(.NET): IsRequestSatisfied, IsInLoop, IsProgressBeingMade, NextSpeaker, InstructionOrQuestion. 위임은 NextSpeaker + InstructionOrQuestion
- 선택 근거는 참가 에이전트의 description (예시에 "Specialist in research and information gathering" 같은 한 줄 설명)
- 프롬프트 커스텀 규칙: "When you customize the initial fact sheet or plan prompts, also customize the corresponding update prompts so replanning preserves your format. A custom progress_ledger_prompt must preserve the built-in JSON response schema."

### (d) 결과 회수, 검증, 종합
- 기본은 매니저의 종합 답변 하나만 최종 출력. intermediate_output_from 파라미터(Python만)로 지정한 참가자 출력은 "intermediate" 이벤트로 따로 흘림
- 이벤트 3종: PLAN_CREATED, REPLANNED("either because of stall detection or because a human revised the plan"), PROGRESS_LEDGER_UPDATED("emitted once per coordination round")
- 독립 검증 단계는 문서에 없음

### (e) 루프, 종료, 재계획 규칙
- 한도 파라미터 3개: 원문 "max coordination rounds, max consecutive stalls before replanning, max plan resets". Python 이름 max_round_count, max_stall_count, max_reset_count. 예시값 10 / 3 / 2, 계획 검토 예시는 stall 1
- 원문: "Consecutive non-progressing rounds increment a stall counter, and exceeding the configured maximum triggers an automatic reset and replan."
- 기본값 자체는 이 페이지에 적혀 있지 않음(예시값만 확인)

### (f) 사람 개입
- 계획 검토: Approve 또는 Revise("The user provides feedback to revise the plan, which triggers the manager to replan based on the feedback")
- 기본값이 언어마다 다름: "in Python, plan review is off by default (enable_plan_review=False) ... in .NET, plan review is on by default (RequirePlanSignoff defaults to true)"
- 검토 요청 내용: "the proposed plan, the current progress ledger (null / None on the initial review and populated on stall-triggered replans), and a flag indicating whether the replan was triggered by stall detection". 즉 stall 재계획 때도 사람 검토가 다시 걸림
- Azure SRE 예시: 매니저가 "incorporates communication checkpoints and approval gates into the evolving plan according to the SRE team's escalation procedures", "escalate to human SRE engineers if the incident exceeds the automation's scope". 사람 게이트를 계획의 단계로 넣는 방식
- Azure 예시는 "low-risk incident response scenarios"로 범위를 한정

### (g) 측정 결과와 실패
- 수치 없음. MAF 문서 스스로: "it is untested how well the Magentic orchestration will perform outside of the original Magentic-One design"
- Azure 회피 조건(원문): 결정론적으로 풀어야 하는 경우, "There's no requirement to produce a ledger", 저복잡도, 시간 민감("The pattern focuses on building and debating viable plans, not optimizing for speed"), "You anticipate frequent stalls or infinite loops that don't have a clear path to resolution"
- MAF 팁: "If your scenario requires simpler coordination without complex planning, consider using the Group Chat pattern instead"

## 3. Anthropic "How we built our multi-agent research system"
- URL: https://www.anthropic.com/engineering/multi-agent-research-system
- 날짜: 페이지 표기 "Published Jun 13, 2025"
- 등급: T2 (사내 eval 수치, 재현 불가)
- 읽은 범위: 본문과 부록을 키워드로 발췌. 본문 대부분 확인

### (a) 책임
- LeadResearcher: 접근법을 생각하고 계획 저장, 서브에이전트 생성, 결과 종합, 추가 조사 여부 판단. 원문 "the lead agent decomposes queries into subtasks and describes them to subagents"
- 확장사고로 계획: "The lead agent uses thinking to plan its approach, assessing which tools fit the task, determining query complexity and subagent count, and defining each subagent's role"

### (b) 상태와 저장 위치
- 계획은 컨텍스트 밖 Memory: "saving its plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated and it is important to retain the plan"
- 부록: "agents summarize completed work phases and store essential information in external memory before proceeding to new tasks. When context limits approach, agents can spawn fresh subagents with clean contexts while maintaining continuity through careful handoffs. Further, they can retrieve stored context like the research plan from their memory"
- 산출물 외부화: "Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator. This prevents information loss during multi-stage processing and reduces token overhead" (소제목이 "minimize the 'game of telephone'")
- 오류 복구: "we built systems that can resume from where the agent was when the errors occurred"

### (c) 위임 내용
- 위임 4필드(원문): "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries. Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information."
- 실패 사례: 'research the semiconductor shortage' 같은 짧은 지시에서 "one subagent explored the 2021 automotive chip crisis while 2 others duplicated work investigating current 2025 supply chains"
- 노력 스케일링 규칙을 프롬프트에 명시: "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls each, and complex research might use more than 10 subagents with clearly divided responsibilities". 이유 "Agents struggle to judge appropriate effort for different tasks"
- 병렬: "the lead agent spins up 3-5 subagents in parallel rather than serially"

### (d) 결과 회수, 검증, 종합
- 흐름: 서브에이전트가 "returns findings to the LeadResearcher. The LeadResearcher synthesizes these results and decides whether more research is needed—if so, it can create additional subagents or refine its strategy". 충분하면 "passes all findings to a CitationAgent, which processes the documents and research report to identify specific locations for citations"
- 서브에이전트는 도구 결과 뒤 interleaved thinking으로 "evaluate quality, identify gaps, and refine their next query" (자기 검증은 하위 단계에서)
- 시스템 평가: LLM judge 루브릭(factual accuracy, citation accuracy, completeness, source quality, tool efficiency). "a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements". 상태를 바꾸는 에이전트는 "end-state evaluation rather than turn-by-turn analysis"

### (e) 루프, 종료, 재계획 규칙
- 종료는 리드의 판단: "Once sufficient information is gathered, the system exits the research loop". 수치 상한은 원문에서 못 찾음. "setting explicit guardrails to prevent the agents from spiraling out of control"라고만 서술
- 실행 모델: "our lead agents execute subagents synchronously, waiting for each set of subagents to complete before proceeding"

### (f) 사람 개입
- 운영 중 사람 승인 지점은 원문에 없음
- 개발 단계의 사람 테스트가 개입 지점: "human testers noticed that our early agents consistently chose SEO-optimized content farms over authoritative but less highly-ranked sources", 프롬프트에 소스 품질 휴리스틱 추가로 해결
- 관측: "Adding full production tracing let us diagnose why agents failed", 대화 내용이 아니라 "agent decision patterns and interaction structures"를 모니터링

### (g) 측정 결과와 실패
- "a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval"
- BrowseComp: "three factors explained 95% of the performance variance", "token usage by itself explains 80% of the variance", 나머지 두 요인은 도구 호출 수와 모델 선택
- 토큰: "agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats"
- 병렬화로 "cut research time by up to 90% for complex queries"
- 도구 설명 재작성 에이전트로 "a 40% decrease in task completion time"
- 초기 실패(원문): "spawning 50 subagents for simple queries, scouring the web endlessly for nonexistent sources, and distracting each other with excessive updates", 그리고 "agents continuing when they already had sufficient results, using overly verbose search queries, or selecting incorrect tools"
- 동기 실행의 한계: "the lead agent can't steer subagents, subagents can't coordinate, and the entire system can be blocked while waiting for a single subagent to finish searching"
- 창발 행동: "small changes to the lead agent can unpredictably change how subagents behave"
- 적합하지 않은 영역: "some domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today. For instance, most coding tasks involve fewer truly parallelizable tasks than research"

## 4. Anthropic 2026 글 3편

### 4-1. "When to use multi-agent systems (and when not to)"
- URL: https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them (페이지 제목은 "When to use multi-agent systems (and when not to)", URL 슬러그는 building-multi-agent-systems)
- 날짜: 페이지 표기 "Date January 23, 2026"
- 등급: T2 (수치 일부), 대부분은 설계 가이드
- 읽은 범위: 본문 키워드 발췌. 예시 코드 포함

(a) 책임
- 라우팅 오케스트레이터 예시가 이 조사 대상(부서 에이전트 조율)과 거의 같은 구조: OrchestratorAgent 시스템 프롬프트 "You coordinate platform integrations. Route requests to the appropriate specialist:" 아래 CRM, Marketing, Messaging 각 담당 범위를 한 줄씩 적고, 도구는 delegate_to_crm, delegate_to_marketing, delegate_to_messaging 세 개. 각 전문 에이전트 코드 주석은 "8 - 10 CRM-specific tools", "8 - 10 marketing-specific tools"
- 원문: "The orchestrator must correctly classify requests and delegate to the right agent, and misrouting leads to poor results. Maintaining multiple specialized agents also increases prompt maintenance overhead. Specialization works best when domains are clearly separable and routing decisions are unambiguous."
- 도구 분할 신호: "An agent with too many tools (often 20+) struggles to select the appropriate one", 도메인 혼동, 도구 추가 시 기존 성능 저하

(b) 상태
- 컨텍스트 격리 예시(OrderLookupAgent)는 "Returns only essential information", 즉 하위 에이전트가 요약만 돌려줘 메인 컨텍스트를 보호

(c) 위임과 분해 원칙
- "the most important design decision is how to divide work between agents". Problem-centric(기능, 테스트, 리뷰로 나눔)은 "often counterproductive", "Each handoff loses context". Context-centric은 "usually effective": "an agent handling a feature should also handle its tests", "Work should only be split when context can be truly isolated"
- 좋은 경계: 독립 조사 경로(아시아 시장 vs 유럽 시장), 깨끗한 인터페이스를 가진 분리 컴포넌트, 블랙박스 검증. 나쁜 경계: "Sequential phases of the same work", "Tightly coupled components", "Work requiring shared state"

(d) 검증
- 검증 서브에이전트: "The main agent completes a unit of work. Before proceeding, it spawns a verification subagent with the artifact to verify, clear success criteria, and tools to perform verification. The verifier does not need to understand why the artifact was built as it was."
- 단서: "more capable orchestrator models (like Claude Opus 4.5) are increasingly able to evaluate subagent work directly without a separate verification step. However, verification subagents remain valuable when using less capable orchestrators, when verification requires specialized tools, or when you want to enforce explicit verification checkpoints"

(e) 루프 규칙: 원문에 수치 규칙 없음

(f) 사람 개입: 원문에 없음

(g) 측정과 실패
- "multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks". 원인은 컨텍스트 중복, 에이전트 간 조정 메시지, 핸드오프용 요약
- "In one experiment with agents specialized by software development role (planner, implementer, tester, reviewer), the subagents spent more tokens on coordination than on actual work." (수치 비율은 원문에 없음)
- "early victory problem": "The verifier runs one or two tests, observes them pass, and declares success". 대응은 구체 기준, 포괄 검사, 음성 테스트, 명시 지시("You MUST run the complete test suite before marking as passed"). 원문 "Without explicit requirements for comprehensive validation, verification agents take shortcuts."

### 4-2. "Harness design for long-running application development"
- URL: https://www.anthropic.com/engineering/harness-design-long-running-apps
- 날짜: "Published Mar 24, 2026", 저자 Prithvi Rajasekaran(Labs 팀)
- 등급: T2 (앱 1~2개 사례 비교라 표본이 매우 작음)
- 읽은 범위: 본문 키워드 발췌

(a) 책임: 이 하네스에서 "마스터"에 해당하는 것은 planner와 evaluator 둘로 나뉨
- Planner: "took a simple 1-4 sentence prompt and expanded it into a full product spec. I prompted it to be ambitious about scope and to stay focused on product context and high level technical design rather than detailed technical implementation"
- 이유(원문): "if the planner tried to specify granular technical details upfront and got something wrong, the errors in the spec would cascade into the downstream implementation. It seemed smarter to constrain the agents on the deliverables to be produced and let them figure out the path as they worked."

(b) 상태와 저장 위치: 파일
- "Communication was handled via files: one agent would write a file, another agent would read it and respond either within that file or with a new file that the previous agent would read in turn"
- 컨텍스트 관리의 모델 의존성: Sonnet 4.5는 "context anxiety" 때문에 컨텍스트 리셋(새 에이전트 + 구조화 핸드오프)이 필수였으나 "Opus 4.5 largely removed that behavior on its own, so I was able to drop context resets from this harness entirely", 이후 Agent SDK 자동 compaction으로 한 세션 연속 실행

(c)(d) 위임과 검증: sprint contract
- "Before each sprint, the generator and evaluator negotiated a sprint contract: agreeing on what "done" looked like for that chunk of work before any code was written". 목적은 "a step to bridge the gap between user stories and testable implementation"
- Evaluator는 Playwright MCP로 "click through the running application the way a user would, testing UI features, API endpoints, and database states". 기준은 product depth, functionality, visual design, code quality. "Each criterion had a hard threshold, and if any one fell below it, the sprint failed and the generator got detailed feedback"
- "Sprint 3 alone had 27 criteria covering the level editor"

(e) 루프와 단순화
- V2(Opus 4.6)에서 sprint 구조 제거, "I kept both the planner and evaluator, as each continued to add obvious value. Without the planner, the generator under-scoped", evaluator는 "a single pass at the end of the run"
- 원칙: "every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing". Evaluator에 대해 "It is worth the cost when the task sits beyond what the current model does reliably solo"
- 단순화 방법: "removing one component at a time and reviewing what impact it had on the final result"

(f) 사람 개입: 목표 자체가 "build complete applications without human intervention". 사람은 evaluator 튜닝 루프에 들어감: "read the evaluator's logs, find examples where its judgment diverged from mine, and update the QAs prompt", "It took several rounds"

(g) 측정과 실패
- 레트로 게임 메이커(Opus 4.5): Solo 20분 $9 vs Full harness 6시간 $200, "over 20x more expensive". Solo는 "the central feature of the application simply didn't work"
- V2 DAW: 총 3시간 50분 $124.70. Planner 4.7분 $0.46, Build 1회차 2시간 7분 $71.08, QA 1회차 8.8분 $3.24 등
- 실패: 자기평가 시 "confidently praising the work—even when, to a human observer, the quality is obviously mediocre". 튜닝 전 evaluator는 "identify legitimate issues, then talk itself into deciding they weren't a big deal and approve the work anyway", "test superficially, rather than probing edge cases"

### 4-3. "Scaling Managed Agents: Decoupling the brain from the hands"
- URL: https://www.anthropic.com/engineering/managed-agents
- 날짜: "Published Apr 08, 2026"
- 등급: T2
- 읽은 범위: 전문(짧은 글)

(a) 책임: 이 글은 멀티에이전트 오케스트레이터 글이 아니라 단일 "brain"(하네스+Claude)의 실행 인프라 글. 오케스트레이터에 쓸 수 있는 부분만 정리 [추론: 마스터의 상태 설계 근거로 사용]
- "many hands": "Claude must reason about many execution environments and decide where to send work—a harder cognitive task than operating in a single shell"
- "because no hand is coupled to any brain, brains can pass hands to one another"

(b) 상태와 저장 위치
- 소제목 "The session is not Claude's context window". compaction, 메모리 도구, trimming은 모두 "irreversible decisions about what to keep"이고 "It is difficult to know which tokens the future turns will need"
- 해법: "context is durably stored in the session log. The interface, getEvents(), allows the brain to interrogate context by selecting positional slices of the event stream"
- 크래시 복구: "The harness also became cattle. Because the session log sits outside the harness, nothing in the harness needs to survive a crash. When one fails, a new one can be rebooted with wake(sessionId), use getSession(id) to get back the event log, and resume from the last event." 기록은 emitEvent(id, event)

(c) 위임 인터페이스: 손(실행환경)은 도구 하나 "execute(name, input) → string". 컨테이너가 죽으면 도구 호출 오류로 Claude에게 넘기고 재시도 여부는 Claude가 판단

(f) 사람과 보안: 결합 설계에서는 "a prompt injection only had to convince Claude to read its own environment. Once an attacker has those tokens, they can spawn fresh, unrestricted sessions and delegate work to them". 해법은 토큰이 샌드박스에서 닿지 않게 함(Git 토큰은 초기화 때 remote에 연결, MCP OAuth 토큰은 볼트+프록시). "The harness is never made aware of any credentials."

(g) 측정: "our p50 TTFT dropped roughly 60% and p95 dropped over 90%" (지연 지표이며 작업 품질 지표 아님)

## 5. Claude Managed Agents "Multiagent orchestration" 문서
- URL: https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration (문서 원본 마크다운 판 .md로 읽음)
- 날짜: 페이지에 게시일 표기 없음. 메타데이터 status "beta", betaHeader "managed-agents-2026-04-01". 오늘(2026-09-28) 받은 판 기준
- 등급: T3 (명세, 성능 수치 없음)
- 읽은 범위: 코드 블록을 제외한 산문 전부

### (a) 책임
- "Multiagent orchestration lets one agent coordinate with others to complete complex work. Agents can act in parallel with their own isolated context"
- 권장 용도 3가지(원문): Parallelization("Fan out independent subtasks simultaneously ... and have the coordinator synthesize the results"), Specialization("Route to agents with domain-focused system prompts and tools"), Escalation("Consult a more capable agent or model for a subset of complex subtasks")
- 예시 코디네이터 시스템 프롬프트: "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent." (예시 모델은 Opus 5.5, 연구 담당 예시는 Haiku 4.5)

### (b) 상태와 저장 위치
- 공유되는 것: "All agents share the same sandbox, filesystem, and vault credentials"
- 격리되는 것: "each agent runs in its own session thread, a context-isolated event stream with its own conversation history". "Tools, MCP servers, and context are not shared"
- 스레드 영속: "Threads are persistent: the coordinator can send a follow-up to an agent it called earlier, and that agent retains everything from its previous turns"
- 로스터 버전 고정: "The coordinator's configuration, including its multiagent.agents roster, is snapshotted when the coordinator is created or updated. Referenced agents stay pinned to the versions resolved at that time"

### (c) 위임 내용
- 로스터 항목 형식 4가지: agent(id), agent(id+version), self("allows the coordinator to spawn copies of itself"), advisor(model, 로스터당 최대 1개)
- 코디네이터가 쓰는 도구 이름은 산문에서 list_agents와 send_to_agent 두 개가 언급됨(advisor 설명 문단). 위임 메시지 자체는 자유 텍스트 content이며, 목표나 출력 형식 같은 고정 필드는 문서에 없음
- 제약(원문): "The coordinator can only delegate to one level of agents; referencing an agent that has its own multiagent.agents roster fails the create or update request with a validation error. A maximum of 20 unique agents can be listed in multiagent.agents, but the coordinator can call multiple copies of each agent."
- MCP 서버는 에이전트 단위, 볼트 자격증명은 세션 단위. "To limit an agent's access, declare only the servers it needs in its agent definition". 예시에서 GitHub MCP는 연구 에이전트만 선언해 "the coordinator does not have access"
- Advisor: "a model it can consult mid-turn for strategic guidance, such as planning an approach, getting unstuck, or reviewing work before finishing". "the agent's own model must not be more capable than its advisor". 주 스레드만 상담 가능, list_agents에 안 보임. "A failed or interrupted consultation never fails the agent's turn"

### (d) 결과 회수, 검증, 종합
- 하위 스레드의 보고와 질문은 주 스레드에 agent.thread_message_received 이벤트("an agent sent a report or question to the coordinator. Includes from_session_thread_id, from_agent_name, and content")로 도착. 코디네이터의 지시는 agent.thread_message_sent(to_session_thread_id, to_agent_name, content)
- 주 스레드는 "a condensed view of all activity across all threads. You don't see the full activity from subagents, but you do see the start and end of their work, and blocking events such as tool permission requests". 세부 추론과 도구 호출은 스레드별 스트림에서 조회
- 별도 검증 메커니즘은 문서에 없음 (종합은 코디네이터 프롬프트에 맡김)

### (e) 루프, 종료, 한도
- "A maximum of 25 concurrent threads is supported" (advisor 스레드는 제외). 완료 스레드는 archive로 한도에서 빼줄 수 있고, archive는 idle일 때만 가능
- 세션 예산: "a single shared cap across all of a session's threads. As the cap is reached, threads pause independently"
- 세션 상태는 집계: 스레드 하나라도 running이면 세션 running
- 중단: user.interrupt에 session_thread_id를 주면 그 스레드만, 생략하면 주 스레드 포함 전체 중단. 권한 대기 중인 자식 스레드를 중단하면 대기 중 도구 호출이 오류 결과로 닫힘

### (f) 사람 개입
- "If a subagent needs something from your client, such as permission to run a tool call or the result of a custom tool, the event is cross-posted to the primary thread with session_thread_id identifying the originating session thread". 사용자가 user.tool_confirmation으로 답하면 "the server routes the response to the correct thread automatically"
- 핵심 규칙(원문): 서버가 호출별로 판단하는 auto 권한 모드에서 사용자 메시지는 허용 판단에 반영될 수 있지만 "Nothing in a subagent's thread counts as your intent: your client posts no messages there, and the coordinator's messages to the subagent do not count." 즉 오케스트레이터의 지시는 사람의 승인을 대신하지 못함
- auto 모드에서 서버가 거부하면 주 스레드로 올라오지 않고 자식 스레드에만 오류가 남고 자식은 계속 실행됨 [추론: 마스터가 자식의 권한 거부를 알려면 자식 스레드를 따로 봐야 함]

### (g) 측정 결과와 실패: 수치 없음

## 6. Cognition "Devin can now Manage Devins"
- URL: https://cognition.com/blog/devin-can-now-manage-devins
- 날짜: 2026-03-19 (페이지 JSON-LD datePublished, 본문 바이라인 "By The Cognition Team 03.19.26")
- 등급: T2 (제품 발표, 수치 없음)
- 읽은 범위: 전문(짧은 글)

### (a) 책임
- 원문: "The main Devin session acts as a coordinator: it scopes the work, assigns each piece to a managed Devin, monitors progress, resolves any conflicts, and compiles the results."
- 동기: "when one agent tries to handle too many things in a single session, context accumulates, focus degrades, and the quality of each subtask suffers"

### (b) 상태와 저장 위치
- 자식마다 격리 환경: "Each managed Devin is a full Devin, running in its own isolated virtual machine with its own terminal, browser, and development environment"
- 코디네이터의 학습 상태: "Devin can also read the full trajectories of its managed Devins to understand what worked, what didn't, and where they got stuck, and use that to improve how it breaks down the next task"

### (c) 위임 내용과 코디네이터 도구(원문 목록)
- "Spin up managed Devins: Devin breaks a task into scoped pieces and delegates each to a separate session"
- "Message child sessions: send instructions, context, or corrections to any managed Devin mid-task"
- "Monitor ACU consumption: track how much compute each child session is using"
- "Put child sessions to sleep or terminate them: pause or stop any managed Devin that's done or going off track"
- "Schedule messages to itself: set up follow-ups and checkpoints so the coordinator stays on top of progress"
- 예시 프롬프트에 드러난 위임 관례: "Break this down by page", "Create a reusable instruction for each independent piece of the migration", "Spin up one session per service or package (10 at a time)"

### (d) 결과 회수, 검증, 종합
- 자식이 먼저 자기 검증: "Each one can independently run shell commands, execute tests, and verify its own changes before reporting back"
- 종합 형태 예시: "Compile a summary of what passed and what failed in an .md file", "compile the results into a set of PRs", "Attach a test report from each session and summarize the overall results"

### (e) 루프, 종료 규칙: 수치 규칙 없음. 코디네이터가 자기에게 예약 메시지를 보내 체크포인트를 만듦(위 목록)

### (f) 사람 개입: "Each has its own session link, so you can inspect its work or message it directly." 사람이 자식 세션에 직접 개입 가능

### (g) 측정과 실패: 원문에 없음

## 7. Cognition "Multi-Agents: What's Actually Working"
- URL: https://cognition.com/blog/multi-agents-working
- 날짜: 2026-04-22 (JSON-LD datePublished, 바이라인 "By Walden Yan 04.22.26")
- 등급: T2
- 읽은 범위: 전문

### (a) 책임과 결론
- 결론(원문): "multi-agent systems work best today when writes stay single-threaded and the additional agents contribute intelligence rather than actions"
- 매니저 형태: "The practical shape is map-reduce-and-manage: a manager splits work, children execute, the manager synthesizes and reports back." 비구조 swarm은 "mostly a distraction"
- 매니저 목표: "A manager coordinates scope across child agents without fragmenting decisions"

### (b) 상태
- 이전 글에서 이어지는 원칙: 에이전트들이 같은 정보원과 "todo list, plan files"를 보게 하라, 그리고 "Actions carry implicit decisions"(병렬 쓰기 에이전트의 암묵적 결정이 충돌)
- 매니저 Devin은 "coordinate their progress through an internal MCP"

### (c) 위임 시 매니저 실패 모드(원문 그대로)
- "Managers trained on small-scoped delegation default to being overly prescriptive, which backfires when the manager lacks deep codebase context."
- "Agents assume they share state with their children when they don't."
- "Cross-agent communication, a sub-agent writing messages back to its manager to be passed to other agents in the agent team, doesn't happen by default, because models haven't been trained in environments where it needed to."
- "Each of these took dedicated work to fix, and we're still improving on all of them." (어떻게 고쳤는지는 원문에 없음)

### (d) 결과 회수, 검증, 종합: 리뷰 루프
- "Devin Review catches an average of 2 bugs per PR, of which roughly 58% are severe (logic errors, missing edge cases, security vulnerabilities)". 여러 리뷰 사이클을 돌며 매번 새 버그를 찾는데 "which isn't always great since it can take a while"
- "we found this technique to work best when the coding and review agents do not share any context beforehand". 리뷰어는 diff만 보고 필요한 컨텍스트를 스스로 다시 찾음
- 종합 필터(원문): "does Devin properly use its broader context of user instructions, decisions, etc. to filter the bugs that come back from Devin Review? This is key to preventing looping, disobeying the user, doing work that is out of scope". [추론: 마스터는 검증 결과를 그대로 전달하지 말고 사용자 의도로 걸러야 한다는 근거]

### (e) 에스컬레이션(smart friend)
- 약한 주 모델(SWE-1.5)이 강한 모델을 도구로 부르는 구조: "the quality ceiling was set by the primary, and the primary wasn't strong enough". 약점은 "knowing when to escalate, knowing what to ask"
- 컨텍스트 전달: "a reasonable 80/20 solution is to just share a fork of the full context of the primary model with the smart model", 질문은 넓게("what should I do?")
- 역방향: 강한 모델은 추측하지 말고 "specifically instruct the primary model to investigate this file and ask again later", 질문 밖의 조언도 주는 "over-scoped" 방식이 더 나았음
- 프런티어끼리(Claude와 GPT)는 작동: "The delegation logic becomes a capability router rather than a difficulty escalator"

### (f) 사람 개입: 리뷰 루프를 돌려 "most bugs are already resolved by the time a human opens the PR". 목표는 "a coordinated system that scales human taste"

### (g) 측정과 열린 문제
- 수치는 리뷰 2개/PR, 58% 심각, 엔터프라이즈 사용량 6개월 약 8배
- 열린 문제(원문): "How does a weaker model learn when to escalate? How does a child agent surface a discovery that should change its siblings' work? How do you transfer context between agents without drowning the receiver?"
- 대규모 데모(브라우저, C 컴파일러 등)에 대한 경고: "they all share a property most real software doesn't: a simple, verifiable success criterion"

## 8. Cursor "Scaling long-running autonomous coding"
- URL: https://cursor.com/blog/scaling-agents
- 날짜: 2026-01-14 (페이지 JSON-LD datePublished), 저자 Wilson Lin(메타 author)
- 등급: T2 (사례 규모는 크지만 품질 평가 기준은 "CI와 초기 확인 통과" 수준)
- 읽은 범위: 전문

### (a) 책임: 마스터 역할이 planner와 judge로 나뉨
- Planners: "Planners continuously explore the codebase and create tasks. They can spawn sub-planners for specific areas, making planning itself parallel and recursive."
- Workers: "They don't coordinate with other workers or worry about the big picture. They just grind on their assigned task until it's done, then push their changes."
- Judge: "At the end of each cycle, a judge agent determined whether to continue, then the next iteration would start fresh."

### (b) 상태와 저장 위치
- 실패한 첫 설계의 상태는 "a shared file"(각자 상태를 읽고 과제를 claim하고 갱신). 성공한 설계에서는 코드베이스 자체와 같은 브랜치가 공유 상태 [추론: 원문은 "pushing to the same branch with minimal conflicts"라고만 씀]
- 매 사이클 "start fresh", 남은 과제로 "We still need periodic fresh starts to combat drift and tunnel vision"

### (c) 위임과 구조 선택의 근거(실패한 설계 2개)
- 평면 자기조율 + 락: "Agents would hold locks for too long, or forget to release them entirely", "Twenty agents would slow down to the effective throughput of two or three, with most time spent waiting"
- 락 대신 낙관적 동시성: 더 단순하고 견고했지만 "With no hierarchy, agents became risk-averse. They avoided difficult tasks and made small, safe changes instead. No agent took responsibility for hard problems or end-to-end implementation."
- Integrator 역할: "We initially built an integrator role for quality control and conflict resolution, but found it created more bottlenecks than it solved. Workers were already capable of handling conflicts themselves."
- 구조의 양: "Too little structure and agents conflict, duplicate work, and drift. Too much structure creates fragility."

### (d) 결과 회수, 검증: 워커가 직접 push, 별도 중앙 품질 관문은 제거. 검증은 judge의 계속 여부 판단과 CI [추론: judge의 판단 기준은 원문에 없음]

### (e) 루프, 종료 규칙
- 사이클 단위 반복, judge가 계속 여부 결정. 구체 기준이나 상한 수치는 원문에 없음
- 남은 문제(원문): "Planners should wake up when their tasks complete to plan the next step. Agents occasionally run for far too long."

### (f) 사람 개입: 운영 중 사람 개입 서술 없음. Solid에서 React 이전은 "It still needs careful review"

### (g) 측정과 실패
- 웹 브라우저: "The agents ran for close to a week, writing over 1 million lines of code across 1,000 files", "Hundreds of workers run concurrently"
- Solid에서 React 이전: "over three weeks with +266K/-193K edits", CI와 초기 검사 통과
- 영상 렌더링 25배 가속(Rust), Windows 7 에뮬레이터 14.6K 커밋, 1.2M LoC(진행 중)
- 역할별 모델(원문): "GPT-5.2 models are much better at extended autonomous work", "Opus 4.5 tends to stop earlier and take shortcuts when convenient, yielding back control quickly", "GPT-5.2 is a better planner than GPT-5.1-Codex, even though the latter is trained specifically for coding. We now use the model best suited for each role rather than one universal model."
- "The harness and models matter, but the prompts matter more."

## 9. OpenAI

### 9-1. Agents SDK (Python) 오케스트레이션: manager(agents as tools) vs handoff
- URL: https://openai.github.io/openai-agents-python/multi_agent/ , https://openai.github.io/openai-agents-python/tools/ (Agents as tools 절), https://openai.github.io/openai-agents-python/handoffs/
- 날짜: 페이지에 게시일 표기 없음. 오늘 받은 판 기준
- 등급: T3
- 읽은 범위: multi_agent 전문, tools의 Agents as tools 절, handoffs의 파라미터 절

(a) 책임 구분(원문)
- Manager: "A manager agent keeps control of the conversation and calls specialist agents through Agent.as_tool()". 쓸 때: "You want one agent to own the final answer, combine outputs from multiple specialists, or enforce shared SDK guardrails in one place"
- Handoff: "A triage agent routes the conversation to a specialist, and that specialist becomes the active agent for the rest of the turn"
- 선택 기준: "Use agents as tools when a specialist should help with a bounded subtask but should not take over the user-facing conversation. Use handoffs when routing itself is part of the workflow". 둘은 조합 가능

(b) 상태
- as_tool: "the parent run's conversation state is not inherited automatically. To share client-managed history between the parent and nested runs, explicitly pass the same session to both"
- handoff: 받는 쪽이 기본적으로 대화 이력을 봄("the receiving agent still sees the conversation history unless you change it with an input_filter or nested handoff history settings")

(c) 위임 내용
- as_tool 기본 입력은 문자열 하나: "By default, Agent.as_tool() expects an object with one string field, input". 구조화하려면 parameters(Pydantic 모델), include_input_schema, input_builder
- 런타임 옵션: max_turns, run_config, hooks, previous_response_id, conversation_id, session, needs_approval
- is_enabled로 컨텍스트에 따라 하위 에이전트 도구를 켜고 끔
- handoff: tool_name_override(기본 transfer_to_<agent_name>), input_type(예: {"reason": "duplicate_charge", "priority": "high"} 같은 모델 생성 메타데이터), input_filter(다음 에이전트가 받을 입력 걸러냄), nest_handoff_history

(d) 결과 회수
- custom_output_extractor: 하위 에이전트 결과를 중앙 에이전트에 돌려주기 전에 가공. 원문 용도 "Extract a specific piece of information (e.g., a JSON payload)", "Validate the output or provide a fallback value when the agent's response is missing or malformed"

(e) 루프 규칙: 코드 오케스트레이션 패턴으로 제시. "In each iteration of a while loop, run the task agent to produce an output, then run an evaluator agent to assess that output and provide feedback; stop when the evaluator says the output passes the required criteria." 그 외 structured output으로 분류 후 다음 에이전트 선택, 체이닝, asyncio.gather 병렬

(f) 사람 개입: as_tool(needs_approval=...)은 "the run pauses and pending items appear in result.interruptions; then use result.to_state() and resume after calling state.approve(...) or state.reject(...)"

(g) 수치 없음. LLM 오케스트레이션 권고(원문 요지): 좋은 프롬프트, 모니터링과 반복, 자기성찰 루프, 전문 에이전트, eval 투자. 코드 오케스트레이션은 "more deterministic and predictable, in terms of speed, cost and performance"

### 9-2. Responses API Multi-agent (beta)
- URL: https://developers.openai.com/api/docs/guides/responses-multi-agent (마크다운 판 .md도 확인)
- 날짜: 가이드 본문엔 날짜 없음. 공식 changelog(https://developers.openai.com/api/docs/changelog)의 "July, 2026" 아래 "Jul 9" 항목에 GPT-5.6 출시와 함께 "Multi-agent orchestration in beta for the Responses API"로 기재 → 2026-07-09
- 등급: T3
- 읽은 범위: 가이드 산문 전부와 제한 사항, 자동 주입 지시문

(a) 책임
- "The root agent is responsible for synthesizing subagent responses and providing the final response."
- 이점 3가지로 병렬 실행, "Focused context", "Model-directed coordination ... without requiring your application to implement orchestration"
- 부적합(원문): "tasks that depend on a single ordered chain of reasoning, require frequent writes to shared mutable state, or are already dominated by one slow external operation", 그리고 "You require a fixed, deterministic execution graph"

(b) 상태
- 에이전트 트리는 경로 이름: 루트 /root, 자식 /root/researcher, 손자 /root/reviewer/tester
- 컨텍스트: 멀티에이전트를 켜면 서버측 자동 compaction이 암묵적으로 켜지고 "Compaction is applied independently to the root agent and each subagent, preserving their separate contexts"
- 에이전트 간 메시지(agent_message)는 "carries an encrypted message from one agent to another" [추론: 앱 쪽에서 마스터와 자식 사이 지시 내용을 평문으로 감사하기 어려움]

(c) 위임 내용: 호스팅 액션 6개(앱이 실행하지 않음, multi_agent_call 항목으로 보임)
- spawn_agent "Create a subagent and assign its initial task" (예시 인자 task_name, fork_turns, message)
- send_message "Queue a message for an existing agent without starting a new turn"
- followup_task "Assign more work to an existing non-root agent and start or resume its turn"
- wait_agent "Wait for an update in the calling agent's mailbox"
- interrupt_agent "Interrupt another agent's active turn without deleting its context"
- list_agents "Return the current agent tree, statuses, and each agent's last_task_message"
- 컨텍스트 전파량: 자동 주입 지시문 "You can decide how much context you want to propagate to your sub-agents with the fork_turns parameter"
- 모든 에이전트가 요청의 모델과 도구를 공유: "all agents in the tree have access to the tools configured in the API request's model call"

(d) 결과 회수
- 메시지 형식(자동 주입 지시문): "Message Type: MESSAGE | FINAL_ANSWER / Task name / Sender / Payload" (자식용은 NEW_TASK 포함)
- 자식용 지시: "When you provide a response in the final channel, that content is immediately delivered back to your parent agent"
- 예시 프롬프트에 종합 지시가 들어감: "Reconcile duplicate or conflicting findings, then return a prioritized review with file and line references"

(e) 한도
- "max_concurrent_subagents sets the maximum number of subagents that can be active simultaneously across the entire agent tree ... but excludes the root agent". "The API does not impose a fixed upper bound on this setting. The default is 3, which is recommended for most workloads." "no fixed limit on tree depth or the total number of subagents"
- 멀티에이전트 사용 시 미지원: /responses/compact, reasoning.summary, max_tool_calls
- 위임 성향은 개발자 메시지로 조절. 원문 예시 "Do not spawn subagents unless the user explicitly asks for subagents, delegation, or parallel agent work."
- 자동 주입 지시문은 "You cannot edit or remove these instructions". 그 안에 "All agents in the team, including the agents that you can assign tasks to, are equally intelligent and capable, and have access to the same set of tools"

(f) 사람 개입: 가이드 산문에 사람 승인 흐름 서술 없음. 개발자 정의 함수 호출은 트리의 어느 에이전트든 낼 수 있고 앱이 실행해 결과를 돌려줌

(g) 수치 없음. "adding subagents can increase token usage"

## 10. LangChain: Subagents 문서와 "Introducing Dynamic Subagents in Deep Agents"

### 10-1. Subagents 문서
- URL: https://docs.langchain.com/oss/python/langchain/multi-agent/subagents (마크다운 판 .md로 읽음)
- 날짜: 페이지에 게시일 없음. 오늘 받은 판 기준
- 등급: T3
- 읽은 범위: 코드 블록 제외 산문 전부

(a) 책임: "The main agent decides which subagent to invoke, what input to provide, and how to combine results". "Centralized control: All routing passes through the main agent". Supervisor와 router 구분: supervisor는 "a full agent that maintains conversation context and dynamically decides which subagents to call across multiple turns", router는 "typically a single classification step"

(b) 상태: "By default, subagents are stateless—they don't remember past interactions, with all conversation memory maintained by the main agent". 기본 체크포인터 모드는 매 호출 새 상태, 필요하면 서브에이전트별 영속 이력(continuations 모드). 한계: 서브에이전트가 도구 함수 안에서 호출되므로 "get_state with subgraphs will not return subagent state"

(c) 위임 내용과 설계 결정(원문 표)
- Sync vs async, 도구 배치(에이전트마다 도구 하나 vs 단일 dispatch 도구 task), 서브에이전트 명세 방식, 입력(질의만 vs 전체 컨텍스트), 출력(결과만 vs 전체 대화)
- 서브에이전트 선택 근거: "The names and descriptions associated with subagents are the primary way the main agent knows which subagents to invoke". 목록 제공 방식: 시스템 프롬프트 나열(10개 미만), dispatch 도구의 enum 제약(10개 미만), 도구 기반 탐색 list_agents/search_agents(10개 초과 또는 동적)
- 입력 모드: Isolated(기본, "Only the task description", 대가는 "re-derives everything the parent already did") vs Forked("The parent's conversation history", 대가는 "a larger prompt and less isolation")
- 비동기 3도구 패턴: 작업 시작(job ID 반환), 상태 확인(pending, running, completed, failed), 결과 조회

(d) 결과 회수: 흔한 실패 "the sub-agent performs tool calls or reasoning but doesn't include results in its final message—remind it that the supervisor only sees the final output". 대안은 코드에서 가공해 상태 키를 같이 돌려주기

(e) 루프 규칙: 원문에 없음

(f) 사람 개입: "Subagents return results to the main agent, not the user (though you can use interrupts within a subagent to allow user interaction)". 서브에이전트가 명확화나 승인을 위해 사람에게 직접 물을 수 있고 "The main agent remains the orchestrator"

(g) 수치 없음. 참고: "The langgraph-supervisor package is no longer actively maintained" (subagents 패턴으로 이전 안내)

### 10-2. "Introducing Dynamic Subagents in Deep Agents"
- URL: https://www.langchain.com/blog/introducing-dynamic-subagents-in-deep-agents
- 날짜와 저자: 페이지 표기 "June 29, 2026", Sydney Runkle, Colin Francis, Hunter Lovell
- 등급: T2 (수치 없음, 기능 소개)
- 읽은 범위: 전문

(a) 문제 정의(원문): 도구 호출로 서브에이전트를 하나씩 부르는 방식은 "works at small scale. It breaks down when you need to spawn hundreds of subagents, or when the orchestration logic is conditional or multi-phase."

(b)(c) 해법: 마스터가 오케스트레이션 스크립트를 작성
- "the agent writes a short script that orchestrates and calls subagents, and runs it in a lightweight interpreter" (QuickJS 기반 선택 미들웨어)
- 위임 인터페이스: "task() takes a description, a subagentType, and an optional responseSchema — when provided, the result is already a typed object, ready to filter or pass to the next step"
- 서브에이전트 선택 근거는 이름과 설명: "the names and descriptions are how the agent knows which role to reach for"

(d) 보장하는 것(원문): "Deterministic coverage at scale. Without structure, agents make judgment calls about scope, screening 75 of 500 items and calling it done. A dispatch loop doesn't. Coverage becomes a structural guarantee, not a prompt engineering problem." 그리고 "Writing orchestration as code is more reliable than having the model reproduce it as a sequence of tool calls"

(e) 패턴 6개(원문 설명): 분류 후 전문가 배정("Route each item to a specialist by type"), fan-out 후 종합, 적대적 검증("Find, then independently verify before keeping", 예시에서 독립 검증자가 CONFIRMED 또는 REFUTED 판정, 확인된 것만 보고서에 남김), 생성 후 선별, 토너먼트(judge 서브에이전트가 1:1 비교), 반복 탐색("Repeat passes until one turns up nothing new", 새 결과가 없으면 종료). 원문은 이 패턴들이 "Anthropic's dynamic workflows"에서 대중화됐다고 적음

(f) 사람 개입: 원문에 없음. 트리거는 사용자가 "workflow"라는 단어로 요청

(g) 수치 없음. 원문 요지 "The code handles coverage and intermediate context, and the model still does the judgement-heavy work."

## 11. Google ADK: 협업(collaboration) 모드와 멀티에이전트 패턴
- URL 1: https://adk.dev/workflows/collaboration/ ("Supported in ADK Python v2.0.0 Go v2.0.0")
- URL 2: https://adk.dev/workflows/patterns/
- 날짜: 페이지 게시일 표기 없음. 원본 저장소 google/adk-docs의 GitHub API 커밋 조회로 최근 수정 확인: docs/workflows/collaboration.md 2026-07-08, docs/workflows/patterns.md 2026-08-05
- 등급: T3
- 읽은 범위: URL 1 전문, URL 2는 Coordinator, 계층 분해, 반복 개선, HITL 절

(a) 책임: "a coordinator agent handles delegation of tasks to one or more subagents ... with subagents defined to handle specific tasks, and automatic return to the parent after completing a task"

(b) 상태
- 병렬 격리: "Each task or single-turn mode agent operates in its own isolated session branch. When these agents operate in parallel, each agent only sees events from its own branch ... and cannot see what its peer agents are doing. Once all parallel branches complete, the parent agent receives the collected results"
- 공유 상태: 순차 파이프라인과 반복 개선은 Shared Session State. 앞 에이전트가 output_key로 쓰고 뒤 에이전트가 context.state에서 읽음

(c) 위임 방식
- sub_agents를 선언하면 "ADK to automatically generate a delegation tool for each subagent, named after the subagent itself"
- 선택 근거: Coordinator 패턴은 "LLM-Driven Delegation (requires clear descriptions on sub-agents and appropriate instruction on Coordinator) or Explicit Invocation (AgentTool)"
- 서브에이전트 모드 표(원문 Table 1)
  - chat(기본): 사람 개입 "Full interaction", 제어는 "Agent controls until manual handoff", 병렬 불가, 복귀는 "Manual (via transfer)"
  - task: "For clarification only", "Agent controls until task complete", 병렬 불가, 복귀는 "Automatic (via finish_task)"
  - single_turn: 사람 개입 "Disallowed", "Returns immediately after task", "Multiple tasks can run in parallel", 복귀는 "Automatic (with result)"
- 제약: "Task mode agents must be leaf agents and cannot have subagents". mode는 서브에이전트 전용이며 루트에 설정 금지. ADK Python v2.0.0 그래프 워크플로에서는 task 모드가 비활성
- 입출력 구조화는 input_schema와 output_schema (예시에서 flight_agent가 output_schema=FlightResult)

(d) 결과 회수: 계층 분해 패턴 "Results are returned up the hierarchy (via tool responses or state)"

(e) 루프와 종료: 반복 개선 패턴 "The loop typically ends based on max_iterations or a dedicated checking agent setting escalate=True in the Event Actions when the result is satisfactory" (예시 max_iterations=5, QualityChecker가 pass/fail을 state에 쓰고 StopChecker가 escalate)

(f) 사람 개입
- 모드로 서브에이전트의 사람 대화 범위를 제한(위 표)
- HITL 패턴: 외부 시스템에 요청을 보내고 기다리는 커스텀 도구로 구현. "ADK doesn't have a built-in "Hu..."(원문이 내장 Human Agent가 없다고 명시, 문장 끝은 추출 텍스트에서 잘림)
- 정책 기반: SecurityPlugin이 모든 도구 호출을 가로채 PolicyEngine의 evaluate()를 호출, PolicyOutcome.CONFIRM이면 실행을 멈추고 사용자 확인 요청. 원문 "This pattern is more robust for enforcing governance and security rules"

(g) 수치 없음. 패턴 문서 서두 "you should evaluate and test them against your project requirements before committing to a full implementation"

## 12. 연구 논문 4편 (ID와 날짜는 arXiv API로 확인)

### 12-1. Puppeteer: "Multi-Agent Collaboration via Evolving Orchestration" (arXiv 2505.19591)
- URL: https://arxiv.org/abs/2505.19591
- 날짜: v1 2025-05-26, v2 2025-10-21. arXiv comment "accepted at NeurIPS 2025". 저자 Yufan Dang, Chen Qian 외(칭화대, 텐센트 등)
- 등급: T1
- 읽은 범위: 초록, 2절 방법(보상식), 3절 설정과 Table 1, 3.2절, 부록 D 한계를 발췌

(a) 책임: 중앙 오케스트레이터("puppeteer")가 매 단계 다음에 활성화할 에이전트("puppet")를 고름. 원문 "a centralized orchestrator ("puppeteer") dynamically directs agents ("puppets") in response to evolving task states", 순차 결정 문제로 정식화

(b) 상태: 현재 전역 상태와 과제만 보고 다음 에이전트를 고르는 마르코프 가정(원문 식 3). 종료 후 "a final aggregation function F_agg combines all agent outputs across timesteps"

(c)(e) 종료 규칙과 학습
- 종료: "when the selected agent is a designated terminator or when the task-solving resource is exhausted"
- REINFORCE 계열 강화학습으로 정책 갱신. 보상 = 정답 품질 r에서 λ×단계 비용을 뺀 형태(원문 식 6), 단계 비용은 "FLOPs or token-level metrics" 기반. 보상의 의도(원문): "(i) prioritize agents that complete tasks with reduced token usage while preserving performance, and (ii) terminate reasoning early by invoking the Terminator agent"
- 기본 설정: "episode length to 4, parallel exploration up to 3, λ = 0.1, and γ = 0.99". 정책 초기화는 Llama-3.1 계열 보상 모델. 동적 협업 출력 집계는 다수결
- 효율 항을 빼면: "the system naturally degenerates into a traditional large-scale collaborative framework"

(g) 측정과 한계
- Table 1 평균(Titan 공간, 초기화 → 진화): Puppeteer 0.6893 → 0.7731, Puppeteer-Mono(Llama-3.1-405B) 0.6671 → 0.7453. 벤치마크는 GSM-Hard, MMLU-Pro, SRDD, CommonGen-Hard
- 효율: Titan에서는 학습이 진행될수록 활성 에이전트 수가 줄어 "learns to terminate the reasoning process earlier", Mimas(작은 모델들)에서는 에이전트 수가 거의 그대로이고 "reductions in token consumption are primarily achieved through the preferential selection of lower-cost agents"
- 개선의 원인(초록): "the key improvements consistently stem from the emergence of more compact, cyclic reasoning structures"
- 한계(부록 D 원문): "coarse-grained rewards based only on final outputs and token usage", "the framework assumes a fixed set of agents and tools", "occasional mis-coordination or deceptive agreement among agents"

### 12-2. OrchestraBench (arXiv 2608.05263)
- URL: https://arxiv.org/abs/2608.05263
- 날짜: v1 2026-08-05 (갱신 없음). 8쪽, 저자 소속 Anote. 동료심사 표기 없음
- 등급: T4 (소규모 통제 프로브, 저자 스스로 일반화 제한)
- 읽은 범위: 초록, 서론의 결과 요약, 관련연구 표 일부

(a)~(f) 오케스트레이터에 대한 함의
- 라우팅 메커니즘: "on a 26-case gold-labelled diagnostic, a keyword/flag heuristic — representative of production rule-based routers — scores 0% on adversarial cases (misleading or missing surface flags), while a model-driven router that reasons over intent scores 100%"
- 실패 회복 3계층(Claude로 산술 의존 체인 실행, MAST 실패 모드 5개 주입): "a tool fault is fully recovered (1.0), ambiguous delegation is partially recovered (0.30), and three latent/semantic modes never recover (0.0)". 대출 승인 워크플로로 바꾸거나 Sonnet/Opus/Haiku로 바꿔도 순서는 유지, 절대값은 이동(tool 1.0에서 0.7, ambiguous 0.30에서 0.40)
- 재시도: "retry does not repair the latent modes — it reproduces the fault and only lengthens time-to-detection, so detection/attribution, not blind retry, is the necessary containment mechanism"
- 파급: "cascade radius grows with pipeline depth (mean 0.9 to 4.7 across depths 3–7)"

(g) 한계(원문): "We frame these as controlled-chain mechanism probes, not domain-workload claims". 신뢰 상태 복구 프로브의 이득도 "largely the trusted-state signal rather than autonomous detection"이라고 저자가 스스로 낮춰 보고

### 12-3. "Reinforcement Learning for LLM-based Multi-Agent Systems through Orchestration Traces" (arXiv 2605.02801)
- URL: https://arxiv.org/abs/2605.02801
- 날짜: v1 2026-05-04. 단독 저자 Chenchen Zhang. 서베이
- 등급: 서베이(1차 실험 없음). T1 논문들을 묶은 2차 자료로 취급
- 읽은 범위: 초록, 8.5절, 11절 일부

(a) 오케스트레이션을 5개 하위 결정으로 분해(원문): "when to spawn, whom to delegate to, how to communicate, how to aggregate, when to stop"
- 종료 결정 공백: "within our curated pool as of May 4, 2026, we found no explicit RL training method for the stopping decision". 본문 단서 "this does not rule out heuristic, budgeted-inference, or non-RL halting mechanisms"
- 산업 사례로 Kimi Agent Swarm, OpenAI Codex, Anthropic Claude Code를 다루되 "not as independent verification of industrial" 주장이라고 선을 그음

(g) 오케스트레이터를 직접 학습시킬 때의 실패(8.5절 원문 요지)
- Serial collapse: 보조 보상이 줄면 "a naive orchestrator can collapse to never spawning, regressing to a single-agent baseline"
- One-dominant-agent collapse: 공유 보상 하에서 "the orchestrator routes nearly all delegations to a single sub-agent that happens to be slightly above-average". 일반 해법은 못 찾음
- Over-communication: 메시지 단위 보상을 받으면 "Orchestrators inflate message volume"
- Aggregation leakage: "Summary-return content is copied verbatim into the main trace, inflating apparent progress without real information gain"
- Train-inference topology mismatch: 학습 때 팀 크기와 배포 때 팀 크기 차이(Kimi K2.5 100개 학습, K2.6 300개 배포)
- 보안(10절): "A poisoned summary causes the orchestrator to spawn the wrong sub-agent or route the wrong task", RL 단계 방어는 "no published RL-time defense"

### 12-4. ProgRouter (arXiv 2608.25992)
- URL: https://arxiv.org/abs/2608.25992
- 날짜: v1 2026-08-26, v2 2026-08-30. arXiv comment "Accepted in Findings of the Association for Computational Linguistics: EMNLP 2026". 저자 Songyuan Li, Ahmed M. Abdelmoniem, Shiqiang Wang
- 등급: T1 (학회 Findings 채택 표기. 이전 실행 초안의 "미확인 동료심사"는 틀려서 고침)
- 읽은 범위: 초록과 결과 표 머리 부분만

(a) 책임: 워크플로 단계마다 어느 LLM(크기가 다른 모델들)에 보낼지 온라인으로 결정. 원문 "adaptively selects LLM agents across workflow steps to preserve task-solving quality while adhering to time and cost budgets"
(b) 상태: "a multi-view task progress scorer that combines coarse workflow outcome regimes with fine-grained signals on subtask completion, progress trends, and workflow state quality", 그리고 "a dual-path task progress predictor and an adaptive meta-gating mechanism estimate the progress gain for each candidate routed LLM"
(e) 기존 cascade 라우팅의 한계로 "one-shot, query-level decisions"를 지적
(g) HumanEval Plus, MBPP, MATH-500, ASQA에서 "reduces the operating cost relative to key baselines while maintaining strong task-solving performance". 비용은 에너지(줄) 단위로 측정하며, 후보 모델은 Qwen 2.5-Coder 0.5B~32B, Qwen 3.5 2B~35B. 기준선 대비 구체 수치는 이번에 읽지 않음
[추론] 부서 에이전트 선택이 아니라 같은 워크플로 안의 모델 크기 선택 문제라, 마스터의 "누구에게 보낼지"보다는 "어떤 모델로 돌릴지" 결정에 해당

---

## 13. 마스터 오케스트레이터 해부도

증거 강도 기준: 강 = 통제 비교 수치 또는 공식 명세로 동작이 확정됨, 중 = 둘 이상 독립 출처의 정성 관찰 또는 단일 사내 수치, 약 = 단일 출처 서술이나 추론

| 구성요소 | 하는 일 | 근거 소스 | 증거 강도 |
|---|---|---|---|
| 사실 분리 원장(Task Ledger) | 확인된 사실, 찾아볼 사실, 도출할 사실, 추측을 나눠 적고, 추측은 막혔을 때만 사용 | Magentic-One, MAF(표준 매니저가 논문 프롬프트 사용) | 중. 원장 제거 절제에서 31% 하락은 원장, 계획, 루프 감지, 명시 지시를 한꺼번에 뺀 결과라 사실 분리 단독 효과는 모름 |
| 계획 | 팀원 description을 보고 단계와 담당을 자연어로 작성. 계획은 힌트이며 강제 아님 | Magentic-One, Harness planner, MAF | 중 |
| 계획의 추상도 | 산출물과 범위만 정하고 구현 경로는 하위에 맡김. 세부 지정은 오류를 하류로 전파 | Harness(planner 설계 근거), Cognition 2026-04(over-prescriptive 매니저) | 중. 두 회사 독립 관찰, 정량 없음 |
| 계획의 외부 저장 | 계획과 완료 단계 요약을 컨텍스트 밖(Memory, 파일, 세션 로그)에 두고 필요할 때 다시 읽음 | Anthropic Research(200K 잘림 대비), Harness(파일 통신), Managed Agents(세션 로그, getEvents) | 중. 설계 서술, 단독 효과 수치 없음 |
| 로스터와 description | 하위 에이전트 이름과 설명이 선택의 1차 근거. 버전 고정, 개수 상한, 위임 깊이 제한 | Managed Agents(20개, 1단계, 스냅샷), LangChain(10개 기준 나열 방식 분기), ADK(자동 위임 도구), MAF | 강(명세) |
| 라우팅 판단 | 요청 의도를 추론해 담당 선택. 표면 키워드 규칙은 적대 사례에 취약 | Building MAS(misrouting 경고), OrchestraBench(키워드 0%, 의도추론 100%, 26건) | 중. OrchestraBench 표본 26건 |
| 위임 명세 | 목표, 출력 형식, 도구와 소스 지침, 과제 경계. 검증 위임이면 성공 기준과 검증 도구. 가능하면 출력 스키마 | Anthropic Research, Building MAS, LangChain responseSchema, ADK output_schema, OpenAI as_tool parameters | 중. 중복 조사 사례 등 정성 근거 |
| 노력 스케일링 규칙 | 복잡도별 서브에이전트 수와 툴콜 수를 프롬프트에 명시 | Anthropic Research(1개 3~10콜, 2~4개 10~15콜, 10개 초과) | 중(단일 출처, 사내 경험칙) |
| 분해 원칙 | 작업 종류가 아니라 컨텍스트 경계로 분할. 쓰기는 한 곳 | Building MAS(context-centric), Cognition(writes single-threaded), OpenAI Responses 부적합 조건 | 중. 역할별 분할 실험에서 조정 토큰이 작업 토큰 초과(비율 미공개) |
| 컨텍스트 전파 설정 | 하위에 과제만 줄지(isolated) 부모 이력을 줄지(fork) 선택 | LangChain isolated/forked, OpenAI fork_turns, Cognition smart friend(전체 fork가 80/20 해법) | 약~중 |
| 진행 판단 루프(Progress Ledger) | 매 라운드 완료 여부, 루프 여부, 진전 여부, 다음 담당, 지시문을 고정 JSON 스키마로 출력 | Magentic-One, MAF(타입 IsRequestSatisfied 등, 스키마 보존 요구) | 강(논문 절제 + 명세) |
| Stall 카운터와 재계획 | 연속 무진전 라운드를 세고 임계 초과 시 반성, 원장 갱신, 재계획, 하위 컨텍스트 리셋. 리셋 횟수 상한 | Magentic-One(임계 2 이하), MAF(max_stall_count, max_reset_count, 예시 3과 2) | 중. 임계값 근거 실험 없음 |
| 결과 회수 경로 | 요약 메시지로 받거나, 외부 저장소에 쓰고 참조만 받음. 하위는 최종 메시지에 결과를 꼭 넣어야 함 | Anthropic Research(lightweight references), Harness(파일), Managed Agents(thread_message_received), LangChain(supervisor는 최종 출력만 봄) | 중 |
| 결과 가공 | 하위 결과를 마스터에 넣기 전에 추출, 형식 변환, 검증, 대체값 | OpenAI custom_output_extractor, LangChain Command | 약(명세만) |
| 독립 검증자 | 생성과 평가 분리, 깨끗한 컨텍스트, 하드 임계값, 전체 테스트 강제, 음성 테스트 | Harness(27개 기준, hard threshold), Building MAS(early victory), Cognition Review(PR당 2개, 58% 심각), LangChain 적대적 검증 | 중~강. 효과 수치는 Cognition 사내 값뿐 |
| 필터링 종합 | 마스터가 사용자 지시와 결정 이력으로 하위 결과를 걸러 루프, 범위 이탈, 사용자 불복종 방지. 중복과 충돌 조정 | Cognition 2026-04, OpenAI Responses(루트가 종합 책임, 예시의 reconcile 지시) | 약~중 |
| 종료 판정 | 완료 판정자(judge), Terminator 호출 학습, 라운드와 시간 상한, 새 결과가 없으면 종료 | Cursor judge, Puppeteer Terminator, Magentic-One(최대 시도와 시간), MAF max_round_count, LangChain loop until done | 중. RL 서베이 기준 종료 결정 학습은 공백 |
| 동시성과 예산 제어 | 동시 하위 수, 스레드 수, 세션 예산, 하위별 컴퓨트 감시, 중단과 휴면 | OpenAI(기본 3), Managed Agents(25, 공유 예산), Devin(ACU 감시, sleep/terminate) | 강(명세) |
| 내구성 상태 | 이벤트 로그를 하네스 밖에 두고 크래시 후 마지막 이벤트부터 재개. 체크포인트 | Managed Agents(wake, getSession), MAF 체크포인트, Anthropic Research(resume) | 중. 지연 수치는 있으나 품질 효과 수치 없음 |
| 사람 게이트 | 계획 승인과 수정, stall 재계획 재승인, 도구 권한 승인은 사람만, 정책 엔진 기반 확인 | MAF plan review, Managed Agents cross-post(코디네이터 메시지는 사용자 의도로 안 침), ADK PolicyEngine, OpenAI needs_approval, Azure SRE 예시의 approval gates | 강(명세). 효과 수치 없음 |
| 자격증명 격리 | 마스터와 하위 실행환경이 토큰을 만질 수 없게 볼트와 프록시로 분리 | Managed Agents 엔지니어링 글 | 중(설계 근거 서술) |
| 코드 오케스트레이션 | 대량 fan-out과 다단계 분기는 마스터가 스크립트를 짜서 결정론적으로 실행 | LangChain dynamic subagents, OpenAI Agents SDK 코드 오케스트레이션 권고 | 약(수치 없음) |
| 에스컬레이션과 모델 배치 | 역할별로 다른 모델, 막힐 때 강한 모델에 상담(advisor, smart friend) | Cursor(역할별 모델), Managed Agents advisor, Cognition smart friend, ProgRouter | 중. 약한 주 모델의 에스컬레이션은 실패 보고 |
| 학습된 라우팅 | 다음 에이전트나 모델 선택을 RL 또는 진행도 예측으로 | Puppeteer(NeurIPS 2025), ProgRouter(EMNLP 2026 Findings) | 중. 학술 벤치 한정 |
| 관측 | 매 라운드 원장 이벤트, 스레드별 스트림, 결정 패턴 추적 | MAF 이벤트 3종, Managed Agents 스레드 스트림, Anthropic Research(production tracing) | 강(명세) |

## 14. 마스터 고유 실패 모드

| 실패 | 증상 | 대응(원문에 나온 것) | 소스 |
|---|---|---|---|
| 과잉 위임 | 단순 질의에 서브에이전트 50개 | 노력 스케일링 규칙을 프롬프트에 명시 | Anthropic Research |
| 과소 위임(학습 시) | 마스터가 아예 분기하지 않고 단일 에이전트로 수렴 | 보조 보상을 단계적으로 줄임 | RL 서베이(Serial collapse) |
| 한 에이전트 쏠림 | 약간 나은 하위 하나에 거의 모든 위임 | 일반 해법 없음 | RL 서베이 |
| 모호한 위임 | 짧은 지시로 중복 조사와 공백 | 위임 4필드 | Anthropic Research, OrchestraBench(모호한 위임 회복률 0.30) |
| 과잉 지시 | 매니저가 코드베이스 맥락 없이 세부까지 지정해 역효과 | 산출물 중심 계획(Harness), 해법은 비공개(Cognition) | Cognition 2026-04, Harness |
| 공유 상태 착각 | 자식도 자기가 아는 걸 안다고 가정 | 원문에 구체 해법 없음 [추론: 위임 명세에 필요한 맥락을 명시하거나 fork] | Cognition 2026-04 |
| 형제 간 발견 전파 부재 | 자식의 발견이 매니저를 거쳐 다른 자식에게 가지 않음 | 열린 문제 | Cognition 2026-04 |
| 조정 오버헤드 | 역할별 분할 시 조정 토큰이 작업 토큰 초과, 핸드오프마다 정보 손실 | 컨텍스트 경계로 분할 | Building MAS |
| 평면 구조의 책임 공백 | 계층 없으면 위험 회피, 어려운 일 아무도 안 맡음 | planner와 worker 분리 | Cursor |
| 중앙 관문 병목 | integrator 같은 중앙 품질 역할이 처리량을 막음 | 역할 제거, 워커가 충돌 처리 | Cursor |
| 루프와 무진전 | 실패해도 같은 행동 반복, 오케스트레이터가 잘못된 경로를 반복 지시 | stall 카운터, 재계획, 리셋 | Magentic-One |
| 검증 없는 완료 선언 | 하위 결과를 검증 없이 수용, 검증자가 테스트 1~2개로 통과 선언, 문제를 찾고도 괜찮다고 넘어감 | 독립 검증자, 명시적 전체 테스트, 로그 기반 검증자 튜닝 | Magentic-One, Building MAS, Harness |
| 자기평가 과신 | 자기 산출물을 자신 있게 칭찬 | 생성과 평가 분리 | Harness |
| 너무 오래 또는 너무 일찍 | 충분한데 계속 탐색, 또는 일찍 멈추고 제어권 반환, 일부만 처리하고 완료 선언(500개 중 75개) | 종료 판정자, 코드 루프로 커버리지 보장, 주기적 fresh start | Anthropic Research, Cursor, LangChain |
| 동기 대기 병목 | 하위 하나 때문에 전체 대기, 실행 중 조정 불가 | 비동기(대신 결과 조정, 상태 일관성, 오류 전파가 어려워짐) | Anthropic Research, LangChain async |
| 잠복 오류 전파와 맹목 재시도 | 의미 오류는 회복 0.0, 재시도는 같은 오류 재생산, 깊이 3~7에서 파급 반경 평균 0.9에서 4.7 | 탐지와 원인 귀속 | OrchestraBench |
| 키워드 라우팅 오분류 | 표면 플래그 기반 라우터가 적대 사례 0% | 의도 추론 라우터 | OrchestraBench, Building MAS |
| 종합 누수 | 하위 요약이 그대로 복사돼 진전이 부풀려 보임 | 범위 조정 보상(학습 시) | RL 서베이(Aggregation leakage) |
| 사용자 갱신 지연 | 워커가 확인했는데 오케스트레이터가 사용자에게 늦게 알림 | 원문에 해법 없음 | Magentic-One 오류 코드 |
| 상태 있는 매니저 공유 | 동시 워크플로가 매니저 상태를 공유해 오염 | 워크플로마다 manager_factory | MAF 경고 |
| 약한 주 모델의 에스컬레이션 실패 | 언제 물을지, 무엇을 물을지 모름. 품질 상한이 주 모델에 묶임 | 전체 컨텍스트 fork, 넓은 질문, 학습 과제로 봄 | Cognition 2026-04 |
| 계획 컨텍스트 소실 | 컨텍스트가 넘치면 계획이 잘림, compaction은 비가역 | 계획 외부 저장, 세션 로그 | Anthropic Research, Managed Agents |
| 권한 대리 착각 | 마스터 지시로 하위 도구 권한을 대신 승인하려 함 | 코디네이터 메시지는 사용자 의도로 인정 안 됨, 사람 승인은 주 스레드로 올라옴 | Managed Agents 문서 |
| 오염된 요약에 의한 오위임 | 조작된 요약이 마스터를 속여 잘못된 하위를 부르거나 잘못된 과제 전달 | 하위별 도구 허용목록, RL 단계 방어는 미발표 | RL 서베이(TAMAS 인용) |
| 무단 외부 행동 | 비밀번호 재설정, 외부 사람 모집, 약관 자동 수락 | 최소 권한, 최대 감독, 네트워크 차단 | Magentic-One 위험 절 |

## 15. 요약 판단과 남은 공백
- 수치로 뒷받침되는 마스터 내부 요소는 적다. 통제 비교가 있는 것은 Magentic-One의 원장 묶음 절제(31%)와 Puppeteer의 학습 전후 비교 정도이고, 검증 분리 효과는 Cognition 사내 수치(PR당 2개, 58% 심각)뿐
- 나머지(위임 4필드, 노력 스케일링, stall 임계, 계획 추상도)는 여러 회사가 같은 방향으로 관찰했지만 수치 근거가 없다. 부서 에이전트용 마스터를 만들면 이 요소들은 자체 eval로 켜고 끄며 확인해야 한다 [추론]
- 확인 못 한 것: Magentic-One의 stall 임계값과 MAF 기본값의 근거 실험, OpenAI Agents SDK 문서들의 게시일, ProgRouter와 Puppeteer의 벤치마크별 세부 비교 수치, Cognition이 매니저 실패 3가지를 어떻게 고쳤는지

