"""Common interface so filter backends can be swapped without changing the
comparison harness (compare_filters.py). This is the "레퍼런스 갈아끼워가면서
테스트" mechanism for the "안전한 응답 필터" element (04 §1 / ADR-3).

Only two backends are actually wired up here (presidio_filter.py, a real
Presidio-based filter; baseline_filter.py, a dependency-free regex filter used
as a comparison floor). NeMo Guardrails, PurpleLlama (Llama Guard/Prompt Guard),
Guardrails AI, and Portkey-AI/gateway are documented as further ResponseFilter
implementations in ../README.md but not installed here — each needs either a
local/hosted LLM backend, a GPU-sized model download, or a proxy API key, which
this environment doesn't have. Wiring one in means implementing this same
interface, not changing the harness.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Detection:
    entity_type: str
    score: float
    span_preview: str


class ResponseFilter(ABC):
    name: str

    @abstractmethod
    def scan(self, text: str) -> list[Detection]:
        """Return every sensitive span this backend finds in `text`."""
