from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Custom JSON response function ---
def create_response(status: str, message: str, data=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    })

# --- Home route ---
@app.route('/', methods=['GET'])
def home():
    return create_response(
        status="success",
        message="Welcome to my Flask API!",
        data={
            "endpoints": {
                "/": "Home route",
                "/student": "Get student information",
                "/student/<name>": "Get student info by name (optional)"
            }
        }
    )

# --- Student info route ---
@app.route('/student', methods=['GET'])
def get_student():
    student_data = {
        "name": "Your Name",
        "grade": 10,
        "section": "Zechariah"
    }
    return create_response(status="success", message="Student info retrieved", data=student_data)

# --- Optional: Dynamic student route ---
@app.route('/student/<name>', methods=['GET'])
def get_student_by_name(name):
    # Example: In real app, you might fetch from a database
    student_data = {
        "name": name,
        "grade": 10,
        "section": "Zechariah"
    }
    return create_response(status="success", message=f"Student info for {name}", data=student_data)

# --- Error handling for 404 ---
@app.errorhandler(404)
def not_found(error):
    return create_response(status="error", message="Resource not found"), 404

# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=True)
