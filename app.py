from flask import Flask, jsonify, request
from todos import TodoManager, TodoStatus

app = Flask(__name__)
todo_manager = TodoManager()

# GET http://127.0.0.1:5000/todos 
# params: ?per_page= nor ?page=
@app.route('/todos', methods=['GET'])
def get_todos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)

    todos = todo_manager.get_all()
    start = (page - 1) * per_page
    end = start + per_page
    paginated_todos = todos[start:end]
    
    return jsonify({
        "todos": paginated_todos,
        "page": page,
        "per_page": per_page,
        "total": len(todos)
    })

# GET http://127.0.0.1:5000/todos/<id>
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = todo_manager.get_by_id(todo_id)
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

# POST http://127.0.0.1:5000/todos/
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    status = data.get('status', TodoStatus.PENDENTE.value)
    if status not in TodoStatus._value2member_map_:
        return jsonify({"error": "Invalid status"}), 400

    new_todo = todo_manager.create(
        title=data['title'],
        description=data.get('description', ''),
        status=status
    )
    return jsonify(new_todo), 201

# PUT http://127.0.0.1:5000/todos/<id>
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = todo_manager.get_by_id(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()
    status = data.get('status')
    if status and status not in TodoStatus._value2member_map_:
        return jsonify({"error": "Invalid status"}), 400

    updated_todo = todo_manager.update(
        todo_id=todo_id,
        title=data.get('title'),
        description=data.get('description'),
        status=status
    )
    return jsonify(updated_todo)

# DELETE http://127.0.0.1:5000/todos/<id>
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    success = todo_manager.delete(todo_id)
    if success:
        return jsonify({"message": "Todo deleted"}), 200
    return jsonify({"error": "Todo not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)