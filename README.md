# Weather App

A simple Flask-based web application that allows users to get weather information for a city.

## Setup

1. Clone the repository.

2. Install dependencies:
- You need to install the required Python packages. Run the following command in your project directory:
  ```
  pip install -r requirements.txt
  ```

3. Create a `.env` file and add your OpenWeather API key:
- In the root of your project directory, create a `.env` file and add the following line:
  ```
  API_KEY=your_api_key
  ```
- Replace `your_api_key` with your actual OpenWeather API key.

4. Run the app:
- Start the Flask application by running this command:
  ```
  python main.py
  ```
- The app will be accessible at `http://127.0.0.1:5000/` in your browser.
