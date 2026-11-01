# SDD (spec-kit) 에이전트 코딩 실전기

- URL: https://tech.kakaopay.com/post/ifkakao-agentic-coding/
- 게시일: 2026. 3. 13
- 저자: wayne.cai (웨인). 자기소개 "뭐든지 즐겁게 일하는 서버 개발자 웨인입니다!", 본문에서 "AI 플랫폼팀 wayne"
- 리뷰어 한줄평: will.109, geuru.geon
- 태그: ifkakao, ifkakao(25), AI, 바이브 코딩, 에이전틱 코딩, SDD, Spec-kit
- 소속: 카카오페이 (AI 플랫폼팀). if(kakao)25 발표 연계 글.
- 원문 고지: "본 자료에는 생성형 AI를 일부 사용한 콘텐츠가 포함되어 있습니다."
- 읽은 방법: curl 원본 HTML에서 본문 전문 추출, 본문 스크린샷 17장 전부 직접 확인. 스크린샷에 본문 텍스트에 없는 정보(모델명, 산출물 파일 목록, analyze 결과 수치 등)가 많음.

## 핵심 한 문장

제어되지 않은 에이전틱 코딩은 프로젝트가 고도화될수록 무분별한 코드 생성과 환각을 낳으므로, GitHub Spec-kit으로 constitution → specify ↔ clarify → plan → tasks → analyze → implement 단계를 밟고, 산출물이 마음에 안 들면 직접 고치지 말고 스펙(specify)으로 돌아가 재생성하는 SDD 방식으로 팀 단위 일관성을 확보한다.

## 배경과 문제

- 팀은 AI 모델을 배포하고 사용하는 AI Platform을 구축하며 에이전틱 코딩을 적극 활용해 개발 기간을 크게 단축.
- 개발 초기, 중기, 후기 단계별 AI 협업 전략으로 환각을 최대한 제어하고, 개발자는 "구체적인 로직 사용을 강제하는 지휘자 역할"을 수행.
- 그러나 엔터프라이즈 시스템에서 고려할 게 많았고, 후반으로 갈수록 "여기저기 막 생성되는 코드"를 줄이기 위한 프롬프트와 노력이 필요. 마지막 단계에서는 AI 생성 코드를 검토하고 수정하는 시간이 점점 길어짐.
- 거의 모든 AI 코딩 도구가 "스펙을 정의하여 한 단계씩 업무를 수행하는 방식"을 채택하는 추세라 Spec-kit 도입.
- 이전 바이브 코딩의 문제(장점 절에서 언급): 프롬프트만으로 지시하다 보니 AI가 맥락을 잃기 쉽고, 대화가 길어질수록 이전 코드 패턴을 기억 못 해 여기저기 다른 스타일 코드 생성.

## 구조와 구성요소

- 도구: GitHub Spec-kit (Specify CLI). 설치 전제: uv.
  - 설치: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
  - 새 프로젝트: `specify init <PROJECT_NAME>`, 기존 프로젝트: `specify init --here` (보통 이것을 씀).
  - 스크린샷 기준 버전: release v0.0.90, 템플릿 spec-kit-template-copilot-sh-v0.0.90.zip, 스크립트 타입 sh.
