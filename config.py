import os
import sys
from pathlib import Path

APP_NAME = "Pomodoro Planner"


def get_data_dir() -> Path:
    if getattr(sys, "frozen", False):
        appdata = os.getenv("APPDATA") #디렉토리 경로 가져오기
        if appdata:
            return Path(appdata) / APP_NAME #파일 생성
    return Path(__file__).resolve().parent / "data"


DATA_DIR = get_data_dir() #디렉토리
PLANNER_DATA_PATH = DATA_DIR / "planner_data.json" #플래너 데이터 디렉토리
POMODORO_DATA_PATH = DATA_DIR / "pomodoro_data.json" #포모도로 데이터 디렉토리

DEFAULT_WORK_MINUTES = 25 #일
DEFAULT_SHORT_BREAK_MINUTES = 5 #짧은 휴식
DEFAULT_LONG_BREAK_MINUTES = 15 #긴 휴식
