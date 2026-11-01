---
status: ACTIVE
layer: 1
layer_note: "외부 출처 조사 기록"
topic: [orchestration]
date: 2026-09-25
summary: "오케스트레이션 외부 근거 모음(Anthropic, OpenAI, MS, Google, MAST 등). 주로 2023~2025년 출처, 연도 표시"
---
# 오케스트레이션 근거 모음 (주로 2023~2025년 출처)

**성격:** 조사 기록. 판단과 설계 제안은 [12-orchestration-application.md](12-orchestration-application.md)에 따로 둔다.

## 이 문서를 읽는 법

- 2026-09-25에 조사 에이전트 4개(설계 패턴, 조직형 시스템, 실패 사례, 실행 환경)가 원문을 직접 읽고 보고한 내용을 출처별로 옮겼다.
- 대부분 WebFetch로 읽었다. WebFetch는 작은 모델이 페이지를 요약해서 돌려주는 방식이라, 인용문이 원문과 한두 단어 다를 수 있다. 설계 문서에 인용할 문장은 원문에서 다시 확인한다.
- 원문 텍스트를 직접 확인한 것: OpenAI PDF(pdftotext로 추출), Microsoft 문서(원문 grep), Claude Code 공식 문서 2개(sub-agents, scheduled-tasks, 메인 세션이 직접 WebFetch로 재확인).
- 모든 출처 앞에 `[연도]`를 붙였다. 논문은 arXiv 번호 앞 네 자리가 최초 제출 연월이다(예: 2308 = 2023년 8월). 학회 게재 연도가 다르면 `[2023, 게재 2024]`처럼 둘 다 적었다. 공식 문서처럼 날짜가 없는 건 조회한 날짜를 적었다.
- **2024년 이전 자료는 GPT-4, GPT-3.5 시절 모델로 실험한 것이 많다.** 지금 모델에서도 그대로인지는 따로 확인해야 한다. 최신 확인 결과는 [11-orchestration-current-2026.md](11-orchestration-current-2026.md)에 모은다.
- 근거 등급
  - **[논문-게재]** 학회나 저널에 실린 논문
  - **[논문-프리프린트]** arXiv 등 동료 심사 전
  - **[벤더]** 회사가 자기 제품이나 자기 연구를 설명한 글. 외부 검증 없음
  - **[실무자]** 독립 실무자 글
  - **[포럼]** 이슈 트래커, 커뮤니티
  - **[공식문서]** 제품 공식 문서
- 논문 저자가 자기 시스템을 평가한 수치(MetaGPT, ChatDev 등)는 참고만 한다.

---

## A. 설계 패턴과 공식 가이드

### A-1. [2024] Anthropic, "Building effective agents" [벤더]

> **2026 현황**: 원칙은 유지. Anthropic 2026-01 글이 더 구체적으로 "일의 종류로 나누지 말고 맥락 경계로 나눠라"고 함. [11 §2-1](11-orchestration-current-2026.md)

URL: https://www.anthropic.com/engineering/building-effective-agents (2024-12-19)

- 워크플로와 에이전트를 구분한다.
  - 워크플로: "LLMs and tools are orchestrated through predefined code paths"
  - 에이전트: "LLMs dynamically direct their own processes and tool usage"
- 기본 단위는 augmented LLM(검색, 도구, 메모리를 붙인 LLM).
- 5개 패턴과 쓰는 조건
  - Prompt chaining: "task can be easily and cleanly decomposed into fixed subtasks"
  - Routing: "distinct categories that are better handled separately"
  - Parallelization(sectioning, voting): 속도를 위해 나눌 수 있거나 "multiple perspectives or attempts are needed"
  - Orchestrator-workers: "complex tasks where you can't predict the subtasks needed". 병렬화와 다른 점은 "subtasks aren't pre-defined, but determined by the orchestrator based on the specific input"
  - Evaluator-optimizer: "clear evaluation criteria, and when iterative refinement provides measurable value"
- 에이전트를 쓰지 말아야 할 때
  - "finding the simplest solution possible, and only increasing complexity when needed."
  - "optimizing single LLM calls with retrieval and in-context examples is usually enough."
  - 자율 에이전트는 "higher costs, and the potential for compounding errors". 샌드박스 테스트와 가드레일을 요구한다.
- 프레임워크에 대해: 추상화 계층이 프롬프트와 응답을 가려 디버깅을 어렵게 만든다. "start by using LLM APIs directly", "incorrect assumptions about what's under the hood are a common source of customer error."
- 3원칙: 단순성, 투명성(계획 단계를 명시적으로 보여주기), 도구 인터페이스(ACI)의 문서화와 테스트.
- "add complexity only when it demonstrably improves outcomes."

### A-2. [2025] Anthropic, "How we built our multi-agent research system" [벤더]
URL: https://www.anthropic.com/engineering/multi-agent-research-system (2025-06-13)

- 구조: orchestrator-worker. LeadResearcher가 계획을 세워 Memory에 저장하고, 병렬 하위 에이전트에게 검색을 맡기고, CitationAgent가 출처를 붙인다.
- 숫자(모두 Anthropic 내부 평가)
  - 멀티에이전트(Opus 4 리드 + Sonnet 4 하위)가 단일 Opus 4보다 90.2% 높음
  - 토큰: 에이전트는 채팅의 약 4배, 멀티에이전트는 약 15배
  - BrowseComp에서 "Token usage by itself explains 80% of the variance". 저자 표현으로 멀티에이전트는 "work mainly because they help spend enough tokens"
  - 병렬 도구 호출로 복잡한 질의의 조사 시간 최대 90% 단축
  - 도구 설명 개선으로 작업 완료 시간 40% 단축
  - 평가는 실제 사용 패턴을 대표하는 질의 약 20개로 시작
