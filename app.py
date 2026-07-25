from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    forecast = None
    error = None

    if request.method == "POST":

        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."

        elif not API_KEY:
            error = "API key is missing. Check your .env file."

        else:

            # =========================
            # CURRENT WEATHER
            # =========================

            current_url = "https://api.openweathermap.org/data/2.5/weather"

            current_params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            # =========================
            # 5-DAY FORECAST
            # =========================

            forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

            forecast_params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:

                # Get current weather
                current_response = requests.get(
                    current_url,
                    params=current_params,
                    timeout=10
                )

                # Get forecast
                forecast_response = requests.get(
                    forecast_url,
                    params=forecast_params,
                    timeout=10
                )

                print(
                    "CURRENT WEATHER STATUS:",
                    current_response.status_code
                )

                print(
                    "FORECAST STATUS:",
                    forecast_response.status_code
                )


                # Check current weather
                if current_response.status_code == 200:

                    data = current_response.json()

                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temperature": round(data["main"]["temp"]),
                        "feels_like": round(data["main"]["feels_like"]),
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "description": data["weather"][0]["description"].title(),
                        "icon": data["weather"][0]["icon"],
                        "lat": data["coord"]["lat"],
                        "lon": data["coord"]["lon"]

                    }

                else:

                    error = "City not found. Please enter a valid city."


                # Check forecast
                if forecast_response.status_code == 200:

                    forecast_data = forecast_response.json()

                    forecast = []

                    # Get one forecast every 24 hours
                    # OpenWeatherMap provides data every 3 hours
                    for item in forecast_data["list"]:

                        date_text = item["dt_txt"]

                        # Select forecasts around 12 PM
                        if "12:00:00" in date_text:

                            date_object = datetime.strptime(
                                date_text,
                                "%Y-%m-%d %H:%M:%S"
                            )

                            forecast.append({

                                "date": date_object.strftime(
                                    "%a, %d %b"
                                ),

                                "temperature": round(
                                    item["main"]["temp"]
                                ),

                                "description": item["weather"][0][
                                    "description"
                                ].title(),

                                "icon": item["weather"][0]["icon"],

                                "humidity": item["main"]["humidity"],

                                "wind": item["wind"]["speed"]

                            })


            except requests.exceptions.RequestException as e:

                print("REQUEST ERROR:", e)

                error = "Could not connect to the weather service."


    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        error=error
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )