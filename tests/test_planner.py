import json

from core.planner import Planner


def test_planner_tracks_active_and_completed_tasks(tmp_path):
    planner = Planner(storage_path=str(tmp_path / "planner_data.json"))

    task = planner.add_task("Write unit tests")
    assert planner.active_tasks()[0].id == task.id

    planner.complete_task(task.id)

    assert planner.active_tasks() == []
    assert planner.completed_tasks()[0].id == task.id
    assert planner.completed_tasks()[0].completed is True


def test_completed_tasks_are_removed_from_persisted_data(tmp_path):
    storage_path = tmp_path / "planner_data.json"
    planner = Planner(storage_path=str(storage_path))

    task = planner.add_task("Write unit tests")
    planner.complete_task(task.id)

    saved_text = storage_path.read_text(encoding="utf-8")
    assert saved_text == ""


def test_persisted_tasks_only_store_id_and_title(tmp_path):
    storage_path = tmp_path / "planner_data.json"
    planner = Planner(storage_path=str(storage_path))

    task = planner.add_task("Write unit tests")

    saved_data = json.loads(storage_path.read_text(encoding="utf-8"))
    assert saved_data == [{"id": task.id, "title": "Write unit tests"}]
