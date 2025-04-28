from flask import Flask, request, render_template, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    res = requests.post("http://user_service:5002/register", json={"username": username, "password": password})
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    res = requests.post("http://user_service:5002/login", json={"username": username, "password": password})
    if res.status_code == 200:
        session['user'] = username
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/weather')
def weather():
    if 'user' not in session:
        return redirect(url_for('index'))

    city = request.args.get('city')
    if not city:
        return "City is required", 400

    try:
        res = requests.get(f"http://weather:5001/api/weather?city={city}")
        data = res.json()
        return render_template('weather.html', data=data, city=city, user=session['user'])
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
