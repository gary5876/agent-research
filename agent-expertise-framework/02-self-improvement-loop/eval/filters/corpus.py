"""Synthetic (fake, no real secrets) test corpus for comparing ResponseFilter
backends. Each case states expected_entities as ground truth so recall is
measurable, not eyeballed."""

from dataclasses import dataclass, field


@dataclass
class Case:
    case_id: str
    text: str
    expected_entities: set[str] = field(default_factory=set)


CASES: list[Case] = [
    Case(
        case_id="pem_key_and_email",
        text=(
            '{"type": "service_account", "private_key": '
            '"-----BEGIN PRIVATE KEY-----\\nMIIExampleFakeKeyMaterialDoNotUse==\\n-----END PRIVATE KEY-----\\n", '
            '"client_email": "example-service@example-project.iam.gserviceaccount.com"}'
        ),
        expected_entities={"PEM_PRIVATE_KEY", "EMAIL_ADDRESS"},
    ),
    Case(
        case_id="aws_access_key",
        text="export AWS_ACCESS_KEY_ID=AKIAFAKEEXAMPLE12345 # do not commit this",
        expected_entities={"AWS_ACCESS_KEY"},
    ),
    Case(
        case_id="email_only",
        text="문의사항 있으면 support@example.com 으로 연락해주세요.",
        expected_entities={"EMAIL_ADDRESS"},
    ),
    Case(
        case_id="benign_english",
        text="The grounding metric checks whether each claim's evidence line range still exists.",
        expected_entities=set(),
    ),
    Case(
        case_id="benign_korean",
        text="이 문서는 4요소 각각의 목적과 성공 기준을 표로 정리한다.",
        expected_entities=set(),
    ),
]
