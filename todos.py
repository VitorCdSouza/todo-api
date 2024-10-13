# todos.py

from enum import Enum

# todo status enums
class TodoStatus(Enum):
    NAO_INICIADO = "nao iniciado"
    EM_ANDAMENTO = "em andamento"
    COMPLETO = "completo"

class TodoManager:
    def __init__(self):
        self.todos = [
            {"id": 1, "title": "Tarefa 1", "description": "Descricao 1", "status": TodoStatus.COMPLETO.value},
            {"id": 2, "title": "Tarefa 2", "description": "Descricao 2", "status": TodoStatus.NAO_INICIADO.value},
            {"id": 3, "title": "Tarefa 3", "description": "Descricao 3", "status": TodoStatus.EM_ANDAMENTO.value},
            {"id": 4, "title": "Tarefa 4", "description": "Descricao 4", "status": TodoStatus.COMPLETO.value},
            {"id": 5, "title": "Tarefa 5", "description": "Descricao 5", "status": TodoStatus.EM_ANDAMENTO.value},
            {"id": 6, "title": "Tarefa 6", "description": "Descricao 6", "status": TodoStatus.NAO_INICIADO.value}
        ]
        self.current_id = 3
    
    def get_all(self):
        return self.todos
    
    def get_by_id(self, todo_id):
        return next((todo for todo in self.todos if todo['id'] == todo_id), None)