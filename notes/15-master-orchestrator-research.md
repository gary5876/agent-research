---
status: ACTIVE
layer: 1
layer_note: "외부 출처 조사 기록, 본문은 sources/master-orchestrator/"
topic: [master]
date: 2026-09-28
summary: "마스터 에이전트(자비스형) 설계를 위한 원문 조사 3개의 목차와 세 조사가 겹치는 결론"
---
# 마스터 오케스트레이터(자비스형) 조사 목차

개별 에이전트(04 폴더의 13, 14번)보다 한 층 위, 여러 부서 에이전트를 조율하는 마스터 에이전트를 설계하기 위한 조사다. 사용자 요구: "오케스트레이션을 담당하는 마스터 에이전트가 있어야 한다. 보통 자비스라는 이름이 붙는다." 설계 판단은 아직 없고, 이 폴더의 다음 번호 문서에서 한다.

## 원문 조사 3개

조사 에이전트가 출처 하나를 끝낼 때마다 파일에 덧붙이는 방식으로 썼다. 위험한 실행 옵션, 권한 설정, 원격 설치 명령은 글자 그대로 옮기지 않고 한국어로 풀어 썼다.

| 파일 | 다루는 것 | 크기 |
|---|---|---|
| [sources/master-internals.md](../sources/master-orchestrator/master-internals.md) | 마스터 내부 설계. Magentic-One(작업 기록과 진행 기록, 막힘 감지와 재계획), Microsoft Agent Framework, Anthropic 리드 에이전트와 2026년 글 3편, Managed Agents 코디네이터, Devin, Cursor, OpenAI, LangChain, Google ADK, 연구 논문 4편. 끝에 마스터 해부도 표와 마스터 고유 실패 모드 | 약 83KB |
| [sources/jarvis-named-systems.md](../sources/master-orchestrator/jarvis-named-systems.md) | 자비스라는 이름의 시스템. Microsoft JARVIS(HuggingGPT), JARVIS-1, 오픈소스 Jarvis 저장소 15개, Anthropic cookbook chief of staff, xAI Grok Bot, 회사 사례. 끝에 반복되는 설계 요소 11가지 | 약 67KB |
| [sources/oss-orchestrators.md](../sources/master-orchestrator/oss-orchestrators.md) | Claude Code 위의 오픈소스 오케스트레이터 13개(superpowers, harness, oh-my-openagent, oh-my-claudecode, ruflo, gastown, GSD, BMAD, SuperClaude, claude-squad, shogun, Ralph, ccpm). 끝에 비교표, 공통 관찰, 가져올 것과 피할 것 | 약 86KB |

## 세 조사가 겹치는 결론 (요약, 근거는 각 원문)

1. 마스터는 직접 일하지 않는다. 계획, 위임, 확인, 보고만 한다. 오픈소스들은 이걸 권한으로 강제한다(마스터는 계획 파일만 쓸 수 있음).
2. 수치 근거가 가장 강한 요소는 Magentic-One의 작업 기록과 진행 기록이다. 빼면 31% 하락(단 계획, 루프 감지, 명시 지시를 함께 뺀 절제).
3. 위임은 고정 양식으로 한다(목표, 출력 형식, 도구, 경계, 성공 기준).
4. 진행 상태는 대화 기억이 아니라 파일이나 이벤트 로그에 둔다. 완료는 에이전트 보고가 아니라 산출물과 별도 검증으로 판정한다.
5. 재시도와 재계획에 숫자 상한을 둔다. "사람에게 묻지 마라", "재시도 무제한"을 넣은 설계일수록 폭주 루프가 보고됐다.
6. 사람 승인 지점은 역할 정의와 행동 등급으로 명시한다. 코디네이터는 사람 승인을 대신할 수 없다(Managed Agents).
7. 부서형 마스터의 효과를 독립적으로 측정한 자료는 세 조사 모두에서 찾지 못했다. 오픈소스의 성능 수치는 거의 전부 자체 측정이거나 근거가 없다.

## 유명한 오케스트레이션 공부 노트

같은 틀(무엇이고 왜 인기인가, 요청 하나의 흐름, 마스터가 하는 일, 위험 검증, 비용, 보안, 가져올 것)로 하나씩 정리한다.

| 공부 노트 | 개발 과정 기록 | 한 화면 흐름도 |
|---|---|---|
| [16-superpowers-study.md](16-superpowers-study.md) | [sources/superpowers/design-history.md](../sources/superpowers/design-history.md) | [diagrams/superpowers-flow/superpowers-flow.png](diagrams/superpowers-flow/superpowers-flow.png) |
