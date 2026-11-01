# "페이지니가 찾아올게요" 금융 AI 컨시어지, 페이지니

- URL: https://tech.kakaopay.com/post/kakaopay-hackathon-paygenie/
- 게시일: 2025-08-13
- 저자: ader.error (카카오페이 프론트엔드 개발자 아더). 팀 구성은 채널클랜 PM 하루(haru.achm), 채널클랜 서버 개발자 데이지(daisy.dani), 도리(dory.m), 마이데이터클랜 서버 개발자 그릿(grit.always), 마이데이터클랜 FE 개발자 아더(ader.error)
- 태그: 카페톤, AWS, AI
- 소속: 카카오페이 (2025 카페톤 with AWS 출품작)
- 리뷰어: benny.ahn

## 핵심 한 문장
AWS Bedrock Agents의 Multi-Agent Collaboration(Supervisor 1개 + Worker 2개)으로 "전체 서비스 추천"과 "가맹점 혜택 추천"을 나눠 맡기고, 프롬프트로 도구 호출 순서와 출력 JSON을 강제한 금융 AI 컨시어지.

## 배경과 문제
- 카카오페이는 결제, 송금, 혜택, 자산관리 등 서비스가 너무 많아 "현재 상황에 가장 적합한 서비스를 찾기 어려운 경우가 많았"음.
- 서비스명이 제각각이라 이름만으로 기능을 유추하기 어렵고, 앱을 헤매며 시간을 낭비함.
- 목표: 검색을 넘어서 사용자의 현재 상황(위치, 시간, 이용 기록)을 먼저 파악해 능동적으로 서비스를 제안하는 AI 컨시어지.
- 주요 기능 4개(스크린샷 슬라이드 기준): 상황 기반 말풍선 선제 제안, 음성(STT)/텍스트/추천 질문 입력, 비정형 질문 하나로 여러 서비스와 활용 시나리오 제안, 취향 조건 기반 장소 추천 + 카카오페이 할인/적립 정보.
- 고령층, 디지털 취약 계층을 고려해 TTS 지원(슬라이드 문구).

## 구조와 구성요소
- FE: TypeScript + React, AWS Amplify 배포.
- BE: AWS Lambda 서버리스("Pay Genie Lambda"). STT만 Lambda 쓸 시간이 없어 EC2에 WebSocket 서버를 따로 띄움.
- STT: 브라우저에서 16kHz PCM으로 리샘플링해 WebSocket으로 EC2에 전송, EC2가 Amazon Transcribe와 통신.
- TTS: Lambda가 Amazon Polly(VoiceId "Jihye", Engine "neural", mp3)로 에이전트 텍스트 응답을 음성으로 변환해 base64로 텍스트와 함께 JSON 반환.
- Lambda는 요청 body에서 text, latitude, longitude를 꺼내 `bedrock invoke_agent` 호출. 위경도는 `sessionState.promptSessionAttributes`로 전달. sessionId는 "no-context"(대화 문맥 유지 안 함으로 보임, 원문은 코드만 제시).
- 멀티 에이전트(Bedrock Agents, Multi-Agent Collaboration):
  - Supervisor Agent 1개: Lambda로부터 요청을 받아 수행 가능한 Worker Agent를 선택하고 위임. 응답은 Worker -> Supervisor -> Lambda로 돌아옴.
  - Worker 1 "전체 서비스" 에이전트: Knowledge Base(S3의 서비스 소개 문서, 기획서, 유즈케이스 문서) + Action Group Lambda -> 전체 서비스 RDS.
  - Worker 2 "가맹점(결제) 혜택" 에이전트: Knowledge Base(S3의 가맹점별 사용자 리뷰 데이터) + Action Group Lambda -> 가맹점, 결제 혜택 RDS.
  - 정형 데이터 = RDS 같은 관계형 저장소, 비정형 데이터 = Knowledge Base.