- 에이전트 호스트: init 시 AI 어시스턴트 선택. 스크린샷 선택지: copilot(GitHub Copilot), claude(Claude Code), gemini(Gemini CLI), cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, codebuddy, qoder, roo, q(Amazon Q Developer CLI), amp, shai, bob(IBM Bob). 저자는 copilot 선택.
- 모델: 스크린샷의 채팅 입력창에 "Claude Opus 4.5"가 선택되어 있음(본문 텍스트에는 모델명 없음). 모드 드롭다운은 Agent/Ask/Edit/Plan, 그 아래 speckit 명령들이 커스텀 에이전트로 등록되어 있음.
- 명령(슬래시 커맨드): /speckit.constitution, /speckit.specify, /speckit.clarify, /speckit.plan, /speckit.tasks, /speckit.analyze, /speckit.implement. 스크린샷에는 추가로 /speckit.checklist("Generate quality checklists to validate requirements completeness, clarity, and consistency (after /speckit.plan)"), /speckit.taskstoissues 가 보이고, analyze 결과 화면에는 "/speckit.do T001" 도 제시됨.
- 단계별 역할(원문 정의):
  - constitution: 시스템의 최상위 규칙 정의(코드 스타일, 테스트 커버리지, 문서화 요구사항 등). 결과 constitution.md는 spec, tasks, plan 등 다른 단계에서도 쓰는 대원칙.
  - specify: 이번에 개발할 구체적 스펙 정의(API 엔드포인트, 데이터 모델, 비즈니스 로직 등).
  - clarify(선택): 요구사항을 더 명확히 할 때. 스펙 분석 결과와 명확화 질문을 최대 5개까지 제안. 문답이 끝나면 스펙 문서 업데이트.
  - plan: constitution과 스펙을 바탕으로 개발 계획 생성. data model 정의 포함.
  - tasks: constitution, spec, plan을 바탕으로 구체 작업 생성. tasks.md에 작업 세부사항과 완료 기준 포함.
  - analyze: constitution 기준으로 spec, plan, task가 잘 작성됐는지, 서로 모순은 없는지 분석하고 수정사항 제안. 스크린샷 툴팁 "Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation."
  - implement: constitution, spec, plan, tasks를 바탕으로 개발. 진행 중 tasks.md가 업데이트되며 task별 완료 표시.
- MCP 연동: specify 단계에서 피그마 MCP나 스펙이 적힌 위키 MCP를 함께 호출 가능. 채팅창의 클립 아이콘으로 MCP를 미리 정의해 두면 편리(스크린샷: 첨부 칩 "com.figma.mcp/mcp", "spec.md"). implement 단계에서 tasks에 정의된 MCP 호출까지 수행.
- 실제 예제 기능: AI Platform 플레이그라운드 화면에 비교 모드(Compare Mode) 추가. 기존 Chat 탭 옆에 Compare 탭을 만들어 두 AI 모델(A/B)을 동시에 테스트하고 응답 비교.
- 스크린샷에서 확인되는 산출물 구조:
  - 브랜치 `001-playground-compare`, 스펙 폴더 `/specs/001-playground-compare/`
  - plan 단계 산출물: plan.md(구현 계획서, 4.5KB), research.md(Phase 0 연구 결과, 5.8KB), data-model.md(데이터 모델 정의, 5.4KB), contracts/compare-api.yaml(API 계약서), quickstart.md(빠른 시작 가이드, 5.6KB)
  - tasks.md 포맷: `[ID] [P?] [Story?] 설명`, [P]는 병렬 실행 가능(다른 파일, 의존성 없음), [Story]는 해당 유저 스토리(US1, US2), 정확한 파일 경로 포함. 경로 규칙 섹션(Frontend, E2E Tests, Components 경로). Phase 1 Setup, Phase 2 Foundational("이 단계 완료 전에는 유저 스토리 구현 불가", 체크포인트 명시), Phase 3부터 User Story별(Priority P1, MVP 표시), Phase 10 Figma Design Compliance(User Story 7) 까지 존재.

## 절차와 규칙

