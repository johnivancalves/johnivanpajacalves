from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

BOOTSTRAP = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
"""

# Home
@app.route('/')
def home():
    return redirect(url_for('students_page'))

# Student List
@app.route('/students')
def students_page():
    html = BOOTSTRAP + """
    <div class="container mt-5">

    <h2 class="text-center mb-4">Student Management System</h2>

    <div class="mb-3">
        <a href="/add_student_form" class="btn btn-success">Add Student</a>
        <a href="/summary_page" class="btn btn-primary">View Summary</a>
    </div>

    <table class="table table-striped table-bordered">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Grade</th>
                <th>Section</th>
                <th>Remarks</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody>
        {% for s in students %}
        <tr>
            <td>{{s.id}}</td>
            <td>{{s.name}}</td>
            <td>{{s.grade}}</td>
            <td>{{s.section}}</td>
            <td>
            {% if s.grade >= 75 %}
                <span class="badge bg-success">Pass</span>
            {% else %}
                <span class="badge bg-danger">Fail</span>
            {% endif %}
            </td>
            <td>
                <a href="/edit_student/{{s.id}}" class="btn btn-warning btn-sm">Edit</a>
                <a href="/delete_student/{{s.id}}" class="btn btn-danger btn-sm"
                onclick="return confirm('Delete student?')">Delete</a>
            </td>
        </tr>
        {% endfor %}
        </tbody>
    </table>

    </div>
    """
    return render_template_string(html, students=students)

# Add Student Form
@app.route('/add_student_form')
def add_student_form():
    html = BOOTSTRAP + """
    <div class="container mt-5">

    <h2>Add Student</h2>

    <form action="/add_student" method="POST">

        <div class="mb-3">
            <label>Name</label>
            <input class="form-control" type="text" name="name" required>
        </div>

        <div class="mb-3">
            <label>Grade</label>
            <input class="form-control" type="number" name="grade" min="0" max="100" required>
        </div>

        <div class="mb-3">
            <label>Section</label>
            <input class="form-control" type="text" name="section" required>
        </div>

        <button class="btn btn-success">Add Student</button>
        <a href="/students" class="btn btn-secondary">Back</a>

    </form>
    </div>
    """
    return render_template_string(html)

# Add Student
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form["name"]
    grade = int(request.form["grade"])
    section = request.form["section"]

    new_id = len(students) + 1

    students.append({
        "id": new_id,
        "name": name,
        "grade": grade,
        "section": section
    })

    return redirect(url_for('students_page'))

# Edit Student
@app.route('/edit_student/<int:id>', methods=['GET','POST'])
def edit_student(id):

    student = next((s for s in students if s["id"]==id),None)

    if request.method == "POST":
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]

        return redirect(url_for('students_page'))

    html = BOOTSTRAP + """
    <div class="container mt-5">

    <h2>Edit Student</h2>

    <form method="POST">

        <div class="mb-3">
            <label>Name</label>
            <input class="form-control" name="name" value="{{student.name}}">
        </div>

        <div class="mb-3">
            <label>Grade</label>
            <input class="form-control" name="grade" type="number" value="{{student.grade}}">
        </div>

        <div class="mb-3">
            <label>Section</label>
            <input class="form-control" name="section" value="{{student.section}}">
        </div>

        <button class="btn btn-warning">Update</button>
        <a href="/students" class="btn btn-secondary">Back</a>

    </form>
    </div>
    """

    return render_template_string(html, student=student)

# Delete Student
@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('students_page'))

# Summary Page
@app.route('/summary_page')
def summary_page():

    grades = [s['grade'] for s in students]

    total = len(students)
    avg = sum(grades)/len(grades) if grades else 0
    passed = len([g for g in grades if g>=75])
    failed = total - passed

    html = BOOTSTRAP + """
    <div class="container mt-5">

    <h2 class="text-center mb-4">Class Summary</h2>

    <div class="row text-center">

        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                <h4>Total Students</h4>
                <h2>{{total}}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                <h4>Passed</h4>
                <h2>{{passed}}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body">
                <h4>Failed</h4>
                <h2>{{failed}}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card bg-dark text-white">
                <div class="card-body">
                <h4>Average</h4>
                <h2>{{avg}}</h2>
                </div>
            </div>
        </div>

    </div>

    <br>
    <a href="/students" class="btn btn-secondary">Back</a>

    </div>
    """

    return render_template_string(html,total=total,avg=round(avg,2),passed=passed,failed=failed)

if __name__ == "__main__":
    app.run(debug=True)
