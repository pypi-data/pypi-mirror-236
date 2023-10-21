"""Module for managing individual tasks in a todolist."""

from datetime import datetime
from typing import Optional


class Task:
    """Represent an individual task in a todolist.

    Attributes:
        id: A unique identifier for the task.
        name: The name of the task.
        description: A brief description of the task.
        created_at: The datetime when the task was created.
        completed: A boolean indicating if the task is completed or not.
    """

    def __init__(self, name: str, description: Optional[str] = ""):
        """Initialize a new Task instance.

        Args:
            name (str): The name of the task.
            description (Optional[str], optional): A description for the task.
            Defaults to an empty string.
        """
        self.id = id(self)  # Unique ID
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.completed = False

    def mark_as_complete(self):
        """Mark the task as completed."""
        self.completed = True
