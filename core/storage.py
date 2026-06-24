from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import PLANNER_DATA_PATH
from core.utils import ensure_parent_dir, to_serializable


class JsonStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or PLANNER_DATA_PATH)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def save(self, data: list[dict[str, Any]]) -> None:
        ensure_parent_dir(self.path)
        self.path.write_text(json.dumps(to_serializable(data), indent=2), encoding="utf-8")
