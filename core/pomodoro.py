from __future__ import annotations

from config import (
    DEFAULT_LONG_BREAK_MINUTES,
    DEFAULT_SHORT_BREAK_MINUTES,
    DEFAULT_WORK_MINUTES,
)


class PomodoroSession:
    def __init__(
        self,
        work_minutes: int = DEFAULT_WORK_MINUTES,
        short_break_minutes: int = DEFAULT_SHORT_BREAK_MINUTES,
        long_break_minutes: int = DEFAULT_LONG_BREAK_MINUTES,
    ) -> None:
        self.work_minutes = work_minutes
        self.short_break_minutes = short_break_minutes
        self.long_break_minutes = long_break_minutes
        self.current_phase = "work"
        self.time_left = work_minutes * 60
        self.completed_work_rounds = 0

    def tick(self, sec: int) -> int:
        self.time_left = max(0, self.time_left - sec)
        return self.time_left

    def complete_current_phase(self) -> str: #페이즈 끝났을때
        if self.current_phase == "work": #현재 상태 일이면
            self.completed_work_rounds += 1 #라운드 1추가
            if self.completed_work_rounds % 4 == 0: #라운드 4 되면
                self.current_phase = "long_break" #긴 휴식
                self.time_left = self.long_break_minutes * 60 #초 추가
            else:
                self.current_phase = "short_break" #짧은 휴식
                self.time_left = self.short_break_minutes * 60 #초 추가
        elif self.current_phase == "short_break": #현재 상태 짧은 휴식이면
            self.current_phase = "work" #일하시오
            self.time_left = self.work_minutes * 60 #초 추가
        elif self.current_phase == "long_break": #현재 상태 긴 휴식이면
            self.current_phase = "work" #일하거라
            self.time_left = self.work_minutes * 60 #초 추가
            self.completed_work_rounds = 0 #라운드 초기화
        return self.current_phase #상태 반환
