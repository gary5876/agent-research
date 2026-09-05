# 연구 요약: "에이전트 전문성은 어디서 나오는가"

**Status:** ACTIVE

[00-llm-friendly-docs-framework.md](00-llm-friendly-docs-framework.md)에서 출발해서, 실제 오픈소스 3개(Apache Amoro, Iceberg, Paimon)를 clone해서 검증한 기록이다.

## 진행 순서

1. **출발 질문**: LLM 친화적 문서를 어떻게 써야 환각을 줄이는가 (`00`)
2. **가설 제기**: "에이전트의 전문성은 그 에이전트가 쓰기 좋게 구조화된 data lake에서 나온다"
3. **1차 검증 대상**: Apache Amoro — lakehouse 관리 시스템이면서, 동시에 `amoro-mcp-server`라는 **에이전트 전용 인터페이스 모듈**을 갖고 있어서 가설을 직접 검증할 수 있는 사례였다
4. **가설 수정**: data lake 하나만으론 부족하다는 결론 도출 (아래 참고)
5. **확장 검증**: Amoro가 관리하는 3개 테이블 포맷(Iceberg/Hudi/Paimon) 중 Iceberg·Paimon을 실제로 clone해서, "테이블 포맷 자체의 설계 철학 차이"와 "각 프로젝트가 AGENTS.md를 얼마나 다르게 쓰는지"까지 비교 대상을 넓혔다

## 최종 결론 (가설 수정본)

> 에이전트의 전문성은 "잘 만들어진 data lake"가 아니라, **data lake + 좁고 명시적인 조회 인터페이스 + 안전한 응답 필터 + 실패 사례 기반 금지 규칙 문서**의 조합에서 나온다.

네 요소 각각의 근거:

| 요소 | 근거 | 상세 |
|---|---|---|
| 정합적인 data lake | Amoro의 self-optimizing, 통합 카탈로그 | [amoro-analysis/domain/self-optimizing.md](../../data-lake/amoro-analysis/domain/self-optimizing.md) |
| 좁고 명시적인 인터페이스 | Amoro MCP 서버가 11개 GET 도구만 노출, "범용 액션 실행기 없음"을 명문화 | [amoro-analysis/agent-interface/tools-and-allowlist.md](../../data-lake/amoro-analysis/agent-interface/tools-and-allowlist.md) |
| 안전한 응답 필터 | 블랙리스트(정규식)+화이트리스트(필드 allowlist) 이중 필터링 | [amoro-analysis/agent-interface/sanitization.md](../../data-lake/amoro-analysis/agent-interface/sanitization.md) |
| 실패 사례 기반 금지 규칙 문서 | Iceberg AGENTS.md가 58,000개+ PR 리뷰 코멘트에서 규칙을 역추출, `Never`/`Ask first` 구분 | [amoro-analysis/lessons/agents-md-case-study.md](../../data-lake/amoro-analysis/lessons/agents-md-case-study.md) |

네 번째 요소는 원래 가설에 없었고, Amoro/Iceberg/Paimon이 각자 가진 `AGENTS.md`의 밀도 차이를 비교하다가 추가로 발견한 것이다.

## 각 분석 디렉터리가 기여한 것

| 디렉터리 | 기여 |
|---|---|
| [../../data-lake/amoro-analysis](../../data-lake/amoro-analysis/README.md) | 핵심 사례. lakehouse 관리 구조 + 에이전트 인터페이스(MCP 서버) 심층 분석. 가설 수정의 근거 대부분이 여기서 나옴 |
| [../../data-lake/iceberg-analysis](../../data-lake/iceberg-analysis/README.md) | "스펙이 먼저, 구현은 나중"인 프로젝트의 모듈 경계 설계와, 리뷰 코멘트 기반 AGENTS.md 사례 |
| [../../data-lake/paimon-analysis](../../data-lake/paimon-analysis/README.md) | Iceberg와 근본적으로 다른 저장 구조(LSM-tree)를 가진 대조군. 얇은 AGENTS.md(빌드 명령만) 사례 |

## 검증 방식에 대한 메모

세 레포 모두 shallow clone(`--depth 1`)으로 로컬에 받아서 실제 코드/스펙 문서를 읽고 검증했다. Hudi(apache/hudi)는 packed 2.9GB로 나머지 둘의 20배 이상이라 clone하지 않았고, 관련 서술은 [amoro-analysis/domain/table-format-comparison.md](../../data-lake/amoro-analysis/domain/table-format-comparison.md)에 "미검증"으로 명시해뒀다 — 이것 자체가 `00`번 문서의 원칙 3번(현재 상태 vs 확인 안 된 상태 구분)을 이 연구 노트 안에서 그대로 지킨 사례다.

## 아직 열려 있는 질문

- `00`의 원칙 12번(검증 시스템: Task → 문서/코드 대조 → 불일치 시 보고)은 이번 분석에서 정적으로 문서를 만드는 데만 적용했고, 실제로 에이전트가 코드를 수정하는 루프에 넣어서 검증하지는 않았다. 다음 단계로 시도해볼 만하다.
- Hudi를 직접 clone해서 위 4요소 프레임을 검증하면 비교가 3자→4자로 완성된다.