- 흐름: `constitution → specify ↔ clarify → plan → tasks → analyze → implement`
- 핵심 규칙: "각 단계에서 마음에 안 드는 부분이 있다면 직접 수정하지 않고 specify 로 돌아가 스펙을 재정의하는 것이 좋습니다." 직접 수정하면 스펙 문서와 실제 코드/계획이 불일치해 일관성 원칙에 어긋나고 나중에 개발자들이 혼란스러워함.
- constitution 작성법: 프롬프트를 잘 쓸 필요 없고 필요한 요소를 다 적는 것이 중요. 정리는 에이전트가 함. 저자는 현재 프로젝트 구조를 읽고 원칙을 세워달라고 주문. 마지막에 "한글로 해달라"고 덧붙여야 알아보기 쉬움.
  - 스크린샷의 실제 constitution 프롬프트 내용: 프로젝트는 ai model을 서빙하는 ai platform, 파이썬 백엔드와 react 프론트엔드, 주요 라이브러리를 검색해서 명시, 파일과 폴더 구조를 파악해 테스팅과 공용 라이브러리 위치를 명확히 정의, 각 서비스 로직이 들어가는 부분 정의, 앞으로 개발은 TDD의 Red Green으로 진행, 개발 완료 후 다시 코드리뷰를 해서 공통 로직이나 리팩토링할 것이 있는지 검사해 마무리하는 과정 포함, 한글 작성.
  - analyze 스크린샷에 드러난 constitution 원칙 7개: I. TDD 주도 개발, II. Tidy First, III. 순환 참조 금지, IV. 한글 사용, V. 모노레포 구조, VI. 표준 준수, VII. 코드 품질. plan 결과에 "Constitution Check: 모든 7개 원칙 PASS".
- specify 작성법: 깔끔하게 적으려 하지 말고 요구사항을 최대한 많이 적음. "정말 두서없이" 적어도 정리는 spec-kit이 함. 생성된 스펙을 검토해 AI가 놓치거나 잘못 이해한 부분을 바로잡음(예: 피그마 디자인 링크 누락 → 추가 요청).
- clarify: 저자는 보통 한두 번. "한글로 진행해 달라"고만 하고 실행. 기획문서나 요구사항에서 우리가 못 찾은 점을 찾아줘서 기획자와 함께 보기에도 유용.
- plan: `/speckit.plan 한글로 진행해`. data model이 마음에 안 들어도 직접 수정보다 /speckit.specify로 다시 정의해 AI가 수정하게.
- tasks: `/speckit.tasks 한글로 작성해`. 마음에 안 드는 작업은 역시 specify로 돌아가는 게 원칙. 단 예외: specify 수정만으로 안 될 때가 있음(예: spec에는 피그마 MCP가 있는데 tasks에는 피그마 작업 누락). 이때는 tasks.md를 참조해 직접 프롬프팅: `/speckit.tasks tasks에 피그마 mcp를 직접 사용하는 작업을 추가해줘`. 이 경우 작성된 스펙과 일치하는지 반드시 확인.
- analyze: implement로 바로 갈 수도 있지만 저자는 먼저 `/speckit.analyze 한글로 작성해`. 결과 제안을 수용할지 선택. 저자는 수정하는 편. 수정 요청 시 모순 부분과 필요한 task까지 변경.
- implement: `/speckit.implement 한글로 진행해`. 이후 "기다림의 시간".
- implement 주의: AI가 tasks에 중점을 두는 것처럼 느껴져 constitution을 가끔 안 지킴. 이럴 땐 constitution에 기반해 tasks가 잘 생성됐는지 다시 체크.

## 수치와 결과

- 본문 텍스트 수치: clarify 질문 최대 5개. 그 외 정량 성과(기간 단축률 등)는 본문에 없음("개발기간을 크게 단축"이라는 정성 표현만).
- 스크린샷 수치(예제 1건 기준):
  - clarify 스펙 분석: 6개 User Story, 15개 요구사항, 4개 엣지 케이스, 6개 측정 가능한 성공 기준. 8개 카테고리 중 6개 Clear, 2개 Partial(Non-Functional Quality Attributes: 성능 목표 일부만 정의, Constraints & Tradeoffs: 기술적 제약 명시 부족). 질문은 1/1개(프롬프트 동시 전송 시 A/B 응답 동기화 정책, 추천 Option A 독립 표시).
  - analyze Metrics: 총 요구사항 15개(FR-001 ~ FR-015), 총 태스크 29개, 커버리지 100%(모든 요구사항에 1개 이상 태스크 연결), 모호성 1개(LOW), 중복 0개, 불일치 2개(MEDIUM), CRITICAL 0, HIGH 0, MEDIUM 2, LOW 4. Unmapped Tasks 없음.
  - analyze Constitution Alignment: TDD 주도 개발 MEDIUM(테스트가 Phase 9에 배치되어 Red→Green→Refactor 미준수 가능성), 테스트 위치 규칙 MEDIUM(plan.md는 tests 경로, tasks.md는 e2e만 사용), 나머지 원칙 PASS.
  - implement 화면: Playground 컴포넌트 1301줄, Todo 9개 생성(Todos 1/9), T001과 T002 병렬 생성.

