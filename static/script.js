document.addEventListener('DOMContentLoaded', () => {
    const getWeatherBtn = document.getElementById('get-weather');  // Button to trigger the weather fetch
    const cityInput = document.getElementById('city-name');  // Input field for the city name
    const weatherInfoDiv = document.getElementById('weather-info');  // where weather info will be displayed
    function getWeather() {
        const city = document.getElementById('city-name').value;
        
        if (!city) {
            alert('Please enter a city');
            return;
        }
    
        fetch(`/get_weather?city=${city}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('weather-info').style.display = 'block';
                    document.getElementById('temp').textContent = `Temperature: ${data.temperature_celsius}°C`;
                    document.getElementById('humidity').textContent = `Humidity: ${data.humidity}%`;
                    document.getElementById('condition').textContent = `Condition: ${data.weather}`;
                }
            })
            .catch(error => {
                alert('Error fetching weather data');
            });
    }
    
    // Event listener for the button click
    getWeatherBtn.addEventListener('click', async () => {
        const city = cityInput.value.trim();  // Get and trim the city name from the input

        // Check if the city input is empty
        if (!city) {
            alert("Please enter a city name.");  // Show an alert if no city is entered
            return;
        }

        // Fetch weather data from the Flask server
        try {
            const response = await fetch(`/get_weather?city=${city}`);
            const data = await response.json();

            // Check if there is an error (like city not found)
            if (data.error) {
                alert(data.error);  // Alert the user if an error occurs
                return;
            }

            // Display the fetched weather data
            weatherInfoDiv.innerHTML = `
                <p>City: ${data.city}, ${data.country}</p>
                <p>Temperature: ${data.temperature_celsius} °C</p>
                <p>Description: ${data.weather}</p>
                <p>Humidity: ${data.humidity}%</p>
                <p>Wind Speed: ${data.wind_speed} m/s</p>
                <p>Clouds: ${data.clouds}%</p>
            `;

            weatherInfoDiv.style.display = 'block';  // Show the weather info div

            
        } catch (error) {
            alert("Error fetching weather data.");  // Handle fetch errors
            console.error(error);
        }
    });
});
