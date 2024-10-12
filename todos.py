# todos.py
class TodoManager:
    def __init__(self):
        self.todos = [
            {"id": 1, "title": "Tarefa 1", "description": "Descricao 1", "status": False},
            {"id": 2, "title": "Tarefa 2", "description": "Descricao 2", "status": False},
            {"id": 3, "title": "Tarefa 3", "description": "Descricao 3", "status": False},
            {"id": 4, "title": "Tarefa 4", "description": "Descricao 4", "status": False},
            {"id": 5, "title": "Tarefa 5", "description": "Descricao 5", "status": False},
            {"id": 6, "title": "Tarefa 6", "description": "Descricao 6", "status": False}
        ]
        self.current_id = 3
    
    def get_all(self):
        return self.todos
    