## 실패, 한계, 주의점

- 저자가 직접 든 단점:
  - constitution, spec, plan, tasks, implement 단계가 많아 처음 접하는 개발자에게 다소 복잡.
  - 간단한 개발은 어떻게 해야 할지 애매. specify를 수정할지 그냥 agent 모드로 수정할지 판단이 개발자마다 다를 수 있음.
  - 파이프라인을 거치면 개발 문서가 굉장히 많이 생기고 토큰도 많이 소모(문서는 반대로 장점일 수도).
- 스펙에 정의된 MCP가 tasks로 전파되지 않는 누락이 실제로 발생(피그마 사례). specify 수정만으로 안 고쳐짐.
- implement 단계에서 constitution을 가끔 안 지킴(tasks 중심으로 동작하는 느낌).
- analyze 스크린샷에서도 최초 tasks가 TDD 원칙과 어긋나게(테스트가 Phase 9) 생성되었음이 드러남.
- "Spec-kit으로 모든 것을 해결할 수는 없습니다."
- init 화면의 보안 경고(스크린샷): 일부 에이전트가 프로젝트 내 에이전트 폴더에 자격증명, 인증 토큰 등을 저장할 수 있으니 .github/ (또는 일부)를 .gitignore에 추가 고려.

## 그림 설명

