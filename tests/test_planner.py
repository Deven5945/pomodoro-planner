from core.planner import Planner


def test_planner_tracks_active_and_completed_tasks():
    planner = Planner()

    task = planner.add_task("Write unit tests")
    assert planner.active_tasks()[0].id == task.id

    planner.complete_task(task.id)

    assert planner.active_tasks() == []
    assert planner.completed_tasks()[0].id == task.id
    assert planner.completed_tasks()[0].completed is True
