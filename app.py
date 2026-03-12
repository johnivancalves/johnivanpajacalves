# app.py
from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Load local .env file (ignored on Render)
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

if not API_KEY:
    raise ValueError("No API_KEY found. Set it in .env or Render environment variables.")

# Home route
@app.route('/')
def home():
    return "Welcome to my Weather Flask API!"

# GET weather by city
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Please provide a city name"}), 400

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()  # Raise error for bad status codes
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Request error: {req_err}"}), 500

    data = response.json()
    weather_info = {
        "city": data.get("name"),
        "temperature": data.get("main", {}).get("temp"),
        "description": data.get("weather", [{}])[0].get("description")
    }
    return jsonify(weather_info)

if __name__ == '__main__':
    # Use 0.0.0.0 for Render and port from environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
