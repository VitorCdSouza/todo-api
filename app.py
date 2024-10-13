from flask import Flask, jsonify, request
from todos import TodoManager

app = Flask(__name__)
todo_manager = TodoManager()

# http://127.0.0.1:5000/todos 
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

# http://127.0.0.1:5000/todos/<id>
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = todo_manager.get_by_id(todo_id)
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)