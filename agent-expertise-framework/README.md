# agent-expertise-framework

이 폴더 자체가 트리다. [08-agent-implementation-schema.md](08-agent-implementation-schema.md)가 뿌리(전체를 종합하는 일반형 스키마)고, 그 아래 4개 폴더가 `01-research-summary.md`의 4요소를 하나씩 맡는 자식이다. 새 연구 주제가 생기면 기존 4개 폴더 중 어디에 속하는지 먼저 판단하고, 안 맞으면 5번째 폴더를 새로 만든다 — 폴더를 안 늘리고 파일만 계속 늘어놓지 않는다.

```
08-agent-implementation-schema.md   ← 뿌리: 4요소 + Agent 해부학을 종합한 일반형
│
├── 00-data-lake/                   ← 요소1: 정합적인 data lake
│   ├── 00-llm-friendly-docs-framework.md
│   └── 01-research-summary.md
│
├── 01-narrow-interface/            ← 요소2: 좁고 명시적인 인터페이스
│   ├── 02-instruction-clarity-incident.md
│   └── 03-instruction-resolution-gate.md
│
├── 02-self-improvement-loop/       ← 요소3: 안전한 응답 필터 (+ 그 필터를 검증하는 루프)
│   ├── 04-purpose-and-self-improvement-loop.md
│   ├── 05-pipeline-options-and-plan.md
│   └── eval/
│
├── 03-orchestration-and-enforcement/  ← 요소4: 실패 사례 기반 금지 규칙 (+ 그걸 구조로 강제하는 실행)
│   ├── 06-orchestrator-pattern.md
│   ├── 07-harness-and-hook-enforcement.md
│   ├── 10-orchestration-evidence-2023-2025.md
│   ├── 11-orchestration-current-2026.md
│   └── 12-orchestration-application.md
│
├── 04-kakaopay-baseline/              ← 4요소를 실제 시스템 수준으로: 카카오페이 기술블로그 바닥선
│   ├── 13-kakaopay-tech-blog-study.md
│   ├── 14-kakaopay-baseline-and-target.md
│   ├── posts/                         (글별 원문 노트 24개)
│   └── diagrams/                      (14번 한 화면 흐름도)
│
└── 05-master-orchestrator/            ← 개별 에이전트 한 층 위: 부서 에이전트를 조율하는 마스터(자비스형)
    ├── 15-master-orchestrator-research.md
    └── sources/                       (원문 조사 3개)
```

## 폴더별 내용

