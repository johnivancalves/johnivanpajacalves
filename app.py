from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Initial student data
students = [
    {
        "name": "John Ivan Calves",
        "grade": 10,
        "section": "Zechariah",
        "photo": "https://i.pravatar.cc/150?img=1"
    },
    {
        "name": "Maria Santos",
        "grade": 9,
        "section": "Gabriel",
        "photo": "https://i.pravatar.cc/150?img=2"
    },
    {
        "name": "Juan Dela Cruz",
        "grade": 11,
        "section": "Michael",
        "photo": "https://i.pravatar.cc/150?img=3"
    }
]

# Home route
@app.route('/')
def home():
    return redirect(url_for('student_dashboard'))

# Student dashboard route
@app.route('/students')
def student_dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                margin: 0;
                padding: 20px;
            }
            h1, h2 {
                text-align: center;
                color: #2c3e50;
            }
            .cards {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                margin-top: 20px;
            }
            .card {
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                padding: 20px;
                width: 250px;
                text-align: center;
                transition: transform 0.2s;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .card img {
                border-radius: 50%;
                width: 100px;
                height: 100px;
                object-fit: cover;
                margin-bottom: 15px;
            }
            .card p {
                margin: 5px 0;
                font-size: 16px;
            }
            .grade {
                font-weight: bold;
                color: #e74c3c;
            }
            .section {
                font-weight: bold;
                color: #3498db;
            }
            form {
                max-width: 400px;
                margin: 30px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            input[type=text], input[type=number], input[type=url] {
                width: 100%;
                padding: 8px;
                margin: 8px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            input[type=submit] {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
                font-size: 16px;
            }
            input[type=submit]:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <h1>Student Dashboard</h1>

        <!-- Form to add new student -->
        <form method="POST" action="{{ url_for('add_student') }}">
            <h2>Add New Student</h2>
            <input type="text" name="name" placeholder="Student Name" required>
            <input type="number" name="grade" placeholder="Grade" min="1" max="12" required>
            <input type="text" name="section" placeholder="Section" required>
            <input type="url" name="photo" placeholder="Photo URL" required>
            <input type="submit" value="Add Student">
        </form>

        <!-- Student Cards -->
        <div class="cards">
            {% for student in students %}
            <div class="card">
                <img src="{{ student.photo }}" alt="Profile Picture of {{ student.name }}">
                <p><strong>Name:</strong> {{ student.name }}</p>
                <p class="grade"><strong>Grade:</strong> {{ student.grade }}</p>
                <p class="section"><strong>Section:</strong> {{ student.section }}</p>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# Route to handle adding a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    grade = int(request.form['grade'])
    section = request.form['section']
    photo = request.form['photo']

    # Add new student to the list
    students.append({
        "name": name,
        "grade": grade,
        "section": section,
        "photo": photo
    })
    return redirect(url_for('student_dashboard'))

if __name__ == "__main__":
    app.run(debug=True)from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Initial student data
students = [
    {
        "name": "John Ivan Calves",
        "grade": 10,
        "section": "Zechariah",
        "photo": "https://i.pravatar.cc/150?img=1"
    },
    {
        "name": "Maria Santos",
        "grade": 9,
        "section": "Gabriel",
        "photo": "https://i.pravatar.cc/150?img=2"
    },
    {
        "name": "Juan Dela Cruz",
        "grade": 11,
        "section": "Michael",
        "photo": "https://i.pravatar.cc/150?img=3"
    }
]

# Home route
@app.route('/')
def home():
    return redirect(url_for('student_dashboard'))

# Student dashboard route
@app.route('/students')
def student_dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                margin: 0;
                padding: 20px;
            }
            h1, h2 {
                text-align: center;
                color: #2c3e50;
            }
            .cards {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                margin-top: 20px;
            }
            .card {
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                padding: 20px;
                width: 250px;
                text-align: center;
                transition: transform 0.2s;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .card img {
                border-radius: 50%;
                width: 100px;
                height: 100px;
                object-fit: cover;
                margin-bottom: 15px;
            }
            .card p {
                margin: 5px 0;
                font-size: 16px;
            }
            .grade {
                font-weight: bold;
                color: #e74c3c;
            }
            .section {
                font-weight: bold;
                color: #3498db;
            }
            form {
                max-width: 400px;
                margin: 30px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            input[type=text], input[type=number], input[type=url] {
                width: 100%;
                padding: 8px;
                margin: 8px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            input[type=submit] {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                width: 100%;
                font-size: 16px;
            }
            input[type=submit]:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <h1>Student Dashboard</h1>

        <!-- Form to add new student -->
        <form method="POST" action="{{ url_for('add_student') }}">
            <h2>Add New Student</h2>
            <input type="text" name="name" placeholder="Student Name" required>
            <input type="number" name="grade" placeholder="Grade" min="1" max="12" required>
            <input type="text" name="section" placeholder="Section" required>
            <input type="url" name="photo" placeholder="Photo URL" required>
            <input type="submit" value="Add Student">
        </form>

        <!-- Student Cards -->
        <div class="cards">
            {% for student in students %}
            <div class="card">
                <img src="{{ student.photo }}" alt="Profile Picture of {{ student.name }}">
                <p><strong>Name:</strong> {{ student.name }}</p>
                <p class="grade"><strong>Grade:</strong> {{ student.grade }}</p>
                <p class="section"><strong>Section:</strong> {{ student.section }}</p>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# Route to handle adding a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    grade = int(request.form['grade'])
    section = request.form['section']
    photo = request.form['photo']

    # Add new student to the list
    students.append({
        "name": name,
        "grade": grade,
        "section": section,
        "photo": photo
    })
    return redirect(url_for('student_dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
