# app.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = "f05802295e2c350701b46feb0ae4e2ef"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

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
    
    # Make request to OpenWeatherMap API
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": "City not found or API error"}), 404
    
    data = response.json()
    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    }
    return jsonify(weather_info)

if __name__ == '__main__':
    app.run(debug=True)

