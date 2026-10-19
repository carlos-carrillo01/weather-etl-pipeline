import json
from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "weather_clean.csv"


def load_raw_files() -> list[dict]:
    json_files = sorted(RAW_DIR.glob("*_weather_raw.json"))

    if not json_files:
        raise FileNotFoundError(
            f"No JSON files found in {RAW_DIR}. Run extract.py first."
        )

    raw_data_list = []

    for file_path in json_files:
        with file_path.open("r", encoding="utf-8") as f:
            raw_data_list.append(json.load(f))

    return raw_data_list


def transform_weather_data(raw_data: dict) -> pd.DataFrame:
    daily = raw_data["daily"]
    city = raw_data["city"]

    df = pd.DataFrame(
        {
            "city": city,
            "date": daily["time"],
            "temp_max_c": daily["temperature_2m_max"],
            "temp_min_c": daily["temperature_2m_min"],
            "precipitation_mm": daily["precipitation_sum"],
        }
    )

    df["date"] = pd.to_datetime(df["date"])

    if df.empty:
        raise ValueError(f"City {city} returned no data.")

    invalid_temperatures = df["temp_max_c"] < df["temp_min_c"]

    if invalid_temperatures.any():
        raise ValueError(
            f"City {city} has a maximum temperature lower than the minimum."
        )

    return df


def transform_all_files() -> pd.DataFrame:
    raw_data_list = load_raw_files()

    dataframes = [
        transform_weather_data(raw_data)
        for raw_data in raw_data_list
    ]

    df = pd.concat(dataframes, ignore_index=True)

    df = df.sort_values(["city", "date"]).reset_index(drop=True)

    return df


def save_clean_data(df: pd.DataFrame) -> None:
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Clean data saved to: {OUTPUT_FILE}")


def main() -> None:
    df = transform_all_files()
    save_clean_data(df)

    print("\nPreview:")
    print(df)


if __name__ == "__main__":
    main()