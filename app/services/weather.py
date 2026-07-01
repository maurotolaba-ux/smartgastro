import os

import requests


def obtener_clima():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = os.getenv("WEATHER_CITY", "Buenos Aires,AR")

    if not api_key:
        return {
            "ok": False,
            "error": "Falta OPENWEATHER_API_KEY en el archivo .env",
            "lluvia": False,
        }

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "es"}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return {
                "ok": False,
                "error": f"API de clima respondio con codigo {response.status_code}",
                "lluvia": False,
            }

        data = response.json()
        descripcion = data["weather"][0]["description"].lower()
        main = data["weather"][0]["main"].lower()
        lluvia = main == "rain" or "lluvia" in descripcion or "rain" in descripcion

        return {
            "ok": True,
            "ciudad": data.get("name", city),
            "temperatura": data["main"]["temp"],
            "descripcion": data["weather"][0]["description"],
            "lluvia": lluvia,
        }
    except requests.RequestException as exc:
        return {
            "ok": False,
            "error": f"No se pudo consultar el clima: {exc}",
            "lluvia": False,
        }
