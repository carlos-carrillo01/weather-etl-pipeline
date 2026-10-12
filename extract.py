import json
from pathlib import Path

import requests

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 19.4326,
    "longitude": -99.1332,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "America/Mexico_City"
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

output_file = RAW_DIR / "weather_raw.json"

with output_file.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


print(f"Data saved in: {output_file}")