import os
import sys
from pathlib import Path

APP_NAME = "Pomodoro Planner"


def get_data_dir() -> Path:
    if getattr(sys, "frozen", False):
        appdata = os.getenv("APPDATA")
        if appdata:
            return Path(appdata) / APP_NAME
    return Path(__file__).resolve().parent / "data"


DATA_DIR = get_data_dir()
PLANNER_DATA_PATH = DATA_DIR / "planner_data.json"
POMODORO_DATA_PATH = DATA_DIR / "pomodoro_data.json"

DEFAULT_WORK_MINUTES = 25
DEFAULT_SHORT_BREAK_MINUTES = 5
DEFAULT_LONG_BREAK_MINUTES = 15
