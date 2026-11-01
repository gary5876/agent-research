# 카카오페이 기술블로그 조사

**Status:** ACTIVE
**Layer:** 1 (외부 출처 조사 기록, 글별 노트는 posts/). 층 구분 기준: [CATALOG.md](../../CATALOG.md)
**조사일:** 2026-09-27
**성격:** 조사 기록. 이 시스템은 카카오페이 기술블로그 수준을 최소 기준(바닥선)으로 삼고 근거가 있으면 그 이상으로 간다(사용자 결정, 2026-09-27). 바닥선과 목표는 [14-kakaopay-baseline-and-target.md](14-kakaopay-baseline-and-target.md). 글별 노트는 `posts/`에, 이 문서는 목차와 글들을 가로지르는 공통 원칙이다.

## 조사 방법

- 블로그 전체 글 164개 목록을 수집했다(`posts/.all-posts-2026-09-27.tsv`). 그중 AI, LLM, 에이전트, 운영 자동화 관련 24개를 읽었다.
- WebFetch 요약을 쓰지 않았다. 원문 HTML을 받아 본문 전체를 직접 텍스트로 뽑아 읽었고, 본문 그림도 내려받아 직접 봤다. 이전에 WebFetch 요약으로 1편을 읽었을 때 디테일과 다이어그램이 빠지고 없는 내용이 끼어든 일이 있었기 때문이다(아래 "agent-research 07번 문서의 오류" 참고).
- 노트마다 같은 틀을 쓴다: 핵심 한 문장, 배경, 구조, 절차와 규칙, 수치, 실패와 한계, 그림 설명, 원문 인용, 우리 설계에 쓸 만한 점. 마지막 항목은 전부 `[추론]`이다.
- 원문 인용에 가운뎃점이나 대시가 있었던 경우: 해커톤 노트는 해당 인용을 빼고 원문을 바꾸지 않았다. `posts/kakaopayins-slow-pr-fast-dev.md`는 인용 속 대시를 콜론으로 바꿨다. 그 노트의 인용은 원문과 문장부호가 다를 수 있다.
- 2026-09-27 기준 `ai-agent-2`는 없다(404, 목록 검색에도 없음).

## 글 목록

### 1. 에이전트와 하네스 (핵심)
| 파일 | 게시일 | 소속 | 한 줄 |
|---|---|---|---|
| [ai-agent-1.md](posts/ai-agent-1.md) | 2026-09-01 | 카카오페이 FE | Agent는 몸, LLM은 머리. 능력을 넓히는 쪽(Tool, MCP, Skill, Plugin)과 실행을 통제하는 쪽(오케스트레이션, Supervisor, Hook, Harness)을 구분 |
| [kakaopayins-slow-pr-fast-dev.md](posts/kakaopayins-slow-pr-fast-dev.md) | 2026-06-12 | 손해보험 | 설계문서, 태스크 분해, 1 태스크 = 1 PR, PR 템플릿을 결정 기록으로. AI 리뷰어 조르깃은 approve 불가 |
| [ifkakao-agentic-coding.md](posts/ifkakao-agentic-coding.md) | 2026-03-13 | AI Platform팀 | spec-kit으로 constitution, specify, clarify, plan, tasks, analyze, implement. 산출물이 틀리면 직접 고치지 말고 specify로 돌아감 |
| [2026-kakaopay-developer-festival.md](posts/2026-kakaopay-developer-festival.md) | 2026-03-24 | 카카오페이 | 사내 행사 스케치. Claude Code 세션 요지, AX 방향 |

