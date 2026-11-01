# JARVIS 이름을 쓴 마스터/컨트롤러 에이전트 조사

조사일: 2026-09-28

## 조사 방법과 한계

- 목적: 부서별 에이전트(마케팅, 개발, 운영) 위에 두는 마스터 오케스트레이터를 흔히 "자비스"라고 부르는데, 실제로 JARVIS라는 이름을 쓰거나 자비스를 표방한 시스템이 마스터 역할을 어떻게 설계했는지 확인한다.
- 방법: arXiv 논문 원문(abs 페이지와 HTML/PDF 본문), GitHub 공식 저장소 README, `gh search repos` 여러 검색어, `gh api`로 저장소 메타데이터(별 수, 마지막 push, 보관 여부, 라이선스, 생성일) 확인, 벤더 문서와 실무자 글은 WebSearch/WebFetch.
- 한계: 키워드 검색으로 찾은 것만 다룬다. "Jarvis"라는 이름의 저장소는 수천 개라서 전수 확인이 아니다. 별 수는 조사 시점 값이며 조작 여부는 직접 판별할 수 없어 정황만 적는다. 본문에서 읽지 않은 숫자는 쓰지 않았고, 추론은 "(추론)"으로 표시했다.
- 증거 등급 표기: 논문 / 공식 저장소 / 벤더 / 독립 실무자 / 포럼.

## 1. Microsoft JARVIS / HuggingGPT

- 논문: https://arxiv.org/abs/2303.17580 (v1 2023-03-30, 최신 v4 2023-12-03 확인). 저자 Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, Yueting Zhuang (저장대학교, Microsoft Research Asia). 증거 등급: 논문.
- 저장소: https://github.com/microsoft/JARVIS. 증거 등급: 공식 저장소. `gh api` 확인값(2026-09-28): 별 25,349, 마지막 push 2025-07-29, 보관 안 됨, 라이선스 MIT, 생성 2023-03-30. README 공지의 마지막 항목은 2024-01-15 EasyTool 공개이고, 2023-07-28 공지에 "새 버전 Jarvis를 곧 공개"라고 적혀 있으나 README 안에서 그 후속 공개는 찾지 못했다. 사실상 연구 코드 보관소로 보는 게 맞다(추론).
- arXiv abs 페이지 comments 칸에서 학회 게재 정보는 확인하지 못했다(학회 게재 여부는 이 조사에서 검증 안 함).

### 마스터(컨트롤러) 설계

README 원문: "an LLM as the controller and numerous expert models as collaborative executors (from HuggingFace Hub)". 즉 마스터는 LLM 하나, 부서 역할은 Hugging Face의 전문 모델들이다. 4단계는 다음과 같다.

1. Task Planning: 사용자 요청을 작업 목록으로 분해하고 실행 순서와 자원 의존성을 정한다.
2. Model Selection: Hugging Face 모델 설명을 보고 각 작업에 모델을 배정한다.
3. Task Execution: 선택된 모델을 호출해 결과를 LLM에 돌려준다.
4. Response Generation: 앞 세 단계의 정보를 요약해 사용자에게 답한다.

위임 형식(논문 3.1, 부록 A.1.1에서 직접 읽음):
- 작업 파싱 템플릿은 네 개 슬롯 `"task"`, `"id"`, `"dep"`, `"args"`로 구성되며 각각 작업 이름, 고유 식별자, 의존성, 인자다. args 안에 text, image, audio, video 하위 필드가 있다.
- 의존 작업의 출력은 `<resource>-task_id` 기호로 참조하고, 실행 단계에서 실제 산출물로 치환한다. 의존성 없는 작업은 "directly in parallel"로 실행한다.
- 의존성이 없으면 `"dep": [-1]`. 사용자 입력을 파싱할 수 없으면 빈 JSON을 내도록 지시한다.
- 과거 대화를 {{ Chat Logs }}로 프롬프트에 넣어 사용자가 앞서 말한 자원을 추적한다(논문이 기술한 범위에서 상태와 기억은 이 채팅 로그가 전부이고, 별도 장기 기억 설계는 논문에서 찾지 못했다).
- 데모(few-shot 예시)를 프롬프트에 넣어 작업 분해 방식을 가르친다("Demonstration-based Parsing").

모델 선택(논문 3.2):
- 작업-모델 배정을 "single-choice problem"으로 정식화한다.
- 컨텍스트 길이 한계 때문에 먼저 작업 유형으로 후보 모델을 거르고, Hugging Face 다운로드 수로 정렬해 상위 K개만 후보로 프롬프트에 넣는다. 각주: 다운로드 수가 인기와 품질을 어느 정도 반영한다고 본다.
- 모델 선택 프롬프트는 출력을 `{"id": ..., "reason": ...}` 형식의 엄격한 JSON으로 요구한다. 즉 위임 결정마다 사유를 남긴다.

응답 생성(논문 3.4): 계획된 작업 목록, 선택된 모델, 추론 결과를 요약해 넣고, 먼저 요청에 바로 답한 다음 과정과 모델 추론 결과를 설명하게 한다.

README에 따르면 서버 모드에서 `/tasks`(1단계 중간 결과)와 `/results`(1~3단계 결과) API를 따로 열어 두어 계획만 따로 확인할 수 있다.

### 측정 결과 (논문 표에서 직접 읽음)

작업 계획 평가(GPT-4가 만든 의사 정답 기준):
- 단일 작업(Table 3): GPT-3.5 Acc 52.62, Pre 62.12, Recall 52.62, F1 54.45. Vicuna-7b F1 29.44, Alpaca-7b F1 4.88.
- 순차 작업(Table 4): GPT-3.5 ED 0.54, Pre 61.09, Recall 45.15, F1 51.92.
- 그래프 작업(Table 5): GPT-3.5 GPT-4 Score 50.48, Pre 54.90, Recall 49.23, F1 51.91.
- 사람이 라벨링한 복잡 요청 46개(Table 6): 순차 작업 Acc GPT-3.5 18.18, GPT-4 41.36. 그래프 작업 Acc GPT-3.5 20.83, GPT-4 58.33, F1 GPT-4 49.28. 저자들은 GPT-4도 사람 라벨과는 "substantial gap"이 있다고 적었다.
- 사람 평가 130개 요청(Table 8): GPT-3.5 작업 계획 통과율 91.22, 타당성 78.47, 모델 선택 통과율 93.89, 타당성 84.29, 최종 성공률 63.08. Vicuna-13b 성공률 15.64, Alpaca-13b 6.92.

읽을 점: 계획 단계와 모델 선택 단계가 각각 90% 넘게 통과해도 요청이 끝까지 해결된 비율은 63.08%였다. 단계별 오류가 곱해지는 구조라는 해석은 추론이다.

### 저자가 밝힌 한계 (논문 5장)

1. 계획이 LLM 능력에 크게 의존해 계획이 항상 실행 가능하고 최적이라고 보장할 수 없다.
2. 효율: 워크플로 전체에서 LLM과 여러 번 상호작용해야 해서 응답 시간이 늘어난다.
3. 토큰 길이: 32K로 늘려도 많은 모델을 연결하기엔 부족하며, 모델 설명을 짧게 요약하는 방법이 과제다.
4. 불안정성: LLM이 지시를 따르지 않거나 틀린 답을 내 프로그램 워크플로에 예외가 생긴다.

### 후속 연구 (같은 저장소)

- TaskBench: https://arxiv.org/abs/2311.18760 (v1 2023-11-30, v4 2024-11-01, arXiv comments "Accepted to NeurIPS 2024"). 논문. 초록에 따르면 작업 자동화를 작업 분해(task decomposition), 도구 선택(tool selection), 인자 예측(parameter prediction) 세 단계로 나누고, 분해된 작업을 Tool Graph(노드는 도구, 방향 간선은 앞 도구 출력 타입이 뒤 도구 입력 타입과 맞는다는 뜻)로 표현한다. 데이터는 도구 그래프에서 부분 그래프를 샘플링한 뒤 거꾸로 사용자 지시문을 생성하는 back-instruct 방식으로 만들고 사람 검증을 거친다. 도메인은 Hugging Face 도구, Multimedia 도구, Daily Life API(저자들이 쇼핑, 교육, 여행 등 40개 API 문서를 직접 작성, 실제 기능 구현은 없음) 세 개다. 본문 4.4에 적힌 수치: 코드 사전학습 모델이 도메인 평균으로 도구 예측 4.45%, 인자 예측 12.76% 향상. 4.5절: 사람 평가와 순위 상관 평균 Kendall τ 0.89, Spearman ρ 0.78. 마스터 설계 관점의 시사점은 HuggingGPT의 task/id/dep/args 구조가 그대로 "도구 호출 그래프" 평가 단위가 됐다는 점이다(추론).
- EasyTool: https://arxiv.org/abs/2401.06201 (v1 2024-01-11, v3 2024-03-27). 논문. 초록 원문 요지: 도구 문서가 "diverse, redundant, or incomplete"해서 LLM의 도구 사용 능력을 떨어뜨리므로, 이를 통일되고 간결한 tool instruction으로 바꾼다. 3.2절 분석에서 문제를 Inconsistency, Redundancy, Incompleteness 셋으로 나누고, 예로 ToolBench의 도구 문서 평균 길이가 약 2,530 토큰(cl100k_base 기준)이라고 적었다. 초록은 토큰 소비를 "significantly" 줄이고 성능을 높였다고만 말하며, 표의 개별 수치는 이 조사에서 옮기지 않았다. HuggingGPT 한계 3번(모델 설명이 토큰을 잡아먹음)에 대한 후속이라고 볼 수 있다(추론).

