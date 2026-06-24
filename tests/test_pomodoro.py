from core.pomodoro import PomodoroSession


def test_pomodoro_session_advances_phases():
    session = PomodoroSession(work_minutes=25, short_break_minutes=5, long_break_minutes=15)

    assert session.current_phase == "work"
    assert session.time_left == 25 * 60

    session.tick(60)
    assert session.time_left == 24 * 60

    session.complete_current_phase()
    assert session.current_phase == "short_break"
    assert session.completed_work_rounds == 1


def test_pomodoro_session_uses_long_break_after_four_rounds():
    session = PomodoroSession(work_minutes=25, short_break_minutes=5, long_break_minutes=15)

    for _ in range(4):
        session.complete_current_phase()
        session.complete_current_phase()

    assert session.current_phase == "long_break"
    assert session.completed_work_rounds == 4