- 모델: 프롬프트에 "당신은 Claude입니다"라고 적혀 있어 Claude 계열로 보임(구체 모델명은 원문에 없음).
- 도구(함수) 이름: `fetch_menu_by_code`, `fetch_all_menus`, `generate_service_response`.
- Knowledge Base 구성 요령:
  - 전체 서비스: 사용자는 입력창에 "자신의 상황, 자신의 문제"를 쓸 것이라 보고, 이것이 기획자의 페르소나와 유즈케이스와 비슷하다고 판단. 서비스 소개 + 페르소나 + 유즈케이스를 서비스별 파일로 묶고, 각 파일에 서비스 식별자를 넣음.
  - 가맹점 혜택: 사용자는 원하는 가맹점 "조건"을 제시할 것이고 이를 가장 잘 담는 것은 다른 사용자 리뷰라고 보고, 가맹점 기본 정보 + 리뷰를 가맹점별 파일로 묶고, 각 파일에 가맹점 식별자 혹은 카테고리를 넣음.
- Bedrock Agent 선택 이유: LangChain 등은 플로우, KB 조회, Function Calling을 코드로 설정해야 하고 KB 파이프라인과 배포도 따로 구성해야 하지만, Bedrock Agent는 기능부터 인프라까지 통합 환경으로 제공해 빠르게 구성 가능.

## 절차와 규칙
- 전체 서비스 에이전트 동작: (1) RAG로 가장 적합한 서비스 식별자 조회 (2) 그 식별자로 Lambda Function 호출해 정형 정보 조회.
- 가맹점 혜택 에이전트 동작: 입력 특성에 따라 분기하는 "더 명확한 프롬프트" 제공.
  - KB 조회 필요 시: RAG로 가맹점 식별자/카테고리 조회 후 Lambda Function으로 정형 정보 조회.
  - KB 조회 불필요 시: RAG를 쓰지 않도록 프롬프트로 제어하고, 위치 정보나 카테고리로 바로 Lambda Function 호출.
- 프롬프트 엔지니어링 4가지 기법(원문 소제목 그대로):
  1. 명확한 역할(Persona) 부여와 행동 원칙 수립: "추론과 함수 호출, 그리고 Lambda 응답을 정확히 중계"하는 역할로 한정, 설명 금지.
  2. 단계별 목표 제시로 논리적 흐름 제어: menu_code 1개 선택 + description 생성 -> 연관 서비스 코드 2~3개 + 설명 생성 -> generate_service_response 호출 -> 결과를 가공 없이 `<answer>` 태그 안에 JSON만.
  3. 조건부 규칙으로 효율성 극대화: KB 검색 우선, menu_code가 명확하면 fetch_menu_by_code, 불명확하거나 KB에 없을 때만 fetch_all_menus. generate_service_response에 쓰는 menu_code는 반드시 fetch_all_menus 결과에 존재해야 함(허구 코드 방지 규칙).
  4. Few-shot 예시 제공 및 엄격한 출력 형식 강제: 함수 호출 이후 `<thinking>`이나 reasoning 재출력 금지, 결과 수정/요약/재구성 금지, `<answer>` 밖 출력 금지, Markdown/자연어 요약 금지, JSON 키 이름/구조 변경 금지. 출력 JSON 스키마 예시(title, description, items{service_name, description, button{text,url}, icon_url}, related_services[]).
- STT 발화 종료 판정: 클라이언트 무음 감지는 구현할 게 많아서, "Transcribe가 변환한 문자가 일정 시간 비어 있으면 발화 종료"로 보고 서버가 `SPEECH_END` 이벤트를 소켓으로 보내면 클라이언트가 스트리밍 중지. 음성 조각 전송 주기 timeSlice 800ms(훅 기본값 500ms).

## 수치와 결과
- Supervisor Agent 1개, Worker Agent 2개.
- 연관 서비스 코드 2~3개 생성 규칙.
- Amazon Transcribe 지원 샘플레이트 16kHz~48kHz(일반 전화 녹음은 8kHz), 16kHz로 리샘플링.
- ScriptProcessor 버퍼 4096, timeSlice 800ms.
- 정확도, 지연 시간, 비용 등 성능 수치는 원문에 없음.

