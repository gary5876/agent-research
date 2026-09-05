"""Runs the GroundingTraceabilityMetric against every Claim currently checked
into this repo's openwiki/.claims/ sidecar — real data, not a synthetic fixture.

Usage:
    source agent-expertise-framework/eval/.venv/bin/activate
    pytest agent-expertise-framework/eval/test_grounding.py -q
"""

import glob
import json
import os

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from grounding_metric import GroundingTraceabilityMetric

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLAIMS_GLOB = os.path.join(REPO_ROOT, "openwiki", ".claims", "**", "*.json")


def _load_claim_cases():
    cases = []
    for claims_file in sorted(glob.glob(CLAIMS_GLOB, recursive=True)):
        with open(claims_file, encoding="utf-8") as f:
            data = json.load(f)
        for claim in data.get("claims", []):
            for evidence in claim.get("evidence", []):
                case_id = f"{os.path.relpath(claims_file, REPO_ROOT)}::{claim['id']}"
                cases.append(
                    pytest.param(
                        claim["statement"],
                        evidence["resource"],
                        id=case_id,
                    )
                )
    return cases


@pytest.mark.parametrize("statement,resource", _load_claim_cases())
def test_claim_is_grounded(statement: str, resource: str):
    test_case = LLMTestCase(input=statement, actual_output=resource)
    assert_test(test_case, [GroundingTraceabilityMetric()])
