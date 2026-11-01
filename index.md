# agent-research 색인

이 저장소에서 무엇을 어디서 찾는지 보여 주는 첫 화면이다. 아래 생성 블록은 각 문서의 머리말에서 만들어진다. 분류를 바꾸고 싶으면 이 파일이 아니라 그 문서의 머리말을 고친다. 구조를 이렇게 정한 이유는 [notes/09-repo-structure-and-pipeline.md](notes/09-repo-structure-and-pipeline.md)에 있다.

## 폴더

| 위치 | 무엇이 들어가나 | 고치는 법 |
|---|---|---|
| `notes/` | 우리가 쓰는 조사 정리, 공부 노트, 설계 판단. 이름은 `NN-slug.md`이고 번호는 식별자일 뿐 분류가 아니다 | 머리말 필수 ([AGENTS.md](AGENTS.md)) |
| `sources/` | 외부 자료 한 건당 노트 하나. 원문 기록이라 쓴 뒤에는 고치지 않는다 | 새로 추가만 한다 |
| `experiments/` | 설계를 실제로 돌려 본 코드 | 폴더마다 README |
| `openwiki/` | OpenWiki가 저장소에서 만든 위키 | 손으로 고치지 않는다(Hook으로 막힘). 로컬 세션에서 재생성 |
| [decisions.md](decisions.md) | 열린 결정과 확정된 결정 | 손으로 관리하는 유일한 목록 |
| [JOURNEY.md](JOURNEY.md) | 날짜순 진행 기록과 사용자 발언 원문 | 큰 단계가 끝날 때 덧붙인다 |
| `.claude/` | 워커 에이전트 4개, Hook 2개, OpenWiki 스킬 | |
| `scripts/` | `build_index.py`(이 색인), `check.py`(커밋 전 검사) | |

## 층 (머리말의 layer)

1. 원본: 사건, 실행 기록, 외부 출처 조사 기록
2. 설계: 1층을 재료로 만든 판단과 설계
3. 구현: 실제로 돌아가는 코드와 설정
4. 생성물: 자동으로 만들어진 뷰 (`openwiki/`)

## 사용 규칙

1. 설계 문서(2층)를 인용하기 전에 그 근거가 된 원본(1층)을 먼저 확인한다. 설계 문서에는 결론만 남아 원 사건의 디테일이 빠져 있을 수 있다.
2. 구현체가 있다고 그 설계가 검증된 것은 아니다. 워커 에이전트 중 researcher는 2026-11-02 이 저장소 재편의 선행 사례 조사에 처음 쓰였고, verifier, doc-writer, supervisor는 아직 정의만 있다.
3. `openwiki/`는 재생성 대상이다. 내용을 바꾸려면 원본 문서를 고치고 다시 생성한다.

<!-- index:start -->

이 블록은 `python3 scripts/build_index.py`가 만든다. 손으로 고치지 않는다.

## 주제별 문서

### expert-agent: 에이전트 하나의 전문성 (4요소와 구현 일반형)

| 문서 | 상태 | 층 | 요약 |
|---|---|---|---|
| [00-llm-friendly-docs-framework.md](notes/00-llm-friendly-docs-framework.md) | ACTIVE | 2 | LLM이 헷갈리지 않는 문서 작성 12원칙(명시성, 상태 구분, 용어집, Constraints, ADR 등). 이 저장소의 출발점 |
| [01-research-summary.md](notes/01-research-summary.md) | ACTIVE | 2 | 12원칙을 Apache Amoro, Iceberg, Paimon으로 검증해 에이전트 전문성 4요소로 정리한 결론 |
| [08-agent-implementation-schema.md](notes/08-agent-implementation-schema.md) | ACTIVE | 2 | 4요소와 Agent 해부학을 하나로 합친 에이전트 구현 일반형(스키마) |
| [09-repo-structure-and-pipeline.md](notes/09-repo-structure-and-pipeline.md) | ACTIVE | 2 | 08 스키마를 이 저장소에 적용한 폴더 구조와 작업 파이프라인. 바꾼 이유, 선행 사례, 규칙, 이전 기록 |

### instruction: 사람의 말을 실행 지시로 바꾸는 층

| 문서 | 상태 | 층 | 요약 |
|---|---|---|---|
| [02-instruction-clarity-incident.md](notes/02-instruction-clarity-incident.md) | ACTIVE | 1 | 조회로 알 수 있는 것을 사용자에게 되물은 오판 사건 기록 |
| [03-instruction-resolution-gate.md](notes/03-instruction-resolution-gate.md) | ACTIVE | 2 | 요구사항 해석 게이트 설계. 조회형과 결정형 구분, 검색과 질문의 조립 루프, 분야별 슬롯 스키마, 완성 프롬프트 확인 |

### self-improvement: 평가와 자체개선 루프

| 문서 | 상태 | 층 | 요약 |
|---|---|---|---|
| [04-purpose-and-self-improvement-loop.md](notes/04-purpose-and-self-improvement-loop.md) | ACTIVE | 2 | 12원칙의 약점 보완과 평가, 원인 진단, 개선으로 도는 자체개선 루프 설계. 일부는 experiments/eval에서 실행 |
| [05-pipeline-options-and-plan.md](notes/05-pipeline-options-and-plan.md) | PLANNED | 2 | 자체개선 루프를 실제로 연결하는 파이프라인 4안 비교와 실행 계획 |

### orchestration: 여러 에이전트 조율의 근거와 판단

