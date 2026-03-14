from __future__ import annotations

from pathlib import Path
import shutil


def copy_fixture(tmp_path: Path, name: str) -> Path:
    fixture_root = Path(__file__).parent / "fixtures" / name
    destination = tmp_path / name
    shutil.copytree(fixture_root, destination)
    return destination
