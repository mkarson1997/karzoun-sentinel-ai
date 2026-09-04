from __future__ import annotations

import os
from pathlib import Path


class WorkspacePathError(ValueError):
    """Raised when a requested path escapes the authorized workspace."""


def resolve_input_path(path: str | Path, *, root: str | Path | None = None) -> Path:
    """Resolve an existing file while keeping access inside an authorized workspace."""

    workspace = _workspace(root)
    candidate = _candidate(path, workspace).resolve(strict=True)
    _ensure_within(candidate, workspace)
    if not candidate.is_file():
        raise WorkspacePathError(f"Input path is not a file: {candidate}")
    return candidate


def resolve_output_path(path: str | Path, *, root: str | Path | None = None) -> Path:
    """Resolve a report target while preventing traversal and symlink escapes."""

    workspace = _workspace(root)
    candidate = _candidate(path, workspace).resolve(strict=False)
    _ensure_within(candidate, workspace)

    parent = candidate.parent.resolve(strict=True)
    _ensure_within(parent, workspace)
    if not parent.is_dir():
        raise WorkspacePathError(f"Output parent is not a directory: {parent}")
    return candidate


def _workspace(root: str | Path | None) -> Path:
    workspace = Path.cwd() if root is None else Path(root)
    workspace = workspace.expanduser().resolve(strict=True)
    if not workspace.is_dir():
        raise WorkspacePathError(f"Workspace is not a directory: {workspace}")
    return workspace


def _candidate(path: str | Path, workspace: Path) -> Path:
    candidate = Path(path).expanduser()
    return candidate if candidate.is_absolute() else workspace / candidate


def _ensure_within(candidate: Path, workspace: Path) -> None:
    try:
        common = os.path.commonpath((str(workspace), str(candidate)))
    except ValueError as exc:
        raise WorkspacePathError("Path is outside the authorized workspace") from exc
    if common != str(workspace):
        raise WorkspacePathError(
            f"Path escapes the authorized workspace: {candidate}"
        )
