from todolist.models.task import Task


def test_task_creation():
    task = Task("Test Task", "A simple task")
    assert task.name == "Test Task"
    assert task.description == "A simple task"
    assert not task.completed


def test_mark_as_complete():
    task = Task("Test Task", "A simple task")
    task.mark_as_complete()
    assert task.completed
