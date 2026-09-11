from flask import Flask, request, render_template
from utility import get_weather

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    city = "Jaipur"
    error = None
    
    if request.method == "POST":
        city = request.form.get("city") or "Jaipur"

    weather = get_weather(city) # Fetch weather data
    
    # Handle case where city is invalid or API fails
    if weather is None:
        error = "City not found. Please try again."
        weather = get_weather("Jaipur") # Load default to keep page looking nice

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)