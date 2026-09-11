from flask import Flask, request, render_template
from utility import get_weather

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    city = "Jaipur"
    error = None

    if request.method == "POST":
        user_city = request.form.get("city")
        if user_city and user_city.strip():
            city = user_city.strip()

    # Try fetching weather for the requested city
    weather = get_weather(city)

    # If the requested city fails, fallback to Jaipur cleanly
    if weather is None:
        if city.lower() != "jaipur":
            error = f"Could not find weather for '{city}'. Showing Jaipur instead."
        
        city = "Jaipur"
        weather = get_weather(city) # FIX: Removed string quotes

        # Ultimate fallback if Open-Meteo is completely down
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