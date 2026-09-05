# 04번 문서의 자체개선 루프 — 실행 가능한 최소 환경

**Layer:** 3 (실제 구현체) — 층 구분 기준: [../../../CATALOG.md](../../../CATALOG.md)

`04-purpose-and-self-improvement-loop.md`는 지금까지 전부 설계 단계(`Status: PLANNED`)였다. 이 디렉터리는 그 설계 중 두 조각을 실제로 돌려본 결과다 — "무엇을 채점할지"가 아니라 "실제로 돌아가는가"를 확인하는 게 목적이다.

## 구성

- `grounding_metric.py` — DeepEval 커스텀 metric. §1 표의 "정합적인 data lake" 성공기준("응답의 사실 주장 각각이 특정 소스로 추적 가능한 비율")을 그대로 채점 로직으로 옮긴 것. LLM judge 호출이 없는 결정론적 metric이라 API 키가 필요 없다.
- `test_grounding.py` — 이 레포의 `openwiki/.claims/**/*.json`에 실제로 들어있는 Claim 전체(30개 evidence)를 대상으로 위 metric을 돌리는 pytest 테스트. 합성 데이터가 아니라 이 레포의 실제 산출물이 테스트 대상이다.
- `test_filter.py` — `filters.PresidioFilter`를 이번 세션 사건과 같은 모양의 **합성(가짜) 서비스 계정 JSON**에 대해 돌리는 스모크 테스트. 실제 유출된 키는 어디에도 쓰지 않는다.
- `filters/` — **레퍼런스를 갈아끼우며 테스트하는 하네스** (05-pipeline-options-and-plan.md §2). `base.py`의 `ResponseFilter` 인터페이스 하나에 백엔드를 꽂는 구조. `baseline_filter.py`(의존성 없는 regex)와 `presidio_filter.py`(Presidio, PEM/AWS키/이메일 recognizer) 두 개를 실제로 구현했고, `corpus.py`의 라벨링된 5개 케이스로 `compare_filters.py`가 recall/false-positive를 비교한다. NeMo Guardrails/PurpleLlama/Guardrails AI/Portkey-AI 게이트웨이는 GPU·API 키 등이 필요해 아직 안 꽂았다 — `ResponseFilter`만 구현하면 `compare_filters.py`의 `BACKENDS`에 추가하는 것으로 끝난다.

## 재현 방법

```bash
python3.12 -m venv agent-expertise-framework/eval/.venv   # 3.9로는 deepeval import가 실패함(union-type 문법)
source agent-expertise-framework/eval/.venv/bin/activate
pip install -r agent-expertise-framework/eval/requirements.txt
python -m spacy download en_core_web_sm  # requirements.txt의 wheel URL로 이미 설치되지만, 안 될 경우 대비

cd agent-expertise-framework/eval
pytest test_grounding.py -q      # 그라운딩 검증
python test_filter.py            # 필터 스모크 테스트 (Presidio 하나)
python compare_filters.py        # 필터 백엔드 교체 비교 (baseline vs presidio)
```

## 실행 결과 (2026-09-02)

- `test_grounding.py`: **30 passed** — 이 레포의 Claim-evidence 30개 전부 소스 라인이 지금도 존재하고 비어있지 않음. 인위적으로 존재하지 않는 라인/파일/형식 오류 케이스를 넣어보면 metric이 정확히 0.0으로 실패 처리하는 것도 별도로 확인함(문서 04 §8 참고).
- `test_filter.py`: 합성 샘플에서 `PEM_PRIVATE_KEY`(score=1.00)와 `EMAIL_ADDRESS`(score=1.00) 둘 다 탐지 성공.
- `compare_filters.py`: baseline recall=0.75(4개 중 3개, AWS 키 케이스 MISS) vs presidio recall=1.00(4/4) — 두 백엔드 모두 무해 텍스트(영문/한글)에서 false positive 0. baseline이 AWS 키를 놓치는 건 "PEM 키 사건 하나만 겪은 사람이 짤 법한" 필터의 실제 커버리지 갭을 그대로 보여준다.

## 아직 안 한 것

전체 파이프라인을 어떻게 연결할지(옵션 4가지)와 단계별 계획은 [../05-pipeline-options-and-plan.md](../05-pipeline-options-and-plan.md) 참고.

- Promptfoo(배포 전 회귀 게이트), Arize Phoenix(배포 후 모니터링), NeMo Guardrails는 설치도 실행도 안 했다.
- `grounding_metric.py`는 OpenWiki의 실제 해시 알고리즘(`repo-lines-v1:sha256:...`)을 재구현한 게 아니라, "파일/라인이 지금 존재하고 비어있지 않은가"만 본다 — OpenWiki처럼 "내용이 바뀌었는지"(해시 불일치)까지는 검증하지 않는다. 더 엄격하게 하려면 evidence의 `version` 필드(base64로 인코딩된 라인 해시 메타데이터)를 디코딩해서 재계산한 해시와 비교해야 한다.
- 04 §7 루프의 ②~⑥(배포전 게이트, 배포후 모니터링, 원인 라우팅, 재검증)은 전혀 연결 안 됐다 — 지금 있는 건 루프의 재료 중 두 조각뿐이다.
