from __future__ import annotations

import customtkinter as ctk

from core.planner import Planner, Task
from core.pomodoro import PomodoroSession
from core.utils import format_time


class PomodoroPlannerApp:
    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.root.title("Pomodoro Planner")
        self.root.geometry("480x360")

        self.planner = Planner()
        self.session = PomodoroSession()
        self.task_input = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Work session")
        self.running = False
        self.timer_id = None
        self._task_row_widgets: dict[int, ctk.CTkFrame] = {}
        self._selected_task_id: int | None = None

        self._build_ui()
        self.render_tasks()
        self.refresh_timer()

    def _build_ui(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        main = ctk.CTkFrame(self.root, corner_radius=12)
        main.pack(fill="both", expand=True, padx=12, pady=12)
        main.pack_propagate(False)

        ctk.CTkLabel(main, text="Pomodoro Planner", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(0, 12))

        timer_frame = ctk.CTkFrame(main, corner_radius=12)
        timer_frame.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(timer_frame, textvariable=self.status_var, font=("Segoe UI", 14, "bold")).pack(pady=(12, 4))
        self.timer_label = ctk.CTkLabel(timer_frame, text=format_time(self.session.time_left), font=("Segoe UI", 32, "bold"))
        self.timer_label.pack(pady=(0, 12))
        button_row = ctk.CTkFrame(timer_frame, fg_color="transparent")
        button_row.pack(pady=(0, 12))
        self.start_pause_button = ctk.CTkButton(button_row, text="Start", command=self.toggle_timer)
        self.start_pause_button.pack(side="left", padx=(0, 6))
        ctk.CTkButton(button_row, text="Skip phase", command=self.advance_phase).pack(side="left")

        task_frame = ctk.CTkFrame(main, corner_radius=12)
        task_frame.pack(fill="both", expand=True)
        entry_row = ctk.CTkFrame(task_frame, fg_color="transparent")
        entry_row.pack(fill="x", pady=(12, 8), padx=12)
        self.task_entry = ctk.CTkEntry(entry_row)
        self.task_entry.pack(side="left", fill="x", expand=True)
        self.task_entry._entry.bind("<Return>", self._on_task_entry_return)
        ctk.CTkButton(entry_row, text="Add", command=self.add_task).pack(side="left", padx=(6, 0))

        self.task_list = ctk.CTkScrollableFrame(task_frame, fg_color="transparent")
        self.task_list.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.task_list.bind("<Double-1>", lambda _event: self.complete_selected_task())

    def add_task(self) -> None:
        title = self.task_entry.get().strip()
        if title:
            self.planner.add_task(title)
            self.task_entry.delete(0, "end")
            self.render_tasks()

    def _on_task_entry_return(self, _event) -> None:
        self.add_task()

    def complete_selected_task(self) -> None:
        if self._selected_task_id is None:
            return
        self.complete_task(self._selected_task_id)
        self._selected_task_id = None

    def _create_task_row(self, task: Task) -> None:
        row = ctk.CTkFrame(self.task_list, fg_color="transparent")
        row.pack(fill="x", pady=1)
        row.bind("<Button-1>", lambda _event, task_id=task.id: self._select_task(task_id))

        label = ctk.CTkLabel(row, text=task.title, anchor="w", justify="left")
        label.pack(side="left", fill="x", expand=True, padx=(0, 6))
        label.bind("<Button-1>", lambda _event, task_id=task.id: self._select_task(task_id))

        ctk.CTkButton(row, text="Done", width=48, command=lambda task_id=task.id: self.complete_task(task_id)).pack(side="right")
        self._task_row_widgets[task.id] = row

    def _select_task(self, task_id: int) -> None:
        self._selected_task_id = task_id

    def render_tasks(self) -> None:
        active_tasks = self.planner.active_tasks()
        active_ids = {task.id for task in active_tasks}

        for task_id, row in list(self._task_row_widgets.items()):
            if task_id not in active_ids:
                row.destroy()
                del self._task_row_widgets[task_id]

        for task in active_tasks:
            if task.id in self._task_row_widgets:
                continue
            self._create_task_row(task)


    def refresh_timer(self) -> None:
        self.timer_label.configure(text=format_time(self.session.time_left))
        self.status_var.set(self.session.current_phase.replace("_", " ").title())

    def complete_task(self, task_id: int) -> None:
        self.planner.complete_task(task_id)
        row = self._task_row_widgets.pop(task_id, None)
        if row is not None:
            row.destroy()
        if self._selected_task_id == task_id:
            self._selected_task_id = None

    def toggle_timer(self) -> None:
        self.running = not self.running
        self.start_pause_button.configure(text="Pause" if self.running else "Start")
        if self.running:
            self._tick_loop()
        elif self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def _tick_loop(self) -> None:
        if not self.running:
            return

        self.session.tick(1)
        self.refresh_timer()

        if self.session.time_left <= 0:
            self.session.complete_current_phase()
            self.refresh_timer()
            self.running = True
            self.start_pause_button.configure(text="Pause")
            self.timer_id = self.root.after(1000, self._tick_loop)
            return

        self.timer_id = self.root.after(1000, self._tick_loop)

    def advance_phase(self) -> None:
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.running = False
        self.start_pause_button.configure(text="Start")
        self.session.complete_current_phase()
        self.refresh_timer()


def main() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.title("Pomodoro Planner")
    root.geometry("480x420")
    PomodoroPlannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
