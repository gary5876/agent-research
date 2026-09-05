"""Dependency-free regex-only filter — the "naive first thing someone writes
after one incident" baseline (ADR-3's original "커스텀 regex" alternative that
was rejected in favor of Presidio+NeMo Guardrails+PurpleLlama+portkey-ai/gateway).
Deliberately only covers what the session's one real incident (PEM private key
exposure) and a textbook email regex would catch — no AWS-key pattern, no NER.
The comparison harness (compare_filters.py) is what makes that gap visible."""

import re

from .base import Detection, ResponseFilter

_PEM_RE = re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC |DSA )?PRIVATE KEY-----")
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


class BaselineRegexFilter(ResponseFilter):
    name = "baseline (regex only, no NER)"

    def scan(self, text: str) -> list[Detection]:
        detections = []
        for match in _PEM_RE.finditer(text):
            span = match.group(0)
            preview = span if len(span) <= 40 else span[:40] + "..."
            detections.append(Detection(entity_type="PEM_PRIVATE_KEY", score=1.0, span_preview=preview))
        for match in _EMAIL_RE.finditer(text):
            span = match.group(0)
            detections.append(Detection(entity_type="EMAIL_ADDRESS", score=1.0, span_preview=span))
        return detections
