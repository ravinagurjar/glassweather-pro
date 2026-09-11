from flask import Flask, request, render_template
from utility import get_weather

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
  city = "Jaipur"
  error = None

  if request.method == "POST":
    user_city = request.form.get("city")
    if user_city:
      city = user_city.strip()

  weather = get_weather(city)  # Fetch weather data

  # Handle case where city is invalid or API fails
  if weather is None:
    error = f"Could not find weather for '{city}'. Showing Jaipur instead."
    weather = get_weather("Jaipur")

    # Ultimate fallback if even Jaipur fails for some network reason
    if weather is None:
      weather = {
          "city": "Jaipur",
          "temp": 25,
          "feels_like": 25,
          "condition": "Clear sky",
          "icon": "meteocons:clear-day-fill",
          "wind": 5,
          "humidity": 40,
          "visibility": 10.0,
          "pressure": 1013,
          "time": "12:00 PM",
          "max_temp": 30,
          "forecast": [],
          "hourly": [],
      }

  return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
  app.run(debug=True)