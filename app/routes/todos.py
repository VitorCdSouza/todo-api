from flask import Blueprint, jsonify, request
from app.services.todos_manager import TodoManager
from app.cache.redis_cache import cache_todos, cache_todo, get_cached_todo

bp = Blueprint("todos", __name__, url_prefix="/todos")

todo_manager = TodoManager()


# GET http://127.0.0.1:5000/todos/
# params: ?per_page= nor ?page= 
@bp.route("/", methods=["GET"])
def get_todos():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 3, type=int)

    todos = cache_todos()
    start = (page - 1) * per_page
    end = start + per_page
    paginated_todos = todos[start:end]

    return jsonify(
        {
            "todos": paginated_todos,
            "page": page,
            "per_page": per_page,
            "total": len(todos),
        }
    )


# GET http://127.0.0.1:5000/todos/<id>
@bp.route("/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = get_cached_todo(todo_id) or todo_manager.get_by_id(todo_id)
    if todo:
        cache_todo(todo)
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404


# POST http://127.0.0.1:5000/todos/
@bp.route("/", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "title" not in data or not data["title"].strip():
        return jsonify({"error": "O título da tarefa é obrigatório"}), 400

    status = data.get("status", "pendente")
    new_todo = todo_manager.create(
        data["title"],
        data.get("description", ""),
        status
    )

    cache_todos()

    return jsonify(new_todo), 201


# PUT http://127.0.0.1:5000/todos/<id>
@bp.route("/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todo_manager.get_by_id(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()
    updated_todo = todo_manager.update(
        todo_id, data.get("title"), data.get("description"), data.get("status")
    )

    if updated_todo:
        cache_todos()
        cache_todo(updated_todo)
        return jsonify(updated_todo)

    return jsonify(updated_todo)


# DELETE http://127.0.0.1:5000/todos/<id>
@bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    success = todo_manager.delete(todo_id)

    if success:
        cache_todos()
        return jsonify({"message": "Todo deleted"}), 200

    return jsonify({"error": "Todo not found"}), 404
