from pathlib import Path

import pytest

from karzoun_sentinel import load_jsonl


def test_load_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "cases.jsonl"
    path.write_text('{"id":"one","prompt":"p","response":"r","context":["c"]}\n', encoding="utf-8")
    cases = load_jsonl(path)
    assert cases[0].id == "one"
    assert cases[0].context == ("c",)


def test_load_jsonl_reports_line_number(tmp_path: Path) -> None:
    path = tmp_path / "broken.jsonl"
    path.write_text("{}\nnot-json\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r":1|:2"):
        load_jsonl(path)
