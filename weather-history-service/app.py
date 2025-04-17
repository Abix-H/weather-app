from flask import Flask, request, jsonify
from models import Session, WeatherHistory
from datetime import datetime

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_weather():
    data = request.json
    if not data or 'city' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    city = data['city'].lower()
    date_str = data.get('date')
    try:
        log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        log_date = datetime.utcnow().date()

    log_time = datetime.utcnow().time()

    temp = data.get('temperature')
    humidity = data.get('humidity')
    description = data.get('description')

    session = Session()
    entry = WeatherHistory(
        city=city,
        date=log_date,
        time=log_time,  # ⬅️ Added
        temperature=temp,
        humidity=humidity,
        description=description
    )
    session.add(entry)
    session.commit()
    return jsonify({'message': 'Weather logged'}), 201

@app.route('/history', methods=['GET'])
def get_history():
    city = request.args.get('city')

    session = Session()

    if city:
        entries = session.query(WeatherHistory).filter_by(city=city.lower()).order_by(WeatherHistory.date, WeatherHistory.time).all()
    else:
        entries = session.query(WeatherHistory).order_by(WeatherHistory.city, WeatherHistory.date, WeatherHistory.time).all()

    return jsonify([
        {
            'city': e.city,
            'date': e.date.strftime('%Y-%m-%d'),
            'time': e.time.strftime('%H:%M:%S'),
            'temp': e.temperature,
            'humidity': e.humidity,
            'description': e.description
        }
        for e in entries
    ])


if __name__ == '__main__':
    app.run(debug=True, port=5004, host='0.0.0.0')
