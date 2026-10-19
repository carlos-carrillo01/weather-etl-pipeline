import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from logger_config import configure_logger

logger = configure_logger(__name__)

load_dotenv()

CSV_FILE = Path("data/processed/weather_clean.csv")

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")

TABLE_NAME = "weather"


def load_clean_data(file_path: Path) -> pd.DataFrame:
    logger.info("Loading data from: %s", file_path)
    
    if not file_path.exists():
        logger.error("Could not find %s. Run transform.py first.", file_path)
        raise FileNotFoundError(
            f"Could not find {file_path}. Run transform.py first."
        )

    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])

    return df


def validate_data(df: pd.DataFrame) -> None:
    logger.info("Validating %d records before loading.", len(df))
    
    required_columns = {
        "city",
        "date",
        "temp_max_c",
        "temp_min_c",
        "precipitation_mm",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        logger.error("Missing required columns: %s", missing_columns)
        raise ValueError(f"Missing columns: {missing_columns}")

    if df.empty:
        logger.error("The CSV contains no data.")
        raise ValueError("The CSV contains no data.")

    if df[["city", "date"]].isnull().any().any():
        logger.error("There are null values in 'city' or 'date'.")
        raise ValueError("There are null values in city or date.")


def load_to_postgres(df: pd.DataFrame) -> None:
    if not all([DB_USER, DB_PASSWORD, DB_NAME]):
        logger.error("Missing environment variables. Check your .env file.")
        raise ValueError(
            "Missing environment variables. Check your .env file."
        )

    connection_string = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(connection_string)

    df.to_sql(
        name=TABLE_NAME,
        con=engine,
        if_exists="replace",
        index=False,
    )

    logger.info("Loaded %d records into table '%s'.", len(df), TABLE_NAME)


def main() -> None:
    df = load_clean_data(CSV_FILE)
    validate_data(df)
    load_to_postgres(df)


if __name__ == "__main__":
    main()