1. init01: 기존 저장소(`~/IdeaProjects/kpap_readonly/kpap`, main 브랜치)에서 `specify init --here` 실행. "GitHub Spec Kit - Spec-Driven Development Toolkit" 배너, "Current directory is not empty (38 items). Template files will be merged with existing content and may overwrite existing files" 경고와 계속 여부 질문.
2. init02: "Specify Project Setup" (Project kpap). "Choose your AI assistant" 목록 17종(copilot, claude, gemini, cursor-agent, qwen, opencode, codex, windsurf, kilocode, auggie, codebuddy, qoder, roo, q, amp, shai, bob).
3. init03: copilot, sh 선택 후 초기화 단계 체크리스트(Check required tools, Fetch latest release v0.0.90, Download template, Extract, Ensure scripts executable, Initialize git repository: existing repo detected, Finalize). "Agent Folder Security" 경고. Next Steps: /speckit.constitution, specify, plan, tasks, implement. Enhancement Commands(선택): /speckit.clarify(plan 전), /speckit.analyze(tasks 후 implement 전, cross-artifact consistency), /speckit.checklist(plan 후, 요구사항 완전성 검증 체크리스트).
4. init04: IDE 채팅 모드 메뉴. Agent/Ask/Edit/Plan 아래 speckit.analyze, checklist, clarify, constitution, implement, plan, specify, tasks, taskstoissues 커스텀 에이전트. 모델 선택 "Claude Opus 4.5".
5. constitution: `/speckit.constitution` 입력 프롬프트 원문(위 절차 절에 요약). 첨부 칩 `.env.sandbox`, 모델 Claude Opus 4.5.
6. specify01: `/speckit.specify` 입력. 첨부 `com.figma.mcp/mcp`, `spec.md`. 두서없는 요구사항: 플레이그라운드에 비교모드, Chat 탭과 Compare 탭 전환, 피그마 URL(node-id=4131-61300), 아이콘 기능(새로고침, 프롬프트 불러오기, 스트리밍모드, 프롬프트 저장하기, 새비교), "Chat 모드 플레이그라운드와 동일", 프롬프트 불러오기 버튼 → 아이콘, 호버 툴팁, Compare 모드 프롬프트 저장 플로우는 Chat과 동일, A/B 각각 따로 저장, 비교 결과 디자인 URL.
7. specify02: 생성된 spec 일부. 개요, "User Scenarios & Testing", User Story 1 비교모드 탭 전환(Priority: P1), "Why this priority", "Independent Test", Acceptance Scenarios를 Given/When/Then 3개로 작성. User Story 2 A/B 모델 설정 및 비교 실행(P1) 시작.
8. specify03: "스펙에 구체적인 피그마 디자인링크도 첨부했어?" 질문에 에이전트가 spec.md 1~50줄을 읽고 Figma 링크 누락을 발견, spec.md +7 -0 수정, "Design References (Figma)" 표(Compare 모드 초기 화면: playground_compare, 비교 결과 화면: playground_compare (with results)) 추가. 다음 단계로 /speckit.plan 안내.
9. specify04: spec.md 안의 Design References 마크다운 표 원문(node-id 4131-61300, 4131-61466).
10. clarify01: specify 후 "PROCEED FROM SPECKIT.SPECIFY" 버튼 두 개(Build Technical Plan, Clarify Spec Requirements). 입력 `/speckit.clarify 한글로 진행해줘`, 첨부 figma mcp와 spec.md.
11. clarify02: "ambiguity & coverage scan" 결과 표 8개 카테고리(Functional Scope & Behavior, Domain & Data Model, Interaction & UX Flow, Edge Cases & Failure Handling, Terminology & Consistency, Completion Signals, Non-Functional Quality Attributes, Constraints & Tradeoffs)와 상태, 질문 1/1(A/B 응답 동기화 정책), Recommended Option A, 선택지 A(독립 표시)/B(동기 표시)/Short(5단어 이하 직접 입력). "Reply with option letter..." 안내.
12. plan02: "Plan 완료 보고". 브랜치 001-playground-compare, 생성 산출물 표(plan.md, research.md, data-model.md, contracts/compare-api.yaml, quickstart.md와 크기). Phase 0 연구 결과 요약: 컴포넌트 구조(기존 Playground.tsx → 탭 기반 리팩토링, ChatMode/CompareMode 분리), 상태 관리(useCompareMode 커스텀 훅), API 호출(Promise.allSettled 병렬 호출, 패널 독립 렌더링), UI 재사용(기존 컴포넌트, 테마만 props 주입), 백엔드 변경(불필요, 기존 invoke API 재사용). "Constitution Check 모든 7개 원칙 PASS". 다음 단계 /speckit.tasks.
13. tasks01: tasks.md 앞부분. Input `/specs/001-playground-compare/`, Prerequisites(plan.md, spec.md, research.md, data-model.md, contracts/ 모두 체크). 포맷 규칙, 경로 규칙(kpap_console/frontend/src/, e2e/, components/Playground/). Phase 1 Setup(T001 [P] 타입 정의, T002 [P] 색상/상수 정의), Phase 2 Foundational(T003 useCompareMode 훅, T004 Playground.tsx 탭 UI 래퍼 리팩토링, "이 단계 완료 전에는 유저 스토리 구현 불가", 체크포인트), Phase 3 User Story 1(P1, MVP, 독립 테스트 기준, T005~T008 [US1] 파일 경로 포함).
14. tasks02: 추가된 "Phase 10: Figma Design Compliance (User Story 7)". 중요 지시 "이 Phase의 모든 태스크는 반드시 Figma MCP 도구를 사용하여 최신 디자인 정보를 직접 가져와야 합니다. 수동으로 색상/크기 값을 추출하거나 하드코딩하지 마세요." Figma MCP 사용 방법(mcp_com_figma_mcp_get_design_context를 nodeId 4131-61300, 4131-61466로 호출, 색상/크기/라운드/폰트 추출, 컴포넌트 스타일 업데이트). 태스크 T033 [P] [US7] Figma MCP로 디자인 토큰 추출(FIGMA_COLORS, FIGMA_SIZES, FIGMA_RADIUS), T034 PlaygroundTabs 스타일 적용, 둘 다 [X] 완료 표시.
15. analyze01: Constitution Alignment Issues 표(위 수치 절), Unmapped Tasks 없음, Metrics 표, Next Actions 권장 조치(MEDIUM A1: plan.md의 tests/components/Playground/CompareMode.test.tsx 참조를 tasks.md와 일치시키거나 Unit 테스트 태스크 추가, 옵션 A/B. MEDIUM D1: TDD 원칙과 tasks.md 구조 조정, 옵션 A 각 Phase에 테스트 우선 태스크 추가(엄격한 TDD), 옵션 B "테스트는 E2E 중심으로 최종 단계에서 작성" 명시(실용적 접근). LOW는 구현 중 해결 가능). "CRITICAL 이슈 없음 → /speckit.implement 진행 가능. MEDIUM 2개는 기능 구현을 차단하는 수준은 아님."
16. analyze02: 수정 내역 요약. 1번 A 적용: Unit 테스트 태스크 추가(T005 PlaygroundTabs 테스트, T010 CompareMode 테스트, T011 useCompareMode 훅 테스트). 2번 A 적용: TDD-First 구조, 각 User Story Phase에서 테스트 태스크를 구현 태스크 앞에 배치(Phase 3: T005 → T006~T009, Phase 4: T010~T011 → T012~T018). Next Actions: 모든 CRITICAL/HIGH/MEDIUM 해결, 구현 시작 `/speckit.implement` 또는 `/speckit.do T001`, MVP 범위 T001~T018(Phase 1~4), TDD 사이클(테스트 먼저 실행 → 실패 확인 → 구현 → 통과 확인). "분석 결과: PASS, 모든 artifacts가 일관성 있고, TDD 원칙을 준수하며, 구현 준비 완료".
17. implements01: implement 실행 로그. Playground.tsx 1~100줄 읽기, "Playground 컴포넌트가 1301줄로 상당히 큽니다" 후 추가 컨텍스트 확인, "Created 9 todos", Phase 1 Setup 시작, T001과 T002 병렬 생성, Todos(1/9) 목록 T001~T006.

