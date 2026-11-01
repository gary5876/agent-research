# 오케스트레이션 2026년 현재 기준 (10번 근거 재검증)

**Status:** ACTIVE
**Layer:** 1 (외부 출처 조사 기록). 층 구분 기준: [CATALOG.md](../../CATALOG.md)
**작성일:** 2026-09-25
**성격:** 조사 기록. [10-orchestration-evidence-2023-2025.md](10-orchestration-evidence-2023-2025.md)의 2023~2025년 근거가 지금도 맞는지 다시 확인하고, 2026년 자료를 새로 모은 것. 판단은 [12-orchestration-application.md](12-orchestration-application.md)에 반영한다.

## 이 문서를 읽는 법

- 2026-09-25에 조사 에이전트 3개(2026년 가이드와 운영 사례, 옛 연구 재검증, 조직형 에이전트와 업무 벤치마크)가 원문을 읽고 보고한 내용이다.
- 대부분 WebFetch(작은 모델이 페이지를 요약해 주는 방식)로 읽었다. 인용문은 원문과 한두 단어 다를 수 있다.
- **메인 세션이 원문에서 다시 확인한 것**에는 `[재확인]`을 붙였다. MAST 수치와 Wharton 페르소나 논문의 모델 목록은 조사 에이전트가 PDF에서 직접 뽑았다.
- 원문을 못 읽고 검색 요약이나 2차 출처로만 본 것은 `[미검증]`으로 표시했다. 인용 전에 원문 대조가 필요하다.
- 근거 등급: [논문-게재] [논문-프리프린트] [공식문서] [벤더] [실무자] [애널리스트] [언론] [집계사이트]
- 2026년 현재 모델 이름은 출처에서 확인한 것만 적는다. 출처마다 다른 세대 모델을 썼으니 수치를 비교할 때 모델명을 같이 본다.

---

## 1. 한눈에: 옛 결론이 2026년에도 맞나

| 옛 결론 (10번 문서) | 2026년 판정 | 근거 절 |
|---|---|---|
| 단일 에이전트로 시작하라 | **유지.** Anthropic, OpenAI, Microsoft, LangChain 모두 2026년 자료에서 같은 말 | §2 |
| 멀티에이전트는 조사, 읽기 작업에만 맞다 | **갱신.** 2026년엔 코딩(쓰기)에도 오케스트레이터와 병렬 워커가 제품으로 나옴. 조건은 파일, 워크트리, VM 단위로 쓰기를 격리하는 것 | §2, §4 |
| 역할(직무)별로 나누는 건 위험하다 (CrewAI 비판 등) | **강화.** Anthropic이 2026-01에 "일의 종류로 나누기"를 명시적으로 문제로 지목 | §2-1 |
| 외부 신호 없는 자기 교정은 성능을 떨어뜨린다 | **약해짐.** 일부 추론 모델(o3-mini, Opus 4.6)은 떨어지지 않음. GPT-5는 여전히 조금 떨어짐 | §5-1 |
| LLM 판정자는 자기 출력을 편애하고 비슷한 모델끼리 실수가 겹친다 | **유지, 더 정교해짐.** 편향 방향과 크기가 모델마다 다름. 장황함 편향은 약해짐 | §5-2 |
| 전문가 페르소나는 정확도를 안 올린다 | **유지.** o3-mini, o4-mini 포함 | §5-3 |
| 같은 비용이면 멀티에이전트가 단일을 못 이긴다 | **대체로 유지.** 단 사람이 설계했고 나눌 수 있는 과제에선 멀티에이전트가 이김 | §5-4 |
| 에이전트 사이 인계에서 정보가 샌다 | **유지.** GPT-5, GPT-5.4 등 2026년 모델로도 같은 방향 | §5-6 |
| 긴 입력의 중간을 놓친다 (lost in the middle) | **약해짐.** 단순 찾기는 대부분 해결. 추론형 과제와 길이 자체로 인한 저하는 남음 | §5-7 |
| 같은 모델 상사는 부하 감독을 잘 못한다 (Project Vend) | **유지, 보강.** 검증자 역할이 실패작의 약 절반을 승인(TeamBench), AI 심판이 2.3~2.9배 과대평가(RLI) | §6 |
| 가상 회사 과제 최고 약 30% (TheAgentCompany) | **옛 수치.** 검증된 최고 42.86%(2025-11). 2026년 유효 등재 없음. 최신 모델 측정값 없음 | §6-1 |

---

## 2. 2026년 공식 가이드

### 2-1. Anthropic

**[2026] "Building multi-agent systems: when and how to use them"** [벤더] [재확인]
URL: https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them (2026-01-23, Cara Phillips 외)
- "A well-designed single agent with appropriate tools can accomplish far more than many developers expect."
- "In our testing, multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks."
- 멀티에이전트가 이기는 경우를 셋으로 한정: 컨텍스트 보호, 병렬화, 전문화.
- **일의 종류로 나누기의 문제**: "Dividing by type of work (one agent writes features, another writes tests, a third reviews code) creates constant coordination overhead. Each handoff loses context... the test-writing agent lacks knowledge of why certain implementation decisions were made and the code reviewer lacks the context of exploration and iteration."
- **권장은 맥락 경계로 나누기**: "Dividing by context boundaries means an agent handling a feature should also handle its tests, because it already possesses the necessary context. Work should only be split when context can be truly isolated."
- **검증 에이전트는 예외**: "Verification subagents remain valuable when using less capable orchestrators, when verification requires specialized tools, or when you want to enforce explicit verification checkpoints in your workflow."
- "More capable orchestrator models (like Claude Opus 4.5) are increasingly able to evaluate subagent work directly without a separate verification step."

