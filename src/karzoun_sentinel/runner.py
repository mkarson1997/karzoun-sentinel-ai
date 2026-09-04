from __future__ import annotations

from collections.abc import Iterable, Sequence
from concurrent.futures import ThreadPoolExecutor

from .evaluators import Evaluator, default_evaluators
from .models import CaseResult, EvaluationCase, SuiteResult


class EvaluationSuite:
    def __init__(self, evaluators: Sequence[Evaluator] | None = None) -> None:
        self.evaluators = tuple(evaluators or default_evaluators())

    def evaluate_case(self, case: EvaluationCase) -> CaseResult:
        evaluations = tuple(evaluator.evaluate(case) for evaluator in self.evaluators)
        return CaseResult(
            case_id=case.id,
            passed=all(item.passed for item in evaluations),
            evaluations=evaluations,
        )

    def evaluate(self, cases: Iterable[EvaluationCase], *, workers: int = 1) -> SuiteResult:
        case_list = list(cases)
        if workers <= 1 or len(case_list) <= 1:
            results = tuple(self.evaluate_case(case) for case in case_list)
            return SuiteResult(cases=results)

        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = tuple(executor.map(self.evaluate_case, case_list))
        return SuiteResult(cases=results)
