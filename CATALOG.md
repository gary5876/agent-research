# 카탈로그: 이 저장소에서 뭘 봐야 하는지

마크다운 연구 문서의 분류(Layer/Status)는 **각 문서 자신의 헤더 태그가 유일한 원본**이다 — 이 파일이 그 분류를 다시 옮겨 적지는 않는다(왜 그렇게 하기로 했는지는 [08-agent-implementation-schema.md](agent-expertise-framework/08-agent-implementation-schema.md) §1의 실패 기록 참고). 이 파일이 실제로 하는 일은 두 가지뿐이다: 마크다운 문서는 어떻게 확인하는지 안내하고, 헤더 태그를 가질 수 없는 나머지 자원(코드/설정/생성물)을 목록으로 남긴다.

## 마크다운 연구 문서 (`agent-expertise-framework/*.md` 08번, `agent-expertise-framework/*/*.md` 나머지)

```
grep -n "Status:\|Layer:" agent-expertise-framework/*.md agent-expertise-framework/*/*.md
```

한 줄로 8개 문서 전부의 상태·층을 바로 확인한다. 전체 흐름과 각 문서가 뭘 다루는지는 [agent-expertise-framework/README.md](agent-expertise-framework/README.md) 색인 참고.

## 헤더 태그를 가질 수 없는 자원

| 자원 | 성격 | 상태 |
|---|---|---|
| [agent-expertise-framework/02-self-improvement-loop/eval/](agent-expertise-framework/02-self-improvement-loop/eval/) | `04`§7 설계를 실제로 돌려본 그라운딩 metric·필터 harness | 실행 결과는 `04`§8에 기록 |
| [.claude/agents/](.claude/agents/) (researcher/verifier/doc-writer/supervisor) | `06`§6에서 정의한 오케스트레이터 워커 에이전트 | 정의만 있고, 이 넷 자체가 명시적으로 dispatch된 적은 없음(단 그 역할은 비평 에이전트 dispatch로 실제 수행된 적 있음, `08`§3 참고) |
| [.claude/hooks/block-openwiki-generated-edits.py](.claude/hooks/block-openwiki-generated-edits.py) + `.claude/settings.json` | `04`§5 Never 규칙을 `07`이 실제 Hook으로 전환한 것 | 적용됨. cwd 버그는 `07`§7-2에서 발견·수정 완료 |
| [openwiki/](openwiki/) | OpenWiki가 연구 문서에서 자동 생성한 근거 인덱스 | 손으로 수정 금지(Hook으로 강제) — 재생성 대상 |
| [README.md](README.md) | 사람이 이 저장소에 처음 들어왔을 때 보는 진입점 | — |

## 사용 규칙

1. **파생물(설계·요약)을 인용하기 전엔 그 근거가 된 원본(사건·실행 기록)을 먼저 확인한다.** 설계 문서는 이미 결론만 정리된 상태라 원 사건의 디테일이 빠져 있을 수 있다.
2. **구현체가 존재한다고 해서 그 설계가 실제로 검증됐다는 뜻은 아니다.** `.claude/agents/`처럼 "정의는 있지만 그 자체로는 실행된 적 없는" 경우 상태를 표에 그대로 남긴다.
3. **`openwiki/`는 재생성 대상이다.** 내용을 바꾸고 싶으면 `agent-expertise-framework/` 원본을 고치고 OpenWiki가 다시 만들게 한다.
