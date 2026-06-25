from __future__ import annotations

from pathlib import Path
from typing import Any


def format_time(total_seconds: int) -> str:
    minutes, seconds = divmod(max(0, total_seconds), 60) #분, 초 계산 - 전체 초/60
    return f"{minutes:02d}:{seconds:02d}"


def ensure_parent_dir(path: str | Path) -> Path: #디렉토리 생성
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True) #부모 디렉토리 한번에 생성, 이미 있으면 무시
    return path


def to_serializable(value: Any) -> Any: #JSON 저장 용이
    if isinstance(value, dict):
        return {key: to_serializable(item) for key, item in value.items()} 
    if isinstance(value, (list, tuple)):
        return [to_serializable(item) for item in value]
    return value
