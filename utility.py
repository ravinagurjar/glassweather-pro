import requests
from datetime import datetime

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

# Preset coordinates for major cities to bypass cloud server geocoding blocks
COMMON_CITIES = {
    "jaipur": {"lat": 26.9124, "lon": 75.7873, "name": "Jaipur"},
    "mumbai": {"lat": 19.0760, "lon": 72.8777, "name": "Mumbai"},
    "delhi": {"lat": 28.6139, "lon": 77.2090, "name": "Delhi"},
    "new york": {"lat": 40.7128, "lon": -74.0060, "name": "New York"},
    "london": {"lat": 51.5074, "lon": -0.1278, "name": "London"},
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "name": "Tokyo"},
    "bangalore": {"lat": 12.9716, "lon": 77.5946, "name": "Bangalore"},
    "pune": {"lat": 18.5204, "lon": 73.8567, "name": "Pune"}
}

def get_weather(city_name):
    cleaned_city = city_name.strip().lower()
    lat, lon, resolved_name = None, None, city_name

    # Check if it's in our common cities fallback first (bypasses cloud blocks)
    if cleaned_city in COMMON_CITIES:
        lat = COMMON_CITIES[cleaned_city]["lat"]
        lon = COMMON_CITIES[cleaned_city]["lon"]
        resolved_name = COMMON_CITIES[cleaned_city]["name"]
    else:
        # Otherwise, try the live geocoding API
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        try:
            geo_res = requests.get(geo_url, params=geo_params, headers=headers, timeout=10).json()
            if geo_res and geo_res.get("results"):
                loc = geo_res["results"][0]
                lat = loc.get("latitude")
                lon = loc.get("longitude")
                resolved_name = loc.get("name", city_name)
        except Exception as e:
            print(f"Geocoding Error: {e}")

        if lat is None or lon is None:
            return None

    # Weather Forecast Request
    w_url = "https://api.open-meteo.com/v1/forecast"
    w_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m,visibility",
        "hourly": "temperature_2m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(w_url, params=w_params, headers=headers, timeout=10).json()
    except Exception as e:
        print(f"Weather API Error: {e}")
        return None

    if not res or "current" not in res or "daily" not in res:
        return None

    current = res["current"]
    daily = res["daily"]
    hourly = res.get("hourly", {})

    weather_code = current.get("weather_code", 0)
    w_info = WEATHER_MAP.get(weather_code, {"cond": "Mostly cloudy", "icon": "meteocons:partly-cloudy-day-fill"})

    # Process 6-Day Forecast Cards
    forecast_days = []
    daily_times = daily.get("time", [])
    
    for i in range(min(6, len(daily_times))):
        try:
            date_obj = datetime.strptime(daily_times[i], "%Y-%m-%d")
            day_str = "Today" if i == 0 else date_obj.strftime("%a")
            day_num = date_obj.strftime("%d")
            d_code = daily.get("weather_code", [0])[i]
            day_w = WEATHER_MAP.get(d_code, {"cond": "Cloudy", "icon": "meteocons:partly-cloudy-day-fill"})
            
            max_t = daily.get("temperature_2m_max", [0])[i]
            min_t = daily.get("temperature_2m_min", [0])[i]

            forecast_days.append({
                "day_num": day_num,
                "day_name": day_str,
                "max_temp": round(max_t) if max_t is not None else 0,
                "min_temp": round(min_t) if min_t is not None else 0,
                "icon": day_w["icon"]
            })
        except Exception:
            continue

    # Process Hourly Forecast Timeline
    hourly_items = []
    hourly_times = hourly.get("time", [])
    current_time_str = current.get("time")
    
    start_idx = 0
    if current_time_str and current_time_str in hourly_times:
        try:
            start_idx = hourly_times.index(current_time_str)
        except ValueError:
            start_idx = 0

    for i in range(start_idx, min(start_idx + 10, len(hourly_times)), 2):
        try:
            time_str = (
                datetime.strptime(hourly_times[i], "%Y-%m-%dT%H:%M")
                .strftime("%I %p")
                .lstrip("0")
            )
            h_code = hourly.get("weather_code", [0])[i]
            h_w = WEATHER_MAP.get(
                h_code,
                {"cond": "Cloudy", "icon": "meteocons:partly-cloudy-day-fill"},
            )
            h_temp = hourly.get("temperature_2m", [0])[i]
            hourly_items.append({
                "time": time_str,
                "temp": round(h_temp) if h_temp is not None else 0,
                "icon": h_w["icon"],
            })
        except Exception:
            continue

    temp_val = current.get("temperature_2m", 0)
    feels_val = current.get("apparent_temperature", 0)
    wind_val = current.get("wind_speed_10m", 0)
    humidity_val = current.get("relative_humidity_2m", 0)
    vis_val = current.get("visibility", 10000)
    pressure_val = current.get("surface_pressure", 1013)
    max_temp_val = daily.get("temperature_2m_max", [0])[0]

    return {
        "city": resolved_name,
        "temp": round(temp_val) if temp_val is not None else 0,
        "feels_like": round(feels_val) if feels_val is not None else 0,
        "condition": w_info["cond"],
        "icon": w_info["icon"],
        "wind": round(wind_val) if wind_val is not None else 0,
        "humidity": humidity_val if humidity_val is not None else 0,
        "visibility": round(vis_val / 1000, 1) if vis_val is not None else 10.0,
        "pressure": round(pressure_val) if pressure_val is not None else 1013,
        "time": datetime.now().strftime("%I:%M %p").lstrip("0"),
        "max_temp": round(max_temp_val) if max_temp_val is not None else 0,
        "forecast": forecast_days,
        "hourly": hourly_items
    }