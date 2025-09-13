import requests
import json


def fetch_tg_json(url: str, params: dict) -> dict:
    """
    HTTP GET kérés küldése az adott URL-re a paraméterekkel, és a JSON válasz feldolgozása.

    Args:
        url (str): A kérés URL-je.
        params (dict): A kéréshez tartozó paraméterek (pl. városnév, API kulcs).

    Returns:
        dict: A szerver válasza JSON formátumban. Üres szótárt ad vissza hiba esetén.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Hibát dob, ha a kérés sikertelen (pl. 404 vagy 500)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Hiba a webes lekérés során: {e}")
        return {}


def parse_tg_weather(json_obj: dict) -> tuple:
    """
    Az Open-Meteo API válaszából kinyeri a hőmérsékleti adatokat és az időpontokat.

    Args:
        json_obj (dict): A JSON válasz objektum.

    Returns:
        tuple: Egy tuple, ami két listát tartalmaz: (időpontok, hőmérsékletek).
               Üres listákat ad vissza, ha az adatok hiányoznak.
    """
    try:
        hourly_data = json_obj['hourly']
        times = [t.split('T')[1] for t in hourly_data['time']]
        temperatures = hourly_data['temperature_2m']
        return times, temperatures
    except (KeyError, IndexError) as e:
        print(f"Hiba az adatok feldolgozása során: {e}")
        return [], []


def deg_to_tg_cardinal(deg: float) -> str:
    """
    A szél irányát (fokokban) átváltja szöveges irányra (pl. É, Dny, K).

    Args:
        deg (float): A szél iránya fokban.

    Returns:
        str: A szélirány rövidítése.
    """
    if not isinstance(deg, (int, float)):
        return "N/A"

    directions = ["É", "ÉK", "K", "DK", "D", "DNy", "Ny", "ÉNy"]
    idx = int((deg / 45) + 0.5) % 8
    return directions[idx]


if __name__ == '__main__':
    # Példa a modul függvényeinek működésére
    print("Példa a deg_to_tg_cardinal() függvényre:")
    print(f"90 fok: {deg_to_tg_cardinal(90)}")
    print(f"225 fok: {deg_to_tg_cardinal(225)}")

    print("\nPélda a fetch_tg_json() és a parse_tg_weather() függvényre:")
    api_url = "https://api.open-meteo.com/v1/forecast"
    test_params = {
        'latitude': 47.4979,
        'longitude': 19.0402,
        'hourly': 'temperature_2m',
        'forecast_days': 1
    }

    data = fetch_tg_json(api_url, test_params)
    if data:
        times, temps = parse_tg_weather(data)
        if times and temps:
            print("Sikeresen lekérdezett óránkénti hőmérséklet adatok a következő 24 órára:")
            for t, temp in zip(times, temps):
                print(f"Idő: {t}, Hőmérséklet: {temp}°C")