import requests
from datetime import datetime

# Weather Code Mapping to Condition Text & Animated Iconify Icons
WEATHER_MAP = {
    0: {"cond": "Clear sky", "icon": "meteocons:clear-day-fill"},
    1: {"cond": "Mainly clear", "icon": "meteocons:clear-day-fill"},
    2: {"cond": "Partly cloudy", "icon": "meteocons:partly-cloudy-day-fill"},
    3: {"cond": "Mostly cloudy", "icon": "meteocons:overcast-day-fill"},
    45: {"cond": "Foggy", "icon": "meteocons:fog-fill"},
    48: {"cond": "Depositing rime fog", "icon": "meteocons:fog-fill"},
    51: {"cond": "Light drizzle", "icon": "meteocons:drizzle-fill"},
    61: {"cond": "Slight rain", "icon": "meteocons:rain-fill"},
    63: {"cond": "Moderate rain", "icon": "meteocons:rain-fill"},
    65: {"cond": "Heavy rain", "icon": "meteocons:heavy-rain-fill"},
    80: {"cond": "Rain showers", "icon": "meteocons:rain-fill"},
    95: {"cond": "Thunderstorm", "icon": "meteocons:thunderstorms-fill"}
}

def get_weather(city_name):
    # Geocoding
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    geo_res = requests.get(geo_url).json()

    if not geo_res.get("results"):
        return None

    loc = geo_res["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]

    # Weather Forecast Request
    w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m,visibility&hourly=temperature_2m,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"
    res = requests.get(w_url).json()

    current = res["current"]
    daily = res["daily"]
    hourly = res["hourly"]

    w_info = WEATHER_MAP.get(current["weather_code"], {"cond": "Mostly cloudy", "icon": "meteocons:partly-cloudy-day-fill"})

    # Process 6-Day Forecast Cards
    forecast_days = []
    days_name = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    for i in range(6):
        date_obj = datetime.strptime(daily["time"][i], "%Y-%m-%d")
        day_str = "Today" if i == 0 else date_obj.strftime("%a")
        day_num = date_obj.strftime("%d")
        day_w = WEATHER_MAP.get(daily["weather_code"][i], {"cond": "Cloudy", "icon": "meteocons:partly-cloudy-day-fill"})
        
        forecast_days.append({
            "day_num": day_num,
            "day_name": day_str,
            "max_temp": round(daily["temperature_2m_max"][i]),
            "min_temp": round(daily["temperature_2m_min"][i]),
            "icon": day_w["icon"]
        })

    # Process Hourly Forecast Timeline (Next 10 hours starting from current hour)
    current_time_str = current.get("time")
    try:
        start_idx = hourly["time"].index(current_time_str)
    except (ValueError, TypeError):
        start_idx = 0

    hourly_items = []
    for i in range(start_idx, start_idx + 10, 2):
        if i >= len(hourly["time"]):
            break
        time_str = (
            datetime.strptime(hourly["time"][i], "%Y-%m-%dT%H:%M")
            .strftime("%I %p")
            .lstrip("0")
        )
        h_w = WEATHER_MAP.get(
            hourly["weather_code"][i],
            {"cond": "Cloudy", "icon": "meteocons:partly-cloudy-day-fill"},
        )
        hourly_items.append({
            "time": time_str,
            "temp": round(hourly["temperature_2m"][i]),
            "icon": h_w["icon"],
        })

    return {
        "city": loc["name"],
        "temp": round(current["temperature_2m"]),
        "feels_like": round(current["apparent_temperature"]),
        "condition": w_info["cond"],
        "icon": w_info["icon"],
        "wind": round(current["wind_speed_10m"]),
        "humidity": current["relative_humidity_2m"],
        "visibility": round(current.get("visibility", 10000) / 1000, 1),
        "pressure": round(current["surface_pressure"]),
        "time": datetime.now().strftime("%I:%M %p").lstrip("0"),
        "max_temp": round(daily["temperature_2m_max"][0]),
        "forecast": forecast_days,
        "hourly": hourly_items
    }