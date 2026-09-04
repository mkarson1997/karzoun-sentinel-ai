from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class EvaluationCase:
    id: str
    prompt: str
    response: str
    context: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    message: str
    severity: Severity
    evidence: str | None = None


@dataclass(frozen=True, slots=True)
class Evaluation:
    evaluator: str
    score: float
    passed: bool
    findings: tuple[Finding, ...] = ()
    metrics: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CaseResult:
    case_id: str
    passed: bool
    evaluations: tuple[Evaluation, ...]

    @property
    def score(self) -> float:
        if not self.evaluations:
            return 1.0
        return sum(item.score for item in self.evaluations) / len(self.evaluations)


@dataclass(frozen=True, slots=True)
class SuiteResult:
    cases: tuple[CaseResult, ...]

    @property
    def passed(self) -> bool:
        return all(case.passed for case in self.cases)

    @property
    def score(self) -> float:
        if not self.cases:
            return 1.0
        return sum(case.score for case in self.cases) / len(self.cases)