## 2. JARVIS-1과 그 밖의 JARVIS 이름 연구 에이전트

### 2-1. JARVIS-1 (CraftJarvis, 마인크래프트)

- 논문: https://arxiv.org/abs/2311.05997 (v1 2023-11-10, v3 2023-11-30). 저자 Zihao Wang 외, 북경대(PKU), UCLA, BUPT, BIGAI, "Team CraftJarvis". 프로젝트 페이지 craftjarvis.org/JARVIS-1. 증거 등급: 논문.
- 여기서 JARVIS는 부서 에이전트를 부리는 사무 비서가 아니라, 마인크래프트에서 멀티모달 언어모델(MLM)이 계획을 세우고 하위 컨트롤러에 목표를 보내는 구조다. 마스터 역할 관점에서 참고할 부분은 "계획자(MLM) 위, 실행기(목표 조건 컨트롤러) 아래"라는 2층 분리와 기억 설계다.

마스터(계획자)가 하는 일 (논문 3장, 부록 A에서 읽음):
- 초록: MLM이 시각 관찰과 텍스트 지시를 계획으로 바꾸고, 계획은 "dispatched to the goal-conditioned controllers"된다.
- 하위 실행기(부록 A.1): 채굴 목표는 텍스트 조건 STEVE-1이 수행하고, 제작과 제련은 환경이 craft/smelt 동작을 직접 실행한다. 즉 마스터는 목표 문자열만 내리고 실제 조작은 하지 않는다.
- 입력(부록 A.2): 시각 이미지, 언어, 상징 정보(인벤토리, 위치, 체력 등). 상징 정보는 템플릿으로 자연어로 바꿔 넣는다.
- 실행 전 자기 점검(self-check): 초기 계획을 받으면 단계별 실행을 머릿속으로 시뮬레이션해 각 단계 뒤 상태(주로 인벤토리)를 예측하고, 목표의 선행 조건을 만족하는지 검증해 결함을 미리 찾는다. 논문 예시는 나무가 부족한 채로 땅을 파기 시작하는 경우다.
- 실행 중 복구: 실행 실패가 나면 환경 피드백을 MLM에 넣고 self-explain으로 원인을 설명하고 원래 계획의 버그를 찾은 뒤 계획을 고친다. 저자들은 사람 개입이나 특권 환경 정보 없이 이걸 한다고 강조한다.

기억(state/memory):
- 부록 A.3: 기억은 성공한 궤적만 기록하는 리스트이고, 각 항목은 `task`, `state`, `plan` 키를 가진 딕셔너리다.
- 3.3절: 이 기억을 RAG 지식 저장소처럼 써서 비슷한 과거 경험을 계획 프롬프트의 예시로 넣는다.
- 3.4절 자기 개선: self-instruct로 커리큘럼 과제를 만들어 탐험하며 경험을 쌓고, 그다음 평가한다.
- 기억 절제 실험(4.2.2): 텍스트 임베딩만 쓰는 검색보다 "검색 전에 추론"을 붙이는 쪽이, 그리고 시각과 상징 상태를 함께 쓰는 멀티모달 검색이 더 낫다고 보고했다(수치는 그림으로만 제시되어 옮기지 않음).

측정 결과(본문에서 읽은 것만):
- 초록: 200개 넘는 과제 수행, 단기 과제는 "nearly perfect", ObtainDiamondPickaxe에서 기존 최고 에이전트 대비 신뢰도 5배.
- 서론 그림 설명: 다이아몬드 곡괭이 성공률 JARVIS-1 6% 대 VPT 2.5%. 4.3절: 이 과제는 서로 다른 시드로 300회 넘게 평가.
- 과제 구성(Table 1): 11개 과제 그룹, 200개 이상.

실패와 한계: 다이아몬드 곡괭이 같은 장기 과제 성공률이 6% 수준이라는 수치 자체가 장기 과제의 한계를 보여준다. 논문 목차에 별도 Limitations 절은 찾지 못했다.

### 2-2. 같은 계열의 후속 (CraftJarvis)

- OmniJARVIS: https://arxiv.org/abs/2407.00114 (2024-06-27, comments "accepted on NeurIPS 2024"). 논문. 초록에서 기존 방식을 "텍스트 목표를 별도 컨트롤러로 보내는 방식"과 "제어 명령을 직접 내는 방식"으로 나누고, 행동 궤적을 이산 토큰으로 만들어 하나의 모델이 추론, 계획, 답변, 행동을 모두 하도록 통합했다. 마스터와 실행기를 분리하는 JARVIS-1 구조에서 한 모델로 합치는 방향으로 간 것이다(추론).
- JARVIS-VLA: https://arxiv.org/abs/2503.16365 (2025-03-20, comments "Accepted by ACL 2025"). 논문. 키보드와 마우스로 게임을 하는 VLA 모델. 초록: 1k개 넘는 원자 과제 지시를 따르고, 비궤적 과제로 사후학습하면 최고 기준선 대비 40% 향상. 오케스트레이터 설계와는 거리가 멀다.

### 2-3. 이름만 JARVIS인 기타 연구 (arXiv 제목 검색)

arXiv API로 제목에 "jarvis"가 들어간 논문을 제출일 순으로 조회했다(최대 40건, 실제 반환 22건). 재료과학 데이터베이스 JARVIS(NIST 계열), 수학 추측 등 에이전트와 무관한 것은 제외했다. 초록만 읽었다.

- JARVIS: A Neuro-Symbolic Commonsense Reasoning Framework for Conversational Embodied Agents, https://arxiv.org/abs/2208.13266 (2022-08-28, comments "19th International Conference on Neurosymbolic Learning and Reasoning"). LLM으로 언어 이해와 하위 목표 계획을 하고, 상징 모듈이 상식 규칙으로 행동을 만든다. TEACh의 EDH 미확인 성공률을 6.1%에서 15.8%로 올렸다고 초록에 적혀 있다. Alexa Prize SimBot 공개 벤치마크 1위.
- JARVIS: A Multi-Agent Code Assistant for High-Quality EDA Script Generation, https://arxiv.org/abs/2505.14978 (2025-05-20). 초록상 다중 에이전트 프레임워크이며 도메인 특화 LLM, 구조 검증용 자체 컴파일러, 규칙 강제, 코드 수정, 검색을 조합한다. 초록에는 구체 수치가 없고 본문은 읽지 않았다. 마스터가 검증기(컴파일러)를 끼고 산출물을 고치는 구조로 보이나 본문 미확인이다(추론).
- Jarvis: Towards Personalized AI Assistant via Personal KV-Cache Retrieval, https://arxiv.org/abs/2510.22765 (2025-10-26). 사용자 정보를 텍스트와 이미지 패치 KV 캐시로 저장했다가 질문 시 검색한다. 마스터 오케스트레이션이 아니라 개인화 기억 설계 참고용이다.
- A Survey on the Safety and Security Threats of Computer-Using Agents: JARVIS or Ultron?, https://arxiv.org/abs/2505.10924 (2025-05-16, comments "Accepted by ACL 2026"). 컴퓨터 사용 에이전트의 안전과 보안 위협 분류, 방어 전략 분류, 벤치마크 정리. "자비스가 될지 울트론이 될지"라는 제목 그대로, 컴퓨터를 직접 조작하는 마스터 에이전트의 위험 목록으로 참고할 만하다.
- Talk to Me, Jarvis, https://arxiv.org/abs/2609.21109 (2026-09-17). 자율주행 레이스카용 오프라인 음성 비서. Mistral 7B 미세조정 명령 분류기로 의도 인식 정확도 97.63%, 평균 처리 지연 1.39초(초록 수치). 마스터 오케스트레이터라기보다 "자연어를 정해진 명령 집합으로 분류하는 라우터" 사례다.
- JARVIS AR 지시 시스템, https://arxiv.org/abs/2604.10108 (2026-04-11). AR에서 단계별 안내와 실시간 상태 검증. 참가자 14명 실험. 오케스트레이션과는 무관.
- VQ-Jarvis(비디오 복원 에이전트, 2603.22998), JARVIS 허위 리뷰 판정 검색 시스템(2602.12941)은 제목만 확인했고 초록은 읽지 않았다.

## 3. GitHub 오픈소스 Jarvis 마스터/오케스트레이터 프로젝트 (2025~2026)

### 검색 방법

`gh search repos`로 다음 검색어를 별 수 정렬로 조회했다: "jarvis" (전체 기간, 그리고 2025-01-01 이후 생성분 각 상위 30~40개), "jarvis orchestrator agent", "jarvis multi-agent", "jarvis master agent", "jarvis claude code", "jarvis ai agent orchestrator", "jarvis agents team", "jarvis chief of staff", "jarvis sub-agents", "jarvis orchestrator", "jarvis delegate agents", "jarvis subagents", "jarvis agent os", "jarvis departments", "jarvis company agents", "jarvis supervisor agent", "jarvis langgraph", "jarvis crewai", "jarvis mcp agents", "iron man jarvis agent claude", 그리고 토픽 jarvis와 multi-agent 동시 지정. 
결과 요약: 이름에 orchestrator, master, multi-agent가 들어간 저장소는 거의 전부 별 0~1개의 개인 실습 저장소였다. 별 100개 이상인 Jarvis 저장소는 대부분 음성 비서, 데스크톱 비서, 개인 AI였고, 부서 에이전트 위의 마스터라는 설계를 명시한 곳은 적었다. "departments", "company agents", "supervisor agent", "crewai" 조합은 결과 0건이었다. 저장소 검색은 이름과 설명만 대상으로 하므로 README 안에서만 Jarvis를 언급하는 프로젝트는 빠졌을 수 있다.

