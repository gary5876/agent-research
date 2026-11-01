# Claude Code 계열 오픈소스 마스터/오케스트레이터 프로젝트 조사

- 조사일: 2026-09-28
- 목적: Claude Code 위에 부서 에이전트를 거느리는 마스터 오케스트레이터를 만들 때 참고할 오픈소스 구현을 찾고, 설계와 평판과 위험을 평가

## 조사 방법과 한계
- 후보 수집: `gh search repos`로 여러 문구 검색("claude code orchestrator", "claude code multi-agent", "claude-flow", "ruflo", "oh-my-opencode", "oh-my-claudecode", "SuperClaude", "gastown", "get-shit-done", "BMAD", "claude squad", "agent orchestrator master agent"), awesome-claude-code 목록의 오케스트레이션 관련 항목, obra/superpowers와 revfactory/harness는 지정 대상으로 직접 확인.
- 저장소 수치(별, 마지막 push, 보관 여부, 라이선스, 최신 릴리스, 기여자 집중도)는 조사 시점 `gh api` 응답 기준. 별 수는 인기 지표일 뿐 품질 증거가 아님.
- 설계 설명은 README와 마스터 프롬프트/정의 파일을 `gh api .../contents`로 받아 직접 읽은 부분만 적음. 저장소 전체 코드를 정독한 것은 아니므로 읽지 않은 파일에 다른 장치가 있을 수 있음.
- 외부 평판은 GitHub 이슈 검색(키워드: cost, token, loop, stub, fake, security 등)과 웹 검색. 웹 검색 결과를 본문까지 읽지 못하고 검색 요약만 본 경우 "(검색 요약만)"으로 표시. 키워드 검색이므로 관련 이슈를 전부 찾았다는 뜻이 아님.
- 위험한 설정(권한 우회 실행 옵션, 권한 허용 목록, 훅 명령줄, 원격 스크립트 실행 설치법)은 원문을 옮기지 않고 한국어로만 서술함.
- [추론] 표시가 붙은 문장은 원문에 없는 내 해석.

---

## 1. obra/superpowers: subagent-driven-development (SDD)

- 저장소: https://github.com/obra/superpowers
- 수치(gh api): 별 292,177, 마지막 push 2026-09-27, 생성 2025-10-09, 보관 아님, MIT, 최신 릴리스 v6.4.2(2026-09-25), 열린 이슈+PR 268
- 기여자 집중도: 상위 100명 커밋 합 657 중 obra 525(약 80%), arittr 79, clkao 8. 사실상 1인 주도.
- 성격: 독립 실행 프로그램이 아니라 Claude Code 플러그인 형태의 스킬 묶음. 마스터는 "지금 세션의 Claude 자신"이고, 그 행동 규칙이 `skills/subagent-driven-development/SKILL.md`와 3개 프롬프트 템플릿(implementer, task-reviewer, re-review)에 들어 있음. 이 조사에서 원문을 직접 읽은 파일은 SKILL.md 전체, implementer-prompt.md 앞부분, hooks/hooks.json.

### 마스터(컨트롤러)가 하는 일
- 입력은 이미 쓰인 계획 파일(writing-plans 스킬 산출물). 컨트롤러는 계획을 한 번 읽고, 과제마다 "새 구현 서브에이전트 1개 투입, 과제 리뷰 1회, 필요 시 수정 루프", 모든 과제가 끝나면 브랜치 전체 최종 리뷰.
- 착수 전 사전 점검: 과제 쌍마다 "공유 파일/인터페이스, 한쪽이 만드는 것과 다른 쪽이 쓰는 것"을 표로 만들어 원장에 기록하고, 충돌은 실행 전에 판정. 원문: "The scan's output is a table, not a verdict."
- 계획 자체는 이 스킬이 아니라 앞 단계(brainstorming, writing-plans)가 담당. SDD는 실행 조율 전용.
- 직접 수정 금지: "Never fix findings yourself in the controller session". 컨트롤러 컨텍스트를 조율 전용으로 비워두는 것이 원칙.
- 병렬 금지: "Never dispatch multiple implementation subagents in parallel (conflicts)."

### 하위 에이전트 지시 방식(위임 템플릿 필드)
- 과제 본문은 스크립트로 별도 brief 파일에 뽑아 두고, 지시문은 다섯 요소만 담음: (1) 이 과제가 프로젝트에서 차지하는 위치 한 줄, (2) brief 파일 경로("read this first, it is your requirements"), (3) 앞 과제에서 정해진 인터페이스와 결정, (4) brief의 모호함에 대한 컨트롤러의 해석, (5) 보고서 파일 경로와 보고 계약.
- 정확한 값(숫자, 시그니처, 테스트 케이스)은 brief에만 둠. 누적 히스토리 붙여넣기 금지. 근거로 든 실제 사례: 지시문이 42k자였고 그중 99%가 과거 요약이었다는 것(프로젝트 자체 관찰, 독립 검증 없음).
- 모델 필드 필수: 생략하면 세션의 가장 비싼 모델을 물려받는다고 경고. 기계적 과제는 싼 모델, 통합 판단은 표준, 설계와 최종 리뷰는 최상위. "Turn count beats token price"라며 리뷰어와 산문형 과제의 하한은 중간 등급으로 둠.
- 하위 에이전트의 재위임 금지: 구현자는 서브에이전트나 리뷰어를 스스로 띄우지 않음("You Do Not Dispatch Subagents").
- 보고 상태 4종: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED. BLOCKED면 같은 모델로 그대로 재시도하는 것을 금지하고 컨텍스트 추가, 모델 상향, 과제 분할, 계획 수정 중 하나를 고르게 함.

### 상태 저장
- 계획별 작업 공간(`.superpowers/sdd/` 아래, git 무시 대상)에 `progress.md` 원장, brief, 보고서, 리뷰 패키지를 파일로 둠. 원장 첫 줄에 계획 파일 경로를 적어 다른 계획의 원장과 구분.
- 압축(compaction) 후엔 기억보다 원장과 git log를 믿으라고 명시. 이유로 든 관찰: 위치를 잃은 컨트롤러가 이미 끝난 과제들을 통째로 재투입한 것이 "the single most expensive failure observed".
- 끝나면 작업 공간을 삭제하고 git 이력을 기록으로 남김.

### 완료/검증 규칙과 재시도 상한
- 과제 완료 조건: 리뷰어가 스펙 준수와 품질 두 판정을 모두 내야 함. 구현자 자기 검토는 리뷰를 대체하지 못함.
- 리뷰어 입력은 brief, 구현 보고서, 스크립트가 만든 diff 패키지 세 파일과 전역 제약. 컨트롤러가 "이건 지적하지 마" 식으로 리뷰를 미리 재단하는 것을 금지.
- 수정 루프 상한 5회: 1~3회는 같은 구현자 재개, 4~5회는 새 구현자에 한 등급 위 모델. 5회 후에도 남은 지적은 컨트롤러가 판정해 "보류(parked)" 또는 "판정 후 다음 과제로 전달". 최종 리뷰의 수정은 한 번의 일괄 수정과 한 번의 재리뷰만 허용.
- 판정 기록 형식: `Ruling: <무엇을 결정> | <왜> | <틀리면 비용>`. 마지막 보고에 모든 Ruling을 빠짐없이 나열해야 함.

### 사람 개입 지점
- 기본은 "멈추지 말고 계속"이며 원문 표현은 "Rulings, not stalls. A running plan does not wait on a human." 멈추는 사유는 넷뿐: 되돌릴 수 없거나 파괴적인 작업, 보안 민감 작업, 작업 트리 밖 부작용(merge, 공유 브랜치 push, 배포), 모든 경로가 추측인 계획.
- main/master 브랜치에서 사람 동의 없이 구현 시작 금지.

### 설치하는 훅/가드(말로 서술)
- 세션 시작, 대화 초기화, 압축 직후에 플러그인 스크립트를 실행해 "using-superpowers" 안내를 컨텍스트에 다시 주입하는 SessionStart 훅 하나. 권한 우회 옵션이나 자동 허용 목록은 이 조사에서 본 파일에는 없었음.

