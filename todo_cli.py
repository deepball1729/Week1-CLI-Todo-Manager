"""
A simple command-line To-Do List Manager.

Design choices:
- TaskManager owns task operations, keeping the menu logic separate.
- Tasks are stored in a JSON file so they remain available after restarting.
- Each task has a numeric ID, title, and completion status.
- Input is validated before changing data.
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tasks.json")


class TaskManager:
    """Create, store, display, and update to-do tasks."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = Path(data_file)
        self.tasks = []
        self._load_tasks()

    def _load_tasks(self):
        """Load saved tasks; use an empty list if the file does not exist yet."""
        if not self.data_file.exists():
            self.tasks = []
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("Saved task data must be a list.")
            self.tasks = data
        except (json.JSONDecodeError, OSError, ValueError) as error:
            # Do not crash on a damaged or unreadable file.
            print(f"Warning: Could not load saved tasks ({error}). Starting empty.")
            self.tasks = []

    def _save_tasks(self):
        """Write tasks to disk so changes persist between runs."""
        try:
            with self.data_file.open("w", encoding="utf-8") as file:
                json.dump(self.tasks, file, indent=4, ensure_ascii=False)
        except OSError as error:
            print(f"Error: Could not save tasks ({error}).")

    def _next_id(self):
        """Return an unused ID, including when earlier tasks were deleted."""
        return max((task.get("id", 0) for task in self.tasks), default=0) + 1

    def add_task(self, title):
        """Add a task after validating its title."""
        title = title.strip()
        if not title:
            return False, "Task title cannot be empty."

        task = {"id": self._next_id(), "title": title, "completed": False}
        self.tasks.append(task)
        self._save_tasks()
        return True, f"Task added with ID {task['id']}."

    def list_tasks(self):
        """Return all tasks, including their status."""
        return self.tasks

    def complete_task(self, task_id):
        """Mark a task as completed using its ID."""
        task = self._find_task(task_id)
        if task is None:
            return False, f"No task found with ID {task_id}."
        if task.get("completed", False):
            return True, "That task is already completed."

        task["completed"] = True
        self._save_tasks()
        return True, f"Task {task_id} marked as completed."

    def remove_task(self, task_id):
        """Remove a task by ID."""
        task = self._find_task(task_id)
        if task is None:
            return False, f"No task found with ID {task_id}."

        self.tasks.remove(task)
        self._save_tasks()
        return True, f"Task {task_id} removed."

    def _find_task(self, task_id):
        """Find one task by ID; return None if it does not exist."""
        for task in self.tasks:
            if task.get("id") == task_id:
                return task
        return None


def display_tasks(manager):
    """Print tasks in a readable format."""
    tasks = manager.list_tasks()
    if not tasks:
        print("\nYour to-do list is empty.")
        return

    print("\n--- Your Tasks ---")
    for task in tasks:
        status = "✓ Completed" if task.get("completed", False) else "Pending"
        print(f"[{task.get('id')}] {task.get('title', '(untitled)')} — {status}")


def read_task_id():
    """Ask for a positive integer task ID and handle invalid input."""
    raw_value = input("Enter task ID: ").strip()
    try:
        task_id = int(raw_value)
        if task_id <= 0:
            raise ValueError
        return task_id
    except ValueError:
        print("Invalid ID. Please enter a positive whole number.")
        return None


def main():
    """Run the menu until the user chooses to exit."""
    manager = TaskManager()
    print("Welcome to the To-Do List Manager!")

    while True:
        print("\n===== TO-DO MENU =====")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task as completed")
        print("4. Remove task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            title = input("Enter task title: ")
            success, message = manager.add_task(title)
            print(message)
        elif choice == "2":
            display_tasks(manager)
        elif choice == "3":
            task_id = read_task_id()
            if task_id is not None:
                success, message = manager.complete_task(task_id)
                print(message)
        elif choice == "4":
            task_id = read_task_id()
            if task_id is not None:
                success, message = manager.remove_task(task_id)
                print(message)
        elif choice == "5":
            print("Goodbye! Your tasks have been saved.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
