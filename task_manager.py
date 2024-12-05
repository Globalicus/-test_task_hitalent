import json
import os
from typing import List, Dict, Optional

class Task:
    def __init__(self, id: int, title: str, description: str, category: str, due_date: str, priority: str, status: str = "Не выполнена"):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def mark_as_done(self):
        self.status = "Выполнена"

    def to_dict(self) -> Dict:
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
        self.filename = filename
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as file:
            tasks_data = json.load(file)
            return [Task(**task) for task in tasks_data]

    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: str):
        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, category, due_date, priority)
        self.tasks.append(new_task)
        self.save_tasks()

    def delete_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    def mark_task_as_done(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                task.mark_as_done()
                self.save_tasks()
                break

    def search_tasks(self, keyword: Optional[str] = None, category: Optional[str] = None, status: Optional[str] = None) -> List[Task]:
        results = self.tasks
        if keyword:
            results = [task for task in results if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            results = [task for task in results if task.category.lower() == category.lower()]
        if status:
            results = [task for task in results if task.status.lower() == status.lower()]
        return results

    def view_tasks(self):
        for task in self.tasks:
            print(f"{task.id}: {task.title} - {task.status}")

def main():
    manager = TaskManager('tasks.json')
    while True:
        command = input("Введите команду (add, delete, done, view, search, exit): ").strip().lower()
        if command == 'add':
            title = input("Название задачи: ")
            description = input("Описание задачи: ")
            category = input("Категория: ")
            due_date = input("Срок выполнения (YYYY-MM-DD): ")
            priority = input("Приоритет (низкий, средний, высокий): ")
            manager.add_task(title, description, category, due_date, priority)
        elif command == 'delete':
            task_id = int(input("ID задачи для удаления: "))
            manager.delete_task(task_id)
        elif command == 'done':
            task_id = int(input("ID задачи для отметки как выполненной: "))
            manager.mark_task_as_done(task_id)
        elif command == 'view':
            manager.view_tasks()
        elif command == 'search':
            keyword = input("Ключевое слово: ")
            results = manager.search_tasks(keyword)
            for task in results:
                print(f"{task.id}: {task.title} - {task.status}")
        elif command == 'exit':
            break
        else:
            print("Неизвестная команда.")

if __name__ == "__main__":
    main()