### 독립적 평판과 이슈
- 비용: #1152(Codex에서 단순 계획 하나를 SDD로 돌렸더니 5시간 토큰 한도 전부 소진), #750(OpenCode+Codex에서 토큰 과다), #743(스킬 사용 후 응답 느려짐, 댓글 26), #512(brainstorming과 writing-plans 효율). 웹 검색 요약상 이슈 #1120은 "쉬운 과제에서 2단 리뷰 루프가 품질 개선 없이 토큰과 시간을 태우는 소용돌이"를 지적(검색 요약만).
- 게이트 우회: #463(컨트롤러가 리뷰어를 띄우지 않고 구현자 자기 확인만 믿고 다음 과제로 넘어감, #995에도 같은 보고). 메인테이너는 v6 재설계에서 리뷰 패키지 기계 생성과 "리뷰어 출력 영수증"을 추가했다며 닫았고, v6 이후 재발 보고는 없다고 적음(메인테이너 주장, 독립 검증 없음).
- 압축 후 망각: #147(자동 압축 후 리뷰 단계를 잊음). 원장 파일 설계가 이 문제의 대응으로 보임 [추론].
- 보안 스캐너: #2181, Hermes 에이전트의 플러그인 설치 보안 검사가 superpowers를 "dangerous"로 차단. 메인테이너 측은 스캐너 오탐으로 봄.
- 이슈 트리아지를 Claude 에이전트가 메인테이너 계정으로 수행한다고 댓글에 명시(#2181).

### 측정 주장 vs 독립 검증
- 릴리스 노트의 "6.0에서 약 2배 빠르고 토큰 약 50% 절감"은 프로젝트 자체 측정(웹 검색 요약으로 확인, 측정 방법은 읽지 못함). 독립 재현은 찾지 못함.

### 공급망 위험(말로 서술)
- 설치 시 세션마다 셸 스크립트가 자동 실행되는 구조(SessionStart 훅). 플러그인 갱신이 곧 실행 코드 갱신이며, 1인 주도 저장소라 계정 탈취 시 영향 범위가 큼 [추론].

## 2. revfactory/harness

- 저장소: https://github.com/revfactory/harness
- 수치(gh api): 별 9,074, 마지막 push 2026-09-26, 생성 2026-03-26, 보관 아님, Apache-2.0, GitHub 릴리스 없음(README 배지상 v2.1.0), 열린 이슈 1
- 기여자 집중도: 커밋 47 중 revfactory 41(약 87%). 1인 저장소.
- 성격: 오케스트레이터 자체가 아니라 "오케스트레이터를 만들어 주는 메타 스킬". 사용자가 "하네스 구성해줘"라고 하면 도메인을 분석해 `.claude/agents/`(누가), `.claude/skills/`(어떻게 + 오케스트레이터 스킬 1개), CLAUDE.md 포인터를 생성. 한국어 자료가 원본. 이 조사에서 읽은 파일은 README_KO.md 전체와 `skills/harness/references/orchestrator-template.md` 전체. SKILL.md 본체(35KB)와 team-patterns.md 등은 읽지 않음.

### 마스터(생성되는 오케스트레이터 스킬)가 하는 일
- 실행 모드 3종 중 하나 또는 혼합을 문서 맨 위에 명시: A 워크플로 조율(Workflow 스크립트로 결정적 팬아웃과 검증), B 지속형 에이전트 협업(이름 붙인 에이전트 + SendMessage + 공유 작업 목록), C 서브에이전트 위임(단발 병렬 호출). 선택 기준은 "팀 크기가 아니라 제어 흐름의 형태".
- 팀 아키텍처 패턴 6종(파이프라인, 팬아웃/팬인, 전문가 풀, 생성-검증, 감독자, 계층적 위임)을 README에 제시.
- 공통 절차: 0단계 기존 작업 확인(`_workspace/` 유무로 최초 실행, 부분 재실행, 새 실행 분기) → 준비 → 실행 → 통합 → 보고. 1단계 작업 목록은 메인 에이전트가 직접 확정해 배열로 넘김.

### 하위 에이전트 지시 방식
- 템플릿 A: 에이전트 구성표(역할, agentType, 사용할 스킬, 산출물 schema 요약). 수집 결과는 항목마다 적대적 검증을 거쳐 통과분만 다음 단계로.
- 템플릿 B: `Agent(name, subagent_type, prompt: 역할 + 작업 지시 + 산출 경로)`와 `TaskCreate(title, assignee, depends_on)`. 팀원당 작업 3~6개 권장.
- 템플릿 C: 표(에이전트, subagent_type, 입력, 산출물 경로). "메인 에이전트는 이미 맡긴 검색을 다시 수행하지 않는다."
- 파일 이름 규칙 `{phase}_{agent}_{artifact}.{ext}`, 모드 전환 지점마다 데이터 전달 경로를 명시하라는 원칙.

### 상태 저장
- `_workspace/` 디렉터리가 상태의 전부. 워크플로 모드는 `run_meta.json`에 runId를 저장해 수정된 단계만 재개(바뀌지 않은 agent 호출은 캐시).
- 템플릿 B의 "산출물 동결": 단계 경계마다 모든 팀원 완료 확인 → 동결 통보(이후 수정은 새 버전 파일로) → 산출물 해시 기록 → 통합 직전 해시 재확인. 이유는 이름 있는 에이전트가 완료 후에도 메시지를 받아 이미 넘긴 파일을 고칠 수 있기 때문.

### 완료/검증 규칙과 재시도 상한
- 빈 결과를 성공으로 판단하지 말 것, 제외되거나 누락된 항목은 보고서에 반드시 밝힐 것, 충돌 데이터는 삭제하지 말고 출처와 함께 병기.
- 재시도: 서브에이전트 실패 시 한 번 재시도 후 누락을 밝히고 진행. 사용량 한도 소진, 인증 만료, 권한 거부처럼 재시도해도 같은 결과인 실패는 재시도 금지.
- 기본 에이전트 수 상한을 두고 사용자가 "철저히, 전수, 모두"를 요청할 때만 늘리게 함.
- 모든 오케스트레이터에 정상 1개 + 오류 1개 이상의 테스트 시나리오를 넣도록 강제.

### 사람 개입 지점
- 절반이 넘는 에이전트(팀원)가 실패하면 사용자에게 알리고 계속 여부 확인. 사용량 한도 도달 시 풀리는 시각과 함께 보고.
- 템플릿 A는 "스킬을 불러오면 Workflow 사용에 동의한 것으로 본다"고 적어, 실행 동의 게이트를 스킬 호출로 갈음함.

### 설치하는 훅/가드
- 이 조사에서 읽은 파일에는 훅, 권한 설정, 자동 허용 목록이 없음. 산출물이 마크다운(에이전트 정의, 스킬)뿐.

### 독립적 평판과 이슈
- #53(2026-08, 닫힘): 생성된 하네스를 약 2시간, 에이전트 5명으로 돌린 사용자가 "조용한 실패" 3종을 보고. (1) 에이전트 정의의 tools 목록에 적은 지연 로딩 도구(TaskCreate, TaskUpdate)가 실제로는 주입되지 않아 오케스트레이터가 대신 갱신, (2) 단계가 끝난 뒤 앞 단계 팀원이 후속 질문에 답하며 산출물을 고침, (3) 사용량 한도 소진을 "한 번 재시도 후 계속" 규칙이 재시도 가능한 실패로 처리. 현재 템플릿의 동결 절차와 재시도 금지 목록은 이 보고의 (2), (3)에 대응하는 내용으로 보임 [추론, 커밋 대조는 안 함].
- #4: 재실행 경로가 `_workspace`를 보관하기 전에 새 입력을 만드는 순서 버그.
- #29: v1이 모든 에이전트를 opus로 고정한 것에 대한 개선 요청(v2에서 반영).
- 외부 블로그나 HN 비평은 찾지 못함(검색 범위: GitHub 이슈와 awesome-claude-code 항목뿐, 웹 검색은 이 프로젝트에 대해 따로 하지 않음).

### 측정 주장 vs 독립 검증
- README: 15개 과제 A/B에서 평균 품질 49.5 → 79.3(+60%), 승률 15/15, 분산 -32%. README가 스스로 "저자 자체 측정, n=15"라고 밝히고 자체 파일럿을 권장함. 논문은 arXiv가 아니라 별도 저장소(revfactory/claude-code-harness, 별 119)에만 있음(#47). 독립 재현은 찾지 못함.

### 공급망 위험(말로 서술)
- 실행 코드가 없고 마크다운만 배포하므로 코드 실행형 공급망 위험은 낮음. 다만 생성된 에이전트 정의의 도구 목록과 오케스트레이터 지시가 사용자 프로젝트에 그대로 들어가므로, 생성물 검토 없이 쓰면 과도한 도구 권한이 부여될 수 있음 [추론].

## 3. code-yeongyu/oh-my-openagent (구 oh-my-opencode, 약칭 OmO)

- 저장소: https://github.com/code-yeongyu/oh-my-openagent (구 주소 code-yeongyu/oh-my-opencode에서 리다이렉트)
- 수치(gh api): 별 69,601, 마지막 push 2026-09-27, 생성 2025-12-03, 보관 아님, 라이선스 API상 NOASSERTION이고 README 배지와 LICENSE.md는 "Sustainable Use License 1.0"(오픈소스 정의상 OSI 라이선스가 아닌 소스 공개형), 최신 릴리스 v5.0.1(2026-09-27), 열린 이슈+PR 1,091
- 기여자 집중도: 상위 100명 커밋 합 17,633 중 code-yeongyu 14,267(약 81%), github-actions 봇 788, sisyphus-dev-ai(프로젝트 자체 AI 봇 계정) 611. 1인 + 자동화 계정 구조.
- 성격: 원래 OpenCode 플러그인이었고, 현재 README는 5.0에서 "OmO ❤️ Pi"로 자체 CLI(`omo`)를 앞세움. Claude Code 전용이 아니라 멀티 하네스, 멀티 모델. 마스터 계층은 Sisyphus(메인 에이전트), Prometheus(계획), Atlas(계획 실행 오케스트레이터), Sisyphus-Junior(작업자). 이 조사에서 원문을 읽은 것은 README 전체, `packages/prompts-core/prompts/atlas/default.md` 전체, `packages/omo-opencode/src/hooks/atlas/AGENTS.md` 앞부분. Sisyphus와 Prometheus 프롬프트 본문은 읽지 않음.

### 마스터(Atlas)가 하는 일
- 프롬프트 첫머리: "You are Atlas - the Master Orchestrator", "You are a conductor, not a musician. ... You DELEGATE, COORDINATE, and VERIFY." 목표는 계획의 모든 과제를 `task()`로 위임해 끝내고 "Final Verification Wave"를 통과하는 것.
- 계획: Prometheus가 만든 `.omo/plans/{plan}.md`의 최상위 체크박스를 파싱. 이름 붙은 의존성이 있는 과제만 순차, 나머지는 전부 병렬("PARALLEL by default"). 원문은 병렬 여부를 묻지 말고 "무엇이 한 메시지로 전부 발사하는 걸 막는가"를 물으라고 함.
- 위임한 탐색을 스스로 다시 하지 말 것(Anti-Duplication Rule).
- 직접 하는 일은 읽기, 검증용 명령 실행, 할 일 관리, 계획 파일 체크박스 갱신으로 한정.

### 하위 에이전트 지시 방식(위임 템플릿 필드)
- 모든 `task()` 지시문은 6개 절 필수: 1 TASK(체크박스 문구를 그대로 인용), 2 EXPECTED OUTCOME(수정 파일 정확한 경로, 기대 동작, 통과해야 할 검증 명령), 3 REQUIRED TOOLS, 4 MUST DO(참조할 파일과 줄, 작성할 테스트, 노트패드에 추가), 5 MUST NOT DO(범위 밖 파일 수정 금지, 의존성 추가 금지, 검증 생략 금지), 6 CONTEXT(노트패드 경로, 상속된 지혜, 앞 과제가 만든 것). "If your prompt is under 30 lines, it's TOO SHORT."
- 작업자에게는 카테고리와 스킬을 붙여 모델을 고름(README상 과제마다 맞는 모델로 병렬 실행).

### 상태 저장
- 계획: `.omo/plans/{plan}.md`의 체크박스(Atlas가 검증 후 `[x]`로 바꿈). 막힌 과제 표기 `[~]`.
- 노트패드: `.omo/notepads/{plan}/` 아래 learnings, decisions, issues, problems 4파일. 추가 전용. 원문 "Subagents are STATELESS. Notepad is your cumulative intelligence." 위임 전마다 읽어 "Inherited Wisdom"에 넣음.
- 별도 패키지 `boulder-state`가 세션과 과제 진행 상태를 저장(코드 파일 목록만 확인, 본문은 읽지 않음).

### 완료/검증 규칙과 재시도 상한
- 위임마다 4단계 검증 필수: 자동 검증(명령 실행), 변경 파일 전부 직접 읽는 코드 리뷰, 사용자 화면 영향이 있으면 직접 QA, 계획 파일을 다시 읽어 남은 체크박스 수를 "ground truth"로 확인. 원문 "Subagents claim "done" when code is broken, stubs are scattered, tests pass trivially, or features were silently expanded." "No evidence = not complete."
- 최종 게이트: 계획의 F1~F4 리뷰어가 모두 APPROVE여야 완료. REJECT가 하나라도 있으면 수정 후 해당 리뷰어 재실행을 "ALL verdicts are APPROVE"까지 반복(상한 명시 없음).
- 재시도 상한은 프롬프트 안에서 서로 모순됨. 140행대 자동 진행 규칙은 "Task fails → Retry 3x → Still fails → Document → Move to next independent task", 330행대 실패 처리 절은 "There is no retry cap."이며 문서화하고 넘어가는 것을 명시적으로 부정("Documenting a failure and moving on produces a partial plan"). 2026-09-28 현재 main 파일에서 두 문장 모두 확인.
- 훅 쪽 상한: Atlas 훅은 세션이 idle이 되면 미완료 할 일이 있을 때 "계속하라" 프롬프트를 자동 주입. 연속 실패 10회면 5분 백오프, 주입 간 5초 쿨다운, 출력 없는 세션에 90초 감시(AGENTS.md 기준).

### 사람 개입 지점
- 원문 "NEVER ask the user "should I continue", "proceed to next task", or any approval-style questions between plan steps." 계획 단계 사이 사람 게이트는 설계상 없음. 사람 개입은 계획 수립(Prometheus 인터뷰) 단계로 몰려 있음 [추론, Prometheus 프롬프트는 읽지 않음].

### 설치하는 훅/가드(말로 서술)
- idle 이벤트마다 자동 계속 프롬프트를 넣는 연속 실행 훅, 도구 실행 전 특정 세션 유형의 쓰기/편집 차단 정책, 도구 실행 후 검증 리마인더 주입, 하위 에이전트 완료 리마인더, 최초 프롬프트 감시.
- 익명 사용 통계 전송(PostHog)이 기본 동작이었음(#3553에서 사용자가 "왜 플러그인이 행동을 엿보느냐"고 문제 제기, 끄는 환경 변수 존재).

### 독립적 평판과 이슈
- 폭주 루프: #3446(2026-04, 닫힘) Atlas를 밤새 돌렸더니 외부 요인으로 막힌 과제를 모델이 텍스트로만 "막혔다"고 말하고 `[~]` 표기를 하지 않아, 텍스트 응답이 성공으로 집계되며 실패 카운터가 계속 0으로 리셋, "infinite BOULDER CONTINUATION loop that ran for 6 hours, bypassing all iteration limits". 프로젝트 봇도 코드상 원인을 확인하는 댓글을 남김. #668(무한 TODO 계속 루프와 세션 기록 소실), #5120(열림, 단순 과제에 Sisyphus가 무한 계획 루프), #6637(열림, 모델 폴백이 영원히 반복되며 종료 안 됨).
- 구독 인증: 2026년 1월 Anthropic이 Claude 구독 인증을 서드파티 클라이언트에서 차단한 사건과 얽힘(이슈 #158 "Claude Max Plan banned", #626, OpenCode #6930 "Using opencode with Anthropic OAuth violates ToS & Results in Ban"). 웹 검색 요약상 HN에서 반발이 컸고 OmO 제작자는 Anthropic OAuth 구현을 직접 만든 적 없다고 해명(검색 요약만, 원문 미확인). 현재 README는 여전히 "/login covers Claude, ChatGPT, Kimi and GLM subscriptions"라고 적고 있어 이용약관 위험 검토가 필요함 [추론].
- README 추천사("OmO does it in 1 hour" 등)는 개인 발언 인용이며 측정 근거 없음.

### 측정 주장 vs 독립 검증
- README에 정량 벤치마크 주장은 없고 추천사 위주. 독립 평가 자료는 찾지 못함.

### 공급망 위험(말로 서술)
- 전역 패키지 설치형 CLI, 1인 + 봇 계정이 하루 단위로 릴리스(v5.0.1이 조사 전날). 빠른 릴리스 주기와 AI 봇의 커밋, 이슈 응대가 섞여 있어 변경 검토 여력이 불투명 [추론].
- 사용자의 기존 Claude 설정, 플러그인, MCP를 재사용하는 동작이 있었고 끄는 옵션 요청 이슈가 있었음(#2949).
- 기본 원격 통계 전송(끌 수 있음). 격리망 환경에서 오류를 낸 보고 있음.

## 4. Yeachan-Heo/oh-my-claudecode (OMC)

- 저장소: https://github.com/Yeachan-Heo/oh-my-claudecode
- 수치(gh api): 별 39,376, 마지막 push 2026-09-27, 생성 2026-01-09, 보관 아님, MIT, 최신 릴리스 v5.5.0(2026-09-22), 열린 이슈+PR 7(별 대비 매우 적음, 빠르게 닫는 운영으로 보임 [추론])
- 기여자 집중도: 상위 100명 커밋 합 3,656 중 Yeachan-Heo 3,110(약 85%), 2위 71, 3위 59.
- 성격: Claude Code 플러그인. oh-my-opencode의 Claude Code판에서 출발. 에이전트 19종(planner, architect, executor, verifier, critic, security-reviewer 등)과 모드 여러 개(Team, Autopilot, Execute, Verify, Ultragoal 등). README는 v4.1.7부터 Team을 "canonical orchestration surface"로 지정. 이 조사에서 읽은 것은 README 주요 절, `skills/team/SKILL.md`(1,050행 중 약 400행), `hooks/hooks.json` 전체, 권한 처리 훅의 컴파일 결과 JS 일부.

### 마스터(Team lead)가 하는 일
- 단계 파이프라인: team-plan → team-prd → team-exec → team-verify → team-fix(루프).
- 단계별 에이전트 라우팅을 리더가 결정. 계획은 explore(haiku) + planner(opus), 요구사항은 analyst(opus), 실행은 executor(sonnet), 검증은 verifier(sonnet) 필수에 인증/암호 변경이면 security-reviewer, 20파일 초과나 구조 변경이면 code-reviewer(opus) 추가. 사용자의 `N:agent-type` 인자는 실행 단계 작업자 종류만 덮어씀.
- 비용 모드에서는 모델을 한 등급씩 낮추되 검증 단계는 최소 sonnet.
- 한 세션에 루프 주체는 하나만 두라고 명시("Use only one primary loop authority in a session"). Claude Code 기본 `/goal`과 자체 모드들이 겹치지 않게 경계를 문서화.

### 하위 에이전트 지시 방식
- 이름을 붙인 팀원을 병렬로 띄우고(`subagent_type`, `name`, `prompt` = 작업자 공통 서문 + 배정 과제), 과제는 공유 작업 목록에 설명(대상 파일과 검증 명령 포함, 예: "Run tsc --noEmit to verify")으로 등록.
- 단계 사이 인계 문서 필수: `.omc/handoffs/<stage>.md`에 Decided, Rejected, Risks, Files, Remaining 5필드, 10~20줄. 다음 단계 팀원 지시문에 포함. 이유는 "important context ... lives only in the lead's conversation history. If the lead's context compacts or agents restart, this knowledge is lost."

### 상태 저장
- MCP 도구(state_read, state_write)로 세션 범위 상태 저장. 필드: current_phase, team_name, fix_loop_count, max_fix_loops, stage_history, 작업자와 실행 시도 기록 등. 세션 ID 없이 집계 상태를 읽어 남의 팀을 재개하지 말라는 규칙, 상태 파일이 깨졌으면 원본 바이트를 보존하고 새로 초기화하지 말라는 규칙이 있음.
- 런타임 상태는 `.omc/` 아래(프롬프트와 대화록이 들어갈 수 있다고 README가 경고), git 무시 대상.

### 완료/검증 규칙과 재시도 상한
- exec → verify → fix 반복은 검증 통과 또는 증거가 있는 종료 상태(blocked/failed)까지. team-fix는 `max_fix_loops` 기본 3회, 넘으면 `failed`로 종료("no infinite loop").
- 감시 규칙: 진행 중 과제가 5분간 메시지 없으면 상태 확인, 10분 이상이면 죽은 작업자로 보고 재배정, 과제 2개 이상 실패한 작업자에게는 새 과제를 주지 않음.
- 종료 상태는 complete, failed, cancelled.

### 사람 개입 지점
- Team 스킬 본문에서 단계 사이 사람 승인 절차는 읽은 범위에서 보이지 않음. 요구사항이 모호하면 team-prd 단계에서 analyst가 기준을 명시하는 구조이고, 사람에게 묻는 규칙은 확인하지 못함.

### 설치하는 훅/가드(말로 서술)
- Claude Code 훅 이벤트 거의 전부에 스크립트를 걸어 둠: 프롬프트 제출 시 키워드 감지와 스킬 주입, 세션 시작 시 설정과 프로젝트 메모리와 위키 로드, 모든 도구 실행 전 강제 규칙 검사, 모든 도구 실행 후 검증기와 규칙 주입과 디렉터리 문맥 주입, 하위 에이전트 시작/종료 추적과 산출물 검증, 압축 직전 메모리 저장, 응답 종료(Stop) 시 문맥 가드와 워크플로 이탈 가드와 "지속 모드"(작업이 안 끝났으면 종료를 막아 계속하게 함)와 코드 단순화.
- 셸 권한 요청 훅: 저장소 경로 안의 읽기 명령, git 상태 조회, lint와 build와 typecheck 같은 정해진 명령 패턴을 사람 확인 없이 자동 허용. 명령 연결용 셸 특수문자가 있으면 자동 허용 제외. build 스크립트는 프로젝트가 정의한 임의 코드를 실행할 수 있어 "안전 명령"이라는 분류가 완전하지 않음 [추론].

### 독립적 평판과 이슈
- 폭주 루프와 토큰 낭비: #2652(Stop 훅의 지속 모드가 비정상 종료된 세션의 상태 파일을 다음 세션에서 읽고 "무한 토큰 소모 루프"를 일으키며 병렬 에이전트 문맥이 무한 누적, 제보자 추정 4~5배 토큰 낭비), #3138(지속 모드 Stop 훅이 Claude Code가 주는 재진입 표시를 무시해 Claude Code 자체 안전장치인 "연속 9회 차단 시 강제 종료"가 매번 발동, 그 결과 OMC의 강화 횟수 예산 기본 50이 사실상 9로 잘림), #1374(상태를 지운 뒤에도 "Autopilot not complete" 무한 반복), #719(한국어 제보, ULTRAWORK 종료 후 stopHook 반복과 토큰 과다), #385와 #240(세션 동결). 모두 닫힘.
- 성능: #3972(도구 호출마다 스킬 레지스트리 재구성과 git 프로세스 실행), #3995(Windows에서 세션 시작 훅이 시간 예산 초과로 실패 개방).
- #3698(열림, 댓글 62): "lightweight workflow, skill consolidation, prompt and hook SSOT" 에픽. 기능과 훅이 과도하게 늘어난 것을 프로젝트 스스로 정리 중인 것으로 보임 [추론].
- 외부 블로그나 HN 비평은 이 프로젝트에 대해 따로 찾지 않음.

### 측정 주장 vs 독립 검증
- README "Smart model routing saves 30-50% on tokens": 측정 방법이나 근거 링크를 README에서 찾지 못함. 독립 검증 없음.
- "Persistent execution - Won't give up until the job is verified complete"는 위 폭주 루프 이슈들과 같은 장치(Stop 훅 지속 모드)에서 나온 문구.

### 공급망 위험(말로 서술)
- 설치 즉시 거의 모든 훅 이벤트에서 Node 스크립트가 실행되고, 일부 셸 명령을 자동 허용하는 권한 훅이 들어감. 플러그인 갱신이 곧 이 스크립트들의 갱신.
- 외부 CLI 작업자(Codex, Gemini 등)를 쓰려면 전역 npm 설치를 요구.
- 네이티브 팀 기능을 위해 사용자 전역 설정에 실험 기능 환경 변수를 켜라고 안내.

## 5. ruvnet/ruflo (구 claude-flow)

- 저장소: https://github.com/ruvnet/ruflo (구 주소 ruvnet/claude-flow에서 리다이렉트)
- 수치(gh api): 별 73,398, 마지막 push 2026-09-27, 생성 2025-06-02, 보관 아님, MIT, 최신 릴리스 v3.46.1(2026-09-26), 열린 이슈+PR 996
- 기여자 집중도: 상위 39명 커밋 합 7,398 중 ruvnet 7,167(약 97%), 2위 84, 3위는 "claude" 계정 52. 사실상 1인 + AI 생성 코드.
- 성격: Claude Code와 Codex를 감싸는 "하네스"를 표방. 100개 이상 에이전트, 스웜 토폴로지(계층, 메시, 적응형), 합의 알고리즘(Raft, Byzantine, Gossip), 벡터 메모리, 원격 연합(federation), 웹 UI까지 내세움. 마스터 역할은 "Queen" 계층. 이 조사에서 원문을 읽은 것은 README 주요 부분, `.claude/agents/hive-mind/queen-coordinator.md` 전체, 저장소 자체의 `.claude/settings.json`(구조만 요약), 이슈 #1514, #1375, #1896, #1427, #1330 본문 앞부분.

### 마스터(Queen Coordinator)가 하는 일
- 프롬프트는 "You are the Queen Coordinator, the sovereign intelligence at the apex of the hive mind hierarchy." 첫 의무가 "Establish dominance hierarchy and write sovereign status", 즉 MCP 메모리에 여왕 상태 JSON을 저장하는 것.
- 지시(royal directives)는 `{id, command, assignee}` 배열을 공유 메모리 키에 쓰는 방식. 예시 지시는 "Initialize swarm topology", "Begin reconnaissance" 수준의 추상 명령.
- 자원 배분 예시는 계산 단위 비율과 메모리 할당(MB)을 JSON으로 저장하지만, 이 값이 실제 실행 자원을 제어하는지는 프롬프트에서 알 수 없음.
- 거버넌스 모드 3종(계층, 민주, 비상), "EVERY 2 MINUTES issue status report", 후계 계획, "Coup prevention mechanisms" 같은 은유가 대부분이고, 과제 분해 절차, 완료 판정 기준, 재시도 상한은 이 파일에 없음.
- 건강 상태 예시 JSON에 coherence_score 0.95, swarm_efficiency 0.88, morale "high" 같은 고정값이 들어 있어, 모델이 측정 없이 이 숫자를 그대로 기록할 여지가 있음 [추론].

### 하위 에이전트 지시 방식
- 위임 대상별 역할 목록(collective-intelligence는 합의와 전략, workers는 실행, scouts는 정보 수집, memory manager는 상태 저장)만 있고 지시문 필드 규격은 없음. 실제 전달은 공유 메모리 키 쓰기.

### 상태 저장
- MCP 메모리 도구로 네임스페이스와 키에 JSON 저장. 백엔드는 SQLite와 HNSW 벡터 인덱스(README). 설치 후 프로젝트에 `.swarm/`, `.hive-mind/`, `memory/`, `coordination/` 등이 생긴다는 사용자 보고(#1375에 인용된 #670).

### 완료/검증 규칙, 재시도 상한, 사람 개입
- Queen 정의 파일에는 없음. 저장소 설정의 스웜 최대 에이전트 15. 연합 기능 설명에는 오작동 에이전트를 "no human in the loop required"로 즉시 강등한다고 적혀 있음.

### 설치하는 훅/가드(말로 서술)
- README 표 기준으로 CLI 설치 경로는 훅을 설치하고 플러그인 경로는 설치하지 않음.
- 저장소 자체 설정(생성기 산출물과 같다는 보장은 없음): 셸 실행 전, 파일 쓰기와 편집 후, 프롬프트 제출, 세션 시작과 종료, Stop, 압축 전(수동과 자동), 하위 에이전트 종료에 훅. 권한 허용 목록 25개에 모든 npx 명령과 모든 node 명령, git push, 자사 MCP 도구 전체를 자동 허용하는 항목이 있고, 거부 목록은 .env 읽기와 루트 전체 삭제 3개뿐. MCP 서버를 매번 최신 버전 패키지를 확인 없이 내려받아 실행하도록 등록. 백그라운드 데몬 자동 시작과 감사, 최적화, 학습 작업을 30분에서 4시간 주기로 예약. 커밋과 PR에 RuFlo 공동저자 표기를 자동 추가.
- 설치 방법 중 하나로 원격 스크립트를 받아 바로 셸에 실행하는 한 줄 설치를 안내.

### 독립적 평판과 이슈
- 가짜 기능: #1514(2026-04, 닫힘) "Ruflo is 99% Theater, 1% Real". v3.5.51 기준 300여 개 MCP 도구 중 약 290개가 실행 백엔드 없이 JSON 상태만 만드는 스텁이라는 외부 감사. 메인테이너는 v3.5.53에서 "Fabricated metrics removed"(캐시 적중마다 절감 토큰에 100을 더하던 코드 제거, 기준값 1000 하드코딩 제거 등)라고 답함. 즉 조작된 지표가 있었다는 것을 메인테이너가 인정한 셈.
- 외부 감사 추적: #1896(열림) AlphaSignal AI 기사(2026-05-07, v3.6.30 대상)를 메인테이너가 직접 이슈로 옮김. 기사 요지 인용: 메모리, 임베딩, 작업 도구는 쓸 만하지만 "the multi-agent swarm runtime its README describes does not yet execute end-to-end." 메인테이너 자신의 현재 main 대조 결과도 `agent_spawn`은 메모리 내 Map에 JSON 기록만 쓰고 하위 프로세스를 띄우지 않음 "Claim still holds", `workflow_execute`는 "Workflow not found"를 반환 "Claim still holds". 약 240개 중 195개 도구가 실제 동작 확인이라는 기사 수치도 인용됨. 기사 원문은 읽지 않았고 이슈 본문 인용만 봄.
- 보안: #1375(2026-03, 닫힘) 외부 보안 감사 요약. (1) MCP 도구 설명에 숨은 지시가 있어 모델이 사용자 저장소에 저장소 소유자를 협업자로 추가하게 만드는 프롬프트 인젝션(#1323 참조), (2) 3.1.0-alpha.55부터 3.5.2까지 난독화된 preinstall 스크립트가 패키지 밖 npm 캐시 디렉터리를 뒤져 삭제하고 오류를 숨김(#1261 공개 후 제거), (3) 삭제해도 다시 생기는 상태 파일과 제거 후에도 남는 백그라운드 프로세스(#373, #710 "Just like a virus, I can't uninstall it", #670 프로젝트에 259파일 45,216줄 주입). 메인테이너는 v3.5.40에서 수정했다고 답함. 후속 댓글의 다른 감사는 `verifySignature()`가 항상 true를 반환한다고 추가 보고.
- 비용: #1330(30분 안에 수백만 토큰 소모), #1427(터미널을 닫은 뒤에도 사용량 한도가 1시간에 4% 증가, 백그라운드 데몬 의심). 이전 조사 메모에 따르면 설정 생성기는 이후 데몬 자동 시작 기본값을 끔으로 바꿨으나, 이 조사에서 생성기 코드를 다시 읽어 확인하지는 않음. 저장소 자체 설정은 여전히 자동 시작 켬.

### 측정 주장 vs 독립 검증
- README "Intelligent routing (89% accuracy)": 근거 링크를 README 해당 줄에서 찾지 못함.
- README 벡터 메모리 "~1.9x~4.7x faster than brute force, recall@10 ~0.99"는 자체 감사 문서와 벤치 스크립트를 링크하고, 작은 N에서는 진다고 스스로 한정함. 과거 과장 지적 이후 표현이 조심스러워진 것으로 보임 [추론].
- README 배지 "ecosystem downloads 8.1M+", "git clones 14d 106k"는 저장소 안 JSON 파일을 근거로 링크. 독립 검증 아님.
- 이전 조사 메모에 hooks 소스 안 "84.8% SWE-Bench" 문자열이 있었다고 적혀 있으나 이번에 재확인하지 않음.

### 공급망 위험(말로 서술)
- 과거 난독화된 파괴적 설치 스크립트 배포 이력, MCP 도구 설명 프롬프트 인젝션 이력이 있음(메인테이너 수정 주장).
- 최신 버전을 매번 자동 설치해 실행하는 MCP 등록과 넓은 셸 자동 허용이 결합되어, 패키지 한 번의 악성 릴리스가 곧 사용자 셸 실행으로 이어지는 구조 [추론].
- 사실상 1인 저장소, 하루 단위 릴리스, 원격 스크립트 즉시 실행형 설치 안내.

## 6. gastownhall/gastown (Gas Town, Steve Yegge)

- 저장소: https://github.com/gastownhall/gastown (원래 steveyegge 개인 계정)
- 수치(gh api): 별 18,204, 마지막 push 2026-09-18, 생성 2025-12-16, 보관 아님, MIT, 최신 릴리스 v1.2.1(2026-06-06), 열린 이슈+PR 483
- 기여자 집중도: 상위 100명 커밋 합 7,400 중 steveyegge 4,831(약 65%), 2위 457, 3위 367. 이번 조사 대상 중 기여가 가장 분산된 편이지만 여전히 1인 주도.
- 성격: Go로 만든 별도 오케스트레이션 시스템. Claude Code 세션 여러 개를 tmux로 띄우고 역할을 나눔: Mayor(마스터), Polecat(일회성 작업자, git worktree 샌드박스), Witness(작업자 생애 관리), Refinery(머지 큐), Deacon(순찰과 복구), Crew 등. 작업 추적은 별도 도구 Beads(`bd`), 저장소는 Dolt(버전 관리되는 SQL DB). 이 조사에서 원문을 읽은 것은 `internal/templates/roles/mayor.md.tmpl` 대부분, `polecat.md.tmpl` 핵심 줄, `internal/config/roles.go`의 기본 실행 명령 주석, 이슈 #4044, #4145 앞부분.

### 마스터(Mayor)가 하는 일
- "Propulsion Principle": 자기 hook에 걸린 일이 있으면 즉시 실행. 원문 "No confirmation. No questions. No waiting. The hook IS your assignment". hook이 비었으면 메일함 확인, 그래도 없으면 사용자 지시 대기.
- 판단 규칙: 조율(상태 확인, 메일, 에스컬레이션, rig 관리)이면 직접, 코드 변경이면 "File a bead, sling it"이 기본값. "If you're unsure, sling it." 안티패턴으로 "Doing everything yourself while the polecat pool sits idle."
- 책임: 작업 배분, rig 간 라우팅, Witness가 못 푼 에스컬레이션 처리, 아키텍처와 우선순위 같은 전략 결정. 작업자 정리와 세션 종료, 일상적 독촉은 Witness 담당이라 Mayor 일이 아니라고 명시.
- 계획: 에픽 단위 일괄 작업은 convoy로 묶고, 의존성은 `bd dep add`로 "X needs Y" 방향으로 등록 후 `bd blocked`로 확인.

### 하위 에이전트 지시 방식
- 위임 = Beads 이슈 하나 생성 + `gt sling <bead> <rig>`. 이 명령이 Polecat을 띄우고 이슈를 그 hook에 걸고 세션을 시작. 지시문 필드는 이슈 본문 자체(별도 템플릿 필드는 Mayor 파일에서 확인 못 함).
- 임시 지시는 메일을 hook에 거는 방식으로도 가능("read the mail content, interpret the prose instructions, and execute them").
- 에이전트 간 전달은 반드시 `gt nudge`(대상이 idle일 때 전달, 아니면 큐), tmux에 키 입력을 직접 보내지 말 것.

### 상태 저장
- 두 단계 Beads: 타운 수준(`hq-` 접두사, 메일과 조율, Dolt에 즉시 저장), rig 수준(프로젝트 이슈). hook에 걸린 일은 세션을 넘어 유지.
- 압축이나 새 세션 후 `prime` 명령으로 역할 문맥 복구. 인계는 "🤝 HANDOFF" 제목 메일.
- 메모리는 Claude Code 기본 MEMORY.md 대신 `remember` 명령으로 Dolt에 저장해 모든 에이전트가 공유하도록 강제("Do NOT write to ~/.claude/*/memory/"). 저장 유형 feedback, project, user, reference, general, 코드나 git에서 유도 가능한 것은 저장 금지.

### 완료/검증 규칙과 재시도
- Polecat 완료 신호는 `gt done` 하나뿐. "There is no approval step." 세션이 `gt done` 없이 끝나면 이슈가 새 Polecat에 재배정되어 "spawn storms"가 난다고 템플릿이 경고.
- 머지 큐 경로는 Refinery가 병합, PR 경로는 CI 통과와 승인 후 `gt done`. 테스트 기준이나 리뷰 절차는 읽은 범위의 템플릿에 구체적으로 없음.
- 재시도 상한: 템플릿에서 찾지 못함. 복구는 Witness와 Deacon의 자동 재시작에 맡김.

### 사람 개입 지점
- 설계상 최소화. Mayor는 hook이 비어 있을 때만 사람을 기다림. 템플릿은 사람이 자리를 비우면 "Witnesses wait → Polecats idle → Gas Town stops"라며 Mayor가 막지 말라고 강조. Mayor는 작업 후 main에 직접 push하도록 되어 있음("Push to main when done").

### 설치하는 훅/가드(말로 서술)
- 역할 설정의 기본 에이전트 실행 명령이 Claude Code의 권한 확인을 모두 건너뛰는 실행 옵션을 켠 상태(roles.go 주석 기준). 샌드박스는 git worktree 분리 정도이며 원격, 로컬 실행 샌드박스는 이슈 #2229에서 기능 요청으로 다뤄짐.
- 역할별로 Claude Code 훅을 동기화 설치하는 명령이 있고, #4250(열림)은 시작 명령이 운영자가 직접 덮어쓴 훅 설정을 조용히 되돌린다는 보고.

### 독립적 평판과 이슈
- 폭주 루프: #4044(열림) 작업 정의가 삭제된 이슈가 Polecat hook에 걸려 있으면 "시작 → 충돌 → 감지 → 재시작"이 무한 반복되고 재시작 기록이 한없이 쌓임, 멈춰 둔 rig에서도 발생. #4145(열림) 중앙 Dolt 서버가 CPU 100~227%로 폭주하고 재시작해도 그대로, 쓰기 조용한 유실. #4188(열림) 완료 확인 로직 오류로 병합된 작업이 미완료로 표시되어 재배정 반복. #1973(닫힘) 워크트리 사전 동기화로 git이 멈추며 Polecat 생성 폭주. #2814(닫힘) 연합 완료 보고가 도구 호출을 조용히 지어내는 것에 취약.
- 비용: 웹 검색 요약상 Yegge 본인이 "expensive as hell"이라고 했고 Anthropic 사용 한도를 피하려고 두 번째 Claude 계정을 쓴다고 함, 병렬 에이전트 12~30개 운영 시 시간당 약 100달러라는 보도(검색 요약만, 원문 미확인).
- 설계 비평: Maggie Appleton "Gas Town's Agent Patterns, Design Bottlenecks, and Vibecoding at Scale"(본문을 요약 도구로 읽음, 원문 정독 아님). 요지는 개념이 겹치고 즉흥적이라 인지 부담이 크고("number of overlapping and ad hoc concepts in this design is overwhelming"), 병목은 구현 속도가 아니라 설계와 계획이며, 손을 뗀 에이전트 개발의 대표적 위험("one of the most critical, emerging footguns")이라는 것.
- 긍정 사례: DoltHub 블로그 "A Day in Gas Town"(2026-01-15)이 있으나 Dolt는 Gas Town이 쓰는 DB의 제작사라 이해관계가 있음. 본문은 읽지 않음.

### 측정 주장 vs 독립 검증
- 처리량이나 품질에 대한 정량 벤치마크 주장은 찾지 못함. 비용 수치는 사용자와 언론 보도 수준.

### 공급망 위험(말로 서술)
- 기본 실행이 권한 확인 전면 생략이고 Mayor가 main에 직접 push하는 구조라, 프롬프트 인젝션이나 오작동이 곧 저장소 변경과 원격 반영으로 이어짐 [추론].
- Go 바이너리 + Dolt SQL 서버 + tmux + 다수 백그라운드 데몬(Deacon, Witness)이 상시 동작. 설치 표면이 넓음.

## 7. Get Shit Done (GSD): gsd-build/get-shit-done → open-gsd/gsd-core

- 저장소: https://github.com/gsd-build/get-shit-done (보관됨) → https://github.com/open-gsd/gsd-core (현행)
- 수치(gh api):
  - gsd-build/get-shit-done: 별 64,446, 마지막 push 2026-05-31, 보관됨(archived=true), MIT, 마지막 릴리스 v1.42.3(2026-05-16). README 첫머리가 "GSD Has Moved"로 바뀌어 있음.
  - open-gsd/gsd-core: 별 9,898, 마지막 push 2026-09-27, 생성 2026-05-22, 보관 아님, MIT, 최신 릴리스 v1.15.0(2026-09-26), 열린 이슈+PR 181.
- 기여자 집중도: gsd-core 상위 100명 커밋 합 5,722 중 trek-e 3,711(약 65%), glittercowboy(원작자 TÂCHES) 945, 3위 133. 옛 저장소는 trek-e 1,435, glittercowboy 945. 원작자에서 다른 메인테이너로 주도권이 넘어간 구조로 보임 [추론].
- 별 수 해석 주의: 별 64k는 보관된 옛 저장소에 남아 있고 현행 저장소는 약 10k.
- 성격: "context rot"(문맥이 차면서 품질이 떨어지는 현상)을 해결하겠다는 스펙 주도 개발 프레임워크. 질문 → 조사 → 요구사항 → 로드맵 → 단계(phase)별 계획 → 실행 → 검증 루프. 여러 런타임 지원(Claude Code, Codex, Cursor 등). 이 조사에서 원문을 읽은 것은 `gsd-core/workflows/execute-phase.md`(91KB) 중 목적, 실행자 위임 블록, 체크포인트 처리, 코드 리뷰 게이트, 단계 목표 검증 부분, `hooks/hooks.json`, 두 저장소 README 일부.

### 마스터(execute-phase 오케스트레이터)가 하는 일
- 원문 "Orchestrator coordinates, not executes. ... discover plans → analyze deps → group waves → spawn agents → handle checkpoints → collect results." 오케스트레이터는 가볍게 유지하고 무거운 일은 새 문맥의 하위 에이전트로.
- 계획(PLAN.md)들의 의존성을 분석해 wave로 묶고 wave 단위 병렬 실행. 병렬 실행자는 각자 git worktree에서 작업. 한 메시지에 여러 Agent 호출을 넣지 말고 하나씩 백그라운드로 띄우라는 규칙(git 설정 파일 잠금 충돌 때문).
- STATE.md, ROADMAP.md 같은 공유 파일은 오케스트레이터만 wave 종료 후 갱신. 실행자는 건드리지 못함.
- 오케스트레이터 자신이 에이전트 worktree 안으로 작업 디렉터리가 흘러 들어가면 실행을 거부하는 셸 가드 등 git 사고 방지 절차가 매우 많음(이슈 번호를 주석으로 단 방어 코드가 수십 개).

### 하위 에이전트 지시 방식(위임 템플릿 필드)
- 실행자 Agent 호출 필드: subagent_type, description, model(설정이 "inherit"이면 생략), 격리 플래그, prompt. prompt 안 블록: `<objective>`(계획 실행, 과제마다 원자적 커밋, SUMMARY.md 생성, STATE와 ROADMAP 수정 금지), `<worktree_branch_check>`, `<parallel_execution>`(git 훅 우회 금지, SUMMARY를 쓰고 바로 커밋한 뒤에야 서술), `<execution_context>`(참조 문서를 오케스트레이터가 미리 본문에 인라인. `@경로`는 Agent 프롬프트에서 펼쳐지지 않는다는 이유), `<required_reading>`(계획, PROJECT.md, STATE.md, 설정, 문맥창이 크면 CONTEXT, RESEARCH, 앞 wave 요약), `<success_criteria>` 체크리스트.
- 문맥창 크기(20만, 50만 토큰)에 따라 넣는 자료를 조건부로 바꿈.

### 상태 저장
- `.planning/` 아래 PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, 단계 디렉터리의 PLAN, SUMMARY, VERIFICATION, UAT, REVIEW 파일. 세션 경계를 넘어 유지되는 구조화 산출물이 곧 상태.
- 재개 게이트: 커밋은 있는데 SUMMARY.md가 없으면 새 실행자를 띄우기 전에 멈춤(중복 작업과 낡은 STATE 방지). 완료 판정은 에이전트의 종료 신호가 아니라 디스크의 SUMMARY와 커밋으로. 신호가 안 와도 산출물이 있으면 성공으로 보고 진행, "Never block indefinitely".

### 완료/검증 규칙과 재시도
- 단계 목표 검증: gsd-verifier 에이전트가 "Verify phase achieved its GOAL, not just completed tasks." 계획의 must_haves를 실제 코드와 대조, 요구사항 ID를 빠짐없이 추적, SUMMARY의 주장과 실제를 교차 확인해 VERIFICATION.md 작성. 상태가 passed일 때만 로드맵 갱신. human_needed면 UAT 파일을 만들어 사람 검증 항목으로 남김.
- 코드 리뷰 게이트는 "Advisory only, never blocks". TDD 모드에서 RED→GREEN 순서 위반만 예외로 차단.
- 외부 AI 위임 시 명령에 기본 300초 제한시간, 프롬프트는 셸 보간이 아니라 표준 입력으로(인젝션 방지). 실패 시 재시도, 건너뛰기, 중단을 사용자에게 제시.
- 실행자 재시도 횟수 상한은 읽은 범위에서 찾지 못함.

### 사람 개입 지점
- 로드맵 승인("You approve it, then you're ready to build").
- 계획에 `autonomous: false`인 체크포인트: human-verify, decision, human-action 3종. 자동 모드면 human-verify는 "approved"로 자동 승인, decision은 기본 선택지가 있으면 자동 선택. human-action(인증 등)과 "blocking-human" 표시, 패키지 설치 검증 관련은 자동 승인 금지.
- 체크포인트 이후에는 기존 에이전트를 재개하지 않고 완료 과제표와 사용자 응답을 넣은 새 연속 에이전트를 띄움. 이유는 재개가 병렬 도구 호출에서 깨진다는 것.
- 설정 `mode`가 interactive(단계마다 확인) 또는 yolo(자동 승인).

### 설치하는 훅/가드(말로 서술)
- 세션 시작 시 경로 정규화와 업데이트 확인, 쓰기와 편집 전 프롬프트 가드와 읽기 가드와 worktree 경로 가드, 쓰기 전 쓰기 가드, 읽기와 검색과 셸 실행 전 비밀 파일 읽기 가드, 하위 에이전트 호출 전 격리 가드, 도구 사용 후와 하위 에이전트 종료와 Stop과 압축 전 문맥 사용량 감시, 웹 읽기 후 프롬프트 인젝션 스캐너, 설정 파일 변경 시 재로드. 이번 조사 대상 중 "방어용" 훅 비중이 가장 높음.
- 옛 저장소 README(v1.42.3)는 Claude Code의 권한 확인을 모두 건너뛰는 실행 옵션으로 돌리라고 권장하며 "GSD is built for frictionless automation. Skip-permissions is how it's intended to run."이라고 적음. 현행 gsd-core README에서는 이 권장 문구를 찾지 못함(grep 기준).

### 독립적 평판과 이슈
- 비용: 옛 저장소 #120 "GSD Using Substantially More Tokens (and time) After Update?" 사용자가 토큰과 시간이 약 4배, 버그 수정 하나에 에이전트 100개 이상이 생겼다고 보고. #452(토큰의 99%가 캐시 읽기), #318(Max 요금제에서 사용량 과다), #1888(파일 목록 나열에 오래 걸림).
- 현행 저장소 이슈는 대부분 메인테이너의 설계 에픽(ADR 번호, "enforcement by construction")이라 외부 사용자 불만 신호가 키워드 검색에서 잘 안 잡힘. #4649(열림) 스킬 탐색이 에이전트 5개에서 모든 SKILL.md를 예산 없이 읽음, #4940(열림) 훅마다 약 45ms 지연.
- HN, 블로그 비평은 이 프로젝트에 대해 따로 검색하지 않음.

### 측정 주장 vs 독립 검증
- "each executor starts with a clean 200k-token context"는 설계 설명이고 품질 향상 수치 주장은 README에서 찾지 못함.

### 공급망 위험(말로 서술)
- 설치는 npm 패키지 최신판을 즉석 실행하는 방식이고, 설치기가 사용자 전역 Claude 설정 디렉터리에 워크플로와 참조 문서를 복사. 훅이 많아 갱신 때마다 실행 코드가 넓게 바뀜.
- 저장소 이전(보관 → 새 조직)이 있었으므로 옛 패키지명과 새 패키지명 혼동에 따른 사칭 패키지 위험을 확인할 필요가 있음 [추론].

## 8. bmad-code-org/BMAD-METHOD

- 저장소: https://github.com/bmad-code-org/BMAD-METHOD
- 수치(gh api): 별 53,554, 마지막 push 2026-09-27, 생성 2025-04-13, 보관 아님, 라이선스 API상 NOASSERTION이지만 LICENSE 파일 첫 줄은 "MIT License, Copyright (c) 2025 BMad Code, LLC", 최신 릴리스 v6.12.0(2026-09-04), 열린 이슈+PR 54
- 기여자 집중도: 상위 100명 커밋 합 1,307 중 alexeyv 676(약 52%), bmadcode(창시자) 195, 릴리스 봇 91. 이번 조사 대상 중 1인 집중도가 가장 낮은 편.
- 성격: "Agile AI Driven Development" 방법론. 역할 페르소나(분석가, PM, 아키텍트, 개발자 등)와 PRD, 아키텍처, 스토리 문서를 거쳐 구현. 현재 v6은 스킬 묶음(모듈)으로 배포. 이 조사에서 원문을 읽은 것은 README 앞부분, `skills/bmad/SKILL.md`(69행 전체), `skills/bmad-build-auto/`의 SKILL.md, workflow.md 앞부분, step-01, step-03, step-04 일부, references/claims-check.md.

### 마스터 구조: "라우터"와 "무인 1회 루프" 두 가지
- `bmad` 스킬(허브)은 실행하지 않는 읽기 전용 라우터. 설치된 스킬과 모듈의 지식 문서를 매 요청마다 다시 스캔해 "다음에 무엇을 할지"만 추천. 규칙: 폴더명이나 일반 지식으로 순서를 지어내지 말 것("Never manufacture a sequence from folder names"), 완료가 불확실하면 진행을 권하지 말고 사용자에게 물을 것, 다음 스킬이 분명하면 "새 문맥을 열어 거기서 실행하라"고 안내하고 현재 도움말 문맥에서 시작하지 말 것, 일반 도움 요청에서는 파일을 쓰지 말 것.
- `bmad-build-auto`는 "One iteration of an unattended development loop". 목표 "Turn intent into a hardened, reviewable artifact, without human interaction." 한 번 호출에 티켓 하나만("never advance to a different ticket regardless of outcome"). 단계: 명확화와 경로 선택(oneshot 또는 full) → 계획 → 구현 → 리뷰.

### 계획
- full 경로 계획의 "Ready for Development" 기준: 모든 과제에 파일 경로와 구체 행동, 의존성 순서, 수용 기준은 Given/When/Then, 수용 기준은 내부 대리 지표가 아니라 의도가 가리키는 가장 바깥 표면을 관찰, 플레이스홀더와 TBD 금지, 알려진 공백 없음, 모순 없음.
- 의도가 계획 파일 안 `<intent-contract>` 블록에 고정되고 구현과 리뷰 단계에서 읽기 전용.
- 의도를 확정할 수 없으면 추측하지 말고 "unclear intent"로 정지("Do not fantasize or leave open questions").

### 하위 에이전트 지시 방식
- full 경로 구현은 설정에 정의된 인계 문구를 "verbatim"으로 따르고, 오케스트레이터가 목표 재진술이나 파일 목록, 수용 기준을 덧붙이지 말라고 명시("the plan is the sub[agent's source]"). 하위 에이전트는 동기 호출로 기다림(백그라운드 금지).
- 리뷰는 여러 "렌즈" 하위 에이전트를 한 메시지로 동시에 띄움. 차이는 파일 경로로만 전달("a launch prompt never carries diff text"). 리뷰 에이전트는 현재 세션과 같은 모델 능력 이상.
- claims-check 렌즈: 계획서를 "testimony, not evidence"로 보고, 경로 추적을 끝낸 뒤에야 계획서를 처음 읽어 코드와 모순되는 주장만 보고. 계획이 리뷰어 판단을 미리 오염시키지 않도록 순서를 강제한 설계.
- 수정 지시 템플릿: "Review of your implementation found problems. Fix each one below with the smallest change ..." + `<파일> | <무엇이 틀림> | <최소 수정이 해야 할 것>` 목록. 같은 구현 에이전트를 이름이나 id로 재참여시키고, 새로 띄우는 것은 재참여가 아니라고 명시.

### 상태 저장
- 계획 파일의 frontmatter(status: draft, ready-for-dev, in-progress, in-review, blocked, built, done, baseline_revision, review_loop_iteration, deferred 목록, lenses_ran)와 본문의 Implementation Notes, Review Triage Log, Plan Change Log. 티켓은 `tickets.py` 스크립트로 조회와 표시.
- 정지 시 계획 파일이나 별도 결과 파일에 최종 상태와 차단 사유를 기록.

### 완료/검증 규칙과 재시도 상한
- 구현 후 계획의 Verification 절 명령을 실행, 입출력 경계 사례 표가 있으면 모든 행이 통과한 테스트로 덮였는지 감사.
- 리뷰 결과 분류: intent_gap(의도 자체 결함, 변경을 패치 파일로 보존하고 코드 되돌린 뒤 정지), bad_plan(계획 결함, 잘 된 부분 KEEP 지시를 뽑고 코드 되돌린 뒤 계획 수정 후 재구현), patch(자동 수정), defer(보류 목록), reject. 리뷰어가 매긴 심각도는 무시("they lack the context to grade").
- bad_plan 재구현 루프 상한 5회. 넘으면 "review repair loop exceeded 5 iterations (non-convergence)"로 blocked 정지.

### 사람 개입 지점
- build-auto는 구현과 리뷰 단계에서 질문과 승인 대기 금지. 대신 불확실하면 멈추고(blocked) 사유를 남기는 방식. 사람은 정지 결과를 보고 다음 호출을 결정.
- 라우터(`bmad`)는 완료 불확실 시 사용자에게 묻는 쪽.

### 설치하는 훅/가드
- 읽은 파일 범위에서 Claude Code 훅이나 권한 설정은 보이지 않음. 대신 Python 렌더 스크립트(`uv run`)가 템플릿을 설정값으로 렌더해 워크플로를 만듦. 작업 전 git 작업 트리가 깨끗한지 확인.

### 독립적 평판과 이슈
- #2280(닫힘): v6.3.0 Party Mode가 페르소나를 하위 에이전트로 띄우고 도구 사용을 막자, 하위 에이전트가 오케스트레이터의 400단어 미만 요약 외에 문맥이 없어 품질이 떨어짐. 제보자 표현 "every test fabricated or deviated from the workflow template"(제목), 각 구성 N=1 일화라고 스스로 한정.
- #511: 스토리마다 새 창을 열어야 하고 dev 단계가 같은 파일을 반복해 읽어 토큰이 많이 듦.
- #2767: 참조로만 적힌 요구사항이 구현 에이전트에게 전달되지 않고 조용히 누락.
- 외부 블로그나 HN 비평은 이 프로젝트에 대해 따로 검색하지 않음.

### 측정 주장 vs 독립 검증
- README에 정량 성능 주장은 찾지 못함.

### 공급망 위험(말로 서술)
- 설치가 npx로 외부 skills CLI를 실행하고 uv로 Python 스크립트를 실행. 매 build-auto 호출이 프로젝트 안 렌더 스크립트를 캐시 없이 실행하므로 `_bmad/scripts`가 변조되면 매 실행이 영향받음 [추론].

## 9. SuperClaude-Org/SuperClaude_Framework

- 저장소: https://github.com/SuperClaude-Org/SuperClaude_Framework
- 수치(gh api): 별 23,905, 마지막 push 2026-09-27, 생성 2025-06-22, 보관 아님, MIT, 최신 릴리스 v4.3.0(2026-03-22, 조사 시점 기준 6개월 전), 열린 이슈+PR 72
- 기여자 집중도: 44명 커밋 합 345 중 mithun50 143, NomenAK 120, kazukinakai 16. 커밋 수 자체가 작음(별 대비).
- 성격: 슬래시 명령 30개, 페르소나 에이전트, 모드, MCP 서버 연동을 묶은 설정 프레임워크. 오케스트레이션 관련 요소는 `/sc:spawn` 명령과 PM Agent. 이 조사에서 읽은 것은 README 설치와 성능 부분, `src/superclaude/commands/spawn.md` 앞 80행, `src/superclaude/agents/pm-agent.md`의 목차와 세션 수명주기 및 Boundaries 부분, 자체 ROI 분석 문서의 결론 부분.

### 마스터 역할
- `/sc:spawn`: 흐름은 Analyze → Decompose(Epic → Story → Task → Subtask) → Orchestrate(순차, 병렬, 적응형 전략) → Monitor → Integrate. 도구는 TodoWrite로 계층 과제 추적. 그러나 문서 내용이 "Intelligent coordination strategy selection", "Advanced dependency analysis and resource optimization" 같은 서술어 수준이고, 하위 에이전트에게 무엇을 어떤 형식으로 넘기는지, 완료를 어떻게 판정하는지는 정의되지 않음. 실질적으로는 모델에게 "잘 쪼개서 잘 하라"는 프롬프트 [추론].
- PM Agent: 구현은 직접 하지 않고 전문 에이전트 위의 "meta-layer"로서 문서화, 실수 분석, 패턴 추출, 월간 문서 정리를 담당. 세션 시작마다 Serena MCP 메모리에서 pm_context, current_plan, last_session, next_actions를 읽어 "Previous / Progress / Next / Blockers"를 보고. 작업 중에는 PDCA(Plan에서 가설 문서 작성, Do, Check, Act) 순환.

### 하위 에이전트 지시 방식, 상태, 완료 규칙, 재시도, 사람 게이트
- 지시 필드 규격: 읽은 범위에서 없음.
- 상태: 외부 MCP(Serena) 메모리 키와 `docs/temp/hypothesis-날짜.md` 같은 문서. MCP가 없으면 이 연속성 장치가 작동하지 않는 구조 [추론].
- 완료 판정, 재시도 상한, 사람 승인 게이트: 읽은 범위에서 명시적 규칙을 찾지 못함.

### 설치하는 훅/가드
- 읽은 범위에서 훅 설치는 확인 못 함. 설치기는 pipx 패키지 또는 저장소의 설치 셸 스크립트로 명령 파일을 사용자 Claude 설정에 복사하고, 선택적으로 MCP 서버를 설치.

### 독립적 평판과 이슈
- 자기 부정 문서: 저장소 안 `docs/research/pm_agent_roi_analysis_2025-10-21.md`가 "For most use cases, PM Agent development is not justified based on ROI analysis", "80% of users: Use Claude 4.5 as-is", "Adding PM Agent = Reinventing features already in Claude 4.5"라고 결론. 프로젝트 핵심 기능 하나를 스스로 불필요하다고 평가한 드문 사례.
- 설치 문제가 이슈 상위를 차지: #161 "This doesn't work..... installation docs are wildly out of date", #481(최신 버전 설치 불가, 댓글 32), #410(열림, 설치 후 Claude Code 멈춤), #494(에이전트가 설치 안 됨), #92(템플릿과 @멘션 확장이 동작 안 함).
- #457: 설치기가 추천 MCP 게이트웨이(airis-mcp-gateway)를 존재하지 않는 다른 조직 주소에서 받으려다 실패. 고치는 PR이 병합됐다가 되돌려졌다고 제보. 실제 게이트웨이 저장소(agiletec-inc, 별 172)의 주 기여자 kazukinakai는 SuperClaude 3위 기여자이기도 함. README가 이 게이트웨이를 "2-3x faster", "30-50% fewer tokens"의 수단으로 소개하므로 이해관계가 있는 추천임.
- 외부 블로그나 HN 비평은 이 프로젝트에 대해 따로 검색하지 않음.

### 측정 주장 vs 독립 검증
- README "For 2-3x faster execution and 30-50% fewer tokens, optionally install MCP servers": 측정 방법 링크를 README에서 찾지 못함. 게이트웨이 제작자와 프레임워크 기여자가 겹침. 독립 검증 없음.

### 공급망 위험(말로 서술)
- 설치기가 존재하지 않는 GitHub 주소에서 MCP 서버를 받으려 한 이력(#457). 그 조직명과 저장소명을 제3자가 선점하면 설치기가 제3자 코드를 받아 실행하는 구조였을 수 있음 [추론, 현재 코드의 URL은 재확인하지 않음].
- 셸 설치 스크립트와 MCP 자동 설치.

## 10. smtg-ai/claude-squad (대조군: 마스터 없는 세션 관리자)

- 저장소: https://github.com/smtg-ai/claude-squad
- 수치(gh api): 별 8,537, 마지막 push 2026-08-20, 생성 2025-03-09, 보관 아님, AGPL-3.0, 최신 릴리스 v1.0.20(2026-08-20), 열린 이슈+PR 55
- 기여자 집중도: 20명 커밋 합 222 중 mufeez-amjad 116, jayshrivastava 87. 2인 공동.
- 성격: Go로 만든 터미널 UI. Claude Code, Codex, Aider 등 여러 에이전트 세션을 tmux 세션과 git worktree로 격리해 동시에 띄우고 사람이 목록에서 골라 보고 diff 확인, 커밋, push하는 도구. 이 조사에서 읽은 것은 README 전체.

### 마스터 설계
- 마스터 에이전트가 없음. 과제 분해와 배정, 결과 검토, 병합 판단을 모두 사람이 함. 즉 "사람이 오케스트레이터"인 구조. 마스터 오케스트레이터 설계의 대조군으로 포함.
- 상태: 세션별 tmux 세션과 worktree 브랜치. 완료 규칙, 재시도, 위임 템플릿 없음.

### 사람 개입 지점과 가드
- 기본은 에이전트가 권한을 물으면 사람이 해당 세션에 들어가 답함. 실험 옵션으로 모든 인스턴스가 Claude Code와 Aider의 확인 프롬프트를 자동 수락하는 모드가 있고 README 기능 목록에 "yolo / auto-accept mode"로 광고.
- 훅 설치 없음.

### 독립적 평판과 이슈
- 이슈 상위는 세션 생성 실패(#132, #96), 새 세션에 MCP 서버 설정이 안 따라옴(#143), 자동 수락 모드 미작동(#151), TUI 느림(#215). 비용이나 폭주 루프 보고는 키워드 검색에서 보이지 않음. 마스터가 없어서 루프가 생길 구조가 아니기 때문으로 보임 [추론].

### 공급망 위험(말로 서술)
- Homebrew 설치 외에 원격 설치 스크립트를 받아 바로 셸로 실행하는 방식도 안내. AGPL-3.0이라 수정본을 네트워크 서비스로 제공하면 소스 공개 의무가 생김(사내 도구화 시 법무 검토 필요) [추론].

## 11. yohey-w/multi-agent-shogun (그리고 저자의 해체 선언)

- 저장소: https://github.com/yohey-w/multi-agent-shogun
- 수치(gh api): 별 1,424, 마지막 push 2026-08-06, 생성 2026-01-25, 보관 아님, MIT, 최신 릴리스 v5.1.0(2026-05-23), 열린 이슈+PR 7
- 기여자 집중도: 11명 커밋 합 365 중 yohey-w 309(약 85%).
- 성격: 여러 코딩 CLI(Claude Code, Codex, Copilot, Kimi, OpenCode, Cursor, Antigravity)를 tmux 창에 띄워 봉건 군대처럼 계층화. Shogun(사용자 명령 수신, 즉시 위임) → Karo(과제 분해와 배정) → Ashigaru 7명(실행) + Gunshi(품질 검사와 고난도 분석). 에이전트 간 통신은 디스크의 YAML 파일과 tmux 알림. 이 조사에서 읽은 것은 README 전체(이전 조사 때 받은 사본을 이번에 재확인)와 `instructions/karo.md`(944행 중 약 250행).
- 중요: README 맨 위에 2026년 8월 추가된 "Sequel" 공지. 저자가 10에이전트 군대를 해체하고 자기 판단을 담은 단일 에이전트 후속 프로젝트(kagemusha)로 옮겼다고 밝힘. 해체 글(Zenn, 일본어)을 요약 도구로 읽은 요지: 멀티 에이전트 조율 기능이 공식 플러그인 등 "표준 기능"이 되면서 차별점이 사라졌고, 남는 자산은 "오레의 판단 버릇", 즉 사람이 반려하고 교정한 기록의 축적뿐이라는 것("オレの却下の蓄積だけは、誰も出荷できない", 내가 반려한 것의 축적만은 누구도 출하할 수 없다). 원문 정독은 아님.

### 마스터(Shogun과 Karo)가 하는 일
- Shogun은 명령을 받아 즉시 Karo에게 넘김. Karo는 금지 행동 목록으로 역할을 강제: F001 직접 실행 금지(Ashigaru에게 위임), F002 사람에게 직접 보고 금지(dashboard.md 갱신으로 대체, 사람 입력 중 끼어들기 방지), F003 실행에 Claude Code Task 서브에이전트 사용 금지(문서 읽기와 분해, 분석은 예외), F004 폴링과 대기 루프 금지(이벤트 구동만), F005 문맥 읽기 생략 금지.
- 분해 원칙: "Split and parallelize whenever possible", 같은 파일에 여러 Ashigaru를 쓰게 하지 말 것. 과제 난이도를 Bloom 분류 수준으로 매겨 L1~L3은 Ashigaru, L4~L6은 Gunshi.
- 대기 방식: Claude Code는 "기다릴" 수 없으므로 배정 후 스스로 멈추고, Gunshi의 QC 완료 알림으로 깨어나면 모든 보고 파일을 전수 스캔("Wake = Full Scan").

### 하위 에이전트 지시 방식(위임 템플릿 필드)
- 과제 YAML: task_id, parent_cmd, bloom_level, description, target_path, echo_message(전국시대 말투의 출진 구호), status(assigned, blocked 등), blocked_by, timestamp. 의존성은 같은 명령 안에서만.
- 모든 내부 독백과 진행 보고를 전국시대 말투로 하라는 규칙이 있음(토큰을 쓰는 연출 요소).

### 상태 저장
- `queue/`(shogun_to_karo.yaml, tasks/, reports/), `dashboard.md`(Karo와 Gunshi만 수정), `saytask/streaks.yaml`, `logs/daily/`. 역할별로 쓸 수 있는 파일을 에이전트 정의에서 제한(OpenCode의 경우 README에 명시).

### 완료/검증 규칙
- 실행 결과는 Ashigaru → Gunshi(QC) → Karo 순으로 전달. 하위 과제가 모두 끝나면 Karo가 원래 명령의 목적을 다시 읽고 산출물 전체와 대조하는 "purpose validation". 목적 미달이면 완료 처리하지 말고 추가 과제를 만들거나 대시보드의 🚨 요대응 절로 올림.
- 재시도 상한은 읽은 범위에서 찾지 못함.

### 사람 개입 지점
- 사람("Lord")은 dashboard.md의 🚨 요대응 절로만 호출됨. 대상: 스킬 후보 승격, 저작권 문제, 기술 선택, 차단 요인, 질문. 요대응 항목이 늘면 휴대폰 푸시 알림(ntfy).
- 반복 패턴을 Ashigaru가 스킬 후보로 제안하고 사람이 승격 여부를 결정.

### 설치하는 가드와 위험(말로 서술)
- 첫 실행 시 Claude Code를 권한 확인 전면 생략 옵션으로 띄워 그 모드를 승인하게 하는 절차가 README 빠른 시작에 포함. Antigravity 작업자도 같은 성격의 옵션으로 실행.
- Windows에서는 ZIP을 받아 설치 배치 파일을 "관리자 권한으로 실행"하라고 안내(WSL2와 Ubuntu 자동 설치).

### 독립적 평판과 이슈
- 이슈 수가 적고 비용이나 루프 보고는 키워드 검색에서 보이지 않음(사용자 기반이 작음).
- README의 비교표는 "Coordination cost: Zero (YAML + tmux)"라고 주장. 조율 LLM 호출이 없다는 뜻이지만, Karo와 Gunshi 자체가 LLM 세션이므로 조율 비용이 0은 아님 [추론].
- 가장 강한 독립 신호는 저자 자신의 해체 결정.

## 12. Ralph 계열: mikeyobrien/ralph-orchestrator, Anthropic 공식 ralph-wiggum 플러그인 (마스터 없는 반복 루프)

- 저장소: https://github.com/mikeyobrien/ralph-orchestrator, https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum
- ralph-orchestrator 수치(gh api): 별 3,159, 마지막 push 2026-09-27, 생성 2025-09-07, 보관 아님, MIT, 최신 릴리스 v2.10.1(2026-06-23), 열린 이슈+PR 7. 기여자 35명 커밋 538 중 mikeyobrien 457(약 85%).
- 성격: "Ralph Wiggum 기법"은 같은 프롬프트로 에이전트를 완료 신호나 반복 상한까지 계속 다시 돌리는 방식. 마스터가 과제를 나누는 대신 "루프 자체"가 오케스트레이터. 이 조사에서 읽은 것은 ralph-orchestrator README 전체(289행)와 Anthropic 플러그인 README의 핵심 줄.

### 설계 요점
- ralph-orchestrator: `ralph plan`이 대화형으로 requirements.md, design.md, implementation-plan.md를 `.ralph/specs/` 아래 만들고, `ralph run`이 에이전트가 `LOOP_COMPLETE`를 출력하거나 반복 상한에 닿을 때까지 반복. "Hat System"(역할 페르소나가 이벤트로 조율), "Backpressure"(테스트, lint, 타입체크 게이트가 미완성 작업을 거부), 지속 메모리와 과제 추적.
- 사람 개입: Telegram 봇 연동. 에이전트가 `human.interact` 이벤트를 내면 응답이 오거나 시간 초과될 때까지 루프가 멈춤. 사람이 언제든 선제적으로 지시를 보낼 수 있고 `/status`, `/tasks`, `/restart` 명령 제공. 이번 조사 대상 중 "비동기 사람 게이트"를 가장 명확히 제품화한 사례.
- Anthropic 플러그인: Stop 훅이 세션 종료를 막고 같은 프롬프트를 다시 넣는 방식. README 원문상 반복 상한 옵션의 기본값은 "unlimited"이고, 완료 약속 문구는 정확한 문자열 일치라 "SUCCESS"와 "BLOCKED" 같은 복수 종료 조건을 못 씀. 그래서 "Always rely on --max-iterations as your primary safety mechanism"이라고 권고. 즉 공식 구현도 기본값만으로는 무한 루프가 가능하고 상한 설정을 사용자 책임으로 둠.
- README 사례 문구 "One $50k contract completed for $297 in API costs"는 일화이며 측정 근거 링크는 읽은 범위에 없음.

### 공급망 위험(말로 서술)
- ralph-orchestrator는 GitHub 릴리스의 설치 스크립트를 받아 바로 셸로 실행하는 방식을 안내(npm, cargo 경로도 있음). 웹 대시보드는 첫 실행 시 자동으로 npm 의존성을 설치. Telegram 봇 토큰을 설정 파일이나 환경 변수에 둠.

## 13. automazeio/ccpm (Claude Code PM)

- 저장소: https://github.com/automazeio/ccpm
- 수치(gh api): 별 8,390, 마지막 push 2026-03-18(조사 시점 약 6개월 전), 생성 2025-08-18, 보관 아님, MIT, GitHub 릴리스 없음, 열린 이슈+PR 4
- 기여자 집중도: 9명 커밋 87 중 ranaroussi 66(약 76%).
- 성격: PRD → 에픽 → GitHub 이슈 → 병렬 구현으로 이어지는 PM 스킬. 상태의 원천을 GitHub Issues로 둠. 이 조사에서 읽은 것은 README(이전 조사 사본) 중 병렬 실행, 결과 주장, 벤치마크 절.

### 설계 요점
- 메인 대화가 "conductor"로 남고, 이슈 하나를 DB, 서비스, API, UI, 테스트 같은 작업 스트림으로 쪼개 에이전트 여러 개를 동시에 돌림. README 원문은 이 스트림들이 "All running simultaneously in the same worktree"라고 적음. superpowers SDD가 충돌을 이유로 구현 에이전트 병렬 투입을 금지하는 것과 정반대 선택.
- 상태: 로컬 `.claude/epics/` 파일과 GitHub 이슈, 이슈 댓글로 진행 공유. 사람과 에이전트가 같은 이슈 보드를 봄.
- 완료 규칙, 재시도 상한, 사람 승인 게이트: 읽은 범위에서 명시 규칙을 찾지 못함.

### 측정 주장 vs 독립 검증
- "Teams using this system report: 89% less time lost to context switching, 75% reduction in bug rates, Up to 3× faster": 출처, 표본, 방법이 없음.
- "Eval score 100%" 배지와 벤치마크 표: PRD 작성 4/4, 이슈 실행 4/4, 스탠드업 3/3 대 기준선 27.7%. 총 11개 시나리오이고, 평가 항목이 "올바른 경로, worktree 확인, 스크립트 실행" 같은 절차 준수 여부라 코드 품질이나 결과물 정확성 측정이 아님 [추론, 평가 스크립트는 읽지 않음].
- 독립 평판은 따로 검색하지 않음.

---

## 비교표

수치는 2026-09-28 `gh api` 기준. "마스터 설계"는 읽은 파일 기준 요약.

| 프로젝트 | 별 | 마지막 push | 라이선스 | 마스터 설계 | 상태 저장 | 사람 게이트 | 위험 신호 |
|---|---|---|---|---|---|---|---|
| obra/superpowers (SDD) | 292,177 | 2026-09-27 | MIT | 컨트롤러가 과제마다 새 구현자 1명 + 리뷰어, 직접 수정 금지, 구현 병렬 금지 | 계획별 작업공간의 progress.md 원장, brief, 보고서 파일 | 파괴적, 보안, 작업트리 밖 부작용, 전부 추측인 계획의 4가지만 정지 | 토큰 과다 보고(#1152), 리뷰 생략 보고(#463, v6에서 대응 주장), 세션 시작 훅, 1인 80% |
| revfactory/harness | 9,074 | 2026-09-26 | Apache-2.0 | 오케스트레이터를 생성하는 메타 스킬. 3모드(워크플로, 지속형, 서브에이전트) | `_workspace/`, run_meta.json, 산출물 해시 동결 | 팀원 절반 이상 실패 시 확인, 사용량 한도 시 보고 | 조용한 실패 3종 보고(#53), 자체 측정 n=15, 코드 없음 |
| code-yeongyu/oh-my-openagent | 69,601 | 2026-09-27 | SUL-1.0(비OSI) | Atlas: 6절 위임 프롬프트, 기본 병렬, 매 위임 4단계 직접 검증, F1~F4 최종 승인 | `.omo/plans` 체크박스, `.omo/notepads` 4파일, boulder-state | 계획 단계 사이 승인 질문 금지 | 재시도 상한 모순("Retry 3x" vs "no retry cap"), 6시간 폭주 루프(#3446), 기본 원격 통계, 구독 약관 논란 |
| Yeachan-Heo/oh-my-claudecode | 39,376 | 2026-09-27 | MIT | Team: plan → prd → exec → verify → fix, 단계별 전문 에이전트 라우팅 | MCP 상태 도구(세션 범위), `.omc/handoffs` 5필드 인계 | 명시 게이트 확인 못 함 | Stop 훅 지속 모드 폭주와 토큰 낭비(#2652, #3138), 거의 모든 훅 이벤트에 스크립트, 일부 셸 자동 허용 |
| ruvnet/ruflo (claude-flow) | 73,398 | 2026-09-27 | MIT | Queen: 공유 메모리에 "royal directives" JSON 기록, 완료 기준 없음 | MCP 메모리(SQLite + HNSW), 다수 숨김 디렉터리 | 없음(연합은 "no human in the loop") | 스텁과 조작 지표(#1514, 메인테이너 일부 인정), 스웜 런타임 미작동(#1896), 난독화 설치 스크립트와 프롬프트 인젝션 이력(#1375), 넓은 셸 자동 허용 |
| gastownhall/gastown | 18,204 | 2026-09-18 | MIT | Mayor: 이슈(bead) 만들어 작업자에게 sling, "No confirmation. No questions." | Beads + Dolt SQL, hook, 메일 | hook이 빌 때만 사람 대기, 작업자 완료에 승인 단계 없음 | 권한 확인 전면 생략이 기본, 무한 재시작 루프(#4044), DB 폭주(#4145), 고비용 보도 |
| open-gsd/gsd-core (구 get-shit-done) | 9,898 (구 64,446, 보관됨) | 2026-09-27 | MIT | 가벼운 오케스트레이터, wave 병렬, 새 문맥 실행자, 목표 검증 에이전트 | `.planning/` STATE, PLAN, SUMMARY, VERIFICATION | 로드맵 승인, 체크포인트 3종(자동 모드는 일부 자동 승인) | 옛 README가 권한 생략 실행 권장, 에이전트 100개 이상 생성 보고(#120), 저장소 이전 |
| bmad-code-org/BMAD-METHOD | 53,554 | 2026-09-27 | MIT(API는 NOASSERTION) | 읽기 전용 라우터 + 무인 1회 루프(티켓 하나), intent-contract 고정 | 계획 파일 frontmatter와 로그 절 | 무인 루프는 질문 대신 blocked 정지 | 하위 에이전트 문맥 부족으로 품질 저하(#2280), 반복 파일 읽기 토큰 |
| SuperClaude_Framework | 23,905 | 2026-09-27 | MIT | `/sc:spawn` 서술형 분해 프롬프트, PM Agent 메타층 | Serena MCP 메모리 키 | 확인 못 함 | 자체 ROI 문서가 PM Agent 불필요 결론, 설치 오류 다수, 없는 주소에서 MCP 설치 시도(#457), 이해관계 있는 성능 주장 |
| smtg-ai/claude-squad | 8,537 | 2026-08-20 | AGPL-3.0 | 마스터 없음(사람이 오케스트레이터) | tmux 세션 + worktree | 사람이 전부 | 자동 수락 실험 모드 광고, 원격 스크립트 설치 |
| yohey-w/multi-agent-shogun | 1,424 | 2026-08-06 | MIT | Shogun → Karo(금지행동 F001~F005) → Ashigaru + Gunshi QC, 목적 재검증 | YAML 큐, dashboard.md | 🚨 요대응 절 + 푸시 알림 | 권한 생략 실행 안내, 관리자 권한 설치, 저자가 2026-08 해체 선언 |
| ralph-orchestrator / ralph-wiggum | 3,159 (orchestrator) | 2026-09-27 | MIT | 마스터 없이 완료 신호까지 같은 프롬프트 반복, 게이트(테스트, lint) | `.ralph/specs`, 메모리 | Telegram 비동기 질문과 차단 | 공식 플러그인 반복 상한 기본값 무제한, 원격 스크립트 설치 |
| automazeio/ccpm | 8,390 | 2026-03-18 | MIT | 메인 대화가 지휘, 이슈를 스트림으로 쪼개 같은 worktree에서 병렬 | `.claude/epics/` + GitHub Issues | 확인 못 함 | 근거 없는 효과 수치, 절차 준수만 재는 11개 평가 |

## 공통 관찰

1. 마스터의 핵심 규칙은 거의 모두 "직접 하지 말고 위임하라"와 "하위 에이전트의 완료 주장을 믿지 마라" 두 가지로 수렴. superpowers("Never fix findings yourself"), OmO Atlas("conductor, not a musician", "Subagents claim "done" when code is broken"), shogun(F001 직접 실행 금지), GSD("Orchestrator coordinates, not executes"), Gas Town("If you're unsure, sling it").
2. 상태는 대화 기억이 아니라 파일에 둠. 이유로 드는 사고도 같음: 압축(compaction) 후 마스터가 위치를 잃고 끝난 일을 다시 시킴(superpowers가 "가장 비싼 실패"로 명시, OMC 인계 문서 도입 사유, GSD의 SUMMARY 기반 재개 게이트). 형태는 원장(progress.md), 계획 체크박스, frontmatter 상태, 인계 문서, DB로 다양.
3. 위임 지시문 필드는 구체적일수록 설계가 성숙. 공통 필드: 과제 본문(가능하면 파일 경로로), 기대 결과와 검증 명령, 하지 말 것, 앞 과제에서 정해진 인터페이스, 보고 형식과 보고 파일 위치, 모델 지정. 반대로 SuperClaude spawn이나 ruflo Queen처럼 필드 규격 없이 서술어만 있는 경우 실제 조율 규칙이 없음.
4. 재시도 상한이 있는 곳과 없는 곳이 갈림. 명시 상한: superpowers 5회(4회차부터 새 에이전트와 상위 모델), BMAD 5회, OMC 3회, harness 1회 + 재시도 무의미 실패 목록. 상한 없음 또는 모순: OmO Atlas("no retry cap"와 "Retry 3x" 공존), Anthropic ralph 플러그인(기본 무제한). 상한이 없거나 약한 곳에서 폭주 루프 이슈가 실제로 보고됨(OmO #3446 6시간, OMC #2652, Gas Town #4044). 이 상관은 이슈 키워드 검색 결과에 기반한 관찰이며 인과를 입증한 것은 아님.
5. "계속 실행" 장치(Stop 훅으로 종료 막기, idle 시 계속 프롬프트 주입)가 폭주의 직접 원인으로 반복 등장. 특히 모델이 "막혔다"고 말만 하고 상태 파일을 안 바꾸면 성공으로 집계되어 실패 카운터가 리셋되는 패턴(OmO #3446). Claude Code 자체에도 연속 차단 9회 강제 종료 안전장치가 있다는 보고(OMC #3138).
6. 사람 게이트는 대부분 "기본은 묻지 마라"로 설계됨. 묻는 조건을 좁은 목록으로 명시한 곳(superpowers 4종, GSD 체크포인트 3종과 자동 승인 예외, BMAD의 blocked 정지, shogun 요대응 절, ralph Telegram)과 사실상 없는 곳(Gas Town, ruflo, OmO 단계 사이)으로 나뉨.
7. 권한 확인 전면 생략 실행을 기본값이나 권장으로 둔 프로젝트가 여럿(Gas Town 기본값, 옛 GSD README 권장, shogun 빠른 시작, claude-squad 실험 모드 광고, ruflo 넓은 자동 허용). 이 경우 마스터의 판단 오류나 프롬프트 인젝션이 곧 저장소 변경과 push로 이어짐.
8. 성능 주장은 거의 전부 자체 측정이거나 근거 없음. 독립 감사가 있었던 ruflo는 도구 다수가 스텁이고 지표가 조작되었다는 결과가 나왔고 메인테이너가 일부 인정. 자체 측정을 스스로 한정한 곳은 harness(n=15 명시)뿐.
9. 별 수와 신뢰도는 무관. 별이 가장 많은 축에 드는 ruflo가 가장 심각한 감사 결과를 받았고, 별 64k의 GSD 원 저장소는 보관됨. 대부분 1인 기여 65~97%.
10. 멀티 에이전트를 가장 공격적으로 밀던 저자 중 하나(shogun)가 스스로 해체하고 "판단 기록을 담은 단일 에이전트"로 돌아섬. Gas Town에 대한 외부 비평도 병목은 구현이 아니라 설계와 판단이라고 지적.

## 가져올 것 / 피할 것 [추론]

아래는 위 조사에서 끌어낸 내 해석이며, 부서 에이전트 위 마스터를 만드는 목적에 맞춰 정리한 것.

### 가져올 것 [추론]
- 마스터는 조율 전용으로 두고 직접 작업을 금지하되, 금지 목록을 명시적 ID로 적기(shogun F001~F005 방식). 마스터 문맥을 깨끗하게 유지하는 효과를 superpowers, OmO, GSD가 공통으로 노림.
- 위임 템플릿을 고정 필드로 만들기: 과제 위치 한 줄, 요구사항 파일 경로(본문 붙여넣기 대신), 앞 단계 결정과 인터페이스, 마스터가 내린 모호성 해석, 기대 결과와 검증 방법, 하지 말 것, 보고 파일 경로와 보고 상태값(DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED). superpowers와 OmO 6절 구조의 합.
- 진행 상태는 파일 원장에 한 줄씩 추가 기록하고, 압축이나 재시작 후엔 원장을 기억보다 우선. 부서 간 인계는 OMC의 Decided, Rejected, Risks, Files, Remaining 5필드 문서.
- 완료는 하위 에이전트의 보고가 아니라 별도 검증자 판정과 파일 증거로. 검증자는 계획서를 "testimony, not evidence"로 취급하고 증거 추적 후에야 주장을 대조(BMAD claims-check). 마지막엔 원래 요청의 목적을 다시 읽고 산출물 전체와 대조(shogun purpose validation, GSD "GOAL, not just completed tasks").
- 재시도 상한을 반드시 숫자로 두고, 상한 도달 시 "모델 상향 또는 새 에이전트 → 그래도 안 되면 판정 기록 후 보류 또는 정지"로 끝나게. 재시도해도 소용없는 실패(사용량 한도, 인증 만료, 권한 거부)는 재시도 금지 목록으로(harness).
- 마스터가 사람 대신 내린 판정은 모두 "무엇, 왜, 틀리면 비용" 형식으로 기록하고 마지막에 빠짐없이 보고(superpowers Rulings). 사람 게이트는 좁은 목록으로 명시하고, 사람 호출은 비동기 채널 하나로 모으기(shogun 요대응 절, ralph Telegram).
- 단계 경계에서 산출물 동결과 해시 기록(harness). 부서 에이전트가 완료 후에도 메시지를 받아 이미 넘긴 결과를 고치는 문제를 막음.
- 모델 지정을 필수 필드로 두고 생략 시 비싼 모델 상속을 막기(superpowers, GSD 모두 경고).

### 피할 것 [추론]
- 종료를 막아 계속 돌리는 Stop 훅이나 idle 자동 계속 주입을 상한과 "진짜 진전" 판정 없이 쓰는 것. 텍스트 응답을 성공으로 세어 실패 카운터를 리셋하는 구조는 특히 위험(OmO #3446).
- 재시도 상한을 프롬프트 안에서 서로 모순되게 적는 것(OmO Atlas). 모델은 어느 쪽이든 고를 수 있음.
- 권한 확인 전면 생략을 기본값으로 두고 마스터나 작업자가 main에 직접 push하게 하는 것(Gas Town). 부서 에이전트가 외부 시스템(마케팅 발송, 운영 변경)에 닿는다면 더 위험.
- 은유와 연출(여왕, 왕실 칙령, 전국시대 말투, 사기 "high")로 채운 마스터 프롬프트. 측정 없이 고정값을 기록하게 만드는 예시 JSON(ruflo Queen)은 가짜 지표의 씨앗이 됨.
- 넓은 셸 자동 허용, 최신 버전을 매번 자동 설치하는 MCP 등록, 원격 스크립트 즉시 실행 설치를 그대로 따라 하는 것. 외부 프레임워크를 도입한다면 훅과 권한 설정을 먼저 읽고 필요한 것만 옮기기.
- 병렬 구현자를 같은 작업 트리에서 동시에 돌리는 것(ccpm 방식). 병렬이 필요하면 worktree 분리와 공유 파일 단일 소유자 규칙(GSD의 STATE, ROADMAP은 오케스트레이터만 수정)을 함께.
- 하위 에이전트에게 짧은 요약만 주고 도구를 막는 것(BMAD #2280). 요약 대신 파일 경로와 읽기 도구를 주기.
- 별 수, README 수치, "eval 100%" 배지를 근거로 채택하는 것. 도입 전 자기 과제로 소규모 파일럿을 돌리고 토큰과 결과를 직접 재기.
- 구조가 커지기 전에 shogun 저자의 결론을 먼저 검토할 것: 조율 배관은 곧 표준 기능이 되고, 오래 남는 자산은 사람의 교정과 반려 기록. 마스터 설계에 "사용자 판단 기록을 누적해 규칙으로 승격하는 경로"를 처음부터 넣는 편이 배관을 늘리는 것보다 나을 수 있음.