## 원문 인용

1. "에이전틱 코딩은 개발을 엄청 효율화시켜주지만 제어되지 않은 에이전틱 코딩을 프로젝트가 고도화될수록 무분별한 코드 생성과 환각이라는 숙제를 안겨줍니다."
2. "개발초기, 중기, 후기의 단계별 AI의 협업전략으로 최대한 환각을 제어하고 개발자는 구체적인 로직 사용을 강제하는 지휘자 역할을 수행하여 개발을 하였습니다."
3. "결국 마지막 단계에서는 AI가 생성한 코드를 검토하고 수정하는 시간이 점점 더 길어졌습니다."
4. "※ 각 단계에서 마음에 안 드는 부분이 있다면 직접 수정하지 않고 specify 로 돌아가 스펙을 재정의하는 것이 좋습니다."
5. "이때 너무 프롬프트를 잘 쓸 필요는 없습니다. 다만 필요한 요소를 다 적는 것이 중요합니다. 정리는 에이전트에서 해줍니다."
6. "만약 직접 수정하게 되면 스펙 문서와 실제코드/계획이 불일치하여 일관성 유지 원칙에 어긋나며 나중에 스펙문서를 보고 개발자들이 혼란스러워 할 수 있습니다."
7. "하지만 실무를 진행하다 보면 specify 수정만으로는 안될 때가 있습니다."
8. "이 작업을 하게 되면 constitution 기준으로 spec, plan, task들이 잘 작성이 되었는지 서로 모순은 없는지 분석해 줍니다."
9. "여기서 느낀 점은 AI가 코드를 생성할 때 tasks에 중점을 두는 것처럼 느꼈습니다. 그래서 constitution에 있는 말을 가끔 안 들을 때도 있습니다."
10. "일단 파이프라인을 거치면 개발문서가 굉장히 많이 만들어 집니다 이에 따른 토큰도 많이 소모합니다."
11. "협업환경에서 다른 개발자가 어떤 작업을 했는지 스펙문서를 통해서 명확하게 알 수 있습니다."
12. "보안이나 테스팅 같은 일관성이 중요한 요소들을 constitution 에 명확히 정의하고 tasks에 작업을 넣는지 안넣었는지 바로 알 수 있고 추가할 수 있습니다."
13. "앞으로 AI가 코드를 대신 작성해 주는 시대가 본격화되면 개발자의 역할은 ‘코드를 작성하는 사람’에서 ‘스펙을 검증하고 테스트를 설계하는 사람’으로 점점 변화할 것이라고 생각합니다."

