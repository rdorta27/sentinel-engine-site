"""Where things are: this repository, the published folder and the sentinel-engine checkout.

The checkout is only needed by the checks that read its files. It is the folder
next to this repository (../core), or the one named by SENTINEL_CORE.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
NUMBERS = SITE / "numbers.json"
CORE = Path(os.environ.get("SENTINEL_CORE") or ROOT.parent / "core")


def repo_kind(rel: str) -> str:
    """GitHub link kind of a path of sentinel-engine: tree for a folder, blob for a file.

    The checkout decides when it is there. Without it, a path with no extension is a folder.
    """
    target = CORE / rel
    if target.exists():
        return "tree" if target.is_dir() else "blob"
    return "blob" if Path(rel).suffix else "tree"
