<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behavior. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->

## 문서 정리 컨벤션

목적: 나중에 뭔가 찾을 때 제목을 하나씩 뒤지지 않고, 층(Layer)으로 바로 찾게 하는 것. `data-lake/me-data-lake`와 같은 방식 — 원본 문서는 옮기거나 병합하지 않고, 분류만 한다.

새 연구 문서를 `agent-expertise-framework/`(또는 새 하위 주제 폴더)에 추가할 때:

1. 제목 바로 아래에 `**Status:**`(DRAFT/ACTIVE/PLANNED/DEPRECATED)와 `**Layer:**`를 반드시 남긴다.
   - Layer 1 = 원본 관찰·사건·실행 기록 (재해석 없이 그대로 근거로 쓸 수 있는 것)
   - Layer 2 = Layer 1을 재료로 만든 설계·프레임워크·비교
   - Layer 3 = 설계를 실제 코드/설정으로 옮긴 구현체
   - Layer 4 = 자동 생성되거나 배포된 뷰 (openwiki/, 루트 README)
2. 문서 하나가 여러 층을 섞어 쓰면, 대표 층을 `**Layer:**`에 적고 괄호로 예외 구간(예: "§8·9는 Layer 1")을 명시한다.
3. 새 문서를 추가하거나 층이 바뀌면 [CATALOG.md](CATALOG.md)의 해당 표도 같이 갱신한다 — 인덱스(각 폴더 README.md)와 카탈로그(CATALOG.md)는 항상 동기화 상태를 유지한다.
4. **정리(로컬 수정)와 배포(git push)는 분리된 요청으로 취급한다.** "정리해서 올려"처럼 같이 지시받아도, 변경사항을 먼저 보여주고 확인받은 뒤에 push한다.
