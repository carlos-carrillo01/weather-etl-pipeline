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
