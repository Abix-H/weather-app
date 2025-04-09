function getWeather() {
    const city = document.getElementById("city-name").value;
    const weatherInfoDiv = document.getElementById("weather-info");

    // Clear previous weather info
    weatherInfoDiv.innerHTML = "";

    if (!city) {
        alert("Please enter a city name");
        return;
    }

    // Call the backend API to fetch weather data
    const apiUrl = `/get_weather?city=${city}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Extract weather data
            const temperature = data.main.temp;
            const humidity = data.main.humidity;
            const weatherDescription = data.weather[0].description;
            const weatherIcon = data.weather[0].icon;

            // Create HTML elements to display the data
            const tempElem = document.createElement("p");
            tempElem.textContent = `Temperature: ${temperature}°C`;

            const humidityElem = document.createElement("p");
            humidityElem.textContent = `Humidity: ${humidity}%`;

            const descriptionElem = document.createElement("p");
            descriptionElem.textContent = `Condition: ${weatherDescription}`;

            const iconElem = document.createElement("img");
            iconElem.src = `http://openweathermap.org/img/wn/${weatherIcon}.png`;
            iconElem.alt = weatherDescription;

            // Append elements to the weather info div
            weatherInfoDiv.appendChild(tempElem);
            weatherInfoDiv.appendChild(humidityElem);
            weatherInfoDiv.appendChild(descriptionElem);
            weatherInfoDiv.appendChild(iconElem);

            // Show the weather info section
            weatherInfoDiv.style.display = "block";
        })
        .catch(error => {
            alert("Error fetching weather data");
            console.log(error);
        });
}
