function getWeather() {
    const city = document.getElementById("city-name").value;  // Get the city input value
    const weatherInfoDiv = document.getElementById("weather-info");  // Div to display weather info
    
    // Clear any previous weather info
    document.getElementById("temp").textContent = "";
    document.getElementById("humidity").textContent = "";
    document.getElementById("condition").textContent = "";
    document.getElementById("weather-icon").src = "";  // Optional: You can keep this line or remove it
    
    if (!city) {
        alert("Please enter a city name");
        return;
    }

    // Fetch weather data from the backend API
    const apiUrl = `/get_weather?city=${city}`;

    fetch(apiUrl)
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Extract relevant data from the response
            const temperature = data.temperature_celsius;  // Celsius temperature
            const humidity = data.humidity;
            const weatherDescription = data.weather;  // Weather description

            // Update the existing HTML elements
            document.getElementById("temp").textContent = `Temperature: ${temperature}°C`;  // Update temperature
            document.getElementById("humidity").textContent = `Humidity: ${humidity}%`;  // Update humidity
            document.getElementById("condition").textContent = `Condition: ${weatherDescription}`;  // Update condition

            // Show the weather info section
            weatherInfoDiv.style.display = "block";
        })
        .catch(error => {
            alert("Error fetching weather data");
            console.log(error);
        });
}
