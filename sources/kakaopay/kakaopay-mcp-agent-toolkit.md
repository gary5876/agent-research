# AI 에이전트와 카카오페이 결제 오픈 API 연동하기: MCP Agent Toolkit 개발기

- URL: https://tech.kakaopay.com/post/kakaopay-mcp-agent-toolkit/
- 게시일: 2025-08-06
- 저자: lee.jj (카카오페이 결제기술파티 개발자 "리")
- 태그: BE, MCP, AI, LLM
- 소속: 카카오페이

## 핵심 한 문장
카카오페이 결제 Open API를 결제/정기결제 8개 MCP Tool로 감싸고, 같은 Tool 정의를 MCP 서버, LangChain, Vercel AI SDK, OpenAI function calling에서 모두 쓸 수 있는 Agent Toolkit으로 만들었다.

## 배경과 문제
- function calling 등장으로 "AI가 결제도 처리할 수 있을까?"라는 질문이 늘어남.
- PayPal, Stripe가 이미 AI Agent Toolkit과 MCP Server를 출시해 결제, 배송 추적, 반품 처리 자동화를 지원.
- 처음엔 OpenAI function calling이나 LangChain tool로 직접 연동하려 했으나 두 가지 문제:
  - 프레임워크 종속성: 특정 AI 프레임워크에 의존하면 다른 도구와 호환성 문제
  - 확장성 한계: 새 AI 도구나 프레임워크가 나올 때마다 별도 구현 필요
- 그래서 MCP 선택. 이유: 프레임워크 독립성(Claude Desktop, Cursor, Windsurf 등 MCP 호스트에서 사용), 확장성(새 도구/프레임워크 추가 용이).

## 구조와 구성요소
전체 구조 (원문 ASCII 도식):
```
AI Agent (Claude/GPT)  <->  MCP Server (Agent Toolkit)  <->  KakaoPay API (Open API)
```

Tool 정의 필드 (원문 그대로):
- method: Tool을 식별하는 고유한 이름
- name: 사람이 읽기 쉬운 Tool 이름
- description: Tool의 기능 설명
- parameters: 입력값 정의 (Zod 스키마)
- actions: Tool의 권한 및 사용 가능한 액션 정의
- execution: 실제 기능 함수(내부적으로 MCP 서버에서 호출)

Tool 목록 8개:
- 결제: demo_payment(데모 결제 링크 생성), ready_payment(결제 준비), approve_payment(승인), get_payment(상태 조회), cancel_payment(취소)
- 정기결제: request_subscription(요청), get_subscription(상태 조회), inactive_subscription(비활성화)

get_payment 예시 코드 요지: `tid`(결제 고유번호)만 사용자 입력 파라미터(Zod, `.describe('결제 고유번호')`), `cid`(가맹점 코드)는 context에서 주입. `actions: { payment: { get: true } }`로 권한 표시. description은 "이 도구는 카카오페이 주문 상태를 조회합니다."

핵심 컴포넌트 (디렉터리 단위):
- MCP Server (modelcontextprotocol/): 카카오페이 API와 AI 에이전트 간 중계
- Shared Core (shared/): 모든 프레임워크 공통 모듈
  - API Client (client.ts): Open API HTTP 통신
  - API Handler (api.ts): MCP 메서드 호출을 카카오페이 API 요청으로 변환
  - Configuration (configuration.ts): 화이트리스트 기반 도구 필터링 및 권한 관리
  - Tools Registry (tools.ts): 모든 결제 도구 등록/관리
  - Payment Tools (shared/payment/), Subscription Tools (shared/subscription/)
- Framework Integrations: LangChain, OpenAI, AI SDK별 모듈

설정 방식: `new KakaoPayAgentToolkit({ secretKey, configuration: { context: { cid: 'TC0ONETIME' }, actions: { payment: { demo: true } } } })` 후 `getTools()`로 각 프레임워크에 전달. LangChain은 `createReactAgent`(gpt-4o), Vercel AI SDK는 `generateText({ maxSteps: 10 })`, OpenAI는 `chat.completions.create({ tools })`.

MCP 호스트 설정: `npx -y @kakaopay-develop/mcp --tools=all --cid=TC0ONETIME`, 환경변수 `KAKAOPAY_SECRET_KEY`.

챗봇 예제: Next.js + Vercel AI SDK(useChat 훅) + Agent Toolkit, 카카오페이 페이봇 스타일 UI. system 메시지 "카카오페이 결제 도우미입니다. 결제 링크 생성, 상태 조회, 취소 등을 도와드립니다."

배포물: npm `@kakaopay-develop/agent-toolkit`(TypeScript 프레임워크 연동 라이브러리), `@kakaopay-develop/mcp`(MCP 서버), GitHub 저장소, 개발자센터 AI 연동 가이드.

## 절차와 규칙
동작 플로우 ("커피 5000원짜리 결제 링크 만들어줘"):
1. 사용자 요청 분석 및 파라미터 추출: LLM이 의도를 "결제 링크 생성"으로 파악, demo_payment 호출 결정, item_name "커피", total_amount 5000 추출
2. MCP 프로토콜 통신: Tool 호출 요청이 MCP 서버로 전달
3. 카카오페이 API 호출: MCP 서버가 파라미터를 Open API 형식으로 변환해 요청
4. 결과 반환: 결제 링크와 TID를 LLM에 전달, LLM이 안내 메시지로 응답

개발 단계 (원문):
- 1단계: API 전체 검토 및 활용성 평가
- 2단계: MCP Tool 구조 설계 및 구현
- 3단계: 프레임워크별 연동 모듈 개발
- 4단계: 실제 챗봇 예제 구현

