from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import limiter
from app.services.todos_manager import TodoManager
from app.cache.redis_cache import cache_todos, cache_todo, get_cached_todo


bp = Blueprint("todos", __name__, url_prefix="/todos")

todo_manager = TodoManager()


# GET http://127.0.0.1:5000/todos/
# params: ?per_page= nor ?page=
@limiter.limit("50 per minute")
@bp.route("/", methods=["GET"])
@jwt_required()
def get_todos():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 3, type=int)

    user_id = get_jwt_identity()
    todos = todo_manager.get_by_user_id(user_id)

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
@limiter.limit("50 per minute")
@bp.route("/<int:todo_id>", methods=["GET"])
@jwt_required()
def get_todo(todo_id):
    user_id = get_jwt_identity()
    todo = get_cached_todo(todo_id) or todo_manager.get_by_id(todo_id, user_id)
    if todo:
        cache_todo(todo)
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404


# POST http://127.0.0.1:5000/todos/
@limiter.limit("20 per minute")
@bp.route("/", methods=["POST"])
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or "title" not in data or not data["title"].strip():
        return jsonify({"error": "O título da tarefa é obrigatório"}), 400

    status = data.get("status", "pendente")
    new_todo = todo_manager.create(
        data["title"],
        data.get("description", ""),
        status,
        user_id=user_id
    )

    cache_todos()

    return jsonify(new_todo), 201


# PUT http://127.0.0.1:5000/todos/<id>
@limiter.limit("50 per minute")
@bp.route("/<int:todo_id>", methods=["PUT"])
@jwt_required()
def update_todo(todo_id):
    user_id = get_jwt_identity()
    todo = todo_manager.get_by_id(todo_id, user_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    updated_todo = todo_manager.update_status(todo_id, new_status)

    if updated_todo:
        cache_todos()
        cache_todo(updated_todo)
        return jsonify(updated_todo)

    return jsonify({"error": "Failed to update todo"}), 400


# DELETE http://127.0.0.1:5000/todos/<id>
@limiter.limit("20 per minute")
@bp.route("/<int:todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id):   
    user_id = get_jwt_identity()
    success = todo_manager.delete(todo_id, user_id)

    if success:
        cache_todos()
        return jsonify({"message": "Todo deleted"}), 200

    return jsonify({"error": "Todo not found"}), 404
