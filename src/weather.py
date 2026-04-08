import requests
from config.settings import WEATHER_API_KEY, WEATHER_UNITS

def get_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": WEATHER_UNITS
    }
    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        print(f"DEBUG weather API response: {data}")  # ← see exact API response

        if data.get("cod") != 200:
            msg = data.get("message", "unknown error")
            return f"Weather error: {msg}"             # ← speaks the actual error now

        temp     = data["main"]["temp"]
        feels    = data["main"]["feels_like"]
        desc     = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return (f"{city.title()} is {temp} degrees celsius, feels like {feels}, "
                f"with {desc} and {humidity} percent humidity.")

    except requests.exceptions.ConnectionError:
        return "No internet connection."
    except requests.exceptions.Timeout:
        return "Weather service timed out."
    except Exception as e:
        print(f"Weather error: {e}")
        return "Couldn't fetch weather data."