규칙: 사람이 설계할 것 3가지. 어떤 API를 AI가 호출할 수 있는지, 어떤 제한사항을 둘 것인지, 어떻게 안정적으로 운영할 것인지. 도구 노출 범위는 configuration의 화이트리스트(actions)로 제한.

## 수치와 결과
- Tool 8개 (결제 5, 정기결제 3)
- Vercel AI SDK 예시 maxSteps: 10
- 데모 예시 금액 5000원, 3000원(장난감)
- 성능, 사용량 등 운영 수치는 원문에 없음

## 실패, 한계, 주의점
- "현재의 카카오페이 MCP는 기존 결제 플로우를 기반으로 하고 있어, AI 에이전트 환경에서는 일부 한계가 있습니다." 구체적 한계 내용은 원문에 없음.
- 향후 계획: AI 에이전트 전용 결제 플로우, Python SDK, AWS Bedrock 등 프레임워크 확장, 더 직관적인 Tool 인터페이스, 문서화.
- 데모 링크는 실제 결제가 이루어지지 않음(대화 예시 안내문).

## 그림 설명
- 그림 1 (Cursor 화면): "커피 결제 링크 생성 요청" 대화. 사용자 "5000원짜리 커피 PC 결제 링크 생성해 줘" 입력, Thought 5s 후 "Called demo_payment" 체크 표시, Thought 2s 후 상품명/금액/TID/PC 결제 링크를 정리해 응답. 도구 호출 1회로 끝나는 흐름을 보여줌.
- 그림 2 (페이 MCP 챗봇 UI): 상단 추천 버튼(카카오페이로 결제하기 / 결제 상태 확인하기 / 취소하기). 커피 모바일, 커피 PC, 장난감 3000원 PC 링크 생성 후 "모든 결제 상태 확인해 줘"로 3건 상태 조회(READY, AUTH_PASSWORD(비밀번호 인증 대기) 등, 총액, 부가세 455원/273원, 생성일시 2025-07-06). 다시 조회하면 장난감이 SUCCESS_PAYMENT로 바뀌고 승인일시 표시. "장난감 결제 취소해 줘"에 CANCEL_PAYMENT, 취소일시, "취소 가능한 금액은 이제 0원" 응답. 여러 건의 상태를 대화 맥락(방금 만든 것들)으로 추적하는 모습.

## 원문 인용
- "프레임워크 종속성: 특정 AI 프레임워크에 의존하면 다른 도구와의 호환성 문제"
- "확장성 한계: 새로운 AI 도구나 프레임워크가 등장할 때마다 별도 구현 필요"
- "MCP의 핵심은 AI가 실행할 수 있는 기능들을 ‘Tool’이라는 단위로 정의하고 관리하는 것입니다."
- "actions: Tool의 권한 및 사용 가능한 액션 정의"
- "Configuration (configuration.ts): 화이트리스트 기반 도구 필터링 및 권한 관리"
- "이 Tool은 사용자에게 입력받은 tid(결제 고유번호)와 context로 설정한 cid(가맹점 코드)를 사용하여 해당 결제의 상세한 상태 정보를 반환합니다."
- "이러한 플로우를 통해 복잡한 결제 API 연동 과정이 사용자에게는 단순한 자연어 대화로 추상화됩니다."
- "가장 큰 깨달음은 “사람이 AI를 도구로 활용한다”는 점이었습니다. AI가 결제 API를 호출할 수 있게 되었다고 해서, 결제 시스템의 핵심 로직이나 비즈니스 규칙이 바뀌는 것은 아닙니다."
- "중요한 것은 여전히 사람이 설계하고 구현해야 한다는 점입니다"
- "현재의 카카오페이 MCP는 기존 결제 플로우를 기반으로 하고 있어, AI 에이전트 환경에서는 일부 한계가 있습니다."

## 우리 설계에 쓸 만한 점
- [추론] 부서 에이전트(마케팅/개발/운영)가 쓰는 도구를 특정 프레임워크 함수가 아니라 MCP Tool 단위로 정의하면 오케스트레이터나 LLM 교체 시 도구를 재작성하지 않아도 된다.
- [추론] Tool 정의에 method/name/description/parameters(스키마)/actions(권한)/execute를 고정 필드로 두는 형식을 그대로 도구 레지스트리 스키마로 쓸 수 있다.
- [추론] actions 화이트리스트처럼 부서별 에이전트에 허용 도구만 노출하는 설정 계층(configuration)을 두면, 예를 들어 마케팅 에이전트는 조회만, 운영 에이전트는 취소 권한까지 같은 식으로 권한을 분리할 수 있다.
- [추론] cid처럼 LLM이 추출하면 안 되는 값(계정, 테넌트, 비밀키)은 context로 주입하고 LLM에는 사용자 의도 파라미터만 맡기는 분리가 안전하다.
- [추론] 조회(get)와 변경(cancel, approve) 도구를 분리해 두면 검수(inspection) 역할이나 사람 승인 단계를 변경 도구 앞에만 걸 수 있다. 원문은 승인 게이트를 언급하지 않았으므로 우리 쪽 추가 설계다.
- [추론] "어떤 API를 호출할 수 있는지, 어떤 제한을 둘지, 어떻게 운영할지는 사람이 설계"라는 원칙을 오케스트레이터 설계 문서의 고정 원칙으로 둘 수 있다.
- [추론] demo_payment처럼 실제 부작용 없는 데모/샌드박스 도구를 먼저 제공하는 방식은 새 에이전트를 운영 투입 전에 검증하는 단계로 쓸 만하다.
- [추론] maxSteps 같은 에이전트 루프 상한을 명시적으로 두는 것은 모니터링 역할의 비용/폭주 방지 규칙으로 옮길 수 있다.
