from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask import send_from_directory

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename, cache_timeout=0)

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    print("Inside get_weather route")  # Ensure this is printed in the terminal

    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City not provided"}), 400

    # Get the API key from environment variables
    api_key = os.getenv('API_KEY') 
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404
    
    data = response.json()
    
    # Print the response data from the API to confirm it's correct
    print(f"Raw API data: {data}")

    kelvin_temp = data['main']['temp']
    celsius_temp = kelvin_temp - 273.15
    fahrenheit_temp = (kelvin_temp - 273.15) * 9/5 + 32
    
    # Prepare the response with the temperature in Celsius and Fahrenheit
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

    # Print the temperatures to confirm the conversion
    print(f"Temperature in Kelvin: {kelvin_temp}")
    print(f"Converted to Celsius: {celsius_temp}")
    print(f"Converted to Fahrenheit: {fahrenheit_temp}")
    
    # Return the new weather_data as the response
    return jsonify(weather_data)

if __name__ == "__main__":
    app.run(debug=True)  # Ensure the app is running in debug mode
