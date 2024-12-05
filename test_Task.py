import pytest  # Импортируем библиотеку для тестирования
from task_manager import TaskManager  # Импортируем классы Task и TaskManager из модуля task_manager


@pytest.fixture
def task_manager():
    # Фикстура для создания экземпляра TaskManager для тестов
    manager = TaskManager('test_tasks.json')  # Создаем TaskManager с тестовым файлом
    manager.tasks = []  # Очищаем список задач для тестов
    return manager  # Возвращаем экземпляр TaskManager


def test_add_task(task_manager):
    # Тест для проверки добавления задачи
    task_manager.add_task("Test Task", "Description", "Work", "2024-12-31", "Высокий")  # Добавляем тестовую задачу
    assert len(task_manager.tasks) == 1  # Проверяем, что в списке задач одна задача
    assert task_manager.tasks[0].title == "Test Task"  # Проверяем, что заголовок задачи соответствует ожидаемому


def test_delete_task(task_manager):
    # Тест для проверки удаления задачи
    task_manager.add_task("Test Task", "Description", "Work", "2024-12-31", "Высокий")  # Добавляем задачу
    task_manager.delete_task(1)  # Удаляем задачу с ID 1
    assert len(task_manager.tasks) == 0  # Проверяем, что список задач пуст


def test_mark_task_as_done(task_manager):
    # Тест для проверки отметки задачи как выполненной
    task_manager.add_task("Test Task", "Description", "Work", "2024-12-31", "Высокий")  # Добавляем задачу
    task_manager.mark_task_as_done(1)  # Отмечаем задачу с ID 1 как выполненную
    assert task_manager.tasks[0].status == "Выполнена"  # Проверяем, что статус задачи изменился на "Выполнена"


def test_search_tasks(task_manager):
    # Тест для проверки поиска задач
    task_manager.add_task("Test Task", "Description", "Work", "2024-12-31", "Высокий")  # Добавляем задачу
    results = task_manager.search_tasks(keyword="Test")  # Ищем задачи по ключевому слову "Test"
    assert len(results) == 1  # Проверяем, что найдено одна задача
