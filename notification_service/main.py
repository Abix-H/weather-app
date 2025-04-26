from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    city = data.get('city')
    weather = data.get('weather')

    if 'storm' in weather.lower() or 'extreme' in weather.lower():
        print(f"ALERT: Extreme weather in {city}! Condition: {weather}")
        return jsonify({"message": f"Notification sent for {city}"}), 200

    return jsonify({"message": "No alert needed"}), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
