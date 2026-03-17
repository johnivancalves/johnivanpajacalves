from flask import Flask, jsonify, request

app = Flask(__name__)

# --- In-memory "database" ---
students = []

# --- Helper function for consistent JSON response ---
def create_response(status: str, message: str, data=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    })

# --- Home Route ---
@app.route('/', methods=['GET'])
def home():
    return create_response(
        status="success",
        message="Welcome to the Student Information System API",
        data={
            "endpoints": {
                "/students [GET]": "Get all students",
                "/students [POST]": "Add a new student",
                "/students/<id> [GET]": "Get a student by ID",
                "/students/<id> [PUT]": "Update a student by ID",
                "/students/<id> [DELETE]": "Delete a student by ID"
            }
        }
    )

# --- Get All Students ---
@app.route('/students', methods=['GET'])
def get_students():
    return create_response(status="success", message=f"{len(students)} students found", data=students)

# --- Add New Student ---
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "grade", "section")):
        return create_response(status="error", message="Missing student information"), 400
    
    student_id = len(students) + 1
    student = {
        "id": student_id,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(student)
    return create_response(status="success", message="Student added successfully", data=student), 201

# --- Get Student by ID ---
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return create_response(status="error", message="Student not found"), 404
    return create_response(status="success", message="Student found", data=student)

# --- Update Student by ID ---
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return create_response(status="error", message="Student not found"), 404

    data = request.get_json()
    student["name"] = data.get("name", student["name"])
    student["grade"] = data.get("grade", student["grade"])
    student["section"] = data.get("section", student["section"])

    return create_response(status="success", message="Student updated successfully", data=student)

# --- Delete Student by ID ---
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return create_response(status="error", message="Student not found"), 404

    students = [s for s in students if s["id"] != student_id]
    return create_response(status="success", message="Student deleted successfully", data=student)

# --- Error Handling ---
@app.errorhandler(404)
def not_found(error):
    return create_response(status="error", message="Resource not found"), 404

if __name__ == "__main__":
    app.run(debug=True)
