from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
from dotenv import load_dotenv
import os

# Initialize the Flask app
app = Flask(__name__)
print(f"Test 1")
# Load environment variables from .env file
load_dotenv()
print(f"Test 2")
# Optional: serve static files (CSS/JS)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename, cache_timeout=0)
print(f"Test 3")
# Home route
@app.route('/')
def home():
    return render_template('index.html')
print(f"Test 4")
# Get weather data route
@app.route('/get_weather', methods=['GET'])
def get_weather():
    print("Inside get_weather route")  # Debug print

    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City not provided"}), 400

    # Get API key from environment variables
    api_key = os.getenv('API_KEY')
    if not api_key:
        return jsonify({"error": "API key not set in .env"}), 500

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()
    print(f"Raw API data: {data}")  # Debug print

    kelvin_temp = data['main']['temp']
    celsius_temp = kelvin_temp - 273.15
    fahrenheit_temp = (kelvin_temp - 273.15) * 9 / 5 + 32

    weather_data = {
        'city': data['name'],
        'country': data['sys']['country'],
        'temperature_kelvin': kelvin_temp,
        'temperature_celsius': round(celsius_temp, 2),
        'temperature_fahrenheit': round(fahrenheit_temp, 2),
        'weather': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'clouds': data['clouds']['all']
    }

    print(f"Temperature in Kelvin: {kelvin_temp}")
    print(f"Converted to Celsius: {celsius_temp}")
    print(f"Converted to Fahrenheit: {fahrenheit_temp}")

    return jsonify(weather_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
