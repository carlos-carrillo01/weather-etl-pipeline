import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from logger_config import configure_logger


logger = configure_logger(__name__)

load_dotenv()

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

CITIES = {
    "Mexico City": {"latitude": 19.4326, "longitude": -99.1332},
    "Guadalajara": {"latitude": 20.6597, "longitude": -103.3496},
}

url = "https://api.open-meteo.com/v1/forecast"


def extract_city_weather(city: str, coordinates: dict) -> dict:
    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "America/Mexico_City",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    data["city"] = city

    return data


def main() -> None:
    cities = os.getenv("CITIES", "Mexico City").split(",")

    for city in cities:
        city = city.strip()

        if city not in CITIES:
            logger.warning("City not configured: %s", city)
            continue

        logger.info("Extracting data from: %s", city)
        
        try:
            data = extract_city_weather(city, CITIES[city])
        except requests.RequestException as error:
            logger.error("Error querying API for %s: %s", city, error)
            continue


        output_file = RAW_DIR / f"{city.lower().replace(' ', '_')}_weather_raw.json"

        with output_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info("Data saved in: %s", output_file)

if __name__ == "__main__":
    main()