import json
import redis
from app.config import Config
from app.services.todos_manager import TodoManager

r = redis.Redis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
)
todo_manager = TodoManager()


# caches in todo data
def cache_todos():
    todos = todo_manager.get_all()
    r.setex("todos", 300, json.dumps(todos))
    return todos


def cache_todo(todo):
    r.setex(f'todo:{todo["id"]}', 300, json.dumps(todo))


def get_cached_todo(todo_id):
    cached_todo = r.get(f"todo:{todo_id}")
    return json.loads(cached_todo) if cached_todo else None
