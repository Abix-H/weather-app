from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime


app = Flask(__name__)
api_key = os.getenv("API_KEY")
# alert_service_url = os.getenv("ALERT_SERVICE_URL")

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City not provided"}), 400
    print(f"🔑 API_KEY (sanitized): {api_key}******" if api_key else "❌ API_KEY is missing")

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code != 200:
        print (f"Error: {response.status_code} - {response.text}")  # Debug print
        return jsonify({"error": "City not found"}), 404

    data = response.json()
    print(data)

    kelvin_temp = data['main']['temp']
    celsius_temp = kelvin_temp - 273.15

    weather_data = {
        'city': data['name'],
        'temperature_celsius': round(celsius_temp, 2),
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'timestamp': datetime.utcnow().isoformat()
    }

    try:
        history_service_url = os.getenv("HISTORY_SERVICE_URL", "http://history:5004/log")
        payload = {
            "city": data['name'],
            "date": datetime.utcnow().strftime('%Y-%m-%d'),
            "temperature": round(celsius_temp, 2),
            "humidity": data['main']['humidity'],
            "description": data['weather'][0]['description']
        }
        history_response = requests.post(history_service_url, json=payload)
        print(f"📜 History log response: {history_response.status_code}")
    except Exception as e:
        print(f"⚠️ Failed to log to history-service: {e}")

    return jsonify(weather_data)


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
