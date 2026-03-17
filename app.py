from flask import Flask, render_template_string

app = Flask(__name__)

# Sample student data
students = [
    {
        "name": "John Ivan Calves",
        "grade": 10,
        "section": "Zechariah",
        "photo": "https://i.pravatar.cc/150?img=1"  # Placeholder avatar
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

@app.route('/')
def home():
    return "Welcome to my Flask Student Dashboard API!"

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
            h1 {
                text-align: center;
                color: #2c3e50;
            }
            .cards {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
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
        </style>
    </head>
    <body>
        <h1>Student Dashboard</h1>
        <div class="cards">
            {% for student in students %}
            <div class="card">
                <img src="{{ student.photo }}" alt="Profile Picture">
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

if __name__ == "__main__":
    app.run(debug=True)
