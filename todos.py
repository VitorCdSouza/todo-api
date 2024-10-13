# todos.py

from enum import Enum

# todo status enums
class TodoStatus(Enum):
    PENDENTE = "pendente"
    INCOMPLETA = "incompleta"
    COMPLETA = "completa"

class TodoManager:
    def __init__(self):
        self.todos = [
            {"id": 1, "title": "Tarefa 1", "description": "Descricao 1", "status": TodoStatus.COMPLETA.value},
            {"id": 2, "title": "Tarefa 2", "description": "Descricao 2", "status": TodoStatus.PENDENTE.value},
            {"id": 3, "title": "Tarefa 3", "description": "Descricao 3", "status": TodoStatus.INCOMPLETA.value},
            {"id": 4, "title": "Tarefa 4", "description": "Descricao 4", "status": TodoStatus.COMPLETA.value},
            {"id": 5, "title": "Tarefa 5", "description": "Descricao 5", "status": TodoStatus.INCOMPLETA.value},
            {"id": 6, "title": "Tarefa 6", "description": "Descricao 6", "status": TodoStatus.PENDENTE.value}
        ]
        self.current_id = 3
    
    def get_all(self):
        return self.todos
    
    def get_by_id(self, todo_id):
        return next((todo for todo in self.todos if todo['id'] == todo_id), None)
    
    def create(self, title, description='', status=TodoStatus.PENDENTE.value):
        new_todo = {
            "id": self.current_id,
            "title": title,
            "description": description,
            "status": status
        }
        self.todos.append(new_todo)
        self.current_id += 1
        return new_todo
    
    def update(self, todo_id, title=None, description=None, status=None):
        todo = self.get_by_id(todo_id)
        if todo:
            if title is not None:
                todo['title'] = title
            if description is not None:
                todo['description'] = description
            if status is not None and status in TodoStatus._value2member_map_:
                todo['status'] = status
            return todo
        return None
    
    def delete(self, todo_id):
        todo = self.get_by_id(todo_id)
        if todo:
            self.todos = [t for t in self.todos if t['id'] != todo_id]
            return True
        return False