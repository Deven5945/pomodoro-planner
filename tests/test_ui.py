import tkinter as tk

import customtkinter as ctk
import pytest

from ui.ctk_ui import PomodoroPlannerApp


def _create_test_root():
    try:
        root = ctk.CTk()
        root.withdraw()
        return root
    except Exception as exc:  # pragma: no cover - environment-dependent
        pytest.skip(f"Tkinter runtime is unavailable: {exc}")


def test_render_tasks_only_creates_rows_for_active_tasks(monkeypatch):
    root = _create_test_root()

    class DummyPlanner:
        def __init__(self):
            self.tasks = []

        def active_tasks(self):
            return []

        def complete_task(self, task_id):
            self.tasks = [task for task in self.tasks if task.id != task_id]

    monkeypatch.setattr("ui.ctk_ui.Planner", DummyPlanner)

    app = PomodoroPlannerApp(root)
    app.render_tasks()

    assert app._task_row_widgets == {}
    root.destroy()


def test_enter_key_triggers_add_task(monkeypatch):
    root = _create_test_root()

    class DummyPlanner:
        def __init__(self):
            self.tasks = []

        def active_tasks(self):
            return []

        def add_task(self, title):
            self.tasks.append(title)

    monkeypatch.setattr("ui.ctk_ui.Planner", DummyPlanner)

    app = PomodoroPlannerApp(root)
    app.task_entry.insert(0, "New task")

    called = {"value": False}

    def fake_add_task():
        called["value"] = True

    monkeypatch.setattr(app, "add_task", fake_add_task)
    app._on_task_entry_return(None)
    root.update()

    assert called["value"] is True
    root.destroy()


def test_complete_selected_task_marks_task_completed(monkeypatch):
    root = _create_test_root()

    class DummyTask:
        def __init__(self, task_id, title):
            self.id = task_id
            self.title = title
            self.completed = False

    class DummyPlanner:
        def __init__(self):
            self.tasks = [DummyTask(1, "Review changes")]

        def active_tasks(self):
            return [task for task in self.tasks if not task.completed]

        def complete_task(self, task_id):
            for task in self.tasks:
                if task.id == task_id:
                    task.completed = True
                    break

    monkeypatch.setattr("ui.ctk_ui.Planner", DummyPlanner)

    app = PomodoroPlannerApp(root)
    app.render_tasks()
    app._selected_task_id = 1

    app.complete_selected_task()

    assert app.planner.active_tasks() == []
    assert 1 not in app._task_row_widgets
    root.destroy()


def test_timer_auto_starts_next_phase_when_current_one_finishes():
    root = _create_test_root()

    app = PomodoroPlannerApp(root)
    app.session.time_left = 1
    app.running = True

    app._tick_loop()

    assert app.running is True
    assert app.session.current_phase == "short_break"
    assert app.session.time_left == 5 * 60
    root.destroy()
