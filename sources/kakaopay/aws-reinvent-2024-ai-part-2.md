# AWS re:Invent 2024 Recap: AI 2편

- URL: https://tech.kakaopay.com/post/aws-reinvent-2024-ai-part-2/
- 게시일: 2025-02-18
- 저자: jay.pg (제이)
- 태그: AWS re:Invent, Amazon SageMaker, Amazon Bedrock
- 소속: 카카오페이 머니코어서비스파티 서버개발자(본문 표기). 저자 소개란에는 "머니코어제휴파티".

## 읽기 전 주의: 이 글은 AWS 제품 업데이트 요약이다
- 본문 전체가 CEO Matt Garman, Dr. Swami Sivasubramanian 키노트에서 발표된 SageMaker, Bedrock 신기능 소개다. 수치(75% 비용 절감, 90% 이용률 등)는 모두 AWS 발표 수치다.
- 카카오페이 자체 실무 서술은 마지막 문장뿐: "저희 카카오페이도 더 나은 사용자 경험을 제공하기 위해 금융 전문가 AI 서비스를 개발하고 제공하고 있는데요." 어떤 기능을 도입했는지는 원문에 없음.
- 저자 의견 문장("~좋은 전략일 것입니다" 등)은 [저자 해석]으로 표시.

## 핵심 한 문장
SageMaker(전문가용 학습/배포 환경)와 Bedrock(API 기반 추론 서비스)의 re:Invent 2024 신기능을 인프라 관리, 비용/지연/정확도 최적화, 데이터 커스터마이징(RAG), 책임감 있는 AI(환각 검증, 유해 콘텐츠 차단) 네 축으로 요약한 글.

## 배경과 문제 (AWS 발표 요약)
- 머신러닝 5단계(데이터 수집, 클러스터 생성, 분산 모델 학습, 튜닝 및 최적화, 성능 조정)가 모두 어렵고, 수십~수백억 파라미터를 최소 몇 주 학습, 수시로 중단해 수렴 검사, 하드웨어 장애 시 직접 교정 필요.
- 여러 region과 AZ를 돌며 유휴 자원 확보 경쟁, 부서 간 자원 배분 조율 필요.
- 서드파티 AI 개발 도구(comet, deepchecks, fiddler, lakera) 도입 시 배포, 데이터 거버넌스, 보안, 컴플라이언스, VPC 외부 노출 방지 부담.
- 서비스 운영 시 지연, 정확도, 비용 균형이 필요. 생성형 AI 단점: 학습 데이터 편향, 확률적 비일관성, 사실관계 오류, 윤리 문제.

## 구조와 구성요소 (AWS 발표 요약)
SageMaker:
- Hyperpod flexible training plans: 컴퓨팅 요구량과 학습 시간대를 입력하면 자원 자동 관리. 용량 확보 수동 작업 제거, 클러스터 자동 생성, 예산과 시간제한 보장.
- Hyperpod task governance: 부서 간 자원 할당 조율, 유휴 자원 능동 재할당, 높은 중요도 task 우선, 실시간 사용량 모니터링.
- 파트너 AI 앱 내재화(comet, deepchecks, fiddler, lakera).
- 그 외 SageMaker Lakehouse, Unified Studio.

Bedrock:
- Marketplace: 100가지 이상 모델, Amazon Nova, Poolside AI, Stable diffusion, Luma AI.
- Model distillation: 소형 모델 생성.
- Prompt Caching: 유사 프롬프트 처리 시 문서를 캐싱해 재사용.
- Intelligent Prompt Routing: 프롬프트별 모델 성능 예측 후 비용과 품질 최적 조합으로 라우팅.
- Knowledge Bases: RAG 워크플로 관리. 신규 structured data retrieval(SageMaker Lakehouse, Redshift, S3 Tables에 쿼리 자동 생성), GraphRAG(knowledge graph 자동 생성).
- data automation: 비정형 문서 ETL 자동화(분할/분류 → 데이터 추출 → 변환/정규화, 문서 유형별 스키마로 JSON 산출). 결과에 confidence score, grounding 같은 검증 값 동봉.
- Guardrails: 유해 콘텐츠 차단. 신규 Automated Reasoning checks(생성 답변을 자동 추론 정책으로 검증, 실패 시 재생성, 검증된 답변만 전달), Multimodal toxicity detection(이미지 safeguard).

## 절차와 규칙 (AWS 발표 요약)
- Automated Reasoning checks 흐름(그림 14): User → Prompt → Generate response → Validate against automated reasoning policy → 통과 시 Verified output, 실패 시 Receive feedback 후 Regenerates response.
- Prompt Routing: 간단한 질문은 간단한 모델, 복잡한 질문은 복잡한 모델. 직접 N개 복잡도 x K개 모델로 최적화하면 정책 변경 시 처음부터 다시 검증해야 하는 문제를 자동화로 해결.
- [저자 해석] 소형 모델은 정확도가 떨어질 수 있으므로 RAG로 보강하는 전략이 좋을 것.
- [저자 해석] SageMaker와 Bedrock을 함께 쓰면 모델 개발부터 서비스 통합까지 원활.

## 수치와 결과 (모두 AWS 발표 수치)
- SageMaker: 2023년 이후 140개 이상 기능 추가, 2017년부터 운영.
- task governance: AWS 내부 전체 자원 이용률 90%까지.
- Model distillation: 최대 5배 빠른 응답, 75% 비용 절감.
- Prompt Caching: 응답 시간 85%, 비용 90%까지 절감.
- Intelligent Prompt Routing: 정확도 유지하며 최대 30% 비용 절감(정적이거나 극히 전문적인 사례 제외).
- Guardrails: 85% 이상 유해 콘텐츠 방지.
- 인프라: Graviton 4, Trainium 2, 10p10u(10 petabits under 10 ms) 네트워크.
- 카카오페이 자체 수치는 원문에 없음.

