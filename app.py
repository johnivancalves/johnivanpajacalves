from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory "database"
students = []

# --- Dashboard Route ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', students=students)

# --- Add Student ---
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    grade = request.form.get('grade')
    section = request.form.get('section')

    if not name or not grade or not section:
        return redirect(url_for('dashboard'))

    student_id = len(students) + 1
    students.append({
        "id": student_id,
        "name": name,
        "grade": grade,
        "section": section
    })
    return redirect(url_for('dashboard'))

# --- Edit Student Form ---
@app.route('/edit/<int:student_id>')
def edit_student_form(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return redirect(url_for('dashboard'))
    return render_template('edit.html', student=student)

# --- Update Student ---
@app.route('/update/<int:student_id>', methods=['POST'])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        student['name'] = request.form.get('name')
        student['grade'] = request.form.get('grade')
        student['section'] = request.form.get('section')
    return redirect(url_for('dashboard'))

# --- Delete Student ---
@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return redirect(url_for('dashboard'))

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
