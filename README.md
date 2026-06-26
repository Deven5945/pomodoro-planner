# Pomodoro Planner

A Simple Pomodoro timer and Planner built with Python and CustomTkinter.

## Features

- Pomodoro Timer
- Planner
- JSON-Based Local Data Saving

<img width="912" height="876" alt="image" src="https://github.com/user-attachments/assets/4179d86a-0a1b-4c95-b875-33dd8c1c2b50" />

## Data Saving

Planner data are stored locally in AppData as JSON files.

## How To Use

Needed libraries
- CustomTkinter
- Pytest (For tests. Not required for general use.)

And then
```
python main.py
```

## Future Plans

- Building Executable (soon, after doing some tests)
- Task breakdown with local/API LLMs (Considering Qwen2.5:3B as local LLM)
- Session statistics
- Adding sounds & notifications
- Time setting(that's why ***pomodoro_data.json*** exists)
- App design (after learning Figma)

## Known Issues

- Korean IME composition text may appear smaller while typing on some Windows systems.
- Lagging when stretching the window and scrolling (I'm trying to fix it)