### 2. LLM 서비스와 플랫폼
| 파일 | 게시일 | 소속 | 한 줄 |
|---|---|---|---|
| [choonsiri.md](posts/choonsiri.md) | 2025-01-24 | 증권 DevOps | 사내 지식 봇. 위키가 원본, 답변에 출처와 수정일, 가드레일 필수, 팀장 버튼으로 게시 |
| [kakaopay-mcp-agent-toolkit.md](posts/kakaopay-mcp-agent-toolkit.md) | 2025-08-06 | 결제기술 | 결제 API를 MCP 도구 8개로. 허용 목록으로 노출 제한, LLM이 뽑으면 안 되는 값은 코드가 주입 |
| [ifkakao2024-document-ai.md](posts/ifkakao2024-document-ai.md) | 2024-12-19 | 손해보험 | 영수증 파이프라인. 신뢰도 임계값, 구조화 JSON |
| [how-llm-works.md](posts/how-llm-works.md) | 2025-09-11 | 정산플랫폼 | LLM 동작 원리와 프롬프트 팁 6개 |
| [ai-platform.md](posts/ai-platform.md) | 2025-11-12 | DevOps | GPU, Kubeflow 플랫폼 |

### 3. 해커톤 AI 프로젝트 (2025)
| 파일 | 게시일 | 멀티에이전트 여부 | 한 줄 |
|---|---|---|---|
| [kakaopay-hackathon-paygenie.md](posts/kakaopay-hackathon-paygenie.md) | 2025-08-13 | **예** (Supervisor 1 + Worker 2) | 부서마다 Worker를 붙이려는 설계. 저자 스스로 응답이 느려지고 불안정했다고 기록 |
| [building-ai-loan-coaching-service.md](posts/building-ai-loan-coaching-service.md) | 2025-08-12 | 부분 | 코드가 상담 단계(status)에 따라 에이전트를 고름 |
| [loan-voice-ai-chatbot.md](posts/loan-voice-ai-chatbot.md) | 2025-05-16 | **아니오 (의도적)** | 흐름이 선형이고 페르소나가 하나라서 단일 에이전트. 역할이 커지거나 다른 서비스와 연결될 때만 전환 |
| [kakaopay-hackathon-aiva.md](posts/kakaopay-hackathon-aiva.md) | 2025-06-19 | 아니오 (기능별 분리, 협업 없음) | 평가 기준 하나당 호출 하나. 최종 판단은 사람 |
| [kakaopay-hackathon-ai-finance-glossary.md](posts/kakaopay-hackathon-ai-finance-glossary.md) | 2025-06-24 | 아니오 (기능별 분리) | 지시가 복잡할수록 성능 저하, 용어 하나당 호출 하나로 쪼갬. 캐시로 30초에서 0.5초 |
| [transaction-summary-and-search-with-ai.md](posts/transaction-summary-and-search-with-ai.md) | 2025-05-15 | 아니오 | 의도 분류, 개체 추출, SQL 생성, SQL 검증을 단계별 호출로 |
| [kakaopay-dr-04.md](posts/kakaopay-dr-04.md) | 2025-04-24 | 해당 없음 | 행사 현장 기록 |

### 4. 운영 자동화
| 파일 | 게시일 | 소속 | 한 줄 |
|---|---|---|---|
| [slack-bot-improving-operational-efficiency.md](posts/slack-bot-improving-operational-efficiency.md) | 2023-06-09 | SRE | 배포 봇. 상태 변경은 요청서에서만, 공유는 자동. 승인과 배포는 사람 |
| [slack-bot-improving-operational-efficiency-2.md](posts/slack-bot-improving-operational-efficiency-2.md) | 2024-07-17 | SRE | 1년 회고. 상시 배포 인원 10명에서 3명, 개선 전 데이터 미수집 반성 |
| [ifkakao2024-dr-pym-project.md](posts/ifkakao2024-dr-pym-project.md) | 2024-12-05 | 증권 | 리소스 추천까지 자동, 적용은 담당자 선택과 승인. CPU 54% 절감. 자동화끼리 충돌한 사례 |
| [ifkakao2024-fds.md](posts/ifkakao2024-fds.md) | 2024-12-26 | 카카오페이 | 재학습과 운영 모델 비교 자동, 배포 버전은 분석가 선택 |
| [slack-angmondbot.md](posts/slack-angmondbot.md), [slack-angmondbot-2.md](posts/slack-angmondbot-2.md) | 2024-08 | 사내 사이드 | 크론 중복 실행을 상태 테이블과 락으로 막음, 수동 킬 스위치 |
| [aws-reinvent-2024-ai-part-1.md](posts/aws-reinvent-2024-ai-part-1.md), [part-2](posts/aws-reinvent-2024-ai-part-2.md) | 2025-02-18 | 머니코어 | **카카오페이 자체 사례 아님**, AWS 세션 요약. Crypto.com 3모델 다수결, MUFG 사람 판단 루프 |

