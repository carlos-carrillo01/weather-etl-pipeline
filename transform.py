import json
from pathlib import Path

import pandas as pd

from logger_config import configure_logger

logger = configure_logger(__name__)

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "weather_clean.csv"


def load_raw_files() -> list[dict]:
    json_files = sorted(RAW_DIR.glob("*_weather_raw.json"))

    if not json_files:
        logger.error("No JSON files found in %s.", RAW_DIR)
        raise FileNotFoundError(
            f"No JSON files found in {RAW_DIR}. Run extract.py first."
        )

    raw_data_list = []

    for file_path in json_files:
        logger.info("Reading raw file: %s", file_path)

        with file_path.open("r", encoding="utf-8") as f:
            raw_data_list.append(json.load(f))

    return raw_data_list


def transform_weather_data(raw_data: dict) -> pd.DataFrame:
    daily = raw_data["daily"]
    city = raw_data["city"]

    logger.info("Transforming data for: %s", city)

    required_daily_keys = {
        "time",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
    }

    missing_keys = required_daily_keys - set(daily.keys())

    if missing_keys:
        logger.error("Missing keys in daily data for %s: %s", city, missing_keys)
        raise ValueError(f"Missing daily keys: {missing_keys}")

    df = pd.DataFrame(
        {
            "city": city,
            "date": daily["time"],
            "temp_max_c": daily["temperature_2m_max"],
            "temp_min_c": daily["temperature_2m_min"],
            "precipitation_mm": daily["precipitation_sum"],
        }
    )

    if df.empty:
        logger.error("City %s returned no data.", city)
        raise ValueError(f"City {city} returned no data.")

    # Convertir fechas antes de validar nulos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    null_counts = df[
        ["date", "temp_max_c", "temp_min_c", "precipitation_mm"]
    ].isnull().sum()

    if null_counts.any():
        logger.warning("Null values in %s: %s", city, null_counts.to_dict())

        df = df.dropna(
            subset=["date", "temp_max_c", "temp_min_c", "precipitation_mm"]
        ).reset_index(drop=True)

    duplicates = df.duplicated(subset=["date"]).sum()

    if duplicates > 0:
        logger.error("City %s has %d duplicate dates.", city, duplicates)
        raise ValueError(f"Duplicate dates in {city}.")

    invalid_temperatures = df["temp_max_c"] < df["temp_min_c"]

    if invalid_temperatures.any():
        logger.error("Invalid temperatures in %s.", city)
        raise ValueError(
            f"Maximum temperature is lower than minimum temperature in {city}."
        )

    negative_precipitation = df["precipitation_mm"] < 0

    if negative_precipitation.any():
        logger.error("Negative precipitation in %s.", city)
        raise ValueError(f"Precipitation cannot be negative in {city}.")

    logger.info("City %s produced %d valid records.", city, len(df))

    return df


def transform_all_files() -> pd.DataFrame:
    raw_data_list = load_raw_files()

    dataframes = [
        transform_weather_data(raw_data)
        for raw_data in raw_data_list
    ]

    df = pd.concat(dataframes, ignore_index=True)
    df = df.sort_values(["city", "date"]).reset_index(drop=True)

    logger.info("Combined dataset has %d records.", len(df))

    return df


def save_clean_data(df: pd.DataFrame) -> None:
    df.to_csv(OUTPUT_FILE, index=False)
    logger.info("Clean data saved to: %s", OUTPUT_FILE)


def main() -> None:
    df = transform_all_files()
    save_clean_data(df)

    logger.info("Preview:\n%s", df.head())


if __name__ == "__main__":
    main()