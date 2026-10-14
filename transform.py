import json
from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/weather_raw.json")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "weather_clean.csv"

def load_raw_data(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError (
            f"I couldn't find {file_path}. Run extract.py first"
        )

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def tranform_weather_data(raw_data: dict) -> pd.DataFrame:
    daily = raw_data["dayli"]

    df = pd.DataFrame(
        {
            "date": daily["time"],
            "temp_max_c": daily["temperature_2m_max"],
            "temp_min_c": daily["temperature_2m_min"],
            "precipitation_mm": daily["precipitation_sum"],
        }
    )

    df["date"] = pd.to_datetime(df["date"]);

    # Convert date to date type
    if df.empty:
        raise ValueError("The API didn't return data to transform")

    if df[["temp_max_c", "temp_min_c", "precipitation_mm"]].isnull().any().any():
        print("Warning: there are null values in the data")

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    return df
