# 카탈로그: 이 저장소의 문서를 층(Layer)별로 분류

`data-lake/me-data-lake/01-catalog.md`와 같은 방식이다. 문서를 옮기거나 고치지 않고, "이 파일이 원본 관찰인지 / 그걸 재료로 만든 설계인지 / 실제로 돌아가는 구현체인지 / 자동 생성된 배포 뷰인지"만 분류한다. 뭔가 찾을 때 제목으로 뒤지지 말고, 먼저 아래 표에서 층을 확인하고 그 층 안에서 스캔할 것.

## Layer 1 — 원본 관찰 / 사건 / 실행 기록

한 번 일어난 일, 실제로 돌려본 결과. 여기 있는 내용은 재해석 없이 그대로 근거로 쓸 수 있다.

| 파일(구간) | 성격 |
|---|---|
| [agent-expertise-framework/02-instruction-clarity-incident.md](agent-expertise-framework/02-instruction-clarity-incident.md) | 지시 대상을 오판한 실제 사건 전문 |
| [agent-expertise-framework/04-purpose-and-self-improvement-loop.md](agent-expertise-framework/04-purpose-and-self-improvement-loop.md) §8 | `eval/`을 실제로 돌린 실행 기록 (그라운딩 metric, 필터 recognizer 결과) |
| [agent-expertise-framework/04-purpose-and-self-improvement-loop.md](agent-expertise-framework/04-purpose-and-self-improvement-loop.md) §9 | 실사례(Replit DB 삭제 등) 문제 7개를 하나씩 검증한 감사 결과 |
| [agent-expertise-framework/06-orchestrator-pattern.md](agent-expertise-framework/06-orchestrator-pattern.md) 내 실패 사례 구간 | 검증 단계를 건너뛰어 실제로 틀렸던 사례(Nessie 1순위, 인터페이스 라이브러리 오판) |
| [agent-expertise-framework/07-harness-and-hook-enforcement.md](agent-expertise-framework/07-harness-and-hook-enforcement.md) §1, §7-2 | 카카오페이 원문 재조사(이미지 포함) + Hook 자체의 cwd 의존 버그 발견 기록 |

## Layer 2 — 설계 / 프레임워크 (Layer 1을 재료로 만든 결론)

| 파일 | 원본(Layer 1) | 스키마 |
|---|---|---|
| [agent-expertise-framework/00-llm-friendly-docs-framework.md](agent-expertise-framework/00-llm-friendly-docs-framework.md) | (세션 출발점 원칙 — 이후 검증됨) | 12원칙 |
| [agent-expertise-framework/01-research-summary.md](agent-expertise-framework/01-research-summary.md) | `data-lake/amoro-analysis`, `iceberg-analysis`, `paimon-analysis` | 3개 OSS 검증 결과 요약 |
| [agent-expertise-framework/03-instruction-resolution-gate.md](agent-expertise-framework/03-instruction-resolution-gate.md) | `02-instruction-clarity-incident.md` | 조회형/결정형 구분 게이트 설계 |
| [agent-expertise-framework/04-purpose-and-self-improvement-loop.md](agent-expertise-framework/04-purpose-and-self-improvement-loop.md) (§1~7, §8·9 제외) | 00번 12원칙 감사 결과 | 평가→원인진단→개선 루프 설계 |
| [agent-expertise-framework/05-pipeline-options-and-plan.md](agent-expertise-framework/05-pipeline-options-and-plan.md) | `04`§7 루프 | 파이프라인 4안 비교 + 실행 계획 |
| [agent-expertise-framework/06-orchestrator-pattern.md](agent-expertise-framework/06-orchestrator-pattern.md) (패턴 서술 구간) | 이 세션 자신의 분해→위임→검증 과정 | 5단계 오케스트레이터 패턴 |

## Layer 3 — 실제 구현체 (설계를 코드/설정으로 옮긴 것)

| 파일 | 대응 설계(Layer 2) | 상태 |
|---|---|---|
| [agent-expertise-framework/eval/](agent-expertise-framework/eval/) | `04`§7 | 그라운딩 metric·필터 harness. 실행 결과는 `04`§8에 기록됨(Layer 1) |
| [.claude/agents/](../agent-research/.claude/agents/) (researcher/verifier/doc-writer/supervisor) | `06-orchestrator-pattern.md` §6 | **파일로만 존재, 아직 실제 dispatch된 적 없음** — 06 문서가 스스로 명시한 한계 |
| [.claude/hooks/block-openwiki-generated-edits.py](.claude/hooks/block-openwiki-generated-edits.py) + `.claude/settings.json` | `04`§5 Never 규칙 → `07`이 실제 Hook으로 전환 | 적용됨. cwd 버그는 `07`§7-2에서 발견·수정 완료 |

## Layer 4 — 자동 생성 / 배포된 뷰

| 파일 | 성격 |
|---|---|
| [openwiki/](openwiki/) | OpenWiki가 Layer 1·2 문서에서 자동 생성한 근거 인덱스. 손으로 수정 금지(Hook으로 강제됨) |
| [README.md](README.md) | 사람이 이 저장소에 처음 들어왔을 때 보는 진입점 |

## 사용 규칙

1. **Layer 2의 결론을 인용하기 전엔 그 근거가 된 Layer 1을 먼저 확인한다.** 설계 문서는 이미 결론만 정리된 상태라 원 사건의 디테일(왜 틀렸는지, 어떤 조건에서 재현됐는지)이 빠져 있을 수 있다.
2. **Layer 3가 존재한다고 해서 Layer 2 설계가 실제로 검증됐다는 뜻은 아니다.** `.claude/agents/`처럼 "파일은 있지만 아직 실행된 적 없는" 구현체는 상태를 표에 그대로 남긴다.
3. **Layer 4(openwiki/)는 재생성 대상이다.** 내용을 바꾸고 싶으면 Layer 1·2 원본 문서를 고치고 OpenWiki가 다시 만들게 한다.