- 멀티에이전트가 맞지 않는 경우
  - "Some domains that require all agents to share the same context or involve many dependencies between agents are not a good fit for multi-agent systems today."
  - "LLM agents are not yet great at coordinating and delegating to other agents in real time."
  - 코딩은 "fewer truly parallelizable tasks than research"
  - "multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance."
- 효과가 나는 이유: 하위 에이전트가 각자 컨텍스트 창에서 병렬 탐색한 뒤 핵심만 압축해서 올림(compression). 도구, 프롬프트, 탐색 경로가 분리됨(separation of concerns).
- 오케스트레이터 프롬프트 교훈
  - 위임할 때 하위 에이전트마다 "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries"를 줘야 한다.
  - 작업 크기에 맞게 노력 조절: 단순 사실 확인은 에이전트 1개, 도구 호출 3~10회. 직접 비교는 하위 에이전트 2~4개, 각 10~15회. 복잡한 조사는 10개 초과.
  - 초기 실패: "spawning 50 subagents for simple queries", 존재하지 않는 출처를 끝없이 검색, 서로 과도한 업데이트로 방해, 지시가 모호하자("research the semiconductor shortage") 하위 에이전트끼리 같은 조사를 중복.
  - "small changes to the lead agent can unpredictably change how subagents behave"
- 운영
  - 상태가 있는 오류는 누적된다: "minor system failures can be catastrophic". 중단 지점에서 재개, 전체 트레이싱, rainbow 배포.
  - 리드가 하위 에이전트를 동기로 기다리는 병목이 있다고 밝힘.
- 정보 손실 대책: 하위 에이전트가 결과를 파일시스템이나 외부 저장소에 직접 쓰고 가벼운 참조만 넘겨서 "game of telephone"을 피함("improving both fidelity and performance"). 컨텍스트가 20만 토큰에 가까워지면 계획을 메모리에 저장. 긴 작업은 단계마다 요약을 외부 메모리에 저장.
- 평가: 채점에는 "single LLM call ... 0.0-1.0 and a pass-fail grade"가 가장 일관적. 하지만 에이전트가 SEO 콘텐츠팜을 선호하는 편향은 **사람 테스트에서만** 드러났다.

### A-3. [연도 미상] OpenAI, "A practical guide to building agents" [벤더, 원문 텍스트 직접 추출]
URL: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf (발행일 표시 없음)

- 에이전트를 만들 조건 3가지: 복잡한 의사결정, 유지보수가 어려운 규칙, 비정형 데이터 의존. "Otherwise, a deterministic solution may suffice."
- "customers typically achieve greater success with an incremental approach."
- "Our general recommendation is to maximize a single agent's capabilities first. More agents can provide intuitive separation of concepts, but can introduce additional complexity and overhead, so often a single agent with tools is sufficient."
- 나눌 신호: "When your agents fail to follow complicated instructions or consistently select incorrect tools"
  - Complex logic: if-then-else 분기가 많아 프롬프트 템플릿으로 감당이 안 될 때
  - Tool overload: 개수보다 유사성과 중복이 문제. "Some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools." 이름과 설명을 개선해도 안 될 때 나눈다.
- 나누기 전 대안: 정책 변수를 받는 단일 베이스 프롬프트(프롬프트 템플릿).
- Manager 패턴(agents as tools): 중앙 매니저가 전문 에이전트를 도구 호출로 부림. "ideal for workflows where you only want one agent to control workflow execution and have access to the user."
- Decentralized 패턴(handoff): 동등한 에이전트끼리 실행권을 넘기고 대화 상태도 함께 넘김. "optimal when you don't need a single agent maintaining central control or synthesis". 대표 용례는 triage.
- 선언형 그래프 프레임워크는 워크플로가 동적일수록 "cumbersome"해진다고 봄(코드 우선 입장).
- 사람 개입 트리거: 실패 임계치 초과(재시도 한도), 되돌릴 수 없거나 위험도가 높은 행동.

### A-4. [2026-09 조회, 문서 날짜 미표시] LangChain / LangGraph 멀티에이전트 문서 [공식문서]
- https://docs.langchain.com/oss/python/langchain/multi-agent (날짜 표시 없음)
  - 쓰는 경우: 도구가 너무 많아 잘못 고를 때, 전문 지식 컨텍스트가 클 때, 순차 제약이 필요할 때.
  - 쓰지 말 때: "Not every complex task requires this approach—a single agent with the right (sometimes dynamic) tools and prompt can often achieve similar results."
  - 패턴 5개: Subagents(메인이 하위를 도구로 호출, 모든 라우팅이 메인 경유), Handoffs(상태 변수로 활성 에이전트 전환), Skills(단일 에이전트가 전문 프롬프트를 필요할 때 로드), Router(분류 후 분배, 결과 합성), Custom workflow.
  - 문서 비교표: 단발 요청은 Subagents 4회 호출, 나머지 3회. 같은 요청 반복 시 총 호출은 Subagents 8회, Handoffs와 Skills 5회, Router 6회. 다중 도메인 비교는 Subagents와 Router 5회에 약 9K 토큰, Handoffs 7회 이상에 약 14K+, Skills 3회에 약 15K.
  - "At the center of multi-agent design is context engineering—deciding what information each agent sees."
