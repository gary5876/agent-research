<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behavior. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->

## 문서 정리 컨벤션

새 연구 문서를 `agent-expertise-framework/`(또는 새 하위 주제 폴더)에 추가할 때:

1. 제목 바로 아래에 `**Status:**`(DRAFT/ACTIVE/PLANNED/DEPRECATED)와 `**Layer:**`(1=원본 관찰·사건·실행기록, 2=그걸 재료로 만든 설계, 3=구현체, 4=자동생성·배포 뷰)를 남긴다. 여러 층이 섞이면 대표 층 + 괄호로 예외 구간을 설명한다. 이 태그가 그 문서의 분류에 대한 **유일한 원본**이다 — 다른 파일에 다시 옮겨 적지 않는다. 확인은 `grep -n "Layer:" agent-expertise-framework/*.md agent-expertise-framework/*/*.md`.
2. 해당 폴더 `README.md` 색인에 "언제 이 문서를 찾을지" 한 줄을 추가하고, 관련 기존 문서와 상호링크한다.
3. **정리(로컬 수정)와 배포(git push)는 분리된 요청으로 취급한다.** 같이 지시받아도 변경사항을 먼저 보여주고 확인받은 뒤에 push한다.

이 세 줄로 될 만큼 좁게 유지하는 이유, 그리고 에이전트 자체를 어떻게 구현할지의 일반형은 [agent-expertise-framework/08-agent-implementation-schema.md](agent-expertise-framework/08-agent-implementation-schema.md)에 있다. 이 스키마를 이 저장소에 완전히 채워 넣는 작업(예: 문서 접근용 Skill)은 아직 없다 — 미리 만들지 않는다, 필요해지면 그때 08을 기준으로 설계한다.
