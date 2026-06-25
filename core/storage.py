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
            return [] #파일 없으면 공백 반환
        try:
            return json.loads(self.path.read_text(encoding="utf-8")) #파일 읽기
        except (json.JSONDecodeError, OSError): #오류나면 공백 반환
            return []

    def save(self, data: list[dict[str, Any]]) -> None:
        ensure_parent_dir(self.path)
        if not data:
            self.path.write_text("", encoding="utf-8") #데이터가 없으면 척결
            return
        self.path.write_text(json.dumps(to_serializable(data), indent=2), encoding="utf-8") # JSON 형식으로 데이터 저장 + 2칸 띄어쓰기
