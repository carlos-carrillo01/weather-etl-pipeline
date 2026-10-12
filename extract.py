import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 19.4326,
    "longitude": -99.1332,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "America/Mexico_City"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data["daily"])
else:
    print("Error:", response.status_code)