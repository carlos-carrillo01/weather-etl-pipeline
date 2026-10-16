# Weather Mini Pipeline

Python ETL pipeline that extracts weather data from Open-Meteo,
transforms it with pandas, and loads it into a PostgreSQL database running on Docker.

## Architecture

```text
Open-Meteo API
      ↓ extract.py
data/raw/weather_raw.json
      ↓ transform.py
data/processed/weather_clean.csv
      ↓ load.py
PostgreSQL (Docker)
      ↓ SQL
Analytical queries
```

## Technologies

- Python
- pandas
- requests
- PostgreSQL
- Docker Compose
- SQLAlchemy
- Git

## How to run it

1. Clone the repository:

```bash
git clone <your-repo>
cd weather-mini-pipeline
```

2. Create the virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Start PostgreSQL:

```bash
docker compose up -d
```

4. Run the full pipeline:

```bash
python main.py
```

5. Query the data:

```bash
docker compose exec postgres psql -U data_engineer -d weather_db
```

```sql
SELECT * FROM weather ORDER BY date;
```

## Data Model

Table: `weather`

| Column | Type | Description |
|---|---|---|
| date | timestamp | Forecast date |
| temp_max_c | float | Maximum temperature in °C |
| temp_min_c | float | Minimum temperature in °C |
| precipitation_mm | float | Accumulated precipitation in mm |

## Future Improvements

- Load data for multiple cities.
- Use environment variables for credentials.
- Add tests with pytest.
- Schedule daily execution.
- Add dbt for SQL transformations.