## 실패, 한계, 주의점
- Intelligent Prompt Routing은 "정적이거나 극히 전문적인 사례 등이 아니라면" 정확도 유지라는 조건부 서술.
- 자동 ETL(data automation)의 가장 큰 우려는 환각. confidence score, grounding으로 대응했다고 설명.
- 환각은 의료 진단, 금융 거래처럼 중요한 결정을 내리는 시스템에 치명적이라고 명시.
- 머신러닝은 여전히 전문 인력과 시간이 많이 필요하므로 전문가가 없으면 Bedrock을 고려하라는 권고.

## 그림 설명
- 그림 1, 2, 4~7, 9~12, 15: 키노트 제품 소개 슬라이드(SageMaker, flexible training plans, 파트너 앱, Marketplace, distillation, Prompt Caching, RAG 예시, Knowledge Bases, structured retrieval, GraphRAG, Multimodal toxicity). 보지 않음. 본문 설명과 중복되는 제품 슬라이드로 판단.
- 그림 3: HyperPod task governance 키노트 화면. 인스턴스 100, 실행 99, Pending recovery 1, GPU/GPU memory/vCPU utilization 게이지 82%, 81%, 83% 등 사용률 대시보드.
- 그림 8: Intelligent Prompt Routing 예시 "Travel planner". 짧은 질문과 긴 일정 요청이 API → Prompt routing을 거쳐 Model A 또는 Model C로 분기.
- 그림 13: Intelligent document processing. 1 Splitting and classifying, 2 Extracting data, 3 Transformation and normalization. 대출 신청서, W-2, 은행 거래내역을 문서 유형별 스키마(Employee info, Federal tax info 등)로 변환해 관계형 DB에 넣을 JSON 산출.
- 그림 14: Automated Reasoning checks 흐름(위 절차 설명 참고).

## 원문 인용
1. "Amazon SageMaker : AI 모델을 훈련, 배포하는 데에 필요한 통합 환경을 제공하는 전문가용 머신 러닝 환경입니다."
2. "진행 중인 훈련을 수시로 중단하고 모델이 잘 수렴하고 있는지 검사해야 하며, 이 와중에 하드웨어 장애라도 발생하면 문제가 생긴 부분을 직접 일일이 교정해야 하므로 무척 번거로운 작업입니다."
3. "부서 간 자원 할당을 조율해 주고, 유휴 자원을 필요한 부서에게 능동적으로 할당해 주는 등 컴퓨팅 자원의 이용률을 끌어올립니다."
4. "실제로 AI 기반 서비스를 운영하기 위해서는 지연속도, 정확도, 비용 등 여러 측면에서 균형을 잡는 것이 중요합니다."
5. "소형 모델을 활용하면 정확도가 떨어질 수 있으므로 RAG를 이용하여 정확도를 보강하는 방법 등을 활용하는 것도 좋은 전략일 것입니다."
6. "만약 프롬프트 복잡도를 N개, 모델 K개로 구분하고 최적화 작업을 했는데, 서비스 정책의 변화로 복잡도나 모델의 개수가 변경된다면 처음부터 다시 최적화하고 검증해야 하는 어려움이 있습니다."
7. "이 자동화 과정에서 가장 우려되는 것은 환각(Hallucination)의 발생 가능성인데 콘텐츠에 confidence score, grounding 등 AI 검증 값을 함께 제공하여 해결했으며"
8. "환각은 의료 진단이나 금융 거래와 같은 중요한 결정을 내리는 AI 시스템에 치명적인 문제를 일으킬 수 있습니다."
9. "이제 사용자의 요청에 따라 AI에서 생성한 답을 Automated Reasoning으로 검토하고 검증된 답변만 전달하는 형태의 AI 서비스를 할 수 있게 되었습니다."
10. "저희 카카오페이도 더 나은 사용자 경험을 제공하기 위해 금융 전문가 AI 서비스를 개발하고 제공하고 있는데요."

## 우리 설계에 쓸 만한 점
- [추론] 이 글은 AWS 제품 카탈로그 요약이므로 카카오페이 운영 사례로 인용하지 말 것. 설계 패턴 아이디어의 출처로만 쓴다.
- [추론] "생성 → 정책 검증 → 실패 시 피드백과 함께 재생성 → 검증된 것만 전달"(Automated Reasoning 흐름)은 운영 부서 점검 에이전트의 기본 게이트 패턴이다. 마케팅 문구나 개발 산출물을 규칙 기반 검증기로 통과시킨 뒤에만 다음 단계로 넘긴다.
- [추론] 산출물에 confidence score와 근거(grounding)를 붙이게 하면, 운영 부서는 점수 임계치 미만 건만 사람 승인으로 보내는 식으로 승인 부담을 줄일 수 있다.
- [추론] 프롬프트 라우팅(쉬운 작업은 작은 모델, 어려운 작업은 큰 모델)은 부서별 에이전트 비용 관리 규칙으로 쓸 수 있다. 다만 라우팅 규칙을 손으로 짜면 정책 변경 때 재검증 비용이 크다는 지적을 기억할 것.
- [추론] task governance의 "중요도 높은 작업 우선, 유휴 자원 재할당, 실시간 사용량 모니터링"은 여러 부서 에이전트가 한정된 토큰/실행 예산을 나눠 쓸 때 운영 부서가 맡을 자원 조정 역할의 모델이 된다.
- [추론] 문서 처리의 "분할/분류 → 추출 → 스키마 정규화" 3단계는 입력 자료(기획서, 요청서)를 구조화하는 전처리 에이전트 설계에 쓸 수 있다.
