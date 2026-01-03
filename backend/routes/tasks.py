from flask import Blueprint, request, jsonify
from db.database import save_task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/task", methods=["POST"])
def create_task():
    data = request.get_json()

    user_id = data.get("user_id", 1)
    task_type = data.get("task_type")
    task_data = data.get("task_data")

    if not task_type:
        return jsonify({"error": "task_type is required"}), 400

    save_task(user_id, task_type, task_data)

    return jsonify({
        "message": "Task created successfully",
        "task_type": task_type
    })
