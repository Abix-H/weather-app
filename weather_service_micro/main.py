from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
OPENWEATHER_API_KEY = os.getenv("API_KEY")

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("weather"):
            weather_condition = data["weather"][0]["description"]
            try:
                requests.post("http://notification_service:5003/notify", json={"city": city, "weather": weather_condition})
            except:
                pass

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
