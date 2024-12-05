import json  # Импортируем модуль для работы с JSON
import os  # Импортируем модуль для работы с файловой системой
from typing import List, Dict, Optional  # Импортируем типы для аннотаций


class Task:
    def __init__(self, id: int, title: str, description: str, category: str, due_date: str, priority: str,
                 status: str = "Не выполнена"):
        # Конструктор класса Task, инициализирует атрибуты задачи
        self.id = id  # Уникальный идентификатор задачи
        self.title = title  # Заголовок задачи
        self.description = description  # Описание задачи
        self.category = category  # Категория задачи
        self.due_date = due_date  # Срок выполнения задачи
        self.priority = priority  # Приоритет задачи
        self.status = status  # Статус задачи (по умолчанию "Не выполнена")

    def mark_as_done(self):
        # Метод для отметки задачи как выполненной
        self.status = "Выполнена"

    def to_dict(self) -> Dict:
        # Метод для преобразования объекта задачи в словарь
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }


class TaskManager:
    def __init__(self, filename: str):
        # Конструктор класса TaskManager, инициализирует имя файла и загружает задачи
        self.filename = filename  # Имя файла для хранения задач
        self.tasks: List[Task] = self.load_tasks()  # Загрузка задач из файла

    def load_tasks(self) -> List[Task]:
        # Метод для загрузки задач из файла
        if not os.path.exists(self.filename):  # Проверяем, существует ли файл
            return []  # Если файл не существует, возвращаем пустой список
        with open(self.filename, 'r', encoding='utf-8') as file:  # Открываем файл для чтения
            tasks_data = json.load(file)  # Загружаем данные из JSON
            return [Task(**task) for task in tasks_data]  # Преобразуем данные в объекты Task

    def save_tasks(self):
        # Метод для сохранения задач в файл
        with open(self.filename, 'w', encoding='utf-8') as file:  # Открываем файл для записи
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False,
                      indent=4)  # Сохраняем задачи в JSON

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: str):
        # Метод для добавления новой задачи
        task_id = len(self.tasks) + 1  # Генерируем новый ID для задачи
        new_task = Task(task_id, title, description, category, due_date, priority)  # Создаем новый объект Task
        self.tasks.append(new_task)  # Добавляем задачу в список
        self.save_tasks()  # Сохраняем изменения в файл

    def delete_task(self, task_id: int):
        # Метод для удаления задачи по ID
        self.tasks = [task for task in self.tasks if task.id != task_id]  # Фильтруем задачи, исключая удаляемую
        self.save_tasks()  # Сохраняем изменения в файл

    def mark_task_as_done(self, task_id: int):
        # Метод для отметки задачи как выполненной
        for task in self.tasks:
            if task.id == task_id:  # Находим задачу по ID
                task.mark_as_done()  # Отмечаем задачу как выполненную
                self.save_tasks()  # Сохраняем изменения в файл
                break  # Прерываем цикл после нахождения и изменения задачи

    def search_tasks(self, keyword: Optional[str] = None, category: Optional[str] = None,
                     status: Optional[str] = None) -> List[Task]:
        # Метод для поиска задач по ключевым словам, категории и статусу
        results = self.tasks  # Начинаем с полного списка задач
        if keyword:
            # Фильтруем задачи по ключевым словам в заголовке или описании
            results = [task for task in results if
                       keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            # Фильтруем задачи по категории
            results = [task for task in results if task.category.lower() == category.lower()]
        if status:
            # Фильтруем задачи по статусу
            results = [task for task in results if task.status.lower() == status.lower()]
        return results  # Возвращаем найденные задачи

    def view_tasks(self):
        # Метод для отображения всех задач
        for task in self.tasks:
            print(f"{task.id}: {task.title} - {task.status}")  # Печатаем ID, заголовок и статус каждой задачи


def main():
    # Основная функция для запуска программы
    manager = TaskManager('tasks.json')  # Создаем экземпляр TaskManager с файлом для хранения задач
    while True:
        command = input(
            "Введите команду (add, delete, done, view, search, exit): ").strip().lower()  # Запрашиваем команду у пользователя
        if command == 'add':
            # Добавление новой задачи
            title = input("Название задачи: ")  # Запрашиваем название
            description = input("Описание задачи: ")  # Запрашиваем описание
            category = input("Категория: ")  # Запрашиваем категорию
            due_date = input("Срок выполнения (YYYY-MM-DD): ")  # Запрашиваем срок выполнения
            priority = input("Приоритет (низкий, средний, высокий): ")  # Запрашиваем приоритет
            manager.add_task(title, description, category, due_date, priority)  # Добавляем задачу
        elif command == 'delete':
            # Удаление задачи
            task_id = int(input("ID задачи для удаления: "))  # Запрашиваем ID задачи
            manager.delete_task(task_id)  # Удаляем задачу
        elif command == 'done':
            # Отметка задачи как выполненной
            task_id = int(input("ID задачи для отметки как выполненной: "))  # Запрашиваем ID задачи
            manager.mark_task_as_done(task_id)  # Отмечаем задачу как выполненную
        elif command == 'view':
            # Просмотр всех задач
            manager.view_tasks()  # Выводим все задачи
        elif command == 'search':
            # Поиск задач
            keyword = input("Ключевое слово: ")  # Запрашиваем ключевое слово
            results = manager.search_tasks(keyword)  # Ищем задачи
            for task in results:
                print(f"{task.id}: {task.title} - {task.status}")  # Выводим найденные задачи
        elif command == 'exit':
            break  # Выход из цикла и завершение программы
        else:
            print("Неизвестная команда.")  # Обработка неизвестной команды


if __name__ == "__main__":
    main()  # Запуск основной функции при выполнении скрипта