- https://docs.langchain.com/oss/python/langchain/multi-agent/subagents
  - 하위 에이전트는 기본이 stateless이고 대화 기억은 메인이 가진다.
  - 입력 방식은 isolated(작업 설명만, 기본값)와 forked(부모 대화 기록 포함) 두 가지.
  - "the supervisor only sees the final output".
- https://github.com/langchain-ai/langgraph-supervisor-py , https://docs.langchain.com/oss/python/migrate/langgraph-supervisor
  - 계층형 예시: research팀 supervisor와 writing팀 supervisor 위에 top-level supervisor.
  - `output_mode`: `full_history`(워커 메시지 전체) 또는 `last_message`(최종 응답만).
  - 이 패키지는 "no longer actively maintained". "We now recommend using the supervisor pattern directly via tools".
  - 계층 이전 방법: 워커가 독립적이면 단일 supervisor로 평탄화. 중간 조정이 정말 필요할 때만 중간 에이전트를 도구로 감싸 중첩.
- 확인 실패: 예전 LangGraph 개념 문서(`langchain-ai.github.io/langgraph/concepts/multi_agent/`)는 리다이렉트만 돌아왔다. 예전 "network" 아키텍처 원문은 못 봤다.

### A-5. [2026] Microsoft, Azure Architecture Center "AI Agent Orchestration Patterns" [공식문서, 원문 grep 확인]
URL: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns (ms.date 2026-02-12, 업데이트 2026-09-21)

- "Use the lowest level of complexity that reliably meets your requirements."
- 복잡도 3단계
  - Direct model call: "If prompt engineering can solve the problem, you don't need an agent."
  - Single agent with tools: "Often the right default for enterprise use cases."
  - Multiagent: 프롬프트 복잡도, 도구 과부하, 보안 경계 때문에 단일 에이전트로 안 될 때만.
- "Decision-making and flow-control overhead often exceed the benefits of breaking the task into multiple agents."
- 패턴: Sequential, Concurrent, Group chat, Handoff, Magentic(매니저가 task ledger를 만들고 동적 할당). 패턴마다 "when to avoid" 목록이 있다.
  - Group chat: "consider limiting group chat orchestration to three or fewer agents."
  - maker-checker 루프(생성 에이전트와 검수 에이전트)는 group chat의 한 형태로 소개.
  - Handoff: 초기 입력만으로 담당이 정해지면 피하고 단순 dispatcher를 쓴다.
- 안티패턴
  - "Adding agents that don't provide meaningful specialization."
  - 기본 sequential, concurrent로 충분한데 복잡한 패턴을 씀
  - 다단계 hop 지연 무시
  - 동시 에이전트끼리 가변 상태 공유
  - 결정적인 작업에 비결정 패턴 사용
- 에이전트 사이에서 출력을 검증한 뒤 넘겨야 오류 연쇄를 막는다. 컨텍스트가 에이전트마다 쌓이므로 요약이나 가지치기로 압축한다.

### A-6. [2026] Google Cloud, "Choose a design pattern for your agentic AI system" [공식문서]
URL: https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system (last reviewed 2026-05-28)

- "If you're early in your agent development, we recommend that you start with a single agent".
- 패턴: single, sequential, parallel, loop, review and critique, iterative refinement, coordinator, hierarchical task decomposition, swarm, ReAct, human-in-the-loop, custom.
- Hierarchical: 모호하고 열린 문제용. "The multi-level structure adds considerable architectural complexity... significantly increases both overall latency and operational costs."
- Coordinator: "more model calls... increases token throughput, operational costs, and overall latency."
- Swarm: "the most complex and costly multi-agent pattern".

### A-7. [2025, 2026] Cognition(Devin), 반대 입장과 후속 [벤더/실무자]

> **2026 현황**: "멀티에이전트는 읽기 작업에만"은 갱신됨. 코딩에도 쓰기를 격리한 병렬 구조가 제품으로 나옴. [11 §4](11-orchestration-current-2026.md)

- [2025] "Don't Build Multi-Agents" (Walden Yan, 2025-06-12) https://cognition.com/blog/dont-build-multi-agents
  - 원칙 1: "Share context, and share full agent traces, not just individual messages"
  - 원칙 2: "Actions carry implicit decisions, and conflicting decisions carry bad results"
  - Flappy Bird 예시: 병렬 하위 에이전트가 서로의 작업을 못 봐서 하나는 마리오 배경을, 다른 하나는 어울리지 않는 새를 만들었다.
  - 권장: 단일 스레드 선형 에이전트. 컨텍스트가 넘칠 때만 별도 압축 모델로 이력 요약. "running multiple agents in collaboration only results in fragile systems"
