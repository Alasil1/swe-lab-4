from flask import Blueprint, request, jsonify
from middleware.auth import authenticate_token

todo_bp = Blueprint("todo", __name__)
todo = []  

@todo_bp.before_request
def before_request():
    authenticate_token()


@todo_bp.route("/", methods=["GET"])
def get_todo():
    return jsonify(todo), 200


@todo_bp.route("/", methods=["POST"])
def add_todo():
    data = request.json
    if not data or not 'task' in data:
        return jsonify({"error": "Task is required"}), 400

    new_todo = {
        "id": len(todo) + 1,
        "task": data["task"],
        "done": False
    }
    todo.append(new_todo)
    return jsonify(new_todo), 201


@todo_bp.route("/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    task_to_update = next((t for t in todo if t['id'] == todo_id), None)

    if not task_to_update:
        return jsonify({"error": "Todo not found"}), 404
    if 'task' in data:
        task_to_update['task'] = data['task']
    if 'done' in data:
        task_to_update['done'] = data['done']

    return jsonify(task_to_update), 200


@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todo
    task_to_delete = next((t for t in todo if t['id'] == todo_id), None)

    if not task_to_delete:
        return jsonify({"error": "Todo not found"}), 404

    todo = [t for t in todo if t['id'] != todo_id]
    return jsonify({"message": "Todo deleted"}), 204
