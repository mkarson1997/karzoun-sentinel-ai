from karzoun_sentinel import compare_reports


def test_regression_gate_catches_score_drop_and_new_failure() -> None:
    baseline = {"score": 0.95, "cases": [{"id": "a", "passed": True}]}
    current = {"score": 0.80, "cases": [{"id": "a", "passed": False}]}
    result = compare_reports(baseline, current, max_score_drop=0.05)
    assert not result.passed
    assert result.new_failed_cases == ("a",)
    assert result.score_drop > 0.1


def test_regression_gate_allows_stable_report() -> None:
    baseline = {"score": 0.90, "cases": [{"id": "a", "passed": True}]}
    current = {"score": 0.91, "cases": [{"id": "a", "passed": True}]}
    assert compare_reports(baseline, current).passed
