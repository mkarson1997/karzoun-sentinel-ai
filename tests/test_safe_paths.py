from pathlib import Path

import pytest

from karzoun_sentinel import (
    WorkspacePathError,
    resolve_input_path,
    resolve_output_path,
)


def test_input_path_stays_inside_workspace(tmp_path: Path) -> None:
    case_file = tmp_path / "cases.jsonl"
    case_file.write_text("{}\n", encoding="utf-8")

    assert resolve_input_path("cases.jsonl", root=tmp_path) == case_file.resolve()


def test_input_path_rejects_parent_traversal(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.json"
    outside.write_text("{}", encoding="utf-8")
    try:
        with pytest.raises(WorkspacePathError):
            resolve_input_path("../outside.json", root=tmp_path)
    finally:
        outside.unlink(missing_ok=True)


def test_output_path_rejects_parent_traversal(tmp_path: Path) -> None:
    with pytest.raises(WorkspacePathError):
        resolve_output_path("../report.json", root=tmp_path)


def test_output_path_allows_file_in_workspace(tmp_path: Path) -> None:
    expected = (tmp_path / "report.json").resolve()
    assert resolve_output_path("report.json", root=tmp_path) == expected
