from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RegressionResult:
    passed: bool
    score_drop: float
    new_failed_cases: tuple[str, ...]
    reasons: tuple[str, ...]


def compare_reports(
    baseline: dict[str, Any],
    current: dict[str, Any],
    *,
    max_score_drop: float = 0.05,
) -> RegressionResult:
    baseline_score = _number(baseline.get("score"), "baseline.score")
    current_score = _number(current.get("score"), "current.score")
    score_drop = max(0.0, baseline_score - current_score)

    baseline_cases = _case_statuses(baseline)
    current_cases = _case_statuses(current)
    new_failed = tuple(
        case_id
        for case_id, passed in current_cases.items()
        if not passed and baseline_cases.get(case_id, True)
    )

    reasons: list[str] = []
    if score_drop > max_score_drop:
        reasons.append(
            f"Suite score dropped by {score_drop:.3f}, "
            f"limit is {max_score_drop:.3f}."
        )
    if new_failed:
        reasons.append("New failing cases: " + ", ".join(new_failed))

    return RegressionResult(
        passed=not reasons,
        score_drop=score_drop,
        new_failed_cases=new_failed,
        reasons=tuple(reasons),
    )


def _case_statuses(report: dict[str, Any]) -> dict[str, bool]:
    cases = report.get("cases", [])
    if not isinstance(cases, list):
        raise ValueError("report.cases must be a list")
    statuses: dict[str, bool] = {}
    for item in cases:
        valid_case = (
            isinstance(item, dict)
            and isinstance(item.get("id"), str)
            and isinstance(item.get("passed"), bool)
        )
        if not valid_case:
            raise ValueError(
                "Each report case must have string 'id' and boolean 'passed'"
            )
        statuses[item["id"]] = item["passed"]
    return statuses


def _number(value: Any, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{field} must be numeric")
    return float(value)
