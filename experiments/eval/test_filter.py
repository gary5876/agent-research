"""Smoke test for the Presidio-backed filter (see filters/presidio_filter.py).
Operationalizes 04's ADR-3 consequence: "이번 세션 사건(private key 노출)과 같은
유형의 패턴을 Presidio 커스텀 recognizer로 등록하는 작업이 별도로 필요하다."

For the full swap-and-compare harness across multiple backends and a labeled
corpus, see compare_filters.py instead — this file just checks the one
incident-shaped sample end to end.

Usage:
    source agent-expertise-framework/eval/.venv/bin/activate
    python agent-expertise-framework/eval/test_filter.py
"""

from filters.presidio_filter import PresidioFilter

SYNTHETIC_SAMPLE = """
{
  "type": "service_account",
  "project_id": "example-project-000000",
  "private_key_id": "0000000000000000000000000000000000000000",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIExampleFakeKeyMaterialDoNotUseThisIsNotARealCredential==\\n-----END PRIVATE KEY-----\\n",
  "client_email": "example-service@example-project.iam.gserviceaccount.com"
}
"""


def main() -> None:
    detections = PresidioFilter().scan(SYNTHETIC_SAMPLE)
    if not detections:
        print("FAIL: filter caught nothing — this recognizer would not have blocked this session's incident")
        return
    for d in sorted(detections, key=lambda d: d.entity_type):
        print(f"CAUGHT: {d.entity_type} score={d.score:.2f} span={d.span_preview!r}")


if __name__ == "__main__":
    main()
