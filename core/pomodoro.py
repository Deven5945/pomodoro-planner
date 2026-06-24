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

    def tick(self, seconds: int) -> int:
        self.time_left = max(0, self.time_left - seconds)
        return self.time_left

    def complete_current_phase(self) -> str:
        if self.current_phase == "work":
            self.completed_work_rounds += 1
            if self.completed_work_rounds >= 4:
                self.current_phase = "long_break"
                self.time_left = self.long_break_minutes * 60
            else:
                self.current_phase = "short_break"
                self.time_left = self.short_break_minutes * 60
        elif self.current_phase == "short_break":
            self.current_phase = "work"
            self.time_left = self.work_minutes * 60
        elif self.current_phase == "long_break":
            self.current_phase = "work"
            self.time_left = self.work_minutes * 60
            self.completed_work_rounds = 0
        return self.current_phase