- [2026] "Multi-Agents: What's Actually Working" (Walden Yan, 2026-04-22) https://cognition.com/blog/multi-agents-working
  - 철회가 아니라 다듬은 입장: "multi-agent systems work best today when writes stay single-threaded and the additional agents contribute intelligence rather than actions".
  - 잘 되는 패턴 3가지: Code Review Loop, Smart Friend, map-reduce-and-manage.
  - 리뷰 에이전트가 PR당 평균 2개 버그, 그중 약 58%가 심각(자사 수치, 외부 검증 없음).
  - 리뷰어와 코더가 **컨텍스트를 전혀 공유하지 않을 때** 가장 잘 됨. 모델은 같은 것을 씀.
  - 리뷰 결과는 코더가 사용자 의도에 비춰 걸러냄: "does Devin properly use its broader context ... to filter the bugs".
  - 관리자 에이전트의 문제: "overly prescriptive ... Agents assume they share state with their children when they don't".
  - 미해결: 하위 에이전트가 찾은 걸 형제 에이전트에게 전달하는 일, 받는 쪽을 압도하지 않고 컨텍스트를 넘기는 일.
- [2025] LangChain, Harrison Chase (2025-06-16) https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems [벤더]
  - 두 입장의 공통점: "Context engineering is crucial", 읽기 위주 멀티에이전트가 쓰기 위주보다 쉽다.

---

## B. 회사 조직처럼 짠 시스템

### B-0. [2026-09 조회] 레포 활동 (gh api, 2026-09-25 조회)
| 레포 | stars | 마지막 push | archived |
|---|---|---|---|
| FoundationAgents/MetaGPT | 70,603 | 2026-01-21 | false |
| OpenBMB/ChatDev | 34,392 | 2026-07-24 | false |
| crewAIInc/crewAI | 59,008 | 2026-09-25 | false |
| camel-ai/camel | 17,770 | 2026-09-20 | false |
| OpenBMB/AgentVerse | 5,142 | 2024-09-09 | false (2년째 멈춤) |

### B-1. [2023] MetaGPT [논문, 저자 자체 평가]
URL: https://arxiv.org/html/2308.00352v7 (최초 2023-08, ICLR 2024 게재로 알려짐, 확인 안 함)

- SOP를 프롬프트 순서로 넣고, 역할(PM, Architect, Project Manager, Engineer, QA)마다 정해진 양식의 문서(PRD, 시스템 설계, 인터페이스 정의)를 만들게 한다. 인계는 "대화"가 아니라 "문서"로. 공유 메시지 풀에 올리고 각 역할은 자기에게 맞는 메시지만 구독한다.
- HumanEval 85.9%, MBPP 87.7% Pass@1. 자체 SoftwareDev 데이터셋에서 ChatDev 대비 실행 가능성 3.75 vs 2.25, 사람 수정 비용 0.83 vs 2.5. 토큰은 31,255 vs 19,292로 더 씀.
- 역할 ablation: Engineer 단독 실행 가능성 1.0, 수정 10회, $0.915. +PM 2.0. +Architect 2.5. 4역할 전부 4.0, 수정 2.5회, $1.385. 역할 추가가 곧 "PRD, 설계문서 같은 중간 산출물 단계 추가"라서 둘의 효과가 분리돼 있지 않다.
- 코드를 실제로 돌려보고 고치는 실행 피드백 추가 시 HumanEval +4.2%p, MBPP +5.4%p.
- LLM을 단순히 이어 붙이면 "cascading hallucinations"가 생긴다고 씀.
- 저자가 밝힌 한계: UI와 프론트 불가, 다양한 실제 요구 충족은 여전히 어려움.

### B-2. [2023] ChatDev [논문, 저자 자체 평가]
URL: https://arxiv.org/html/2307.07924v5 (최초 2023-07)

