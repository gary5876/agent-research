"""DeepEval custom metric operationalizing 04-purpose-and-self-improvement-loop.md
§1's success criterion for the "정합적인 data lake" element:

    "응답의 사실 주장 각각이 특정 소스로 추적 가능한 비율이 100%에 가까워야 함"

Given a claim's evidence resource (an OpenWiki `repo://path#Lstart-Lend` reference),
this checks the referenced file/line range still exists and is non-empty. It is
fully deterministic (no LLM judge call), so it needs no API key.
"""

import os
import re

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RESOURCE_RE = re.compile(r"^repo://(?P<path>[^#]+)#L(?P<start>\d+)-L(?P<end>\d+)$")


class GroundingTraceabilityMetric(BaseMetric):
    def __init__(self, threshold: float = 1.0):
        self.threshold = threshold
        self.async_mode = False
        self.score = 0.0
        self.reason = ""
        self.success = False

    @property
    def __name__(self):
        return "Grounding Traceability"

    def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        resource = test_case.actual_output
        match = RESOURCE_RE.match(resource or "")
        if not match:
            return self._fail(f"evidence resource is not in repo://path#Lstart-Lend format: {resource!r}")

        path = match.group("path")
        start, end = int(match.group("start")), int(match.group("end"))
        full_path = os.path.join(REPO_ROOT, path)

        if not os.path.isfile(full_path):
            return self._fail(f"source file no longer exists: {path}")

        with open(full_path, encoding="utf-8") as f:
            lines = f.readlines()

        if start < 1 or end > len(lines) or start > end:
            return self._fail(f"L{start}-L{end} out of bounds (file has {len(lines)} lines)")

        selected = "".join(lines[start - 1 : end]).strip()
        if not selected:
            return self._fail(f"L{start}-L{end} of {path} is empty")

        self.score = 1.0
        self.reason = f"L{start}-L{end} of {path} exists and is non-empty ({end - start + 1} lines)"
        self.success = True
        return self.score

    def _fail(self, reason: str) -> float:
        self.score = 0.0
        self.reason = reason
        self.success = False
        return self.score

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        return self.measure(test_case, *args, **kwargs)

    def is_successful(self) -> bool:
        return self.success