## 글들을 가로지르는 공통 원칙

아래는 여러 글에서 반복되는 것만 모았다. 괄호 안이 근거 노트다.

1. **실수는 프롬프트가 아니라 구조로 막는다.** "대문자로 써두는 건 확률이지만, 어기면 빌드가 깨지는 건 보장" (ai-agent-1). 상태 변경을 요청서 한 곳에만 두어 공유 누락을 구조적으로 없앤 배포 봇(slack-bot-1), 틀린 산출물을 직접 고치지 않고 명세로 되돌아가는 SDD(agentic-coding)가 같은 원칙이다.
2. **추천과 초안까지는 AI, 승인과 실행은 사람.** 조르깃은 approve 불가(slow-pr), Dr.Pym은 추천까지 자동이고 적용은 담당자가 선택(dr-pym), 배포 봇은 승인과 배포를 사람이(slack-bot-1), 춘시리 주간보고는 팀장 버튼(choonsiri), AIVA는 최종 판단을 사람이(aiva), FDS는 배포 버전을 분석가가(fds). 예외 없이 반복된다.
3. **멀티에이전트는 조건이 맞을 때만.** 실제로 Supervisor형 멀티에이전트를 만든 건 페이지니 하나였고 느리고 불안정했다고 적었다. 대출 음성 챗봇은 흐름이 선형이라 일부러 단일 에이전트를 택했다. 나머지는 기능별로 따로 두거나 코드가 단계에 따라 고르는 방식이었다.
4. **한 번에 하나씩, 작게 쪼갠다.** 1 태스크 = 1 PR(slow-pr), 평가 기준 하나당 호출 하나(aiva), 용어 하나당 호출 하나(glossary), 의도 분류, 추출, 생성, 검증을 각각 호출(transaction-search), 작게라도 빨리 릴리스(angmond).
5. **흐름은 코드가 쥔다.** 대출 코치는 LLM Supervisor 대신 코드가 status로 에이전트를 고르고, 거래내역 검색은 Bedrock Agent를 버리고 서버가 도구 실행을 직접 쥐었다. spec-kit도 정해진 단계 순서를 따른다.
6. **원본은 한 곳, 답에는 출처를 붙인다.** 위키가 원본이고 잘못된 답은 위키부터 고치며, 답변에 참고 문서와 수정일을 붙인다(choonsiri). PR 템플릿이 결정 기록이 된다(slow-pr).
7. **도구와 권한은 좁게.** 필요한 도구만 켠다(ai-agent-1), 허용 목록으로 노출을 제한하고 LLM이 뽑으면 안 되는 값은 코드가 주입한다(mcp-toolkit), 모든 호출은 보안팀이 관리하는 가드레일을 거친다(choonsiri).
8. **검증은 외부 신호로.** 루프 종료 기준은 외부 검증 통과가 가장 믿을 만하다(ai-agent-1). SQL을 별도 호출로 검증(transaction-search), analyze 단계에서 CRITICAL 0이어야 구현 허용(agentic-coding), 코드 실행 결과로 판단(aiva).
9. **개선 전후를 측정한다.** 개선 전 데이터를 안 모아 효과를 증명하지 못했다는 반성(slack-bot-2). 반대로 해커톤 글들에는 정확도나 환각률 같은 정량 평가가 없다.

## 카카오페이 글 안의 긴장 (결정할 때 볼 것)