**[2026] "Harness design for long-running application development"** [벤더]
URL: https://www.anthropic.com/engineering/harness-design-long-running-apps (2026-03-24)
- Planner, Generator, Evaluator 3개 에이전트 구성.
- Opus 4.5 시절 비용 $200/6시간. 같은 작업을 단일 에이전트로 하면 $9/20분.
- Opus 4.6에서 스프린트 분해를 없애고 QA를 1회로 줄였다. DAW 앱 제작에 $124.70, 3시간 50분.
- "every component in a harness encodes an assumption about what the model can't do on its own"
- "find the simplest solution possible, and only increase complexity when needed"
- 모델이 좋아질수록 구조를 걷어낸 사례가 명시돼 있다.

**[2026] "Scaling Managed Agents"** [벤더]
URL: https://www.anthropic.com/engineering/managed-agents (2026-04-08)
- "Harnesses encode assumptions that go stale as models improve."
- Sonnet 4.5의 "context anxiety" 대응용 우회책이 Opus 4.5에서는 필요 없어졌다.

**[2026] "Patterns and problems in multiagent systems"** [벤더, 연구 글] [재확인]
URL: https://www.anthropic.com/research/multiagent-systems (2026-08-13, Frontier Red Team, 교신저자 Carolyn Zou)
- 이번 조사에서 가장 최신이고 중요한 출처.
- 동조: "18 out of 30 agents decided to create a git branch with the exact same branch name, 'mvp-game-loop.'"
- 정보 분산 과제(hidden-profile): 4개 에이전트 그룹이 Mythos 5는 약 85%, 다른 모델은 "17–36%, far below solo ceilings near 100%".
- 목표 충돌: "98% of Mythos 5 runs ended in truce". 조사 보고로는 Sonnet 4.6과 Opus 4.6 실행은 대부분 힘으로 끝나거나 결론이 안 났다.
- 코드 공유: Sonnet 5는 "relatively high code sharing"을 유지했고, 다른 모델은 격리로 충돌 가능성을 줄였다.
- 악성 행동: 에이전트가 "malicious code that was disguised as belonging to another agent"를 배포.
- 권고: 사람 감독과 메커니즘 설계는 선택이 아니라 필수. 멀티에이전트 상호작용이 잘 되는 조건을 "deliberately and early" 찾아야 한다.
- 요약: **최신 모델이 에이전트끼리의 조정을 실제로 더 잘하지만, 실패 패턴이 사라지지는 않았다.**