- 역할: CEO, CTO, programmer, reviewer, tester. 설계, 코딩, 테스트 단계를 chat chain으로 잇고 각 단계는 두 에이전트 대화. "communicative dehallucination"(답하기 전에 상대에게 구체 정보를 되묻기).
- Quality: ChatDev 0.3953, GPT-Engineer 0.1419, MetaGPT 0.1523. 실행 가능성 0.88.
- ablation: 역할 제거 시 Quality 0.2212, 실행 가능성 0.58로 가장 크게 하락. dehallucination 제거 시 Quality 0.3094.
- 한계: 단순한 로직만 구현하는 경향, 요구사항이 구체적이지 않으면 과제를 이해 못함, 토큰과 시간 비용 증가.
- 주의: MetaGPT 논문에선 MetaGPT가, ChatDev 논문에선 ChatDev가 이긴다. 각자 자기 데이터셋과 지표로 잰 결과다.
- 후속: [2024] Experiential Co-Learning(ACL 2024), [2025] MacNet(ICLR 2025, DAG로 연결), [2025] "Multi-Agent Collaboration via Evolving Orchestration"(NeurIPS 2025, https://arxiv.org/abs/2505.19591). 마지막 논문은 "대부분의 접근이 정적 조직 구조에 의존해 복잡도가 커지면 적응하지 못한다"고 쓰고, RL로 학습한 중앙 오케스트레이터가 그때그때 에이전트를 골라 부르는 방식이 성능과 비용 모두 개선, 학습된 구조는 "더 작고 순환적인" 형태로 수렴했다고 보고 [논문]. ChatDev 팀 스스로 고정 조직도에서 동적 오케스트레이션으로 옮겨갔다. [2026] ChatDev 2.0(DevAll, 2026-01-07)은 노코드 멀티에이전트 오케스트레이션 플랫폼으로 전환 [벤더].

### B-3. CrewAI hierarchical(매니저 에이전트)
- [2025] Partha Sarkar, "Why CrewAI's Manager-Worker Architecture Fails and How to Fix It", Towards Data Science, 2025-11-25 [실무자] https://towardsdatascience.com/why-crewais-manager-worker-architecture-fails-and-how-to-fix-it/
  - Langfuse 트레이스 근거: "노트북 과열" 같은 순수 기술 질문에도 매니저가 기술, 청구 등 에이전트 3개를 전부 순차 호출했다. 마지막 청구 에이전트 답이 기술 답을 덮어썼다. 15,759토큰, 38초를 써서 약 200토큰짜리 답.
  - 원인: hierarchical 프로세스가 조건 분기나 진짜 위임을 강제하지 않음.
  - 해결: 매니저를 직접 정의하고 "분류, 해당 에이전트만 호출, 종료, 필요시 종합"을 단계별로 명시. 토큰 7,700~12,000으로 감소.
- 공식 문서는 매니저가 "역할과 능력에 따라 작업 배분하고 결과를 검증"한다고 설명 [벤더] https://docs.crewai.com/en/learn/hierarchical-process
- GitHub 이슈 [포럼]: #4783(2026-03, 매니저가 워커에게 위임 실패), #2054(매니저가 잘못된 도구 할당), #1399, #1823(coworker not found), #3925(언어에 따라 동작이 다름). 모두 closed. 현재 버전 재현 여부는 확인 안 함.

### B-4. [2023~2024] AgentVerse, CAMEL, 조직 구조 연구 [논문]
- [2023] AgentVerse https://arxiv.org/html/2308.10848
  - 수직(리더가 최종 결정) 구조는 수학, 소프트웨어처럼 정답 하나가 필요한 과제에, 수평(합의) 구조는 컨설팅, 도구 사용에 적합.
  - GPT-3.5 그룹은 수학 추론에서 단독보다 못했고, 오답의 약 10%는 맞게 풀던 에이전트가 다른 에이전트의 틀린 피드백에 휩쓸려 생김(GPT-4에선 관찰 안 됨).
  - Minecraft 실험에서 효율을 위해 다른 에이전트를 공격하거나 마을 도서관을 부수는 행동 보고.
- [2023] CAMEL https://arxiv.org/abs/2303.17760: 역할극 협업에서 역할 뒤바뀜, 지시 반복, 불량 응답, 무한 루프가 주요 문제.
- [2024] "Embodied LLM Agents Learn to Cooperate in Organized Teams" https://arxiv.org/abs/2403.12482: 에이전트가 과보고하고 아무 지시나 따르는 경향 때문에 정보 중복과 혼란. 지정 리더가 효율을 높였고, Criticize-Reflect로 조직 프롬프트를 개선하니 통신 비용 감소(초록 수준만 확인).

### B-5. 직함과 페르소나가 성능을 올리나

> **2026 재검증**: 여전히 성립. o3-mini, o4-mini 같은 추론 모델도 효과 없음. [11 §5-3](11-orchestration-current-2026.md)

- [2023, 게재 2024] 부정: "When 'A Helpful Assistant' Is Not Really Helpful" (EMNLP 2024 Findings) [논문-게재] https://arxiv.org/abs/2311.10054. 페르소나 162개, 모델 계열 4개, 사실 질문 2,410개. 시스템 프롬프트 페르소나는 무페르소나 대비 향상 없음. 질문별 최적 페르소나를 사후에 고르면 좋아지지만 자동 선택은 어려움.
- [2025] 부정: Wharton "Playing Pretend: Expert Personas Don't Improve Factual Accuracy" (2025-12) [논문-프리프린트] https://arxiv.org/abs/2512.05858. 모델 6개, GPQA Diamond, MMLU-Pro. 도메인이 맞는 전문가 페르소나도 유의미한 효과 없음(Gemini 2.0 Flash 예외). 도메인이 안 맞으면 가끔 저하. 저자 권고는 페르소나보다 과제별 지시, 예시, 평가 워크플로에 투자.
- [2023, 게재 2024] 긍정: "Better Zero-Shot Reasoning with Role-Play Prompting" (NAACL 2024) [논문-게재] https://arxiv.org/abs/2308.07702. ChatGPT AQuA 53.5%에서 63.8%. 저자 해석은 역할극이 단계적 추론을 잘 유도하는 트리거라는 것. 2023년 ChatGPT 기준.
- [2026] 혼합: "When Does Persona Prompting Actually Help?" (arXiv 2605.29420) [논문-프리프린트]. 과제와 지표에 따라 돕기도 해치기도 함. 요약만 봤고 수치는 못 봄.

### B-6. "AI 회사/부서" 실제 운영 사례
- [2025] Anthropic Project Vend 2단계 (2025-12-18) [벤더, 실제 운영된 매장] https://www.anthropic.com/research/project-vend-2
  - 점장 에이전트 Claudius, CEO 에이전트 Seymour Cash(OKR 도구 보유), 굿즈 담당 Clothius.
  - CEO 도입 후 할인 약 80% 감소, 무료 제공 절반. 하지만 "Seymour authorized such requests about eight times as often as it denied them", "the business started to make money may have been in spite of the CEO, rather than because of it". 이유는 "the same underlying model"이라 CEO가 점장과 같은 결함과 맹점을 공유했기 때문. 밤에는 둘이 "ETERNAL TRANSCENDENCE INFINITE COMPLETE" 같은 잡담을 함.
  - 효과가 있던 것: 가격과 배송일을 도구로 확인하게 강제한 절차("we rediscovered that bureaucracy matters"), 담당 상품 영역을 명확히 나눈 역할 분리(Clothius).
- [2024, 게재 2025] TheAgentCompany (CMU 등, NeurIPS 2025 D&B) [논문-게재] https://arxiv.org/abs/2412.14161
  - 가상 회사 환경(GitLab, RocketChat, ownCloud, Plane). 최고 에이전트가 과제의 약 30% 완료(논문 시점). **2026 기준 리더보드 검증 1위는 42.86%(2025-11), 2026년 유효 등재 없음. 11 §6-1**
  - 개발 과제는 상대적으로 잘하고 행정, 재무, 데이터 과제가 가장 어려움(저자 가설: 이런 데이터는 사내 비공개라 학습이 부족).
  - 담당자를 못 찾자 다른 사용자 이름을 바꿔 "해결한 척"한 사례.
- [2025] Gartner (2025-06-25) [애널리스트 예측] https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027: 2027년 말까지 에이전틱 AI 프로젝트 40% 이상 취소 예측.
- 마케팅 부서형 실사례: "AI marketing team multi-agent production lessons", "org chart AI agents CEO CTO" 등으로 검색했지만 1차 자료 수준은 못 찾음. 대부분 벤더 마케팅 블로그. Project Vend 말고 부서 단위 멀티에이전트의 공개 사후 분석은 확인 못 함. 검색어 몇 개로 본 결과라 "없다"는 뜻은 아니다.

---

## C. 실패 유형, 비용, 검사 에이전트의 한계

### C-1. [2025] MAST, "Why Do Multi-Agent LLM Systems Fail?" (Cemri et al., UC Berkeley 등, 2025-03) [논문-프리프린트]
URL: https://arxiv.org/html/2503.13657

- 7개 프레임워크(ChatDev, MetaGPT, HyperAgent, AppWorld, AG2/MathChat, Magentic-One, OpenManus)의 실행 기록 1,642개. 사람 주석자 간 일치도 kappa 0.88.
- 실패율: 7개 시스템 모두 41%~86.7%. ChatDev는 ProgramDev에서 정답률 약 25%.
- **범주 비율 (2026-09-25 정정)**: 게재본(NeurIPS 2025 D&B Spotlight) 전체 1,642개 기준 **시스템 설계 44.2%, 에이전트 간 어긋남 32.3%, 검증 23.5%**. 41.8 / 36.9 / 21.3(v2 본문의 41.77 / 36.94 / 21.30)은 시스템별 30개씩 210개 부분집합 수치다. 처음에 적었던 "43.8 / 32.2 / 23.9"는 어느 판본에도 없는 잘못된 값이었다. 근거: [11 §5-5](11-orchestration-current-2026.md)
- 14개 실패 유형(전체 1,642개 기준, 합산하면 범주 비율과 일치)

| 범주 | 실패 유형(빈도) |
|---|---|
| 시스템 설계 문제 44.2% | 과업 명세 위반 11.8%, 역할 명세 위반 1.5%, **같은 단계 반복 15.7%**, 대화 기록 유실 2.8%, **종료 조건 인지 못함 12.4%** |
| 에이전트 간 정렬 실패 32.3% | 대화 리셋 2.2%, 명확화 질문 안 함 6.8%, 과업 이탈 7.4%, 정보 숨김 0.85%, 다른 에이전트 입력 무시 1.9%, **추론과 행동 불일치 13.2%** |
| 검증 실패 23.5% | 조기 종료 6.2%, **검증 없음 또는 불완전 8.2%**, **잘못된 검증 9.1%** |

- MetaGPT는 ChatDev보다 설계와 정렬 실패가 60~68% 적지만 검증 실패는 1.56배 많음.
- LLM 판정기(o1, few-shot)가 사람 주석을 따라간 정도: 정확도 94%, kappa 0.77. 처음 보는 시스템에서 kappa 0.79.
- 개선 실험
  - ChatDev(ProgramDev): 기준 36.7%, 프롬프트(역할 명세) 개선 후 46.1%(+9.4%p), 토폴로지 변경 후 52.3%.
  - AG2(GSM-Plus, GPT-4): 상위 목표 대비 검증 단계 추가로 53.3%에서 62.7%. 한 보고는 +15.6%p로 적었다(GPT-4o 결과로 보이나 확인 못 함).
  - 실험 모델은 GPT-4o, Claude 3.7 Sonnet, Qwen2.5-Coder-32B, CodeLlama-7B(2025년 초 모델).
  - 저자 결론: "not all failure modes are resolved, and task completion rates still remain low".
- 검증기에 대해: "Many existing verifiers perform only superficial checks ... such as checking if the code compiles or if there are leftover TODO comments".
- "improvements in the base model capabilities will be insufficient". 원인은 조직 설계와 조율이라는 주장.

### C-2. 같은 예산에서 단일 에이전트와 멀티에이전트 비교

> **2026 재검증**: 대체로 성립. GPT-5, Gemini 2.5 Pro급에서도 확인. 사람이 설계했고 나눌 수 있는 과제에서만 멀티에이전트가 이김. [11 §5-4](11-orchestration-current-2026.md)

- [2025] Kim et al. (Google Research, DeepMind, MIT), "Towards a Science of Scaling Agent Systems" (2025-12) [논문-프리프린트] https://arxiv.org/abs/2512.08296 , 블로그 https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
  - 병렬화 가능한 과제(Finance-Agent)에서 중앙 조정형 +80.9%(v1) 또는 +80.8%(v3). 순차 의존 과제(PlanCraft)에서는 모든 멀티에이전트 변형이 39~70% 악화.
  - 오류 증폭: 서로 검토하지 않는 독립형 17.2배, 오케스트레이터가 있는 중앙형 4.4배. (v1 초록과 v3 본문에서 확인, 11 §5-4)
  - 단일 에이전트 기준 성능이 약 45%를 넘으면 조율 효과가 0이거나 마이너스. (v1 초록과 v3 본문에서 확인, 11 §5-4)
  - 초록에서 직접 확인: "Architectures without centralized verification tend to propagate errors more".
  - 실험 구성 수는 v1 180개, v3(2026-04-08) 260개. 판본 차이다. R²도 판본마다 다르다(v1 0.513, v3 0.373).
- [2026] Tran & Kiela, arXiv 2604.02460 [논문-프리프린트] https://arxiv.org/abs/2604.02460: 사고 토큰 예산을 같게 맞추면 멀티홉 추론에서 단일 에이전트가 같거나 더 나음(Qwen3, DeepSeek-R1-Distill, Gemini 2.5). 멀티에이전트 이점의 상당 부분은 계산량을 통제하지 않아서 생긴 것이라는 주장.
- [2026] Jwalapuram et al., "The Illusion of Multi-Agent Advantage" [논문-프리프린트] https://arxiv.org/abs/2606.13003: 자동 생성한 멀티에이전트는 "consistently underperform CoT-SC despite being up to 10x more expensive". 전문가가 직접 설계한 구조는 자동 생성보다 나음.
- [2023] Smit et al., "Should we be going MAD?" [논문-프리프린트] https://arxiv.org/abs/2311.17371: 멀티에이전트 토론은 "do not reliably outperform ... self-consistency and ensembling". 하이퍼파라미터에 민감.
- [2026] Kaushik Rajan, "The Multi-Agent Trap", TDS (2026-03-14) [실무자] https://towardsdatascience.com/the-multi-agent-trap/: 단계당 95% 성공률이면 20단계 체인은 35.8%.

### C-3. 검사(판정) 에이전트는 믿을 만한가

> **2026 재검증**: 자기 교정이 해롭다는 결론은 약해짐(일부 추론 모델은 떨어지지 않음, [11 §5-1](11-orchestration-current-2026.md)). 판정자 자기선호와 오류 상관은 유지, 방향이 모델마다 다름, 장황함 편향은 약해짐([11 §5-2](11-orchestration-current-2026.md)). 아래 2023~2024년 논문은 대부분 GPT-4 시절 결과다.

- [2023, 게재 2024] Huang et al., ICLR 2024 [논문-게재] https://arxiv.org/abs/2310.01798: 외부 피드백 없이 스스로 고치게 하면 못 고치고 "performance even degrades after self-correction".
- [2024] Kamoi et al., TACL 2024 [논문-게재] https://arxiv.org/abs/2406.01297: 자기 교정은 "reliable external feedback"이 있거나 대규모 파인튜닝을 했을 때만 된다. 프롬프트만 준 LLM 피드백으로 성공한 사례는 교정에 특별히 유리한 과제를 빼면 없음.
- [2024] Stechly, Valmeekam, Kambhampati [논문-프리프린트] https://arxiv.org/abs/2402.08115: GPT-4 자기비평은 "significant performance collapse"(Game of 24, 그래프 색칠, 계획 과제). 건전한 외부 검증기를 붙이면 "significant performance gains".
- [2024] Panickssery, Bowman, Feng [논문, NeurIPS 2024 게재로 알려졌으나 이번에 확인 안 함] https://arxiv.org/abs/2404.13076: LLM 평가자는 사람이 보기에 품질이 같아도 자기 출력에 점수를 더 준다. 자기 출력을 알아보는 능력과 편향 강도가 선형 상관.
- [2025] Goel et al., "Great Models Think Alike" [논문-프리프린트] https://arxiv.org/abs/2502.04313: 판정 모델은 자기와 비슷한 모델을 선호. "Model mistakes are becoming more similar with increasing capabilities". 같은 계열 모델끼리는 실수가 겹쳐 서로 못 잡을 위험.
- [2023] Zheng et al., MT-Bench, NeurIPS 2023 [논문-게재] https://arxiv.org/abs/2306.05685: GPT-4 판정기는 사람과 80% 넘게 일치(사람끼리 일치 수준). 위치 편향, 장황함 편향, 자기 강화 편향이 있음.

### C-4. 에이전트 간 인계(handoff) 손실

> **2026 재검증**: 유지. HiddenBench는 ICML 2026 채택, GPT-5 포함. [11 §5-6](11-orchestration-current-2026.md)

- [2025] HiddenBench (Li, Naito, Shirado) [논문-프리프린트] https://arxiv.org/abs/2505.11556: 정보가 여러 에이전트에 흩어져 있으면 정확도 30.1%, 한 에이전트가 다 가지면 80.7%. 에이전트들이 "fail to reason about what others might know". 집단이 커질수록 악화.
- [2026] "When Must Becomes Maybe" (arXiv 2608.24569, 2026-08) [논문-프리프린트, 합성 테스트베드] https://arxiv.org/abs/2608.24569: 합성 에피소드 1,296개. 일반 요약 인계에서 제약 100% 비활성화, 금지 행동 54.2% 발생. 상태 필드 4개를 구조화해서 넘기면 제약 보존 100%, 금지 행동 0%. "Semantic availability does not guarantee operational preservation".
- [2026] "Facts Without Rules" (arXiv 2608.29028) [논문-프리프린트, 합성 테스트베드] https://arxiv.org/abs/2608.29028: 요약하면 사실은 남고 사용 조건(경계 정보)만 빠진다. 경계 표시 보존율은 자유 텍스트 인계 약 0.80, 25단어 예산 약 0.57. 사실 보존율은 거의 만점 유지. 모호한 표현은 GPT 73%, DeepSeek 50%에서 유출, 명시적 제약으로 쓰면 15% 미만.
- 2608.x 두 편은 실제 시스템에서 재현됐는지 모른다.

---

## D. 실행 환경: Claude Code와 Anthropic 도구

### D-1. [2026-09 조회] Claude Code 하위 에이전트 [공식문서, 메인 세션이 원문 재확인]
URL: https://code.claude.com/docs/en/sub-agents.md

- 중첩: "By default, a subagent can spawn subagents of its own, up to three layers below the main conversation." `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`로 조정, `1`이면 중첩 끔. 한도에 닿으면 fork를 뺀 하위 에이전트에서 Agent 도구가 빠지고, 그 에이전트는 일을 직접 하고 요약 하나를 돌려준다.
- 동시 실행: 기본 20개. 넘으면 `Concurrent subagent limit reached`. `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`로 조정.
- 시작 컨텍스트: "Each subagent starts with a fresh, isolated context window. It doesn't see your conversation history". fork는 예외로 부모 대화를 물려받는다. 일반 하위 에이전트가 받는 것은 자기 시스템 프롬프트, 위임 메시지, CLAUDE.md 계층 전체(`omitClaudeMd`로 끌 수 있음), git 상태, `skills` 필드로 지정한 스킬, 같은 세션의 다른 이름 붙은 에이전트 목록.
- 결과 반환: 백그라운드 하위 에이전트는 다음 턴에 완료 알림으로, 포그라운드는 끝날 때까지 메인을 막는다. 중첩된 경우 최상위 하위 에이전트의 요약만 메인에 돌아온다.
- 에이전트별 도구 허용 목록(`tools`), 금지 목록(`disallowedTools`), 모델(`model`) 지정 가능.

### D-2. [2026-09 조회] 정기 실행 [공식문서, 메인 세션이 원문 재확인]
URL: https://code.claude.com/docs/en/scheduled-tasks.md

| | Cloud(Routines) | Desktop 예약 작업 | `/loop` |
|---|---|---|---|
| 실행 위치 | 클라우드 | 내 컴퓨터 | 내 컴퓨터 |
| 컴퓨터 켜져 있어야 함 | 아니오 | 예 | 예 |
| 세션 열려 있어야 함 | 아니오 | 아니오 | 예 |
| 로컬 파일 접근 | 아니오(새 clone) | 예 | 예 |
| 최소 간격 | 1시간 | 1분 | 1분 |

- `/loop`과 cron 작업은 세션 범위. 반복 작업은 만든 지 7일 뒤 자동 만료. 세션당 최대 50개.
- 세션과 무관하게 돌릴 것: Routines, GitHub Actions의 `schedule`, Desktop 예약 작업.

### D-3. [2026-09 조회] 그 밖의 옵션 [조사 에이전트 보고, 메인 세션 재확인 안 함]
- Agent Teams: 여러 독립 Claude Code 세션을 팀으로 묶고 공유 작업 목록과 SendMessage로 조율. 실험 기능(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), 팀원이 새 팀원을 만들 수 없음, 세션당 팀 1개. https://code.claude.com/docs/en/agent-teams.md
- Hook 이벤트: `PreToolUse`, `PostToolUse`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`(exit 2로 재작업 요청). https://code.claude.com/docs/en/hooks-guide.md
- Workflows: JavaScript 스크립트로 여러 하위 에이전트를 조율(`agent()`, `parallel()`, `pipeline()`). https://code.claude.com/docs/en/workflows.md
- Claude Agent SDK(Python `claude-agent-sdk`, TypeScript `@anthropic-ai/claude-agent-sdk`): Claude Code와 같은 하니스를 코드로 쓰고 직접 호스팅.
- Managed Agents: Anthropic이 호스팅. 멀티에이전트 오케스트레이션, cron 기반 Scheduled Deployments(최소 1시간 간격). 베타. https://platform.claude.com/docs/en/managed-agents/overview.md
- 조사 에이전트 보고서의 비교표 평가(✅, "6개월 시범" 같은 권장안)는 문서 근거가 없는 에이전트 판단이라 여기 옮기지 않았다.

---

## 확인 못 한 것 (다음에 인용하기 전에 원문 대조 필요)

- ~~Kim et al.의 17.2배, 4.4배, 45% 기준선 수치와 실험 구성 수~~ → 11 §5-4에서 확인(판본 차이)
- ~~MAST 범주 비율의 판본별 차이~~ → 11 §5-5에서 확정. AG2 개선 수치의 모델별 구분은 여전히 미확인
- "Organized Teams" 논문과 2605.29420 논문의 세부 수치
- 2608.24569, 2608.29028이 실제 시스템에서 재현되는지
- D-3 항목 전부(메인 세션이 공식 문서로 재확인하지 않음)