| 폴더 | 담당 요소 | 안에 있는 문서 |
|---|---|---|
| [00-data-lake/](00-data-lake/) | 요소1: 정합적인 data lake | [00-llm-friendly-docs-framework.md](00-data-lake/00-llm-friendly-docs-framework.md) — 세션의 출발점. LLM용 문서 작성 12원칙(명시성, 상태 구분, 용어집, Constraints, ADR 등). [01-research-summary.md](00-data-lake/01-research-summary.md) — 그 프레임워크를 Amoro/Iceberg/Paimon으로 검증한 결과, 4요소로 정리된 최종 결론 |
| [01-narrow-interface/](01-narrow-interface/) | 요소2: 좁고 명시적인 인터페이스 | [02-instruction-clarity-incident.md](01-narrow-interface/02-instruction-clarity-incident.md) — 반대 방향 사례: LLM에게 지시할 때 생기는 오판 실사례. [03-instruction-resolution-gate.md](01-narrow-interface/03-instruction-resolution-gate.md) — 그 사건을 재료로 설계한 요구사항 해석 게이트(조회형/결정형 구분, 검색과 질문이 맞물리는 조립 루프, 분야별 슬롯 스키마, 완성 프롬프트 확인, 구조적 강제) |
| [02-self-improvement-loop/](02-self-improvement-loop/) | 요소3: 안전한 응답 필터 | [04-purpose-and-self-improvement-loop.md](02-self-improvement-loop/04-purpose-and-self-improvement-loop.md) — 00번 12원칙의 약점 보완 + 평가→원인진단→개선 자체개선 루프 설계, [eval/](02-self-improvement-loop/eval/)에 그라운딩 metric·필터 recognizer 실제 구현. [05-pipeline-options-and-plan.md](02-self-improvement-loop/05-pipeline-options-and-plan.md) — 그 루프를 실제로 연결하는 파이프라인 4안 비교 |
| [03-orchestration-and-enforcement/](03-orchestration-and-enforcement/) | 요소4: 실패 사례 기반 금지 규칙 | [06-orchestrator-pattern.md](03-orchestration-and-enforcement/06-orchestrator-pattern.md) — 이 세션이 실제로 수행한 분해→위임→검증 오케스트레이터 패턴, 실제 워커 에이전트(`.claude/agents/`) 정의. [07-harness-and-hook-enforcement.md](03-orchestration-and-enforcement/07-harness-and-hook-enforcement.md) — 카카오페이 원문 재조사, "Hook은 확정·프롬프트는 확률" 원칙을 실제 Hook으로 전환. [10-orchestration-evidence-2023-2025.md](03-orchestration-and-enforcement/10-orchestration-evidence-2023-2025.md): 오케스트레이션 외부 근거 모음(Anthropic, OpenAI, MS, Google, MAST, 조직형 멀티에이전트, 검사 에이전트 신뢰성), 출처마다 연도 표시. [11-orchestration-current-2026.md](03-orchestration-and-enforcement/11-orchestration-current-2026.md): 10번 결론이 2026년 모델에서도 맞는지 재검증한 판정표와 2026년 가이드, 운영 사례, 업무 벤치마크. 10과 다르면 11을 따른다. [12-orchestration-application.md](03-orchestration-and-enforcement/12-orchestration-application.md): 10, 11을 "부서별 에이전트 조직" 구상에 적용한 판단 |
| [04-kakaopay-baseline/](04-kakaopay-baseline/) | 4요소를 실제 시스템 수준으로: 카카오페이 바닥선 | [13-kakaopay-tech-blog-study.md](04-kakaopay-baseline/13-kakaopay-tech-blog-study.md): 카카오페이 기술블로그 AI, 에이전트, 운영 자동화 글 24개를 원문 HTML로 읽은 조사, 글들을 가로지르는 공통 원칙, 07번 문서의 원문 대조 오류 목록. [14-kakaopay-baseline-and-target.md](04-kakaopay-baseline/14-kakaopay-baseline-and-target.md): 영역별로 카카오페이 바닥선과 그 이상을 정한 설계, 한 화면 흐름도 [diagrams/system-flow.png](04-kakaopay-baseline/diagrams/system-flow.png) |
| [05-master-orchestrator/](05-master-orchestrator/) | 개별 에이전트 위의 조율 층: 마스터 에이전트 | [15-master-orchestrator-research.md](05-master-orchestrator/15-master-orchestrator-research.md): 마스터 내부 설계(작업 기록과 진행 기록 등), 자비스라는 이름의 시스템, Claude Code 위 오픈소스 오케스트레이터 13개를 원문으로 조사한 목차와 세 조사가 겹치는 결론. 설계 판단은 다음 번호 문서 |

## 뿌리 문서

[08-agent-implementation-schema.md](08-agent-implementation-schema.md) — `01`의 4요소와 `07`의 Agent 해부학(LLM/몸/Tools·Context·Skills)이 같은 결론의 다른 단면이라는 걸 확인하고 하나의 일반형으로 종합. 이 폴더 구조 자체가 이 문서가 정의한 4요소를 그대로 물리적으로 구현한 것이다. 스키마만 정의하고, agent-research 자신에게 채워 넣는 건 다음 문서(09, 미작성)로 명시적으로 미룸.

## 관련 분석 디렉터리 (같은 workspace, 형제 폴더)

- [../../data-lake/amoro-analysis](../../data-lake/amoro-analysis/README.md) — 핵심 사례 (lakehouse 관리 + 에이전트 인터페이스)
- [../../data-lake/iceberg-analysis](../../data-lake/iceberg-analysis/README.md) — 테이블 포맷 비교 대상 1
- [../../data-lake/paimon-analysis](../../data-lake/paimon-analysis/README.md) — 테이블 포맷 비교 대상 2

## 읽는 순서

처음이면 `00-data-lake/00-...` → `00-data-lake/01-...` → `08`(전체 종합) 순으로. 폴더 번호(00~03)가 곧 읽는 순서이자 요소 순서다.
