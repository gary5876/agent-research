# LLM 친화적 문서 작성 프레임워크

**Status:** ACTIVE

이 세션의 출발점이 된 원본 원칙. "환각이 심해지는 문제"를 문서 설계로 완화하는 방법론이다. 이후 진행한 모든 분석(`../../data-lake/amoro-analysis`, `../../data-lake/iceberg-analysis`, `../../data-lake/paimon-analysis`)이 이 프레임워크를 실제 오픈소스 프로젝트로 검증/보완한 결과다 — 요약은 [01-research-summary.md](01-research-summary.md).

## 핵심 한 문장

> LLM이 문서의 내용을 "추론해서 복원"할 필요가 없도록, 정보의 구조·관계·조건을 명시적으로 적어놓은 문서가 읽기 좋은 문서다.

## 1. 명시성

사람은 "카카오 OAuth로 로그인한다"만 봐도 이해하지만, LLM은 provider·grant type·토큰 발급 위치·회원가입과 로그인 구분·DB 저장값·재로그인 흐름·프론트/백엔드/외부서비스 중 누가 뭘 호출하는지가 다 빠져 있다고 본다. 흐름을 번호 매겨 단계별로, 조건까지 명시해야 한다.

## 2. "무엇"보다 "왜"를 같이 적기

"Redis를 사용한다"보다 "Redis는 세션/임시 상태 저장용이고, 영구 데이터·권한 정보·비즈니스 데이터는 저장하지 않는다. 이유: TTL 만료 가능하므로"처럼 목적과 배제 대상, 이유를 함께 적어야 한다. 그래야 LLM이 "Redis가 있으니 캐싱에 쓰자"처럼 설계와 어긋나는 그럴듯한 판단을 내리지 않는다.

## 3. 현재 상태 vs 목표 상태 분리

문서와 코드가 둘 다 context로 들어가기 때문에, 문서가 미래/과거 상태를 현재처럼 써놓으면 충돌이 생긴다. `현재 구현` / `변경 예정`을 분리하거나 `Status: ACTIVE / DEPRECATED / PLANNED` 같은 상태값을 명시한다.

## 4. 용어집

같은 개념을 User/Member/Account/Student처럼 여러 이름으로 부르면 LLM이 이들을 다른 개념으로 오인한다. 용어 대응표를 만들고, **사용하지 않는 용어까지 명시**한다(예: "Member는 사용 안 함, User 사용").

## 5. 파일 구조는 "목록"이 아니라 "책임"

디렉터리 트리는 LLM이 이미 안다. 대신 "Controller는 HTTP 요청/응답만 담당하고 비즈니스 로직을 넣지 않는다"처럼 계층별 책임과 금지사항을 서술해야 한다.

## 6. "하지 말아야 할 것"을 명시 (Constraints)

"무엇을 할 수 있는가"보다 "무엇을 절대 하면 안 되는가"가 명확할수록 코드 수정이 안정적이다. Architecture Rules / Constraints / Invariants로 별도 분리한다.

## 7. 숫자와 조건은 정확하게

"일정 시간 유지된다"가 아니라 "Access Token TTL 30분, Refresh Token TTL 14일"처럼, 조건 → 기준 → 결과를 구체적 수치로 명시한다.

## 8. 코드-문서-DB-Redis 연결 관계 명시

문서에 관련 코드 파일, 관련 DB 테이블, 관련 캐시 키를 나열해두면 LLM이 문서 → 코드 → 데이터를 따라갈 수 있다.

## 9. 거대한 단일 문서로 만들지 않기

`docs/architecture/`, `docs/domain/`, `docs/api/`, `docs/rules/`, `docs/decisions/`처럼 주제별로 쪼개서, 에이전트가 필요한 부분만 읽을 수 있게 한다.

## 10. ADR (Architecture Decision Record)

"왜 지금 이 구조인가"를 Context/Decision/Alternatives/Consequences로 기록한다. 현재 코드가 왜 이렇게 생겼는지를 설명해주는 문서.

## 11. 문서 계층 구조

```
PROJECT → RULES / ARCHITECTURE / DOMAIN → MODULE → API / DB / CODE
```
각 문서는 필요한 만큼만: Purpose, Scope, Current State, Responsibilities, Dependencies, Rules/Constraints, Inputs/Outputs, Failure Cases, Related Code/DB, Related Documents, Examples, Status.

## 12. 문서만으론 부족하다 — 검증 시스템이 핵심

> "프로젝트를 이해하고 수정해"라고만 시키면 안 된다. Agent가 작업 전에 **검증 가능한 사실을 수집**하게 해야 한다.

```
Task → 관련 문서 검색 → 관련 코드 검색 → 현재 구현 확인
     → 문서와 코드 일치 여부 확인 → 불일치 시 수정 대신 보고
     → 변경 계획 → 코드 수정 → 테스트 → 변경 후 문서/코드 일치 재검증
```

**문서 = LLM에게 프로젝트를 알려주는 지식**, **검증 시스템 = 그 지식을 멋대로 만들어내지 못하게 하는 장치**. 대규모 프로젝트에서 환각을 억제하는 핵심은 결국 "LLM이 모르는 것을 모른다고 말하게 만드는 구조"다.
