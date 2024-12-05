import pytest
from task_manager import Task, TaskManager

@pytest.fixture
def task_manager():
    manager = TaskManager('test_tasks.json')
    manager.tasks = []  # Очистка задач для тестов
    return manager

def test_add_task(task_manager):
    task_manager.add_task("Test Task", "Description", "Work", "2024-12-31", "Высокий")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Test Task"

def test_delete_task(task_manager):
    task_manager.add_task("Test Task", "Description", "Work", "2024-12-31", "Высокий")
    task_manager.delete_task(1)
    assert len(task_manager.tasks) == 0

def test_mark_task_as_done(task_manager):
    task_manager.add_task("Test Task", "Description", "Work", "2024-12-31", "Высокий")
    task_manager.mark_task_as_done(1)
    assert task_manager.tasks[0].status == "Выполнена"

def test_search_tasks(task_manager):
    task_manager.add_task("Test Task", "Description", "Work", "2024-12-31", "Высокий")
    results = task_manager.search_tasks(keyword="Test")
    assert len(results) == 1
