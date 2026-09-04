from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from .dataset import load_jsonl
from .regression import compare_reports
from .reporting import render_markdown, save_json, suite_to_dict
from .runner import EvaluationSuite


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinelai",
        description="Evaluate and regression-test LLM outputs",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Evaluate a JSONL dataset")
    evaluate.add_argument("dataset")
    evaluate.add_argument("--workers", type=int, default=1)
    evaluate.add_argument("--json", dest="json_path")
    evaluate.add_argument("--markdown", dest="markdown_path")
    evaluate.add_argument("--allow-failures", action="store_true")

    compare = subparsers.add_parser(
        "compare",
        help="Compare current report against a baseline",
    )
    compare.add_argument("baseline")
    compare.add_argument("current")
    compare.add_argument("--max-score-drop", type=float, default=0.05)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "evaluate":
        result = EvaluationSuite().evaluate(
            load_jsonl(args.dataset),
            workers=max(1, args.workers),
        )
        payload = suite_to_dict(result)
        if args.json_path:
            save_json(result, args.json_path)
        if args.markdown_path:
            Path(args.markdown_path).write_text(
                render_markdown(result),
                encoding="utf-8",
            )
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0 if result.passed or args.allow_failures else 1

    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    current = json.loads(Path(args.current).read_text(encoding="utf-8"))
    comparison = compare_reports(
        baseline,
        current,
        max_score_drop=args.max_score_drop,
    )
    for reason in comparison.reasons:
        print(reason)
    return 0 if comparison.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
