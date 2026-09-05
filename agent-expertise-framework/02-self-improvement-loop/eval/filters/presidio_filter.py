"""Presidio-backed ResponseFilter — regex pattern recognizers (custom PEM key
recognizer, ADR-3) plus spaCy NER-based builtin recognizers (EMAIL_ADDRESS, etc.)."""

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider

from .base import Detection, ResponseFilter

PEM_PRIVATE_KEY_PATTERN = Pattern(
    name="pem_private_key_pattern",
    regex=r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC |DSA )?PRIVATE KEY-----",
    score=1.0,
)

AWS_ACCESS_KEY_PATTERN = Pattern(
    name="aws_access_key_pattern",
    regex=r"\bAKIA[0-9A-Z]{16}\b",
    score=1.0,
)


class PresidioFilter(ResponseFilter):
    name = "presidio (regex + spaCy NER)"

    def __init__(self) -> None:
        provider = NlpEngineProvider(
            nlp_configuration={
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
            }
        )
        self._analyzer = AnalyzerEngine(nlp_engine=provider.create_engine(), supported_languages=["en"])
        self._analyzer.registry.add_recognizer(
            PatternRecognizer(supported_entity="PEM_PRIVATE_KEY", patterns=[PEM_PRIVATE_KEY_PATTERN])
        )
        self._analyzer.registry.add_recognizer(
            PatternRecognizer(supported_entity="AWS_ACCESS_KEY", patterns=[AWS_ACCESS_KEY_PATTERN])
        )

    def scan(self, text: str) -> list[Detection]:
        results = self._analyzer.analyze(
            text=text,
            entities=["PEM_PRIVATE_KEY", "AWS_ACCESS_KEY", "EMAIL_ADDRESS"],
            language="en",
        )
        detections = []
        for r in results:
            span = text[r.start : r.end]
            preview = span if len(span) <= 40 else span[:40] + "..."
            detections.append(Detection(entity_type=r.entity_type, score=r.score, span_preview=preview))
        return detections
