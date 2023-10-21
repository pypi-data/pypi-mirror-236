"""Module for managing tasks in a task list."""

from typing import List
from todolist.models.task import Task
from todolist.exceptions.task_exceptions import TaskNotFoundError


class TaskList:
    """A class to represent a list of tasks."""

    def __init__(self):
        """Initialize an empty list of tasks."""
        self.tasks: List[Task] = []

    def add_task(self, name: str, description: str) -> None:
        """Add a new task to the list.

        Args:
            name (str): The name of the task.
            description (str): A description of the task.
        """
        task = Task(name, description)
        self.tasks.append(task)

    def complete_task(self, task_name: str) -> None:
        """Mark a task as complete.

        Args:
            task_name (str): The name of the task to mark as complete.

        Raises:
            TaskNotFoundError: If the task with the given name is not found.
        """
        for task in self.tasks:
            if task.name == task_name:
                task.mark_as_complete()
                return
        raise TaskNotFoundError("Task not found!")

    def remove_task(self, task_name: str) -> None:
        """Remove a task from the list.

        Args:
            task_name (str): The name of the task to remove.

        Raises:
            TaskNotFoundError: If the task with the given name is not found.
        """
        for task in self.tasks:
            if task.name == task_name:
                self.tasks.remove(task)
                return
        raise TaskNotFoundError("Task not found!")

    def display_tasks(self) -> List[str]:
        """Return a list of uncompleted tasks.

        with their names and descriptions.

        Returns:
            List[str]: A list of uncompleted tasks.
        """
        return [
            f"{task.name} - {task.description}"
            for task in self.tasks
            if not task.completed
        ]
