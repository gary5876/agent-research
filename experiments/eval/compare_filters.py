"""Runs every registered ResponseFilter backend against the same synthetic
corpus and reports recall + false positives per backend — the "레퍼런스
갈아끼워가면서 테스트" harness for the 안전한 응답 필터 element.

Usage:
    source agent-expertise-framework/eval/.venv/bin/activate
    python agent-expertise-framework/eval/compare_filters.py
"""

from filters.baseline_filter import BaselineRegexFilter
from filters.corpus import CASES
from filters.presidio_filter import PresidioFilter

BACKENDS = [BaselineRegexFilter(), PresidioFilter()]


def main() -> None:
    for backend in BACKENDS:
        print(f"\n=== {backend.name} ===")
        total_expected = 0
        total_caught = 0
        false_positives = 0
        for case in CASES:
            detections = backend.scan(case.text)
            found_types = {d.entity_type for d in detections}
            missed = case.expected_entities - found_types
            extra = found_types - case.expected_entities
            total_expected += len(case.expected_entities)
            total_caught += len(case.expected_entities & found_types)
            false_positives += len(extra)
            status = "OK" if not missed and not extra else "MISS" if missed else "EXTRA"
            print(f"  [{status:4s}] {case.case_id:20s} found={sorted(found_types)!s:45s} expected={sorted(case.expected_entities)}")
        recall = total_caught / total_expected if total_expected else 1.0
        print(f"  -> recall={recall:.2f} ({total_caught}/{total_expected}), false_positives={false_positives}")


if __name__ == "__main__":
    main()