## 우리 설계에 쓸 만한 점

- [추론] 기획 역할의 산출물 체인을 spec-kit 단계와 1:1로 맞출 수 있다: constitution(부서 공통 대원칙) → spec → clarify 질문 → plan(+research, data-model, contracts) → tasks → analyze → implement. 각 단계 산출물을 파일로 남기면 문서관리 역할이 추적할 대상이 명확해진다.
- [추론] constitution은 모든 부서 에이전트가 참조하는 최상위 규칙 파일로 두고, 부서별(마케팅/개발/운영) constitution을 분리할지 공통 하나로 둘지 결정해야 한다. 원문은 프로젝트당 하나.
- [추론] "산출물이 마음에 안 들면 직접 고치지 말고 스펙으로 돌아가 재생성" 규칙은 오케스트레이터의 되돌림 규칙으로 옮길 수 있다. 검수에서 반려되면 제작 산출물을 패치하지 않고 기획(spec) 단계로 되돌린다. 단 원문도 예외(스펙 수정으로 안 되는 전파 누락)를 인정했으므로 예외 경로(하위 산출물 직접 수정 후 스펙 일치 확인)를 명시해야 한다.
- [추론] analyze 단계는 검수 역할의 "제작 전 검수" 버전이다. constitution 대비 spec, plan, tasks의 교차 일관성, 요구사항 커버리지(모든 요구사항에 태스크 연결), 미매핑 태스크, 심각도(CRITICAL/HIGH/MEDIUM/LOW)를 내고, CRITICAL 0이 아니면 implement 진입을 막는 게이트로 쓸 수 있다. 원문 스크린샷의 게이트 문구가 "CRITICAL 이슈 없음 → implement 진행 가능".
- [추론] clarify는 기획 역할이 사람(기획자, 요청자)에게 최대 5개의 구조화된 질문과 추천안을 내는 단계로 쓸 수 있다. 사람 검토 지점을 "모든 산출물"이 아니라 "모호성 질문"과 "analyze 결과 수용 여부"에 집중시키는 설계.
- [추론] tasks 포맷([ID] [P] [Story] 설명 + 정확한 파일 경로, Phase, 체크포인트, "이 단계 완료 전 다음 단계 불가")은 오케스트레이터가 병렬 분배와 순서 제어에 그대로 쓸 수 있는 기계 판독 형식이다.
- [추론] implement 단계에서 constitution이 무시되는 현상은 "상위 규칙은 태스크 텍스트에 내려와 있어야 지켜진다"는 뜻으로 읽힌다. 따라서 constitution 원칙을 각 task에 명시적으로 주입하거나, 원칙 위반을 Hook(테스트 존재 여부, 경로 규칙)으로 검사하는 편이 안전하다. ai-agent-1의 "프롬프트는 확률, Hook은 보장"과 같은 방향.
- [추론] MCP 사용 지시가 spec에서 tasks로 전파되지 않은 사례는, 도구 사용 요구를 태스크 단위에 명시하고(예: "반드시 Figma MCP로 가져올 것, 하드코딩 금지") 검수 역할이 태스크별 도구 호출 여부를 확인하는 체크가 필요함을 보여준다.
- [추론] 단계가 많고 문서, 토큰이 많이 든다는 단점 때문에, 작은 작업은 SDD 전체를 타지 않는 경량 경로를 오케스트레이터가 판별해야 한다. 원문은 이 판단이 "개발자마다 다를 수 있다"고만 했고 기준은 주지 않았다.
- [추론] 모델 배치 참고: 원문 스크린샷의 실사용 모델은 Claude Opus 4.5(무거운 모델)이며 모든 speckit 단계가 같은 모델로 돈 것으로 보인다. 역할별 모델 분리 근거는 이 글에는 없다.