### 3-1. open-jarvis/OpenJarvis (Stanford)

- URL: https://github.com/open-jarvis/OpenJarvis , 논문 https://arxiv.org/abs/2605.17172 (2026-05-16), 프로젝트 사이트 openjarvis.stanford.edu. 증거 등급: 공식 저장소 + 논문.
- `gh api` 확인값: 별 10,284, 포크 2,375, 마지막 push 2026-09-27, 보관 안 됨, Apache-2.0, 생성 2026-02-15.
- 성격: README상 Stanford SAIL의 Hazy Research와 Scaling Intelligence Lab 개발, "local-first personal AI" 프레임워크. 부서 에이전트를 부리는 마스터라기보다 개인 AI 스택이다. 다만 내부에 `orchestrator` 에이전트와 로컬/클라우드 모델 라우팅 오케스트레이터가 있어 참고 가치가 있다.

설계(README와 코드에서 읽음):
- 내장 에이전트 8종을 실행 방식 셋(on-demand, scheduled, continuous)으로 나눈다. 예: `morning_digest`(예약, 메일과 캘린더와 건강과 뉴스 브리핑), `deep_research`(요청 시, 인용 포함 다단계 조사), `monitor_operative`(상시, 기억과 압축과 검색이 있는 장기 감시), `orchestrator`(요청 시, 도구 자동 선택 다회전 추론), `operative`(상시, 상태 관리하는 자율 에이전트). 부서별 에이전트를 실행 주기로 나눈다는 발상은 마케팅/개발/운영 설계에 옮겨 쓸 만하다(추론).
- `src/openjarvis/agents/orchestrator.py`: OrchestratorAgent는 도구 정의를 넣어 모델을 부르고, tool_calls가 있으면 실행하고 반복하며, 없으면 최종 답을 낸다. 기본 최대 10턴. 도구 병렬 실행 옵션이 있다. 도구 호출 직전 훅(before_tool_call)이 거부하면 "[Governance] Tool ... was not approved ... Adjust your plan and try a different approach." 메시지를 모델에 돌려준다. 즉 거부를 오류로 끝내지 않고 마스터가 계획을 바꾸게 한다.
- 사람 승인: `tools/_stubs.py`에서 도구 명세에 `requires_confirmation` 필드가 있고, 이 값이 참인데 대화형 모드가 아니거나 확인 콜백이 없으면 실행하지 않고 "requires confirmation but no confirmation" 결과를 돌려준다. 사용자가 거부하면 "execution denied by user". 그 전에 capability_policy가 에이전트별 권한(capability)을 검사한다. 프런트엔드에 ApprovalBell 컴포넌트 파일이 있다(파일명만 확인).
- 루프 방지: `agents/loop_guard.py` 기본값은 같은 (도구 이름, 인자) 해시 3회 반복 시 차단, 창 크기 6으로 A-B-A-B 같은 핑퐁 감지, 폴링 도구 예산 5회, 메시지 100개 넘으면 4단계 압축, 첫 순환은 경고하고 두 번째에 차단.
- 샌드박스: `sandbox/`(WASM 러너, 마운트 보안), `security/guardrails.py`, `security/subprocess_sandbox.py` 파일이 있다(내용은 읽지 않음).
- `agents/hybrid/skillorchestra/`: SkillOrchestra(arXiv 2602.19672) 이식본. README에 따르면 "skill handbook"을 두고 5가지 라우팅 전략(router_decides, analyze_model_decide, weighted_avg, weakest_skill, strongest_skill)으로 어떤 모델에 맡길지 정한다. 원본의 explore, learn, select 학습 파이프라인은 이식하지 않았다고 스스로 밝힌다.

측정 결과(논문 초록 수치만):
- 기존 개인 AI 스택에서 Claude Opus 4.6을 Qwen3.5-9B로 바꾸면 PinchBench, GAIA 등에서 정확도가 25~39pp 떨어진다.
- 최신 프롬프트 최적화기만으로는 로컬과 클라우드 격차를 5pp만 줄인다.
- LLM-guided spec search(클라우드 모델이 스펙 수정안을 내고, 성능이 떨어지지 않는 수정만 채택)를 쓰면 온디바이스 스펙이 8개 벤치마크 중 4개에서 클라우드와 같거나 높고, 평균 3.2pp 이내, 한계 API 비용 약 800배, 전체 지연 4배 감소.
- 스펙은 다섯 가지 원시 요소 Intelligence, Engine, Agents, Tools & Memory, Learning의 타입 있는 명세로 표현한다.

실패와 위험:
- README의 설치 안내가 원격 스크립트를 받아 바로 셸로 실행하는 설치 방식(macOS, Linux, WSL2)과 PowerShell로 원격 스크립트를 바로 실행하는 방식(Windows)을 기본으로 제시한다. 설치 전에 스크립트 내용을 받아서 읽어 보는 편이 안전하다.
- `code-assistant` 프리셋은 README 표현으로 "code execution, file I/O, and shell access"를 가진다. 마스터에 셸 권한을 줄 때 위 승인 필드와 capability 정책을 켜야 한다(추론).
- 스킬을 OpenClaw의 약 13,700개 커뮤니티 스킬, 또는 "any GitHub repo"에서 가져올 수 있다고 README에 적혀 있다. 외부 스킬 가져오기는 공급망 위험 경로다(추론).
- 별 10,284개는 7개월 남짓에 쌓였지만 대학 연구실, 논문, 포크 2,375개가 함께 있어 정상 성장으로 보인다(추론).

### 3-2. ethanplusai/jarvis (Claude Code 위의 음성 마스터)

- URL: https://github.com/ethanplusai/jarvis . 증거 등급: 공식 저장소(개인 개발자 Ethan, ethanplus.ai).
- `gh api` 확인값: 별 809, 포크 277, 마지막 push 2026-09-10, 보관 안 됨, 라이선스 NOASSERTION(README상 개인 비상업 무료, 상업 사용은 별도 라이선스), 생성 2026-03-26.
- 이번 조사에서 "Claude Code 세션들 위의 마스터"를 가장 구체적으로 문서화한 저장소다. README가 설계 결정과 신뢰 가정을 스스로 적어 두었다.

