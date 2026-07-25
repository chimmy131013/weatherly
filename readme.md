Weatherly is a simple weather app made using Flask, OpenWeatherMap API, HTML, CSS, JavaScript, and Docker.

It allows users to search for a city and see the current weather, 5-day forecast, and location on an interactive map.


Features:
Search weather by city
Current temperature
Feels-like temperature
Humidity
Wind speed
5-day forecast
Weather icons
Interactive map
Dark mode
Responsive design
Docker support


Docker Commands
Build the Docker image:  docker build -t weather_app .
Run the Docker container: docker run --env-file .env -p 5000:5000 weather_app


API Key:
Create a .env file:
OPENWEATHER_API_KEY=your_api_key


Run the Project:
Install the required libraries:
pip install -r requirements.txt

Run Flask:
python app.py

Open in browser:
http://localhost:5000