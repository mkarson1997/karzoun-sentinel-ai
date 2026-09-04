from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import CaseResult, Evaluation, Finding, SuiteResult


def suite_to_dict(result: SuiteResult) -> dict[str, Any]:
    return {
        "passed": result.passed,
        "score": result.score,
        "cases": [_case_to_dict(case) for case in result.cases],
    }


def save_json(result: SuiteResult, path: str | Path) -> None:
    payload = json.dumps(
        suite_to_dict(result),
        indent=2,
        ensure_ascii=False,
    )
    Path(path).write_text(payload + "\n", encoding="utf-8")


def render_markdown(result: SuiteResult) -> str:
    lines = [
        "# SentinelAI Evaluation Report",
        "",
        f"**Status:** {'PASS' if result.passed else 'FAIL'}  ",
        f"**Suite score:** {result.score:.3f}",
        "",
        "| Case | Status | Score |",
        "| --- | --- | ---: |",
    ]
    for case in result.cases:
        status = "PASS" if case.passed else "FAIL"
        lines.append(f"| `{case.case_id}` | {status} | {case.score:.3f} |")

    for case in result.cases:
        findings = [
            finding
            for evaluation in case.evaluations
            for finding in evaluation.findings
        ]
        if not findings:
            continue
        lines.extend(["", f"## {case.case_id}", ""])
        for finding in findings:
            heading = f"{finding.severity.value.upper()} · {finding.code}"
            lines.append(f"- **{heading}**: {finding.message}")
    return "\n".join(lines) + "\n"


def _case_to_dict(case: CaseResult) -> dict[str, Any]:
    return {
        "id": case.case_id,
        "passed": case.passed,
        "score": case.score,
        "evaluations": [
            _evaluation_to_dict(item) for item in case.evaluations
        ],
    }


def _evaluation_to_dict(evaluation: Evaluation) -> dict[str, Any]:
    return {
        "evaluator": evaluation.evaluator,
        "score": evaluation.score,
        "passed": evaluation.passed,
        "metrics": evaluation.metrics,
        "findings": [
            _finding_to_dict(item) for item in evaluation.findings
        ],
    }


def _finding_to_dict(finding: Finding) -> dict[str, Any]:
    return {
        "code": finding.code,
        "message": finding.message,
        "severity": finding.severity.value,
        "evidence": finding.evidence,
    }
