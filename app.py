from flask import Flask, render_template_string, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "admin123"
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

    # Admin table
    c.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # Default admin
    c.execute("SELECT * FROM admin")
    if not c.fetchone():
        c.execute("INSERT INTO admin(username,password) VALUES(?,?)", ("admin", "admin123"))

    conn.commit()
    conn.close()

init_db()

BOOTSTRAP = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
"""

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", (user, pw))
        admin = c.fetchone()
        conn.close()

        if admin:
            session['admin'] = user
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Login"

    return BOOTSTRAP + """
    <div class="container mt-5">
        <h3>Admin Login</h3>
        <form method="POST">
            <input class="form-control mb-2" name="username" placeholder="Username" required>
            <input class="form-control mb-2" type="password" name="password" placeholder="Password" required>
            <button class="btn btn-dark">Login</button>
        </form>
    </div>
    """

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

# ---------------- DASHBOARD ----------------
@app.route('/')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()

    total = len(students)

    html = BOOTSTRAP + """
    <div class="container mt-4">

    <nav class="navbar navbar-dark bg-dark">
        <span class="navbar-brand">Student Dashboard</span>
        <a href="/logout" class="btn btn-danger">Logout</a>
    </nav>

    <br>

    <div class="card bg-primary text-white text-center p-3 mb-4">
        <h4>Total Students</h4>
        <h1>{{total}}</h1>
    </div>

    <button class="btn btn-success mb-3" data-bs-toggle="modal" data-bs-target="#addModal">
        + Add Student
    </button>

    <table class="table table-bordered">
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
                <button class="btn btn-warning btn-sm" data-bs-toggle="modal" data-bs-target="#edit{{s[0]}}">
                    Edit
                </button>

                <a href="/delete/{{s[0]}}" class="btn btn-danger btn-sm"
                   onclick="return confirm('Delete student?')">Delete</a>
            </td>
        </tr>

        <!-- EDIT MODAL -->
        <div class="modal fade" id="edit{{s[0]}}">
            <div class="modal-dialog">
                <div class="modal-content">

                    <form method="POST" action="/edit/{{s[0]}}">

                    <div class="modal-header">
                        <h5>Edit Student</h5>
                        <button class="btn-close" data-bs-dismiss="modal"></button>
                    </div>

                    <div class="modal-body">
                        <input class="form-control mb-2" name="name" value="{{s[1]}}" required>
                        <input class="form-control mb-2" name="age" type="number" value="{{s[2]}}" required>

                        <select class="form-control mb-2" name="gender">
                            <option {{'selected' if s[3]=='Male' else ''}}>Male</option>
                            <option {{'selected' if s[3]=='Female' else ''}}>Female</option>
                        </select>

                        <input class="form-control mb-2" name="address" value="{{s[4]}}" required>
                        <input class="form-control mb-2" name="contact" value="{{s[5]}}" required>
                    </div>

                    <div class="modal-footer">
                        <button class="btn btn-primary">Update</button>
                    </div>

                    </form>

                </div>
            </div>
        </div>

        {% endfor %}
        </tbody>
    </table>

    <!-- ADD MODAL -->
    <div class="modal fade" id="addModal">
        <div class="modal-dialog">
            <div class="modal-content">

                <form method="POST" action="/add">

                <div class="modal-header">
                    <h5>Add Student</h5>
                    <button class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body">
                    <input class="form-control mb-2" name="name" required>
                    <input class="form-control mb-2" name="age" type="number" required>

                    <select class="form-control mb-2" name="gender">
                        <option>Male</option>
                        <option>Female</option>
                    </select>

                    <input class="form-control mb-2" name="address" required>
                    <input class="form-control mb-2" name="contact" required>
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

# ---------------- ADD ----------------
@app.route('/add', methods=['POST'])
def add():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO students(name,age,gender,address,contact) VALUES(?,?,?,?,?)",
              (request.form['name'], request.form['age'], request.form['gender'],
               request.form['address'], request.form['contact']))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# ---------------- EDIT ----------------
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        UPDATE students
        SET name=?, age=?, gender=?, address=?, contact=?
        WHERE id=?
    """, (request.form['name'], request.form['age'], request.form['gender'],
          request.form['address'], request.form['contact'], id))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# ---------------- DELETE ----------------
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
