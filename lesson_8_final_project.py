from flask import Flask, request, jsonify


app = Flask(__name__)
tasks = {}
MAX_ID = 0


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_specific_task(task_id):
    if task_id in tasks:
        return jsonify(tasks[task_id]), 200
    else:
        return jsonify({"error": "task not found"}), 404     


@app.route("/tasks", methods=["POST"])
def add_task():
    global MAX_ID
    data = request.get_json()
    if not data or "title" not in data or "description" not in data:
       return jsonify({"error": "Bad Request, data must include title and description"}), 400
    MAX_ID += 1
    tasks[MAX_ID] = {"completed": False, "description": data["description"] , "id": MAX_ID , "title" : data["title"]}
    return jsonify(tasks[MAX_ID]), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def change_description_and_title(task_id):
    if task_id in tasks:
        data = request.get_json()
        if not data or "title" not in data or "description" not in data:
            return jsonify({"error": "Bad Request, data must include title and description"}), 400
        tasks[task_id] = {"completed": False , "description": data["description"] , "id": task_id , "title": data["title"]}
        return jsonify(tasks[task_id]), 200
    else:
        return jsonify({"error" : "task not found"}), 404


@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def change_status_to_completed(task_id):
    if task_id in tasks:
        dict_for_completed = {}
        tasks[task_id] ["completed"] = True
        dict_for_completed = {"message": "task marked as completed" , "task" : tasks[task_id]}
        return jsonify(dict_for_completed), 200
    else:
        return jsonify({"error" : "task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def deleteStudent(task_id):
    if task_id in tasks:
       del tasks[task_id]
    return jsonify({"message": "task deleted"}), 200


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)