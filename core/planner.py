from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from config import PLANNER_DATA_PATH
from core.storage import JsonStore


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class Planner:
    def __init__(self, storage_path: str | None = None) -> None:
        self.storage = JsonStore(storage_path or PLANNER_DATA_PATH)
        self.tasks: List[Task] = [Task(**item) for item in self.storage.load()]
        self._next_id = max((task.id for task in self.tasks), default=0) + 1

    def add_task(self, title: str) -> Task:
        task = Task(id=self._next_id, title=title)
        self._next_id += 1
        self.tasks.append(task)
        self._persist()
        return task

    def active_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.completed]

    def completed_tasks(self) -> List[Task]:
        return [task for task in self.tasks if task.completed]

    def complete_task(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.id == task_id and not task.completed:
                task.completed = True
                self._persist()
                return task
        return None

    def _persist(self) -> None:
        self.storage.save([task.__dict__ for task in self.tasks])
