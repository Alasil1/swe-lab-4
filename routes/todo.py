from flask import Blueprint, request, jsonify
from middleware.auth import authenticate_token
todo_bp = Blueprint("todo", __name__)
todo = []  

@todo_bp.before_request
def before_request():
    authenticate_token()


@todo_bp.route("/", methods=["GET"])
def get_todo():
    return jsonify(todo)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    return jsonify(task)

@todo_bp.route("/", methods=["POST"])
def add_todo():
    new_todo = {
        "id": len(todo) + 1,
        "title": request.json.get("title"),
        "completed": request.json.get("completed",False),
    }
    todo.append(new_todo)
    return jsonify(new_todo), 201


@todo_bp.route("/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    task_to_update = next((t for t in todo if t['id'] == todo_id), None)
    if not task_to_update:
        return jsonify({"error": "Todo not found"}), 404
    task_to_update["title"] = request.json.get("title",task_to_update["title"])
    task_to_update["completed"] = request.json.get("completed",task_to_update["completed"])


    return jsonify(task_to_update)


@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todo
    todo = [t for t in todo if t['id'] != todo_id]
    return jsonify({"message": "Todo deleted"}), 204
