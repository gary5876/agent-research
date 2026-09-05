# agent-research

에이전트 전문성은 어디서 나오는가에 대한 연구 노트. "LLM이 읽기 좋은 문서를 어떻게 쓸까"에서 시작해서, 지시문 해석 오류 사례, 자기개선 루프, 오케스트레이터 패턴, Hook을 통한 강제까지 이어지는 기록이다.

## 뭔가 찾고 있다면

제목으로 뒤지지 말고 [CATALOG.md](CATALOG.md)부터 열 것. "이게 원본 사건인지, 그걸로 만든 설계인지, 실제 구현체인지, 자동 생성된 뷰인지"로 층을 나눠뒀다 (`data-lake/me-data-lake`와 같은 방식).

## 시작점

순서대로 처음부터 읽고 싶으면 [agent-expertise-framework/README.md](agent-expertise-framework/README.md)가 전체 문서 인덱스다. 순서대로 읽으면 아래 흐름을 따라가게 된다.

1. LLM 친화적 문서 작성 원칙 수립 (`00`)
2. 그 원칙을 Apache Amoro/Iceberg/Paimon 세 오픈소스로 검증 (`01`)
3. 반대 방향 — 사용자가 LLM에게 지시할 때 생기는 오판 사례 (`02`)
4. 그 사건을 재료로 만든 요구사항 해석 게이트 설계 (`03`)
5. 자체개선 루프 설계 + 실제 구현한 그라운딩 metric/필터 (`04`, `agent-expertise-framework/eval/`)
6. 루프를 실제로 연결하는 파이프라인 옵션 비교 (`05`)
7. 오케스트레이터 패턴 — 이 프로젝트 자신이 수행한 분해→위임→검증 과정을 역추출 (`06`, `.claude/agents/`)
8. 프롬프트만으로는 안 지켜지는 규칙을 Hook으로 강제한 사례 (`07`, `.claude/hooks/`)

## 이 저장소 자체가 실험 대상

`.claude/agents/`의 4개 서브에이전트(researcher/verifier/doc-writer/supervisor)와 `.claude/hooks/`의 PreToolUse Hook은 위 문서들이 설계한 내용을 실제로 이 저장소에 적용한 결과물이다. 즉 연구 결과를 논문처럼 정리만 한 게 아니라, 이 저장소의 워크플로 자체에 반영해뒀다.

## openwiki/

`openwiki/`는 OpenWiki가 위 문서들로부터 자동 생성한 근거 기반 위키다. 손으로 직접 수정하지 않고, 원본 문서(`agent-expertise-framework/`)를 고치면 재생성되는 방식으로 관리한다.
