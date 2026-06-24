import importlib
import sys

import config


def test_get_data_dir_uses_appdata_when_frozen(monkeypatch, tmp_path):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setattr(sys, "frozen", True, raising=False)

    reloaded_config = importlib.reload(config)

    assert reloaded_config.get_data_dir() == tmp_path / "Pomodoro Planner"
