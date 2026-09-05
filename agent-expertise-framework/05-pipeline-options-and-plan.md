# 전체 파이프라인 옵션과 실행 계획

**Status:** PLANNED
**Layer:** 2 (설계) — 층 구분 기준: [CATALOG.md](../CATALOG.md)

`04-purpose-and-self-improvement-loop.md` §7이 자체개선 루프의 단계(①~⑥)를 정의했지만, 그 단계들을 실제로 어떤 아키텍처로 연결할지는 정하지 않았다. 이 문서는 (1) 전체 파이프라인을 연결하는 4가지 방식을 검증된 도구 목록(04 ADR-2~5)을 기준으로 정리하고, (2) "레퍼런스를 갈아끼우며 테스트"할 수 있는 환경을 실제로 만들어 돌려보고, (3) 그 결과를 근거로 실행 계획을 세운다.

## 핵심 한 문장

> 4가지 파이프라인은 서로 대체재가 아니라 "몇 단계까지 자동화할 것인가"의 누적 스펙트럼이다 — A가 가장 가볍고, D로 갈수록 04 §7의 ①~⑥을 더 많이 커버하지만 운영 비용도 커진다.

## 1. 전체 파이프라인 옵션 4가지

| | 이름 | 핵심 구성 | 커버하는 §7 단계 | 강점 | 약점 |
|---|---|---|---|---|---|
| A | CI 게이트형 | DeepEval(②) + Promptfoo(③) 만, PR마다 실행 | ②③만, ④⑤⑥은 사람이 수동 | OpenWiki의 **설계상** 운영 방식(daily cron + PR)과 철학이 같아 이 레포에 바로 얹기 쉬움. 구현 최소 | 배포 후 실사용 트래픽에서 발생하는 실패를 못 잡음 — 사전에 생각 못 한 케이스는 그냥 새어나감. **주의**: `gh run list`로 확인한 결과 이 레포의 `openwiki-update.yml`은 필요한 API 키 시크릿이 하나도 설정 안 돼 있어 최근 스케줄 실행 3건이 전부 30~37초 만에 failure로 끝남 — "daily cron + PR"은 코드로는 존재하지만 지금 이 레포에서 실제로 작동하는 상태가 아니다. 이 옵션을 택해도 시크릿부터 설정해야 한다 |
| B | 게이트웨이 중앙집중형 | 모든 응답이 Portkey-AI/gateway(12.9k★) 한 지점을 통과, 내장 가드레일 50+가 필터(요소3) 담당, 게이트웨이 로그를 DeepEval이 배치 채점 | ②③(배치)④(게이트웨이 로그) | 필터를 위해 Presidio+NeMo Guardrails+PurpleLlama 여러 개를 따로 통합할 필요 없이 게이트웨이 하나로 수렴 | portkey-ai/gateway는 04 ADR-3에서 이미 "최근 커밋 3개월 전"으로 확인된 정체 신호 — 전체 파이프라인의 단일 장애점(SPOF)을 유지보수 신호가 가장 약한 도구에 맡기는 리스크 |
| C | 옵저버빌리티 우선형 | 사전 게이트 없이 전량 배포, Arize Phoenix(④)가 실시간 트레이싱, DeepEval을 온라인 채점기로 부착, 이상 시 알림→⑤⑥ | ②④⑤⑥, ③(사전 차단) 없음 | 실제 트래픽 기반이라 합성 테스트케이스가 못 잡는 케이스까지 커버 | 나쁜 응답이 최소 1번은 사용자에게 노출된 뒤에야 잡힘 — `02`/`03`이 세운 "판단을 사전에 구조적으로 막는다"는 이 프로젝트의 원래 철학과 정면으로 어긋남 |
| D | 완전 조합형 (04 §7 원안) | DeepEval(②)+Promptfoo(③)+Phoenix(④)+5분류 원인 라우팅(⑤)+재검증(⑥) 전부 | ①~⑥ 전부 | 04가 이미 설계·부분 구현(§8)한 것과 정확히 일치, 4요소 전부 커버 | 도구 4~5개 동시 운영 — A/B/C보다 구현·유지보수 비용이 가장 큼 |

이 넷은 배타적이지 않다 — A ⊂ D 방향으로 구성요소가 누적된다. 그래서 같은 채점 코어(`eval/grounding_metric.py`, `eval/filters/`)를 유지한 채로 앞뒤에 붙는 게이트/모니터링 조합만 바꿔서 비교할 수 있다.

## 2. 레퍼런스를 갈아끼우며 테스트하는 환경 (`eval/filters/`)

파이프라인 옵션 자체를 다 구현해보기 전에, 먼저 "요소3(안전한 응답 필터)의 레퍼런스 5개 중 뭘 골라도 같은 방식으로 비교할 수 있는가"를 검증했다 — 이게 파이프라인 선택(§1)의 근거가 되는 실측 데이터다.

**구조**: `filters/base.py`의 `ResponseFilter` 인터페이스(`scan(text) -> list[Detection]`) 하나에 백엔드를 꽂는 방식. `compare_filters.py`가 등록된 모든 백엔드를 같은 라벨링된 corpus(`filters/corpus.py`, 5개 케이스: PEM 키+이메일, AWS 키, 이메일만, 영문 무해 텍스트, 한글 무해 텍스트)에 대해 돌리고 recall/false-positive를 계산한다.

