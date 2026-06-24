from pathlib import Path

APP_NAME = "Pomodoro Planner"
DATA_DIR = Path(__file__).resolve().parent / "data"
PLANNER_DATA_PATH = DATA_DIR / "planner_data.json"
POMODORO_DATA_PATH = DATA_DIR / "pomodoro_data.json"

DEFAULT_WORK_MINUTES = 25
DEFAULT_SHORT_BREAK_MINUTES = 5
DEFAULT_LONG_BREAK_MINUTES = 15