마스터가 하는 일(README 원문 기준):
- 두뇌는 "ONE long-lived `claude -p` process"이고 기본 모델은 Sonnet. 요청마다 새로 띄우지 않고 한 프로세스에 대화를 계속 넣는다.
- 설계 단계: 음성으로 한 번에 질문 하나씩 묻고 두세 가지 접근을 제시하며, 사용자가 하나에 동의하기 전에는 아무것도 시작하지 않는다. 합의 내용은 프로세스를 띄우기 전에 프로젝트 안 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`로 저장되고, 번호 매긴 절 단위로 읽어 주며 음성으로 승인받는다.
- 위임: 실제 작업은 별도 `claude -p` 세션(run)에 브리프를 주어 맡긴다. 브리프는 단계별 계획을 쓰고, 그 계획을 스펙에 비춰 검토하고, 테스트 주도 개발로 작업 단위 실행하며 계획의 체크박스를 채우라고 지시한다. 진행률은 추측하지 않고 체크박스를 읽어 답한다.
- 감시: 자기가 띄운 것뿐 아니라 그 컴퓨터의 모든 Claude Code 세션을 본다. 사람 입력을 기다리는 세션은 즉시 소리로 알리고, 단순히 끝난 세션은 다음 휴지 때 한 문장으로 묶어 알린다. 브라우저 탭이 없으면 macOS 알림으로 바꾼다. 세션에 메시지를 넣거나 터미널의 권한 확인 프롬프트에 키 하나를 눌러 답할 수도 있다.
- 상태와 기억: 장기 기억은 "a folder of plain Markdown files, one fact per file"이고 두뇌가 항상 보는 색인이 있다. 모든 run은 SQLite 행(프롬프트, 프로젝트, 상태, 토큰 사용량, 전체 이벤트 스트림)으로 기록된다.
- 불변 조건 두 가지: run은 항상 succeeded, failed, timed_out, cancelled 중 하나의 종료 상태에 도달한다. 모든 상태 전이는 알림보다 먼저 DB에 기록되며 WebSocket은 캐시 무효화 힌트일 뿐 진실의 원천이 아니다.
- 도구 제한: 두뇌가 쓸 수 있는 도구는 `brain.py` 상단 허용 목록으로 정한다. 외부 MCP 서버는 `data/jarvis/connections.json`에 사용자가 직접 넣은 것만 쓰고, 사용자 전역 설정의 MCP 서버는 물려받지 않도록 격리 옵션으로 실행한다. README 측정값: 연결된 도구 하나당 매 턴 약 250 토큰의 컨텍스트를 쓴다.
- 오염 차단(taint gate): 웹 검색, 웹 페이지 읽기, 화면, 다른 세션 기록, 연결된 MCP 서버 결과를 읽은 턴에서는 그 턴이 끝날 때까지 행동 도구를 모두 거부하고(기억 쓰기 도구는 그 생성이 끝날 때까지), 사용자의 음성으로 시작한 턴이 아니면 행동 도구가 아예 돌지 않는다. MCP 서버 결과는 "reported, never obeyed".
- 비용 격리: 자식 프로세스를 띄울 때 `ANTHROPIC_*`, `CLAUDE_CODE_*` 환경변수를 모두 지운다. README 설명: CLI가 상속받은 API 키를 로그인보다 우선해 조용히 과금이 API 키로 넘어가는 문제를 막기 위해서다.
- 테스트: README상 약 1,640개 테스트, 네트워크와 화면을 건드리지 않으며 실제 claude 프로세스를 띄우는 테스트는 없다.

저자가 밝힌 실패 지점과 의도적 신뢰 결정 다섯 가지(README "What this trusts, and why"):
1. 디렉터리 이름과 세션의 대기 사유 문자열이 음성 문장에 들어가므로, 그 컴퓨터에 디렉터리를 만들 수 있는 누구나 JARVIS가 말할 단어를 넣을 수 있다(구조 있는 지시문은 못 만들게 문자 집합을 제한).
2. 오염 차단은 "행동"을 막을 뿐 "설득"은 못 막는다. 공격자가 심은 제안이 컨텍스트에 남아 있다가 다음 턴에 사용자가 다시 말하면 실행될 수 있다고 명시한다.
3. 모든 run이 최고 권한으로 돈다. 실행 옵션 기본값이 켜져 있어 모든 run이 권한 확인을 모두 건너뛰는 실행 옵션으로 뜬다. 이유는 run에 권한 질문에 답할 터미널이 없어서, 없으면 영원히 멈추기 때문이라고 적었다. 파일시스템 접근은 제한되지 않는다.
4. 루프백(localhost 특정 포트 범위)을 신뢰한다. 같은 포트에 붙은 다른 로컬 프로세스도 run을 시작할 수 있다. 그 외 접근은 권한 0600 토큰 파일로 막는다.
5. 오디오 응답 확인이 끊기면 최대 45초 동안 짧은 대답이 자기 음성 메아리로 오인돼 버려질 수 있다.

요구사항 한계: macOS 전용(AppleScript), Chrome 전용(Web Speech API), Fish Audio 키 필수(대체 음성 없음).

평가: 마스터 설계 요소(설계 합의 후 착수, 스펙 파일, 체크박스 기반 진행 판단, 종료 상태 보장, 오염 차단, 사람 대기 세션 알림)가 잘 드러나지만, 하위 작업자에게 권한 확인 없는 전권을 주는 구조다. 부서 에이전트 설계에 가져온다면 하위 실행의 권한 범위 제한이 가장 먼저 바꿔야 할 지점이다(추론).

### 3-3. vierisid/jarvis (usejarvis.dev, 부서 역할 계층을 가진 상시 데몬)

- URL: https://github.com/vierisid/jarvis , 사이트 usejarvis.dev. 증거 등급: 공식 저장소.
- `gh api` 확인값: 별 665, 포크 186, 마지막 push 2026-09-26, 보관 안 됨, 라이선스 표기 NOASSERTION(LICENSE 파일은 "Jarvis Source Available License 2.0 (Based on RSALv2)", 오픈소스 라이선스가 아니라 소스 공개형), 생성 2026-02-23. 커밋 약 448개(API 페이지 수로 셈), 기여자 10명(API 응답 길이).
- 사용자 요구(마케팅/개발/운영 부서 위의 마스터)와 가장 가까운 구조를 코드와 설정 파일로 가지고 있다.

마스터 설계(README와 파일에서 읽음):
- README: "An always-on autonomous AI daemon with desktop awareness, multi-agent hierarchy, visual workflows, and goal pursuit." 서버에 상주하는 데몬 하나가 두뇌이고, 각 컴퓨터에 설치한 sidecar가 그 기기의 데스크톱, 브라우저, 터미널, 파일시스템 등 "눈과 손"을 제공한다.
- 역할 파일(`roles/`): 최상위 역할로 `ceo-founder`, `chief-of-staff`, `dev-lead`, `marketing-director`, `system-admin`, `executive-assistant`, `personal-assistant`, `research-specialist`, `activity-observer`가 있고, `roles/specialists/` 아래에 content-writer, customer-support, data-analyst, financial-analyst, hr-specialist, legal-advisor, marketing-strategist, project-coordinator, research-analyst, software-engineer, system-administrator, workflow-default가 있다.
- 역할 파일 구조(chief-of-staff.yaml, marketing-director.yaml에서 확인): `responsibilities`(소유 업무), `autonomous_actions`(승인 없이 가능한 행동), `approval_required`(명시 승인 필요 행동), `kpis`(지표, 목표, 점검 주기), `communication_style`, `heartbeat_instructions`(주기 점검 절차), `sub_roles`(생성하고 위임할 수 있는 하위 역할), `tools`, `authority_level`(1~10).
- 예: `ceo-founder`의 sub_roles는 `marketing-director`(과제당 최대 예산 500 USD)와 `dev-lead`(1000 USD)이고 둘 다 `reports_to: ceo-founder`, authority_level 9. `chief-of-staff`는 authority_level 7, 하위 역할 research-assistant(과제당 100 USD), heartbeat 기본 "every 2 hours during business hours"에 일정 점검, 메일 분류(URGENT/IMPORTANT/FYI/NOISE), 마감 점검(7일, 3일, 1일, 4시간 전 알림), 액션 아이템 후속, 일일 브리핑, 개선 제안 6단계를 수행한다.
- marketing-director의 승인 필요 목록 예: 라이브 게시, 광고비 지출, 고객이나 언론 접촉, 공개 발표, 이메일 캠페인 발송, 제품 기능 주장. 승인 없이 가능한 것은 초안 작성, 경쟁사 조사, 지표 분석, 게시 예약을 초안 상태로 두기, 하위 에이전트(Content Writer, Social Media Manager) 생성 등.
- 위임 코드(`src/agents/delegation.ts`): delegateTask는 부모-자식 관계인지, 부모에게 `can_spawn_children` 권한이 있는지 확인한 뒤 자식에게 commitment(할 일, 맥락, 우선순위, 마감, 담당자, 생성자)를 만들고 `requires_response: true` 작업 메시지를 보낸다. reportCompletion은 자식이 `{task, success, summary, details}` JSON을 부모에게 보고하며, 실패면 우선순위를 high로 올린다.
- 위임 도구(`src/actions/tools/delegate.ts`): 동기 모드는 전문가 하위 에이전트를 만들고, 그 역할에 허용된 도구만 담은 범위 제한 도구 레지스트리를 주어 끝까지 실행한 뒤 종료시키고, 사용 도구 목록과 토큰 수를 붙여 마스터에게 돌려준다. 병렬이나 지속 작업은 manage_agents를 쓰라고 도구 설명에 적혀 있다. 코드 주석: 하위 에이전트는 부모의 권한 엔진과 부모의 유효 프로필(그 턴의 오염 상태 포함) 아래에서 돌기 때문에 "delegation is not a way around the gate: governed actions are denied outright in a sub-agent." README도 "authority stays with the top-level agent"라고 적었다.
- 권한 분류(`src/roles/authority.ts`): 행동을 read_data, write_data, delete_data, send_message, send_email, execute_command, install_software, make_payment, modify_settings, spawn_agent, terminate_agent, access_browser, control_app으로 나누고, 영향도를 read, write, external, destructive 넷으로 매핑한다. destructive(결제, 삭제, 에이전트 종료, 명령 실행, 설치, 설정 변경)는 음성으로 승인할 수 없고 대시보드 클릭만 인정한다. 비파괴 행동의 음성 승인은 음성 인식 신뢰도 0.85 이상일 때만 받는다.
- README "Authority & Autonomy": 런타임 강제, soft-gate 승인, 채팅/Telegram/Discord로 승인 요청 전달, 전체 감사 기록, 긴급 일시정지와 중지, 연속 승인을 학습해 자동 승인 규칙을 제안. Security 절: 재시작으로 끊긴 승인된 행동은 저절로 재실행하지 않고 사용자가 한 번 실행할지 닫을지 정한다.
- 기억: SQLite에 저장하는 vault 지식 그래프(개체, 사실, 관계)를 매 응답 후 자동 추출하고 시스템 프롬프트에 주입한다.
- 목표 추적: OKR 계층(objective, key result, daily action), 0.0~1.0 점수, 아침 계획과 저녁 회고, 뒤처지면 "drill sergeant" 식으로 독촉.
- 도구 루프: README 표현으로 턴당 최대 200회 반복, "runs until the task is complete, not until the response looks done."

측정 결과: README에 성능 수치나 벤치마크는 없다. 커밋 수, 테스트 CI 배지만 확인했다.

실패와 위험(README에서 읽은 것과 추론 구분):
- 원격 설치 스크립트를 받아 바로 셸로 실행하는 설치 방식을 "One-liner"로 제공한다. bun 전역 패키지와 Docker 방식도 있다.
- 초기 설정 때 sidecar 없이 쓰려면 인증 없이 전체 접근을 허용하는 설정을 임시로 켜고 등록 후 끄라고 안내한다. 끄는 걸 잊으면 대시보드가 무인증으로 열린다(추론).
- 화면을 5~10초마다 캡처하고 OCR과 클라우드 비전으로 보낸다(README). 개인정보 노출 범위가 넓다.
- 익명 사용 지표를 기본 전송하며 끌 수 있다고 README에 적혀 있다.
- 관리형 호스팅 파트너(opencove.host)를 README에서 홍보한다. 제3자 호스팅에 API 키와 화면 데이터가 올라가는 구조다(추론).
- 첫 설정 뒤에는 배경 서비스가 재시작해야 켜진다고 README가 스스로 밝힌 알려진 문제가 있다.
- 역할 YAML의 KPI(예: "unread_email_count < 10")가 실제로 측정되는지 코드 수준 확인은 하지 않았다.

### 3-4. adewaskar/jarvis (Claude Agent SDK 기반 음성 비서, 기본 읽기 전용)

- URL: https://github.com/adewaskar/jarvis . 증거 등급: 공식 저장소(개인).
- `gh api` 확인값: 별 265, 포크 116, 마지막 push 2026-08-05, 보관 안 됨, MIT, 생성 2026-08-02. 생성 사흘 뒤 마지막 push인데 별 265, 포크 116이다. 짧은 기간에 모인 관심으로 보이며 이후 유지보수는 확인되지 않는다(추론).
- 설계: 브라우저(얼굴과 음성)와 브리지(두뇌와 손) 두 프로세스. 브리지는 Claude Agent SDK로 Claude Code를 헤드리스로 돌린다. 기본 모델 `claude-opus-5`, effort medium(README 값). 사용자 설정 파일의 MCP 서버들을 SDK에 넘긴다.
- 부서 위임 구조는 없다. 단일 두뇌가 MCP 도구를 직접 쓰는 형태다. 마스터 설계로서 참고할 점은 승인 방식이다.
- 도구 게이트: README 원문 "The tool gate starts read-only." 검색, 생성, 조회는 자유롭고 보내기, 탭, 삭제, 설치, 결제 같은 효과 있는 도구는 거부된다. 이유: "Voice is a poor interface for a confirmation dialog", 그래서 사용 시점이 아니라 사전에 `decideTool()`에서 결정한다. 브리지가 파일시스템 설정 소스를 비워서 자기 게이트만 유일한 권한이 되고, 전역의 권한 우회 설정도 이를 덮을 수 없다고 적었다. 쓰기를 켜는 별도 실행 스크립트가 있고 켜기 전에 `decideTool()`을 읽으라고 경고한다.
- 보안: 로컬 개발 origin만 WebSocket 허용, 파일과 미디어 엔드포인트는 허용 루트로 제한하고 사설망과 루프백 주소를 거부(SSRF 방어), 모델이 만든 HUD HTML은 DOMPurify와 클래스 허용 목록, 엄격한 CSP로 소독.
- 측정 결과: 없음.
- 대비: ethanplusai/jarvis는 하위 run에 전권을 주고 오염 차단으로 방어하는 반면, 이 저장소는 기본 거부(default-deny)를 택했다. 음성 인터페이스에서 실시간 승인을 어떻게 할지에 대한 두 가지 다른 답이다(추론).

### 3-5. cchen1436/JarvisBench (마스터의 "사용자 주의 배분"을 재는 벤치마크)

- URL: https://github.com/cchen1436/JarvisBench . 증거 등급: 공식 저장소(연구 프리뷰, 논문 링크는 README에서 찾지 못함).
- `gh api` 확인값: 별 102, 포크 1, 마지막 push 2026-08-26, 보관 안 됨, 라이선스 없음(README: 재배포는 아직 허가되지 않음), 생성 2026-08-11.
- 핵심 개념: README "evaluates how a control layer allocates scarce user attention during long-horizon agent work." Jarvis를 실행 관리자가 아니라 "주의 배분 계층"으로 정의한다. docs/ARCHITECTURE.md 원문: 다중 에이전트 실행에서 "Parent remains the execution manager. Jarvis is a separate attention allocator with its own prompt, context, state, and model call." README에서도 "Parent is the execution manager and Jarvis is the attention layer; they are never the same logical agent."
- 평가 축: Track 1은 컨트롤러가 유용한 순간에 사용자 판단을 요청하고 그 답을 올바른 실행 노드로 되돌려 보내는지, Track 2는 점진적으로 공개되는 제한된 진행 기록만 보고 사용자 질문에 답할 수 있는지를 잰다. 기준선은 컨트롤러 없음(`none`).
- 상태 설계: 변경 가능한 제어 상태는 세션별로만 두고, 프로젝트 전체에 공유되는 것은 추가만 가능한 이벤트 버스와 결정 원장(decision ledger)뿐이다. Track 2는 작업자 프로세스나 작업 공간에 손댈 수 없는 불변 재생만 받는다.
- 과제: 단일 에이전트 과제 20개를 다른 벤치마크에서 가져왔다(UniClawBench 6, Pi-Bench 4, AgentIF-OneDay 3, WildClawBench 2, 그 외 5개 각 1).
- 측정 결과: README에는 점수가 없고 공식 채점은 별도 봉인 평가기로 한다고 적혀 있다.
- 시사점: "자비스" 역할을 (a) 일을 나눠 주는 실행 관리자와 (b) 사람에게 언제 무엇을 물을지 정하는 주의 관리자로 쪼갤 수 있다는 설계 관점을 준다(추론).

### 3-6. Grominet95/jarvis-OS (미션 엔진과 자율성 등급)

- URL: https://github.com/Grominet95/jarvis-OS . 증거 등급: 공식 저장소(개인, 프랑스어 README).
- `gh api` 확인값: 별 168, 포크 50, 마지막 push 2026-08-24, 보관 안 됨, AGPL-3.0, 생성 2026-01-12.
- 설계(README에서 읽음, 코드는 읽지 않음):
  - Mission Engine: 요청을 계획된 미션으로 바꾸고 각 단계를 구조, 결정론, 의미 세 층으로 검증하며 충돌 후 재개. 파일은 `mission/orchestrator.py`, `worker_agent.py`, `verifier.py`, `governance.py`, `reflexion.py`, `capability_engine.py`.
  - 거버넌스: 파일시스템이나 네트워크를 건드리는 모든 것은 "위험 x 범주 x 예산" 복합 게이트를 거치고 변경 불가 감사 기록을 남긴다.
  - 선제적 이니셔티브: 각 이니셔티브는 트리거, 목표, 최대 비용(토큰, 시간, 돈), 자율성 등급 0~5(0은 답변만, 5는 게시/결제/연락이며 사람 승인 필수), 상태를 가진다. 3(샌드박스 실행), 4(프로젝트 파일 수정), 5(게시, 결제, 연락)는 행동 전에 복합 게이트를 거친다.
  - Command Center: 진행 중 이니셔티브와 미션의 목표, 예산, 권한, heartbeat, 비용을 한 화면에서 본다. README 표현 "Jarvis ne fait pas des trucs, il gère des workstreams"(일을 하는 게 아니라 작업 흐름을 관리한다).
  - 야간 Curator: 매일 밤 사실 모순, 안 쓰는 스킬, 프롬프트 드리프트, 비용, 반복 오류를 보고하고 패치를 제안만 하며, 게이트를 넘는 것은 사람이 승인한다.
  - Skill Lab: 사용에서 생긴 스킬을 Docker 샌드박스에서 시험하고 사람이 승인한 뒤 설치한다.
  - 기억: SQLite를 진실의 원천으로, 날짜와 출처가 붙은 원자적 사실, 사람이 읽을 수 있는 Markdown 미러.
  - 코드 품질 장치: 4층 구조를 import-linter 계약으로 CI에서 강제, 단위 테스트 약 587개(README 수치).
- 측정 결과: 에이전트 성능 수치 없음.

### 3-7. cgoinglove/thursday (음성 마스터 + 뒤에서 일하는 봇 팀)

- URL: https://github.com/cgoinglove/thursday . 증거 등급: 공식 저장소(개인). 이름은 Thursday이고 설명에 "An open-source FRIDAY"라고 적었다. 자비스 계열 명명(아이언맨 AI)을 따른 경우로 포함했다.
- `gh api` 확인값: 별 10, 포크 0, 마지막 push 2026-09-27, MIT, 생성 2026-09-08. 작은 신규 저장소다.
- 설계(README): 음성 모델이 통화를 유지하고, 몇 초 넘게 걸리는 일은 모두 백그라운드 봇에게 넘긴다. 이유: 브라우저를 여는 음성 모델은 1분간 조용해지고 "a silent call is a dead call". 봇끼리 일부를 넘기고, 필요한 결과가 올 때까지 일부를 보류하고, 돌아온 것을 확인하고, 결정이 사용자 몫일 때만 묻는다. 모든 인계는 저장되어 누가 무엇을 했는지 스레드로 볼 수 있다. 결제는 Pay 버튼 앞에서 멈춘다.
- 저자가 밝힌 한계: "It is not a sandbox. Bots run real commands as you. Stopping at Pay and asking before using a login are instructions a model follows, not locks." 즉 승인 지점이 코드 강제가 아니라 프롬프트 지시라는 점을 스스로 밝힌다.

### 3-8. 작은 저장소지만 마스터 구조가 명확한 사례

- PhillipHamnett/ai-wealth-consultant, https://github.com/PhillipHamnett/ai-wealth-consultant . 별 1, 포크 1, 생성과 마지막 push 모두 2026-05-20, 라이선스 없음. 증거 등급: 공식 저장소(개인, 사실상 단발 공개).
  - Claude Code 서브에이전트 파일로 만든 3층 구조: 최상위 Jarvis(`jarvis-wealth-orchestrator`), 중간 관리자 Vera(세무)와 Mira(투자), 그 아래 전문가 다수(README는 24개라고 적음). 부서장 아래 전문가를 두는 형태라 사용자 요구의 "마스터 아래 부서 에이전트" 구조와 가장 닮았다.
  - Jarvis 에이전트 파일에서 읽은 규칙: 세션 시작 시 `client-profile/*.md` 8개 파일을 모두 읽는다. 여러 전문가가 필요하면 한 메시지에서 여러 Agent 호출로 병렬 fan-out. 하위 에이전트는 사용자 메시지를 못 보므로 질문, 관련 프로필 사실, 원하는 반환 형식을 브리프에 모두 담는다. "Default to over-consulting." 행동 제안에는 투자 쪽 전문가, 세무 관리자, 준법 담당(Sasha)을 반드시 함께 부른다. 최종 종합은 위임하지 않는다("never delegates the final synthesis", README). 새 사실은 즉시 해당 프로필 파일에 쓰고 답변에서 알린다. 빠르게 바뀌는 규칙은 인용 시점에 검증하고, 못 하면 "unverified"라고 쓴다.
  - 사람 승인: 실제 주문은 환경변수 두 개를 모두 끄고, 브리프에 문자 그대로 `EXECUTE: confirmed` 토큰이 있을 때만. 기본값은 모의투자, 읽기 전용. 세무 신고는 사람 서명 없이 절대 금지.
  - 한계: 에이전트 정의에서 도구에 Bash, Write가 포함되어 있어, 위 금지 규칙은 프롬프트 수준 약속이다(추론). 측정 결과 없음.
- Byrens-AiBot-JARVIS/mission-control, https://github.com/Byrens-AiBot-JARVIS/mission-control . 별 0, 2026-02-18 생성, 이튿날 이후 push 없음. "Shared brain for the Jarvis agent team." Convex 실시간 DB에 agents, tasks, messages, activities, documents, notifications 테이블을 두고 CLI로 에이전트 등록, 작업 상태(inbox, assigned, in_progress, review, done), 작업별 스레드, 활동 피드(감사 로그), 알림을 다룬다. 공유 작업판을 마스터의 상태 저장소로 쓰는 패턴의 예다. 위험: README에 실제 배포 백엔드 URL이 적혀 있고 설정이 없으면 코드에 하드코딩된 기본 URL을 쓴다고 명시한다. 남의 공유 백엔드에 작업 내용을 쓰게 될 수 있다.
- 그 밖에 검색에서 이름에 Jarvis와 orchestrator가 같이 들어간 저장소(예: nikocarba/my-first-coding-agent-repo "JARVIS orchestrator + Claude Code workers", phynyx1980/Phynyx-Agent-Cockpit, Tylersfritz/jarvis-orchestrator, rook1ess/JarvisOrchestrator, mdk32366/JARVIS-Master-Agent, atulmishra84/jarvis-chief-of-staff)는 모두 별 0~1개였고 README를 읽지 않았다.

### 3-9. 이름은 Jarvis지만 마스터 오케스트레이터가 아닌 것 (확인 결과 제외)

- ascending-llc/jarvis-registry (별 3,170, Apache-2.0, 2025-10-04 생성, 2026-09-25 push): README상 기업용 MCP와 A2A 에이전트 게이트웨이. "orchestrator agents coordinate worker agents through the same secure gateway", OAuth/OIDC, 도구 단위 ACL, 감사 로그를 제공한다. 마스터 자체가 아니라 마스터와 부서 에이전트가 도구에 접근하는 통로와 권한 계층이다. 부서별 도구 권한 분리가 필요하면 이런 게이트웨이 계층이 해법 후보다(추론).
- heardlabs/heard (별 189, Apache-2.0): 코딩 에이전트 출력을 음성으로 읽어 주는 층. README가 "Jarvis-style narrator"라고 부른다. 마스터가 아니라 알림층이다. 위험: README 권장 설치가 AI 코딩 도구에 붙여 넣으라는 명령인데, zip을 내려받아 응용프로그램 폴더에 풀고 macOS 격리 속성(다운로드 파일 검사 표시)을 지운 뒤 바로 여는 방식이다. 서명 검사를 우회하는 설치를 AI 에이전트가 실행하게 유도하는 형태라 공급망 위험이 크다.
- blogminhquy/javis-os (별 199, 포크 121, MIT, 2026-06-28 생성): 베트남어 README. 설치 명령이 Windows에서 PowerShell 실행 정책을 우회하는 방식이다. README가 스스로 Claude 구독을 백그라운드 상시 실행, VPS, 다인 공유에 쓰는 것은 개인 사용 범위를 넘을 수 있다고 경고한다. Kanban에 목표를 주면 AI가 사양을 쓰고 작업자를 골라 백그라운드로 돌리며 예외 때만 부른다는 기능 설명이 있으나 코드는 읽지 않았다.
- YINDEEINDY/MYJarvis (별 1, 생성과 마지막 push 모두 2026-04-28): Claude Code 구독 위 `claude -p` 서브프로세스 두뇌, 4단계 신뢰 게이트(auto, approve, confirm, block), Haiku 기반 중요도 1~5 점수로 라우팅, "8-perspective Council". 단발 공개로 보인다.
- jev-chat/jev-chat-jarvis: 2026-09-21 생성, 6일 만에 별 6,772, 포크 1,166. 메신저 답장 추천 도구로 마스터 오케스트레이터가 아니다. 생성 직후 별이 매우 빠르게 늘었으므로 별 수를 신뢰 지표로 쓰면 안 되는 예로 기록한다(조작 여부는 판별하지 않음).
- danilofalcao/jarvis(여러 모델을 고르는 코딩 도우미, 2025-01 이후 push 없음), isair/jarvis, akshayaggarwal99/jarvis-ai-assistant 등 별 수백 개짜리 다수는 음성/데스크톱 비서였다.

## 4. 회사와 실무자의 "자비스형" 또는 비서실장(chief of staff)형 마스터 에이전트

### 4-1. Anthropic Claude Cookbook: The chief of staff agent

- URL: https://github.com/anthropics/claude-cookbooks/tree/main/claude_agent_sdk (노트북 `01_The_chief_of_staff_agent.ipynb`, 코드 `chief_of_staff_agent/`), 웹판 https://platform.claude.com/cookbook/claude-agent-sdk-01-the-chief-of-staff-agent . 증거 등급: 벤더(공식 튜토리얼).
- 날짜: 현재 경로 기준 가장 오래된 커밋 2025-10-23, 최근 모델 표기 갱신 커밋 2026-02-17("update all model references from Claude 4.5 to Claude 4.6"). 경로 이동 전 이력은 확인하지 않았다.
- 시나리오(노트북 원문): Series A로 10M 달러를 막 조달한 50인 스타트업의 CEO를 위한 AI Chief of Staff. 최종 에이전트는 "Coordinate specialized subagents for different domains", "Aggregate insights from multiple sources", "Provide executive summaries with actionable recommendations".
- 마스터 설계(agent.py와 노트북에서 읽음):
  - 모델 `claude-opus-4-6`, 허용 도구는 Task(서브에이전트 위임), Read, Write, Edit, Bash, WebSearch.
  - 하위 에이전트는 `.claude/agents/`의 Markdown 파일 두 개: `financial-analyst`(도구 Read, Bash, WebSearch)와 `recruiter`. 프런트매터는 name, description, tools 세 필드이고, 노트북은 description이 "main chief of staff agent to know when to invoke each subagent"하는 용도라고 설명한다. 위임 호출 예시는 Task 도구에 description, prompt, subagent_type을 넘기는 형태다.
  - 노트북이 든 서브에이전트 이유 세 가지: 전문화, 분리된 컨텍스트(자기 대화 이력과 도구), 병렬화.
  - 기억: 작업 디렉터리의 CLAUDE.md에 회사 개요, 재무 요약(월 소진액 약 50만 달러, 런웨이 20개월 등), 조직 구성, 우선순위, 보상 기준, 이사회 구성, 최근 결정을 넣는다. 노트북 관찰: CLAUDE.md와 세부 CSV가 함께 있으면 에이전트가 더 세밀한 원천(CSV)을 찾아 읽는 경향이 있고, 요약 수치를 쓰게 하려면 프롬프트로 유도해야 한다. 예로 CLAUDE.md의 50만 달러 대 CSV의 총 52.5만, 순 23.5만 달러 차이를 든다. 권장: CLAUDE.md에는 고수준 맥락, 세부 데이터 위치, 언제 어느 수준 숫자를 쓸지에 대한 지침을 둔다.
  - 계획 모드: 실행 없이 계획만 만들게 하고, 계획을 파일로 저장해 검토, 승인 후 대화를 이어서 실행하는 "plan → review → approve → execute" 순환을 제시한다. 노트북 스스로 헤드리스 SDK에서는 계획 모드가 아직 완전히 맞춰지지 않았다고 적었다(에이전트가 대화형 전용 도구를 부르려 함). 계획이 텍스트, Write 호출, 내부 계획 디렉터리 중 어디로 나올지 몰라 우선순위 기반 수집 로직을 따로 짰다.
  - 훅: 도구 실행 뒤에 결정론적 스크립트를 돌려 감사 기록을 남긴다. 예제는 Bash, Write, Edit 호출을 감시해 보고서 변경 이력을 `audit/report_history.json`에, 스크립트 사용을 `audit/script_usage_log.json`에 적는다. 노트북 표현: 훅은 "deterministically" 실행되어 검증과 감사 기록에 적합하다.
  - 출력 스타일: 청중별(executive, technical) 응답 형식을 파일로 분리.
  - 슬래시 명령: `/budget-impact`, `/strategic-brief`, `/talent-scan` 같은 검증된 프롬프트 템플릿. 노트북은 이것이 에이전트 능력이 아니라 사용자용 단축키라고 명시한다.
  - SDK 설정 주의: 파일시스템의 CLAUDE.md, 서브에이전트, 명령, 훅을 읽으려면 설정 소스에 project(훅은 local까지)를 넣어야 하고, 넣지 않으면 "isolation mode"로 돈다고 코드 주석에 적혀 있다.
- 측정 결과: 없음(튜토리얼).
- 한계: 예제 데이터는 가상 회사다. 하위 에이전트 두 개, 사람 승인은 계획 모드 검토 한 가지뿐이라 부서 규모 운영 설계로는 출발점 수준이다(추론).

### 4-2. xAI Grok Bot (2026-08-11, "chief of staff" 봇이 위에 있는 봇 팀)

- URL: https://x.ai/news/introducing-grok-bot (공식 발표, 2026-08-11). 보도: https://www.unite.ai/xai-launches-grok-bot-always-on-ai-teammates-with-their-own-cloud-computers/ . 증거 등급: 벤더(발표문은 WebFetch 요약으로 읽음, 원문 전체 인용은 아님).
- 공식 발표 요약: 여러 봇이 병렬로 일하고 "chief of staff" 봇이 나머지를 관리한다. 전문 봇은 받은편지함, 경비, 채용, 버그 수정, 운영 같은 lane을 맡고, 서로 메시지를 보내고 스레드로 맥락을 공유하며 그룹 채팅에서 스스로 조율한다. 봇은 일을 끝까지 하고 "only come back when something needs your approval". 한 번 시연한 작업을 routine으로 저장해 이후 혼자 실행한다.
- Unite.AI 보도 인용: 각 봇이 자기 클라우드 컴퓨터를 갖고 사용자의 기존 도구에 로그인하며, xAI가 이를 "a small team with a chief of staff on top"으로 표현했다고 한다. 접근은 기존 구독(SuperGrok Heavy, Cursor Ultra 월 200달러, Cursor Teams Premium 좌석당 월 120달러)에 묶여 있다.
- 한계: 베타, 기업 사용자는 대기자 명단. 발표문 요약에서 보안, 권한 통제, 접근 관리에 관한 설명은 찾지 못했다. 측정 결과는 없음.
- 독립 해설(atal upadhyay, 2026-08-16, https://atalupadhyay.wordpress.com/2026/08/16/grok-4-6-grok-bot-and-the-rise-of-the-chief-of-staff-agent-pattern/ , 독립 실무자): 이 패턴의 요소로 진입점 하나인 chief of staff 에이전트, 서브에이전트별 컨텍스트 격리, 에이전트 간 직접 통신, 클라우드에서의 지속 실행, 현실 세계 결과가 있는 행동의 승인 게이트, 반복 절차의 매크로 녹화와 결정론적 재생을 든다. 다단계 작업이 중간에 실패하면 처음부터 다시 해야 하는 점을 신뢰 위험으로 지적한다.

### 4-3. Quick Custom Intelligence(QCI)의 Jarvis (2026-07-30 보도자료)

- URL: https://www.globenewswire.com/news-release/2026/07/30/3336346/0/en/QCI-Advances-Beyond-AI-Agents-with-the-Next-Generation-of-Jarvis.html . 증거 등급: 벤더(보도자료, 자사 주장).
- 내용(인용): Jarvis를 "an AI assistant"에서 "a coordinated machine that manages work across the organization"으로 바꾸고, "specialized agents, tools, and workflows"를 하나의 운영 시스템으로 연결했으며 "keeping people in control of critical decisions".
- 수치(자사 주장, 독립 검증 없음): 내부 운영 워크플로의 약 80%를 지원, 고객 티켓 평균 해결 시간 약 40% 단축(3주에서 1.8주).
- 설계 세부(위임 방식, 승인 규칙, 실패 사례)는 보도자료에서 찾지 못했다.

### 4-4. Google "Project Jarvis" (2024 보도, 이후 Project Mariner)

- 9to5Google 2024-10-26 보도(출처 The Information), https://9to5google.com/2024/10/26/google-jarvis-agent-chrome/ . 증거 등급: 언론 보도(2차).
- 내용: Gemini 2.0 기반 Chrome 에이전트로, 화면을 자주 캡처해 해석한 뒤 버튼 클릭이나 입력을 한다. "operates relatively slowly because the model needs to think for a few seconds before taking each action". 12월 미리보기 가능성.
- 위키백과 Project Mariner 문서(https://en.wikipedia.org/wiki/Project_Mariner , 2차 자료): 2024-12-11 연구 프로토타입 공개, 2025-05-20 갱신, "discontinued on May 4, 2026"로 적혀 있다. 이 문서에는 Jarvis라는 코드명 언급이 없어 Jarvis와 Mariner가 같은 프로젝트라는 연결은 보도와 검색 요약에 기댄 것이다(직접 1차 확인 못 함).
- 이것은 부서를 부리는 마스터가 아니라 브라우저 조작 에이전트다. 이름이 Jarvis였다는 점 때문에 기록만 한다.

### 4-5. 독립 실무자 글 (Jarvis 또는 chief of staff 마스터를 직접 만든 사례)

- Doneyli De Jesus, "I Built an AI Chief of Staff That Runs My Life While I Sleep", 2026-03-15, https://doneyli.substack.com/p/i-built-an-ai-chief-of-staff-that . 독립 실무자. Jarvis 언급 없음. WebFetch 요약으로 읽음.
  - 구조: 에이전트 26개(비서실장 계열 7, 로컬 인프라 9, 콘텐츠와 조사 10). 전용 2022 MacBook Pro에서 macOS launchd로 돌린다. 1단계는 30분마다 LLM 없이 규칙만으로, 2단계는 매일 오후 5시에 전체 메일 분류.
  - 기억 3층: 관찰 기록(비용 0), LLM으로 일일 기억 합성(약 550 토큰 상한), BM25 전문 검색. 최근 접근 기억은 주기당 0.02씩 천천히 감쇠.
  - 단계적 자율: 1단계는 모든 초안 승인, 2단계는 신뢰도 0.9 초과 시 감독하의 자동 발송, 3단계는 코드에 박아 둔 자동 발송 금지 연락처(VIP, 가족)만 빼고 완전 자율.
  - 글에 적힌 수치: 두 사용자 합산 하루 3달러, Claude Max 월 100달러, 하루 메일 100통 이상, 단계화된 범주에서 수정 없이 발송되는 비율 80% 이상, Python 43,000줄, 테스트 파일 133개, 커밋 313개.
  - 실패: 다중 사용자(본인과 배우자) 버그로 브리핑이 엉뚱한 메일로 가고, Signal 봇이 잘못된 DB를 조회하고, 초안에 다른 사람 이름으로 서명됐다. 인증, 설정, 기억, 페르소나, 알림, 예약 작업을 사용자별로 격리해야 했다.
- Amit, "The AI Chief of Staff Is a Fleet, Not an Agent", 2026-06-06, https://dev.to/amitrix/the-ai-chief-of-staff-is-a-fleet-not-an-agent-1i . 독립 실무자. Jarvis 언급 없음.
  - 주장(인용): "A real AI Chief of Staff is not one agent. It's a fleet of 20+ specialized agents." 각 에이전트가 자기 일정(5분~주 단위), 좁은 쓰기 권한(예: 특정 채널에만), 새 데이터가 없으면 실행하지 않는 트리거 조건을 갖는다.
  - 상태: CSV(레지스트리), YAML(설정), Markdown(서술). "The file system is the bus."
  - 자율 사다리: L0~L1 읽기 전용 분류와 초안 제안(현재), L2 저위험 로컬 쓰기만 자동, 그 이상은 미래. "Nothing customer-facing leaves without human approval."
  - 수치: 트리거 조건으로 LLM 호출을 하루 5,760회에서 의미 있는 30~50회로 줄였다.
  - 스스로 밝힌 부족한 점: 에이전트 간 학습, 고정 주기를 넘는 적응형 일정, 신뢰 등급 자동 승격, 전체 관측성.
- Sid Bharath, "How to Build a Jarvis AI Assistant With Claude Code", 2026-01-21(갱신 2026-08-25), https://sidbharath.com/blog/how-i-built-jarvis/ . 독립 실무자. WebFetch 요약으로 읽음.
  - 계층형 서브에이전트가 아니라 파일 기반 시스템. JSON이 진실의 원천(projects.json, tasks.json)이고 Markdown 대시보드는 생성된 보기다. CLAUDE.md는 운영 매뉴얼, 반복 절차는 Skills로.
  - 승인 규칙: Read(자동), Prepare(초안 검토 필요), Act(메일 발송, 일정 생성, 파일 삭제는 명시 승인). 인용: "Important boundaries deserve controls", "Do not begin by connecting your entire digital life with broad write permissions."
  - 스스로 밝힌 실수: 개인, 업무, 영업을 한 시스템에 섞었다가 분리함. Markdown을 너무 오래 DB처럼 써서 신뢰성 문제 뒤 JSON으로 옮김. CLAUDE.md에 너무 많이 적어서 절차를 Skills로 옮김. 자동화와 사람 판단 제거를 혼동함. "The goal is leverage, not absence."
- Pascal Matthiesen, "I Built My Own Jarvis With Zero Code and a Telegram Bot", https://www.arcade.dev/blog/claude-routines-arcade-gateways/ . 벤더 블로그(Arcade.dev 자사 제품 홍보), 날짜는 WebFetch 결과에서 확인 못 함. Claude Routines로 매시간 실행, Arcade MCP 게이트웨이로 Gmail, GitHub, Slack, Telegram 도구를 한 엔드포인트로 묶고, 처리한 항목은 Git에 커밋한 JSON 파일로 중복 방지. 설정 약 15분이라고 적었다. 마스터-부서 구조는 아니다.
- 검색에서 FrankX("Build Your Own Jarvis", 2026-06-07 갱신), Jeff Su(Claude Cowork로 Jarvis 만들기) 글도 나왔지만 본문을 읽지 않았다.

## 5. 종합: 출처들에서 "자비스형 마스터"가 구체적으로 뜻하는 것

### 5-1. 이름의 쓰임새는 세 갈래다

1. 연구 논문의 JARVIS(Microsoft HuggingGPT, CraftJarvis JARVIS-1): "LLM이 컨트롤러, 다른 모델이나 컨트롤러가 실행기"라는 2층 구조. 마스터는 계획하고 배정하고 결과를 종합할 뿐 직접 실행하지 않는다.
2. 오픈소스 개인 비서 Jarvis(ethanplusai, vierisid, adewaskar, Grominet95, OpenJarvis 등): 대부분은 음성과 상시 실행이 핵심이고, 부서 계층을 명시한 것은 vierisid/jarvis(역할 YAML의 ceo-founder 아래 marketing-director, dev-lead)와 소규모 PhillipHamnett 사례 정도다. 검색한 범위에서 별 수가 많은 Jarvis 저장소 대부분은 부서 오케스트레이터가 아니었다.
3. 회사 제품과 실무 글의 "chief of staff" 에이전트(Anthropic cookbook, xAI Grok Bot, 실무자 글): 이름은 Jarvis가 아니어도 같은 역할. "사람 한 명의 주의와 결정을 지키면서 전문 에이전트 여럿을 관리하는 층"이라는 정의가 반복된다.

### 5-2. 반복해서 나온 설계 요소 (출처 표시)

1. 구조화된 위임 단위. HuggingGPT의 task, id, dep, args와 `<resource>-id` 의존 참조, vierisid의 commitment(what, context, priority, deadline, assigned_to, created_from), cookbook의 Task 호출(description, prompt, subagent_type). 하위 에이전트는 사용자 대화를 못 보므로 브리프에 맥락을 다 넣어야 한다는 규칙은 PhillipHamnett 에이전트 파일에 명시되어 있다.
2. 전문가 선택을 설명문 기반 단일 선택으로 푼다. HuggingGPT는 유형으로 거르고 인기순 상위 K개를 프롬프트에 넣고 사유와 함께 고르게 했고, cookbook은 서브에이전트 description을 호출 판단 근거로 쓴다. 후보 설명이 길면 토큰 문제가 생긴다는 점은 HuggingGPT 한계 3번, EasyTool, ethanplusai의 "도구당 매 턴 약 250 토큰" 측정이 모두 가리킨다.
3. 착수 전 계획과 승인. ethanplusai(설계 합의 후 스펙 파일, 계획, 스펙 대비 검토, 실행), cookbook(계획 모드, 계획 파일 저장, 검토 후 실행), JARVIS-1(실행 전 자기 점검으로 선행 조건 검증), Grominet95(미션 단계별 3층 검증).
4. 행동 등급별 승인. vierisid(autonomous_actions와 approval_required를 역할마다 나열, 영향도 read, write, external, destructive, 파괴적 행동은 음성 승인 불가), Grominet95(자율성 0~5), MYJarvis(auto, approve, confirm, block), Sid Bharath(Read, Prepare, Act), Doneyli(3단계 자율과 절대 자동 발송 금지 목록), Amit(L0~L2), adewaskar(기본 읽기 전용). 공통점은 외부로 나가는 것(발송, 게시, 결제, 연락)을 사람 승인 뒤에 둔다는 것이다.
5. 권한은 위에 남고 아래로 새지 않는다. vierisid의 하위 에이전트는 부모 권한 엔진과 오염 상태 아래서 돌고 통제 대상 행동은 아예 거부된다. 역할별 도구 목록으로 범위 제한 레지스트리를 준다. 반례는 ethanplusai로, 하위 run이 권한 확인을 모두 건너뛰는 실행 옵션으로 돈다고 스스로 밝혔다.
6. 외부 입력 오염 차단. ethanplusai(웹, 화면, 다른 세션, MCP 결과를 읽은 턴에는 행동 도구 거부, "reported, never obeyed"), vierisid(taint-gating 파일과 부모 오염 상태 상속). ethanplusai는 이것이 설득까지 막지는 못한다고 한계를 적었다.
7. 상태는 파일이나 DB에 두고 대화에 두지 않는다. ethanplusai(SQLite run 기록, 사실 하나당 Markdown 파일 하나), vierisid(SQLite 지식 그래프, commitments), Byrens(Convex 작업판), Amit("The file system is the bus"), Sid Bharath(JSON이 진실의 원천), JARVIS-1(task, state, plan 궤적 기억), PhillipHamnett(프로필 파일 즉시 갱신), JarvisBench(추가만 가능한 이벤트 버스와 결정 원장).
8. 종료 보장과 루프 방지. ethanplusai(모든 run은 네 종료 상태 중 하나에 반드시 도달), OpenJarvis(같은 호출 3회, 핑퐁 패턴 차단, 최대 턴 10), vierisid(턴당 최대 200회 반복), Grominet95(충돌 후 재개). Grok Bot 해설은 중간 실패 시 재시작 부담을 신뢰 위험으로 꼽았다.
9. 사람의 주의를 관리하는 기능. ethanplusai(사람을 기다리는 세션은 즉시, 끝난 세션은 모아서 알림), JarvisBench(주의 배분을 실행 관리자와 분리된 층으로 정의하고 따로 평가), Grok Bot("only come back when something needs your approval"), thursday(결정이 사용자 몫일 때만 질문).
10. 주기 점검(heartbeat)과 예산. vierisid(역할별 heartbeat, 하위 역할별 과제당 최대 예산 USD), Grominet95(이니셔티브별 최대 비용), Doneyli(규칙 기반 30분 주기와 LLM 일일 주기 분리), Amit(새 데이터 없으면 실행 안 함으로 호출 수 감소).
11. 감사 기록. cookbook(도구 실행 뒤 결정론적 훅으로 보고서 변경 기록), vierisid(전체 감사 기록, 재시작 뒤 미완료 승인 행동은 자동 재실행 금지), Grominet95(변경 불가 감사 기록), ethanplusai(상태 전이는 알림보다 DB 기록이 먼저).

### 5-3. 측정 근거의 수준

- 마스터의 품질을 숫자로 잰 것은 논문 쪽뿐이다. HuggingGPT는 사람 평가에서 계획 통과율 91.22%, 모델 선택 통과율 93.89%인데 최종 성공률은 63.08%였고, 사람 라벨 복잡 요청에서는 GPT-4도 순차 작업 정확도 41.36%였다. TaskBench는 이를 작업 분해, 도구 선택, 인자 예측으로 나눠 재는 틀을 만들었다. OpenJarvis는 로컬 모델로 바꾸면 25~39pp 떨어진다는 수치를 냈다.
- 오픈소스 Jarvis 저장소들은 성능 수치가 없고 테스트 개수 정도만 적었다. 회사 수치(QCI 80%, 40% 단축)는 자사 보도자료이고, 실무자 수치(Doneyli 80% 이상 무수정 발송, Amit 5,760회에서 30~50회)는 각자 환경의 자기 보고다.
- 따라서 "자비스형 마스터가 부서 에이전트를 잘 부린다"는 주장을 뒷받침하는 독립 측정은 이번 조사에서 찾지 못했다. 설계 요소는 반복 확인되지만 효과 크기는 모른다.

### 5-4. 부서형(마케팅/개발/운영) 설계에 옮길 때 눈에 띈 점 (추론)

- 가장 가까운 기존 구현은 vierisid/jarvis의 역할 YAML(책임, 무승인 행동, 승인 필요 행동, KPI, heartbeat, 하위 역할과 예산, 도구, 권한 등급)이다. 부서 에이전트 정의서의 필드 목록으로 그대로 참고할 만하다. 다만 소스 공개형 라이선스라 코드 재사용에는 제약이 있다.
- JarvisBench의 구분처럼, 일을 나눠 주는 실행 관리자와 사람에게 언제 물을지 정하는 주의 관리자를 한 에이전트에 몰지 않는 선택지가 있다.
- 단계별 통과율이 높아도 끝까지 해결되는 비율은 크게 떨어진다는 HuggingGPT 결과는, 부서를 여러 단 거치는 위임일수록 중간 검증 단계가 필요하다는 근거로 읽을 수 있다.

### 5-5. 공급망 위험 요약

- 원격 스크립트를 받아 바로 셸로 실행하는 설치 방식: OpenJarvis, vierisid/jarvis의 기본 또는 대안 설치.
- zip을 받아 macOS 격리 속성을 지우고 바로 여는 설치를 AI 코딩 도구에 붙여 넣게 하는 방식: heardlabs/heard.
- PowerShell 실행 정책을 우회하는 설치: blogminhquy/javis-os.
- 짧은 기간의 급격한 별 증가: jev-chat/jev-chat-jarvis(6일 만에 별 6,772). adewaskar/jarvis도 생성 사흘 사이 별 265, 포크 116 이후 push 없음.
- 별 0~1개 단발 공개 저장소: Jarvis orchestrator 이름을 단 저장소 다수, PhillipHamnett, MYJarvis, Byrens(하드코딩된 외부 백엔드 URL).
- 하위 실행에 전권 부여: ethanplusai(스스로 밝힘), thursday(승인 지점이 코드 강제가 아니라 프롬프트 지시라고 스스로 밝힘).
- 외부 스킬 대량 가져오기: OpenJarvis README가 OpenClaw 커뮤니티 스킬 약 13,700개와 임의의 GitHub 저장소를 가져올 수 있다고 적었다.
