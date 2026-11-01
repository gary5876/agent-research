# 결정 목록

방향을 정하는 결정만 여기 둔다. 문서 하나 안에서 풀 연구 질문은 그 문서의 "열린 질문" 절에 두고, [index.md](index.md)의 "다음에 할 일"이 자동으로 모아 보여 준다.

- ID는 한 번 붙이면 다시 쓰지 않는다. 상태는 `open`, `decided`, `superseded` 셋이다.
- 결정이 나면 행을 지우지 않고 상태와 결정 칸, 날짜를 바꾼다. 뒤집히면 `superseded`로 바꾸고 새 행을 단다.
- 근거 칸에는 그 결정이 나온 문서를 링크한다.

## 열린 결정

| ID | 상태 | 질문 | 결정 | 날짜 | 근거 |
|---|---|---|---|---|---|
| D01 | open | 실행 중에 새 모호함이 생기면 멈추고 다시 물을지, superpowers처럼 결정하고 기록할지, 섞을지(예: 명세 의도는 멈추고 구현 세부는 결정 후 기록) | | | [16 끝 절](notes/16-superpowers-study.md), D07과 충돌 |
| D02 | open | 마스터 설계 1절, 자비스의 역할과 권한 최종 확인 | | | [JOURNEY.md](JOURNEY.md) 6절, [17 1~4절](notes/17-orchestration-news-2026-10.md)(역할 분배보다 과제별 모델 라우팅, 승인 우회 대비) |
| D03 | open | 마스터 오케스트레이터 구현을 이 저장소에서 할지 별도 저장소에서 할지 | | | [09](notes/09-repo-structure-and-pipeline.md) |
| D04 | open | 첫 번째로 만들 "한 부서의 한 작업"을 무엇으로 할지 | | | [12 열린 질문](notes/12-orchestration-application.md), [17 1절](notes/17-orchestration-news-2026-10.md)(단일 에이전트와 스킬로 시작하는 근거) |
| D05 | open | 평가 세트 20개를 어디서 구할지 | | | [12 열린 질문](notes/12-orchestration-application.md) |
| D17 | open | 부서를 에이전트 단위로 나눌지, 스킬을 가진 단일 에이전트로 시작해 필요할 때만 나눌지 | | | [17 1절](notes/17-orchestration-news-2026-10.md), [12 3절](notes/12-orchestration-application.md) |

## 확정된 결정

| ID | 상태 | 질문 | 결정 | 날짜 | 근거 |
|---|---|---|---|---|---|
| D06 | decided | 이 저장소의 핵심 목표 | 전문성 있는 에이전트 만들기. 문서 설계는 목적이 아니라 에이전트가 정보를 빠르고 정확하게 찾게 하는 수단 | 2026-09-02 | [JOURNEY.md](JOURNEY.md) 2절, 3절 |
| D07 | decided | 계획의 명확도 기준 | 질문 개수 상한 대신 명확도 기준을 두고, 그 기준을 채울 때까지 묻는다. 계획 안의 모순은 실행 전에 푼다 | 2026-09-28 | [JOURNEY.md](JOURNEY.md) 6절 |
| D08 | decided | 생성 위키를 손으로 고치지 않는다는 규칙을 어떻게 지킬지 | 프롬프트가 아니라 PreToolUse Hook으로 막는다 | 2026-09-05 | [07](notes/07-harness-and-hook-enforcement.md) |
| D09 | decided | 문서 분류를 어디에 둘지 | 문서 자신의 태그가 유일한 원본. 카탈로그 해시 검증 시스템은 과잉이라 폐기 | 2026-09-06 | [08 §1](notes/08-agent-implementation-schema.md) |
| D10 | decided | 10번(2023~2025 근거)과 11번(2026 재검증)이 다를 때 | 11을 따른다 | 2026-09-25 | [11](notes/11-orchestration-current-2026.md), [12](notes/12-orchestration-application.md) |
| D11 | decided | 시스템의 기준선 | 카카오페이 기술블로그 수준을 바닥선으로 하고 근거가 있으면 그 이상으로 간다 | 2026-09-27 | [14](notes/14-kakaopay-baseline-and-target.md) |
| D12 | decided | 마스터 설계의 큰 틀 | B안. 판단은 자비스(마스터 에이전트), 실행 흐름은 workflow 코드 | 2026-09-28 | [JOURNEY.md](JOURNEY.md) 6절 |
| D13 | decided | 좋은 오케스트레이션의 평가 항목 | 위험 검증, 비용 최적화, 보안 검증을 포함한다 | 2026-09-29 | [JOURNEY.md](JOURNEY.md) 6절 |
| D14 | decided | 다음 공부 순서 | 설계 전에 유명한 오케스트레이션부터 공부한다. 1번은 superpowers, 남은 것은 gstack, oh-my-openagent, BMAD 등 | 2026-09-29 | [16](notes/16-superpowers-study.md), [JOURNEY.md](JOURNEY.md) 6절 |
| D15 | decided | 저장소 구조 | 자료 종류별 층(notes, sources, experiments)으로 나누고 주제는 머리말로 단다 | 2026-11-02 | [09](notes/09-repo-structure-and-pipeline.md) |
| D16 | decided | OpenWiki 재생성 방식 | Claude 세션 안에서 로컬로만 돌린다. CI 예약 워크플로와 모델 API 키는 두지 않는다 | 2026-11-02 | [09](notes/09-repo-structure-and-pipeline.md) |
