<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behavior. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->

## 이 저장소에서 일하는 법

처음 열 파일은 [index.md](index.md)다. 구조를 이렇게 정한 이유와 전체 규칙은 [notes/09-repo-structure-and-pipeline.md](notes/09-repo-structure-and-pipeline.md)에 있다.

**폴더**: 정리 문서는 `notes/NN-slug.md`(번호는 가장 큰 번호 + 1, 한 번 붙이면 바꾸지 않음), 외부 자료 원문 노트는 `sources/<주제>/`(쓴 뒤 고치지 않음), 실행 코드는 `experiments/<이름>/`.

**머리말**: `notes/` 문서는 YAML 머리말에 `status`, `layer`, `topic`, `date`, `summary`(선택 `layer_note`)를 단다. 이 머리말이 그 문서 분류의 유일한 원본이다. 허용 값은 `scripts/build_index.py`의 `TOPICS`와 `STATUSES`에만 있다. 새 topic이 필요하면 거기에 한 줄 추가한다.

**손으로 관리하는 목록은 둘뿐**: [decisions.md](decisions.md)(방향 결정)와 [JOURNEY.md](JOURNEY.md)(진행 기록). 그 밖의 색인은 `build_index.py`가 만든다.

**파이프라인**

1. 질문 등록: 방향 결정은 `decisions.md`에 `open` 행, 문서 안의 질문은 그 문서의 "열린 질문" 절
2. 조사: researcher 에이전트, 원문 노트는 `sources/`
3. 검증: 문서에 넣을 주장은 verifier로 재확인
4. 정리: `notes/NN-slug.md`에 머리말과 함께
5. 마감: `decisions.md` 상태 갱신, 큰 단계가 끝나면 JOURNEY에 덧붙임
6. 색인과 검사: `python3 scripts/build_index.py` 다음 `python3 scripts/check.py`
7. 커밋: 로컬 커밋. 커밋 직전 Hook이 `check.py`를 돌린다
8. 위키: 필요할 때 로컬 Claude 세션에서 OpenWiki 스킬로 재생성. CI 예약 실행과 API 키는 쓰지 않는다
9. 배포: **정리(로컬 수정)와 배포(git push)는 분리된 요청으로 취급한다.** 같이 지시받아도 변경사항을 먼저 보여주고 확인받은 뒤에 push한다.