**실제로 꽂아본 것**: `filters/baseline_filter.py`(의존성 없는 순수 regex, PEM+이메일만 앎)와 `filters/presidio_filter.py`(Presidio, PEM+AWS키+이메일 recognizer 등록). **실행 결과**:

```
baseline (regex only, no NER)   -> recall=0.75 (3/4), false_positives=0   [AWS 키 케이스 MISS]
presidio (regex + spaCy NER)    -> recall=1.00 (4/4), false_positives=0
```

이건 조작한 결과가 아니라 실제로 재현되는 실패다 — baseline은 "PEM 키 사건 하나만 겪은 사람이 짤 법한" 필터라 AWS 키 패턴이 없어서 그 케이스를 그대로 놓친다. 두 백엔드 모두 벤치 무해 텍스트(영문/한글)에서 false positive는 0이었다.

**아직 안 꽂은 것**: NeMo Guardrails(로컬/호스팅 LLM 백엔드 필요), PurpleLlama의 Llama Guard/Prompt Guard(GPU 모델 다운로드 필요), Guardrails AI(별도 검증 스키마 작성 필요), Portkey-AI/gateway(프록시 서버+API 키 필요) — 넷 다 `ResponseFilter`를 구현하기만 하면 `compare_filters.py`의 `BACKENDS` 리스트에 한 줄 추가로 꽂힌다. 지금 이 환경에서 API 키나 GPU 없이 실행 가능한 후보 2개만 실제로 검증했다는 걸 그대로 인정한다.

## 3. 계획

### 3-1. 파이프라인 선택

**A(CI 게이트형)를 1단계로 채택**한다. 근거:
- `02`/`03`이 세운 이 프로젝트의 원칙(판단을 사전에 구조적으로 막는다)과 맞는 건 C가 아니라 A/D다.
- D는 맞지만 지금 `eval/`에 실제로 있는 건 ②(그라운딩 metric, 필터)뿐이고 ③(Promptfoo)·④(모니터링, ADR-7로 Phoenix→Langfuse 1순위 변경)·⑤(라우팅)는 전혀 연결 안 됐다 — 한 번에 D로 가는 건 검증 안 된 도구 여러 개를 동시에 붙이는 것과 같다.
- B는 SPOF가 유지보수 신호 최약체(portkey-ai/gateway)라는 게 이미 확인돼 있어 지금 단계에서 채택 리스크가 크다.
- 따라서 **A로 시작해서 D 방향으로 단계적으로 확장**한다 — B/C는 각 단계에서 "이 지점에 다른 조합을 끼울 수도 있었다"는 대안으로 남겨둔다.

### 3-2. 단계별 계획

| 단계 | 산출물 | 상태 |
|---|---|---|
| 1 | 그라운딩 metric(`grounding_metric.py`) + 필터 비교 하네스(`filters/`) | **완료** (§8, §2) |
| 2 | 04 §1 표의 나머지 성공기준(요소2 인터페이스, 요소4 Constraints)도 DeepEval 커스텀 metric으로 operationalize | 미착수 |
| 3 | 2단계 metric들을 실제 `pytest`/`deepeval test run` CI 워크플로(`.github/workflows/`)에 연결 — Promptfoo로 PR마다 회귀 게이트 | 미착수 |
| 4 | 필터 백엔드 3개(NeMo Guardrails/PurpleLlama/Guardrails AI 중 최소 1개) 실제로 꽂아서 `compare_filters.py`로 Presidio와 비교 | 미착수 |
| 5 | ⑤ 원인 라우팅(5분류 자동 배정) 로직 설계·구현 — 지금은 04 §7에 서술만 있음 | 미착수 |
| 6 | Langfuse 연결(④, ADR-7 — Phoenix 대신), 파이프라인 D로 확장 여부는 1~5단계 결과를 보고 재판단 | 미착수 |
| 7 | Giskard 자동 스캔 + Promptfoo 매트릭스 뷰 활성화(ADR-6, 엣지케이스 n차원 커버리지) | 미착수 |
| 8 | Temporal 도입(ADR-8, 지속상태+재시도/핸드오프) — LangGraph를 쓰게 되면 이 둘을 같이 채택 | 미착수 |

### 3-3. 다음 즉시 할 일

2단계(요소2·요소4 metric operationalize)부터 진행 — 1단계가 요소1(그라운딩)·요소3(필터)을 이미 다뤘으므로, 다음 차례는 나머지 두 요소를 같은 방식(결정론적 DeepEval 커스텀 metric)으로 채우는 것이다. 7·8단계(Giskard/Temporal)는 방향 결정(04 §9-4 이전에 나온, 어떤 에이전트를 만들지) 이후 실제 오케스트레이션 코드가 생겼을 때 붙는 게 자연스럽다 — 지금은 순서만 잡아두고 착수하지 않는다.

## 관련 문서

- [04-purpose-and-self-improvement-loop.md](04-purpose-and-self-improvement-loop.md) — §7 루프 정의, ADR-2~8(도구 선정 근거)
- [eval/README.md](eval/README.md), [eval/filters/](eval/filters/) — 이 문서 §2의 실행 환경
