# agent-expertise-framework

이 세션에서 다룬 전체 주제의 뿌리 디렉터리. "LLM 친화적 문서를 어떻게 쓰는가"라는 질문에서 시작해서 "에이전트의 전문성은 어디서 나오는가"라는 질문으로 이어진 흐름을 정리했다.

| 파일 | 내용 |
|---|---|
| [00-llm-friendly-docs-framework.md](00-llm-friendly-docs-framework.md) | 세션의 출발점. LLM용 문서 작성 12원칙 (명시성, 상태 구분, 용어집, Constraints, ADR 등) |
| [01-research-summary.md](01-research-summary.md) | 그 프레임워크를 Amoro/Iceberg/Paimon으로 검증한 결과 요약. 최종 결론과 각 분석의 기여도 정리 |
| [02-instruction-clarity-incident.md](02-instruction-clarity-incident.md) | 반대 방향 사례: LLM에게 지시할 때 생기는 오판 실사례와, 지시문을 어떻게 써야 오판을 막는지 정리 |
| [03-instruction-resolution-gate.md](03-instruction-resolution-gate.md) | 02번 사건을 재료로 설계한 요구사항 해석 게이트. 조회형/결정형 애매함을 구분하고, 왜 이 로직을 모델 판단이 아니라 구조적 게이트로 강제해야 하는지 정리 |
| [04-purpose-and-self-improvement-loop.md](04-purpose-and-self-improvement-loop.md) | 4요소 각각의 목적을 명시하고, 00번 12원칙 중 실제 조사로 확인된 약점(3·4·6·10·12)을 보완. 응답 품질을 평가→원인진단→개선하는 자체개선 루프 설계. [eval/](04-purpose-and-self-improvement-loop.md#8-실행-기록--7-루프-중-실제로-돌려본-조각-eval)에 그라운딩 metric·필터 recognizer를 실제로 구현해 돌린 결과 포함. §9에 실제 사례(Replit DB 삭제 등) 문제 7개를 하나씩 검증한 감사 결과와 새 요소 후보 2개 |
| [05-pipeline-options-and-plan.md](05-pipeline-options-and-plan.md) | 04 §7 루프를 실제로 연결하는 방식 4가지(CI 게이트형/게이트웨이 중앙집중형/옵저버빌리티 우선형/완전 조합형) 비교, `eval/filters/`로 만든 레퍼런스 교체 테스트 하네스와 실행 결과, 단계별 실행 계획 |
| [06-orchestrator-pattern.md](06-orchestrator-pattern.md) | "관리자 에이전트가 필요하다"는 문제의식을, 이 세션이 실제로 수행한 분해→병렬위임→감시→검증→반영 5단계로 역추출해 문서화. 검증 단계를 건너뛰어 실제로 틀렸던 사례(Nessie 1순위, 인터페이스 라이브러리 오판) 포함, 진짜 병렬 실행·재시도는 아직 검증 안 됐다는 한계도 명시. §6에 `.claude/agents/`의 실제 워커 에이전트(researcher/verifier/doc-writer/supervisor) 정의. §2-1 흐름도를 4개 에이전트+Hook 반영해 갱신(2026-09-05) — 단, 에이전트는 파일로만 존재하고 아직 dispatch된 적 없다는 것도 명시 |
| [07-harness-and-hook-enforcement.md](07-harness-and-hook-enforcement.md) | 카카오페이 기술블로그 원문을 기본틀/문제점/해결방법 세 갈래로 나눠 재조사(1차 요약이 너무 얕았음). 본문 다이어그램 2장도 WebFetch가 안 본 걸 발견해 이미지를 직접 다운로드해서 확인(§1-1a). 15개 문제 목록, 5단계 고도화 경로(`05`의 파이프라인 A→D와 대응), "Hook은 확정·프롬프트는 확률" 원칙을 실제로 적용해 `04` §5의 Never 규칙 하나를 `.claude/settings.json` `PreToolUse` hook으로 전환. `openwiki` 패키지의 공급망 신뢰성을 npm/GitHub/조직 정보까지 4단계로 실제 검증(§7-1), Hook 자체의 cwd 의존 버그를 발견해 수정(§7-2) |

## 관련 분석 디렉터리 (같은 workspace, 형제 폴더)

- [../../data-lake/amoro-analysis](../../data-lake/amoro-analysis/README.md) — 핵심 사례 (lakehouse 관리 + 에이전트 인터페이스)
- [../../data-lake/iceberg-analysis](../../data-lake/iceberg-analysis/README.md) — 테이블 포맷 비교 대상 1
- [../../data-lake/paimon-analysis](../../data-lake/paimon-analysis/README.md) — 테이블 포맷 비교 대상 2

## 읽는 순서

처음이면 `00` → `01` → `01`에서 링크한 분석 디렉터리 순으로 읽으면 된다. 이미 분석 내용을 아는 상태면 `01`만 봐도 전체 결론이 요약되어 있다.