- **1편의 페르소나 분할 vs 실제 사례와 외부 연구.** 1편은 멀티에이전트 예시로 "같은 모델에 서로 다른 지시"를 줘서 "깐깐한 아키텍트", "손 빠른 주니어", "악독한 QA"로 나누는 방식을 든다. 이건 개념 설명이고 실측은 없다. 반면 카카오페이 실사례는 대부분 단일 에이전트이거나 기능별 분리였다. 외부 연구에서는 페르소나가 정확도를 올리지 않았고(`../03-orchestration-and-enforcement/11-orchestration-current-2026.md` §5-3), Anthropic 2026 글은 일의 종류로 나누는 걸 문제로 지목했다(11 §2-1).
- **1편의 Supervisor(가벼운 모델로 진행 상태 감시) vs Project Vend 같은 사례.** 1편의 Supervisor는 옳고 그름이 아니라 진행 상태만 본다고 역할을 좁혀 둬서, 같은 모델 상사가 부하의 판단을 승인해 주는 문제(11 §3-1, 10 B-6)와는 다른 역할이다. 이 좁힌 정의를 지키는 게 중요하다.

## agent-research 07번 문서의 오류 (원문 대조 결과)

`fundamentals/agent-research/agent-expertise-framework/03-orchestration-and-enforcement/07-harness-and-hook-enforcement.md`가 1편을 WebFetch 요약으로 옮기면서 생긴 오류다. 메인 세션이 원문 HTML에서 직접 확인한 것에 `[재확인]`을 붙였다.

1. 제목이 틀렸다. 07은 "AI Agent 아키텍처와 구성요소", 실제는 "AI Agent, 넌 누구냐 1 - Tool, MCP, Skill, Harness는 무엇인가" `[재확인]`. 저자(marsh.mallow)도 빠졌다.
2. 07 §3의 "5단계 고도화 경로"는 원문에 없다 `[재확인: "5단계" 문자열 없음]`. 원문의 순서 권고는 "마켓플레이스에서 플러그인 하나 설치해 Tool부터 붙여보세요" 하나다.
3. 07이 인용 부호로 쓴 "Hook 실행은 보장되고 프롬프트는 확률"은 원문 문장이 아니다. 실제 문장은 "“반드시 XYZ 해라”라고 대문자로 써두는 건 확률이지만, 어기면 빌드가 깨지는 건 보장입니다" `[재확인]`.
4. "한국어는 3배 이상 토큰"은 과장이다. 원문은 한 예시에 "3 토큰 이상"이라 쓰고 "정확한 수치는 아니고 참고용 예시", 결론은 "몇 배" `[재확인]`. 07 §4의 "최대 45배"는 이 과장 위에 세운 추정이다.
5. "샌드박싱"은 원문에 없다 `[재확인]`. 원문은 "권한을 좁혀 두지 않으면". "15개 문제"는 중복을 포함해 부풀린 개수다.
6. MCP의 "범용 어댑터 규격" 비유는 원문에 없다 `[재확인: "어댑터" 없음]`. 원문 비교표에는 MCP 행이 없다.
7. 그림 1 설명의 "셀 실행"은 "셸 실행"의 오기이고, LLM 상자("판단만 하는 함수: 상태 없음, 루프 없음, 손발 없음")와 화살표가 빠졌다.
8. 통째로 빠진 내용: 멀티에이전트 페르소나 예시와 Main Agent의 작업 큐, 공통 State, Supervisor의 Nudge와 Escalate, Hook 예시, 하네스 표의 예시 열, "일을 어떻게 나눌지가 오케스트레이션이고, 나뉜 일이 무엇을 통과해야 하는지가 하네스", "실패를 자산으로 바꾸는 장치", 과금 세부.

같은 잘못된 인용이 `fundamentals/site/githubio/portfolio/_posts/2026-09-05-hooks-are-deterministic-until-they-break.md` 12행에도 카카오페이 원칙으로 인용되어 있다. 공개된 포트폴리오 글이므로 수정 여부는 사용자가 결정한다.
