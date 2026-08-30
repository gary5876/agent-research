# agent-expertise-framework

이 세션에서 다룬 전체 주제의 뿌리 디렉터리. "LLM 친화적 문서를 어떻게 쓰는가"라는 질문에서 시작해서 "에이전트의 전문성은 어디서 나오는가"라는 질문으로 이어진 흐름을 정리했다.

| 파일 | 내용 |
|---|---|
| [00-llm-friendly-docs-framework.md](00-llm-friendly-docs-framework.md) | 세션의 출발점. LLM용 문서 작성 12원칙 (명시성, 상태 구분, 용어집, Constraints, ADR 등) |
| [01-research-summary.md](01-research-summary.md) | 그 프레임워크를 Amoro/Iceberg/Paimon으로 검증한 결과 요약. 최종 결론과 각 분석의 기여도 정리 |
| [02-instruction-clarity-incident.md](02-instruction-clarity-incident.md) | 반대 방향 사례: LLM에게 지시할 때 생기는 오판 실사례와, 지시문을 어떻게 써야 오판을 막는지 정리 |
| [03-instruction-resolution-gate.md](03-instruction-resolution-gate.md) | 02번 사건을 재료로 설계한 요구사항 해석 게이트. 조회형/결정형 애매함을 구분하고, 왜 이 로직을 모델 판단이 아니라 구조적 게이트로 강제해야 하는지 정리 |

## 관련 분석 디렉터리 (같은 workspace, 형제 폴더)

- [../../data-lake/amoro-analysis](../../data-lake/amoro-analysis/README.md) — 핵심 사례 (lakehouse 관리 + 에이전트 인터페이스)
- [../../data-lake/iceberg-analysis](../../data-lake/iceberg-analysis/README.md) — 테이블 포맷 비교 대상 1
- [../../data-lake/paimon-analysis](../../data-lake/paimon-analysis/README.md) — 테이블 포맷 비교 대상 2

## 읽는 순서

처음이면 `00` → `01` → `01`에서 링크한 분석 디렉터리 순으로 읽으면 된다. 이미 분석 내용을 아는 상태면 `01`만 봐도 전체 결론이 요약되어 있다.
