from __future__ import annotations

from pathlib import Path
from typing import NamedTuple


class DirTree(NamedTuple):
    name: Path
    files: list[Path]
    dirs: list[DirTree]


def get_dirtree(parent: Path, directory: Path = Path()) -> DirTree:
    full_dir = parent / directory

    files = []
    dirs = []
    for item in full_dir.iterdir():
        if item.is_file():
            files.append(item.relative_to(full_dir))
        elif item.is_dir():
            dirs.append(get_dirtree(full_dir, item.relative_to(full_dir)))

    return DirTree(name=directory, files=files, dirs=dirs)