| 문서 | 상태 | 층 | 요약 |
|---|---|---|---|
| [06-orchestrator-pattern.md](notes/06-orchestrator-pattern.md) | ACTIVE | 2 | 이 저장소 작업에서 실제로 쓴 분해, 위임, 검증 오케스트레이터 패턴과 워커 에이전트 4개 정의 |
| [07-harness-and-hook-enforcement.md](notes/07-harness-and-hook-enforcement.md) | ACTIVE | 2 | 규칙을 프롬프트가 아니라 Hook으로 강제한 사례. 생성 위키 수정 차단 Hook과 그 버그 수정 |
| [10-orchestration-evidence-2023-2025.md](notes/10-orchestration-evidence-2023-2025.md) | ACTIVE | 1 | 오케스트레이션 외부 근거 모음(Anthropic, OpenAI, MS, Google, MAST 등). 주로 2023~2025년 출처, 연도 표시 |
| [11-orchestration-current-2026.md](notes/11-orchestration-current-2026.md) | ACTIVE | 1 | 10번 결론을 2026년 모델 기준으로 재검증한 판정표와 2026년 가이드, 운영 사례. 10과 다르면 11을 따름 |
| [12-orchestration-application.md](notes/12-orchestration-application.md) | DRAFT | 2 | 10, 11번 근거를 부서별 에이전트 조직 구상에 적용한 설계 판단 |
| [16-superpowers-study.md](notes/16-superpowers-study.md) | ACTIVE | 1 | superpowers v6.3.0을 설치본 원문으로 공부한 노트. 요청 흐름, 위험 검증, 비용, 보안, 가져올 것 |
| [17-orchestration-news-2026-10.md](notes/17-orchestration-news-2026-10.md) | ACTIVE | 1 | 2026-10-01 ~ 11-02 에이전트 오케스트레이션 소식. 검증한 17개 주장 중심으로 마스터 설계에 미치는 영향과 11번 판정표 갱신 |

### master: 마스터 에이전트 (자비스형)

| 문서 | 상태 | 층 | 요약 |
|---|---|---|---|
| [15-master-orchestrator-research.md](notes/15-master-orchestrator-research.md) | ACTIVE | 1 | 마스터 에이전트(자비스형) 설계를 위한 원문 조사 3개의 목차와 세 조사가 겹치는 결론 |
| [16-superpowers-study.md](notes/16-superpowers-study.md) | ACTIVE | 1 | superpowers v6.3.0을 설치본 원문으로 공부한 노트. 요청 흐름, 위험 검증, 비용, 보안, 가져올 것 |
| [17-orchestration-news-2026-10.md](notes/17-orchestration-news-2026-10.md) | ACTIVE | 1 | 2026-10-01 ~ 11-02 에이전트 오케스트레이션 소식. 검증한 17개 주장 중심으로 마스터 설계에 미치는 영향과 11번 판정표 갱신 |

### baseline: 카카오페이 바닥선

| 문서 | 상태 | 층 | 요약 |
|---|---|---|---|
| [13-kakaopay-tech-blog-study.md](notes/13-kakaopay-tech-blog-study.md) | ACTIVE | 1 | 카카오페이 기술블로그 AI, 에이전트, 운영 자동화 글 24개 조사 목차와 공통 원칙 |
| [14-kakaopay-baseline-and-target.md](notes/14-kakaopay-baseline-and-target.md) | DRAFT | 2 | 영역 10개별로 카카오페이 바닥선과 그 이상을 정한 설계와 한 화면 흐름도 |

### repo-ops: 이 저장소 운영 (구조, 파이프라인)

| 문서 | 상태 | 층 | 요약 |
|---|---|---|---|
| [09-repo-structure-and-pipeline.md](notes/09-repo-structure-and-pipeline.md) | ACTIVE | 2 | 08 스키마를 이 저장소에 적용한 폴더 구조와 작업 파이프라인. 바꾼 이유, 선행 사례, 규칙, 이전 기록 |

## 원문 자료 (sources/)

고치지 않는 외부 자료 노트. 목차 문서는 그 폴더를 링크하는 notes 문서다.

| 폴더 | 파일 수 | 목차 문서 |
|---|---|---|
| [sources/kakaopay/](sources/kakaopay/) | 24 | [07](notes/07-harness-and-hook-enforcement.md), [13](notes/13-kakaopay-tech-blog-study.md), [14](notes/14-kakaopay-baseline-and-target.md) |
| [sources/master-orchestrator/](sources/master-orchestrator/) | 3 | [15](notes/15-master-orchestrator-research.md) |
| [sources/news-2026-10/](sources/news-2026-10/) | 6 | [17](notes/17-orchestration-news-2026-10.md) |
| [sources/superpowers/](sources/superpowers/) | 1 | [15](notes/15-master-orchestrator-research.md), [16](notes/16-superpowers-study.md) |

## 실험 (experiments/)

- [experiments/eval/](experiments/eval/): 04번 문서의 자체개선 루프 — 실행 가능한 최소 환경

## 다음에 할 일

- 열린 결정 6개: [decisions.md](decisions.md)
- 열린 질문이 남은 문서 (문서 안의 "열린 질문" 절, 숫자는 남은 항목 수):

  - [01-research-summary.md](notes/01-research-summary.md): 2개
  - [03-instruction-resolution-gate.md](notes/03-instruction-resolution-gate.md): 4개
  - [04-purpose-and-self-improvement-loop.md](notes/04-purpose-and-self-improvement-loop.md): 7개
  - [06-orchestrator-pattern.md](notes/06-orchestrator-pattern.md): 4개
  - [07-harness-and-hook-enforcement.md](notes/07-harness-and-hook-enforcement.md): 4개
  - [09-repo-structure-and-pipeline.md](notes/09-repo-structure-and-pipeline.md): 2개
  - [12-orchestration-application.md](notes/12-orchestration-application.md): 3개
  - [17-orchestration-news-2026-10.md](notes/17-orchestration-news-2026-10.md): 3개

<!-- index:end -->
