from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "students.db"

# --- Initialize Database ---
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        address TEXT,
        contact TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

BOOTSTRAP = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
"""

# --- Dashboard ---
@app.route('/')
def dashboard():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()

    total = len(students)

    html = BOOTSTRAP + """
    <div class="container mt-4">

    <!-- NAVBAR -->
    <nav class="navbar navbar-dark bg-dark rounded">
        <div class="container-fluid">
            <span class="navbar-brand">🎓 Student Information Dashboard</span>
        </div>
    </nav>

    <br>

    <!-- SUMMARY -->
    <div class="card bg-primary text-white text-center p-3 mb-4">
        <h4>Total Students</h4>
        <h1>{{total}}</h1>
    </div>

    <!-- ADD BUTTON -->
    <button class="btn btn-success mb-3" data-bs-toggle="modal" data-bs-target="#addModal">
        + Add Student
    </button>

    <!-- TABLE -->
    <table class="table table-bordered table-striped">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
                <th>Gender</th>
                <th>Address</th>
                <th>Contact</th>
                <th>Action</th>
            </tr>
        </thead>

        <tbody>
        {% for s in students %}
        <tr>
            <td>{{s[0]}}</td>
            <td>{{s[1]}}</td>
            <td>{{s[2]}}</td>
            <td>{{s[3]}}</td>
            <td>{{s[4]}}</td>
            <td>{{s[5]}}</td>
            <td>
                <a href="/delete/{{s[0]}}" class="btn btn-danger btn-sm"
                   onclick="return confirm('Delete student?')">Delete</a>
            </td>
        </tr>
        {% endfor %}
        </tbody>
    </table>

    <!-- ADD MODAL -->
    <div class="modal fade" id="addModal">
        <div class="modal-dialog">
            <div class="modal-content">

                <form method="POST" action="/add">

                <div class="modal-header">
                    <h5 class="modal-title">Add Student</h5>
                    <button class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">

                    <input class="form-control mb-2" name="name" placeholder="Full Name" required>
                    <input class="form-control mb-2" name="age" type="number" placeholder="Age" required>
                    
                    <select class="form-control mb-2" name="gender" required>
                        <option value="">Select Gender</option>
                        <option>Male</option>
                        <option>Female</option>
                    </select>

                    <input class="form-control mb-2" name="address" placeholder="Address" required>
                    <input class="form-control mb-2" name="contact" placeholder="Contact Number" required>

                </div>

                <div class="modal-footer">
                    <button class="btn btn-success">Save</button>
                </div>

                </form>

            </div>
        </div>
    </div>

    </div>
    """

    return render_template_string(html, students=students, total=total)

# --- Add Student ---
@app.route('/add', methods=['POST'])
def add():
    data = (
        request.form['name'],
        request.form['age'],
        request.form['gender'],
        request.form['address'],
        request.form['contact']
    )

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO students(name,age,gender,address,contact) VALUES(?,?,?,?,?)", data)
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

# --- Delete ---
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