## 실패, 한계, 주의점
- "여러 Woker 에이전트와 이들을 지휘하는 Supervisor 에이전트 구조에서는 원하는 응답을 안정적으로 얻는 것이 쉽지 않았습니다."
- Supervisor 때문에 응답이 느려질 수 있는 점이 단점으로 작용.
- 매번 전체 메뉴 DB 조회는 응답 속도와 비용 측면에서 비효율적이었음 -> 조건부 규칙으로 해결.
- `<thinking>` 태그가 반복 동작하며 단순 질문의 응답 정확도가 떨어짐 -> 특정 함수 호출 뒤 추론 중지 명시로 해결.
- STT: 음성은 녹음되어 전달되는데 변환이 안 되는 현상(샘플레이트 불일치)이 있었음, 언제까지 음성을 보낼지 결정하는 문제.
- STT는 시간 부족으로 Lambda 대신 EC2 별도 서버.
- "짧은 기간 때문에 더 깊게 파보지 못한 아쉬움", 팀원 dory.m: "실제 프로덕트에 미치진 못하겠지만".

## 그림 설명
- 01~04: 서비스 기능 소개 슬라이드(앱 화면 목업). 03은 "교통카드 금액이 갑자기 빠져나갔는데, 내가 언제 탔어? 나 돈 없어ㅠㅠ" 입력에 "적합한 서비스(교통카드 이용내역)"와 "추천 서비스(모바일 교통카드, 후불관리)"를 이유와 함께 보여주고, TTS가 "고령층, 디지털 취약 계층인 시니어 세그를 고려한 설계"라고 적힘. 나머지도 같은 성격의 UI 슬라이드.
- 05 전체 시스템 다이어그램: User -> Amplify -> Pay Genie Lambda -> Supervisor Agent. Supervisor 아래 두 박스 "전체 서비스 Agent"(Bedrock Agent -> 전체 서비스 Action Group Lambda -> 전체 서비스 RDS, Bedrock Agent -> 전체 서비스 Knowledge Base <- 전체 서비스 소개 S3 <- 서비스 소개 문서)와 "가맹점, 결제 혜택 Agent"(Bedrock Agent -> 가맹점, 결제 혜택 Action Group Lambda -> RDS, Knowledge Base <- 가맹점 리뷰 S3 <- 가맹점 별 사용자 리뷰 데이터). 별도 "Speech-To-Text" 박스(WebSocket EC2 <-> Amazon Transcribe)가 Amplify와 양방향 연결. Lambda에서 "Text-To-Speech"(Amazon Polly)로 분기.
- 06: 05의 왼쪽(User, Amplify, STT, Lambda, Supervisor) 확대.
- 07: Multi-Agent Collaboration 부분 확대(Supervisor와 두 Worker 박스).
- 08: Lambda -> Amazon Polly TTS 부분 확대.
- 09 전체서비스 에이전트 다이어그램: 전체 서비스 에이전트 -> 전체 서비스 Lambda -> 전체 서비스 DB, 에이전트 -> 전체 서비스 Knowledge Base <- "기획서, 유즈케이스 문서"(S3).
- 10 가맹점 혜택 에이전트 다이어그램: 가맹점 혜택 에이전트 -> 가맹점 혜택 Lambda -> 가맹점 혜택 DB, 에이전트 -> 가맹점 혜택 Knowledge Base <- 가맹점 리뷰 데이터(S3).

