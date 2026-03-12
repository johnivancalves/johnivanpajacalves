from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# --- Sample in-memory data ---
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# --- Base Style ---
STYLE = """
<style>
body{
    font-family: Arial;
    background:#f4f6f9;
    padding:30px;
}
.container{
    max-width:900px;
    margin:auto;
    background:white;
    padding:20px;
    border-radius:8px;
    box-shadow:0 0 10px rgba(0,0,0,0.1);
}
h1,h2{
    text-align:center;
}
table{
    width:100%;
    border-collapse:collapse;
}
th,td{
    padding:10px;
    border-bottom:1px solid #ddd;
    text-align:center;
}
th{
    background:#007BFF;
    color:white;
}
.pass{
    color:green;
    font-weight:bold;
}
.fail{
    color:red;
    font-weight:bold;
}
.btn{
    padding:6px 10px;
    text-decoration:none;
    border-radius:4px;
    color:white;
}
.edit{background:orange;}
.delete{background:red;}
.add{background:green;}
.summary{background:#007BFF;}
.card{
    display:inline-block;
    width:23%;
    padding:15px;
    margin:1%;
    background:#007BFF;
    color:white;
    border-radius:6px;
    text-align:center;
}
input{
    padding:8px;
    width:95%;
}
form{
    margin-top:20px;
}
</style>
"""

# --- Home ---
@app.route('/')
def home():
    return redirect(url_for('list_students'))

# --- View Students ---
@app.route('/students')
def list_students():
    html = STYLE + """
    <div class="container">
    <h1>Student Management System</h1>

    <a class="btn add" href="/add_student_form">Add Student</a>
    <a class="btn summary" href="/summary_page">Summary</a>

    <br><br>

    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Grade</th>
            <th>Section</th>
            <th>Remarks</th>
            <th>Actions</th>
        </tr>

        {% for s in students %}
        <tr>
            <td>{{s.id}}</td>
            <td>{{s.name}}</td>
            <td>{{s.grade}}</td>
            <td>{{s.section}}</td>
            <td class="{{'pass' if s.grade>=75 else 'fail'}}">
                {{ 'Pass' if s.grade>=75 else 'Fail' }}
            </td>
            <td>
                <a class="btn edit" href="/edit_student/{{s.id}}">Edit</a>
                <a class="btn delete" onclick="return confirm('Delete student?')" href="/delete_student/{{s.id}}">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    </div>
    """
    return render_template_string(html, students=students)

# --- Add Form ---
@app.route('/add_student_form')
def add_student_form():
    html = STYLE + """
    <div class="container">
    <h2>Add Student</h2>

    <form action="/add_student" method="POST">
        Name:<br>
        <input type="text" name="name" required><br><br>

        Grade:<br>
        <input type="number" name="grade" min="0" max="100" required><br><br>

        Section:<br>
        <input type="text" name="section" required><br><br>

        <button class="btn add">Add Student</button>
    </form>

    <br>
    <a href="/students">Back</a>
    </div>
    """
    return render_template_string(html)

# --- Add Student ---
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    grade = int(request.form['grade'])
    section = request.form['section']

    new_id = len(students) + 1

    students.append({
        "id": new_id,
        "name": name,
        "grade": grade,
        "section": section
    })

    return redirect(url_for('list_students'))

# --- Edit Student ---
@app.route('/edit_student/<int:id>', methods=['GET','POST'])
def edit_student(id):
    student = next((s for s in students if s["id"]==id),None)

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        return redirect(url_for('list_students'))

    html = STYLE + """
    <div class="container">
    <h2>Edit Student</h2>

    <form method="POST">
        Name:<br>
        <input type="text" name="name" value="{{student.name}}"><br><br>

        Grade:<br>
        <input type="number" name="grade" value="{{student.grade}}"><br><br>

        Section:<br>
        <input type="text" name="section" value="{{student.section}}"><br><br>

        <button class="btn edit">Update</button>
    </form>

    <br>
    <a href="/students">Back</a>
    </div>
    """
    return render_template_string(html, student=student)

# --- Delete ---
@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

# --- Summary Dashboard ---
@app.route('/summary_page')
def summary_page():
    grades=[s['grade'] for s in students]

    total=len(students)
    avg=sum(grades)/len(grades) if grades else 0
    passed=len([g for g in grades if g>=75])
    failed=total-passed

    html = STYLE + """
    <div class="container">
    <h2>Class Summary</h2>

    <div class="card">
        <h3>Total Students</h3>
        <h1>{{total}}</h1>
    </div>

    <div class="card">
        <h3>Average Grade</h3>
        <h1>{{avg}}</h1>
    </div>

    <div class="card">
        <h3>Passed</h3>
        <h1>{{passed}}</h1>
    </div>

    <div class="card">
        <h3>Failed</h3>
        <h1>{{failed}}</h1>
    </div>

    <br><br>
    <a href="/students">Back</a>
    </div>
    """

    return render_template_string(html,total=total,avg=round(avg,2),passed=passed,failed=failed)

if __name__ == '__main__':
    app.run(debug=True)