**[2026] Managed Agents 멀티에이전트 오케스트레이션** [공식문서, 베타] [재확인]
URL: https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration (베타 헤더 `managed-agents-2026-04-01`, 출시 블로그 2026-05-19 https://claude.com/blog/new-in-claude-managed-agents)
- 모든 에이전트가 같은 샌드박스, 파일시스템, 인증 정보를 공유하고, 각자 맥락이 분리된 스레드에서 돈다. 도구, MCP 서버, 컨텍스트는 공유하지 않는다.
- "The coordinator can only delegate to one level of agents; referencing an agent that has its own `multiagent.agents` roster fails the create or update request with a validation error."
- 로스터에 최대 20개 에이전트, 같은 에이전트를 여러 복사본으로 호출 가능. 동시 스레드 최대 25개.
- 코디네이터가 자기 복사본(`self`)을 만들 수 있고, 조언자(`advisor`) 모델을 하나 붙일 수 있다.

### 2-2. OpenAI
- **Responses API Multi-agent 가이드** [공식문서, 날짜 표기 없음] https://developers.openai.com/api/docs/guides/responses-multi-agent
  - GPT-5.6 전용 베타. GPT-5.6 출시일 2026-07-09 [미검증, openai.com 403].
  - 단일 에이전트를 쓰라는 조건: "Each step depends directly on the previous step", "Agents would contend over the same mutable resource", "You require a fixed, deterministic execution graph".
  - 깊이 제한은 "no fixed limit on the total number of subagents or tree depth". 다만 `max_concurrent_subagents` 기본값 3을 "recommended for most workloads".
- **GPT-5.6 모델 가이드** [공식문서, 날짜 표기 없음] https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6
  - "you often do not need to prescribe every step"
- 2025 practical guide(10 A-3)의 "단일 에이전트에 도구를 늘려라"와 모순은 없다. 멀티에이전트가 API 호스팅 기능으로 들어간 게 달라진 점이다.

### 2-3. Microsoft
- Azure Architecture Center "AI Agent Orchestration Patterns" (ms.date 2026-02-12, 업데이트 2026-09-21) [공식문서]. 10 A-5와 같은 문서다. "Use the lowest level of complexity that reliably meets your requirements." Magentic 패턴 비용이 "most variable".

### 2-4. LangChain
- [2026] "Choosing the Right Multi-Agent Architecture" (2026-01-14, Sydney Runkle) [벤더] https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture : "Start with a single agent and good prompt engineering. Add tools before adding agents."
- [2026] "Building Multi-Agent Applications with Deep Agents" (2026-01-21) [벤더] https://www.langchain.com/blog/building-multi-agent-applications-with-deep-agents : 하위 에이전트의 목적을 컨텍스트 격리("dumb zone" 회피)로 정의.
- [2026] "Introducing Dynamic Subagents in Deep Agents" (2026-06-29) [벤더] https://www.langchain.com/blog/introducing-dynamic-subagents-in-deep-agents : 모델이 오케스트레이션 코드(JS)를 직접 쓴다. LLM이 500개 중 75개만 보고 끝났다고 하는 문제를 코드 루프가 막는다: "screening 75 of 500 items and calling it done. A dispatch loop doesn't."

### 2-5. Google
- 2026년에 입장 변화를 보여주는 공식 가이드는 찾지 못했다(검색어 "Google ADK multi-agent guidance 2026", "Google Developers Blog 2026 multi-agent patterns ADK").
- 검색 요약이 "2026-09"라고 한 "Developer's guide to multi-agent patterns in ADK"는 원문 확인 결과 2025-12-16이었다.

---

## 3. 2026년 실제 운영 사례

마케팅, 운영 분야에서 구조, 에이전트 수, 실패, 비용을 모두 공개한 2026년 1차 엔지니어링 글은 찾지 못했다. 검색에 나온 마케팅 글(예: "34% of enterprises", "90.2% better")은 벤더나 에이전시 콘텐츠였다. 90.2%는 2025년 Anthropic 리서치 시스템 수치를 마케팅 맥락으로 잘못 옮긴 것이다.

- **[2026] DoorDash Flux** [실무자, 독립 기업 엔지니어링 블로그] https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/ (2026-08-11)
  - 월 130,000건 작업. 자동 코드리뷰 주 25,000건 이상, 플레이북 300개 이상, 호출 주 10,000건 이상.
  - **구조는 계층형 멀티에이전트가 아니라 "YAML 플레이북 + 샌드박스 + MCP 게이트웨이".** 플레이북 하나에 에이전트 단계와 결정적 단계(일반 코드)를 섞는다.
  - 교훈: "Start narrow to earn trust." 코드리뷰 하나로 시작해 CI 분류, 온콜, 유지보수로 확장.
  - 운영 자동화의 실제 모습에 가장 가까운 사례.
- [2025] DoorDash "Beyond Single Agents" (2025-11-11, 참고) https://careersatdoordash.com/blog/beyond-single-agents-doordash-building-collaborative-ai-ecosystem/
  - 사업 운영과 재무 보고는 결정적 워크플로, 탐색은 단일 에이전트.
  - 계층형 딥에이전트는 "building and testing" 단계, 스웜은 "research frontier"라고 스스로 적음.
  - "these systems only amplify any inconsistencies in their underlying components"
- **[2026] Google "Production-Ready AI Agents: 5 Lessons from Refactoring a Monolith"** [벤더] https://developers.googleblog.com/production-ready-ai-agents-5-lessons-from-refactoring-a-monolith/ (2026-04-21)
  - 영업 아웃리치. 하위 에이전트 5개를 순차 파이프라인으로: 회사 조사, 검색 계획, 사례 조사, 선별, 이메일 작성.
  - 모델명, 비용, 전후 비교 수치 없음. "모놀리스"는 단일 에이전트가 아니라 for 루프 스크립트였다.
- **[2026] Cursor "Scaling long-running autonomous coding"** [벤더, 자사 실험기] https://cursor.com/blog/scaling-agents (2026-01-14, Wilson Lin)
  - 동등한 권한의 에이전트가 락으로 협업하는 평면 구조는 실패: "Twenty agents would slow down to the effective throughput of two or three".
  - 통합자, 리뷰어 역할도 "created more bottlenecks than it solved".
  - 최종 구조는 Planner(하위 planner를 재귀 생성) + Worker + judge. 수백 개 에이전트 동시 실행.
  - GPT-5.2가 GPT-5.1-Codex보다 planner 역할을 더 잘했다.
- **[2026] Anthropic C 컴파일러** [벤더] https://www.anthropic.com/engineering/building-c-compiler (2026-02-05)
  - 병렬 에이전트 16개, 오케스트레이터 없이 git 파일 락으로 작업 점유. Opus 4.6, 약 2,000 세션, "just under $20,000".
  - 실패: "New features and bugfixes frequently broke existing functionality".
- [2026] Dust 블로그 [벤더] https://dust.tt/blog/multi-agent-systems (2026-05-20): Back Market 사기 탐지로 5개월간 약 €100K 차단. 에이전트 구조는 서술 안 함.
- [2026] Claude Managed Agents 고객 사례 (2026-05-19) [벤더]: Harvey 완료율 약 6배, Wisedocs 리뷰 50% 단축. 멀티에이전트가 아니라 다른 기능(dreaming 등)에 붙은 수치다.

### 3-1. AI가 사업을 직접 운영한 사례

- **[2026] Anthropic Project Deal** [벤더] https://www.anthropic.com/features/project-deal (2026-04-24)
  - 직원 69명이 1인당 $100을 받고, 에이전트끼리 협상해 186건, $4,000 이상 거래.
  - 약한 모델(Haiku)을 받은 사람은 더 나쁜 결과를 얻고도 알아채지 못했다.
- Project Vend 3단계는 찾지 못했다(검색어 "Project Vend phase 3 2026", anthropic.com 한정 검색). 2단계 내용은 10 B-6.
- **[2026] Andon Labs** (Vend 운영사) [벤더 겸 연구기관, 1차 사후분석] https://andonlabs.com/blog
  - Andon Market(샌프란시스코, 2026-04-10 개점): Claude Sonnet 4.6 기반 단일 에이전트 Luna가 운영, 사람 직원 2명 채용. 채용 재현 실험에서 21회 실행 전부가 부적격 지원자 채용을 승인, 기밀 지시는 21회 중 7회 위반 (/blog/ai-bosses-2, 2026-08-14).
  - Andon Café(스톡홀름, Gemini 3.1 Pro, 2026-06-30 글): 2개월 매출 $9,000, 지출 $38,000. 임대료와 인건비 빼고도 약 $5,600 손실. 베이커리 1,331개를 사서 326개만 팔았다. 고객 설득에 넘어가 에스프레소를 $3.60에서 $1.00로 내렸다.
  - "Why we built Pion"(2026-09-14): 두 매장 모두 아직 적자.
  - Andon FM(/blog/andon-fm-2, 2026-07-07): 모델 4개가 각자 라디오 방송사 운영, 6주 매출 Claude $2,662, Gemini $1,948, GPT $586, Grok $505. 사고: Gemini의 나치 군가 방송, Grok의 출력 붕괴, Claude의 청취자와 부적절한 관계 형성. 자율 콘텐츠 발행이라 마케팅 운영에 참고가 된다.
  - IEEE Spectrum (2026-09-14) [언론] https://spectrum.ieee.org/andon-labs-agentic-ai-businesses : 주문 누락, 배송 일정 오해, 직원 해고 사례 보도. 매장마다 AI 관리자 1명 구조.
- 조사 결과 2026년 실제 사업 운영 사례는 전부 **단일 관리자 에이전트 + 사람 직원** 구조였다. 조직도형 멀티에이전트로 실제 사업을 운영한 공개 사후분석은 찾지 못했다.

---

## 4. 2026년 코딩 에이전트에서 표준이 된 패턴

- **하위 에이전트는 사실상 표준.** Simon Willison (2026-03-16) [실무자] https://simonwillison.net/2026/Mar/16/codex-subagents/ : Codex 하위 에이전트 정식 출시. "the subagents pattern is widely supported in coding agents now". 지원: Codex, Claude Code, Gemini CLI, Mistral Vibe, OpenCode, VS Code, Cursor.
- Cognition "Devin can now Manage Devins" (2026-03-19) [벤더] https://cognition.com/blog/devin-can-now-manage-devins : 코디네이터가 범위 설정, 배정, 모니터링, 충돌 해결, 결과 취합. 각 Devin은 격리된 VM.
- Cognition "Multi-Agents: What's Actually Working" (2026-04-22)는 10 A-7 참고. FlowHunt 블로그[벤더, 날짜 없음]는 이를 두고 "The post does not retract the earlier essay by name, but the architectural concession is unambiguous"라고 해석.
- **Claude Code** [공식문서, 날짜 표기 없음]
  - Agent teams https://code.claude.com/docs/en/agent-teams : 아직 실험 기능이고 기본값은 꺼짐. "Start with 3-5 teammates". "No nested teams: teammates cannot spawn their own teammates". 순차 작업, 같은 파일 수정, 의존성 많은 작업에는 "a single session or subagents are more effective".
  - Dynamic workflows https://code.claude.com/docs/en/workflows (발표 2026-05-28): 스크립트가 오케스트레이터. 기본 동시 16개, 1회 최대 1,000개 에이전트. 에이전트 25개 또는 토큰 150만 초과 시 경고. 사례: Bun을 Zig에서 Rust로 75만 줄 이식, 11일 만에 테스트 99.8% 통과.
- **2026년에 굳은 두 가지** (조사 에이전트 정리)
  1. LLM이 매 턴 판단하는 오케스트레이션에서 **코드가 오케스트레이터**인 방식으로 이동. Claude workflows, LangChain dynamic subagents, GPT-5.6 programmatic tool calling.
  2. **쓰기는 한 곳, 읽기와 검증은 병렬.** Cognition 글과 Claude 문서의 "Avoid file conflicts"가 같은 얘기.

---

## 5. 옛 연구 재검증

### 5-1. 외부 신호 없는 자기 교정 → 약해짐
- **[2026] Liu & Meng, "Self-Correction as Feedback Control"** [논문-프리프린트] arXiv 2604.22273 (v2 2026-05-04)
  - 정답 신호 없이 최대 4회 자기 교정. GSM8K, MATH, StrategyQA.
  - GSM8K: GPT-4o-mini -6.2pp, GPT-4.1 -0.2, Claude Sonnet 4 -1.2, GPT-5 -1.8 (96.2→94.4), Claude Opus 4.6 +0.6, o3-mini +3.4 (93.2→96.6). 초록상 o4-mini ±0.
  - 핵심 변수는 오류 유입률. o3-mini는 오류 유입 0.0%에 교정률 44.1%. "먼저 검증" 프롬프트로 GPT-4o-mini의 -6.2pp가 +0.2pp로 바뀜.
- [2025~2026] Tsui, "Self-Correction Bench" [논문-게재, COLM 2026] arXiv 2507.02778 (최신 2026-08-02): 비추론 오픈모델 14개에서 자기 오류 사각지대 64.5%. 같은 오류를 외부 출처로 주면 고친다. 답 뒤에 "Wait"만 붙여도 사각지대 89.3% 감소.
- [2026] Chen et al., "The Self-Correction Illusion" [논문-프리프린트] arXiv 2606.05976 (v2 2026-07-31): 같은 오류 텍스트를 사고 영역에서 user, tool, memory 역할로 옮겨 붙이기만 해도 명시적 교정률이 23~93pp 상승(12개 설정 중 10개 유의).
- [2025] MatSciBench [논문-게재, KDD '26] arXiv 2510.12171: 비추론 5개 모델에서 자기 교정으로 342개 악화, 233개 개선, 순 -2.1%. 악화 원인의 69.6%는 맞는 답을 틀렸다고 오판. thinking 모델은 실험 대상 아님.
- [2026] Self-Verification Dilemma [논문-프리프린트] arXiv 2602.03485: 추론 모델 내부 재검토는 "vast majority are confirmatory rather than corrective".
- [2026] Illusion of Insight [논문-프리프린트] arXiv 2601.00514 (v2 2026-04-19): R1 계열 100만 개 이상 추론 기록 분석. 중간의 "aha" 전환은 드물고 정답률을 거의 안 올림.
- Stechly et al.(10 C-3)은 ICLR 2025로 게재됨. o1 이후 모델로 같은 실험을 다시 한 논문은 못 찾음.
- **판정**: "자기 교정은 해롭다"를 모든 모델에 일반화하면 틀린다. 더 정확한 최신 틀은 "오류를 새로 만들어 넣는 비율이 0에 가까워야만 이득". GPT-5 결과는 기준선이 90%대라 천장 효과일 수도 있다(조사 에이전트 추론).

### 5-2. LLM 판정자 편향 → 유지, 정교해짐
- [2026] Yang et al., "Quantifying and Mitigating Self-Preference Bias" [논문-프리프린트] arXiv 2604.22891 (v4 2026-06-02): 판정 모델 20개(추론 모델 R1-0528, Qwen3-235B-Thinking, Kimi-K2-Thinking 포함). 성능과 낮은 자기선호는 "uncorrelated, or even negatively correlated". 자기선호 계수 DeepSeek-V3.2 +0.226, Claude Sonnet 4.5 -0.229(자기 답을 오히려 깎음), R1-0528 -0.097, Qwen3-Thinking Explanation 과제 +0.540.
- [2026] Pombal et al. [논문-프리프린트] arXiv 2604.06996 (2026-04-08): 판정 모델 GPT-5, Claude 4.5 Sonnet/Haiku, Qwen3, Llama 4, Gemma 3. 루브릭 평가에서도 자기 출력이 실패한 항목을 통과로 잘못 채점할 확률이 "more than 50% more likely". GPT-5는 HealthBench에서 앙상블 대비 자기에게 약 4점 더 줌.
- [2026] Huang et al., "Reasoning Model Is Superior LLM-Judge, Yet Suffers from Biases" [논문, ACL 2026 EvalEval 워크숍] arXiv 2601.03630: 추론 모델이 더 좋은 판정자지만 "still exhibit strong evaluation biases".
- [2026] Norman et al., "Reliability without Validity" [논문-프리프린트] arXiv 2606.19544 (2026-06-17): 9개 회사 판정 모델 21개. 장황함 편향 0.011 미만으로 작음. 위치 편향은 실서비스 판정자 2개에서만 심함(0.10 초과). 벤치마크에 따라 판정자 순위가 최대 14계단 바뀜.
- [2025] Kim et al., "Correlated Errors in LLMs" [논문-게재, ICML 2025] arXiv 2506.07962: 350개 이상 모델. 둘 다 틀릴 때 60% 확률로 같은 오답. 크고 정확한 모델일수록 회사가 달라도 오류가 더 겹침.
- **판정**: 자기선호와 오류 상관은 유지. "항상 자기 편"이 아니라 방향과 크기가 모델마다 다르다. 장황함 편향은 약해졌고 위치 편향은 일부에만 남음.

### 5-3. 전문가 페르소나 → 유지
- [2025] Wharton "Playing Pretend"(10 B-5) PDF 확인: 모델은 GPT-4o, GPT-4o-mini, o3-mini, o4-mini, Gemini 2.0 Flash, Gemini 2.5 Flash. 추론 모델도 효과 없음. 아이나 비전문가 같은 저능력 페르소나는 정답률을 떨어뜨림.
- [2026] Hu et al., PRISM [논문-프리프린트] arXiv 2603.18507 (2026-03-19): MMLU에서 모든 페르소나가 정답률을 떨어뜨림(68.0% 대 71.6%). 반례로 R1 증류 소형 모델(7~8B)에서는 전문가 페르소나가 성능을 올림. 평가 모델이 모두 소형.
- [2026] Xiao et al. [논문-프리프린트] arXiv 2605.29420 (2026-05-28): 역할 38개, 문항 1,140개. 페르소나를 주면 전문성 깊이는 늘고 명료성은 줄어듦. 의료와 심리 상담형 질문에서만 나았다.
- GPT-5나 Claude 4.x급에서 페르소나가 정답률에 주는 영향을 직접 잰 논문은 못 찾음.

### 5-4. 같은 비용에서 멀티에이전트 대 단일 → 대체로 유지
- **Kim et al. (Google) 수치 정리** [논문-프리프린트] arXiv 2512.08296
  - v1(2025-12-09) 초록: 구성 180개, 독립 에이전트 오류 증폭 17.2배, 중앙 조정 4.4배, 단일 에이전트 기준 약 45% 초과 시 음의 효과, R²=0.513, 중앙형 +80.9%.
  - v3(2026-04-08) 초록: 구성 260개, R²=0.373(과제 기반 역량 지표 쓰면 0.413), +80.8%에서 -70.0%, 보류 설정에서 아키텍처 예측 87%. 본문에 17.2배, 4.4배, 45% 문장이 남아 있음.
  - v3 모델: GPT-5-nano/mini/5, Gemini 2.0 Flash/2.5 Flash/2.5 Pro, Claude Sonnet 3.7/4/4.5.
  - **180과 260은 판본 차이.** 인용할 때 판본을 적는다. Google 블로그는 2026-01-28.
- [2026] Tran & Kiela [논문-프리프린트] arXiv 2604.02460 (v2 2026-04-11): Gemini 2.5 Flash/Pro, Qwen3-30B-A3B, DeepSeek-R1-Distill-Llama-70B. 사고 토큰을 맞추면 단일이 같거나 나음(예: FRAMES Gemini 2.5 Pro 0.700 대 0.680). Gemini API는 요청한 예산이 실제로 지켜지지 않아 비교가 왜곡된다고 지적.
- [2026] Jwalapuram et al., "The Illusion of Multi-Agent Advantage" [논문-프리프린트] arXiv 2606.13003 (v2 2026-06-13): GPT-4o, GPT-5, GPT-OSS-120B, Gemini 2.5 Pro. GPQA-Diamond GPT-5 기준 단일 CoT-SC 87.35%($46) 대 자동 설계 AFlow 84.13%($275). 사람이 설계한 멀티에이전트는 SMFR 과제에서 96.51% 대 56.97%로 이김.
- [2026] "Rethinking the Value of Multi-Agent Workflow: A Strong Single Agent Baseline" [논문-프리프린트] arXiv 2601.12307 (2026-01-18): 같은 모델을 쓰는 워크플로는 단일 에이전트로 동등 성능, KV 캐시 재사용으로 더 효율적. 서로 다른 모델을 섞는 구성은 예외.
- [2026] "At Equal Inference Cost, Multi-Agent Structure Does Not Beat a Single Frozen Agent" [논문-프리프린트] arXiv 2609.04217 (페이지 날짜 2026-06-25로 ID와 불일치, 7B 모델만): 같은 비용에서 팀 0.769 대 단일 0.754, p=0.80로 차이 없음. planner와 critic 프롬프트가 "evolve to empty or low-impact prompts". 가중치 낮게.
- 반례: [2026] Wunderlich et al. [논문, ACL 2026 SRW] arXiv 2605.01566: 같은 예산에서 토론이 self-consistency보다 +1.3pp, mixture-of-agents +2.7pp. 모델은 Llama 3.1 70B/8B(4bit)뿐, 추론 모델은 실험 안 함.
- [2026] Bertalanič & Fortuna [논문, ACM CAIS] arXiv 2605.00914: 7~8B 동질 에이전트 10개 토론. 다수 의견 동조 최대 85.5%, 이미 나온 정답을 투표로 버린 격차 최대 32.3pp. 토큰은 자기 교정의 2.1~3.4배, 정답률은 같거나 낮음.
- **판정**: GPT-5, Gemini 2.5 Pro급에서도 유지. 더 정확한 결론은 "사람이 설계했고 나눌 수 있는 과제에서만 멀티에이전트가 이긴다".

### 5-5. MAST 수치 확정
- arXiv 2503.13657: v1 2025-03-17, v2 2025-04-22, v3 2025-10-26.
- **게재: NeurIPS 2025 Datasets & Benchmarks 트랙 Spotlight** [논문-게재]. neurips.cc 페이지와 proceedings PDF로 확인.
- proceedings PDF 수치
  - **전체 1,642개 기록(Figure 1): 시스템 설계 44.2%, 에이전트 간 어긋남 32.3%, 과제 검증 23.5%.** 세부 합산도 일치(11.8+1.5+15.7+2.8+12.4=44.2).
  - 시스템별 첫 30개씩 210개 부분집합(Figure 4): 41.8 / 36.9 / 21.3. v2 본문의 41.77 / 36.94 / 21.30이 이것.
  - 다른 그림에 37.17 / 31.41 / 31.41도 있음(초기 소표본으로 추정, 캡션 미확인).
- 10번 문서에 처음 적었던 "43.8 / 32.2 / 23.9"는 어느 판본에도 없었다. 2차 요약의 오기로 보인다. **인용은 "NeurIPS 2025 D&B, 1,642개 기록, 44.2 / 32.3 / 23.5"로.**
- 실험 모델: GPT-4o, Claude 3.7 Sonnet, Qwen2.5-Coder-32B, CodeLlama-7B.
- 2026년 후속
  - [2026] OrchestraBench [논문-프리프린트] arXiv 2608.05263 (2026-08-05): MAST 실패 5종을 Claude 에이전트(Sonnet, Opus, Haiku)에 주입. 도구 오류 회복률 1.0, 모호한 위임 0.30, 잠재적 의미 오류 0.0. 파이프라인이 깊어질수록 오류 파급 범위가 0.9에서 4.7로 커짐.
  - [2026] ToMAS arXiv 2609.16986: MAST 데이터를 학습 데이터로 쓰는 파일럿, Qwen2.5-1.5B, 효과 없음.
  - MAST 분류를 GPT-5나 Claude 4.x 시스템에 다시 적용해 새 분포를 낸 연구는 못 찾음.

### 5-6. 인계 시 정보 손실 → 유지
- [2025~2026] HiddenBench [논문-게재, ICML 2026] arXiv 2505.11556 (v4 2026-05-13): 모델 15개(GPT-5, GPT-5-nano, GPT-4.1/mini, Gemini 2.5 Pro/Flash/Flash-Lite, Qwen, Llama 등). 정보를 나눠 가진 멀티에이전트 30.1%, 다 가진 단일 80.7%. 최고 모델 Gemini 2.5 Pro도 격차 -0.310. GPT-5 계열이 GPT-4.1-mini보다 못한 경우도 있음.
- [2026] "When Must Becomes Maybe" arXiv 2608.24569 (2026-08-25): 실제 API 호출(1,772 에피소드, 8,789회). 모델 GPT-5.4, GPT-5.4-mini, DS-V4-Pro/Flash, GLM-5, Kimi-K2.5, Qwen3.5 등. 요약 압축에서 제약 100% 비활성화, 금지 행동 54.2%. 상태 필드 4개 복원 시 0%.
- [2026] "Facts Without Rules" arXiv 2608.29028 (2026-08-29): GPT-5-mini, DeepSeek-R1-32B. 경계 정보 보존율 약 0.80에서 25단어 요약 약 0.57. 모호한 제약은 50~73% 유출.
- [2026] Min et al. arXiv 2608.06503 (2026-08-06): AppWorld에서 컨텍스트 압축이 실행 상태를 흔든다.
- 같은 벤치마크를 다른 팀이 재현한 연구는 못 찾음. 다만 여러 팀이 2026년 모델로 같은 방향 결과를 냈다.

### 5-7. 긴 입력의 중간 놓치기 → 약해짐
- [2025] Chroma "Context Rot" (2025-07-14) [업계 기술보고서]: 18개 모델(o3, GPT-4.1, Claude Opus 4/Sonnet 4, Gemini 2.5 Pro 등). 단순 찾기에서는 위치에 따른 차이 "no notable variation". 하지만 입력이 길수록 성능 하락, 질문과 정답의 유사도가 낮을수록 더 빨리 하락.
- [2025] Du et al., "Context Length Alone Hurts" [논문-게재, EMNLP 2025 Findings] arXiv 2510.05381: 관련 정보를 완벽히 찾아도 길이만으로 13.9~85% 하락.
- [2025] NoLiMa [논문-게재, ICML 2025]: 32K에서 13개 모델 중 11개가 짧은 입력 대비 50% 아래. o1도 50% 미만 [미검증, 검색 요약].
- [2026] Ebrahimzadeh & Salili [ICML 2026 워크숍] arXiv 2601.02023: Gemini 2.5 Flash, DeepSeek-V3.2는 위치에 강함. Claude 4.5 Haiku는 중간 구간 논리추론이 약 50%까지 떨어지는 "most pronounced U-shaped degradation". GPT-5-mini는 깊이 50% 지점에서 약 80%로 급락.
- [2025] arXiv 2602.14188 (FLLM2025, IEEE): GPT-5, Grok-4, Gemini 2.5. "lost in the middle ... largely resolved in newer models". 다만 300K 토큰에서 정답률 50~53%.
- **판정**: 단순 찾기의 위치 효과는 대부분 사라짐. 추론형이나 증거가 흩어진 과제에선 U자 곡선이 남음. 길이 자체로 인한 저하는 여전히 강함.

---

## 6. 조직형 에이전트와 업무 벤치마크 (2026)

### 6-1. 업무형 벤치마크
- **TheAgentCompany** [공식, 리더보드 JSON 직접 조회] https://the-agent-company.com/#/leaderboard (175개 과제)
  - 검증된 1위: TTE-MatrixAgent + DeepSeek-V3.2, 완수율 42.86%, 부분점수 52.4% (2025-11-10). 단 동료 역할과 채점 역할을 원래 설정(Claude 3.5 Sonnet) 대신 Qwen_Plus로 돌려서 그대로 비교하기 어렵다.
  - 2위 MUSE + Gemini 2.5 Flash 41.14% (2025-10-13), OpenHands-Versa + Claude Sonnet 4 33.14%, 논문의 Gemini 2.5 Pro 30.29%.
  - **2026년 유효 등재 0건.** IRIS-Agent + GPT-5.4가 2026-06-26에 46.29%로 올랐다가 2026-07-22 철회. 사유 "accidental answer leakage in some graph nodes" (github.com/TheAgentCompany/experiments PR #16).
  - **역할극형 멀티에이전트 OWL RolePlay + GPT-4o/o3-mini는 완수율 4.0%** (2025-05-10). 같은 시기 단일 에이전트 GPT-4o는 8.6%.
  - 레포 마지막 push 2025-11-17. "지금은 약 30%"가 아니라 "최신 모델로는 측정값이 없다"가 정확하다.
- **OSWorld 2.0** [공식] https://osworld-v2.xlang.ai/ (2026-06-26 공개)
  - 장시간 워크플로 108개. 과제당 평균 318회 도구 호출(1.0은 약 30회), 69.6%가 1시간 넘게 걸림. 사람 중앙값 약 1.6시간.
  - 최고 Claude Opus 4.8 완수 20.6%, Opus 4.7 18.2%, GPT-5.5 약 14%.
  - OSWorld 1은 리더보드가 JS로 로드돼 원문을 못 읽음. 집계사이트에 "Qwen3.8 Max 86.1%, 2026-09-22"가 있음 [미검증]. 사람 기준선 72.36%.
- **tau-bench** [공식, 날짜 표기 없음] https://taubench.com/
  - tau2(소매, 항공, 통신): Qwen 3.5-397B 87.9%, Gemini 3.0 Pro 85.4%, Claude Opus 4.5 85.3%.
  - tau3-Banking(지식 검색): 1위도 55.2%(Qwen 3.8 Max), Claude Opus 5 48.7%.
- **GDPval**: OpenAI 페이지 403. 논문은 ICLR 2026. "GPT-5.2가 전문가 대비 승+무 70.9%" [미검증].
  - GDPval-AA v2.1 (Artificial Analysis, 2026-09) [독립 평가기관] https://artificialanalysis.ai/evaluations/gdpval-aa : 1위 Claude Opus 5.5(max) Elo 1846, Opus 5.5(xhigh) 1820, Fable 5.1 1735. **사람이 아니라 LLM 판정자가 쌍비교로 채점**하므로 "전문가 대비 몇 %"로 읽으면 안 된다.
- **Remote Labor Index** (CAIS, 2026-07-01) https://safe.ai/blog/significant-increase-in-digital-labor-automation
  - 실제 프리랜서 프로젝트 240건 중 고객이 받아줄 수준으로 끝낸 비율: Fable 5 15.8%, Opus 4.8 8.3%, GPT-5.5 6.3%. 2025-10 출시 때 최고는 2.5%.
  - **AI 판정자는 성능을 2.3~2.9배 과대평가.** 1위 모델 대표 산출물 3건도 "none ... would be accepted as finished work".
- **Vending-Bench 2** (Andon Labs, 2026-09-24) [벤더 겸 연구기관] https://andonlabs.com/blog/opus-5-5-gpt-6-sol-grok-4-7-vending-bench
  - 시작 자금 $500 기준 최종 잔고: GPT-6 Astra $15,515, GPT-6 Sol $14,428, Opus 5 $11,182, Grok 4.7 $10,537, Opus 5.5 $9,235.
  - 성과가 좋은 모델일수록 공급업체 기만, 카르텔 제안, 환불 거부(Grok 57%) 같은 비정렬 행동이 함께 보고됨.
- **AD-Bench** [논문-프리프린트] arXiv 2602.14257 (2026-02-15, 개정 06-22): 실제 광고 플랫폼 분석 요청 기반. 1위 Claude Opus 4.7 Pass@1 76.9%, 최고 난이도 61.4%.
- 목록만 확인하고 원문 안 읽은 것: OmegaUse-OfficeVal(2607.27155), ERPBench(2609.04667), FM-Bench(2608.18423).
- 요약(조사 에이전트): 짧은 과제는 포화, 사람이 1시간 넘게 걸리는 업무는 15~20% 정도 완수.

### 6-2. 팀 구조 연구
- [2026] "Multi-Agent Teams Hold Experts Back" [논문-게재, ICML 2026] arXiv 2602.01011: LLM 팀은 최고 멤버보다 성능이 최대 41.1% 낮았다. 전문가가 누구인지 알려줘도 의견을 평균내는 쪽으로 타협.
- [2026] TeamBench (MIT Media Lab, Microsoft) [논문-프리프린트] arXiv 2605.07073 (2026-05-08)
  - 역할을 OS 권한으로 강제한 팀과 프롬프트로만 나눈 팀의 통과율은 통계적으로 차이 없음.
  - **검증자 역할이 실패한 제출물의 거의 절반을 승인.**
  - 팀은 개별 에이전트가 약할 때만 도움이 됐다.

### 6-3. 프레임워크 현황 (gh api, 2026-09-25 조회)
| 레포 | stars | 마지막 push | 상태 |
|---|---|---|---|
| FoundationAgents/MetaGPT | 70,603 | 2026-01-21 | 사실상 정체 |
| OpenBMB/ChatDev | 34,392 | 2026-07-24 | 2026-01-07 ChatDev 2.0(DevAll) 노코드 플랫폼으로 전환, v1은 유지보수만 |
| OpenBMB/AgentVerse | 5,142 | 2024-09-09 | 방치 |
| camel-ai/camel | 17,771 | 2026-09-20 | 활동 중 |
| microsoft/autogen | 61,154 | 2026-04-15 | README에 Maintenance Mode 명시, Microsoft Agent Framework로 안내 |
| microsoft/agent-framework | 13,793 | 2026-09-25 | 1.0 GA, python-1.19.0(2026-09-18) |
| crewAIInc/crewAI | 59,009 | 2026-09-25 | 1.15.22(2026-09-16) |
| langchain-ai/langgraph | 42,262 | 2026-09-23 | 활동 중 |
| openai/openai-agents-python | 29,696 | 2026-09-25 | 활동 중 |
| google/adk-python | 21,637 | 2026-09-25 | 활동 중 |
| anthropics/claude-agent-sdk-python | 8,161 | 2026-09-25 | 활동 중 |

조직도형의 원조 프로젝트들은 정체되거나(MetaGPT, AgentVerse) 방향을 바꿨다(ChatDev 2.0).

### 6-4. 기업 도입 데이터
- **측정된 설문**
  - McKinsey State of AI 2026 (2026-08, 조사 2026-05~06, n=1,719) [애널리스트 설문] [미검증, 원문 타임아웃, 2차 출처]: 대기업 에이전트 확산 비율 27%에서 40%, 대개 1~2개 기능. EBIT 영향 보고 37%로 전년과 비슷, 고성과 기업 약 6%.
  - McKinsey 2025판 (CX Today 인용, 2026-02-23) [언론 경유]: 에이전트 실험 62%, 확산 23%. 고성과 기업의 65%는 사람 검토 절차를 정의해 둠, 그 외 23%.
  - LangChain State of Agent Engineering (2026-06-12, 조사 2025-11~12, n=1,340) [벤더 설문] https://www.langchain.com/state-of-agent-engineering : 프로덕션 도입 57.3%, 최대 장벽은 품질(32%), 평가 방법은 사람 검토 59.8%. 매일 쓰는 에이전트는 코딩 보조가 압도적. 역할 기반 팀 사용률 수치는 없음.
  - [2025~2026] "Measuring Agents in Production" (UC Berkeley 등) [논문-프리프린트] arXiv 2512.04123 (개정 2026-06-04, 사례 20건과 실무자 86명): **68%의 에이전트가 최대 10단계 안에서 사람 개입을 받음.** 74%가 주로 사람 평가에 의존.
- **애널리스트 예측 (측정값 아님)**
  - Gartner 2025-06 "2027년까지 40% 이상 취소"의 갱신이나 실측치는 못 찾음. gartner.com 403.
  - Gartner 2026 보도자료 [미검증, 검색 요약]: 2026-05-05 경영진 350명 설문(약 80%가 인력 감축, 감축과 ROI 무관), 2026-05-26 일률적 거버넌스 실패 예측, 2026-07-28 영업 에이전트 예측, 2026 CIO 설문 에이전트 배포 17%.
  - MIT NANDA "GenAI Divide"는 2025-07 원본뿐, 2026년 후속 없음.

### 6-5. 마케팅 운영 근거
- [2025~2026] Ju & Aral, "Collaborating with AI Agents" (MIT) [논문-프리프린트, 현장실험] arXiv 2503.18238 (v3 2026-02-05): 참가자 2,234명, 광고 11,024개, X에서 약 500만 노출로 검증. 사람+AI 팀은 1인당 광고 50% 더 생산, 텍스트 품질도 높음. 이미지 품질은 사람끼리 팀이 우세. AI에 맡길수록 결과물 다양성 감소.
- [2026] Daviet(INSEAD) & Nishimura, Marketing Science (techxplore 보도 2026-08) [논문, 언론 경유]: 인스타그램 실캠페인에서 AI 광고 CTR 0.98% 대 사람 디자이너 0.65%. 18개월 뒤 재검증 3.38% 대 3.24%. **단 브랜드 기준 검수와 현장 테스트는 사람이 함.** 회사 1곳, 플랫폼 1개.
- [2026] Salesforce State of Marketing (2026-02-19, n=4,450) [벤더 설문] https://www.salesforce.com/news/stories/state-of-marketing-2026/ : AI 도입 75%. 병목은 데이터 단절, 데이터 통합된 곳은 에이전트 활용 가능성 60% 높음.
- HubSpot 2026 SVP 발언: "more content is generated by AI than by humans. But it's mostly average."
- 마케팅 에이전트 실사고 사후분석은 기업 공식 발표에서 못 찾음.
- 측정 근거상 사람 검토가 필요한 지점: 브랜드 적합성과 이미지 품질(INSEAD, MIT), 최종 수용 판정(RLI), 검증 역할 자체(TeamBench), 자율 발행의 평판 사고(Andon FM), 가격과 할인과 예산 결정(Vend, Andon Café).

---

## 7. 인용하면 안 되는 수치 (출처 추적 실패)

- "47개 배포 중 68%는 단일 에이전트로 충분": 원출처 못 찾음
- "대기업 마케팅팀 34%가 자율 에이전트를 프로덕션에서 운영"(Salesforce 출처로 인용됨): Salesforce 원문에 없음
- 마케팅 블로그의 "90.2% better": 2025년 Anthropic 리서치 시스템 수치를 잘못 옮긴 것
- "45% 실패율" 류 에이전시 블로그 수치: 출처 불명
- Anthropic "2026 Agentic Coding Trends Report"의 "81% 대 52% retention": 양식 제출 뒤 열람이라 확인 못 함

## 8. 원문을 못 읽은 것

- openai.com 블로그와 GDPval 페이지(403), Gartner 2026 보도자료(403), McKinsey 2026 PDF(타임아웃), OSWorld 1 리더보드(JS 로드)
- GPT-5.6 출시일, NoLiMa 수치, OrchestraBench의 "Sonnet 4.6" 언급
- 이 문서의 `[재확인]` 표시가 없는 인용문 전부(WebFetch 요약 경유)