## 원문 인용
1. "크게 Supervisor Agent 1개와 Worker Agent 2개로 구성했습니다. 이를 Multi-agent Collaboration 방식이라고 합니다."
2. "Supervisor Agent는 Lambda로부터 요청을 받고, 해당 요청을 수행할 수 있는 Worker Agent를 선택합니다."
3. "Agent를 활용하는 이 모든 과정은 프롬프트로 제어할 수 있습니다."
4. "각 부서별로 Worker Agent를 개발하면, 이것이 페이지니 Supervisor Agent에 연동되어 적절한 응답을 제공하고, 이를 통해 사용자의 맥락에 가장 알맞은 페이로운 응답을 제공할 수 있는 구조를 생각했습니다."
5. "Supervisor Agent에 의해 답변 응답이 느려질 수 있는 부분이 단점으로 작용하기도 했는데요. 궁극적으로는 Supervisor 에이전트가 적절한 Worker 에이전트 여러 개를 호출하고 이들의 응답을 조합하는 등 더 발전된 형태도 고려한다는 측면에서 Multi-Agent 구조를 채택했습니다."
6. "Bedrock Agent는 에이전트의 기능적인 부분부터 인프라적인 부분까지 모두 통합 환경으로 제공해 줍니다."
7. "기본적인 서비스 소개와 더불어 페르소나와 유즈케이스를 각 서비스별 파일로 묶어 Knowledge Base를 구성했습니다."
8. "여러 Woker 에이전트와 이들을 지휘하는 Supervisor 에이전트 구조에서는 원하는 응답을 안정적으로 얻는 것이 쉽지 않았습니다."
9. "당신은 Claude입니다. 당신의 역할은 추론과 함수 호출, 그리고 Lambda 응답을 정확히 중계하는 것입니다."
10. "bedrock이 따라야 할 생각의 순서를 정하여 이전보다 안정적으로 최종 목표인 정해진 함수 호출까지 유도할 수 있었습니다."
11. "generate_service_response 호출 시 사용되는 모든 menu_code는 반드시 fetch_all_menus 결과에 존재하는 코드여야 합니다."
12. "매번 전체 메뉴 DB를 조회하는 것은 응답 속도와 비용 측면에서 매우 비효율적이었습니다."
13. "특히 <thinking> 태그가 반복적으로 동작하며 단순한 질문에 대한 응답 정확도가 떨어지는 문제가 있었는데요, 특정 함수 호출 이후에는 추론을 멈추도록 명시하여 이를 해결했습니다."

## 우리 설계에 쓸 만한 점
- [추론] 부서(마케팅/개발/운영)마다 Worker 에이전트를 따로 만들고 Supervisor 하나에 "연동"하는 구조는 페이지니가 명시한 확장 의도(부서별 Worker)와 그대로 겹친다.
- [추론] Worker마다 "비정형 지식(KB) + 정형 조회 도구(Lambda->DB)" 한 쌍을 주는 패턴을 부서 에이전트 기본 템플릿으로 쓸 수 있다.
- [추론] Supervisor 추가로 지연이 생긴다는 점을 저자들도 인정했으므로, 단일 부서로 명확한 요청은 라우터를 건너뛰는 경로를 두는 것을 검토할 만하다.
- [추론] "KB 먼저, 식별자 명확하면 단건 조회, 불명확할 때만 전체 조회" 같은 조건부 도구 순서를 프롬프트에 명시하면 비용과 속도를 줄일 수 있다.
- [추론] "출력에 쓰는 ID는 반드시 조회 결과에 존재해야 한다"는 규칙은 에이전트가 없는 항목을 지어내는 것을 막는 가드레일로 옮겨 쓸 수 있다.
- [추론] Worker 출력은 정해진 JSON 스키마 + `<answer>` 태그로 고정하고 Supervisor가 재가공하지 못하게 하면 부서 간 결과 조합이 안정적일 것이다.
- [추론] 도구 호출 후 추론을 멈추게 하는 규칙은 단순 요청에서 과잉 추론으로 정확도가 떨어지는 문제에 대한 실제 대응 사례다.
- [추론] KB 문서를 "사용자가 입력할 법한 형태"(페르소나, 유즈케이스, 리뷰)로 구성해 유사도 검색 적중률을 높인 방법은 부서별 지식베이스 설계에 참고할 만하다.
- [추론] 평가 지표나 수치가 전혀 없으므로, 이 구조를 따를 경우 라우팅 정확도와 지연 시간 측정은 우리가 별도로 설계해야 한다.
