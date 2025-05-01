from flask import Flask, request, jsonify, send_from_directory
import csv
import os
from datetime import datetime
import requests

app = Flask(__name__)

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

HISTORY_SERVICE_URL = os.getenv("HISTORY_SERVICE_URL", "http://history:5004/history")

@app.route('/export', methods=['GET'])
def export_csv():
    city = request.args.get('city')

    try:
        params = {'city': city} if city else {}
        response = requests.get(HISTORY_SERVICE_URL, params=params)

        if response.status_code != 200:
            return jsonify({'error': f'history-service returned {response.status_code}'}), 502

        history_data = response.json()

        if not history_data:
            return jsonify({'error': 'No data found'}), 404

    except Exception as e:
        return jsonify({'error': 'Failed to contact history-service', 'detail': str(e)}), 500

    # Determine filename
    name = city.lower() if city else "all_cities"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_weather_{timestamp}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    # Generate CSV
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['city', 'date', 'time', 'temp', 'humidity', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(history_data)

    return jsonify({
        'message': 'CSV export generated',
        'download_url': f'/download/{filename}'
    })

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(EXPORT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')
