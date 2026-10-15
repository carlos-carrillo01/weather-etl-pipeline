from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

CSV_FILE = Path("data/processed/weather_clean.csv")

DB_USER = "data_engineer"
DB_PASSWORD = "secret"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "weather_db"

TABLE_NAME = "weather"


def load_clean_data(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(
            f"I couldn't find. {file_path}. Run transform.py first"
        )
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_to_postgres(df: pd.DataFrame) -> None:
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

    print(f" {len(df)} records were loaded into the table '{TABLE_NAME}'")


def main() -> None:
    df = load_clean_data(CSV_FILE)
    load_to_postgres(df)

if __name__ == "__main__":
    main()

