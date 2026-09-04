from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import EvaluationCase


def load_jsonl(path: str | Path) -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []
    source = Path(path)
    for line_number, raw_line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on {source}:{line_number}: {exc.msg}") from exc
        cases.append(_case_from_mapping(payload, source=str(source), line=line_number))
    return cases


def _case_from_mapping(payload: Any, *, source: str, line: int) -> EvaluationCase:
    if not isinstance(payload, dict):
        raise ValueError(f"Expected object on {source}:{line}")

    case_id = payload.get("id")
    prompt = payload.get("prompt")
    response = payload.get("response")
    context = payload.get("context", [])
    metadata = payload.get("metadata", {})

    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError(f"Missing non-empty string 'id' on {source}:{line}")
    if not isinstance(prompt, str) or not isinstance(response, str):
        raise ValueError(f"'prompt' and 'response' must be strings on {source}:{line}")
    if not isinstance(context, list) or not all(isinstance(item, str) for item in context):
        raise ValueError(f"'context' must be a list of strings on {source}:{line}")
    if not isinstance(metadata, dict):
        raise ValueError(f"'metadata' must be an object on {source}:{line}")

    return EvaluationCase(
        id=case_id,
        prompt=prompt,
        response=response,
        context=tuple(context),
        metadata=metadata,
    )
