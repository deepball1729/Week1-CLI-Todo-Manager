# Week 1 Task — Python CLI To-Do List Manager

## Overview

This project is a command-line To-Do List Manager written in Python. It lets a user:

- Add a task
- View all tasks and their status
- Mark a task as completed
- Remove a task
- Save tasks automatically so they remain after the application closes

The program uses only Python's standard library. No external dependencies are required.

## Requirements

- Python 3.8 or newer
- A terminal or command prompt

Check Python is installed:

```bash
python --version
```

On some systems, use `python3 --version`.

## How to run

1. Extract the ZIP archive.
2. Open a terminal in the extracted project folder.
3. Run:

```bash
python todo_cli.py
```

If your system uses `python3`, run `python3 todo_cli.py` instead.

The application creates `tasks.json` in the same folder when it saves the first change. Keep this file if you want to preserve your tasks.

## Menu options

1. **Add task** — enter a title; blank titles are rejected.
2. **View tasks** — see task IDs, titles, and whether each task is pending or completed.
3. **Mark task as completed** — enter the ID of an existing task.
4. **Remove task** — enter the ID of the task to delete.
5. **Exit** — close the application.

## Design and implementation

- `TaskManager` groups task-related operations in one class. This keeps data handling separate from the menu.
- Each task is represented as a dictionary with `id`, `title`, and `completed` fields.
- Task IDs make it possible to complete or delete a specific task.
- `tasks.json` stores data in JSON format, allowing persistence between sessions.
- Small functions (`display_tasks`, `read_task_id`, and `main`) keep the user interface readable.
- Comments explain important design decisions and error-handling behavior.

## Error handling and validation

- Blank task titles are not accepted.
- Menu choices outside 1–5 are rejected with a helpful message.
- Task IDs must be positive whole numbers.
- A task ID that does not exist produces a message instead of crashing.
- Missing saved-data files are treated as a new list.
- Invalid JSON or file-access problems are caught and reported.

## Logic flow / pseudocode

```text
START
  Load tasks from tasks.json
  REPEAT
    Display menu
    Read user's choice
    IF choice is Add:
      Read and validate title
      Add task and save
    ELSE IF choice is View:
      Display tasks or an empty-list message
    ELSE IF choice is Complete:
      Read and validate ID
      Mark matching task completed and save
    ELSE IF choice is Remove:
      Read and validate ID
      Remove matching task and save
    ELSE IF choice is Exit:
      Display goodbye message
      STOP
    ELSE:
      Display invalid-choice message
  UNTIL exit
END
```

## Manual test scenarios

1. **Add a task:** choose `1`, enter `Finish Python assignment`; then choose `2` and confirm it appears as Pending.
2. **Reject a blank title:** choose `1`, press Enter without typing a title; confirm the program displays an error.
3. **Complete a task:** choose `3`, enter the ID shown in the task list, then choose `2`; confirm the status is Completed.
4. **Reject an invalid ID:** choose `4`, enter `99999`; confirm the program reports that no task was found.
5. **Reject invalid menu input:** enter `abc` or `9` at the menu; confirm the program continues running.
6. **Remove a task:** choose `4`, enter an existing task ID, then view the list to confirm it is gone.
7. **Check persistence:** add a task, exit, run the program again, and view tasks. The task should still be present.

## Project structure

```text
todo_cli_week1/
├── todo_cli.py
├── README.md
└── tasks.json   (created automatically when tasks are saved)
```

## License

This is an educational project created for practice.
